"""Build tab callbacks: Quick Deploy, Custom Build, warehouse management, progress tracking."""

from __future__ import annotations

import json
import logging
import threading
import time
import traceback
import uuid
from typing import Any, Optional

import dash
import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, State, callback, ctx, html, no_update, clientside_callback

import genie_factory
from genie_factory.specs import load_spec

from services.databricks import (
    _get_spark,
    _get_workspace_client,
    _get_user_spark,
    _get_user_workspace_client,
    _list_warehouses,
    _warehouse_badge,
)
from services.deployment import _log_deployment, _log_deploy_start, _log_deploy_complete
from services.admin import _is_manager, _get_setting, _ensure_first_admin
from components.cards import _build_success_card, _build_error_card, _serialize_result
from state import (
    _set_progress,
    _get_progress,
    _set_deploy_result,
    _get_deploy_result,
    _cleanup_session,
    _set_step,
    _get_step,
    _deploy_start_time,
    _deploy_lock,
)
from presets import (
    SUBINDUSTRIES,
    SUBINDUSTRY_USE_CASES,
    SUBINDUSTRY_ICONS,
    DATASET_SIZE_PRESETS,
    DATASET_SIZE_ESTIMATES,
)

logger = logging.getLogger("genie-factory")

# ---------------------------------------------------------------------------
# Deploy step definitions
# ---------------------------------------------------------------------------

DEPLOY_STEPS = [
    {"id": "connect",   "label": "Connecting",      "avg_seconds": 8},
    {"id": "generate",  "label": "Loading Spec",    "avg_seconds": 3},
    {"id": "namespace", "label": "Setting Up",      "avg_seconds": 12},
    {"id": "deploying", "label": "Deploying",       "avg_seconds": 50},
]

STEP_IDS = [s["id"] for s in DEPLOY_STEPS]

# ---------------------------------------------------------------------------
# Error categories
# ---------------------------------------------------------------------------

ERROR_CATEGORIES = {
    "LLM_GENERATION": {
        "label": "LLM Generation",
        "icon": "fa-brain",
        "description": "The AI model failed to generate a valid domain specification.",
        "suggestions": [
            "Try a different LLM endpoint if available.",
            "Simplify the business context description.",
            "Retry -- transient model errors are common.",
        ],
    },
    "SQL_EXECUTION": {
        "label": "SQL Execution",
        "icon": "fa-database",
        "description": "A SQL statement failed during table or view creation.",
        "suggestions": [
            "Ensure your SQL warehouse is running.",
            "Check Unity Catalog permissions on the target catalog/schema.",
            "Retry -- warehouse may have been warming up.",
        ],
    },
    "GENIE_API": {
        "label": "Genie API",
        "icon": "fa-robot",
        "description": "The Genie Space REST API returned an error.",
        "suggestions": [
            "The API may be rate-limited. Wait 30 seconds and retry.",
            "Ensure the warehouse is RUNNING before deploying.",
            "Check if you have permission to create Genie spaces.",
        ],
    },
    "PERMISSIONS": {
        "label": "Permissions",
        "icon": "fa-lock",
        "description": "Insufficient permissions to create resources.",
        "suggestions": [
            "Verify you have CREATE SCHEMA on the target catalog.",
            "Ask your workspace admin for broader permissions.",
            "Try deploying to the default catalog.",
        ],
    },
    "WAREHOUSE": {
        "label": "Warehouse",
        "icon": "fa-server",
        "description": "Could not connect to or use the SQL warehouse.",
        "suggestions": [
            "Start the warehouse before deploying.",
            "Select a different warehouse.",
            "Create a new serverless warehouse.",
        ],
    },
    "UNKNOWN": {
        "label": "Unknown Error",
        "icon": "fa-question-circle",
        "description": "An unexpected error occurred.",
        "suggestions": [
            "Check the error details below for clues.",
            "Retry the deployment.",
            "Contact your workspace admin if the issue persists.",
        ],
    },
}


def _categorize_error(error_msg: str) -> str:
    """Classify an error message into a category."""
    msg = error_msg.lower()
    if any(kw in msg for kw in ("llm", "generation", "endpoint", "model", "max_tokens", "json", "parse")):
        return "LLM_GENERATION"
    if any(kw in msg for kw in ("sql", "table", "column", "schema", "ctas", "explain", "resolution")):
        return "SQL_EXECUTION"
    if any(kw in msg for kw in ("genie", "space", "429", "rate limit", "/api/2.0/genie")):
        return "GENIE_API"
    if any(kw in msg for kw in ("permission", "denied", "unauthorized", "forbidden", "privilege")):
        return "PERMISSIONS"
    if any(kw in msg for kw in ("warehouse", "cluster", "compute", "stopped", "starting")):
        return "WAREHOUSE"
    return "UNKNOWN"


def _estimate_deploy_minutes(params: dict) -> int:
    """Estimate total deploy time in minutes."""
    is_preset = bool(params.get("domain_spec_subindustry"))
    if is_preset:
        return 2
    num_tables = params.get("num_tables", 3)
    target_rows = params.get("target_rows", 5000)
    base = 3
    if target_rows and int(target_rows) > 10000:
        base += 2
    if num_tables and int(num_tables) > 3:
        base += 1
    return base


# ---------------------------------------------------------------------------
# Logger interceptor -- map genie_factory log messages to step IDs
# ---------------------------------------------------------------------------

_STEP_PATTERNS = {
    "connect": ["connect", "session", "workspace"],
    "generate": ["loading spec", "loaded spec", "generating", "domain"],
    "namespace": ["schema ready", "schema", "namespace", "catalog"],
    "deploying": ["creating table", "table", "ctas", "rows", "metadata", "comment",
                   "metric view", "metric", "genie space", "genie", "warehouse",
                   "tag", "description", "view"],
}


class _DeployLogHandler(logging.Handler):
    """Intercepts genie_factory logger to capture progress messages.

    Step transitions are handled by explicit _set_step() calls in the
    deploy thread — the handler only logs messages, it does NOT change steps.
    """

    def __init__(self, session_id: str) -> None:
        super().__init__()
        self.session_id = session_id

    def emit(self, record: logging.LogRecord) -> None:
        _set_progress(self.session_id, record.getMessage())


# ---------------------------------------------------------------------------
# Background deploy thread
# ---------------------------------------------------------------------------

def _run_deploy_in_thread(session_id: str, params: dict, user_spark: Any = None, user_ws: Any = None) -> None:
    """Execute deployment in a background thread. Stores result in state.

    user_spark and user_ws are OBO-authenticated clients created in the
    calling callback (while Flask request context is still available).
    Falls back to SP auth if not provided.
    """
    handler = _DeployLogHandler(session_id)
    gf_logger = logging.getLogger("genie_factory")
    gf_logger.addHandler(handler)
    gf_logger.setLevel(logging.INFO)

    deployment_id = str(uuid.uuid4())
    spark = None
    ws = None

    try:
        # -- Step: connect --
        _set_step(session_id, "connect")
        _set_progress(session_id, "Establishing Spark session...")
        spark = user_spark or _get_spark()
        ws = user_ws or _get_workspace_client()

        deployer_email = params.get("deployer_email", "")
        _set_progress(session_id, f"Connected as {deployer_email or 'service principal'}")
        warehouse_id = params.get("warehouse_id", "auto")

        # Log deploy start (best-effort)
        try:
            _log_deploy_start(
                spark,
                deployment_id=deployment_id,
                deployer_email=deployer_email,
                industry=params.get("industry", ""),
                company_name=params.get("company_name", ""),
                use_case=params.get("use_case", ""),
                business_context=params.get("business_context", ""),
                warehouse_id=warehouse_id,
                params_json=json.dumps(
                    {k: v for k, v in params.items() if k != "domain_spec"},
                    default=str,
                ),
            )
        except Exception as e:
            logger.warning("Failed to log deploy start: %s", e)

        # Audit: deploy_started (best-effort)
        try:
            from services.admin import _log_audit_event
            _log_audit_event(spark, "deploy_started", deployer_email, details=f"Quick Deploy: {params.get('industry', '')} / {params.get('use_case', '')}")
        except Exception:
            pass

        # -- Step: generate / load spec --
        _set_step(session_id, "generate")

        is_preset = bool(params.get("domain_spec_subindustry"))

        if is_preset:
            # Quick Deploy: load pre-built spec from package
            _set_progress(session_id, "Loading pre-built spec...")
            spec_sub = params["domain_spec_subindustry"]
            spec_label = params["domain_spec_label"]
            spec = load_spec(spec_sub, spec_label)
            if spec is None:
                raise RuntimeError(
                    f"Pre-built spec not found for {spec_sub} / {spec_label}. "
                    f"This use case may require a Custom Build."
                )
            _set_progress(session_id, f"Loaded spec: {spec.company_name} — {len(spec.tables)} tables, {len(spec.metric_views)} metric views")

            _set_step(session_id, "namespace")
            _set_progress(session_id, f"Setting up schema for {spec.company_name}...")

            _set_step(session_id, "deploying")
            _set_progress(session_id, f"Deploying tables, metrics, and Genie space...")

            result = genie_factory.deploy(
                industry=spec_sub,
                use_case=params.get("use_case", spec.use_case),
                spark=spark,
                domain_spec=spec,
                warehouse_id=warehouse_id,
                workspace_client=ws,
                deployer_email=deployer_email,
            )
        else:
            # Custom Build: LLM-based generation
            _set_progress(session_id, "Generating domain spec via LLM...")

            deploy_kwargs: dict[str, Any] = {
                "industry": params.get("industry", "Manufacturing"),
                "use_case": params.get("use_case", ""),
                "spark": spark,
                "company_name": params.get("company_name"),
                "business_context": params.get("business_context"),
                "num_tables": params.get("num_tables", 3),
                "num_products": params.get("num_products", 20),
                "num_locations": params.get("num_locations", 8),
                "warehouse_id": warehouse_id,
                "workspace_client": ws,
                "deployer_email": deployer_email,
            }

            catalog = params.get("catalog")
            if catalog:
                deploy_kwargs["catalog"] = catalog
            schema = params.get("schema")
            if schema:
                deploy_kwargs["schema"] = schema

            llm_endpoint = params.get("llm_endpoint")
            if llm_endpoint:
                deploy_kwargs["llm_endpoint"] = llm_endpoint

            _set_step(session_id, "namespace")
            _set_progress(session_id, f"Setting up schema...")

            _set_step(session_id, "deploying")
            _set_progress(session_id, f"Deploying tables, metrics, and Genie space...")

            result = genie_factory.deploy(**deploy_kwargs)

        # -- Deployment succeeded --
        serialized = _serialize_result(result)
        serialized["deployment_id"] = deployment_id
        serialized["_deploy_mode"] = "quick" if is_preset else "custom"

        # Log deploy complete (best-effort)
        try:
            warnings = result.get("warnings", [])
            genie = result.get("genie", {})
            genie_status = genie.get("status", "") if isinstance(genie, dict) else ""
            if genie_status == "failed":
                _log_deploy_complete(spark, deployment_id, "partial", result=result, warnings=warnings)
            else:
                _log_deploy_complete(spark, deployment_id, "success", result=result, warnings=warnings)
        except Exception as e:
            logger.warning("Failed to log deploy complete: %s", e)

        # Audit: deploy_completed (best-effort)
        try:
            from services.admin import _log_audit_event
            _log_audit_event(spark, "deploy_completed", deployer_email, target_deployment_id=deployment_id, details=f"Deployed {result.get('fqn', '')}")
        except Exception:
            pass

        _set_step(session_id, "done")
        _set_deploy_result(session_id, {"status": "success", "result": serialized})

    except Exception as exc:
        error_msg = str(exc)
        error_tb = traceback.format_exc()
        category = _categorize_error(error_msg)
        logger.error("Deploy failed [%s]: %s\n%s", category, error_msg, error_tb)

        # Log deploy failure (best-effort)
        if spark:
            try:
                _log_deploy_complete(
                    spark, deployment_id, "failed",
                    error_category=category,
                    error_message=error_msg[:1000],
                )
            except Exception:
                pass

        # Audit: deploy_failed (best-effort)
        try:
            from services.admin import _log_audit_event
            _log_audit_event(spark, "deploy_failed", deployer_email, details=str(error_msg)[:500])
        except Exception:
            pass

        _set_deploy_result(session_id, {
            "status": "error",
            "error": error_msg,
            "error_traceback": error_tb,
            "error_category": category,
            "deployment_id": deployment_id,
            "params": {k: v for k, v in params.items() if k != "domain_spec"},
        })

    finally:
        gf_logger.removeHandler(handler)


# ---------------------------------------------------------------------------
# Step progress bar builder
# ---------------------------------------------------------------------------

def _build_step_bar(current_step: str, session_id: str) -> html.Div:
    """Build a visual progress bar showing deploy steps."""
    steps = DEPLOY_STEPS
    current_idx = -1
    for i, s in enumerate(steps):
        if s["id"] == current_step:
            current_idx = i
            break
    if current_step == "done":
        current_idx = len(steps)

    # Calculate elapsed time
    with _deploy_lock:
        start_ts = _deploy_start_time.get(session_id, 0)
    elapsed = int(time.time() - start_ts) if start_ts else 0
    elapsed_str = f"{elapsed // 60}:{elapsed % 60:02d}" if elapsed else "0:00"

    step_items = []
    for i, step in enumerate(steps):
        if i < current_idx:
            # Completed
            icon = html.I(className="fas fa-check-circle", style={"color": "#00A972", "fontSize": "1.1rem"})
            label_style = {"color": "#00A972", "fontWeight": "600", "fontSize": "0.75rem"}
        elif i == current_idx:
            # Active
            icon = html.I(className="fas fa-spinner fa-spin", style={"color": "#FF3621", "fontSize": "1.1rem"})
            label_style = {"color": "#FF3621", "fontWeight": "700", "fontSize": "0.75rem"}
        else:
            # Pending
            icon = html.I(className="far fa-circle", style={"color": "#6C757D", "fontSize": "1.1rem"})
            label_style = {"color": "#6C757D", "fontSize": "0.75rem"}

        step_items.append(
            html.Div([
                icon,
                html.Div(step["label"], style=label_style, className="mt-1"),
            ], className="text-center", style={"flex": "1", "minWidth": "80px"})
        )

        # Connector line between steps
        if i < len(steps) - 1:
            connector_color = "#00A972" if i < current_idx else "#DEE2E6"
            step_items.append(
                html.Div(style={
                    "flex": "1",
                    "height": "2px",
                    "backgroundColor": connector_color,
                    "alignSelf": "center",
                    "marginTop": "-0.75rem",
                    "minWidth": "20px",
                    "maxWidth": "60px",
                })
            )

    # Percentage estimate
    if current_idx >= len(steps):
        pct = 100
    elif current_idx >= 0:
        total_avg = sum(s["avg_seconds"] for s in steps)
        done_avg = sum(steps[i]["avg_seconds"] for i in range(current_idx))
        pct = min(int((done_avg / total_avg) * 100), 99)
    else:
        pct = 0

    return html.Div([
        html.Div(step_items, className="d-flex align-items-start justify-content-between mb-3"),
        dbc.Progress(
            value=pct,
            striped=True,
            animated=True if current_step != "done" else False,
            color="success" if current_step == "done" else "primary",
            className="mb-2",
            style={"height": "6px"},
        ),
        html.Div([
            html.Small(f"{pct}%", className="text-muted-brand"),
            html.Small(f"Elapsed: {elapsed_str}", className="text-muted-brand ms-3"),
        ], className="d-flex"),
    ])


# ---------------------------------------------------------------------------
# Error card builder
# ---------------------------------------------------------------------------

def _build_categorized_error_card(
    error_msg: str,
    error_category: str,
    error_tb: str = "",
    params: Optional[dict] = None,
) -> dbc.Card:
    """Build a detailed error card with category info and suggestions."""
    cat_info = ERROR_CATEGORIES.get(error_category, ERROR_CATEGORIES["UNKNOWN"])

    suggestion_items = [html.Li(s) for s in cat_info["suggestions"]]

    body_children = [
        html.Div([
            html.I(className=f"fas {cat_info['icon']} me-2", style={"color": "#DC3545", "fontSize": "1.2rem"}),
            html.Span(cat_info["label"], style={"fontWeight": "700", "fontSize": "1.1rem", "color": "#DC3545"}),
        ], className="mb-2"),
        html.P(cat_info["description"], className="text-muted-brand mb-3"),
        html.Div([
            html.Strong("What to try:", className="d-block mb-1"),
            html.Ul(suggestion_items, style={"paddingLeft": "1.25rem", "marginBottom": "0"}),
        ], className="mb-3", style={"background": "#F8F9FA", "padding": "1rem", "borderRadius": "8px"}),
        html.Details([
            html.Summary("Error details", style={"cursor": "pointer", "fontSize": "0.85rem", "color": "#6C757D"}),
            html.Pre(
                error_msg,
                style={
                    "background": "#1B3139",
                    "color": "#F8F9FA",
                    "padding": "1rem",
                    "borderRadius": "8px",
                    "fontSize": "0.8rem",
                    "whiteSpace": "pre-wrap",
                    "maxHeight": "200px",
                    "overflowY": "auto",
                    "marginTop": "0.5rem",
                },
            ),
        ]),
    ]

    if error_tb:
        body_children.append(
            html.Details([
                html.Summary("Full traceback", style={"cursor": "pointer", "fontSize": "0.85rem", "color": "#6C757D", "marginTop": "0.5rem"}),
                html.Pre(
                    error_tb,
                    style={
                        "background": "#1B3139",
                        "color": "#F8F9FA",
                        "padding": "1rem",
                        "borderRadius": "8px",
                        "fontSize": "0.75rem",
                        "whiteSpace": "pre-wrap",
                        "maxHeight": "300px",
                        "overflowY": "auto",
                        "marginTop": "0.5rem",
                    },
                ),
            ])
        )

    body_children.extend([
        html.Hr(className="section-divider"),
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-redo me-2"), "Retry"],
                id="retry-deploy-btn",
                color="primary",
                className="me-2",
            ),
            dbc.Button(
                [html.I(className="fas fa-plus me-2"), "Build Another"],
                id="deploy-another-btn",
                color="secondary",
                outline=True,
            ),
        ]),
    ])

    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-exclamation-circle me-2", style={"color": "#DC3545"}),
            "Deployment Failed",
        ]),
        dbc.CardBody(body_children),
    ], className="error-card")


# ===========================================================================
# Callbacks
# ===========================================================================

# ---------------------------------------------------------------------------
# 1. Toggle config collapse
# ---------------------------------------------------------------------------

@callback(
    Output("config-collapse", "is_open"),
    Input("config-card-header", "n_clicks"),
    State("config-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_config_collapse(n_clicks: int, is_open: bool) -> bool:
    return not is_open


# ---------------------------------------------------------------------------
# 1b. Toggle progress card collapse
# ---------------------------------------------------------------------------

@callback(
    Output("progress-collapse", "is_open", allow_duplicate=True),
    Input("progress-card-header", "n_clicks"),
    State("progress-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_progress_collapse(n_clicks: int, is_open: bool) -> bool:
    return not is_open


# ---------------------------------------------------------------------------
# 1c. Toggle results card collapse
# ---------------------------------------------------------------------------

@callback(
    Output("results-collapse", "is_open", allow_duplicate=True),
    Input("results-card-header", "n_clicks"),
    State("results-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_results_collapse(n_clicks: int, is_open: bool) -> bool:
    return not is_open


# ---------------------------------------------------------------------------
# 2. Toggle custom industry / populate use case presets
# ---------------------------------------------------------------------------

@callback(
    Output("custom-industry-input", "style"),
    Output("custom-industry-input", "value"),
    Output("use-case-preset-dropdown", "options"),
    Output("use-case-preset-dropdown", "value"),
    Input("industry-dropdown", "value"),
    prevent_initial_call=True,
)
def toggle_custom_industry(subindustry: Optional[str]):
    hide = {"display": "none"}
    show = {"display": "block"}
    if not subindustry:
        return hide, "", [], None

    if subindustry == "Custom":
        return show, "", [], None

    presets = SUBINDUSTRY_USE_CASES.get(subindustry, [])
    options = [{"label": p["label"], "value": p["label"]} for p in presets]
    return hide, "", options, None


# ---------------------------------------------------------------------------
# 3. Apply use case preset (fill form fields)
# ---------------------------------------------------------------------------

@callback(
    Output("company-input", "value"),
    Output("use-case-input", "value"),
    Output("context-input", "value"),
    Input("use-case-preset-dropdown", "value"),
    State("industry-dropdown", "value"),
    prevent_initial_call=True,
)
def apply_use_case_preset(
    preset_label: Optional[str],
    subindustry: Optional[str],
):
    if not preset_label or not subindustry:
        return no_update, no_update, no_update

    presets = SUBINDUSTRY_USE_CASES.get(subindustry, [])
    match = next((p for p in presets if p["label"] == preset_label), None)
    if not match:
        return no_update, no_update, no_update

    return (
        match.get("company_name", ""),
        match.get("use_case", ""),
        match.get("business_context", ""),
    )


# ---------------------------------------------------------------------------
# 4. Update dataset size fields from preset
# ---------------------------------------------------------------------------

@callback(
    Output("dataset-size-estimate", "children"),
    Output("num-tables", "value"),
    Output("num-products", "value"),
    Output("num-locations", "value"),
    Output("scale-input", "value"),
    Output("target-rows-input", "value"),
    Input("dataset-size-dropdown", "value"),
    prevent_initial_call=True,
)
def update_dataset_size(size: Optional[str]):
    """Auto-fill data generation fields from preset."""
    if size == "custom":
        return "Adjust the fields below.", no_update, no_update, no_update, no_update, no_update
    preset = DATASET_SIZE_PRESETS.get(size, DATASET_SIZE_PRESETS.get("demo", {}))
    estimate = DATASET_SIZE_ESTIMATES.get(size, "")
    return (
        estimate,
        preset.get("num_tables", 3),
        preset.get("num_products", 20),
        preset.get("num_locations", 8),
        preset.get("scale", 1),
        preset.get("target_rows", 5000),
    )


# ---------------------------------------------------------------------------
# 5. Auto-switch to Custom when user edits detail fields
# ---------------------------------------------------------------------------

@callback(
    Output("dataset-size-dropdown", "value"),
    Input("num-tables", "value"),
    Input("num-products", "value"),
    Input("num-locations", "value"),
    Input("scale-input", "value"),
    Input("target-rows-input", "value"),
    State("dataset-size-dropdown", "value"),
    prevent_initial_call=True,
)
def auto_switch_to_custom(num_tables, num_products, num_locations, scale, target_rows, current_size):
    """Switch dataset size dropdown to 'Custom' when user manually edits any detail field."""
    if current_size == "custom":
        return no_update
    preset = DATASET_SIZE_PRESETS.get(current_size)
    if not preset:
        return "custom"
    # Check if values still match the preset
    try:
        if (int(num_tables or 0) == preset["num_tables"] and
            int(num_products or 0) == preset["num_products"] and
            int(num_locations or 0) == preset["num_locations"] and
            int(scale or 0) == preset["scale"] and
            int(target_rows or 0) == preset["target_rows"]):
            return no_update
    except (ValueError, TypeError):
        pass
    return "custom"


# ---------------------------------------------------------------------------
# 6. Character count for business context
# ---------------------------------------------------------------------------

@callback(
    Output("context-char-count", "children"),
    Input("context-input", "value"),
)
def update_char_count(value: Optional[str]):
    """Show character count guidance for business context."""
    count = len(value) if value else 0
    color = "#00A972" if 100 <= count <= 300 else "#6C757D"
    return html.Span(f"{count} characters (aim for 100\u2013300)", style={"color": color})


# ---------------------------------------------------------------------------
# 7. Auto-detect user from forwarded headers
# ---------------------------------------------------------------------------

@callback(
    Output("deployer-name-store", "data"),
    Input("main-tabs", "active_tab"),
    prevent_initial_call=False,
)
def auto_detect_user(active_tab):
    """Auto-detect the user's identity from Databricks Apps forwarded headers."""
    from flask import request

    email = (
        request.headers.get("x-forwarded-email")
        or request.headers.get("x-forwarded-preferred-username")
        or request.headers.get("x-forwarded-user")
        or ""
    )
    if email:
        name_part = email.split("@")[0]
        display_name = " ".join(part.capitalize() for part in name_part.replace(".", " ").replace("_", " ").split())
        is_admin = False
        try:
            spark = _get_spark()
            _ensure_first_admin(spark, email)
            is_admin = _is_manager(spark, email)
        except Exception as e:
            # If DB is unreachable, grant admin so deployer can fix permissions
            logger.warning("Admin check failed for %s — defaulting to admin: %s", email, e)
            is_admin = True
        return {"email": email, "display_name": display_name, "is_admin": is_admin}
    return {"email": "", "display_name": "Unknown User", "is_admin": False}


# ---------------------------------------------------------------------------
# 8. Update navbar user display
# ---------------------------------------------------------------------------

@callback(
    Output("navbar-user-display", "children"),
    Output("footer-deployer-email", "children"),
    Input("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def update_navbar_user(deployer_info):
    """Show logged-in user in navbar and footer."""
    if not deployer_info:
        return "", ""
    name = deployer_info.get("display_name", "")
    email = deployer_info.get("email", "")
    is_admin = deployer_info.get("is_admin", False)
    role_badge = (
        dbc.Badge("Admin", color="success", className="ms-2", pill=True)
        if is_admin
        else dbc.Badge("User", color="secondary", className="ms-2", pill=True)
    )
    navbar = [name, role_badge] if name and name != "Unknown User" else ""
    footer = email if email else ""
    return navbar, footer


# ---------------------------------------------------------------------------
# 9. Refresh warehouses
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-dropdown", "options"),
    Output("warehouse-dropdown", "value"),
    Output("warehouse-store", "data"),
    Output("warehouse-alert-area", "children"),
    Input("refresh-warehouses-btn", "n_clicks"),
    Input("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def refresh_warehouses(n_clicks: int, deployer_info):
    """Load warehouses -- triggered by Refresh button or auto on page load."""
    try:
        user_ws = _get_user_workspace_client()
        warehouses = _list_warehouses(ws=user_ws)
        options = []
        for wh in warehouses:
            serverless = " [Serverless]" if wh.get("enable_serverless_compute") else ""
            label = f"{wh['name']}  \u2014  {wh['state']}  ({wh['warehouse_type']}, {wh['cluster_size']}{serverless})"
            options.append({"label": label, "value": wh["id"]})
        running = [wh["id"] for wh in warehouses if wh["state"] == "RUNNING"]
        default = running[0] if running else (warehouses[0]["id"] if warehouses else None)
        # Show warning alert if no running warehouses
        alert_content = ""
        if not any(wh["state"] == "RUNNING" for wh in warehouses):
            alert_content = dbc.Alert([
                html.Div([
                    html.I(className="fas fa-exclamation-triangle me-2", style={"fontSize": "1.1rem"}),
                    html.Strong("No warehouse is running"),
                ], className="mb-2"),
                html.P("A SQL warehouse must be running to deploy. Start one in Advanced Options or wait for one to become available.",
                       className="mb-0", style={"fontSize": "0.9rem"}),
            ], color="warning", className="mb-3")
        return options, default, warehouses, alert_content
    except Exception:
        logger.error("Failed to list warehouses:\n%s", traceback.format_exc())
        return [], None, [], ""


# ---------------------------------------------------------------------------
# 10. Auto-refresh warehouse status (interval-driven)
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-alert-area", "children", allow_duplicate=True),
    Input("warehouse-refresh-interval", "n_intervals"),
    State("main-tabs", "active_tab"),
    State("warehouse-store", "data"),
    prevent_initial_call=True,
)
def auto_refresh_warehouse_status(n_intervals, active_tab, warehouse_data):
    """Lightweight poll: update warehouse alert every 30s while on Build tab."""
    if active_tab != "deploy-tab":
        return no_update
    try:
        warehouses = _list_warehouses()
        if not any(wh["state"] == "RUNNING" for wh in warehouses):
            return dbc.Alert([
                html.Div([
                    html.I(className="fas fa-exclamation-triangle me-2"),
                    html.Strong("No warehouse is running"),
                ], className="mb-2"),
                html.P("A SQL warehouse must be running to deploy.",
                       className="mb-0", style={"fontSize": "0.9rem"}),
            ], color="warning", className="mb-3")
        return ""
    except Exception:
        return no_update


# ---------------------------------------------------------------------------
# 11. Update warehouse badge for selected warehouse
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-status-badge", "children"),
    Output("start-warehouse-btn", "disabled"),
    Output("stop-warehouse-btn", "disabled"),
    Input("warehouse-dropdown", "value"),
    State("warehouse-store", "data"),
)
def update_warehouse_badge(warehouse_id: Optional[str], warehouses: Optional[list]):
    if not warehouse_id or not warehouses:
        return "", True, True
    wh = next((w for w in warehouses if w["id"] == warehouse_id), None)
    if not wh:
        return "", True, True
    wh_state = wh["state"]
    color, icon = _warehouse_badge(wh_state)
    badge = dbc.Badge([html.I(className=f"fas {icon} me-1"), wh_state], color=color, className="me-2")
    info = html.Small(
        f"{wh['warehouse_type']}  \u00b7  {wh['cluster_size']}" + ("  \u00b7  Serverless" if wh.get("enable_serverless_compute") else ""),
        className="text-muted-brand",
    )
    tier = "Serverless" if wh.get("enable_serverless_compute") else "Classic"
    size = wh.get("cluster_size", "")
    size_cost = {"2X-Small": "$", "X-Small": "$", "Small": "$$", "Medium": "$$$", "Large": "$$$$"}.get(size, "$$")
    cost_info = html.Small(f"{tier} \u00b7 {size_cost}", style={"color": "#6C757D", "marginLeft": "0.5rem"})
    start_disabled = wh_state != "STOPPED"
    stop_disabled = wh_state != "RUNNING"
    return html.Div([badge, info, cost_info], className="d-flex align-items-center"), start_disabled, stop_disabled


# ---------------------------------------------------------------------------
# 12. Start a stopped warehouse
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-status-badge", "children", allow_duplicate=True),
    Output("start-warehouse-btn", "disabled", allow_duplicate=True),
    Input("start-warehouse-btn", "n_clicks"),
    State("warehouse-dropdown", "value"),
    prevent_initial_call=True,
)
def start_warehouse(n_clicks: int, warehouse_id: Optional[str]):
    if not n_clicks or not warehouse_id:
        return no_update, no_update
    try:
        w = _get_user_workspace_client()
        w.warehouses.start(warehouse_id)
        badge = dbc.Badge([html.I(className="fas fa-spinner fa-spin me-1"), "STARTING"], color="warning", className="me-2")
        msg = html.Small("Starting... click Refresh to update.", className="text-muted-brand")
        return html.Div([badge, msg], className="d-flex align-items-center"), True
    except Exception:
        return dbc.Alert(f"Failed to start: {traceback.format_exc()}", color="danger", className="mt-2 mb-0"), True


# ---------------------------------------------------------------------------
# 12b. Stop a running warehouse
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-status-badge", "children", allow_duplicate=True),
    Output("stop-warehouse-btn", "disabled", allow_duplicate=True),
    Input("stop-warehouse-btn", "n_clicks"),
    State("warehouse-dropdown", "value"),
    prevent_initial_call=True,
)
def stop_warehouse(n_clicks: int, warehouse_id: Optional[str]):
    if not n_clicks or not warehouse_id:
        return no_update, no_update
    try:
        w = _get_user_workspace_client()
        w.warehouses.stop(warehouse_id)
        badge = dbc.Badge([html.I(className="fas fa-spinner fa-spin me-1"), "STOPPING"], color="warning", className="me-2")
        msg = html.Small("Stopping... click Refresh to update.", className="text-muted-brand")
        return html.Div([badge, msg], className="d-flex align-items-center"), True
    except Exception:
        return dbc.Alert(f"Failed to stop: {traceback.format_exc()}", color="danger", className="mt-2 mb-0"), True


# ---------------------------------------------------------------------------
# 13. Create a new serverless warehouse
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-dropdown", "options", allow_duplicate=True),
    Output("warehouse-dropdown", "value", allow_duplicate=True),
    Output("warehouse-store", "data", allow_duplicate=True),
    Output("warehouse-alert-area", "children", allow_duplicate=True),
    Input("create-warehouse-btn", "n_clicks"),
    State("new-warehouse-name", "value"),
    State("new-warehouse-size", "value"),
    prevent_initial_call=True,
)
def create_warehouse(n_clicks: int, name: Optional[str], size: Optional[str]):
    if not n_clicks:
        return no_update, no_update, no_update, no_update
    if not name or not name.strip():
        return no_update, no_update, no_update, dbc.Alert("Please enter a warehouse name.", color="warning", dismissable=True)
    try:
        w = _get_workspace_client()
        from databricks.sdk.service.sql import CreateWarehouseRequestWarehouseType
        result = w.warehouses.create(name=name.strip(), cluster_size=size or "Small", max_num_clusters=1, auto_stop_mins=10, warehouse_type=CreateWarehouseRequestWarehouseType.PRO, enable_serverless_compute=True)
        warehouses = _list_warehouses()
        options = []
        for wh in warehouses:
            serverless = " [Serverless]" if wh.get("enable_serverless_compute") else ""
            label = f"{wh['name']}  \u2014  {wh['state']}  ({wh['warehouse_type']}, {wh['cluster_size']}{serverless})"
            options.append({"label": label, "value": wh["id"]})
        return options, result.id, warehouses, dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Created '{name.strip()}' \u2014 starting automatically."], color="success", dismissable=True)
    except Exception:
        return no_update, no_update, no_update, dbc.Alert(f"Failed: {traceback.format_exc()}", color="danger", dismissable=True)


# ---------------------------------------------------------------------------
# 14. Start deploy (validate + background thread) -- Custom Build
# ---------------------------------------------------------------------------

@callback(
    Output("deploy-session-id", "data"),
    Output("deploy-btn-wrapper", "style"),
    Output("progress-interval", "disabled"),
    Output("deploy-progress-area", "children"),
    Output("deploy-results", "children", allow_duplicate=True),
    Output("config-collapse", "is_open", allow_duplicate=True),
    Output("progress-collapse", "is_open"),
    Output("progress-card-wrapper", "style"),
    Output("config-summary", "children"),
    Output("config-summary", "style"),
    Output("deploy-params-store", "data"),
    Input("deploy-btn", "n_clicks"),
    State("deployer-name-store", "data"),
    State("industry-dropdown", "value"),
    State("custom-industry-input", "value"),
    State("company-input", "value"),
    State("use-case-input", "value"),
    State("context-input", "value"),
    State("num-tables", "value"),
    State("num-products", "value"),
    State("num-locations", "value"),
    State("scale-input", "value"),
    State("target-rows-input", "value"),
    State("catalog-input", "value"),
    State("schema-input", "value"),
    State("warehouse-dropdown", "value"),
    prevent_initial_call=True,
)
def start_deploy(
    n_clicks, deployer_name, industry, custom_industry, company_name, use_case, business_context,
    num_tables, num_products, num_locations, scale, target_rows, catalog, schema, warehouse_id,
):
    """Validate inputs and kick off deploy in a background thread."""
    no_updates = (no_update,) * 11
    if not n_clicks:
        return no_updates

    resolved_industry = custom_industry if industry == "Custom" else industry

    deployer_info = deployer_name or {"email": "", "display_name": "Unknown User"}
    if isinstance(deployer_info, str):
        deployer_info = {"email": "", "display_name": deployer_info}
    deployer_email = deployer_info.get("email", "")
    if not deployer_email:
        from flask import request
        deployer_email = request.headers.get("x-forwarded-email", "")

    missing = []
    if not resolved_industry:
        missing.append("Industry")
    if not company_name:
        missing.append("Company Name")
    if not use_case:
        missing.append("Use Case")
    if not business_context:
        missing.append("Business Context")
    if not warehouse_id:
        missing.append("SQL Warehouse (click Refresh)")

    if missing:
        return (
            no_update, no_update,
            True, dbc.Alert(f"Please fill in: {', '.join(missing)}", color="warning", dismissable=True),
            no_update, no_update, no_update, no_update, no_update, no_update,
            no_update,
        )

    # Override warehouse if admin-locked
    try:
        spark_check = _get_spark()
        if _get_setting(spark_check, "warehouse_policy") == "admin_locked":
            locked = _get_setting(spark_check, "locked_warehouse_id")
            if locked:
                warehouse_id = locked
    except Exception:
        pass

    # Create OBO clients while Flask request context is active
    user_spark = _get_user_spark()
    user_ws = _get_user_workspace_client()

    session_id = str(uuid.uuid4())

    # Record start time
    with _deploy_lock:
        _deploy_start_time[session_id] = time.time()

    params = {
        "deployer_info": deployer_info,
        "deployer_email": deployer_email,
        "industry": resolved_industry,
        "company_name": company_name,
        "use_case": use_case,
        "business_context": business_context,
        "num_tables": int(num_tables or 3),
        "num_products": int(num_products or 20),
        "num_locations": int(num_locations or 8),
        "catalog": catalog if catalog else None,
        "schema": schema if schema else None,
        "warehouse_id": warehouse_id,
        "scale": int(scale or 1),
        "target_rows": int(target_rows) if target_rows else None,
    }

    # Start background thread with OBO auth
    thread = threading.Thread(target=_run_deploy_in_thread, args=(session_id, params, user_spark, user_ws), daemon=True)
    thread.start()

    # Initial progress content (body of the progress collapse)
    est_minutes = _estimate_deploy_minutes(params)
    initial_bar = _build_step_bar("connect", session_id)
    progress_content = dbc.CardBody([
        initial_bar,
        html.Small(f"This typically takes ~{est_minutes} minutes.", className="text-muted-brand mt-2", style={"display": "block"}),
    ])

    # Config summary shown when card is collapsed during deploy
    summary_text = f"{resolved_industry}  /  {company_name}  \u2014  {use_case}"
    summary = html.Span(summary_text)

    return (
        session_id,
        {"display": "none"},  # hide deploy button
        False,  # enable interval polling
        progress_content,
        "",  # clear previous results
        False,  # collapse config card
        True,  # expand progress card
        {"display": "block", "borderLeft": "4px solid #FF3621"},  # show progress card wrapper
        summary,  # config summary content
        {"display": "block", "padding": "0.5rem 1.25rem", "fontSize": "0.85rem", "color": "#6C757D", "borderTop": "1px solid #DEE2E6"},  # show config summary
        params,  # store params for retry
    )


# ---------------------------------------------------------------------------
# 15. Poll deploy progress
# ---------------------------------------------------------------------------

@callback(
    Output("deploy-progress-area", "children", allow_duplicate=True),
    Output("deploy-results", "children"),
    Output("progress-interval", "disabled", allow_duplicate=True),
    Output("progress-collapse", "is_open", allow_duplicate=True),
    Output("results-collapse", "is_open"),
    Output("results-card-wrapper", "style"),
    Output("deploy-btn-wrapper", "style", allow_duplicate=True),
    Output("progress-header-icon", "className"),
    Output("progress-header-icon", "style"),
    Input("progress-interval", "n_intervals"),
    State("deploy-session-id", "data"),
    State("deploy-params-store", "data"),
    prevent_initial_call=True,
)
def poll_deploy_progress(n_intervals, session_id, deploy_params):
    """Poll for progress updates from the background deploy thread."""
    no_updates = (no_update,) * 9
    if not session_id:
        return no_updates

    messages = _get_progress(session_id)
    result = _get_deploy_result(session_id)
    is_done = result is not None

    # Step progress bar
    current_step = _get_step(session_id)
    step_bar = _build_step_bar(current_step or "connect", session_id)

    # Detailed log (collapsible)
    msg_items = []
    for i, msg in enumerate(messages):
        is_last = (i == len(messages) - 1) and not is_done
        icon_cls = "fas fa-spinner fa-spin" if is_last else "fas fa-check-circle"
        icon_color = "#FF3621" if is_last else "#00A972"
        msg_items.append(html.Div([
            html.I(className=f"{icon_cls} me-2", style={"color": icon_color, "fontSize": "0.8rem"}),
            html.Span(msg, style={"fontSize": "0.85rem"}),
        ], className="mb-1"))

    progress_content = dbc.CardBody([
        step_bar,
        html.Details([
            html.Summary("Show detailed log", style={"cursor": "pointer", "fontSize": "0.8rem", "color": "#6C757D", "marginTop": "0.75rem"}),
            html.Div(msg_items, className="mt-2"),
        ]) if msg_items else html.Div(),
    ])

    if is_done:
        _cleanup_session(session_id)
        is_success = result["status"] == "success"
        if is_success:
            result_content = _build_success_card(result["result"])
        else:
            error_msg = result.get("error", "Unknown error")
            error_tb = result.get("error_traceback", "")
            error_cat = result.get("error_category", "UNKNOWN")
            failed_params = result.get("params", {})
            result_content = _build_categorized_error_card(error_msg, error_cat, error_tb, failed_params)

        done_icon = "fas fa-check-circle me-2" if is_success else "fas fa-exclamation-circle me-2"
        done_color = {"color": "#00A972"} if is_success else {"color": "#DC3545"}

        return (
            progress_content,
            result_content,
            True,   # stop polling
            False,  # collapse progress
            True,   # expand results card (details inside are collapsed via <details>)
            {"display": "block"},  # show results card wrapper
            {"display": "block"},  # show deploy button again
            done_icon,  # update progress header icon (stop spinner)
            done_color,  # update progress header icon color
        )

    # Still in progress -- only update progress content
    return (progress_content,) + (no_update,) * 8


# ---------------------------------------------------------------------------
# 16. Deploy another (reset form)
# ---------------------------------------------------------------------------

@callback(
    Output("deploy-results", "children", allow_duplicate=True),
    Output("deploy-progress-area", "children", allow_duplicate=True),
    Output("config-collapse", "is_open", allow_duplicate=True),
    Output("progress-card-wrapper", "style", allow_duplicate=True),
    Output("results-card-wrapper", "style", allow_duplicate=True),
    Output("progress-collapse", "is_open", allow_duplicate=True),
    Output("results-collapse", "is_open", allow_duplicate=True),
    Output("config-summary", "style", allow_duplicate=True),
    Output("deploy-btn-wrapper", "style", allow_duplicate=True),
    Output("quick-deploy-view", "style", allow_duplicate=True),
    Input("deploy-another-btn", "n_clicks"),
    prevent_initial_call=True,
)
def deploy_another(n_clicks):
    """Clear results and show config form again (restore Quick Deploy view)."""
    if not n_clicks:
        return (no_update,) * 10
    return (
        "",  # clear results
        "",  # clear progress
        True,  # expand config
        {"display": "none"},  # hide progress card
        {"display": "none"},  # hide results card
        False,  # collapse progress
        False,  # collapse results
        {"display": "none"},  # hide config summary
        no_update,  # deploy button visibility controlled by view
        {"display": "block"},  # restore quick deploy view
    )


# ---------------------------------------------------------------------------
# 17. Retry deploy
# ---------------------------------------------------------------------------

@callback(
    Output("deploy-session-id", "data", allow_duplicate=True),
    Output("deploy-btn-wrapper", "style", allow_duplicate=True),
    Output("progress-interval", "disabled", allow_duplicate=True),
    Output("deploy-progress-area", "children", allow_duplicate=True),
    Output("deploy-results", "children", allow_duplicate=True),
    Output("config-collapse", "is_open", allow_duplicate=True),
    Output("progress-collapse", "is_open", allow_duplicate=True),
    Output("progress-card-wrapper", "style", allow_duplicate=True),
    Output("results-card-wrapper", "style", allow_duplicate=True),
    Output("results-collapse", "is_open", allow_duplicate=True),
    Input("retry-deploy-btn", "n_clicks"),
    State("deploy-params-store", "data"),
    prevent_initial_call=True,
)
def retry_deploy(n_clicks, params):
    if not n_clicks or not params:
        return (no_update,) * 10

    # Create OBO clients while Flask request context is active
    user_spark = _get_user_spark()
    user_ws = _get_user_workspace_client()

    session_id = str(uuid.uuid4())

    # Record start time
    with _deploy_lock:
        _deploy_start_time[session_id] = time.time()

    thread = threading.Thread(
        target=_run_deploy_in_thread, args=(session_id, params, user_spark, user_ws), daemon=True
    )
    thread.start()

    return (
        session_id,
        {"display": "none"},  # hide deploy button
        False,  # enable polling
        dbc.CardBody([
            _build_step_bar("connect", session_id),
            html.Small("Retrying deployment...", className="text-muted-brand mt-2", style={"display": "block"}),
        ]),
        "",  # clear results
        False,  # collapse config
        True,  # expand progress
        {"display": "block", "borderLeft": "4px solid #FF3621"},  # show progress wrapper
        {"display": "none"},  # hide results
        False,  # collapse results
    )


# ---------------------------------------------------------------------------
# 18. Restore deploy state on tab switch
# ---------------------------------------------------------------------------

@callback(
    Output("progress-card-wrapper", "style", allow_duplicate=True),
    Output("results-card-wrapper", "style", allow_duplicate=True),
    Output("config-collapse", "is_open", allow_duplicate=True),
    Output("deploy-btn-wrapper", "style", allow_duplicate=True),
    Output("config-summary", "style", allow_duplicate=True),
    Output("quick-deploy-view", "style", allow_duplicate=True),
    Input("main-tabs", "active_tab"),
    State("deploy-session-id", "data"),
    State("progress-interval", "disabled"),
    prevent_initial_call=True,
)
def restore_deploy_state_on_tab_switch(active_tab, session_id, interval_disabled):
    """When returning to Build tab during active deploy, restore progress card visibility.
    When returning with no active deploy, hide everything and restore quick-deploy-view."""
    if active_tab != "deploy-tab":
        return no_update, no_update, no_update, no_update, no_update, no_update
    # If there's an active deploy session and interval is running
    if session_id and not interval_disabled:
        return (
            {"display": "block", "borderLeft": "4px solid #FF3621"},  # show progress card
            no_update,  # don't touch results
            False,  # collapse config
            {"display": "none"},  # hide deploy button
            {"display": "block", "padding": "0.5rem 1.25rem", "fontSize": "0.85rem", "color": "#6C757D", "borderTop": "1px solid #DEE2E6"},  # show summary
            no_update,  # don't touch quick deploy view during active deploy
        )
    # No active deploy — hide progress/results, restore quick deploy view
    return (
        {"display": "none"},  # hide progress card
        {"display": "none"},  # hide results card
        no_update,
        no_update,
        no_update,
        {"display": "block"},  # show quick deploy view
    )


# ---------------------------------------------------------------------------
# 19. Warehouse policy enforcement
# ---------------------------------------------------------------------------

@callback(
    Output("warehouse-dropdown", "value", allow_duplicate=True),
    Output("warehouse-dropdown", "disabled"),
    Output("warehouse-status-badge", "children", allow_duplicate=True),
    Output("warehouse-dropdown", "options", allow_duplicate=True),
    Input("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def enforce_warehouse_policy(deployer_info):
    """Enforce admin warehouse policy on the Build tab dropdown."""
    try:
        spark = _get_spark()
        policy = _get_setting(spark, "warehouse_policy")

        if policy == "admin_locked":
            locked_id = _get_setting(spark, "locked_warehouse_id") or ""
            locked_name = _get_setting(spark, "locked_warehouse_name") or "Admin-selected"
            if locked_id:
                badge = dbc.Badge(
                    [html.I(className="fas fa-lock me-1"), f"Warehouse locked by admin: {locked_name}"],
                    color="info", className="mt-1",
                )
                return locked_id, True, badge, no_update

        elif policy == "recommended":
            rec_id = _get_setting(spark, "recommended_warehouse_id") or ""
            rec_name = _get_setting(spark, "recommended_warehouse_name") or "Admin-recommended"
            if rec_id:
                badge = dbc.Badge(
                    [html.I(className="fas fa-star me-1"), f"Recommended by admin: {rec_name}"],
                    color="info", className="mt-1",
                )
                return rec_id, False, badge, no_update

        elif policy == "allowlist":
            allowlist_raw = _get_setting(spark, "warehouse_allowlist") or "[]"
            try:
                allowlist_ids = json.loads(allowlist_raw)
            except (json.JSONDecodeError, TypeError):
                allowlist_ids = []
            if allowlist_ids:
                try:
                    warehouses = _list_warehouses()
                    filtered_options = []
                    for wh in warehouses:
                        if wh["id"] in allowlist_ids:
                            serverless = " [Serverless]" if wh.get("enable_serverless_compute") else ""
                            label = f"{wh['name']}  \u2014  {wh['state']}  ({wh['warehouse_type']}, {wh['cluster_size']}{serverless})"
                            filtered_options.append({"label": label, "value": wh["id"]})
                    running = [wh["id"] for wh in warehouses if wh["id"] in allowlist_ids and wh["state"] == "RUNNING"]
                    default = running[0] if running else (filtered_options[0]["value"] if filtered_options else None)
                    badge = dbc.Badge(
                        [html.I(className="fas fa-list me-1"), f"Restricted to {len(filtered_options)} approved warehouse(s)"],
                        color="info", className="mt-1",
                    )
                    return default, False, badge, filtered_options
                except Exception:
                    pass
    except Exception:
        pass
    return no_update, False, no_update, no_update


# ---------------------------------------------------------------------------
# 20. Quick Deploy: show use case cards when subindustry card clicked
# ---------------------------------------------------------------------------

@callback(
    Output("use-case-card-area", "children"),
    Output("selected-industry-store", "data"),
    Input({"type": "subindustry-card", "index": ALL}, "n_clicks"),
    State("selected-industry-store", "data"),
    prevent_initial_call=True,
)
def show_use_case_cards(n_clicks_list, current_industry):
    """Show use case cards when a subindustry card is clicked; toggle off on re-click."""
    if not any(v for v in n_clicks_list if v):
        return no_update, no_update

    triggered = ctx.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return no_update, no_update
    subindustry = triggered["index"]

    # Toggle: collapse if same subindustry clicked again
    if subindustry == current_industry:
        return "", None

    use_cases = SUBINDUSTRY_USE_CASES.get(subindustry, [])
    icon = SUBINDUSTRY_ICONS.get(subindustry, "fa-industry")

    if not use_cases:
        return html.P(f"No presets available for {subindustry}.", className="text-muted-brand"), subindustry

    cards = []
    for idx, uc in enumerate(use_cases):
        has_spec = uc.get("has_preset_spec", False)

        info_id = f"uc-info-{subindustry.replace(' ', '-').replace('&', '')}-{idx}"
        card = dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H6(uc["label"], className="mb-0 d-inline", style={"color": "#1B3139"}),
                        html.Span(
                            html.I(className="fas fa-info-circle", style={"color": "#6C757D", "fontSize": "0.85rem"}),
                            id=info_id, className="ms-2", style={"cursor": "pointer"},
                        ),
                        dbc.Tooltip(
                            html.P(uc.get("business_context", ""), style={"fontSize": "0.8rem", "marginBottom": "0", "textAlign": "left"}),
                            target=info_id, placement="top", style={"maxWidth": "350px"},
                        ),
                    ], className="mb-2"),
                    html.P(uc.get("company_name", ""), style={"fontSize": "0.85rem", "fontWeight": "600", "color": "#FF3621", "marginBottom": "0.25rem"}),
                    html.P(
                        uc.get("business_context", "")[:100] + "..." if len(uc.get("business_context", "")) > 100 else uc.get("business_context", ""),
                        style={"fontSize": "0.8rem", "color": "#6C757D", "marginBottom": "0.75rem"},
                    ),
                    dbc.Button(
                        [html.I(className="fas fa-rocket me-1"), "Deploy Now"],
                        id={"type": "quick-deploy-btn", "index": f"{subindustry}:{idx}"},
                        color="primary", size="sm",
                        disabled=not has_spec,
                    ),
                ], style={"padding": "1rem"}),
            ], className="quick-deploy-card h-100"),
            md=4, sm=6, xs=12, className="mb-3",
        )
        cards.append(card)

    return html.Div([
        html.Hr(className="my-3"),
        html.H6([html.I(className=f"fas {icon} me-2"), f"{subindustry} Use Cases"], className="mb-3", style={"color": "#1B3139"}),
        dbc.Row(cards, className="g-3"),
    ]), subindustry


# ---------------------------------------------------------------------------
# 21. Switch between Quick Deploy and Custom Build views
# ---------------------------------------------------------------------------

@callback(
    Output("quick-deploy-view", "style"),
    Output("custom-build-view", "style"),
    Input("switch-to-custom-link", "n_clicks"),
    Input("switch-to-custom-link-intro", "n_clicks"),
    Input("switch-to-quick-link", "n_clicks"),
    prevent_initial_call=True,
)
def switch_build_mode(to_custom_clicks, to_custom_intro_clicks, to_quick_clicks):
    """Toggle between Quick Deploy and Custom Build views."""
    triggered = ctx.triggered_id
    if triggered in ("switch-to-custom-link", "switch-to-custom-link-intro"):
        return {"display": "none"}, {"display": "block"}
    elif triggered == "switch-to-quick-link":
        return {"display": "block"}, {"display": "none"}
    return no_update, no_update


# ---------------------------------------------------------------------------
# 22. Quick Deploy start
# ---------------------------------------------------------------------------

@callback(
    Output("deploy-session-id", "data", allow_duplicate=True),
    Output("deploy-btn-wrapper", "style", allow_duplicate=True),
    Output("progress-interval", "disabled", allow_duplicate=True),
    Output("deploy-progress-area", "children", allow_duplicate=True),
    Output("deploy-results", "children", allow_duplicate=True),
    Output("config-collapse", "is_open", allow_duplicate=True),
    Output("progress-collapse", "is_open", allow_duplicate=True),
    Output("progress-card-wrapper", "style", allow_duplicate=True),
    Output("quick-deploy-view", "style", allow_duplicate=True),
    Output("deploy-params-store", "data", allow_duplicate=True),
    Input({"type": "quick-deploy-btn", "index": ALL}, "n_clicks"),
    State("warehouse-store", "data"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def quick_deploy_start(n_clicks_list, warehouse_data, deployer_info):
    """Start a Quick Deploy from a subindustry use case preset."""
    if not any(v for v in n_clicks_list if v):
        return (no_update,) * 10

    triggered = ctx.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return (no_update,) * 10

    # Parse subindustry:idx from the button index
    parts = triggered["index"].split(":", 1)
    subindustry = parts[0]
    idx = int(parts[1])
    use_cases = SUBINDUSTRY_USE_CASES.get(subindustry, [])
    if idx >= len(use_cases):
        return (no_update,) * 10
    preset = use_cases[idx]

    # Create OBO clients while Flask request context is active
    user_spark = _get_user_spark()
    user_ws = _get_user_workspace_client()

    # Auto-detect warehouse — prefer running, auto-start stopped if needed
    warehouse_id = ""
    warehouses = warehouse_data if isinstance(warehouse_data, list) else []
    if not warehouses:
        try:
            warehouses = _list_warehouses(ws=user_ws)
        except Exception:
            warehouses = []
    for wh in warehouses:
        if wh.get("state") == "RUNNING":
            warehouse_id = wh["id"]
            break
    if not warehouse_id and warehouses:
        warehouse_id = warehouses[0].get("id", "")
        try:
            user_ws.warehouses.start(warehouse_id)
            logger.info("Quick Deploy: auto-started warehouse %s", warehouse_id)
        except Exception as e:
            logger.warning("Quick Deploy: failed to auto-start warehouse: %s", e)

    if not warehouse_id:
        return (no_update,) * 10  # No warehouse available at all

    # Override warehouse if admin-locked
    try:
        spark_check = _get_spark()
        if _get_setting(spark_check, "warehouse_policy") == "admin_locked":
            locked = _get_setting(spark_check, "locked_warehouse_id")
            if locked:
                warehouse_id = locked
    except Exception:
        pass

    deployer = deployer_info or {"email": "", "display_name": "Unknown User"}
    if isinstance(deployer, str):
        deployer = {"email": "", "display_name": deployer}
    deployer_email = deployer.get("email", "")
    if not deployer_email:
        from flask import request
        deployer_email = request.headers.get("x-forwarded-email", "")

    session_id = str(uuid.uuid4())

    params = {
        "deployer_info": deployer,
        "deployer_email": deployer_email,
        "industry": subindustry,
        "company_name": preset.get("company_name", ""),
        "use_case": preset.get("use_case", preset["label"]),
        "business_context": preset.get("business_context", ""),
        "warehouse_id": warehouse_id,
        "domain_spec_subindustry": subindustry,
        "domain_spec_label": preset["label"],
    }

    # Record start time
    with _deploy_lock:
        _deploy_start_time[session_id] = time.time()

    thread = threading.Thread(
        target=_run_deploy_in_thread, args=(session_id, params, user_spark, user_ws), daemon=True
    )
    thread.start()

    return (
        session_id,
        {"display": "none"},
        False,  # enable polling
        dbc.CardBody([
            _build_step_bar("connect", session_id),
            html.Small(f"Deploying {preset.get('company_name', preset['label'])}...", className="text-muted-brand mt-2", style={"display": "block"}),
        ]),
        "",  # clear results
        False,  # collapse config
        True,   # expand progress
        {"display": "block", "borderLeft": "4px solid #FF3621"},
        {"display": "none"},  # hide quick deploy view
        params,  # store params
    )


# ---------------------------------------------------------------------------
# 23. Quick Customize -- switch to Custom Build with pre-filled fields
# ---------------------------------------------------------------------------

@callback(
    Output("quick-deploy-view", "style", allow_duplicate=True),
    Output("custom-build-view", "style", allow_duplicate=True),
    Output("industry-dropdown", "value", allow_duplicate=True),
    Output("company-input", "value", allow_duplicate=True),
    Output("use-case-input", "value", allow_duplicate=True),
    Output("context-input", "value", allow_duplicate=True),
    Output("use-case-preset-dropdown", "value", allow_duplicate=True),
    Input({"type": "quick-customize-link", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def quick_customize(n_clicks_list):
    """Switch to Custom Build with pre-filled values from a use case preset."""
    if not any(v for v in n_clicks_list if v):
        return (no_update,) * 7

    triggered = ctx.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return (no_update,) * 7

    parts = triggered["index"].split(":", 1)
    subindustry = parts[0]
    idx = int(parts[1])
    use_cases = SUBINDUSTRY_USE_CASES.get(subindustry, [])
    if idx >= len(use_cases):
        return (no_update,) * 7
    preset = use_cases[idx]

    return (
        {"display": "none"},   # hide quick deploy
        {"display": "block"},  # show custom build
        subindustry,
        preset.get("company_name", ""),
        preset.get("use_case", ""),
        preset.get("business_context", ""),
        preset["label"],  # sets the preset dropdown
    )


# ---------------------------------------------------------------------------
# 24. Auto-scroll to use-case cards when subindustry is selected
# ---------------------------------------------------------------------------

clientside_callback(
    """function(children) {
        if (children && children !== '' && children !== null) {
            setTimeout(function() {
                var el = document.getElementById('use-case-card-area');
                if (el && el.offsetHeight > 0) {
                    el.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            }, 300);
        }
        return window.dash_clientside.no_update;
    }""",
    Output("use-case-card-area", "className"),
    Input("use-case-card-area", "children"),
    prevent_initial_call=True,
)


# ---------------------------------------------------------------------------
# 26. Request a use case
# ---------------------------------------------------------------------------

@callback(
    Output("request-uc-status", "children"),
    Output("request-uc-email", "value"),
    Output("request-uc-description", "value"),
    Input("request-uc-btn", "n_clicks"),
    State("request-uc-email", "value"),
    State("request-uc-description", "value"),
    prevent_initial_call=True,
)
def submit_use_case_request(n_clicks, email, description):
    """Log a use case request (stored in audit log if available)."""
    if not n_clicks:
        return no_update, no_update, no_update
    if not email or not description:
        return dbc.Alert("Please provide both your email and a use case description.", color="warning", dismissable=True, duration=4000), no_update, no_update
    try:
        from services.admin import _log_audit_event
        spark = _get_spark()
        _log_audit_event(
            spark, "use_case_request", email,
            details=f"Requested use case: {description}",
        )
    except Exception:
        pass  # Best-effort logging
    return (
        dbc.Alert([html.I(className="fas fa-check-circle me-1"), "Request submitted! We'll review your suggestion."], color="success", dismissable=True, duration=5000),
        "",  # clear email
        "",  # clear description
    )
