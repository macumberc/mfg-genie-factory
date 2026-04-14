"""Admin tab callbacks: manager management, warehouse policy, tab visibility."""

from __future__ import annotations

import json
import logging
import os
import traceback

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, dcc, html, ALL

from services.databricks import _get_spark, _get_workspace_client, _list_warehouses
from services.admin import (
    _is_manager,
    _get_managers,
    _add_manager,
    _remove_manager,
    _get_setting,
    _set_setting,
    _list_workspace_users,
    _ensure_managers_table,
    _ensure_first_admin,
    _log_audit_event,
    _get_recent_activity,
    _get_deployment_analytics,
)
from services.deployment import _get_active_deployments, _mark_torn_down
from services.meta import _get_meta_fqn, _get_log_table, _get_managers_table, _get_settings_table
from components.cards import _build_manager_table

logger = logging.getLogger("genie-factory")


# ---------------------------------------------------------------------------
# Admin Tab Visibility
# ---------------------------------------------------------------------------


@callback(
    Output("admin-tab-element", "tab_style"),
    Input("deployer-name-store", "data"),
)
def update_admin_tab_visibility(deployer_info):
    """Show Admin tab for managers. Uses is_admin from store, falls back to DB check."""
    if not deployer_info or not isinstance(deployer_info, dict):
        return {"display": "none"}
    email = deployer_info.get("email", "")
    if not email:
        return {"display": "none"}
    is_admin = deployer_info.get("is_admin", False)
    if is_admin:
        return {}
    # Fallback: re-check DB
    try:
        spark = _get_spark()
        _ensure_first_admin(spark, email)
        if _is_manager(spark, email):
            return {}
    except Exception:
        pass
    return {"display": "none"}


# ---------------------------------------------------------------------------
# Admin Tab Callbacks
# ---------------------------------------------------------------------------


@callback(
    Output("admin-gate", "children"),
    Output("admin-gate", "style"),
    Output("admin-panel", "style"),
    Output("admin-system-info", "children"),
    Output("admin-manager-list", "children"),
    Output("warehouse-policy-radio", "value"),
    Output("admin-warehouse-selector", "style", allow_duplicate=True),
    Output("policy-save-no-lock", "style", allow_duplicate=True),
    Output("admin-warehouse-dropdown", "options"),
    Output("admin-warehouse-dropdown", "value"),
    Output("admin-warehouse-allowlist-selector", "style", allow_duplicate=True),
    Output("admin-warehouse-allowlist-dropdown", "options"),
    Output("admin-warehouse-allowlist-dropdown", "value"),
    Output("admin-recommended-selector", "style", allow_duplicate=True),
    Output("admin-recommended-dropdown", "options"),
    Output("admin-recommended-dropdown", "value"),
    Output("admin-wh-select-dropdown", "options"),
    Output("admin-app-info", "children"),
    Output("new-manager-dropdown", "options"),
    Input("main-tabs", "active_tab"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def load_admin_tab(active_tab, deployer_info):
    """Load admin data when tab is clicked. All UI components are in the static layout."""
    num_outputs = 19
    no_updates = (dash.no_update,) * num_outputs
    if active_tab != "admin-tab":
        return no_updates

    if isinstance(deployer_info, str):
        deployer_info = {"email": "", "display_name": deployer_info}
    user_email = (deployer_info or {}).get("email", "")
    logger.info("Admin tab: loading for user=%s", user_email)

    no_data = (dash.no_update,) * (num_outputs - 3)
    if not user_email:
        gate = dbc.Alert([html.I(className="fas fa-exclamation-triangle me-2"), "Unable to determine your identity. Try refreshing the page."], color="warning")
        return (gate, {}, {"display": "none"}) + no_data

    try:
        spark = _get_spark()
        _ensure_first_admin(spark, user_email)
        if not _is_manager(spark, user_email):
            gate = html.Div([
                html.Div(html.I(className="fas fa-lock", style={"fontSize": "3rem", "color": "#DEE2E6"}), className="text-center mb-3"),
                html.P("Admin access required.", className="text-center text-muted-brand", style={"fontSize": "1.1rem"}),
                html.P(f"Logged in as: {user_email}", className="text-center text-muted-brand", style={"fontSize": "0.85rem"}),
                html.P("Contact an existing admin to be added as a manager.", className="text-center text-muted-brand", style={"fontSize": "0.9rem"}),
            ], style={"padding": "3rem 1rem"})
            return (gate, {}, {"display": "none"}) + no_data

        # User is a manager — populate the admin panel
        _log_audit_event(spark, "admin_accessed", user_email, details="Accessed admin panel")
        managers = _get_managers(spark)
        manager_table = _build_manager_table(managers)

        wh_policy = _get_setting(spark, "warehouse_policy") or "user_choice"
        locked_wh_id = _get_setting(spark, "locked_warehouse_id") or ""
        recommended_wh_id = _get_setting(spark, "recommended_warehouse_id") or ""

        # Parse saved allowlist
        allowlist_raw = _get_setting(spark, "warehouse_allowlist") or "[]"
        try:
            allowlist_ids = json.loads(allowlist_raw)
        except (json.JSONDecodeError, TypeError):
            allowlist_ids = []

        try:
            warehouses = _list_warehouses()
            wh_options = [{"label": f"{wh['name']} ({wh['state']}, {wh['cluster_size']})", "value": wh["id"]} for wh in warehouses]
        except Exception:
            warehouses = []
            wh_options = []

        hide = {"display": "none"}
        show = {}

        # Determine which sub-panels to show based on saved policy
        wh_selector_style = show if wh_policy == "admin_locked" else hide
        save_no_lock_style = show if wh_policy == "user_choice" else hide
        allowlist_selector_style = show if wh_policy == "allowlist" else hide
        recommended_selector_style = show if wh_policy == "recommended" else hide

        # Build system configuration info
        meta_fqn = _get_meta_fqn(spark)
        log_tbl = _get_log_table(spark)
        mgr_tbl = _get_managers_table(spark)
        settings_tbl = _get_settings_table(spark)
        audit_tbl = f"{meta_fqn}.audit_log"

        # Get workspace host for clickable Catalog Explorer links
        try:
            ws = _get_workspace_client()
            _ws_host = ws.config.host.rstrip("/") if hasattr(ws, "config") and ws.config.host else ""
        except Exception:
            _ws_host = ""

        def _table_link(fqn: str) -> html.A | html.Code:
            """Return a clickable Catalog Explorer link for a fully-qualified table name, or a plain Code element if host is unavailable."""
            _link_style = {"fontSize": "0.8rem", "fontFamily": "'JetBrains Mono', 'Fira Code', monospace"}
            parts = fqn.split(".")
            if _ws_host and len(parts) == 3:
                url = f"{_ws_host}/explore/data/{parts[0]}/{parts[1]}/{parts[2]}"
                return html.A(fqn, href=url, target="_blank", style=_link_style)
            return html.Code(fqn, style={"fontSize": "0.8rem"})

        _mono = {"fontFamily": "'JetBrains Mono', 'Fira Code', monospace", "fontSize": "0.85rem", "color": "#FF3621"}
        system_info = html.Div([
            dbc.Row([
                dbc.Col([
                    html.Small("Metadata Schema", className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                    html.Span(meta_fqn, style=_mono),
                ], md=6),
                dbc.Col([
                    html.Small("Warehouse Policy", className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                    html.Span(wh_policy, style={"fontWeight": "600"}),
                ], md=6),
            ], className="mb-3"),
            html.H6("System Tables", className="mb-2", style={"fontSize": "0.85rem"}),
            html.Table([
                html.Tbody([
                    html.Tr([html.Td("Deployment Log", style={"fontSize": "0.8rem", "color": "#6C757D", "width": "40%"}), html.Td(_table_link(log_tbl))]),
                    html.Tr([html.Td("Managers", style={"fontSize": "0.8rem", "color": "#6C757D"}), html.Td(_table_link(mgr_tbl))]),
                    html.Tr([html.Td("Settings", style={"fontSize": "0.8rem", "color": "#6C757D"}), html.Td(_table_link(settings_tbl))]),
                    html.Tr([html.Td("Audit Log", style={"fontSize": "0.8rem", "color": "#6C757D"}), html.Td(_table_link(audit_tbl))]),
                ]),
            ], className="result-table", style={"width": "100%"}),
            html.Details([
                html.Summary("Quick SQL Reference", style={"cursor": "pointer", "fontSize": "0.8rem", "color": "#6C757D", "marginTop": "0.75rem"}),
                html.Pre(
                    f"-- Active deployments\nSELECT * FROM {log_tbl} WHERE status = 'active' ORDER BY deployed_at DESC;\n\n"
                    f"-- Failed deployments\nSELECT * FROM {log_tbl} WHERE status = 'failed' ORDER BY started_at DESC;\n\n"
                    f"-- Managers\nSELECT * FROM {mgr_tbl};\n\n"
                    f"-- Settings\nSELECT * FROM {settings_tbl};\n\n"
                    f"-- Recent audit events\nSELECT * FROM {audit_tbl} ORDER BY event_at DESC LIMIT 20;",
                    style={"background": "#1B3139", "color": "#F8F9FA", "padding": "1rem", "borderRadius": "8px",
                           "fontSize": "0.75rem", "whiteSpace": "pre-wrap", "marginTop": "0.5rem"},
                ),
            ]),
        ])

        # Build App Information card content
        _llm_endpoint = _get_setting(spark, "llm_endpoint") or os.environ.get("GENIE_FACTORY_LLM_ENDPOINT", "databricks-claude-sonnet-4-6")
        _sp_id = ""
        _app_url = ""
        try:
            _sp_id = ws.config.client_id or ""
        except Exception:
            pass
        try:
            _app_url = _ws_host
        except Exception:
            pass
        try:
            _active_count = spark.sql(f"SELECT COUNT(*) as c FROM {_get_log_table(spark)} WHERE status IN ('active', 'success', 'partial')").first()["c"]
        except Exception:
            _active_count = "?"
        _info_style = {"fontFamily": "'JetBrains Mono', 'Fira Code', monospace", "fontSize": "0.85rem"}
        app_info = html.Div([
            html.Table([
                html.Tbody([
                    html.Tr([html.Td("Workspace Host", style={"fontSize": "0.85rem", "color": "#6C757D", "width": "40%", "padding": "0.35rem 0"}), html.Td(html.Code(_app_url or "Unknown", style={"fontSize": "0.8rem"}))]),
                    html.Tr([html.Td("Service Principal", style={"fontSize": "0.85rem", "color": "#6C757D", "padding": "0.35rem 0"}), html.Td(html.Code(_sp_id or "N/A", style={"fontSize": "0.8rem"}))]),
                    html.Tr([html.Td("LLM Endpoint", style={"fontSize": "0.85rem", "color": "#6C757D", "padding": "0.35rem 0"}), html.Td(html.Code(_llm_endpoint, style={"fontSize": "0.8rem"}))]),
                    html.Tr([html.Td("Metadata Catalog", style={"fontSize": "0.85rem", "color": "#6C757D", "padding": "0.35rem 0"}), html.Td(html.Code(meta_fqn.split(".")[0] if "." in meta_fqn else meta_fqn, style={"fontSize": "0.8rem"}))]),
                    html.Tr([html.Td("Managers", style={"fontSize": "0.85rem", "color": "#6C757D", "padding": "0.35rem 0"}), html.Td(str(len(managers)))]),
                    html.Tr([html.Td("Active Deployments", style={"fontSize": "0.85rem", "color": "#6C757D", "padding": "0.35rem 0"}), html.Td(str(_active_count))]),
                ]),
            ], className="result-table", style={"width": "100%"}),
        ])

        # Fetch workspace users for manager dropdown (with timeout protection)
        try:
            users = _list_workspace_users()
            user_options = [{"label": f"{u['display_name']} ({u['email']})", "value": u["email"]} for u in users]
        except Exception:
            user_options = []

        logger.info("Admin tab: loaded %d managers, %d users, policy=%s", len(managers), len(user_options), wh_policy)
        return (
            "",                          # clear gate content
            hide,                        # hide gate
            {"display": "block"},        # show admin panel
            system_info,                 # admin-system-info
            manager_table,
            wh_policy,
            wh_selector_style,           # admin-warehouse-selector
            save_no_lock_style,          # policy-save-no-lock
            wh_options,                  # admin-warehouse-dropdown options
            locked_wh_id,                # admin-warehouse-dropdown value
            allowlist_selector_style,    # admin-warehouse-allowlist-selector
            wh_options,                  # admin-warehouse-allowlist-dropdown options (same list)
            allowlist_ids,               # admin-warehouse-allowlist-dropdown value
            recommended_selector_style,  # admin-recommended-selector
            wh_options,                  # admin-recommended-dropdown options (same list)
            recommended_wh_id,           # admin-recommended-dropdown value
            wh_options,                  # admin-wh-select-dropdown options
            app_info,                    # admin-app-info
            user_options,                # new-manager-dropdown options
        )
    except Exception:
        tb = traceback.format_exc()
        logger.error("Admin tab failed:\n%s", tb)
        gate = dbc.Alert([html.I(className="fas fa-exclamation-circle me-2"), f"Error loading admin panel: {tb}"], color="danger")
        return (gate, {}, {"display": "none"}) + no_data


@callback(
    Output("admin-manager-list", "children", allow_duplicate=True),
    Output("new-manager-email", "value"),
    Output("add-manager-status", "children"),
    Input("add-manager-btn", "n_clicks"),
    State("new-manager-email", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def add_manager_callback(n_clicks, email_input, deployer_info):
    import re
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update
    email = (email_input or "").strip()
    if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return dash.no_update, dash.no_update, dbc.Alert("Please enter a valid email address.", color="warning", dismissable=True, duration=3000)
    user_email = (deployer_info or {}).get("email", "")
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dash.no_update, dash.no_update, dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _add_manager(spark, email, user_email)
        _log_audit_event(spark, "manager_added", user_email, target_email=email, details=f"Added {email} as manager")
        managers = _get_managers(spark)
        return (
            _build_manager_table(managers),
            "",  # clear input
            dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Added {email} as manager."], color="success", dismissable=True, duration=3000),
        )
    except Exception as e:
        return dash.no_update, dash.no_update, dbc.Alert(f"Failed: {e}", color="danger", dismissable=True)


@callback(
    Output("admin-manager-list", "children", allow_duplicate=True),
    Output("admin-status", "children", allow_duplicate=True),
    Input({"type": "remove-manager-btn", "index": dash.ALL}, "n_clicks"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def remove_manager_callback(n_clicks_list, deployer_info):
    ctx = dash.callback_context
    if not ctx.triggered or not any(v for v in n_clicks_list if v):
        return dash.no_update, dash.no_update
    user_email = (deployer_info or {}).get("email", "")
    prop_id = ctx.triggered[0]["prop_id"]
    target_email = json.loads(prop_id.rsplit(".", 1)[0])["index"]
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dash.no_update, dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _remove_manager(spark, target_email)
        _log_audit_event(spark, "manager_removed", user_email, target_email=target_email, details=f"Removed {target_email} as manager")
        managers = _get_managers(spark)
        return (
            _build_manager_table(managers),
            dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Removed {target_email}."], color="success", dismissable=True),
        )
    except Exception:
        return dash.no_update, dbc.Alert(f"Failed: {traceback.format_exc()}", color="danger", dismissable=True)


@callback(
    Output("admin-warehouse-selector", "style"),
    Output("policy-save-no-lock", "style"),
    Output("admin-warehouse-allowlist-selector", "style"),
    Output("admin-recommended-selector", "style"),
    Output("policy-description", "children"),
    Input("warehouse-policy-radio", "value"),
    prevent_initial_call=True,
)
def toggle_warehouse_policy_ui(policy):
    hide = {"display": "none"}
    show = {}
    descriptions = {
        "user_choice": "Users can select any available warehouse.",
        "recommended": "A default warehouse is pre-selected, but users can change it.",
        "allowlist": "Users can only choose from admin-approved warehouses.",
        "admin_locked": "All deployments use a single warehouse. Users cannot change it.",
    }
    desc = html.Small(descriptions.get(policy, ""), style={"color": "#6C757D"})
    if policy == "admin_locked":
        return show, hide, hide, hide, desc
    elif policy == "allowlist":
        return hide, hide, show, hide, desc
    elif policy == "recommended":
        return hide, hide, hide, show, desc
    else:  # user_choice
        return hide, show, hide, hide, desc


@callback(
    Output("admin-status", "children", allow_duplicate=True),
    Input("save-warehouse-policy-btn", "n_clicks"),
    State("warehouse-policy-radio", "value"),
    State("admin-warehouse-dropdown", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def save_warehouse_policy_locked(n_clicks, policy, warehouse_id, deployer_info):
    if not n_clicks:
        return dash.no_update
    user_email = deployer_info.get("email", "") if deployer_info else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _set_setting(spark, "warehouse_policy", policy, user_email)
        if policy == "admin_locked" and warehouse_id:
            _set_setting(spark, "locked_warehouse_id", warehouse_id, user_email)
            # Get warehouse name for display
            try:
                warehouses = _list_warehouses()
                wh = next((w for w in warehouses if w["id"] == warehouse_id), None)
                if wh:
                    _set_setting(spark, "locked_warehouse_name", wh["name"], user_email)
            except Exception:
                pass
        _log_audit_event(spark, "policy_change", user_email, details=f"Warehouse policy set to '{policy}'" + (f" (warehouse={warehouse_id})" if warehouse_id else ""))
        return dbc.Alert([html.I(className="fas fa-check-circle me-1"), "Warehouse policy saved."], color="success", dismissable=True)
    except Exception:
        return dbc.Alert(f"Failed to save: {traceback.format_exc()}", color="danger", dismissable=True)


@callback(
    Output("admin-status", "children", allow_duplicate=True),
    Input("save-policy-user-choice-btn", "n_clicks"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def save_warehouse_policy_user_choice(n_clicks, deployer_info):
    if not n_clicks:
        return dash.no_update
    user_email = deployer_info.get("email", "") if deployer_info else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _set_setting(spark, "warehouse_policy", "user_choice", user_email)
        _log_audit_event(spark, "policy_change", user_email, details="Warehouse policy set to 'user_choice'")
        return dbc.Alert([html.I(className="fas fa-check-circle me-1"), "Warehouse policy saved — users can choose their own warehouse."], color="success", dismissable=True)
    except Exception:
        return dbc.Alert(f"Failed to save: {traceback.format_exc()}", color="danger", dismissable=True)


@callback(
    Output("admin-status", "children", allow_duplicate=True),
    Input("save-allowlist-policy-btn", "n_clicks"),
    State("admin-warehouse-allowlist-dropdown", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def save_warehouse_policy_allowlist(n_clicks, selected_ids, deployer_info):
    """Save allowlist warehouse policy — only selected warehouses appear in the Build tab."""
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "") if isinstance(deployer_info, dict) else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _set_setting(spark, "warehouse_policy", "allowlist", user_email)
        _set_setting(spark, "warehouse_allowlist", json.dumps(selected_ids or []), user_email)
        _log_audit_event(spark, "policy_change", user_email, details=f"Set warehouse policy to allowlist ({len(selected_ids or [])} warehouses)")
        return dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Allowlist policy saved — {len(selected_ids or [])} warehouses allowed."], color="success", dismissable=True, duration=3000)
    except Exception:
        return dbc.Alert(f"Failed: {traceback.format_exc()}", color="danger", dismissable=True)


@callback(
    Output("admin-status", "children", allow_duplicate=True),
    Input("save-recommended-policy-btn", "n_clicks"),
    State("admin-recommended-dropdown", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def save_warehouse_policy_recommended(n_clicks, warehouse_id, deployer_info):
    """Save recommended warehouse policy — pre-selects a warehouse but users can override."""
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "") if isinstance(deployer_info, dict) else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _set_setting(spark, "warehouse_policy", "recommended", user_email)
        _set_setting(spark, "recommended_warehouse_id", warehouse_id or "", user_email)
        # Store warehouse name for display on Build tab
        if warehouse_id:
            try:
                warehouses = _list_warehouses()
                wh = next((w for w in warehouses if w["id"] == warehouse_id), None)
                if wh:
                    _set_setting(spark, "recommended_warehouse_name", wh["name"], user_email)
            except Exception:
                pass
        _log_audit_event(spark, "policy_change", user_email, details=f"Set warehouse policy to recommended (warehouse={warehouse_id})")
        return dbc.Alert([html.I(className="fas fa-check-circle me-1"), "Recommended policy saved."], color="success", dismissable=True, duration=3000)
    except Exception:
        return dbc.Alert(f"Failed: {traceback.format_exc()}", color="danger", dismissable=True)


# ---------------------------------------------------------------------------
# Catalog Policy
# ---------------------------------------------------------------------------


@callback(
    Output("admin-status", "children", allow_duplicate=True),
    Input("save-catalog-policy-btn", "n_clicks"),
    State("admin-default-catalog-input", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def save_catalog_policy(n_clicks, catalog, deployer_info):
    """Save the default catalog override."""
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "") if isinstance(deployer_info, dict) else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _set_setting(spark, "default_catalog", (catalog or "").strip(), user_email)
        _log_audit_event(
            spark, "policy_change", user_email,
            details=f"Set default catalog to '{(catalog or '').strip() or '(auto-detect)'}'",
        )
        msg = (
            f"Default catalog set to '{catalog.strip()}'."
            if catalog and catalog.strip()
            else "Default catalog cleared — will auto-detect."
        )
        return dbc.Alert(
            [html.I(className="fas fa-check-circle me-1"), msg],
            color="success", dismissable=True, duration=3000,
        )
    except Exception as e:
        return dbc.Alert(f"Failed: {e}", color="danger", dismissable=True)


@callback(
    Output("catalog-restrict-collapse", "is_open"),
    Input("catalog-policy-radio", "value"),
    prevent_initial_call=True,
)
def toggle_catalog_restrict(policy):
    return policy == "restrict"


@callback(
    Output("catalog-policy-radio-status", "children"),
    Input("save-catalog-policy-radio-btn", "n_clicks"),
    State("catalog-policy-radio", "value"),
    State("approved-catalogs-dropdown", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def save_catalog_policy_radio(n_clicks, policy, approved_catalogs, deployer_info):
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "")
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        _set_setting(spark, "catalog_policy", policy, user_email)
        _set_setting(spark, "approved_catalogs", json.dumps(approved_catalogs or []), user_email)
        _log_audit_event(spark, "policy_change", user_email, details=f"Catalog policy set to '{policy}'")
        msg = f"Catalog policy saved — {len(approved_catalogs or [])} catalogs approved." if policy == "restrict" else "Catalog policy saved — all catalogs allowed."
        return dbc.Alert([html.I(className="fas fa-check-circle me-1"), msg], color="success", dismissable=True, duration=3000)
    except Exception as e:
        return dbc.Alert(f"Failed: {e}", color="danger", dismissable=True)


@callback(
    Output("catalog-policy-radio", "value"),
    Output("approved-catalogs-dropdown", "value"),
    Input("admin-sub-tabs", "active_tab"),
    prevent_initial_call=True,
)
def load_catalog_policy(active_tab):
    if active_tab != "admin-warehouses-tab":
        return dash.no_update, dash.no_update
    try:
        spark = _get_spark()
        policy = _get_setting(spark, "catalog_policy") or "allow_all"
        raw = _get_setting(spark, "approved_catalogs") or "[]"
        try:
            approved = json.loads(raw)
        except Exception:
            approved = []
        return policy, approved
    except Exception:
        return "allow_all", []


# ---------------------------------------------------------------------------
# Analytics Dashboard
# ---------------------------------------------------------------------------

EVENT_ICONS = {
    "teardown": "fas fa-trash-alt",
    "manager_added": "fas fa-user-plus",
    "manager_removed": "fas fa-user-minus",
    "policy_change": "fas fa-cog",
}


@callback(
    Output("analytics-content", "children"),
    Output("deployment-summary-content", "children"),
    Input("refresh-analytics-btn", "n_clicks"),
    Input("analytics-timeframe", "value"),
    prevent_initial_call=True,
    running=[
        (Output("refresh-analytics-btn", "disabled"), True, False),
        (Output("refresh-analytics-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Loading..."], [html.I(className="fas fa-sync-alt me-1"), "Refresh"]),
    ],
)
def refresh_analytics(n_clicks, timeframe):
    try:
        spark = _get_spark()
        data = _get_deployment_analytics(spark, int(timeframe))
        s = data.get("summary", {})
        total = s.get("total_deploys", 0)
        active = s.get("active_count", 0)
        failed = s.get("failed_count", 0)

        # Summary cards
        summary_row = dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(str(total), className="mb-0"), html.Small("Total Deploys", className="text-muted-brand"),
            ]), className="text-center"), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(str(active), className="mb-0", style={"color": "#00A972"}), html.Small("Active", className="text-muted-brand"),
            ]), className="text-center"), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(str(failed), className="mb-0", style={"color": "#DC3545"}), html.Small("Failed", className="text-muted-brand"),
            ]), className="text-center"), md=3),
        ], className="mb-3")

        # Industry breakdown with CSS bars
        per_industry = data.get("per_industry", [])
        max_cnt = max((r["cnt"] for r in per_industry), default=1)
        industry_rows = []
        for r in per_industry:
            pct = (r["cnt"] / max_cnt) * 100 if max_cnt else 0
            industry_rows.append(html.Tr([
                html.Td(r.get("industry", ""), style={"fontSize": "0.85rem"}),
                html.Td(html.Div(style={"background": "#FF3621", "height": "16px", "borderRadius": "4px", "width": f"{pct}%"}), style={"width": "50%"}),
                html.Td(str(r["cnt"]), style={"textAlign": "right", "fontSize": "0.85rem"}),
            ]))
        industry_table = html.Table([
            html.Thead(html.Tr([html.Th("Industry"), html.Th(""), html.Th("Count")])),
            html.Tbody(industry_rows),
        ], className="result-table", style={"width": "100%"}) if industry_rows else html.P("No data", className="text-muted-brand")

        # Per user
        per_user = data.get("per_user", [])
        user_rows = [html.Tr([html.Td(r.get("deployed_by", ""), style={"fontSize": "0.85rem"}), html.Td(str(r["cnt"]), style={"textAlign": "right"})]) for r in per_user]
        user_table = html.Table([
            html.Thead(html.Tr([html.Th("User"), html.Th("Deploys")])),
            html.Tbody(user_rows),
        ], className="result-table", style={"width": "100%"}) if user_rows else html.P("No data", className="text-muted-brand")

        analytics_content = html.Div([
            summary_row,
            html.H6("By Industry", className="mt-3 mb-2"), industry_table,
            html.H6("By User", className="mt-3 mb-2"), user_table,
        ])

        # Build deployment summary
        log_table = _get_log_table(spark)
        where = f"WHERE started_at >= date_sub(current_date(), {int(timeframe)})" if int(timeframe) > 0 else ""
        summary_parts = []
        try:
            detail_row = spark.sql(f"""
                SELECT
                    COALESCE(SUM(total_rows), 0) as total_rows_generated,
                    ROUND(AVG(COALESCE(
                        SIZE(FROM_JSON(tables_json, 'MAP<STRING, BIGINT>')),
                        0
                    )), 1) as avg_tables_per_deploy
                FROM {log_table} {where}
            """).first().asDict()
            total_rows_gen = detail_row.get("total_rows_generated", 0)
            avg_tables = detail_row.get("avg_tables_per_deploy", 0)
            summary_parts.append(dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4(f"{int(total_rows_gen):,}" if total_rows_gen else "0", className="mb-0"),
                    html.Small("Total Rows Generated", className="text-muted-brand"),
                ]), className="text-center"), md=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4(str(avg_tables or 0), className="mb-0"),
                    html.Small("Avg Tables / Deploy", className="text-muted-brand"),
                ]), className="text-center"), md=4),
            ], className="mb-3"))
        except Exception:
            pass

        # Most popular use cases
        try:
            uc_rows = [r.asDict() for r in spark.sql(f"""
                SELECT use_case, COUNT(*) as cnt
                FROM {log_table} {where}
                WHERE use_case IS NOT NULL AND use_case != ''
                GROUP BY use_case ORDER BY cnt DESC LIMIT 5
            """).collect()]
            if uc_rows:
                uc_items = [html.Tr([
                    html.Td(r.get("use_case", "")[:80], style={"fontSize": "0.85rem"}),
                    html.Td(str(r["cnt"]), style={"textAlign": "right", "fontSize": "0.85rem"}),
                ]) for r in uc_rows]
                summary_parts.append(html.H6("Most Popular Use Cases", className="mt-2 mb-2", style={"fontSize": "0.9rem"}))
                summary_parts.append(html.Table([
                    html.Thead(html.Tr([html.Th("Use Case"), html.Th("Count")])),
                    html.Tbody(uc_items),
                ], className="result-table", style={"width": "100%"}))
        except Exception:
            pass

        # Recent failures with error categories
        try:
            fail_rows = [r.asDict() for r in spark.sql(f"""
                SELECT
                    COALESCE(error_category, 'Unknown') as error_category,
                    COUNT(*) as cnt
                FROM {log_table}
                WHERE status = 'failed'
                {('AND ' + where.replace('WHERE ', '')) if where else ''}
                GROUP BY error_category ORDER BY cnt DESC LIMIT 5
            """).collect()]
            if fail_rows:
                fail_items = [html.Tr([
                    html.Td(r.get("error_category", "Unknown"), style={"fontSize": "0.85rem"}),
                    html.Td(str(r["cnt"]), style={"textAlign": "right", "fontSize": "0.85rem", "color": "#DC3545"}),
                ]) for r in fail_rows]
                summary_parts.append(html.H6("Failure Categories", className="mt-3 mb-2", style={"fontSize": "0.9rem"}))
                summary_parts.append(html.Table([
                    html.Thead(html.Tr([html.Th("Error Category"), html.Th("Count")])),
                    html.Tbody(fail_items),
                ], className="result-table", style={"width": "100%"}))
        except Exception:
            pass

        deployment_summary = html.Div(summary_parts) if summary_parts else html.P("No deployment data available.", className="text-muted-brand")

        return analytics_content, deployment_summary
    except Exception as e:
        return dbc.Alert(f"Failed to load analytics: {e}", color="danger"), dash.no_update


# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------


@callback(
    Output("audit-trail-content", "children"),
    Input("refresh-audit-btn", "n_clicks"),
    prevent_initial_call=True,
    running=[
        (Output("refresh-audit-btn", "disabled"), True, False),
        (Output("refresh-audit-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Loading..."], [html.I(className="fas fa-sync-alt me-1"), "Refresh"]),
    ],
)
def refresh_audit_trail(n_clicks):
    if not n_clicks:
        return dash.no_update
    try:
        spark = _get_spark()
        events = _get_recent_activity(spark, limit=30)
        if not events:
            return html.P("No recent activity.", className="text-muted-brand")
        items = []
        for ev in events:
            icon = EVENT_ICONS.get(ev.get("event_type", ""), "fas fa-circle")
            desc = ev.get("details", ev.get("event_type", ""))
            items.append(html.Div([
                html.I(className=f"{icon} me-2", style={"color": "#6C757D", "width": "20px"}),
                html.Span(ev.get("actor_email", ""), style={"fontWeight": "600", "fontSize": "0.85rem"}),
                html.Span(f" — {desc}", style={"fontSize": "0.85rem", "color": "#6C757D"}),
                html.Small(f"  {ev.get('event_at', '')}", style={"color": "#ADB5BD", "marginLeft": "0.5rem"}),
            ], className="mb-2", style={"borderLeft": "3px solid #DEE2E6", "paddingLeft": "0.75rem"}))
        return html.Div(items)
    except Exception:
        return html.P("Failed to load activity.", className="text-muted-brand")


# ---------------------------------------------------------------------------
# Stale Deployment Cleanup
# ---------------------------------------------------------------------------


@callback(
    Output("cleanup-status", "children"),
    Input("cleanup-stale-btn", "n_clicks"),
    State("cleanup-age-threshold", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
    running=[
        (Output("cleanup-stale-btn", "disabled"), True, False),
        (Output("cleanup-stale-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Cleaning..."], [html.I(className="fas fa-trash-alt me-1"), "Clean Up All"]),
    ],
)
def cleanup_stale_deployments(n_clicks, age_threshold, deployer_info):
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "")
    try:
        from datetime import datetime, timezone, timedelta
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        ws = _get_workspace_client()
        import genie_factory
        from genie_factory import teardown

        threshold_days = int(age_threshold)
        cutoff = datetime.now(timezone.utc) - timedelta(days=threshold_days)
        all_active = _get_active_deployments(spark, is_manager=True)
        stale = []
        for dep in all_active:
            try:
                dep_date = datetime.strptime(dep.get("deployed_at", ""), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                if dep_date < cutoff:
                    stale.append(dep)
            except (ValueError, TypeError):
                continue

        if not stale:
            return dbc.Alert(f"No deployments older than {threshold_days} days found.", color="info", dismissable=True)

        torn = []
        failed = []
        for dep in stale:
            dep_id = dep.get("deployment_id", "")
            company = dep.get("company_name", dep_id)
            try:
                teardown_kwargs = {
                    "catalog": dep.get("catalog", ""),
                    "schema": dep.get("schema_name", dep.get("schema", "")),
                    "fqn": dep.get("fqn", ""),
                    "genie": {"space_id": dep.get("genie_space_id", "")},
                }
                teardown(spark, workspace_client=ws, **teardown_kwargs)
                _mark_torn_down(spark, dep_id, torn_down_by=user_email)
                _log_audit_event(spark, "teardown", user_email, target_deployment_id=dep_id, details=f"Stale cleanup: tore down '{company}' (>{threshold_days}d)")
                torn.append(company)
            except Exception as e:
                failed.append(f"{company}: {e}")

        alerts = []
        if torn:
            alerts.append(dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Cleaned up {len(torn)} stale deployment(s): {', '.join(torn)}"], color="success", dismissable=True))
        if failed:
            alerts.append(dbc.Alert([html.I(className="fas fa-exclamation-circle me-1"), f"Failed: {'; '.join(failed)}"], color="danger", dismissable=True))
        return html.Div(alerts)
    except Exception:
        return dbc.Alert(f"Cleanup failed: {traceback.format_exc()}", color="danger", dismissable=True)


# ---------------------------------------------------------------------------
# Warehouse Management
# ---------------------------------------------------------------------------


@callback(
    Output("admin-wh-select-dropdown", "options", allow_duplicate=True),
    Input("refresh-admin-warehouses-btn", "n_clicks"),
    prevent_initial_call=True,
    running=[
        (Output("refresh-admin-warehouses-btn", "disabled"), True, False),
        (Output("refresh-admin-warehouses-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Loading..."], [html.I(className="fas fa-sync-alt me-1"), "Refresh"]),
    ],
)
def refresh_admin_warehouses(n_clicks):
    if not n_clicks:
        return dash.no_update
    try:
        warehouses = _list_warehouses()
        if not warehouses:
            return []
        return [{"label": f"{wh['name']} ({wh['state']})", "value": wh["id"]} for wh in warehouses]
    except Exception as e:
        logger.error("Failed to load warehouses: %s", e)
        return []


@callback(
    Output("admin-wh-detail-panel", "children"),
    Input("admin-wh-select-dropdown", "value"),
    State("admin-wh-select-dropdown", "options"),
    prevent_initial_call=True,
)
def show_warehouse_detail(wh_id, options):
    if not wh_id:
        return ""
    try:
        warehouses = _list_warehouses()
        wh = next((w for w in warehouses if w["id"] == wh_id), None)
        if not wh:
            return html.P("Warehouse not found.", className="text-muted-brand")

        state_color = {"RUNNING": "success", "STOPPED": "secondary", "STARTING": "warning", "STOPPING": "warning"}.get(wh["state"], "secondary")

        # Action buttons
        actions = []
        if wh["state"] == "STOPPED":
            actions.append(dbc.Button([html.I(className="fas fa-play me-1"), "Start"],
                id={"type": "admin-wh-action", "index": f"start:{wh['id']}"}, color="success", outline=True, size="sm", className="me-2"))
        elif wh["state"] == "RUNNING":
            actions.append(dbc.Button([html.I(className="fas fa-stop me-1"), "Stop"],
                id={"type": "admin-wh-action", "index": f"stop:{wh['id']}"}, color="warning", outline=True, size="sm", className="me-2"))
        actions.append(dbc.Button([html.I(className="fas fa-trash-alt me-1"), "Delete"],
            id={"type": "admin-wh-action", "index": f"delete:{wh['id']}"}, color="danger", outline=True, size="sm"))

        return dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Small("State", className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                        dbc.Badge(wh["state"], color=state_color),
                    ], md=3),
                    dbc.Col([
                        html.Small("Size", className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                        html.Span(wh.get("cluster_size", "Unknown"), style={"fontSize": "0.9rem"}),
                    ], md=3),
                    dbc.Col([
                        html.Small("Type", className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                        html.Span("Serverless" if wh.get("enable_serverless_compute") else "Classic", style={"fontSize": "0.9rem"}),
                    ], md=3),
                    dbc.Col(html.Div(actions), md=3, className="d-flex align-items-center justify-content-end"),
                ]),
            ], style={"padding": "0.75rem"}),
        ], className="mt-2")
    except Exception as e:
        return dbc.Alert(f"Error: {e}", color="danger")


@callback(
    Output("admin-wh-status", "children"),
    Output("admin-wh-select-dropdown", "options", allow_duplicate=True),
    Input({"type": "admin-wh-action", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def admin_warehouse_action(n_clicks_list):
    if not any(v for v in n_clicks_list if v):
        return dash.no_update, dash.no_update
    triggered = dash.ctx.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return dash.no_update, dash.no_update
    action_wh = triggered["index"]  # "start:wh_id", "stop:wh_id", or "delete:wh_id"
    action, wh_id = action_wh.split(":", 1)
    try:
        ws = _get_workspace_client()
        if action == "start":
            ws.warehouses.start(wh_id)
            msg = dbc.Alert("Warehouse starting...", color="success", dismissable=True, duration=3000)
        elif action == "stop":
            ws.warehouses.stop(wh_id)
            msg = dbc.Alert("Warehouse stopping...", color="warning", dismissable=True, duration=3000)
        elif action == "delete":
            ws.warehouses.delete(wh_id)
            msg = dbc.Alert("Warehouse deleted.", color="info", dismissable=True, duration=3000)
        else:
            msg = ""
        # Refresh dropdown options after action
        try:
            warehouses = _list_warehouses()
            updated_options = [{"label": f"{wh['name']} ({wh['state']})", "value": wh["id"]} for wh in warehouses]
        except Exception:
            updated_options = dash.no_update
        return msg, updated_options
    except Exception as e:
        return dbc.Alert(f"Failed: {e}", color="danger", dismissable=True), dash.no_update


@callback(
    Output("admin-wh-status", "children", allow_duplicate=True),
    Input("admin-create-wh-btn", "n_clicks"),
    State("admin-new-wh-name", "value"),
    State("admin-new-wh-size", "value"),
    prevent_initial_call=True,
)
def admin_create_warehouse(n_clicks, name, size):
    if not n_clicks or not name:
        return dash.no_update
    try:
        ws = _get_workspace_client()
        ws.warehouses.create(
            name=name,
            cluster_size=size,
            warehouse_type="PRO",
            enable_serverless_compute=True,
            auto_stop_mins=10,
        )
        return dbc.Alert(f"Created warehouse '{name}'", color="success", dismissable=True, duration=3000)
    except Exception as e:
        return dbc.Alert(f"Failed to create: {e}", color="danger", dismissable=True)


# ---------------------------------------------------------------------------
# Bulk Teardown Callbacks
# ---------------------------------------------------------------------------


@callback(
    Output("teardown-user-dropdown", "options"),
    Input("admin-sub-tabs", "active_tab"),
    prevent_initial_call=True,
)
def lazy_load_teardown_users(active_tab):
    """Populate the teardown-by-user dropdown when the Bulk Teardown tab is selected."""
    if active_tab != "admin-bulk-tab":
        return dash.no_update
    try:
        spark = _get_spark()
        deployments = _get_active_deployments(spark, is_manager=True)
        users = sorted(set(d.get("deployed_by", "") for d in deployments if d.get("deployed_by")))
        return [{"label": u, "value": u} for u in users]
    except Exception:
        return []


@callback(
    Output("teardown-user-status", "children"),
    Input("teardown-by-user-btn", "n_clicks"),
    State("teardown-user-dropdown", "value"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
    running=[
        (Output("teardown-by-user-btn", "disabled"), True, False),
        (Output("teardown-by-user-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Working..."], [html.I(className="fas fa-trash-alt me-1"), "Teardown All"]),
    ],
)
def teardown_by_user(n_clicks, target_email, deployer_info):
    """Teardown all active deployments for a specific user."""
    if not n_clicks or not target_email:
        return dash.no_update
    actor = (deployer_info or {}).get("email", "")
    try:
        spark = _get_spark()
        if not _is_manager(spark, actor):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        ws = _get_workspace_client()
        deployments = _get_active_deployments(spark, is_manager=True)
        user_deps = [d for d in deployments if d.get("deployed_by") == target_email]
        if not user_deps:
            return dbc.Alert(f"No active deployments found for {target_email}.", color="info", dismissable=True)
        count = 0
        errors = []
        for dep in user_deps:
            dep_id = dep.get("deployment_id", "")
            company = dep.get("company_name", dep_id)
            try:
                import genie_factory
                from genie_factory import teardown
                teardown_kwargs = {
                    "catalog": dep.get("catalog", ""),
                    "schema": dep.get("schema_name", dep.get("schema", "")),
                    "fqn": dep.get("fqn", ""),
                    "genie": {"space_id": dep.get("genie_space_id", "")},
                }
                teardown(spark, workspace_client=ws, **teardown_kwargs)
                _mark_torn_down(spark, dep_id, torn_down_by=actor)
                _log_audit_event(spark, "teardown", actor, target_deployment_id=dep_id, details=f"Bulk teardown for user {target_email}")
                count += 1
            except Exception as e:
                errors.append(f"{company}: {e}")
        alerts = []
        if count:
            alerts.append(dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Torn down {count} deployment(s) for {target_email}."], color="success", dismissable=True))
        if errors:
            alerts.append(dbc.Alert([html.I(className="fas fa-exclamation-circle me-1"), f"Failed: {'; '.join(errors)}"], color="danger", dismissable=True))
        return html.Div(alerts)
    except Exception as e:
        return dbc.Alert(f"Failed: {e}", color="danger", dismissable=True)


@callback(
    Output("teardown-all-status", "children"),
    Input("teardown-all-btn", "n_clicks"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
    running=[
        (Output("teardown-all-btn", "disabled"), True, False),
        (Output("teardown-all-btn", "children"), [html.I(className="fas fa-spinner fa-spin me-1"), "Working..."], [html.I(className="fas fa-skull-crossbones me-1"), "Teardown Everything"]),
    ],
)
def teardown_all_deployments(n_clicks, deployer_info):
    """Teardown ALL active deployments across all users."""
    if not n_clicks:
        return dash.no_update
    actor = (deployer_info or {}).get("email", "")
    try:
        spark = _get_spark()
        if not _is_manager(spark, actor):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        ws = _get_workspace_client()
        deployments = _get_active_deployments(spark, is_manager=True)
        if not deployments:
            return dbc.Alert("No active deployments found.", color="info", dismissable=True)
        count = 0
        errors = []
        for dep in deployments:
            dep_id = dep.get("deployment_id", "")
            company = dep.get("company_name", dep_id)
            try:
                import genie_factory
                from genie_factory import teardown
                teardown_kwargs = {
                    "catalog": dep.get("catalog", ""),
                    "schema": dep.get("schema_name", dep.get("schema", "")),
                    "fqn": dep.get("fqn", ""),
                    "genie": {"space_id": dep.get("genie_space_id", "")},
                }
                teardown(spark, workspace_client=ws, **teardown_kwargs)
                _mark_torn_down(spark, dep_id, torn_down_by=actor)
                _log_audit_event(spark, "teardown", actor, target_deployment_id=dep_id, details="Bulk teardown all")
                count += 1
            except Exception as e:
                errors.append(f"{company}: {e}")
        alerts = []
        if count:
            alerts.append(dbc.Alert([html.I(className="fas fa-check-circle me-1"), f"Torn down {count} deployment(s)."], color="success", dismissable=True))
        if errors:
            alerts.append(dbc.Alert([html.I(className="fas fa-exclamation-circle me-1"), f"Failed: {'; '.join(errors)}"], color="danger", dismissable=True))
        return html.Div(alerts)
    except Exception as e:
        return dbc.Alert(f"Failed: {e}", color="danger", dismissable=True)


# ---------------------------------------------------------------------------
# Reset Backend Tables
# ---------------------------------------------------------------------------

@callback(
    Output("reset-backend-status", "children"),
    Input("reset-backend-btn", "n_clicks"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def reset_backend_tables(n_clicks, deployer_info):
    """Drop and recreate all backend metadata tables."""
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "") if isinstance(deployer_info, dict) else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        fqn = _get_meta_fqn(spark)
        dropped = []
        for table in ["app_managers", "app_settings", "deployment_log", "audit_log"]:
            try:
                spark.sql(f"DROP TABLE IF EXISTS {fqn}.{table}")
                dropped.append(table)
            except Exception as e:
                logger.warning("Failed to drop %s.%s: %s", fqn, table, e)
        from services.admin import _ensure_managers_table, _ensure_settings_table
        from services.deployment import _ensure_log_table
        _ensure_managers_table(spark)
        _ensure_settings_table(spark)
        _ensure_log_table(spark)
        _ensure_first_admin(spark, user_email)
        return dbc.Alert(
            [html.I(className="fas fa-check-circle me-1"),
             f"Backend tables reset. Dropped: {', '.join(dropped)}. You have been re-added as admin."],
            color="success", dismissable=True,
        )
    except Exception as e:
        return dbc.Alert(f"Reset failed: {e}", color="danger", dismissable=True)


# ---------------------------------------------------------------------------
# Drop Backend Tables (without recreating)
# ---------------------------------------------------------------------------

@callback(
    Output("drop-backend-status", "children"),
    Input("drop-backend-btn", "n_clicks"),
    State("deployer-name-store", "data"),
    prevent_initial_call=True,
)
def drop_backend_tables(n_clicks, deployer_info):
    """Drop all backend metadata tables permanently."""
    if not n_clicks:
        return dash.no_update
    user_email = (deployer_info or {}).get("email", "") if isinstance(deployer_info, dict) else ""
    try:
        spark = _get_spark()
        if not _is_manager(spark, user_email):
            return dbc.Alert("Permission denied.", color="danger", dismissable=True)
        fqn = _get_meta_fqn(spark)
        dropped = []
        for table in ["app_managers", "app_settings", "deployment_log", "audit_log"]:
            try:
                spark.sql(f"DROP TABLE IF EXISTS {fqn}.{table}")
                dropped.append(table)
            except Exception as e:
                logger.warning("Failed to drop %s.%s: %s", fqn, table, e)
        try:
            spark.sql(f"DROP SCHEMA IF EXISTS {fqn}")
            dropped.append(fqn)
        except Exception as e:
            logger.warning("Failed to drop schema %s: %s", fqn, e)
        return dbc.Alert(
            [html.I(className="fas fa-check-circle me-1"),
             f"Dropped: {', '.join(dropped)}. Backend tables have been permanently removed."],
            color="warning", dismissable=True,
        )
    except Exception as e:
        return dbc.Alert(f"Drop failed: {e}", color="danger", dismissable=True)
