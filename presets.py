"""Manufacturing subindustry presets, enriched with spec metadata for the Dash app UI."""

import logging

from genie_factory.presets import SUBINDUSTRIES, USE_CASES as _RAW_USE_CASES
from genie_factory.specs import load_spec

logger = logging.getLogger("genie-factory")

# ---------------------------------------------------------------------------
# Enrich use cases with company_name and business_context from bundled specs
# ---------------------------------------------------------------------------

SUBINDUSTRY_USE_CASES: dict[str, list[dict]] = {}

for _sub in SUBINDUSTRIES:
    _enriched = []
    for _uc in _RAW_USE_CASES.get(_sub, []):
        _spec = load_spec(_sub, _uc["label"])
        _enriched.append({
            "label": _uc["label"],
            "use_case": _uc["use_case"],
            "company_name": _spec.company_name if _spec else "",
            "business_context": _spec.space_description if _spec else _uc["use_case"],
            "has_preset_spec": _spec is not None,
        })
    SUBINDUSTRY_USE_CASES[_sub] = _enriched

# Clean up module-level loop variables
del _sub, _enriched, _uc, _spec

# ---------------------------------------------------------------------------
# Icons for each manufacturing subindustry
# ---------------------------------------------------------------------------

SUBINDUSTRY_ICONS = {
    "Automotive": "fa-car",
    "Semiconductor": "fa-microchip",
    "Computer & Electronic": "fa-laptop",
    "Logistics": "fa-truck",
    "Chemicals & Materials": "fa-flask",
    "Machinery": "fa-cogs",
    "Oil & Gas Integrated": "fa-oil-can",
    "Oil & Gas Refining": "fa-fire",
    "Oil & Gas Midstream": "fa-stream",
    "Oil & Gas Upstream": "fa-hard-hat",
    "Electric Utility": "fa-bolt",
    "Aerospace": "fa-plane",
    "Power Generation": "fa-plug",
    "Industrial Distribution": "fa-warehouse",
    "Railroad": "fa-train",
    "Mining": "fa-mountain",
    "Food & Beverage": "fa-utensils",
    "Construction & Engineering": "fa-drafting-compass",
}

# ---------------------------------------------------------------------------
# Dataset size presets
# ---------------------------------------------------------------------------

DATASET_SIZE_PRESETS = {
    "demo":     {"num_tables": 3, "num_products": 20, "num_locations": 8,  "scale": 1,  "target_rows": 1000,  "est_minutes": 2},
    "standard": {"num_tables": 3, "num_products": 20, "num_locations": 8,  "scale": 3,  "target_rows": 5000,  "est_minutes": 3},
    "large":    {"num_tables": 4, "num_products": 50, "num_locations": 16, "scale": 10, "target_rows": 15000, "est_minutes": 7},
}

DATASET_SIZE_ESTIMATES = {
    "demo": "~1,000 rows per table. Ideal for quick demos. ~2 min deploy (pre-built spec).",
    "standard": "~5,000 rows per table. Good for realistic exploration. ~3 min deploy.",
    "large": "~15,000 rows per table. Best for large-scale demos. ~7 min deploy.",
}
