"""Monthly refresh job: tear down and redeploy all 88 manufacturing demos.

This module is invoked monthly by a Databricks Workflow to keep the
rolling-date data window current. Each refresh:

  1. Lists every (subindustry, use_case) pair available via presets.
  2. For each, calls ``genie_factory.notebook.deploy_use_case(...)`` which
     drops the schema, regenerates data from the current calendar, and
     replaces the Genie space with a fresh one. ``deploy()`` is already
     idempotent — it CREATE OR REPLACEs tables, transfers ownership, and
     replaces managed Genie spaces.
  3. Reports per-spec outcome to a JSON manifest written into a workspace
     volume so the operator can spot-check.

Concurrency stays at 3 to respect the workspace's 5-qpm Genie space
creation cap (see CLAUDE.md).

Run via the Databricks notebook task in ``notebooks/monthly_refresh.py``
or locally with::

    python -m genie_factory.refresh --concurrency 3

Environment overrides:

  GENIE_FACTORY_END_DATE     pin the calendar end date (ISO yyyy-mm-dd)
  GENIE_FACTORY_REFRESH_OUT  path to write per-spec result JSON
  GENIE_FACTORY_CONCURRENCY  override concurrency (default 3)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

from .presets import SUBINDUSTRIES, USE_CASES

_logger = logging.getLogger("genie_factory.refresh")


def _all_use_case_pairs(
    subindustry_slugs: list[str] | None = None,
) -> list[tuple[str, str]]:
    """Return every (subindustry, use_case_label) pair in the preset corpus.

    ``subindustry_slugs`` optionally filters to one or more subindustries by
    their slug form (e.g. ``["logistics", "machinery"]``).
    """
    from .specs import _slugify

    keep: set[str] | None = None
    if subindustry_slugs:
        keep = set(subindustry_slugs)
    pairs: list[tuple[str, str]] = []
    for sub in SUBINDUSTRIES:
        if keep is not None and _slugify(sub) not in keep:
            continue
        for uc in USE_CASES.get(sub, []):
            pairs.append((sub, uc["label"]))
    return pairs


def _deploy_one(sub: str, label: str, spark: Any = None, catalog: str | None = None) -> dict[str, Any]:
    """Run a single deploy. Catches all errors so one bad spec doesn't
    abort the whole refresh. ``spark`` is captured on the orchestrator
    thread and passed in because ``SparkSession.getActiveSession()`` is
    thread-local on Databricks runtimes and returns None in worker threads.
    """
    from .notebook import deploy_use_case

    started = time.time()
    overrides: dict[str, Any] = {}
    if spark is not None:
        overrides["spark"] = spark
    if catalog:
        overrides["catalog"] = catalog
    try:
        result = deploy_use_case(sub, label, **overrides)
        return {
            "subindustry": sub,
            "use_case": label,
            "status": "success",
            "duration_seconds": round(time.time() - started, 1),
            "fqn": result.get("fqn"),
            "tables": result.get("tables"),
            "genie": result.get("genie"),
            "warnings": result.get("warnings", []),
        }
    except Exception as exc:  # noqa: BLE001 — we genuinely want to swallow per-spec
        return {
            "subindustry": sub,
            "use_case": label,
            "status": "error",
            "duration_seconds": round(time.time() - started, 1),
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }


def _teardown_one(sub: str, label: str, spark: Any, workspace_client: Any = None) -> dict[str, Any]:
    """Tear down a single spec's schema + Genie space(s).

    Looks up the spec's expected title (``"<industry> - <space_title>"``)
    and deletes every matching Genie space (handling Databricks'
    timestamp-suffix variant via ``find_managed_spaces``). Then drops the
    schema CASCADE.

    Implemented directly rather than calling ``cleanup()`` because
    ``cleanup()``'s space-resolution path falls back to a legacy
    ``fqn=<...>`` description marker that current deploys don't emit.
    Catches all errors so one bad spec doesn't abort the whole teardown.
    """
    from .genie import (
        _default_workspace_client,
        delete_genie_space,
        find_managed_spaces,
    )
    from .specs import load_spec
    from .validators import resolve_namespace

    started = time.time()
    try:
        spec = load_spec(sub, label)
        if spec is None:
            return {
                "subindustry": sub,
                "use_case": label,
                "status": "skipped",
                "duration_seconds": round(time.time() - started, 1),
                "error": "spec not found on disk",
            }
        ns = resolve_namespace(spark, catalog=None, schema=None,
                               schema_basename=spec.schema_basename)
        ws = workspace_client or _default_workspace_client()
        notes: list[str] = []

        # 1. Delete managed Genie spaces by expected title.
        expected_title = f"{spec.industry} - {spec.space_title}"
        deleted_space_ids: list[str] = []
        try:
            managed = find_managed_spaces(spark, ns.fqn, title=expected_title, workspace_client=ws)
            for s in managed:
                sid = s.get("space_id")
                if not sid:
                    continue
                try:
                    delete_genie_space(spark, sid, workspace_client=ws)
                    deleted_space_ids.append(sid)
                except Exception as exc:  # noqa: BLE001
                    notes.append(f"Failed to delete Genie space {sid}: {exc}")
        except Exception as exc:  # noqa: BLE001
            notes.append(f"Failed to list managed Genie spaces for {ns.fqn}: {exc}")

        # 2. Drop schema CASCADE.
        dropped_schema = False
        try:
            spark.sql(f"DROP SCHEMA IF EXISTS {ns.fqn} CASCADE")
            dropped_schema = True
        except Exception as exc:  # noqa: BLE001
            notes.append(f"Failed to drop schema {ns.fqn}: {exc}")

        return {
            "subindustry": sub,
            "use_case": label,
            "status": "success",
            "duration_seconds": round(time.time() - started, 1),
            "fqn": ns.fqn,
            "dropped_schema": dropped_schema,
            "deleted_space_ids": deleted_space_ids,
            "notes": notes,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "subindustry": sub,
            "use_case": label,
            "status": "error",
            "duration_seconds": round(time.time() - started, 1),
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }


def teardown_all(
    concurrency: int = 3,
    out_path: Path | None = None,
    spark: Any = None,
    subindustries: list[str] | None = None,
    workspace_client: Any = None,
) -> dict[str, Any]:
    """Tear down every spec in parallel: drop schemas + delete Genie spaces.

    Mirrors ``refresh_all``'s shape so the manifest surfaces the same way
    in the bundle job-output. Default scope is all 88 specs;
    ``subindustries`` optionally filters to a subset.
    """
    pairs = _all_use_case_pairs(subindustries)
    _logger.info(
        "Starting teardown of %d demos at concurrency %d (filter=%s)",
        len(pairs), concurrency, subindustries or "ALL",
    )

    if spark is None:
        try:
            from pyspark.sql import SparkSession
            spark = SparkSession.getActiveSession()
        except Exception:  # noqa: BLE001
            spark = None

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {
            pool.submit(_teardown_one, sub, label, spark, workspace_client): (sub, label)
            for sub, label in pairs
        }
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            _logger.info("[%s] %s/%s in %ss", r["status"].upper(),
                         r["subindustry"], r["use_case"], r["duration_seconds"])

    ok = sum(1 for r in results if r["status"] == "success")
    err = sum(1 for r in results if r["status"] == "error")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    manifest = {
        "ran_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "operation": "teardown",
        "concurrency": concurrency,
        "total": len(results),
        "success": ok,
        "error": err,
        "skipped": skipped,
        "results": sorted(results, key=lambda r: (r["subindustry"], r["use_case"])),
    }

    if out_path is None:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_path = Path(os.environ.get(
            "GENIE_FACTORY_REFRESH_OUT", f"/tmp/genie_factory_teardown_{ts}.json"
        ))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2))

    _logger.info("Teardown complete: %d/%d success, %d error, %d skipped. Manifest: %s",
                 ok, len(results), err, skipped, out_path)
    return manifest


def refresh_all(
    concurrency: int = 3,
    out_path: Path | None = None,
    spark: Any = None,
    subindustries: list[str] | None = None,
    catalog: str | None = None,
) -> dict[str, Any]:
    """Refresh every spec in parallel (bounded by ``concurrency``).

    Returns a manifest dict with per-spec results and an overall summary.
    Writes the manifest to ``out_path`` (defaults to
    ``/tmp/genie_factory_refresh_<UTC timestamp>.json``).

    ``spark`` must be supplied when invoked from a Databricks notebook —
    pass the global ``spark`` from the calling cell. ``SparkSession.
    getActiveSession()`` is thread-local on Databricks runtimes and
    returns None inside the ThreadPoolExecutor workers, so we capture it
    here and forward to each ``_deploy_one`` call explicitly.
    """
    pairs = _all_use_case_pairs(subindustries)
    _logger.info(
        "Starting refresh of %d demos at concurrency %d (anchor=%s, filter=%s)",
        len(pairs),
        concurrency,
        os.environ.get("GENIE_FACTORY_END_DATE") or "CURRENT_DATE()",
        subindustries or "ALL",
    )

    # If the caller didn't pass spark, try to resolve it from the active
    # session on this (main) thread. Worker threads can't, so we capture
    # it here once.
    if spark is None:
        try:
            from pyspark.sql import SparkSession
            spark = SparkSession.getActiveSession()
        except Exception:  # noqa: BLE001
            spark = None

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(_deploy_one, sub, label, spark, catalog): (sub, label) for sub, label in pairs}
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            tag = r["status"].upper()
            _logger.info("[%s] %s/%s in %ss", tag, r["subindustry"], r["use_case"], r["duration_seconds"])

    ok = sum(1 for r in results if r["status"] == "success")
    err = sum(1 for r in results if r["status"] == "error")
    manifest = {
        "ran_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "anchor_date": os.environ.get("GENIE_FACTORY_END_DATE") or "CURRENT_DATE()",
        "concurrency": concurrency,
        "total": len(results),
        "success": ok,
        "error": err,
        "results": sorted(results, key=lambda r: (r["subindustry"], r["use_case"])),
    }

    if out_path is None:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_path = Path(os.environ.get("GENIE_FACTORY_REFRESH_OUT", f"/tmp/genie_factory_refresh_{ts}.json"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2))

    _logger.info("Refresh complete: %d/%d success, %d error. Manifest: %s", ok, len(results), err, out_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--concurrency",
        type=int,
        default=int(os.environ.get("GENIE_FACTORY_CONCURRENCY", "3")),
        help="parallel deploys (default 3 to stay under 5 qpm Genie cap)",
    )
    parser.add_argument("--out", type=Path, default=None, help="manifest output path")
    parser.add_argument(
        "--subindustries",
        default=None,
        help="comma-separated subindustry slugs to refresh/teardown (default: all 88 specs)",
    )
    parser.add_argument(
        "--teardown",
        action="store_true",
        help="DESTRUCTIVE: drop schemas + delete Genie spaces instead of deploying",
    )
    parser.add_argument(
        "--catalog",
        default=os.environ.get("GENIE_FACTORY_CATALOG") or None,
        help="target catalog for deploys (default: workspace current_catalog())",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    subs = (
        [s.strip() for s in args.subindustries.split(",") if s.strip()]
        if args.subindustries else None
    )
    if args.teardown:
        manifest = teardown_all(
            concurrency=args.concurrency, out_path=args.out, subindustries=subs,
        )
    else:
        manifest = refresh_all(
            concurrency=args.concurrency, out_path=args.out, subindustries=subs,
            catalog=args.catalog,
        )
    return 0 if manifest["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
