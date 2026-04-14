"""Dash application instance and configuration."""

import os
import dash
import dash_bootstrap_components as dbc

APP_TITLE = "Genie Factory"
PAGE_TITLE = "Genie Factory"
PORT = int(os.environ.get("DATABRICKS_APP_PORT", 8000))

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    title=PAGE_TITLE,
    suppress_callback_exceptions=True,
)
