"""Centralized mutable state shared across modules."""

import os
import time
import threading
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Configuration (read from environment once at import time)
# ---------------------------------------------------------------------------

_META_CATALOG_ENV = os.environ.get("GENIE_FACTORY_CATALOG", "")  # empty = auto-detect
_META_SCHEMA = os.environ.get("GENIE_FACTORY_SCHEMA", "genie_factory")
_ADMIN_CONTACT_EMAIL = os.environ.get("GENIE_FACTORY_ADMIN_EMAIL", "")

_meta_catalog_cache: Optional[str] = None

# ---------------------------------------------------------------------------
# Deploy progress tracking (thread-safe)
# ---------------------------------------------------------------------------

_deploy_progress: dict[str, list[str]] = {}
_deploy_results: dict[str, dict] = {}
_deploy_lock = threading.Lock()
_deploy_step: dict[str, str] = {}  # session_id -> current step ID
_deploy_start_time: dict[str, float] = {}  # session_id -> start timestamp


def _set_step(session_id: str, step_id: str) -> None:
    with _deploy_lock:
        _deploy_step[session_id] = step_id


def _get_step(session_id: str) -> str:
    with _deploy_lock:
        return _deploy_step.get(session_id, "")


def _set_progress(session_id: str, message: str) -> None:
    with _deploy_lock:
        _deploy_progress.setdefault(session_id, []).append(message)


def _get_progress(session_id: str) -> list[str]:
    with _deploy_lock:
        return list(_deploy_progress.get(session_id, []))


def _set_deploy_result(session_id: str, result: dict) -> None:
    with _deploy_lock:
        _deploy_results[session_id] = result


def _get_deploy_result(session_id: str) -> Optional[dict]:
    with _deploy_lock:
        return _deploy_results.get(session_id)


def _cleanup_session(session_id: str) -> None:
    with _deploy_lock:
        _deploy_progress.pop(session_id, None)
        _deploy_results.pop(session_id, None)
        _deploy_step.pop(session_id, None)
        _deploy_start_time.pop(session_id, None)

# ---------------------------------------------------------------------------
# Workspace users cache
# ---------------------------------------------------------------------------

_workspace_users_cache: dict[str, Any] = {"users": [], "fetched_at": 0.0}
_USERS_CACHE_TTL = 300  # 5 minutes
