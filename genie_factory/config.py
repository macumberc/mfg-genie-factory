"""Package-wide configuration for the Genie space generator."""

from __future__ import annotations

import os

PACKAGE_NAME = "genie-factory"

DEFAULT_SEED = 20250306
AUTO_WAREHOUSE = "auto"
HTTP_TIMEOUT_SECONDS = 30
LLM_TIMEOUT_SECONDS = 300

SPACE_DESCRIPTION_MARKER = "Managed by genie_factory"

# LLM endpoint for domain generation (configurable via env var)
DEFAULT_LLM_ENDPOINT = os.environ.get(
    "GENIE_FACTORY_LLM_ENDPOINT", "databricks-claude-sonnet-4-6"
)
LLM_MAX_TOKENS = 16000
LLM_TEMPERATURE = 0.3
LLM_MAX_RETRIES = 2
LLM_MAX_TOKENS_CAP = 32000
