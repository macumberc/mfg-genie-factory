"""Admin management: managers CRUD, settings CRUD, workspace user listing."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Optional

import state
from services.databricks import _get_workspace_client
from services.meta import _get_managers_table, _get_meta_fqn, _get_settings_table

logger = logging.getLogger("genie-factory")


def _ensure_managers_table(spark: Any) -> None:
    fqn = _get_meta_fqn(spark)
    mgr_table = _get_managers_table(spark)
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {fqn}")
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {mgr_table} (
            email STRING COMMENT 'Email of the app manager',
            role STRING COMMENT 'Role assignment: manager',
            added_by STRING COMMENT 'Email of the admin who granted this role',
            added_at STRING COMMENT 'UTC timestamp when the role was granted'
        ) USING DELTA
        COMMENT 'Genie Factory application managers with elevated permissions'
    """)
    # Auto-bootstrap: if no managers exist, add the current user as first manager
    try:
        count = spark.sql(f"SELECT COUNT(*) FROM {mgr_table}").first()[0]
        if count == 0:
            from flask import request
            email = request.headers.get("x-forwarded-email", "")
            if email:
                now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                esc_email = email.replace("'", "''")
                spark.sql(f"""
                    MERGE INTO {mgr_table} AS t
                    USING (SELECT '{esc_email}' AS email) AS s ON t.email = s.email
                    WHEN NOT MATCHED THEN INSERT (email, role, added_by, added_at)
                    VALUES (s.email, 'manager', 'auto-bootstrap', '{now}')
                """)
                logger.info("Auto-bootstrapped first manager: %s", email)
    except Exception as e:
        logger.warning("Manager auto-bootstrap check failed: %s", e)


def _ensure_settings_table(spark: Any) -> None:
    fqn = _get_meta_fqn(spark)
    settings_table = _get_settings_table(spark)
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {fqn}")
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {settings_table} (
            setting_key STRING COMMENT 'Configuration key name',
            setting_value STRING COMMENT 'Configuration value (JSON or plain text)',
            updated_by STRING COMMENT 'Email of the admin who last updated this setting',
            updated_at STRING COMMENT 'UTC timestamp of last update'
        ) USING DELTA
        COMMENT 'Genie Factory app-wide configuration settings managed by admins'
    """)


def _ensure_first_admin(spark: Any, email: str) -> None:
    """Ensure at least one admin exists."""
    if not email:
        return
    try:
        _ensure_managers_table(spark)
        mgr_table = _get_managers_table(spark)
        esc = email.replace("'", "''")
        already = spark.sql(f"SELECT COUNT(*) FROM {mgr_table} WHERE email = '{esc}'").first()[0]
        if already > 0:
            return
        total = spark.sql(f"SELECT COUNT(*) FROM {mgr_table}").first()[0]
        if total == 0:
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            spark.sql(f"""
                MERGE INTO {mgr_table} AS t
                USING (SELECT '{esc}' AS email) AS s ON t.email = s.email
                WHEN NOT MATCHED THEN INSERT (email, role, added_by, added_at)
                VALUES (s.email, 'manager', 'auto-bootstrap', '{now}')
            """)
            logger.info("Auto-bootstrapped first admin: %s", email)
    except Exception as e:
        logger.warning("_ensure_first_admin failed: %s", e)


def _is_manager(spark: Any, email: str) -> bool:
    if not email:
        return False
    try:
        _ensure_managers_table(spark)
        count = spark.sql(f"""
            SELECT COUNT(*) as cnt FROM {_get_managers_table(spark)}
            WHERE email = '{email.replace("'", "''")}'
        """).first()["cnt"]
        return count > 0
    except Exception as e:
        logger.warning("Failed to check manager status: %s", e)
        return False


def _get_managers(spark: Any) -> list[dict]:
    try:
        _ensure_managers_table(spark)
        rows = spark.sql(f"SELECT * FROM {_get_managers_table(spark)} ORDER BY added_at DESC").collect()
        return [row.asDict() for row in rows]
    except Exception as e:
        logger.warning("Failed to get managers: %s", e)
        return []


def _add_manager(spark: Any, email: str, added_by: str) -> None:
    _ensure_managers_table(spark)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    spark.sql(f"""
        MERGE INTO {_get_managers_table(spark)} AS t
        USING (SELECT '{email.replace("'", "''")}' AS email) AS s
        ON t.email = s.email
        WHEN NOT MATCHED THEN INSERT (email, role, added_by, added_at)
        VALUES (s.email, 'manager', '{added_by.replace("'", "''")}', '{now}')
    """)


def _remove_manager(spark: Any, email: str) -> None:
    _ensure_managers_table(spark)
    spark.sql(f"DELETE FROM {_get_managers_table(spark)} WHERE email = '{email.replace(chr(39), chr(39)+chr(39))}'")


def _get_setting(spark: Any, key: str) -> Optional[str]:
    try:
        _ensure_settings_table(spark)
        row = spark.sql(f"""
            SELECT setting_value FROM {_get_settings_table(spark)}
            WHERE setting_key = '{key.replace("'", "''")}'
        """).first()
        return row["setting_value"] if row else None
    except Exception:
        return None


def _set_setting(spark: Any, key: str, value: str, updated_by: str) -> None:
    _ensure_settings_table(spark)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    esc_key = key.replace("'", "''")
    esc_val = value.replace("'", "''")
    esc_by = updated_by.replace("'", "''")
    spark.sql(f"""
        MERGE INTO {_get_settings_table(spark)} AS t
        USING (SELECT '{esc_key}' AS setting_key) AS s
        ON t.setting_key = s.setting_key
        WHEN MATCHED THEN UPDATE SET setting_value = '{esc_val}', updated_by = '{esc_by}', updated_at = '{now}'
        WHEN NOT MATCHED THEN INSERT (setting_key, setting_value, updated_by, updated_at)
        VALUES ('{esc_key}', '{esc_val}', '{esc_by}', '{now}')
    """)


def _ensure_audit_table(spark: Any) -> None:
    """Create the audit log table if it doesn't exist."""
    fqn = _get_meta_fqn(spark)
    audit_table = f"{fqn}.audit_log"
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {fqn}")
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {audit_table} (
            event_id STRING,
            event_type STRING COMMENT 'teardown, manager_added, manager_removed, policy_change',
            actor_email STRING,
            target_deployment_id STRING,
            target_email STRING,
            details STRING COMMENT 'JSON with extra context',
            event_at STRING
        ) USING DELTA
        COMMENT 'Audit trail for Genie Factory admin actions'
    """)


def _log_audit_event(
    spark: Any,
    event_type: str,
    actor_email: str,
    target_deployment_id: str = "",
    target_email: str = "",
    details: str = "",
) -> None:
    """Log an audit event (best effort)."""
    import uuid as _uuid
    try:
        _ensure_audit_table(spark)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        event_id = str(_uuid.uuid4())
        fqn = _get_meta_fqn(spark)
        esc = lambda s: str(s).replace("'", "''") if s else ""
        spark.sql(f"""
            INSERT INTO {fqn}.audit_log VALUES (
                '{event_id}', '{esc(event_type)}', '{esc(actor_email)}',
                '{esc(target_deployment_id)}', '{esc(target_email)}',
                '{esc(details)}', '{now}'
            )
        """)
    except Exception as e:
        logger.warning("Failed to log audit event: %s", e)


def _get_recent_activity(spark: Any, limit: int = 50) -> list[dict]:
    """Fetch recent audit events."""
    try:
        _ensure_audit_table(spark)
        fqn = _get_meta_fqn(spark)
        rows = spark.sql(f"SELECT * FROM {fqn}.audit_log ORDER BY event_at DESC LIMIT {limit}").collect()
        return [r.asDict() for r in rows]
    except Exception as e:
        logger.warning("Failed to get audit events: %s", e)
        return []


def _get_deployment_analytics(spark: Any, days: int = 30) -> dict:
    """Query deployment_log for analytics summary."""
    from services.meta import _get_log_table
    try:
        log_table = _get_log_table(spark)
        where = f"WHERE started_at >= date_sub(current_date(), {days})" if days > 0 else ""

        summary = spark.sql(f"""
            SELECT
                COUNT(*) as total_deploys,
                SUM(CASE WHEN status IN ('active', 'success', 'partial') THEN 1 ELSE 0 END) as active_count,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count,
                SUM(CASE WHEN status = 'torn_down' THEN 1 ELSE 0 END) as torn_down_count
            FROM {log_table} {where}
        """).first().asDict()

        per_user = [r.asDict() for r in spark.sql(f"""
            SELECT deployed_by, COUNT(*) as cnt
            FROM {log_table} {where}
            GROUP BY deployed_by ORDER BY cnt DESC LIMIT 20
        """).collect()]

        per_industry = [r.asDict() for r in spark.sql(f"""
            SELECT industry, COUNT(*) as cnt
            FROM {log_table} {where}
            GROUP BY industry ORDER BY cnt DESC
        """).collect()]

        return {"summary": summary, "per_user": per_user, "per_industry": per_industry}
    except Exception as e:
        logger.warning("Failed to get analytics: %s", e)
        return {"summary": {}, "per_user": [], "per_industry": []}


def _list_workspace_users() -> list[dict]:
    """Fetch workspace users from SCIM API with caching and timeout."""
    import concurrent.futures
    now = time.time()
    if state._workspace_users_cache["users"] and (now - state._workspace_users_cache["fetched_at"]) < state._USERS_CACHE_TTL:
        return state._workspace_users_cache["users"]

    def _fetch():
        ws = _get_workspace_client()
        users = []
        for u in ws.users.list(count=500):
            email = ""
            if u.emails:
                for e in u.emails:
                    if e.primary:
                        email = e.value
                        break
                if not email:
                    email = u.emails[0].value
            display_name = u.display_name or (email.split("@")[0] if email else "")
            if email:
                users.append({"email": email, "display_name": display_name})
        users.sort(key=lambda x: x["display_name"].lower())
        return users

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_fetch)
            users = future.result(timeout=15)  # 15 second timeout
        state._workspace_users_cache["users"] = users
        state._workspace_users_cache["fetched_at"] = now
        return users
    except concurrent.futures.TimeoutError:
        logger.warning("SCIM user list timed out after 15s")
        return state._workspace_users_cache.get("users", [])
    except Exception as e:
        logger.warning("Failed to list workspace users: %s", e)
        return state._workspace_users_cache.get("users", [])
