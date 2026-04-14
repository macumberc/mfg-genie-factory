"""Dash layout definitions: navbar, tabs, footer, and full page layout."""

import dash_bootstrap_components as dbc
from dash import dcc, html

try:
    from importlib.metadata import version as _pkg_version
    __version__ = _pkg_version("genie-factory")
except Exception:
    __version__ = "0.2.0-dev"

from presets import (
    SUBINDUSTRIES,
    SUBINDUSTRY_USE_CASES,
    SUBINDUSTRY_ICONS,
    DATASET_SIZE_PRESETS,
    DATASET_SIZE_ESTIMATES,
)
from state import _ADMIN_CONTACT_EMAIL
from components.cards import _faq_item
from app_instance import APP_TITLE

# --- Navbar ---

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    html.A(
                        html.Div([
                            html.Img(src="/assets/genie-icon.svg", height="48px", className="navbar-genie-icon"),
                            html.Div([
                                html.Span(APP_TITLE, className="navbar-title"),
                                html.Span("Manufacturing Genie Room Builder", className="navbar-subtitle"),
                            ], className="navbar-title-group"),
                        ], className="d-flex align-items-center"),
                        id="navbar-home-link",
                        href="/",
                        style={"textDecoration": "none", "color": "inherit"},
                    ),
                ),
                dbc.Col(
                    html.Div(id="navbar-user-display", className="navbar-user"),
                    width="auto", className="d-flex align-items-center",
                ),
            ], align="center", className="w-100"),
        ],
        fluid=True,
    ),
    className="navbar-custom mb-4",
)

# ---------------------------------------------------------------------------
# Deploy Tab
# ---------------------------------------------------------------------------

industry_input = dbc.Col([
    dbc.Label("Subindustry", html_for="industry-dropdown", className="form-label"),
    dbc.Select(
        id="industry-dropdown",
        options=[{"label": i, "value": i} for i in SUBINDUSTRIES],
        placeholder="Select a subindustry...",
    ),
    dbc.Input(id="custom-industry-input", type="text", placeholder="Enter custom subindustry...", className="mt-2", style={"display": "none"}),
], md=6)

company_input = dbc.Col([
    dbc.Label("Company Name", html_for="company-input", className="form-label"),
    dbc.Input(id="company-input", type="text", placeholder="e.g. MedFlow Analytics"),
], md=6)

use_case_preset = dbc.Col([
    dbc.Label("Suggested Use Cases", html_for="use-case-preset-dropdown", className="form-label"),
    dcc.Dropdown(
        id="use-case-preset-dropdown",
        placeholder="Select a pre-built use case or type your own below...",
        searchable=True,
        options=[],
    ),
], md=12, className="mt-3")

use_case_input = dbc.Col([
    dbc.Label("Use Case", html_for="use-case-input", className="form-label"),
    dbc.Textarea(id="use-case-input", placeholder="e.g. 'Patient readmission prediction and hospital capacity planning'", rows=2),
    dbc.Tooltip("Describe the analytics use case in 1-2 sentences. More specificity produces better tables and metrics.", target="use-case-input", placement="top"),
], md=12, className="mt-3")

business_context_input = dbc.Col([
    dbc.Label("Business Context", html_for="context-input", className="form-label"),
    dbc.Textarea(id="context-input", placeholder="2-3 sentence scenario: fictional company, operational problem, and quantified impact.", rows=3),
    dbc.Tooltip("Describe a fictional company, its operational problem, and the quantified business impact. More detail produces better synthetic data.", target="context-input", placement="top"),
    html.Small(id="context-char-count", className="text-muted-brand", style={"fontSize": "0.75rem"}),
], md=12, className="mt-3")

advanced_options = dbc.Accordion([
    dbc.AccordionItem(
        html.Div([
            # Warehouse selector
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("SQL Warehouse", html_for="warehouse-dropdown", className="form-label"),
                        dbc.Select(id="warehouse-dropdown", placeholder="Auto-detecting..."),
                    ], md=7),
                    dbc.Col([
                        dbc.Label("Actions", className="form-label", style={"visibility": "hidden"}),
                        html.Div([
                            dbc.Button([html.I(className="fas fa-sync-alt me-1"), "Refresh"], id="refresh-warehouses-btn", color="secondary", outline=True, size="sm", className="me-2"),
                            dbc.Button([html.I(className="fas fa-play me-1"), "Start"], id="start-warehouse-btn", color="success", outline=True, size="sm", disabled=True, className="me-2"),
                            dbc.Button([html.I(className="fas fa-stop me-1"), "Stop"], id="stop-warehouse-btn", color="danger", outline=True, size="sm", disabled=True),
                        ], className="d-flex"),
                    ], md=5),
                ], className="align-items-end"),
                html.Div(id="warehouse-status-badge", className="mt-2"),
                # Hidden placeholders for create warehouse callback IDs
                html.Div([
                    dbc.Input(id="new-warehouse-name", type="hidden"),
                    dbc.Input(id="new-warehouse-size", type="hidden", value="Small"),
                    html.Button(id="create-warehouse-btn", style={"display": "none"}),
                ], style={"display": "none"}),
            ]),
            html.Hr(className="section-divider"),
            # Data generation options
            dbc.Row([
                dbc.Col([
                    dbc.Label("Dataset Size", className="form-label"),
                    dbc.Select(
                        id="dataset-size-dropdown",
                        options=[
                            {"label": "Demo (~1K rows/table)", "value": "demo"},
                            {"label": "Standard (~5K rows/table)", "value": "standard"},
                            {"label": "Large (~15K rows/table)", "value": "large"},
                            {"label": "Custom", "value": "custom"},
                        ],
                        value="standard",
                    ),
                    html.Small(id="dataset-size-estimate", children=DATASET_SIZE_ESTIMATES["standard"],
                               className="text-muted-brand mt-1 d-block", style={"fontSize": "0.8rem"}),
                ], md=4),
                dbc.Col([dbc.Label("Catalog", className="form-label"), dbc.Input(id="catalog-input", type="text", placeholder="Default")], md=4),
                dbc.Col([dbc.Label("Schema", className="form-label"), dbc.Input(id="schema-input", type="text", placeholder="Auto")], md=4),
            ]),
            # Data generation detail fields (always visible, auto-filled by preset)
            dbc.Row([
                dbc.Col([dbc.Label("Tables", className="form-label"), dbc.Input(id="num-tables", type="number", value=3, min=1, max=5)], md=2),
                dbc.Col([dbc.Label("Products", className="form-label"), dbc.Input(id="num-products", type="number", value=20, min=5, max=100)], md=2),
                dbc.Col([dbc.Label("Locations", className="form-label"), dbc.Input(id="num-locations", type="number", value=8, min=2, max=32)], md=2),
                dbc.Col([dbc.Label("Scale (yrs)", className="form-label"), dbc.Input(id="scale-input", type="number", value=1, min=1, max=10)], md=3),
                dbc.Col([dbc.Label("Fact Rows", className="form-label"), dbc.Input(id="target-rows-input", type="number", value=5000, min=100, max=100000, placeholder="Target fact table rows")], md=3),
            ], className="mt-2"),
        ]),
        title="Advanced Options",
    )
], start_collapsed=True, className="mt-3")

intro_card = dbc.Card([
    dbc.CardBody([
        html.H5("How It Works", className="mb-4 text-center"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("1", className="step-circle completed", style={"margin": "0 auto 0.75rem auto"}),
                    html.H6("Configure", className="text-center mb-2"),
                    html.P("Choose an industry, name a fictional company, and describe the analytics use case.",
                           className="text-center", style={"fontSize": "0.85rem", "color": "#6C757D"}),
                ]),
            ], md=4),
            dbc.Col([
                html.Div([
                    html.Div("2", className="step-circle completed", style={"margin": "0 auto 0.75rem auto"}),
                    html.H6("Build", className="text-center mb-2"),
                    html.P("AI generates a domain model, synthetic Delta tables, metric views, and a Genie space.",
                           className="text-center", style={"fontSize": "0.85rem", "color": "#6C757D"}),
                ]),
            ], md=4),
            dbc.Col([
                html.Div([
                    html.Div("3", className="step-circle completed", style={"margin": "0 auto 0.75rem auto"}),
                    html.H6("Demo", className="text-center mb-2"),
                    html.P("Open the Genie space and start asking business questions in natural language.",
                           className="text-center", style={"fontSize": "0.85rem", "color": "#6C757D"}),
                ]),
            ], md=4),
        ]),
        html.Hr(className="section-divider mt-3"),
        html.Div([
            html.Small("Each deployment creates: ", style={"fontWeight": "600"}),
            html.Small("Synthetic Delta tables in Unity Catalog  •  Metric views with governed KPIs  •  A Genie space with sample Q&A",
                       style={"color": "#6C757D"}),
        ], className="text-center"),
    ]),
], className="mb-4")

deploy_button = html.Div(
    dbc.Button(
        [html.I(className="fas fa-rocket me-2"), "Build Genie Space"],
        id="deploy-btn", color="primary", size="lg", className="w-100",
    ),
    id="deploy-btn-wrapper", className="mb-4",
)

def _build_subindustry_grid():
    """Build the static grid of subindustry cards for Quick Deploy."""
    cards = []
    for sub in SUBINDUSTRIES:
        if sub == "Custom":
            continue
        icon = SUBINDUSTRY_ICONS.get(sub, "fa-building")
        count = len(SUBINDUSTRY_USE_CASES.get(sub, []))
        card = dbc.Col(
            html.Div(
                dbc.Card(
                    dbc.CardBody([
                        html.I(className=f"fas {icon}", style={"fontSize": "2rem", "color": "#FF3621"}),
                        html.H6(sub, className="mt-2 mb-1", style={"fontSize": "0.9rem"}),
                        html.Small(f"{count} use cases", className="text-muted-brand"),
                    ], style={"textAlign": "center", "cursor": "pointer", "padding": "1.25rem 0.75rem"}),
                    className="quick-deploy-card h-100",
                ),
                id={"type": "subindustry-card", "index": sub},
                n_clicks=0,
            ),
            md=3, sm=4, xs=6, className="mb-3",
        )
        cards.append(card)
    return dbc.Row(cards)


deploy_tab = dbc.Tab(
    label="🏭 Build",
    tab_id="deploy-tab",
    children=html.Div([
        dcc.Store(id="build-mode-store", data="quick"),
        dcc.Store(id="selected-industry-store", storage_type="memory"),
        html.Div(id="scroll-trigger-dummy", style={"display": "none"}),

        # Quick Deploy view (default)
        html.Div(id="quick-deploy-view", children=[
            html.Div([
                html.P([
                    "Generate a demo-ready Genie space in minutes. ",
                    html.Strong("Pick a subindustry and use case below"),
                    " to get started.",
                ], className="text-muted-brand mb-0", style={"fontSize": "0.95rem"}),
            ], className="mb-3"),
            html.H5("Choose a Subindustry", className="mb-3"),
            _build_subindustry_grid(),
            html.Div(id="use-case-card-area"),
            # Request a use case
            html.Hr(className="section-divider mt-4"),
            dbc.Card([
                dbc.CardBody([
                    html.H6([html.I(className="fas fa-lightbulb me-2", style={"color": "#FF3621"}), "Request a Use Case"], className="mb-2"),
                    html.P("Don't see what you need? Submit a request and we'll add it.", className="text-muted-brand mb-3", style={"fontSize": "0.85rem"}),
                    dbc.Row([
                        dbc.Col(dbc.Input(id="request-uc-email", type="email", placeholder="Your email"), md=4),
                        dbc.Col(dbc.Input(id="request-uc-description", type="text", placeholder="Describe the use case you'd like added"), md=6),
                        dbc.Col(dbc.Button([html.I(className="fas fa-paper-plane me-1"), "Submit"], id="request-uc-btn", color="primary", outline=True, size="sm", className="w-100"), md=2),
                    ], className="g-2 align-items-end"),
                    html.Div(id="request-uc-status", className="mt-2"),
                ]),
            ]),
            # Hidden placeholders for callback IDs that reference custom build links
            html.A(id="switch-to-custom-link-intro", style={"display": "none"}),
            html.A(id="switch-to-custom-link", style={"display": "none"}),
        ]),

        # Custom Build view (hidden by default) -- wraps ALL existing form content
        html.Div(id="custom-build-view", style={"display": "none"}, children=[
            dbc.Row([
                dbc.Col(html.H5("Custom Build", className="mb-0"), width="auto"),
                dbc.Col(
                    html.A([html.I(className="fas fa-bolt me-1"), "Quick Deploy"],
                           id="switch-to-quick-link", href="#",
                           style={"fontSize": "0.9rem", "textDecoration": "none"}),
                    width="auto", className="ms-auto d-flex align-items-center",
                ),
            ], className="mb-3 align-items-center"),
            # Config card with collapsible body
            dbc.Card([
                dbc.CardHeader(html.Div(
                    [html.I(className="fas fa-cog me-2"), "Configuration",
                     html.I(className="fas fa-chevron-down ms-auto", id="config-chevron", style={"transition": "transform 0.2s"})],
                    id="config-card-header",
                    style={"cursor": "pointer"},
                    className="d-flex align-items-center",
                )),
                dbc.Collapse(
                    dbc.CardBody([
                        dbc.Row([industry_input, company_input]),
                        dbc.Row([use_case_preset]),
                        dbc.Row([use_case_input]),
                        dbc.Row([business_context_input]),
                        advanced_options,
                    ]),
                    id="config-collapse",
                    is_open=True,
                ),
                # Summary shown when collapsed during deploy
                html.Div(id="config-summary", style={"display": "none", "padding": "0.5rem 1.25rem", "fontSize": "0.85rem", "color": "#6C757D", "borderTop": "1px solid #DEE2E6"}),
            ], className="mb-4"),
            html.Div(id="warehouse-alert-area"),
            deploy_button,
        ]),

        # Progress and Results cards -- SHARED between both modes (always visible)
        # Progress card with collapsible body
        dbc.Card([
            dbc.CardHeader(html.Div(
                [html.I(className="fas fa-spinner fa-spin me-2", id="progress-header-icon"), "Deployment In Progress",
                 html.I(className="fas fa-chevron-down ms-auto", id="progress-chevron", style={"transition": "transform 0.2s"})],
                id="progress-card-header",
                style={"cursor": "pointer"},
                className="d-flex align-items-center",
            )),
            dbc.Collapse(
                html.Div(id="deploy-progress-area"),
                id="progress-collapse",
                is_open=False,
            ),
        ], id="progress-card-wrapper", className="mb-4", style={"display": "none", "borderLeft": "4px solid #FF3621"}),
        # Results card with collapsible body
        dbc.Card([
            dbc.CardHeader(html.Div(
                [html.I(className="fas fa-check-circle me-2", id="results-header-icon", style={"color": "#00A972"}), html.Span("Deployment Complete", id="results-header-text"),
                 html.I(className="fas fa-chevron-down ms-auto", id="results-chevron", style={"transition": "transform 0.2s"})],
                id="results-card-header",
                style={"cursor": "pointer"},
                className="d-flex align-items-center",
            )),
            dbc.Collapse(
                html.Div(id="deploy-results"),
                id="results-collapse",
                is_open=False,
            ),
        ], id="results-card-wrapper", className="mb-4", style={"display": "none"}),
        dcc.Store(id="warehouse-store", storage_type="memory"),
        dcc.Store(id="deployer-name-store", storage_type="memory"),
        dcc.Store(id="deploy-session-id", storage_type="memory"),
        dcc.Store(id="deploy-params-store", storage_type="memory"),
        dcc.Interval(id="progress-interval", interval=1000, disabled=True),
        dcc.Interval(id="warehouse-refresh-interval", interval=30000, disabled=False),
        # Hidden retry buttons (populated dynamically in error/partial result cards)
        html.Div([
            html.Button(id="retry-deploy-btn", style={"display": "none"}),
            html.Button(id="retry-genie-btn", style={"display": "none"}),
        ], style={"display": "none"}),
    ], className="pt-3"),
)

# ---------------------------------------------------------------------------
# Manage Tab
# ---------------------------------------------------------------------------

manage_tab = dbc.Tab(
    label="📋 Manage",
    tab_id="manage-tab",
    children=html.Div([
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-list me-2"), "Active Deployments"]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dbc.Button([html.I(className="fas fa-sync-alt me-1"), "Refresh"], id="refresh-deployments-btn", color="secondary", outline=True, size="sm"),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Button([html.I(className="fas fa-trash-alt me-1"), "Teardown Selected"], id="teardown-selected-btn", color="danger", outline=True, size="sm", disabled=True),
                        width="auto",
                    ),
                ], className="mb-3 g-2"),
                # Filter and sort controls
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Industry", className="form-label", style={"fontSize": "0.8rem"}),
                        dcc.Dropdown(id="filter-industry-dropdown", placeholder="All",
                                     options=[{"label": i, "value": i} for i in SUBINDUSTRIES if i != "Custom"],
                                     searchable=True, style={"fontSize": "0.85rem"}),
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Age", className="form-label", style={"fontSize": "0.8rem"}),
                        dbc.Select(id="filter-age-dropdown", options=[
                            {"label": "All", "value": "all"},
                            {"label": "< 7 days", "value": "7"},
                            {"label": "7-30 days", "value": "30"},
                            {"label": "> 30 days", "value": "30+"},
                        ], value="all", style={"fontSize": "0.85rem"}),
                    ], md=2),
                    dbc.Col([
                        dbc.Label("Sort", className="form-label", style={"fontSize": "0.8rem"}),
                        dbc.Select(id="sort-dropdown", options=[
                            {"label": "Newest", "value": "date_desc"},
                            {"label": "Oldest", "value": "date_asc"},
                            {"label": "Industry", "value": "industry"},
                            {"label": "Company", "value": "company"},
                        ], value="date_desc", style={"fontSize": "0.85rem"}),
                    ], md=2),
                    dbc.Col([
                        dbc.Label("\u00a0", className="form-label", style={"fontSize": "0.8rem"}),
                        dbc.Checkbox(id="select-all-checkbox", label="Select All", value=False),
                    ], md=2),
                ], className="mb-3"),
                dcc.Loading(
                    id="loading-deployments",
                    type="default",
                    children=html.Div(id="deployments-list"),
                    color="#FF3621",
                ),
                html.Div(id="teardown-status", className="mt-3"),
            ]),
        ], className="mb-4"),
        dcc.Store(id="deployments-store", storage_type="memory"),
        dcc.Store(id="teardown-target", storage_type="memory"),
        dcc.ConfirmDialog(id="teardown-confirm", message="This will permanently drop the schema (CASCADE) and delete the Genie space. Are you sure?"),
    ], className="pt-3"),
)

# ---------------------------------------------------------------------------
# FAQ & Help Tab
# ---------------------------------------------------------------------------

faq_tab = dbc.Tab(
    label="❓ FAQ & Help",
    tab_id="faq-tab",
    children=html.Div([
        # Getting Started
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-play-circle me-2"), "Getting Started"]),
            dbc.CardBody([
                dbc.Accordion([
                    _faq_item("How do I deploy a Genie space?", html.P(
                        "Pick a subindustry from the grid on the Build tab, choose a use case, and click Deploy Now. "
                        "The space will be ready in about 2 minutes. You'll get a direct link to the Genie space when it's done."
                    )),
                    _faq_item("What gets created during a deployment?", html.Div([
                        html.P("Each deployment creates the following in your workspace:"),
                        html.Ul([
                            html.Li("A Unity Catalog schema with 3 synthetic Delta tables (transaction, snapshot, and forecast)"),
                            html.Li("2 metric views with governed KPI definitions (MEASURE syntax)"),
                            html.Li("A fully configured Genie space with sample questions, example SQL, benchmarks, and domain instructions"),
                        ]),
                    ])),
                    _faq_item("How do I request a new use case?", html.P(
                        "Use the Request a Use Case form at the bottom of the Build tab. Enter your email and a short description "
                        "of the use case you'd like added. We review requests regularly and add new pre-built specs."
                    )),
                    _faq_item("Can I deploy the same use case multiple times?", html.P(
                        "Yes. Each deployment gets its own schema and Genie space, so you can deploy the same use case "
                        "as many times as you like. This is useful when demoing to different customers or teams."
                    )),
                ], start_collapsed=True, always_open=True),
            ]),
        ], className="mb-4"),
        # Demos & Usage
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-presentation-screen me-2"), "Demos & Usage"]),
            dbc.CardBody([
                dbc.Accordion([
                    _faq_item("How should I demo a Genie space to a customer?", html.Div([
                        html.P("Tips for effective customer demos:"),
                        html.Ul([
                            html.Li("Start with the sample questions -- they're designed to showcase the data and metric views"),
                            html.Li("Show dimension filters by asking follow-ups like 'What about just the Northeast region?'"),
                            html.Li("Highlight the metric views -- they demonstrate governed, reusable KPIs"),
                            html.Li("Let the customer ask their own questions to show Genie's natural language flexibility"),
                        ]),
                    ])),
                    _faq_item("Should I teardown after demoing?", html.P(
                        "Yes -- tear down deployments after demos to keep your workspace clean and avoid catalog sprawl. "
                        "Use the Manage tab for per-deployment teardown or the Admin tab for bulk cleanup."
                    )),
                    _faq_item("Who owns the Genie space and data?", html.P(
                        "The Genie space and data are created under your workspace directory. The schema and all tables "
                        "are tagged with your email address for traceability. You have full ownership and can teardown at any time."
                    )),
                ], start_collapsed=True, always_open=True),
            ]),
        ], className="mb-4"),
        # Troubleshooting
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-wrench me-2"), "Troubleshooting"]),
            dbc.CardBody([
                dbc.Accordion([
                    _faq_item("Why did my deployment fail?", html.Div([
                        html.P("Check the error details card that appears after a failure. Common causes include:"),
                        html.Ul([
                            html.Li("SQL warehouse is stopped or unavailable"),
                            html.Li("Insufficient permissions on the target catalog or schema"),
                            html.Li("Genie API rate limits (try again in a minute)"),
                        ]),
                        html.P([html.Strong("Fix: "), "Resolve the specific error and try deploying again."], className="mb-0"),
                    ])),
                    _faq_item("Data was created but Genie space failed", html.P(
                        "Deployment has two phases: (1) data generation (tables, metric views) and (2) Genie space creation. "
                        "If phase 1 succeeds but phase 2 fails, the data is still usable. Retry usually works. "
                        "If it keeps failing, check that the app's service principal has workspace permissions for Genie."
                    )),
                    _faq_item("My warehouse is stopped", html.P(
                        "The app auto-starts stopped warehouses when you deploy. You can also manually start a warehouse "
                        "from Advanced Options on the Build tab -- find your warehouse in the dropdown and click Start. "
                        "Serverless warehouses typically start in 30-60 seconds."
                    )),
                    _faq_item("I can't see my deployment on the Manage tab", html.P(
                        "Click the Refresh button. Deployments only appear after the log record is written at the end "
                        "of a successful deploy. If the deploy failed mid-way, no record is created. "
                        "Deployments are per-user unless you're an admin, in which case you see all deployments."
                    )),
                ], start_collapsed=True, always_open=True),
            ]),
        ], className="mb-4"),
        # Administration
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-user-shield me-2"), "Administration"]),
            dbc.CardBody([
                dbc.Accordion([
                    _faq_item("How does the admin system work?", html.P(
                        "The first person to deploy becomes an auto-admin. Admins can manage warehouse policy, "
                        "catalog settings, app managers, and perform bulk teardown. The Admin tab is only visible to managers."
                    )),
                    _faq_item("Can multiple people use this app?", html.P(
                        "Yes. Each user sees their own deployments on the Manage tab. "
                        "Admins see all deployments across users and can teardown on behalf of others."
                    )),
                ], start_collapsed=True, always_open=True),
            ]),
        ], className="mb-4"),
    ], className="pt-3"),
)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

about_footer = html.Div([
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6([html.I(className="fas fa-info-circle me-2"), "About"], className="mb-2"),
                    html.P(
                        "Genie Factory uses AI to generate realistic, industry-specific demo environments "
                        "on Databricks. Each deployment creates synthetic data, governed metrics, and a fully "
                        "configured Genie space — ready for natural language exploration in minutes.",
                        className="text-muted-brand mb-0", style={"fontSize": "0.85rem"},
                    ),
                ], md=6),
                dbc.Col([
                    html.H6([html.I(className="fas fa-life-ring me-2"), "Need Help?"], className="mb-2"),
                    html.P("Having issues or want to request a feature? Reach out:", className="text-muted-brand mb-2", style={"fontSize": "0.85rem"}),
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-envelope me-2", style={"width": "16px", "color": "#6C757D"}),
                            html.A(_ADMIN_CONTACT_EMAIL, href=f"mailto:{_ADMIN_CONTACT_EMAIL}", style={"fontSize": "0.85rem"}),
                        ], className="mb-1") if _ADMIN_CONTACT_EMAIL else html.Div(),
                        html.Div([
                            html.I(className="fas fa-user me-2", style={"width": "16px", "color": "#6C757D"}),
                            html.Span(id="footer-deployer-email", style={"fontSize": "0.85rem", "color": "#6C757D"}),
                        ], className="mb-1"),
                        html.Div([
                            html.I(className="fab fa-slack me-2", style={"width": "16px", "color": "#6C757D"}),
                            html.Span("#genie-factory (coming soon)", style={"fontSize": "0.85rem", "color": "#ADB5BD"}),
                        ]),
                    ]),
                ], md=6),
            ]),
        ]),
    ], style={"backgroundColor": "#F8F9FA"}),
    html.Div(
        html.Small(f"v{__version__}", style={"color": "#6C757D"}),
        style={"textAlign": "right", "padding": "4px 12px 0 0"},
    ),
], className="about-footer")

# ---------------------------------------------------------------------------
# Admin Tab
# ---------------------------------------------------------------------------

admin_tab = dbc.Tab(
    label="⚙️ Admin",
    tab_id="admin-tab",
    id="admin-tab-element",
    tab_style={"display": "none"},
    children=html.Div([
        # Gate: shown when not a manager or loading
        html.Div(id="admin-gate", children=[
            html.Div([
                html.I(className="fas fa-spinner fa-spin me-2", style={"color": "#6C757D"}),
                html.Span("Loading admin panel...", style={"color": "#6C757D"}),
            ], className="text-center p-5"),
        ]),
        # Admin panel: hidden until verified as manager
        html.Div(id="admin-panel", style={"display": "none"}, children=[
            dbc.Tabs(id="admin-sub-tabs", active_tab="admin-activity-tab", children=[

                # Sub-tab 1: Activity & Analytics
                dbc.Tab(label="Activity & Analytics", tab_id="admin-activity-tab", children=html.Div([
                    # Deployment Summary card (FIRST)
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-list-alt me-2"), "Deployment Summary"]),
                        dbc.CardBody(id="deployment-summary-content", children=[
                            html.P("Click Refresh Analytics to load.", className="text-muted-brand"),
                        ]),
                    ], className="mb-4"),

                    # Deployment Analytics card (SECOND)
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-chart-bar me-2"), "Deployment Analytics"]),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(dbc.Select(id="analytics-timeframe", options=[
                                    {"label": "Last 7 days", "value": "7"},
                                    {"label": "Last 30 days", "value": "30"},
                                    {"label": "All time", "value": "0"},
                                ], value="30"), md=3),
                                dbc.Col(dbc.Button([html.I(className="fas fa-sync-alt me-1"), "Refresh"], id="refresh-analytics-btn", color="secondary", outline=True, size="sm"), width="auto"),
                            ], className="mb-3 align-items-end"),
                            html.Div(id="analytics-content"),
                        ]),
                    ], className="mb-4"),

                    # Recent Activity card (LAST)
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-history me-2"), "Recent Activity"]),
                        dbc.CardBody([
                            html.Div(id="audit-trail-content", style={"maxHeight": "400px", "overflowY": "auto"}),
                            dbc.Button([html.I(className="fas fa-sync-alt me-1"), "Refresh"], id="refresh-audit-btn", color="secondary", outline=True, size="sm", className="mt-2"),
                        ]),
                    ], className="mb-4"),
                ], className="pt-3")),

                # Sub-tab 2: Managers
                dbc.Tab(label="Managers", tab_id="admin-managers-tab", children=html.Div([
                    # App Managers card
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-user-shield me-2"), "App Managers"]),
                        dbc.CardBody([
                            html.P("Managers can view all deployments and teardown any deployment.", className="text-muted-brand mb-3", style={"fontSize": "0.85rem"}),
                            html.Div(id="admin-manager-list"),
                            html.Hr(className="section-divider"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Add Manager", className="form-label"),
                                    dbc.Input(id="new-manager-email", type="email", placeholder="user@company.com", size="sm"),
                                    # Hidden placeholder for old dropdown callback ID
                                    dcc.Dropdown(id="new-manager-dropdown", style={"display": "none"}),
                                ], md=8),
                                dbc.Col([
                                    dbc.Label("\u00a0", className="form-label"),
                                    dbc.Button([html.I(className="fas fa-plus me-1"), "Add"], id="add-manager-btn", color="primary", size="sm", className="w-100"),
                                ], md=2),
                            ], className="align-items-end"),
                            html.Div(id="add-manager-status", className="mt-2"),
                        ]),
                    ], className="mb-4"),
                ], className="pt-3")),

                # Sub-tab 3: Catalogs & Warehouses
                dbc.Tab(label="Catalogs & Warehouses", tab_id="admin-warehouses-tab", children=html.Div([

                    # Default Catalog card (moved from System tab)
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-database me-2"), "Default Catalog"]),
                        dbc.CardBody([
                            html.P("Override the default catalog for new deployments. Leave blank to auto-detect.", className="text-muted-brand mb-2"),
                            dbc.Input(id="admin-default-catalog-input", placeholder="Auto-detect (current catalog)", size="sm", className="mb-2"),
                            dbc.Button([html.I(className="fas fa-save me-1"), "Save"], id="save-catalog-policy-btn", color="primary", size="sm"),
                            html.Div(id="catalog-policy-status", className="mt-2"),
                        ]),
                    ], className="mb-4"),

                    # Hidden placeholders for removed catalog policy callback IDs
                    html.Div([
                        dbc.RadioItems(id="catalog-policy-radio", value="allow_all"),
                        dcc.Dropdown(id="approved-catalogs-dropdown"),
                        dbc.Collapse(id="catalog-restrict-collapse", is_open=False),
                        html.Button(id="save-catalog-policy-radio-btn", style={"display": "none"}),
                        html.Div(id="catalog-policy-radio-status"),
                    ], style={"display": "none"}),

                    # Warehouse Policy card
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-sliders-h me-2"), "Warehouse Policy"]),
                        dbc.CardBody([
                            html.P("Control which SQL warehouses users can select when deploying.", className="text-muted-brand mb-3", style={"fontSize": "0.85rem"}),
                            dbc.RadioItems(
                                id="warehouse-policy-radio",
                                options=[
                                    {"label": html.Span([
                                        html.I(className="fas fa-globe me-2"),
                                        html.Span([
                                            html.Strong("Allow all"),
                                            html.Br(),
                                            html.Small("Users can select any available warehouse", style={"color": "#6C757D"}),
                                        ]),
                                    ]), "value": "user_choice"},
                                    {"label": html.Span([
                                        html.I(className="fas fa-star me-2"),
                                        html.Span([
                                            html.Strong("Recommended"),
                                            html.Br(),
                                            html.Small("Suggest a default warehouse but allow overrides", style={"color": "#6C757D"}),
                                        ]),
                                    ]), "value": "recommended"},
                                    {"label": html.Span([
                                        html.I(className="fas fa-list me-2"),
                                        html.Span([
                                            html.Strong("Restrict"),
                                            html.Br(),
                                            html.Small("Only approved warehouses are available", style={"color": "#6C757D"}),
                                        ]),
                                    ]), "value": "allowlist"},
                                    {"label": html.Span([
                                        html.I(className="fas fa-lock me-2"),
                                        html.Span([
                                            html.Strong("Admin locked"),
                                            html.Br(),
                                            html.Small("Force all deploys to use a single warehouse", style={"color": "#6C757D"}),
                                        ]),
                                    ]), "value": "admin_locked"},
                                ],
                                value="user_choice",
                                className="mb-3",
                            ),
                            # Description for each mode
                            html.Div(id="policy-description", children=[
                                html.Small("Users can select any available warehouse.", style={"color": "#6C757D"}),
                            ], className="mb-3"),
                            # Conditional panels per policy mode
                            html.Div(id="admin-warehouse-selector", style={"display": "none"}, children=[
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Locked Warehouse", className="form-label"),
                                        dcc.Dropdown(id="admin-warehouse-dropdown", placeholder="Select warehouse..."),
                                    ], md=8),
                                    dbc.Col([
                                        dbc.Label("\u00a0", className="form-label"),
                                        dbc.Button([html.I(className="fas fa-lock me-1"), "Lock"], id="save-warehouse-policy-btn", color="primary", size="sm", className="w-100"),
                                    ], md=4),
                                ], className="align-items-end"),
                            ]),
                            html.Div(id="admin-recommended-selector", style={"display": "none"}, children=[
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Recommended Warehouse", className="form-label"),
                                        dcc.Dropdown(id="admin-recommended-dropdown", placeholder="Select warehouse..."),
                                    ], md=8),
                                    dbc.Col([
                                        dbc.Label("\u00a0", className="form-label"),
                                        dbc.Button([html.I(className="fas fa-star me-1"), "Set"], id="save-recommended-policy-btn", color="primary", size="sm", className="w-100"),
                                    ], md=4),
                                ], className="align-items-end"),
                                html.Div(id="recommended-wh-detail", className="mt-2"),
                            ]),
                            html.Div(id="admin-warehouse-allowlist-selector", style={"display": "none"}, children=[
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Allowed Warehouses", className="form-label"),
                                        dcc.Dropdown(id="admin-warehouse-allowlist-dropdown", multi=True, placeholder="Select allowed warehouses..."),
                                    ], md=8),
                                    dbc.Col([
                                        dbc.Label("\u00a0", className="form-label"),
                                        dbc.Button([html.I(className="fas fa-save me-1"), "Save"], id="save-allowlist-policy-btn", color="primary", size="sm", className="w-100"),
                                    ], md=4),
                                ], className="align-items-end"),
                            ]),
                            html.Div(id="policy-save-no-lock", style={"display": "none"}, children=[
                                dbc.Button([html.I(className="fas fa-save me-1"), "Save Policy"], id="save-policy-user-choice-btn", color="primary", size="sm"),
                            ]),
                        ]),
                    ], className="mb-4"),

                    # Warehouse Management card (REWORKED -- cleaner side-by-side layout)
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-server me-2"), "Warehouse Management"]),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Warehouse", className="form-label"),
                                    dcc.Dropdown(id="admin-wh-select-dropdown", placeholder="Choose a warehouse..."),
                                ], md=8),
                                dbc.Col([
                                    dbc.Label("\u00a0", className="form-label"),
                                    dbc.Button([html.I(className="fas fa-sync-alt me-1"), "Refresh"], id="refresh-admin-warehouses-btn", color="secondary", outline=True, size="sm", className="w-100"),
                                ], md=2, className="d-flex align-items-end"),
                            ], className="mb-3 align-items-end"),
                            # Detail panel for selected warehouse
                            html.Div(id="admin-wh-detail-panel"),
                            # Keep the old list div hidden for callback compat
                            html.Div(id="admin-warehouse-list", style={"display": "none"}),
                            html.Div([
                                dbc.Input(id="admin-new-wh-name", type="hidden"),
                                dbc.Input(id="admin-new-wh-size", type="hidden", value="Small"),
                                html.Button(id="admin-create-wh-btn", style={"display": "none"}),
                                html.Div(id="admin-wh-status"),
                            ], style={"display": "none"}),
                        ]),
                    ], className="mb-4"),

                ], className="pt-3")),

                # Sub-tab 4: Bulk Teardown
                dbc.Tab(label="Bulk Teardown", tab_id="admin-bulk-tab", children=html.Div([
                    # Stale Deployment Cleanup
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-broom me-2"), "Stale Deployment Cleanup"]),
                        dbc.CardBody([
                            html.P("Remove old deployments that are no longer needed. This tears down the schema (CASCADE) and deletes the Genie space.", className="text-muted-brand mb-3", style={"fontSize": "0.85rem"}),
                            html.Div(id="stale-summary"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Older than"),
                                    dbc.Select(id="cleanup-age-threshold", options=[
                                        {"label": "30 days", "value": "30"},
                                        {"label": "60 days", "value": "60"},
                                        {"label": "90 days", "value": "90"},
                                    ], value="30"),
                                ], md=4),
                                dbc.Col([
                                    dbc.Label("\u00a0"),
                                    dbc.Button([html.I(className="fas fa-trash-alt me-1"), "Clean Up All"], id="cleanup-stale-btn", color="danger", outline=True, className="w-100"),
                                ], md=4),
                            ], className="align-items-end"),
                            html.Div(id="cleanup-status", className="mt-2"),
                        ]),
                    ], className="mb-4"),

                    # Teardown by User
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-user-times me-2"), "Teardown by User"]),
                        dbc.CardBody([
                            html.P("Remove all active deployments for a specific user.", className="text-muted-brand mb-3", style={"fontSize": "0.85rem"}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("User"),
                                    dcc.Dropdown(id="teardown-user-dropdown", placeholder="Select user...", searchable=True),
                                ], md=6),
                                dbc.Col([
                                    dbc.Label("\u00a0"),
                                    dbc.Button([html.I(className="fas fa-trash-alt me-1"), "Teardown All"], id="teardown-by-user-btn", color="danger", outline=True),
                                ], width="auto"),
                            ], className="align-items-end"),
                            html.Div(id="teardown-user-status", className="mt-2"),
                        ]),
                    ], className="mb-4"),

                    # Teardown All Deployments
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-exclamation-triangle me-2 text-warning"), "Teardown All Deployments"]),
                        dbc.CardBody([
                            html.P("Remove ALL active deployments across all users.", className="text-muted-brand mb-2", style={"fontSize": "0.85rem"}),
                            html.P([html.I(className="fas fa-exclamation-circle me-1"), "This action cannot be undone."], className="text-danger mb-3", style={"fontSize": "0.85rem", "fontWeight": "600"}),
                            dbc.Button([html.I(className="fas fa-skull-crossbones me-1"), "Teardown Everything"], id="teardown-all-btn", color="danger"),
                            html.Div(id="teardown-all-status", className="mt-2"),
                        ]),
                    ], className="mb-4", style={"borderLeft": "4px solid #DC3545"}),

                    # Backend Teardown
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-database me-2 text-warning"), "Backend Teardown"]),
                        dbc.CardBody([
                            html.P(
                                "Manage the metadata tables (managers, settings, deployment log, audit log).",
                                className="text-muted-brand mb-3", style={"fontSize": "0.85rem"},
                            ),
                            html.P([html.I(className="fas fa-exclamation-circle me-1"), "This action cannot be undone."], className="text-danger mb-3", style={"fontSize": "0.85rem", "fontWeight": "600"}),
                            dbc.Row([
                                dbc.Col([
                                    html.P("Drop and recreate all tables. Clears history but restores a clean state.", style={"fontSize": "0.8rem", "color": "#6C757D"}),
                                    dbc.Button([html.I(className="fas fa-redo me-1"), "Reset Tables"], id="reset-backend-btn", color="warning", outline=True),
                                ], md=6),
                                dbc.Col([
                                    html.P("Permanently drop all tables without recreating.", style={"fontSize": "0.8rem", "color": "#DC3545"}),
                                    dbc.Button([html.I(className="fas fa-trash-alt me-1"), "Drop Tables"], id="drop-backend-btn", color="danger"),
                                ], md=6),
                            ]),
                            html.Div(id="reset-backend-status", className="mt-2"),
                            html.Div(id="drop-backend-status", className="mt-2"),
                        ]),
                    ], className="mb-4", style={"borderLeft": "4px solid #FFC107"}),
                ], className="pt-3")),

                # Sub-tab 5: System
                dbc.Tab(label="System", tab_id="admin-system-tab", children=html.Div([
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-cog me-2"), "System Configuration"]),
                        dbc.CardBody(id="admin-system-info", children=[
                            html.P("Loading system configuration...", className="text-muted-brand"),
                        ]),
                    ], className="mb-4"),
                    # App Information
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fas fa-server me-2"), "App Information"]),
                        dbc.CardBody(id="admin-app-info", children=[
                            html.P("Loading...", className="text-muted-brand"),
                        ]),
                    ], className="mb-4"),
                ], className="pt-3")),

                # Sub-tab 6: Telemetry
                dbc.Tab(label="Telemetry", tab_id="admin-telemetry-tab", children=html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-chart-line", style={"fontSize": "3rem", "color": "#DEE2E6"}),
                            ], className="text-center mb-3"),
                            html.H5("Telemetry", className="text-center mb-2"),
                            html.P("Usage analytics, deployment trends, and system health monitoring.", className="text-center text-muted-brand"),
                            dbc.Badge("Coming Soon", className="d-block mx-auto", style={"fontSize": "0.85rem", "width": "fit-content", "backgroundColor": "#495057", "color": "#FFFFFF"}),
                        ], style={"padding": "3rem 1rem"}),
                    ]),
                ], className="pt-3")),
            ]),
        ]),
        html.Div(id="admin-status", className="mt-2"),
    ], className="pt-3"),
)

# ---------------------------------------------------------------------------
# Full Layout
# ---------------------------------------------------------------------------

layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Tabs(
            id="main-tabs",
            active_tab="deploy-tab",
            children=[deploy_tab, manage_tab, faq_tab, admin_tab],
            className="mb-3",
            persistence=True,
            persistence_type="session",
        ),
        about_footer,
    ], fluid=True),
])
