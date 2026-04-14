"""UI builder functions for deployment cards, result cards, and admin tables.

These functions accept plain dicts and return Dash component trees.
No service or SDK imports — safe to import from any callback module.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import dash_bootstrap_components as dbc
from dash import html

_CODE_STYLE = {
    "color": "#FF3621",
    "fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
    "fontSize": "0.8rem",
}


def _deployment_age_badge(deployed_at_str: str) -> tuple:
    """Return (text, badge_color) for deployment age."""
    if not deployed_at_str:
        return "Unknown", "secondary"
    try:
        deployed_at = datetime.strptime(deployed_at_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - deployed_at).days
    except (ValueError, TypeError):
        return "Unknown", "secondary"

    if days == 0:
        text = "Today"
    elif days == 1:
        text = "Yesterday"
    elif days < 7:
        text = f"{days}d ago"
    elif days < 30:
        text = f"{days // 7}w ago"
    else:
        text = f"{days // 30}mo ago"

    if days < 7:
        color = "success"
    elif days < 30:
        color = "warning"
    else:
        color = "danger"

    return text, color


def _faq_item(question: str, answer) -> dbc.AccordionItem:
    return dbc.AccordionItem(answer, title=question)


def _build_success_card(result: dict[str, Any]) -> dbc.CardBody:
    """Build the success result card with Genie space link."""
    tables = result.get("tables", {})
    total_rows = sum(tables.values())
    mv_count = len(result.get("metric_view_fqdns", {}))
    genie_url = result.get("genie_url", "")
    genie = result.get("genie", {})
    genie_status = genie.get("status", "") if isinstance(genie, dict) else getattr(genie, "status", "")

    table_rows = [
        html.Tr([html.Td(name, className="mono"), html.Td(f"{count:,} rows", style={"textAlign": "right"})])
        for name, count in tables.items()
    ]
    table_rows.append(html.Tr(
        [html.Td("Total", style={"fontWeight": "700"}), html.Td(f"{total_rows:,} rows", style={"textAlign": "right", "fontWeight": "700"})],
        style={"borderTop": "2px solid #1B3139"},
    ))

    genie_failed = genie_status in ("failed", "skipped") or (not genie_url and genie_status != "created")
    genie_reason = ""
    if isinstance(genie, dict):
        genie_reason = genie.get("reason", "")

    body_children = []

    # Genie failure alert
    if genie_failed:
        body_children.append(dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            html.Strong("Genie Space creation failed. "),
            html.Span("Data and schema were created successfully, but the Genie room could not be provisioned. "),
            html.Span("This is usually a transient issue — try deploying again. "),
            *([html.Details([
                html.Summary("Error details", style={"cursor": "pointer", "fontSize": "0.85rem"}),
                html.Pre(genie_reason, style={"fontSize": "0.8rem", "marginTop": "0.5rem", "whiteSpace": "pre-wrap"}),
            ])] if genie_reason else []),
        ], color="warning", className="mb-3"))

    # Genie Space Link (prominent) — always visible
    if genie_url:
        body_children.append(
            html.Div([
                html.A(
                    [html.Img(src="/assets/genie-icon.svg", height="40px", style={"marginRight": "0.75rem", "verticalAlign": "middle"}),
                     "Open Genie Space",
                     html.I(className="fas fa-external-link-alt ms-2", style={"fontSize": "0.85rem"})],
                    href=genie_url, target="_blank", className="btn-genie-prominent",
                ),
            ], className="text-center my-3"),
        )

    # Collapsible details section
    details_content = html.Div([
        html.Hr(className="section-divider"),
        # Header
        html.H6([html.I(className="fas fa-info-circle me-2"), "Deployment Details"], className="mb-3", style={"color": "#1B3139"}),
        # Two-column summary
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Small("SCHEMA", className="form-label d-block"),
                    html.Code(result.get("fqn", ""), style=_CODE_STYLE),
                ], className="mb-3"),
                html.Div([
                    html.Small("CATALOG", className="form-label d-block"),
                    html.Span(result.get("catalog", ""), style={"fontSize": "0.9rem"}),
                ]),
            ], md=6),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Div(str(len(tables)), style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#1B3139"}),
                        html.Small("Tables", className="text-muted-brand"),
                    ], className="text-center"),
                    dbc.Col([
                        html.Div(f"{total_rows:,}", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#1B3139"}),
                        html.Small("Total Rows", className="text-muted-brand"),
                    ], className="text-center"),
                    dbc.Col([
                        html.Div(str(mv_count), style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#1B3139"}),
                        html.Small("Metric Views", className="text-muted-brand"),
                    ], className="text-center"),
                ]),
            ], md=6),
        ], className="mb-3"),
        # Table breakdown
        dbc.Table([
            html.Thead(html.Tr([
                html.Th("Table", style={"fontSize": "0.75rem", "textTransform": "uppercase", "color": "#6C757D"}),
                html.Th("Rows", style={"fontSize": "0.75rem", "textTransform": "uppercase", "color": "#6C757D", "textAlign": "right"}),
            ])),
            html.Tbody([
                html.Tr([html.Td(name, style={"fontFamily": "monospace", "fontSize": "0.85rem"}), html.Td(f"{count:,}", style={"textAlign": "right"})]) for name, count in tables.items()
            ] + [
                html.Tr([
                    html.Td("Total", style={"fontWeight": "700"}),
                    html.Td(f"{total_rows:,}", style={"textAlign": "right", "fontWeight": "700"}),
                ], style={"borderTop": "2px solid #1B3139"}),
            ]),
        ], bordered=False, hover=True, size="sm", className="mb-0"),
    ], className="mt-2")

    body_children.append(
        html.Details(
            [html.Summary("Show deployment details", style={"cursor": "pointer", "fontSize": "0.85rem", "color": "#6C757D"}),
             details_content],
            className="mt-2",
        )
    )

    # Build Another button — always visible
    body_children.extend([
        html.Hr(className="section-divider"),
        dbc.Button(
            [html.I(className="fas fa-plus me-2"), "Build Another"],
            id="deploy-another-btn", color="secondary", outline=True,
        ),
    ])

    return dbc.CardBody(body_children)


def _build_error_card(error_msg: str) -> dbc.Card:
    return dbc.Card([
        dbc.CardHeader([html.I(className="fas fa-exclamation-circle me-2", style={"color": "#DC3545"}), "Deployment Failed"]),
        dbc.CardBody([
            html.P("An error occurred:"),
            html.Pre(error_msg, style={"background": "#1B3139", "color": "#F8F9FA", "padding": "1rem", "borderRadius": "8px", "fontSize": "0.85rem", "whiteSpace": "pre-wrap", "maxHeight": "300px", "overflowY": "auto"}),
        ]),
    ], className="error-card")


def _serialize_result(result: dict[str, Any]) -> dict[str, Any]:
    """Make deployment result JSON-serializable."""
    store = {}
    for key, value in result.items():
        if key == "genie":
            if hasattr(value, "__dict__"):
                store[key] = {k: v for k, v in value.__dict__.items() if not k.startswith("_")}
            elif isinstance(value, dict):
                store[key] = value
            else:
                store[key] = str(value)
        elif isinstance(value, dict):
            store[key] = {str(k): v for k, v in value.items()}
        else:
            try:
                json.dumps(value)
                store[key] = value
            except (TypeError, ValueError):
                store[key] = str(value)
    return store


def _build_empty_state() -> html.Div:
    """Build a friendly empty state for the manage tab."""
    return html.Div([
        html.Div(html.I(className="fas fa-rocket", style={"fontSize": "3rem", "color": "#DEE2E6"}), className="text-center mb-3"),
        html.P("No active deployments yet.", className="text-center text-muted-brand", style={"fontSize": "1.1rem"}),
        html.P("Switch to the Build tab to create your first Genie Space.", className="text-center text-muted-brand", style={"fontSize": "0.9rem"}),
    ], style={"padding": "3rem 1rem"})


def _build_deployments_table(deployments: list[dict]) -> html.Div:
    """Build the active deployments as card-based list with per-row teardown."""
    cards = []

    for dep in deployments:
        tables_json = dep.get("tables_json", "{}")
        try:
            tables_dict = json.loads(tables_json) if isinstance(tables_json, str) else {}
        except Exception:
            tables_dict = {}
        num_tables = len(tables_dict)

        genie_title = dep.get("genie_space_title", "") or dep.get("company_name", "Genie Space")
        deployed_by = dep.get("deployed_by", "unknown")
        dep_id = dep.get("deployment_id", "")
        use_case = dep.get("use_case", "")
        biz_context = dep.get("business_context", "")
        fqn = dep.get("fqn", "")

        age_text, age_color = _deployment_age_badge(dep.get("deployed_at", ""))
        age_badge = dbc.Badge(age_text, color=age_color, className="ms-2", style={"fontSize": "0.7rem"})

        clone_btn = dbc.Button(
            [html.I(className="fas fa-clone me-1"), "Clone"],
            id={"type": "clone-deploy-btn", "index": dep_id},
            color="secondary", outline=True, size="sm", className="me-2",
        )

        teardown_btn = dbc.Button(
            [html.I(className="fas fa-trash-alt me-1"), "Teardown"],
            id={"type": "teardown-row-btn", "index": dep_id},
            color="danger", outline=True, size="sm",
        )

        # Header stats: table count + row count
        total_rows = dep.get("total_rows", 0)
        if not total_rows and tables_dict:
            total_rows = sum(tables_dict.values())
        header_stats = None
        if total_rows:
            header_stats = html.Div(
                f"{num_tables} tables \u00b7 {total_rows:,} rows",
                style={"fontSize": "0.8rem", "color": "#6C757D", "marginTop": "0.25rem"},
            )

        detail_items = []
        if use_case:
            detail_items.append(html.Div([html.Strong("Use Case: "), html.Span(use_case)], style={"fontSize": "0.85rem"}))
        if biz_context:
            detail_items.append(html.Div([html.Strong("Business Context: "), html.Span(biz_context)], style={"fontSize": "0.85rem", "color": "#6C757D"}))
        if tables_dict:
            table_list = [
                html.Li([html.Span(tname, style=_CODE_STYLE), f": {count:,} rows"], style={"fontSize": "0.85rem"})
                for tname, count in tables_dict.items()
            ]
            detail_items.append(html.Div([html.Strong(f"Tables ({num_tables}):"), html.Ul(table_list, style={"marginBottom": "0"})], style={"fontSize": "0.85rem", "marginTop": "0.25rem"}))

        card_body_children = [
            # Top row: checkbox + company name + age badge + clone + teardown
            dbc.Row([
                dbc.Col(dbc.Checkbox(id={"type": "teardown-checkbox", "index": dep_id}, value=False), width="auto", style={"paddingRight": "0"}),
                dbc.Col([html.H6(dep.get("company_name", ""), className="mb-0 d-inline"), age_badge], width="auto"),
                dbc.Col([clone_btn, teardown_btn], width="auto", className="ms-auto"),
            ], align="center", className="mb-2"),
        ]

        # Header stats row (if available)
        if header_stats:
            card_body_children.append(header_stats)

        card_body_children.extend([
            # Info row
            dbc.Row([
                dbc.Col([
                    html.Small("Schema", className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                    html.Span(fqn, style=_CODE_STYLE),
                ], md=5),
                dbc.Col([
                    html.Small([html.Img(src="/assets/genie-icon.svg", height="20px", style={"marginRight": "0.375rem", "verticalAlign": "middle"}), "Genie Room"], className="text-muted-brand d-block", style={"fontSize": "0.75rem"}),
                    html.Span(genie_title, style=_CODE_STYLE),
                ], md=7),
            ]),
            # Deployed by
            html.Div(
                [html.I(className="fas fa-user me-1", style={"fontSize": "0.7rem"}),
                 html.Span(deployed_by)],
                style={"fontSize": "0.8rem", "color": "#6C757D", "marginTop": "0.5rem"},
            ),
        ])

        if detail_items:
            card_body_children.append(html.Details([
                html.Summary("Details", style={"cursor": "pointer", "fontSize": "0.8rem", "color": "#6C757D", "marginTop": "0.5rem"}),
                html.Div(detail_items, className="mt-2"),
            ]))

        card = dbc.Card([
            dbc.CardBody(card_body_children, style={"padding": "1rem"}),
        ], className="mb-2")
        cards.append(card)

    return html.Div(cards)


def _build_manager_table(managers: list[dict]) -> html.Div:
    """Build a simple table of current managers with remove buttons."""
    if not managers:
        return html.P("No managers configured.", className="text-muted-brand")
    rows = []
    for m in managers:
        rows.append(html.Tr([
            html.Td(m["email"]),
            html.Td(m.get("added_by", ""), style={"fontSize": "0.85rem", "color": "#6C757D"}),
            html.Td(
                dbc.Button([html.I(className="fas fa-times")], id={"type": "remove-manager-btn", "index": m["email"]}, color="danger", outline=True, size="sm"),
                style={"textAlign": "right"},
            ),
        ]))
    return html.Table([
        html.Thead(html.Tr([html.Th("Email"), html.Th("Added By"), html.Th("")])),
        html.Tbody(rows),
    ], className="result-table", style={"width": "100%"})
