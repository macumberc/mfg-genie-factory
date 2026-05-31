"""Deploy-time tracking of per-use-case markdown demo scripts.

Companion to ``genie_factory.tagging``'s ``space_tag_mapping`` sidecar, kept in
its own module because demo scripts and taxonomy tags are distinct concerns.
``deploy()`` calls :func:`record_demo_script` (best-effort) so every deploy —
and therefore every monthly refresh — upserts the rendered markdown demo script
for the demo into ``<catalog>.genie_factory.demo_scripts``.

The script itself is produced deterministically (no LLM) by
:func:`genie_factory.demos.render_demo` from the spec's ``to_dict()`` payload.

The two tracking tables join on ``schema_fqn`` (the stable upsert key that
survives refreshes even though ``space_id`` can change on a full recreate)::

    SELECT m.space_id, m.mfg_subindustry, d.demo_script_md
    FROM   <cat>.genie_factory.space_tag_mapping m
    JOIN   <cat>.genie_factory.demo_scripts      d USING (schema_fqn)

CLI::

    PYTHONPATH=. python -m genie_factory.demo_tracking --backfill [--catalog X]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any, Optional

_logger = logging.getLogger("genie_factory.demo_tracking")

_SCHEMA = "genie_factory"
_TABLE = "demo_scripts"

# Column order is authoritative — the CREATE DDL, the StructType, and the
# INSERT column list all derive from it.
_COLUMNS = [
    "schema_fqn",
    "catalog",
    "schema_name",
    "space_id",
    "space_title",
    "industry",
    "use_case",
    "demo_script_md",
    "script_chars",
    "updated_at",
]


def _esc(value: str) -> str:
    """Escape a string for a single-quoted SQL literal (used only for the
    controlled ``schema_fqn`` delete key — never for markdown)."""
    return str(value).replace("'", "''")


def table_fqn(spark: Any, catalog: Optional[str] = None) -> str:
    """Resolve the fully-qualified demo-scripts table name."""
    from .validators import current_catalog

    cat = catalog or current_catalog(spark)
    return f"{cat}.{_SCHEMA}.{_TABLE}"


def ensure_demo_scripts_table(spark: Any, catalog: Optional[str] = None) -> str:
    """Create the schema + demo-scripts table if absent. Returns the table FQN."""
    from .validators import current_catalog

    cat = catalog or current_catalog(spark)
    table = f"{cat}.{_SCHEMA}.{_TABLE}"
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {cat}.{_SCHEMA}")
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS {table} (
            schema_fqn STRING COMMENT 'Fully-qualified catalog.schema of the demo (stable upsert key; joins to space_tag_mapping)',
            catalog STRING COMMENT 'Unity Catalog catalog',
            schema_name STRING COMMENT 'Schema name within the catalog',
            space_id STRING COMMENT 'Genie space resource ID (mirrors space_tag_mapping at deploy time)',
            space_title STRING COMMENT 'Genie space display title',
            industry STRING COMMENT 'Spec industry string',
            use_case STRING COMMENT 'Spec use-case string',
            demo_script_md STRING COMMENT 'Rendered markdown sales demo script (genie_factory.demos.render_demo)',
            script_chars BIGINT COMMENT 'Character length of demo_script_md (freshness/sanity check)',
            updated_at STRING COMMENT 'UTC timestamp of the last upsert'
        ) USING DELTA
        COMMENT 'Per-use-case markdown demo scripts for deployed Genie Factory demos (one row per demo schema, keyed by schema_fqn)'
        """
    )
    return table


def write_demo_script_row(
    spark: Any,
    catalog: Optional[str],
    row: dict[str, Any],
) -> str:
    """Upsert one demo-script row, keyed by ``schema_fqn`` (delete-then-insert).

    Builds the row through a typed DataFrame + temp view rather than a
    string-literal INSERT, so arbitrary markdown (quotes, newlines, emoji,
    backslashes) needs no escaping. Only the ``schema_fqn`` delete key — a
    controlled ``catalog.schema`` value with no user text — is interpolated.
    """
    from pyspark.sql import Row
    from pyspark.sql.types import LongType, StringType, StructField, StructType

    table = ensure_demo_scripts_table(spark, catalog)
    schema_fqn = row["schema_fqn"]

    struct = StructType(
        [
            StructField(c, LongType() if c == "script_chars" else StringType(), True)
            for c in _COLUMNS
        ]
    )
    data = Row(*[row.get(c) for c in _COLUMNS])
    df = spark.createDataFrame([data], schema=struct)
    # Temp views are session-global, NOT thread-local. Under a concurrent
    # refresh (refresh_all at concurrency>1) a fixed view name lets one worker's
    # createOrReplaceTempView clobber another's before its INSERT runs, which
    # both drops rows and duplicates others. Key the view name on the (unique
    # per worker) schema_fqn so concurrent deploys never share a view.
    view = "_gf_demo_scripts_upsert_" + re.sub(r"[^0-9a-zA-Z]", "_", schema_fqn)
    df.createOrReplaceTempView(view)

    col_list = ", ".join(_COLUMNS)
    spark.sql(f"DELETE FROM {table} WHERE schema_fqn = '{_esc(schema_fqn)}'")
    spark.sql(f"INSERT INTO {table} ({col_list}) SELECT {col_list} FROM {view}")
    spark.catalog.dropTempView(view)
    return table


def record_demo_script(
    spark: Any,
    domain_spec: Any,
    fqn: str,
    catalog: str,
    schema_name: str,
    space_id: Optional[str] = None,
    space_title: Optional[str] = None,
) -> dict[str, Any]:
    """Render the spec's markdown demo script and upsert it into the tracking
    table. Best-effort and self-contained: collects warnings, never raises, so a
    demo-script failure cannot abort a deploy.
    """
    from .demos import render_demo

    warnings: list[dict[str, str]] = []
    try:
        md = render_demo(domain_spec.to_dict())
    except Exception as exc:  # noqa: BLE001
        _logger.warning("Demo-script render failed for %s: %s", fqn, exc)
        return {"table": None, "chars": 0,
                "warnings": [{"category": "demo_script", "name": fqn, "error": str(exc)}]}

    table = None
    try:
        table = write_demo_script_row(
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
                "demo_script_md": md,
                "script_chars": len(md),
                "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
    except Exception as exc:  # noqa: BLE001
        _logger.warning("Demo-script write failed for %s: %s", fqn, exc)
        warnings.append({"category": "demo_script", "name": fqn, "error": str(exc)})

    return {"table": table, "chars": len(md), "warnings": warnings}


# --------------------------------------------------------------------------- #
# CLI — backfill demo scripts for already-deployed demos
# --------------------------------------------------------------------------- #

def _local_specs_by_basename() -> dict[str, Any]:
    """Map ``schema_basename -> DomainSpec`` for every local spec JSON."""
    import glob

    from .generator import DomainSpec

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    specs_dir = os.path.join(repo_root, "genie_factory", "specs")
    out: dict[str, Any] = {}
    for path in glob.glob(os.path.join(specs_dir, "*", "*.json")):
        with open(path, encoding="utf-8") as f:
            spec = DomainSpec.from_dict(json.load(f))
        out[spec.schema_basename] = spec
    return out


def backfill(spark: Any, catalog: Optional[str] = None) -> dict[str, Any]:
    """Populate ``demo_scripts`` for every demo already recorded in
    ``space_tag_mapping``. Matches each mapping row to a local spec by
    ``schema_name`` == ``schema_basename`` and upserts the rendered script.
    """
    from .tagging import mapping_table_fqn

    mapping = mapping_table_fqn(spark, catalog)
    rows = spark.sql(
        f"SELECT schema_fqn, catalog, schema_name, space_id, space_title, "
        f"industry, use_case FROM {mapping}"
    ).collect()
    specs = _local_specs_by_basename()

    written, skipped, errors = 0, [], []
    for r in rows:
        spec = specs.get(r["schema_name"])
        if spec is None:
            skipped.append(r["schema_name"])
            continue
        res = record_demo_script(
            spark,
            spec,
            fqn=r["schema_fqn"],
            catalog=r["catalog"] or catalog,
            schema_name=r["schema_name"],
            space_id=r["space_id"],
            space_title=r["space_title"],
        )
        if res["warnings"]:
            errors.extend(res["warnings"])
        else:
            written += 1
    summary = {"written": written, "skipped_no_local_spec": skipped, "errors": errors}
    _logger.info("Demo-script backfill: %s", json.dumps(summary))
    return summary


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(prog="python -m genie_factory.demo_tracking")
    parser.add_argument(
        "--backfill", action="store_true",
        help="Populate demo_scripts for every demo in space_tag_mapping.",
    )
    parser.add_argument("--catalog", default=None, help="Target catalog (default: current).")
    args = parser.parse_args()

    if not args.backfill:
        parser.print_help()
        return

    from pyspark.sql import SparkSession

    spark = SparkSession.getActiveSession()
    if spark is None:
        raise SystemExit("No active Spark session — run inside a Databricks notebook.")
    summary = backfill(spark, catalog=args.catalog)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
