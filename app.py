"""Mfg Genie Factory — Databricks App for deploying manufacturing demo Genie rooms."""

from __future__ import annotations

import logging

from app_instance import PORT, app
from layout import layout

# Register all callbacks by importing the callbacks package
import callbacks  # noqa: F401

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logger = logging.getLogger("genie-factory")

app.layout = layout

server = app.server  # Expose the Flask server for WSGI


def _bootstrap_permissions():
    """Best-effort: grant the app's SP catalog + warehouse permissions on startup."""
    try:
        from services.databricks import _get_spark, _get_workspace_client
        import state
        spark = _get_spark()
        ws = _get_workspace_client()
        sp_id = ws.config.client_id or ""
        if not sp_id:
            return

        # --- Catalog grants ---
        catalogs_to_grant = set()
        catalogs_to_grant.add(spark.sql("SELECT current_catalog()").first()[0])
        if state._META_CATALOG_ENV:
            catalogs_to_grant.add(state._META_CATALOG_ENV)
        for catalog in catalogs_to_grant:
            for stmt in [
                f"GRANT USE CATALOG ON CATALOG `{catalog}` TO `{sp_id}`",
                f"GRANT CREATE SCHEMA ON CATALOG `{catalog}` TO `{sp_id}`",
                f"GRANT ALL PRIVILEGES ON CATALOG `{catalog}` TO `{sp_id}`",
            ]:
                try:
                    spark.sql(stmt)
                except Exception:
                    pass
            logger.info("Bootstrap: SP %s permissions checked on catalog %s", sp_id[:12], catalog)

        # --- Warehouse grants (Genie space creation needs CAN_MANAGE) ---
        try:
            for wh in ws.warehouses.list():
                try:
                    ws.permissions.update(
                        "sql/warehouses",
                        wh.id,
                        access_control_list=[{
                            "service_principal_name": sp_id,
                            "permission_level": "CAN_MANAGE",
                        }],
                    )
                except Exception:
                    pass
            logger.info("Bootstrap: SP %s warehouse permissions checked", sp_id[:12])
        except Exception as e:
            logger.warning("Bootstrap warehouse grants skipped: %s", e)

        # --- Workspace directory grants (Genie registers spaces under user dirs) ---
        try:
            import requests as _req
            host = ws.config.host.rstrip("/")
            auth_headers = ws.config.authenticate()
            if callable(auth_headers):
                auth_headers = auth_headers()
            # Grant on /Users root so SP can register Genie spaces for any user
            resp = _req.get(f"{host}/api/2.0/workspace/list", headers=auth_headers, json={"path": "/"}, timeout=10)
            if resp.ok:
                for obj in resp.json().get("objects", []):
                    if obj.get("path") == "/Users":
                        users_dir_id = obj["object_id"]
                        _req.patch(
                            f"{host}/api/2.0/permissions/directories/{users_dir_id}",
                            headers=auth_headers,
                            json={"access_control_list": [{"service_principal_name": sp_id, "permission_level": "CAN_MANAGE"}]},
                            timeout=10,
                        )
                        logger.info("Bootstrap: SP %s granted CAN_MANAGE on /Users directory", sp_id[:12])
                        break
        except Exception as e:
            logger.warning("Bootstrap workspace directory grants skipped: %s", e)

    except Exception as e:
        logger.warning("Bootstrap permissions check skipped: %s", e)


def _bootstrap_backend_tables():
    """Create the metadata schema and tables at startup so callbacks don't fail."""
    try:
        from services.databricks import _get_spark
        from services.admin import _ensure_managers_table, _ensure_settings_table
        from services.deployment import _ensure_log_table
        spark = _get_spark()
        _ensure_managers_table(spark)
        _ensure_settings_table(spark)
        _ensure_log_table(spark)
        logger.info("Bootstrap: backend tables ready")
    except Exception as e:
        logger.warning("Bootstrap backend tables failed (will retry lazily): %s", e)


_bootstrap_permissions()
_bootstrap_backend_tables()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
