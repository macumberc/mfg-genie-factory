"""Deployment log CRUD operations (Delta table)."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from services.meta import _get_log_table, _get_meta_fqn

logger = logging.getLogger("genie-factory")


def _ensure_log_table(spark: Any) -> None:
    """Create the deployment log schema and table if they don't exist."""
    fqn = _get_meta_fqn(spark)
    log_table = _get_log_table(spark)
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {fqn}")
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {log_table} (
            deployment_id STRING COMMENT 'Unique identifier for this deployment',
            deployed_by STRING COMMENT 'Email of the user who initiated the deployment',
            deployed_at STRING COMMENT 'UTC timestamp when deployment completed',
            industry STRING COMMENT 'Industry vertical selected for the demo',
            company_name STRING COMMENT 'Fictional company name used in the demo scenario',
            use_case STRING COMMENT 'Short description of the analytics use case',
            business_context STRING COMMENT 'Full business scenario narrative',
            catalog STRING COMMENT 'Unity Catalog catalog containing the deployed schema',
            schema_name STRING COMMENT 'Schema name within the catalog',
            fqn STRING COMMENT 'Fully qualified catalog.schema name',
            warehouse_id STRING COMMENT 'SQL warehouse ID used for Genie space',
            genie_space_id STRING COMMENT 'Genie space resource ID',
            genie_space_url STRING COMMENT 'Direct URL to the Genie space',
            genie_space_title STRING COMMENT 'Display title of the Genie space',
            tables_json STRING COMMENT 'JSON map of table_name to row_count',
            total_rows LONG COMMENT 'Total rows across all tables in this deployment',
            status STRING COMMENT 'Deployment lifecycle status: active or torn_down',
            torn_down_at STRING COMMENT 'UTC timestamp when deployment was torn down'
        ) USING DELTA
        COMMENT 'Tracks all Genie Factory deployments including schema, tables, Genie spaces, and teardown status'
    """)
    # Add columns if table existed before this version
    for col, typ in [
        ("business_context", "STRING"),
        ("genie_space_title", "STRING"),
        # Phase 2 additions
        ("error_category", "STRING"),
        ("error_message", "STRING"),
        ("started_at", "STRING"),
        ("completed_at", "STRING"),
        ("warnings_json", "STRING"),
        ("deploy_params_json", "STRING"),
        # Phase 5 additions
        ("torn_down_by", "STRING"),
    ]:
        try:
            spark.sql(f"ALTER TABLE {log_table} ADD COLUMN {col} {typ}")
        except Exception:
            pass  # Column already exists
    # Apply table comment for existing tables
    try:
        spark.sql(f"ALTER TABLE {log_table} SET TBLPROPERTIES ('comment' = 'Tracks all Genie Factory deployments including schema, tables, Genie spaces, and teardown status')")
    except Exception:
        pass


def _esc(s: Any) -> str:
    """Escape a value for SQL string literals."""
    return str(s).replace("'", "''").replace("\\", "\\\\") if s else ""


def _log_deploy_start(
    spark: Any,
    deployment_id: str,
    deployer_email: str,
    industry: str,
    company_name: str,
    use_case: str,
    business_context: str,
    warehouse_id: str,
    params_json: str = "",
) -> None:
    """Write initial in_progress record at deploy start."""
    _ensure_log_table(spark)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_table = _get_log_table(spark)
    spark.sql(f"""
        INSERT INTO {log_table} (
            deployment_id, deployed_by, industry, company_name, use_case,
            business_context, warehouse_id, status, started_at, deploy_params_json
        ) VALUES (
            '{deployment_id}',
            '{_esc(deployer_email)}',
            '{_esc(industry)}',
            '{_esc(company_name)}',
            '{_esc(use_case)}',
            '{_esc(business_context)}',
            '{_esc(warehouse_id)}',
            'in_progress',
            '{now}',
            '{_esc(params_json)}'
        )
    """)


def _log_deploy_complete(
    spark: Any,
    deployment_id: str,
    status: str,
    result: Optional[dict] = None,
    error_category: Optional[str] = None,
    error_message: Optional[str] = None,
    warnings: Optional[list] = None,
) -> None:
    """Update the in_progress record with final status and results."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_table = _get_log_table(spark)

    if status in ("success", "partial") and result:
        genie = result.get("genie", {})
        if hasattr(genie, "__dict__"):
            genie = {k: v for k, v in genie.__dict__.items() if not k.startswith("_")}
        tables = result.get("tables", {})
        total_rows = sum(tables.values()) if tables else 0
        genie_title = genie.get("title", "") if isinstance(genie, dict) else ""

        set_clauses = f"""
            status = '{_esc(status)}',
            deployed_at = '{now}',
            completed_at = '{now}',
            catalog = '{_esc(result.get("catalog", ""))}',
            schema_name = '{_esc(result.get("schema", ""))}',
            fqn = '{_esc(result.get("fqn", ""))}',
            genie_space_id = '{_esc(genie.get("space_id", "") if isinstance(genie, dict) else "")}',
            genie_space_url = '{_esc(result.get("genie_url", ""))}',
            genie_space_title = '{_esc(genie_title)}',
            tables_json = '{_esc(json.dumps(tables))}',
            total_rows = {total_rows},
            warnings_json = '{_esc(json.dumps(warnings or []))}'
        """
        if error_category:
            set_clauses += f",\n            error_category = '{_esc(error_category)}'"
        if error_message:
            set_clauses += f",\n            error_message = '{_esc(error_message[:1000])}'"

        spark.sql(f"""
            UPDATE {log_table}
            SET {set_clauses}
            WHERE deployment_id = '{deployment_id}'
        """)
    else:
        # Failed deploy — only update status and error fields
        spark.sql(f"""
            UPDATE {log_table}
            SET status = 'failed',
                completed_at = '{now}',
                error_category = '{_esc(error_category or "UNKNOWN")}',
                error_message = '{_esc((error_message or "")[:1000])}'
            WHERE deployment_id = '{deployment_id}'
        """)


def _log_deployment(
    spark: Any,
    result: dict,
    industry: str,
    company_name: str,
    use_case: str,
    business_context: str,
    warehouse_id: str,
) -> str:
    """Insert a deployment record into the Delta table. Returns deployment_id."""
    _ensure_log_table(spark)
    deployment_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    genie = result.get("genie", {})
    if hasattr(genie, "__dict__"):
        genie = {k: v for k, v in genie.__dict__.items() if not k.startswith("_")}

    tables = result.get("tables", {})
    total_rows = sum(tables.values()) if tables else 0
    genie_title = genie.get("title", "") if isinstance(genie, dict) else ""

    spark.sql(f"""
        INSERT INTO {_get_log_table(spark)} VALUES (
            '{deployment_id}',
            '{_esc(result.get("username", "unknown"))}',
            '{now}',
            '{_esc(industry)}',
            '{_esc(company_name)}',
            '{_esc(use_case)}',
            '{_esc(business_context)}',
            '{_esc(result.get("catalog", ""))}',
            '{_esc(result.get("schema", ""))}',
            '{_esc(result.get("fqn", ""))}',
            '{_esc(warehouse_id)}',
            '{_esc(genie.get("space_id", "") if isinstance(genie, dict) else "")}',
            '{_esc(result.get("genie_url", ""))}',
            '{_esc(genie_title)}',
            '{_esc(json.dumps(tables))}',
            {total_rows},
            'active',
            NULL
        )
    """)
    return deployment_id


def _get_active_deployments(
    spark: Any,
    user_email: Optional[str] = None,
    is_manager: bool = False,
) -> list[dict]:
    """Fetch active deployments. Managers see all; regular users see only their own."""
    try:
        _ensure_log_table(spark)
        query = f"""
            SELECT deployment_id, deployed_by, deployed_at, industry, company_name,
                   use_case, business_context, fqn, genie_space_id, genie_space_url,
                   genie_space_title, total_rows, catalog, schema_name, tables_json
            FROM {_get_log_table(spark)}
            WHERE status IN ('active', 'success', 'partial')
        """
        if user_email and not is_manager:
            query += f" AND deployed_by = '{user_email.replace(chr(39), chr(39)+chr(39))}'"
        query += " ORDER BY deployed_at DESC"
        rows = spark.sql(query).collect()
        return [row.asDict() for row in rows]
    except Exception as e:
        logger.warning("Failed to read deployment log: %s", e)
        return []


def _mark_torn_down(spark: Any, deployment_id: str, torn_down_by: str = "") -> None:
    """Mark a deployment as torn down in the Delta table."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    torn_by_clause = f", torn_down_by = '{_esc(torn_down_by)}'" if torn_down_by else ""
    spark.sql(f"""
        UPDATE {_get_log_table(spark)}
        SET status = 'torn_down', torn_down_at = '{now}'{torn_by_clause}
        WHERE deployment_id = '{deployment_id}'
    """)
