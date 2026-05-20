# Databricks notebook source
# MAGIC %md
# MAGIC # Monthly demo refresh — Manufacturing Genie spaces
# MAGIC
# MAGIC This notebook is the task body for the scheduled Databricks Workflow
# MAGIC that re-runs every preset deploy once a month. Because the engine
# MAGIC now generates rolling current-date data (``CURRENT_DATE()`` end), the
# MAGIC monthly cadence keeps the trailing-12-month window inside the data.
# MAGIC
# MAGIC The refresh is idempotent: ``deploy()`` CREATE OR REPLACEs tables,
# MAGIC re-creates metric views, and replaces the managed Genie space.
# MAGIC Spaces retain their friendly title (`<industry> - <space_title>`) so
# MAGIC any direct URL share keeps working.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install the library

# COMMAND ----------

# MAGIC %pip install --quiet git+https://github.com/macumberc/mfg-genie-factory.git@chad/data-quality-remediation
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run the refresh

# COMMAND ----------

import logging
import os

# Default to 3-way concurrency to respect the 5-qpm Genie API cap.
# Override via the job's parameter `concurrency` if needed.
try:
    concurrency = int(dbutils.widgets.get("concurrency"))  # noqa: F821
except Exception:
    concurrency = 3

# Optional: pin the data window end (ISO yyyy-mm-dd). When omitted, the
# engine rolls with CURRENT_DATE().
try:
    end_date = dbutils.widgets.get("end_date")  # noqa: F821
    if end_date:
        os.environ["GENIE_FACTORY_END_DATE"] = end_date
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

from genie_factory.refresh import refresh_all

manifest = refresh_all(concurrency=concurrency)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Surface the result on the job UI

# COMMAND ----------

import json

print("=" * 72)
print(f"REFRESH MANIFEST  ({manifest['ran_at']})")
print("=" * 72)
print(f"  anchor   : {manifest['anchor_date']}")
print(f"  total    : {manifest['total']}")
print(f"  success  : {manifest['success']}")
print(f"  error    : {manifest['error']}")
print(f"  concurr. : {manifest['concurrency']}")
print()
if manifest["error"]:
    print(f"ERRORS ({manifest['error']} of {manifest['total']}):")
    # Show full traceback for the FIRST error so we can diagnose; then a
    # one-line summary for the rest.
    first_err_shown = False
    for r in manifest["results"]:
        if r["status"] != "error":
            continue
        if not first_err_shown:
            print(f"\n--- First failure: {r['subindustry']}/{r['use_case']} ---")
            print(f"error: {r.get('error','')}")
            print("traceback:")
            print(r.get("traceback", "(no traceback)"))
            print("--- end first failure ---\n")
            first_err_shown = True
        else:
            print(f"  {r['subindustry']}/{r['use_case']}: {r.get('error','')[:140]}")
    print()

# Return the manifest summary plus the first failure traceback inline so
# the get-output API surfaces it even when stdout/stderr are not captured.
first_failure = next(
    (r for r in manifest["results"] if r["status"] == "error"),
    None,
)
result_summary = {
    "ran_at": manifest["ran_at"],
    "success": manifest["success"],
    "error": manifest["error"],
    "total": manifest["total"],
}
if first_failure:
    result_summary["first_failure"] = {
        "subindustry": first_failure["subindustry"],
        "use_case": first_failure["use_case"],
        "error": first_failure.get("error", "")[:500],
        "traceback": (first_failure.get("traceback") or "")[-3000:],
    }
dbutils.notebook.exit(json.dumps(result_summary))  # noqa: F821
