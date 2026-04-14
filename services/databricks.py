"""Databricks SDK helpers: OAuth config, Spark session, WorkspaceClient, warehouses."""

from __future__ import annotations

import os
from typing import Any


def _get_oauth_config() -> Any:
    """Create a Config using only the SP's OAuth credentials.

    DATABRICKS_TOKEN must be hidden during SDK Config creation to avoid
    the 'more than one authorization method' validation error.
    """
    from databricks.sdk.core import Config

    saved_token = os.environ.pop("DATABRICKS_TOKEN", None)
    try:
        return Config()
    finally:
        if saved_token:
            os.environ["DATABRICKS_TOKEN"] = saved_token


def _get_spark() -> Any:
    """Create a serverless DatabricksConnect session."""
    from databricks.connect import DatabricksSession

    saved_token = os.environ.pop("DATABRICKS_TOKEN", None)
    try:
        spark = DatabricksSession.builder.serverless(True).getOrCreate()
    finally:
        if saved_token:
            os.environ["DATABRICKS_TOKEN"] = saved_token
    return spark


def _get_workspace_client() -> Any:
    """Create a WorkspaceClient from OAuth credentials."""
    from databricks.sdk import WorkspaceClient

    cfg = _get_oauth_config()
    return WorkspaceClient(config=cfg)


def _get_user_spark() -> Any:
    """Alias for _get_spark — Databricks Apps don't forward user tokens."""
    return _get_spark()


def _get_user_workspace_client() -> Any:
    """Alias for _get_workspace_client — Databricks Apps don't forward user tokens."""
    return _get_workspace_client()


def _list_warehouses(ws: Any = None) -> list[dict]:
    """Fetch SQL warehouses. Uses provided client or falls back to SP."""
    w = ws or _get_workspace_client()
    warehouses = []
    for wh in w.warehouses.list():
        warehouses.append({
            "id": wh.id,
            "name": wh.name,
            "state": wh.state.value if wh.state else "UNKNOWN",
            "warehouse_type": wh.warehouse_type.value if wh.warehouse_type else "UNKNOWN",
            "cluster_size": wh.cluster_size or "Unknown",
            "enable_serverless_compute": getattr(wh, "enable_serverless_compute", False),
        })
    return warehouses


def _list_serving_endpoints() -> list[dict]:
    """Fetch serving endpoints, filtering to those that support sufficient output tokens."""
    try:
        ws = _get_workspace_client()
        endpoints = []
        # Known Foundation Model API endpoints support high token counts
        _HIGH_CAPACITY_PATTERNS = ("claude", "gpt-4", "dbrx", "mixtral", "llama-3.1-70b", "llama-3.1-405b")
        for ep in ws.serving_endpoints.list():
            try:
                state_val = str(getattr(ep.state, "ready", getattr(ep.state, "value", "UNKNOWN"))) if ep.state else "UNKNOWN"
            except Exception:
                state_val = "UNKNOWN"
            name = ep.name or ""
            # Foundation Model API endpoints (databricks-*) generally support high token counts
            # Custom endpoints may have lower limits
            is_foundation = name.startswith("databricks-")
            is_high_capacity = is_foundation or any(p in name.lower() for p in _HIGH_CAPACITY_PATTERNS)
            if is_high_capacity:
                endpoints.append({
                    "name": name,
                    "state": state_val,
                    "is_foundation": is_foundation,
                })
        return endpoints
    except Exception:
        return []


def _warehouse_badge(state: str) -> tuple[str, str]:
    """Return (badge color, icon) for a warehouse state."""
    mapping = {
        "RUNNING": ("success", "fa-circle"),
        "STOPPED": ("secondary", "fa-circle"),
        "STARTING": ("warning", "fa-spinner fa-spin"),
        "STOPPING": ("warning", "fa-spinner fa-spin"),
        "DELETING": ("danger", "fa-times-circle"),
    }
    return mapping.get(state, ("secondary", "fa-question-circle"))
