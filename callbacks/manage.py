"""Manage tab callbacks: deployment listing, teardown, batch operations."""

from __future__ import annotations

import json
import logging
import traceback
from typing import Optional

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, html, ALL

import genie_factory
from genie_factory import teardown
from services.databricks import _get_spark, _get_workspace_client, _get_user_workspace_client
from services.deployment import _get_active_deployments, _mark_torn_down
from services.admin import _is_manager, _log_audit_event
from components.cards import _build_deployments_table, _build_empty_state, _build_error_card

logger = logging.getLogger("genie-factory")


# ---------------------------------------------------------------------------
# Manage Tab Callbacks
# ---------------------------------------------------------------------------


@callback(
    Output("deployments-list", "children"),
    Output("deployments-store", "data"),
    Input("refresh-deployments-btn", "n_clicks"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
    running=[
        (Output("refresh-deployments-btn", "disabled"), True, False),
        (Output("refresh-deployments-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Loading..."], [html.I(className="fas fa-sync-alt me-1"), "Refresh"]),
    ],
)
def refresh_deployments(n_clicks: int, deployer_info):
    if not n_clicks:
        return dash.no_update, dash.no_update
    user_email = deployer_info.get("email", "") if deployer_info else ""
    try:
        spark = _get_spark()
        is_mgr = _is_manager(spark, user_email)
        deployments = _get_active_deployments(spark, user_email=user_email, is_manager=is_mgr)

        if not deployments:
            return _build_empty_state(), []

        table = _build_deployments_table(deployments)
        return table, [d for d in deployments]

    except Exception:
        tb = traceback.format_exc()
        logger.error("Failed to load deployments:\n%s", tb)
        return _build_error_card(tb), []


@callback(
    Output("deployments-list", "children", allow_duplicate=True),
    Output("deployments-store", "data", allow_duplicate=True),
    Input("main-tabs", "active_tab"),
    State("deployer-name-store", "data"),
    State("deployments-store", "data"),
    prevent_initial_call=True,
)
def auto_load_manage_tab(active_tab, deployer_info, existing_data):
    """Auto-load deployments when user switches to the Manage tab.

    Uses cached data if available to avoid re-querying on every tab switch.
    Users click Refresh for fresh data.
    """
    if active_tab != "manage-tab":
        return dash.no_update, dash.no_update
    # Use cached data if already loaded (persist across tab switches)
    if existing_data is not None and len(existing_data) > 0:
        return _build_deployments_table(existing_data), dash.no_update
    user_email = deployer_info.get("email", "") if deployer_info else ""
    try:
        spark = _get_spark()
        is_mgr = _is_manager(spark, user_email)
        deployments = _get_active_deployments(spark, user_email=user_email, is_manager=is_mgr)
        if not deployments:
            return _build_empty_state(), []
        return _build_deployments_table(deployments), [d for d in deployments]
    except Exception:
        tb = traceback.format_exc()
        logger.error("Failed to auto-load deployments:\n%s", tb)
        return _build_error_card(tb), []


@callback(
    Output("teardown-confirm", "displayed"),
    Output("teardown-target", "data"),
    Input({"type": "teardown-row-btn", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def request_teardown(n_clicks_list):
    """When a row's teardown button is clicked, store its ID and show confirm."""
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks_list):
        return dash.no_update, dash.no_update
    prop_id = ctx.triggered[0]["prop_id"]
    dep_id = json.loads(prop_id.rsplit(".", 1)[0])["index"]
    return True, [dep_id]


@callback(
    Output("teardown-status", "children"),
    Output("deployments-list", "children", allow_duplicate=True),
    Output("deployments-store", "data", allow_duplicate=True),
    Input("teardown-confirm", "submit_n_clicks"),
    State("teardown-target", "data"),
    State("deployments-store", "data"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def do_teardown(submit_n_clicks: int, target_ids, deployments: Optional[list], deployer_info=None):
    if not submit_n_clicks or not target_ids or not deployments:
        return dash.no_update, dash.no_update, dash.no_update

    # Normalize to list
    if isinstance(target_ids, str):
        target_ids = [target_ids]

    user_email = deployer_info.get("email", "") if deployer_info else ""

    try:
        spark = _get_spark()  # SP for system table access
        user_ws = _get_user_workspace_client()  # OBO for teardown operations
        user_is_manager = _is_manager(spark, user_email)

        torn = []
        failed = []
        for dep_id in target_ids:
            dep = next((d for d in deployments if d["deployment_id"] == dep_id), None)
            if not dep:
                continue
            # Permission check: only the deployer or a manager can teardown
            dep_owner = dep.get("deployed_by", "")
            if not user_is_manager and dep_owner != user_email:
                failed.append(f"{dep.get('company_name', dep_id)}: Permission denied — only the deployer or a manager can teardown")
                continue
            try:
                teardown_kwargs = {
                    "catalog": dep.get("catalog", ""),
                    "schema": dep.get("schema_name", dep.get("schema", "")),
                    "fqn": dep.get("fqn", ""),
                    "genie": {"space_id": dep.get("genie_space_id", "")},
                }
                teardown(spark, workspace_client=user_ws, **teardown_kwargs)
                _mark_torn_down(spark, dep_id, torn_down_by=user_email)
                company = dep.get("company_name", dep_id)
                _log_audit_event(spark, "teardown", user_email, target_deployment_id=dep_id, details=f"Tore down '{company}'")
                torn.append(company)
            except Exception as e:
                failed.append(f"{dep.get('company_name', dep_id)}: {e}")

        remaining = _get_active_deployments(spark, user_email=user_email, is_manager=user_is_manager)
        table = _build_deployments_table(remaining) if remaining else _build_empty_state()

        alerts = []
        if torn:
            alerts.append(dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Torn down: {', '.join(torn)}"], color="success", dismissable=True))
        if failed:
            alerts.append(dbc.Alert([html.I(className="fas fa-exclamation-circle me-1"), f"Failed: {'; '.join(failed)}"], color="danger", dismissable=True))

        return html.Div(alerts), table, [d for d in remaining] if remaining else []

    except Exception:
        tb = traceback.format_exc()
        logger.error("Teardown failed:\n%s", tb)
        return dbc.Alert(f"Teardown failed: {tb}", color="danger", dismissable=True), dash.no_update, dash.no_update


@callback(
    Output("teardown-selected-btn", "disabled"),
    Input({"type": "teardown-checkbox", "index": dash.ALL}, "value"),
    prevent_initial_call=True,
)
def toggle_teardown_selected_btn(values):
    """Enable 'Teardown Selected' button when at least one checkbox is checked."""
    if any(values):
        return False
    return True


@callback(
    Output("teardown-confirm", "displayed", allow_duplicate=True),
    Output("teardown-target", "data", allow_duplicate=True),
    Input("teardown-selected-btn", "n_clicks"),
    State({"type": "teardown-checkbox", "index": dash.ALL}, "value"),
    State({"type": "teardown-checkbox", "index": dash.ALL}, "id"),
    prevent_initial_call=True,
)
def request_batch_teardown(n_clicks, values, ids):
    """Collect checked deployment IDs and show confirm dialog."""
    if not n_clicks:
        return dash.no_update, dash.no_update
    selected = [id_dict["index"] for id_dict, val in zip(ids, values) if val]
    if not selected:
        return dash.no_update, dash.no_update
    return True, selected


# ---------------------------------------------------------------------------
# Filter / Sort / Select All / Clone
# ---------------------------------------------------------------------------


@callback(
    Output("deployments-list", "children", allow_duplicate=True),
    Input("filter-industry-dropdown", "value"),
    Input("filter-age-dropdown", "value"),
    Input("sort-dropdown", "value"),
    State("deployments-store", "data"),
    prevent_initial_call=True,
)
def filter_and_sort_deployments(industry_filter, age_filter, sort_by, deployments):
    """Client-side filter and sort of the cached deployment list."""
    if not deployments:
        return _build_empty_state()

    from datetime import datetime, timezone

    filtered = list(deployments)

    if industry_filter:
        filtered = [d for d in filtered if d.get("industry") == industry_filter]

    if age_filter and age_filter != "all":
        now = datetime.now(timezone.utc)

        def age_days(d):
            try:
                dt = datetime.strptime(d.get("deployed_at", ""), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                return (now - dt).days
            except (ValueError, TypeError):
                return 0

        if age_filter == "7":
            filtered = [d for d in filtered if age_days(d) < 7]
        elif age_filter == "30":
            filtered = [d for d in filtered if 7 <= age_days(d) < 30]
        elif age_filter == "30+":
            filtered = [d for d in filtered if age_days(d) >= 30]

    if sort_by == "date_asc":
        filtered.sort(key=lambda d: d.get("deployed_at", ""))
    elif sort_by == "industry":
        filtered.sort(key=lambda d: d.get("industry", ""))
    elif sort_by == "company":
        filtered.sort(key=lambda d: d.get("company_name", ""))
    # default date_desc is already the query order

    return _build_deployments_table(filtered) if filtered else _build_empty_state()


@callback(
    Output({"type": "teardown-checkbox", "index": dash.ALL}, "value", allow_duplicate=True),
    Input("select-all-checkbox", "value"),
    State({"type": "teardown-checkbox", "index": dash.ALL}, "id"),
    prevent_initial_call=True,
)
def toggle_select_all(select_all_value, checkbox_ids):
    """Toggle all teardown checkboxes when Select All is checked/unchecked."""
    if not checkbox_ids:
        return dash.no_update
    return [select_all_value] * len(checkbox_ids)


@callback(
    Output("main-tabs", "active_tab"),
    Output("quick-deploy-view", "style", allow_duplicate=True),
    Output("custom-build-view", "style", allow_duplicate=True),
    Output("industry-dropdown", "value", allow_duplicate=True),
    Output("company-input", "value", allow_duplicate=True),
    Output("use-case-input", "value", allow_duplicate=True),
    Output("context-input", "value", allow_duplicate=True),
    Input({"type": "clone-deploy-btn", "index": dash.ALL}, "n_clicks"),
    State("deployments-store", "data"),
    prevent_initial_call=True,
)
def clone_deployment(n_clicks_list, deployments):
    """Clone a deployment: switch to Build tab with pre-filled form fields."""
    if not any(v for v in n_clicks_list if v) or not deployments:
        return (dash.no_update,) * 7

    triggered = dash.ctx.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return (dash.no_update,) * 7

    dep_id = triggered["index"]
    dep = next((d for d in deployments if d.get("deployment_id") == dep_id), None)
    if not dep:
        return (dash.no_update,) * 7

    # Audit log the clone action (best-effort)
    try:
        spark = _get_spark()
        _log_audit_event(spark, "clone", "", details=f"Cloned deployment for {dep.get('industry', dep_id)}")
    except Exception:
        pass

    return (
        "deploy-tab",
        {"display": "none"},   # hide quick deploy
        {"display": "block"},  # show custom build
        dep.get("industry", ""),
        dep.get("company_name", "") + " (copy)",
        dep.get("use_case", ""),
        dep.get("business_context", ""),
    )
