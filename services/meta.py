"""Catalog, schema, and table FQN resolution for metadata tables."""

from __future__ import annotations

import logging
from typing import Any

import state

logger = logging.getLogger("genie-factory")


def _get_meta_catalog(spark: Any) -> str:
    """Resolve the catalog for metadata tables (deployment log, managers, settings).

    Verifies the SP has actual access (USE CATALOG), not just that the catalog
    exists in the metastore.  Falls back to current_catalog() on permission errors.
    """
    if state._meta_catalog_cache:
        return state._meta_catalog_cache
    if state._META_CATALOG_ENV:
        accessible = False
        try:
            spark.sql(f"USE CATALOG {state._META_CATALOG_ENV}")
            accessible = True
        except Exception:
            pass
        if accessible:
            state._meta_catalog_cache = state._META_CATALOG_ENV
        else:
            fallback = spark.sql("SELECT current_catalog()").first()[0]
            logger.warning(
                "Catalog '%s' is not accessible (missing USE CATALOG). "
                "Falling back to workspace default: '%s'",
                state._META_CATALOG_ENV, fallback,
            )
            state._meta_catalog_cache = fallback
    else:
        state._meta_catalog_cache = spark.sql("SELECT current_catalog()").first()[0]
    return state._meta_catalog_cache


def _get_meta_fqn(spark: Any) -> str:
    """Return the fully-qualified schema for metadata tables."""
    return f"{_get_meta_catalog(spark)}.{state._META_SCHEMA}"


def _get_log_table(spark: Any) -> str:
    return f"{_get_meta_fqn(spark)}.deployment_log"


def _get_managers_table(spark: Any) -> str:
    return f"{_get_meta_fqn(spark)}.app_managers"


def _get_settings_table(spark: Any) -> str:
    return f"{_get_meta_fqn(spark)}.app_settings"
