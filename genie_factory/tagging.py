"""Corporate-taxonomy tagging for deployed Genie demos.

Genie *spaces* cannot carry tags — the ``PATCH /api/2.0/genie/spaces/{id}``
endpoint silently drops a ``tags`` field (same as it does for ``title``), and the
SDK ``GenieAPI.update_space`` exposes no tags parameter. So instead of tagging the
space object, we attach the two taxonomy tags to the things that *can* be tagged
and queried, via two complementary mechanisms:

  #1  **Unity Catalog tags** — ``ALTER SCHEMA/TABLE ... SET TAGS`` on the deployed
      schema and each of its tables. Best-effort: a governed-tag policy may block
      ``SET TAGS`` if the run identity lacks ``APPLY TAG``/ownership, so failures
      are collected as warnings rather than raised. Queryable via
      ``system.information_schema.{schema_tags,table_tags}``.

  #2  **Sidecar Delta table** ``<catalog>.genie_factory.space_tag_mapping`` — one
      upserted row per deployed schema recording space_id, title, subindustry, and
      outcome use case. Always written (independent of UC tag privileges); it is
      the guaranteed-queryable record and survives nothing automatically, so it is
      refreshed on every deploy (keyed by stable ``schema_fqn``).

Two tag keys are emitted:
  * ``mfg_subindustry``      — one of the 20 allowed subindustry values
  * ``mfg_outcome_usecase``  — one of the 25 allowed outcome/use-case values

The per-spec values live on the spec JSON (``DomainSpec.mfg_subindustry`` /
``.mfg_outcome_usecase``), populated by ``--populate-specs`` below. ``deploy()``
reads them off the spec and falls back to deriving the subindustry from
``industry`` when a spec predates this field.

CLI::

    python -m genie_factory.tagging --populate-specs [--dry-run]
"""

from __future__ import annotations

import argparse
import glob
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

_logger = logging.getLogger("genie_factory.tagging")

TAG_SUBINDUSTRY = "mfg_subindustry"
TAG_OUTCOME = "mfg_outcome_usecase"

# Entity type for the workspace entity-tag-assignments API. Genie spaces ARE
# taggable through this API (the /genie/spaces PATCH endpoint silently drops a
# `tags` field, but /api/2.0/entity-tag-assignments accepts geniespaces tags).
ENTITY_TYPE_GENIE = "geniespaces"

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SPECS_DIR = os.path.join(_REPO_ROOT, "genie_factory", "specs")

# --------------------------------------------------------------------------- #
# Allowed taxonomy values (the corporate vocabulary the tags must draw from).
# --------------------------------------------------------------------------- #

ALLOWED_SUBINDUSTRIES = {
    "Automotive", "Semiconductor", "Computer & Electronic", "Logistics",
    "Chemicals & Materials", "Machinery", "Oil & Gas Integrated",
    "Oil & Gas Downstream & Refining", "Aerospace", "Electric Utility",
    "Oil & Gas Midstream", "Enterprise Software", "Oil & Gas Upstream",
    "Agriculture", "Industrial Distribution", "Railroad", "Mining",
    "Food & Beverage", "Construction & Engineering", "Power Generation",
}

ALLOWED_OUTCOMES = {
    "Demand Forecasting", "Predictive Maintenance & Asset Health",
    "Design Space Simulation & Exploration", "Production Monitoring",
    "Prescriptive Maintenance", "Supply & Materials Planning",
    "Defect Detection", "Inventory Optimization",
    "Distribution & Logistics Optimization", "Product & Process Traceability",
    "Cyber Threat Monitoring & Detection", "Operations Resource Efficiency",
    "Quality Event Root Cause Analysis", "Customer 360", "Workforce Safety",
    "Scenario Planning & Business Simulation", "Dynamic Pricing",
    "Feedstock, Formulation, & Recipe Control",
    "Incident & Field Service Assistant", "Sustainability & Circular Economy",
    # Added from manual taxonomy corrections applied on the mfg-industry-prod
    # deployment — refined the best-fit "(loose)" buckets into specific use cases.
    "Working Capital & Cash Flow Optimization", "Expense & Spend Intelligence",
    "Capital Investment Simulation", "Commodity & Energy Trading",
    "Regulation Compliance, & External Reporting",
}

# Map the repo's ``industry`` strings onto the allowed subindustry vocabulary.
# Identity for all but the entries below; anything not listed passes through
# unchanged (and is validated against ALLOWED_SUBINDUSTRIES at populate time).
SUBINDUSTRY_TAG_MAP = {
    "Oil & Gas Refining": "Oil & Gas Downstream & Refining",  # vocabulary rename
    # Reclassification applied on the mfg-industry-prod deployment: the three
    # upstream demos are tagged under the Integrated subindustry (their titles
    # keep the "Oil & Gas Upstream" branding via the spec ``industry`` field).
    "Oil & Gas Upstream": "Oil & Gas Integrated",
}

# Best-fit map of every spec's outcome use case onto the allowed vocabulary,
# keyed by (subindustry_slug, spec_filename_stem). Entries flagged in comments
# as (loose) had no exact allowed value and were best-fit to the nearest one.
OUTCOME_USECASE_MAP: dict[str, dict[str, str]] = {
    "aerospace": {
        "demand_forecasting": "Demand Forecasting",
        "design_space_simulation_for_fuel_efficiency": "Design Space Simulation & Exploration",
        "financial_analytics_reporting": "Operations Resource Efficiency",  # (loose)
        "predictive_maintenance_asset_health": "Predictive Maintenance & Asset Health",
        "product_traceability_anti_counterfeit": "Product & Process Traceability",
        "quality_event_root_cause_analysis": "Quality Event Root Cause Analysis",
        "supply_materials_planning": "Supply & Materials Planning",
        "working_capital_cash_flow_optimization": "Operations Resource Efficiency",  # (loose)
    },
    "automotive": {
        "design_space_simulation_for_safety": "Design Space Simulation & Exploration",
        "product_feature_usage_analytics": "Customer 360",
        "vehicle_health_maintenance_report": "Predictive Maintenance & Asset Health",
        "vehicle_recall_root_cause_analysis": "Quality Event Root Cause Analysis",
    },
    "chemicals_materials": {
        "autonomous_lab_experiments": "Feedstock, Formulation, & Recipe Control",
        "demand_forecasting": "Demand Forecasting",
        "product_process_traceability": "Product & Process Traceability",
        "quality_event_root_cause_analysis": "Quality Event Root Cause Analysis",
    },
    "computer_electronic": {
        "design_space_simulation_system_on_chip": "Design Space Simulation & Exploration",
        "predictive_maintenance_troubleshoot": "Predictive Maintenance & Asset Health",
        "visual_defect_detection": "Defect Detection",
    },
    "construction_engineering": {
        "engineering_bid_creation": "Scenario Planning & Business Simulation",  # (loose)
        "production_and_project_completion_monitoring": "Production Monitoring",
    },
    "electric_utility": {
        "demand_forecasting": "Demand Forecasting",
        "grid_management_energy_mix": "Operations Resource Efficiency",  # (loose)
        "outage_response": "Incident & Field Service Assistant",
        "transformer_asset_health": "Predictive Maintenance & Asset Health",
    },
    "food_beverage": {
        "inventory_optimization": "Inventory Optimization",
        "product_process_traceability_recall": "Product & Process Traceability",
        "quality_event_root_cause_analysis": "Quality Event Root Cause Analysis",
        "scenario_planning_business_simulation": "Scenario Planning & Business Simulation",
    },
    "industrial_distribution": {
        "demand_forecasting": "Demand Forecasting",
        "inventory_optimization": "Inventory Optimization",
        "working_capital_cash_flow_optimization": "Operations Resource Efficiency",  # (loose)
    },
    "logistics": {
        "fleet_planning_and_optimization": "Distribution & Logistics Optimization",
        "load_demand_forecasting": "Demand Forecasting",
        "route_planning": "Distribution & Logistics Optimization",
    },
    "machinery": {
        "asset_health": "Predictive Maintenance & Asset Health",
        "demand_forecasting": "Demand Forecasting",
        "field_service_assistant": "Incident & Field Service Assistant",
        "financial_analytics_reporting": "Working Capital & Cash Flow Optimization",
        "machining_process_defect_detection": "Defect Detection",
        "manufacturing_resource_planning": "Supply & Materials Planning",
        "production_monitoring": "Production Monitoring",
        "quality_event_root_cause_analysis": "Quality Event Root Cause Analysis",
        "spare_part_inventory_optimization": "Inventory Optimization",
        "spend_intelligence": "Expense & Spend Intelligence",
        "working_capital_cash_flow_optimization": "Working Capital & Cash Flow Optimization",
    },
    "mining": {
        "haul_vehicle_asset_health": "Predictive Maintenance & Asset Health",
        "production_monitoring_control_center": "Production Monitoring",
    },
    "oil_gas_integrated": {
        "capital_investment_simulation": "Capital Investment Simulation",
        "financial_analytics_reporting": "Expense & Spend Intelligence",
        "predictive_maintenance_asset_health": "Predictive Maintenance & Asset Health",
        "production_monitoring_control_center": "Production Monitoring",
        "scenario_planning_business_simulation": "Scenario Planning & Business Simulation",
        "working_capital_cash_flow_optimization": "Working Capital & Cash Flow Optimization",
    },
    "oil_gas_midstream": {
        "automated_reporting_of_carbon_intensity": "Operations Resource Efficiency",
        "energy_trading": "Commodity & Energy Trading",
        "financial_analytics_reporting": "Regulation Compliance, & External Reporting",
        "logistics_optimization": "Distribution & Logistics Optimization",
        "regulation_compliance": "Regulation Compliance, & External Reporting",
        "scenario_planning_business_simulation": "Scenario Planning & Business Simulation",
        "spend_intelligence": "Expense & Spend Intelligence",
        "working_capital_cash_flow_optimization": "Working Capital & Cash Flow Optimization",
    },
    "oil_gas_refining": {
        "energy_use_monitoring_heat": "Production Monitoring",
        "financial_analytics_reporting": "Expense & Spend Intelligence",
        "predictive_maintenance_asset_health": "Predictive Maintenance & Asset Health",
        "production_monitoring": "Production Monitoring",
        "quality_event_root_cause_analysis": "Quality Event Root Cause Analysis",
        "working_capital_cash_flow_optimization": "Working Capital & Cash Flow Optimization",
    },
    "oil_gas_upstream": {
        "predictive_maintenance_asset_health": "Predictive Maintenance & Asset Health",
        "reservoir_management": "Production Monitoring",  # (loose)
        "well_production_monitoring_flow": "Production Monitoring",
    },
    "power_generation": {
        "financial_analytics_reporting": "Operations Resource Efficiency",  # (loose)
        "grid_management_energy_mix": "Operations Resource Efficiency",  # (loose)
        "hydro_optimization": "Operations Resource Efficiency",  # (loose)
        "nuclear_safety": "Workforce Safety",  # (loose)
        "outage_response": "Incident & Field Service Assistant",
        "solar_optimization_behind_the_meter": "Sustainability & Circular Economy",
        "wind_optimization": "Operations Resource Efficiency",  # (loose)
    },
    "railroad": {
        "freight_demand_forecasting": "Demand Forecasting",
        "predictive_maintenance_asset_health": "Predictive Maintenance & Asset Health",
        "route_planning": "Distribution & Logistics Optimization",
    },
    "semiconductor": {
        "demand_forecasting": "Demand Forecasting",
        "design_space_simulation": "Design Space Simulation & Exploration",
        "financial_analytics_reporting": "Operations Resource Efficiency",  # (loose)
        "quality_event_root_cause_analysis": "Quality Event Root Cause Analysis",
        "salable_inventory_optimization": "Inventory Optimization",
        "supply_materials_capacity_allocation": "Supply & Materials Planning",
        "virtual_metrology_defect_detection": "Defect Detection",
    },
}


# --------------------------------------------------------------------------- #
# Value resolution
# --------------------------------------------------------------------------- #

def normalize_subindustry(industry: str) -> str:
    """Map a spec ``industry`` string onto the allowed subindustry vocabulary."""
    return SUBINDUSTRY_TAG_MAP.get(industry, industry)


def resolve_tags(domain_spec: Any) -> dict[str, str]:
    """Return the {tag_key: value} dict for a spec.

    Prefers the explicit spec fields; falls back to deriving the subindustry
    from ``industry`` for specs that predate the field. Outcome is omitted when
    unknown (empty string) so a missing mapping skips the outcome tag rather
    than writing a junk value.
    """
    subindustry = getattr(domain_spec, "mfg_subindustry", "") or normalize_subindustry(
        getattr(domain_spec, "industry", "")
    )
    outcome = getattr(domain_spec, "mfg_outcome_usecase", "") or ""
    tags: dict[str, str] = {}
    if subindustry:
        tags[TAG_SUBINDUSTRY] = subindustry
    if outcome:
        tags[TAG_OUTCOME] = outcome
    return tags


def _esc(value: str) -> str:
    """Escape a string for a single-quoted SQL literal."""
    return str(value).replace("'", "''")


# --------------------------------------------------------------------------- #
# #1 — Unity Catalog tags
# --------------------------------------------------------------------------- #

def apply_uc_tags(
    spark: Any,
    fqn: str,
    table_names: list[str],
    tags: dict[str, str],
) -> list[dict[str, str]]:
    """Best-effort ``SET TAGS`` on the schema and each table.

    Returns a list of warning dicts for any statement that failed (e.g. blocked
    by a governed-tag policy). Never raises.
    """
    warnings: list[dict[str, str]] = []
    if not tags:
        return warnings

    set_clause = ", ".join(f"'{_esc(k)}' = '{_esc(v)}'" for k, v in tags.items())

    targets = [("SCHEMA", fqn)] + [("TABLE", f"{fqn}.{t}") for t in table_names]
    for obj_type, obj_name in targets:
        try:
            spark.sql(f"ALTER {obj_type} {obj_name} SET TAGS ({set_clause})")
        except Exception as exc:  # noqa: BLE001 — best-effort; surface as warning
            _logger.warning("SET TAGS on %s %s failed: %s", obj_type, obj_name, exc)
            warnings.append(
                {"category": "uc_tag", "name": obj_name, "error": str(exc)}
            )
    return warnings


# --------------------------------------------------------------------------- #
# #1b — Genie space tags (entity-tag-assignments API)
# --------------------------------------------------------------------------- #

def assign_space_tags(
    workspace_client: Any,
    space_id: str,
    tags: dict[str, str],
) -> list[dict[str, str]]:
    """Assign tags to a Genie space via the entity-tag-assignments API.

    Idempotent upsert per tag: ``POST /api/2.0/entity-tag-assignments`` to
    create, falling back to ``PATCH .../{entity_type}/{id}/tags/{key}`` to
    update when the tag already exists. Best-effort — returns warnings, never
    raises. Free-form values are accepted (no governed-tag policy required).
    """
    from .genie import _api_request, _default_workspace_client

    warnings: list[dict[str, str]] = []
    if not tags or not space_id:
        return warnings

    ws = workspace_client or _default_workspace_client()
    for key, value in tags.items():
        try:
            _api_request(
                ws,
                "POST",
                "/api/2.0/entity-tag-assignments",
                payload={
                    "entity_type": ENTITY_TYPE_GENIE,
                    "entity_id": space_id,
                    "tag_key": key,
                    "tag_value": value,
                },
                expected_statuses=(200, 201),
            )
        except Exception:  # noqa: BLE001 — most likely "already exists"; update.
            try:
                _api_request(
                    ws,
                    "PATCH",
                    f"/api/2.0/entity-tag-assignments/{ENTITY_TYPE_GENIE}/{space_id}"
                    f"/tags/{key}?update_mask=tag_value",
                    payload={"tag_value": value},
                    expected_statuses=(200,),
                )
            except Exception as exc:  # noqa: BLE001
                _logger.warning(
                    "Space tag %s=%s on %s failed: %s", key, value, space_id, exc
                )
                warnings.append(
                    {"category": "space_tag",
                     "name": f"{space_id}:{key}", "error": str(exc)}
                )
    return warnings


# --------------------------------------------------------------------------- #
# #2 — Sidecar Delta mapping table
# --------------------------------------------------------------------------- #

_MAPPING_SCHEMA = "genie_factory"
_MAPPING_TABLE = "space_tag_mapping"


def mapping_table_fqn(spark: Any, catalog: Optional[str] = None) -> str:
    """Resolve the fully-qualified sidecar table name."""
    from .validators import current_catalog

    cat = catalog or current_catalog(spark)
    return f"{cat}.{_MAPPING_SCHEMA}.{_MAPPING_TABLE}"


def ensure_mapping_table(spark: Any, catalog: Optional[str] = None) -> str:
    """Create the sidecar schema + table if absent. Returns the table FQN."""
    from .validators import current_catalog

    cat = catalog or current_catalog(spark)
    table = f"{cat}.{_MAPPING_SCHEMA}.{_MAPPING_TABLE}"
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {cat}.{_MAPPING_SCHEMA}")
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS {table} (
            schema_fqn STRING COMMENT 'Fully-qualified catalog.schema of the demo (stable upsert key)',
            catalog STRING COMMENT 'Unity Catalog catalog',
            schema_name STRING COMMENT 'Schema name within the catalog',
            space_id STRING COMMENT 'Genie space resource ID (changes each refresh)',
            space_title STRING COMMENT 'Genie space display title',
            industry STRING COMMENT 'Spec industry string',
            use_case STRING COMMENT 'Spec use-case string',
            mfg_subindustry STRING COMMENT 'Allowed-taxonomy subindustry tag value',
            mfg_outcome_usecase STRING COMMENT 'Allowed-taxonomy outcome use-case tag value',
            updated_at STRING COMMENT 'UTC timestamp of the last upsert'
        ) USING DELTA
        COMMENT 'Maps each Genie Factory demo schema to its subindustry/outcome taxonomy tags (sidecar for un-taggable Genie spaces)'
        """
    )
    return table


def write_mapping_row(
    spark: Any,
    catalog: Optional[str],
    row: dict[str, Any],
) -> str:
    """Upsert one mapping row, keyed by ``schema_fqn`` (delete-then-insert).

    Keying on schema_fqn (stable across refreshes) keeps exactly one current row
    per demo even though space_id changes every refresh cycle.
    """
    table = ensure_mapping_table(spark, catalog)
    schema_fqn = row["schema_fqn"]
    spark.sql(f"DELETE FROM {table} WHERE schema_fqn = '{_esc(schema_fqn)}'")
    cols = [
        "schema_fqn", "catalog", "schema_name", "space_id", "space_title",
        "industry", "use_case", "mfg_subindustry", "mfg_outcome_usecase",
        "updated_at",
    ]
    values = ", ".join(f"'{_esc(row.get(c, '') or '')}'" for c in cols)
    spark.sql(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({values})")
    return table


# --------------------------------------------------------------------------- #
# Orchestration — called from deploy()
# --------------------------------------------------------------------------- #

def apply_tags_and_record(
    spark: Any,
    domain_spec: Any,
    fqn: str,
    catalog: str,
    schema_name: str,
    table_names: list[str],
    space_id: Optional[str] = None,
    space_title: Optional[str] = None,
    workspace_client: Any = None,
) -> dict[str, Any]:
    """Apply tags (#1 UC schema/tables, #1b Genie space) and upsert the sidecar
    mapping row (#2).

    Best-effort and self-contained: collects warnings, never raises, so a tag
    failure cannot abort a deploy.
    """
    warnings: list[dict[str, str]] = []
    tags = resolve_tags(domain_spec)

    # #1 Unity Catalog tags on schema + tables.
    warnings.extend(apply_uc_tags(spark, fqn, table_names, tags))

    # #1b Genie space tags (entity-tag-assignments API).
    if space_id:
        warnings.extend(assign_space_tags(workspace_client, space_id, tags))

    # #2 Sidecar mapping row (always attempted).
    mapping_table = None
    try:
        mapping_table = write_mapping_row(
            spark,
            catalog,
            {
                "schema_fqn": fqn,
                "catalog": catalog,
                "schema_name": schema_name,
                "space_id": space_id or "",
                "space_title": space_title or getattr(domain_spec, "space_title", ""),
                "industry": getattr(domain_spec, "industry", ""),
                "use_case": getattr(domain_spec, "use_case", ""),
                "mfg_subindustry": tags.get(TAG_SUBINDUSTRY, ""),
                "mfg_outcome_usecase": tags.get(TAG_OUTCOME, ""),
                "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
    except Exception as exc:  # noqa: BLE001
        _logger.warning("Sidecar mapping write failed for %s: %s", fqn, exc)
        warnings.append({"category": "tag_mapping", "name": fqn, "error": str(exc)})

    return {"tags": tags, "warnings": warnings, "mapping_table": mapping_table}


# --------------------------------------------------------------------------- #
# CLI — populate spec JSONs with the taxonomy fields
# --------------------------------------------------------------------------- #

def populate_specs(dry_run: bool = False) -> dict[str, Any]:
    """Write ``mfg_subindustry`` + ``mfg_outcome_usecase`` into every spec JSON.

    Validates each value against the allowed vocabulary and refuses to write an
    out-of-vocabulary value. Returns a summary dict.
    """
    updated, skipped, errors = 0, 0, []
    unmapped: list[str] = []

    from pathlib import Path

    from .remediation import write_spec

    for path in sorted(glob.glob(os.path.join(_SPECS_DIR, "*", "*.json"))):
        sub = os.path.basename(os.path.dirname(path))
        stem = os.path.basename(path)[:-5]
        with open(path, encoding="utf-8") as f:
            spec = json.load(f)

        subindustry = normalize_subindustry(spec.get("industry", ""))
        outcome = OUTCOME_USECASE_MAP.get(sub, {}).get(stem, "")

        if subindustry and subindustry not in ALLOWED_SUBINDUSTRIES:
            errors.append(f"{sub}/{stem}: subindustry '{subindustry}' not allowed")
            continue
        if outcome and outcome not in ALLOWED_OUTCOMES:
            errors.append(f"{sub}/{stem}: outcome '{outcome}' not allowed")
            continue
        if not outcome:
            unmapped.append(f"{sub}/{stem}")

        if (
            spec.get("mfg_subindustry") == subindustry
            and spec.get("mfg_outcome_usecase") == outcome
        ):
            skipped += 1
            continue

        spec["mfg_subindustry"] = subindustry
        spec["mfg_outcome_usecase"] = outcome
        if not dry_run:
            write_spec(Path(path), spec)
        updated += 1
        _logger.info("%s %s/%s -> (%s | %s)",
                     "DRY" if dry_run else "SET", sub, stem, subindustry, outcome)

    summary = {
        "updated": updated,
        "skipped": skipped,
        "unmapped": unmapped,
        "errors": errors,
    }
    return summary


def _spec_title_tag_map() -> dict[str, dict[str, str]]:
    """Build {deployed_space_title: tags} from the local spec corpus.

    Deployed titles follow ``build_genie_payload``'s
    ``f"{industry} - {space_title}"`` convention, so we reproduce it here to
    match a live space back to its taxonomy values without parsing descriptions.
    """
    from .generator import DomainSpec

    out: dict[str, dict[str, str]] = {}
    for path in sorted(glob.glob(os.path.join(_SPECS_DIR, "*", "*.json"))):
        with open(path, encoding="utf-8") as f:
            spec = DomainSpec.from_dict(json.load(f))
        title = f"{spec.industry} - {spec.space_title}"
        out[title] = resolve_tags(spec)
    return out


def tag_existing_spaces(
    workspace_client: Any = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Propagate taxonomy tags to every already-deployed managed Genie space.

    Matches live spaces to specs by title (tolerating the Databricks
    timestamp-suffix rename), then upserts entity tags. Use this to tag spaces
    that were deployed before space-tagging was wired into deploy(), without a
    full redeploy.
    """
    from .genie import _default_workspace_client, _list_all_genie_spaces, _TIMESTAMP_SUFFIX_RE

    ws = workspace_client or _default_workspace_client()
    title_map = _spec_title_tag_map()
    spaces = _list_all_genie_spaces(ws)

    assigned, unmatched, failed = [], [], []
    for space in spaces:
        title = space.get("title", "") or ""
        tags = title_map.get(title) or title_map.get(_TIMESTAMP_SUFFIX_RE.sub("", title))
        if not tags:
            # Skip non-GF spaces silently; report GF-looking ones that miss.
            if (space.get("description", "") or "").lstrip().startswith("**Subindustry:**"):
                unmatched.append(title)
            continue
        space_id = space.get("space_id")
        if dry_run:
            assigned.append({"title": title, "space_id": space_id, "tags": tags})
            continue
        warns = assign_space_tags(ws, space_id, tags)
        if warns:
            failed.append({"title": title, "space_id": space_id, "warnings": warns})
        else:
            assigned.append({"title": title, "space_id": space_id, "tags": tags})

    summary = {
        "total_spaces": len(spaces),
        "assigned": len(assigned),
        "unmatched_gf": unmatched,
        "failed": failed,
    }
    return summary


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(prog="python -m genie_factory.tagging")
    parser.add_argument(
        "--populate-specs", action="store_true",
        help="Write mfg_subindustry + mfg_outcome_usecase into all spec JSONs.",
    )
    parser.add_argument(
        "--tag-spaces", action="store_true",
        help="Propagate taxonomy tags to all already-deployed Genie spaces "
             "(matches live spaces to specs by title). Uses DATABRICKS_CONFIG_PROFILE.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Don't write/assign.")
    args = parser.parse_args()

    if args.populate_specs:
        summary = populate_specs(dry_run=args.dry_run)
        print(json.dumps(summary, indent=2))
        if summary["errors"]:
            raise SystemExit(1)
    elif args.tag_spaces:
        summary = tag_existing_spaces(dry_run=args.dry_run)
        print(json.dumps(summary, indent=2))
        if summary["failed"]:
            raise SystemExit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
