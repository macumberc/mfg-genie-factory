"""Genie Space Generator — deploy a Genie data room for any industry and use case."""

from __future__ import annotations

from typing import Any, Optional

from .cleanup import cleanup as _cleanup
from .config import DEFAULT_SEED
from .data import (
    build_metric_view_sqls_from_spec,
    build_table_sqls_from_spec,
    get_table_column_comments,
    get_table_descriptions,
    metric_view_fqdns,
    table_fqdns,
)
from .genie import build_genie_payload, create_or_replace_genie_space, resolve_warehouse_id
from .generator import DomainSpec, generate_domain_spec
from .results import DeploymentResult, GenieSpaceResult
from .validators import catalog_exists, current_catalog, resolve_namespace, sql_string

import logging

_logger = logging.getLogger("genie_factory")
_logger.addHandler(logging.NullHandler())

try:
    from importlib.metadata import version as _version

    __version__ = _version("genie-factory")
except Exception:
    __version__ = "0.0.0-dev"


_CATALOG_FALLBACK_ERRORS = ("PERMISSION_DENIED", "UNAUTHORIZED", "INVALID_STATE")


def _log(msg: str) -> None:
    _logger.info(msg)


def _display_html(html: str) -> None:
    try:
        import IPython  # type: ignore[import-untyped]

        ip = IPython.get_ipython()
        if ip and hasattr(ip, "user_ns") and "displayHTML" in ip.user_ns:
            ip.user_ns["displayHTML"](html)
            return
    except (ImportError, AttributeError):
        pass


def _progress(message: str, icon: str = "&#9679;") -> None:
    """Show a styled progress message, falling back to print."""
    html = _PROGRESS_HTML % {"icon": icon, "message": message}
    try:
        import IPython
        ip = IPython.get_ipython()
        if ip and hasattr(ip, "user_ns") and "displayHTML" in ip.user_ns:
            ip.user_ns["displayHTML"](html)
            return
    except (ImportError, AttributeError):
        pass
    print(f"  {message}")


def _get_spark() -> Any:
    """Get the active SparkSession, or raise if none is available."""
    try:
        from pyspark.sql import SparkSession
        session = SparkSession.getActiveSession()
        if session:
            return session
    except ImportError:
        pass
    raise RuntimeError(
        "No active SparkSession found. Run this in a Databricks notebook "
        "or pass spark= explicitly."
    )


def _explain_or_raise(spark: Any, sql: str, context: str) -> None:
    """Run EXPLAIN to validate SQL before execution.

    Catches column resolution errors early with a descriptive message.
    """
    try:
        spark.sql(f"EXPLAIN {sql}")
    except Exception as exc:
        raise RuntimeError(
            f"SQL validation failed for {context}: {exc}\n"
            f"Generated SQL (first 500 chars): {sql[:500]}"
        ) from exc



_PROGRESS_HTML = """\
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 4px 0; color: #888; font-size: 12px;">
  <span style="color: #bbb;">%(icon)s</span> %(message)s
</div>
"""

_SUMMARY_HTML = """\
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 520px; margin: 24px 0;">
  <div style="background: linear-gradient(135deg, #1B3139 0%%, #2a4a55 100%%);
              border-radius: 12px; padding: 36px 32px; color: white;
              box-shadow: 0 4px 16px rgba(0,0,0,0.2); text-align: center;">
    <div style="margin-bottom: 8px;">
      <span style="background: #00A972; display: inline-block; width: 8px; height: 8px;
                   border-radius: 50%%; vertical-align: middle; margin-right: 6px;"></span>
      <span style="font-size: 11px; color: #8fb8c8; text-transform: uppercase;
                   letter-spacing: 1.5px; font-weight: 600; vertical-align: middle;">Ready</span>
    </div>
    <div style="font-size: 22px; font-weight: 700; margin-bottom: 4px; line-height: 1.3;">
      %(company_name)s
    </div>
    <div style="font-size: 14px; color: #9bbcc8; margin-bottom: 6px;">
      %(space_title)s
    </div>
    <div style="font-size: 12px; color: #6c8793; margin-bottom: 28px;">
      %(industry)s
    </div>
    <div>%(genie_button)s</div>
  </div>
</div>
"""


def deploy(
    industry: str,
    use_case: str,
    spark: Any = None,
    catalog: Optional[str] = None,
    schema: Optional[str] = None,
    warehouse_id: Optional[str] = "auto",
    seed: int = DEFAULT_SEED,
    workspace_client: Any = None,
    deployer_email: Optional[str] = None,
    domain_spec: Optional[Any] = None,
    # LLM-only params — ignored when domain_spec is provided
    company_name: Optional[str] = None,
    business_context: Optional[str] = None,
    llm_endpoint: Optional[str] = None,
    num_tables: int = 3,
    num_products: int = 20,
    num_locations: int = 8,
) -> dict[str, Any]:
    """Deploy a custom Genie data room for any industry and use case.

    Parameters
    ----------
    industry : str
        Industry or subindustry vertical (e.g., "Automotive", "Semiconductor").
    spark : SparkSession, optional
        If omitted, the active SparkSession is used automatically
        (works in any Databricks notebook).
    use_case : str
        Short description of the analytics use case.
    catalog : str, optional
        Target catalog. Defaults to the workspace's current catalog.
    schema : str, optional
        Target schema. Defaults to ``{basename}_{username}``.
    warehouse_id : str, optional
        SQL warehouse ID for the Genie space. ``"auto"`` (default)
        auto-detects the best available warehouse. Pass ``None`` to skip
        Genie space creation.
    seed : int
        Deterministic seed for data generation.
    workspace_client : WorkspaceClient, optional
        Databricks SDK WorkspaceClient for API auth. If not provided,
        one is created from the default auth chain (works in notebooks).
    deployer_email : str, optional
        Email of the deploying user for schema scoping and telemetry.
    domain_spec : DomainSpec, optional
        Pre-generated domain specification. When provided, skips the LLM
        generation step entirely. Used by ``deploy_use_case()`` to load
        specs bundled in the package.
    company_name : str, optional
        Fictional company name. LLM-only — ignored when ``domain_spec``
        is provided.
    business_context : str, optional
        Business scenario description. LLM-only — ignored when
        ``domain_spec`` is provided.
    llm_endpoint : str, optional
        Foundation Model API endpoint. LLM-only — ignored when
        ``domain_spec`` is provided.
    num_tables : int
        Number of tables for LLM to generate (default 3). LLM-only.
    num_products : int
        Number of entity items for LLM prompt (default 20). LLM-only.
    num_locations : int
        Number of locations for LLM prompt (default 8). LLM-only.

    Returns
    -------
    dict
        Pass this dict as ``**result`` to :func:`teardown` to remove everything.
    """
    if spark is None:
        spark = _get_spark()

    _progress(f"Deploying <b>{industry}</b> &mdash; {use_case}...", "&#8942;")

    # 1. Use pre-generated spec or generate via LLM
    if domain_spec is not None:
        pass  # Pre-built spec, no LLM needed
    else:
        # Fill in defaults for optional fields
        if not company_name:
            company_name = f"a fictional {industry} company"
        if not business_context:
            business_context = (
                f"Generate a realistic business scenario for a {industry} company "
                f"focused on {use_case}. Include specific metrics, scale, and "
                f"quantified business impact."
            )

        _log(f"Generating domain model for {industry} / {company_name} ...")
        _endpoint_kwargs: dict[str, Any] = {}
        if llm_endpoint:
            _endpoint_kwargs["endpoint"] = llm_endpoint
        domain_spec = generate_domain_spec(
            spark,
            industry=industry,
            company_name=company_name,
            use_case=use_case,
            business_context=business_context,
            num_tables=num_tables,
            num_products=num_products,
            num_locations=num_locations,
            workspace_client=workspace_client,
            **_endpoint_kwargs,
        )
    # 2. Resolve namespace
    ns = resolve_namespace(
        spark,
        catalog=catalog,
        schema=schema,
        schema_basename=domain_spec.schema_basename,
        deployer_email=deployer_email,
    )

    # 3. Create catalog with permission-denied fallback
    catalog_attempted = False
    if catalog_exists(spark, ns.catalog):
        pass  # Catalog exists
    else:
        try:
            spark.sql(f"CREATE CATALOG IF NOT EXISTS {ns.catalog}")
            catalog_attempted = True
        except Exception as exc:
            msg = str(exc)
            if any(err in msg for err in _CATALOG_FALLBACK_ERRORS):
                fallback = current_catalog(spark)
                ns = resolve_namespace(
                    spark,
                    catalog=fallback,
                    schema=ns.schema,
                    schema_basename=domain_spec.schema_basename,
                    deployer_email=deployer_email,
                )
            else:
                raise

    # 4. Create schema with permission-denied fallback
    schema_comment = f"{domain_spec.company_name} {domain_spec.use_case} demo data"
    try:
        spark.sql(
            f"CREATE SCHEMA IF NOT EXISTS {ns.fqn} "
            f"COMMENT '{sql_string(schema_comment)}'"
        )
    except Exception as exc:
        msg = str(exc)
        if any(err in msg for err in _CATALOG_FALLBACK_ERRORS):
            fallback = current_catalog(spark)
            if ns.catalog != fallback:
                ns = resolve_namespace(
                    spark,
                    catalog=fallback,
                    schema=ns.schema,
                    schema_basename=domain_spec.schema_basename,
                    deployer_email=deployer_email,
                )
                spark.sql(
                    f"CREATE SCHEMA IF NOT EXISTS {ns.fqn} "
                    f"COMMENT '{sql_string(schema_comment)}'"
                )
            else:
                raise
        else:
            raise

    # Ensure SP has privileges on schema (needed when schema already exists
    # from a prior deployment where ownership was transferred to the deployer)
    if workspace_client:
        try:
            sp_id = workspace_client.config.client_id or ""
            if sp_id:
                spark.sql(f"GRANT ALL PRIVILEGES ON SCHEMA {ns.fqn} TO `{sp_id}`")
        except Exception:
            pass

    # Tag schema with deployer (ownership transfer happens after all objects are created)
    if deployer_email:
        try:
            spark.sql(f"ALTER SCHEMA {ns.fqn} SET DBPROPERTIES ('deployer_email' = '{sql_string(deployer_email)}')")
        except Exception:
            pass

    _progress("Schema ready", "&#10003;")

    # 4b. Grant deployer access to the schema (SP owns the objects, user needs SELECT)
    if deployer_email:
        try:
            esc_email = deployer_email.replace("`", "``")
            spark.sql(f"GRANT USE SCHEMA ON SCHEMA {ns.fqn} TO `{esc_email}`")
            spark.sql(f"GRANT SELECT ON SCHEMA {ns.fqn} TO `{esc_email}`")
            _logger.info("Granted schema access to deployer: %s", deployer_email)
        except Exception as exc:
            _logger.warning("Failed to grant deployer schema access (non-blocking): %s", exc)

    # 5. Build and execute CTAS statements
    _progress("Creating tables...", "&#8942;")
    sqls = build_table_sqls_from_spec(domain_spec, ns.fqn, seed, scale=3, target_rows=5000)
    tables: dict[str, int] = {}
    for name, sql in sqls.items():
        _explain_or_raise(spark, sql, f"table '{name}'")
        spark.sql(sql)
        cnt = spark.table(f"{ns.fqn}.{name}").count()
        tables[name] = cnt

    _progress("Tables created", "&#10003;")

    # (Ownership transfer moved to end of deploy, after all objects are created)

    # 6. Apply column comments
    column_comment_warnings: list[dict[str, str]] = []
    column_comments = get_table_column_comments(domain_spec)
    for table_name, cols in column_comments.items():
        for col, comment in cols.items():
            try:
                spark.sql(
                    f"ALTER TABLE {ns.fqn}.{table_name} "
                    f"ALTER COLUMN {col} COMMENT '{sql_string(comment)}'"
                )
            except Exception as exc:
                _logger.warning("Column comment for '%s.%s' failed: %s", table_name, col, exc)
                column_comment_warnings.append({
                    "category": "column_comment",
                    "name": f"{table_name}.{col}",
                    "error": str(exc),
                })
    # 6b. Apply table descriptions
    description_warnings: list[dict[str, str]] = []
    table_descriptions = get_table_descriptions(domain_spec)
    for table_name, desc in table_descriptions.items():
        try:
            spark.sql(
                f"ALTER TABLE {ns.fqn}.{table_name} "
                f"SET TBLPROPERTIES ('comment' = '{sql_string(desc)}')"
            )
        except Exception as exc:
            _logger.warning("Table description for '%s' failed: %s", table_name, exc)
            description_warnings.append({
                "category": "table_description",
                "name": table_name,
                "error": str(exc),
            })
    _progress("Metadata applied", "&#10003;")

    # 7. Create metric views
    _progress("Creating metric views...", "&#8942;")
    mv_sqls = build_metric_view_sqls_from_spec(domain_spec, ns.fqn)
    mv_failed: list[str] = []
    for mv_name, mv_sql in mv_sqls.items():
        try:
            spark.sql(mv_sql)
        except Exception as exc:
            _logger.warning("Metric view '%s' creation failed: %s", mv_name, exc)
            mv_failed.append(mv_name)
    _progress("Metric views created", "&#10003;")

    # (Ownership transfer moved to end of deploy, after all objects are created)

    _progress("Creating Genie space...", "&#8942;")

    # 8. Auto-detect warehouse
    resolved_wh, skip_reason = resolve_warehouse_id(spark, warehouse_id, workspace_client=workspace_client)

    # 9. Create/replace Genie space
    genie: GenieSpaceResult
    genie_payload_for_retry: dict | None = None
    if resolved_wh:
        # Build payload before the API call so we can store it for retry on failure
        genie_payload_for_retry = build_genie_payload(
            domain_spec, ns.fqn, resolved_wh, ns.username,
            excluded_views=set(mv_failed),
        )
        try:
            genie = create_or_replace_genie_space(
                spark, domain_spec, ns.fqn, resolved_wh, ns.username,
                excluded_views=set(mv_failed),
                workspace_client=workspace_client,
            )
            genie_payload_for_retry = None  # Success — no need to retain payload
        except Exception as exc:
            _logger.warning("Genie space creation failed: %s", exc)
            genie = GenieSpaceResult(
                status="failed", requested=True, reason=str(exc)
            )
    else:
        genie = GenieSpaceResult(
            status="skipped", requested=False, reason=skip_reason
        )

    # Exclude failed metric views from the result
    all_mv_fqdns = metric_view_fqdns(domain_spec, ns.fqn)
    active_mv_fqdns = {k: v for k, v in all_mv_fqdns.items() if k not in mv_failed}

    # Collect all warnings
    all_warnings: list[dict[str, str]] = []
    for name in mv_failed:
        all_warnings.append({"category": "metric_view", "name": name, "error": "Creation failed"})
    all_warnings.extend(column_comment_warnings)
    all_warnings.extend(description_warnings)

    # 10. Transfer ownership to deployer (done last so SP can create all objects first)
    if deployer_email:
        esc_owner = deployer_email.replace("`", "``")
        for obj_type, obj_name in (
            [("SCHEMA", ns.fqn)]
            + [("TABLE", f"{ns.fqn}.{t}") for t in tables]
            + [("VIEW", f"{ns.fqn}.{mv}") for mv in mv_sqls if mv not in mv_failed]
        ):
            try:
                spark.sql(f"ALTER {obj_type} {obj_name} SET OWNER TO `{esc_owner}`")
            except Exception:
                pass  # Best-effort — may fail if user is not a UC principal

    result = DeploymentResult(
        catalog=ns.catalog,
        schema=ns.schema,
        fqn=ns.fqn,
        seed=seed,
        schema_created=True,
        catalog_attempted=catalog_attempted,
        tables=tables,
        table_fqdns=table_fqdns(domain_spec, ns.fqn),
        metric_view_fqdns=active_mv_fqdns,
        warehouse_id=resolved_wh,
        genie=genie,
        warnings=all_warnings,
        genie_payload=genie_payload_for_retry,
    )

    # 10. Display summary
    if genie.url:
        genie_button = (
            f'<a href="{genie.url}" target="_blank" '
            f'style="display: inline-flex; align-items: center; gap: 8px; '
            f'background: #FF3621; color: white; padding: 14px 40px; '
            f'border-radius: 8px; text-decoration: none; font-size: 15px; '
            f'font-weight: 600; letter-spacing: 0.3px; '
            f'box-shadow: 0 2px 8px rgba(255,54,33,0.3);">'
            f'Open Genie Space &#8599;</a>'
        )
    else:
        genie_button = (
            '<span style="color: #6c8793; font-size: 13px; font-style: italic;">'
            'Genie space creation skipped</span>'
        )
    _progress("Done", "&#10003;")

    # Strip "CompanyName - " prefix from space title for display
    # Strip "CompanyName - " prefix from space title for display
    display_title = domain_spec.space_title
    if " - " in display_title:
        display_title = display_title.split(" - ", 1)[1]

    _display_html(
        _SUMMARY_HTML
        % {
            "company_name": domain_spec.company_name,
            "space_title": display_title,
            "industry": industry,
            "genie_button": genie_button,
        }
    )

    return result.as_dict()


def teardown(spark: Any = None, workspace_client: Any = None, **kwargs: Any) -> dict[str, Any]:
    """Remove all resources created by :func:`deploy`.

    The easiest way to call this is to unpack the dict returned by ``deploy``::

        result = deploy_use_case("Automotive", "Vehicle Recall Root Cause Analysis")
        teardown(**result)
    """
    if spark is None:
        spark = _get_spark()
    result = _cleanup(spark, deployment=kwargs, workspace_client=workspace_client)
    fqn = kwargs.get("fqn", "")
    _progress(f"Cleaned up <b>{fqn}</b>", "&#10003;")
    return result


def retry_genie_space(spark: Any, genie_payload: dict, workspace_client: Any = None) -> dict:
    """Retry Genie space creation with a pre-built payload.

    Used when a deploy partially succeeds (data created) but Genie space
    creation failed. Avoids re-running data generation.
    """
    from .genie import _api_request, _default_workspace_client

    ws = workspace_client or _default_workspace_client()
    _log("Retrying Genie space creation...")
    created = _api_request(ws, "POST", "/api/2.0/genie/spaces",
                           payload=genie_payload, expected_statuses=(200, 201))
    space_id = created.get("space_id", "")
    host = ws.config.host.rstrip("/")
    url = f"{host}/genie/rooms/{space_id}?isDbOne=true&utm_source=databricks-one" if space_id else ""
    _log(f"Genie space created: {url}")
    return {"space_id": space_id, "url": url, "status": "created"}


from .notebook import deploy_use_case, list_use_cases
from .presets import SUBINDUSTRIES, USE_CASES

__all__ = [
    "deploy",
    "teardown",
    "retry_genie_space",
    "list_use_cases",
    "deploy_use_case",
    "SUBINDUSTRIES",
    "USE_CASES",
]
