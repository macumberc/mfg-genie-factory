"""Shared fixtures for Genie Factory tests.

These tests focus on pure functions that require no Spark session,
Databricks API access, or external services.
"""

import sys
import os

import pytest

# Ensure the project root is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def sample_email() -> str:
    return "chad.macumber@databricks.com"


@pytest.fixture
def sample_slug() -> str:
    return "chad_macumber"
