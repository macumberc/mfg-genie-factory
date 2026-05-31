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

# MAGIC %pip install --quiet git+https://github.com/macumberc/mfg-genie-factory.git@main
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run the refresh

# COMMAND ----------

import json
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

# Auto-grant CAN_MANAGE to this workspace's admin group on every space the
# refresh recreates. Job parameter `admin_groups` overrides if set.
os.environ.setdefault("GENIE_FACTORY_ADMIN_GROUPS", "genie-factory-admins")
try:
    admin_groups = dbutils.widgets.get("admin_groups")  # noqa: F821
    if admin_groups:
        os.environ["GENIE_FACTORY_ADMIN_GROUPS"] = admin_groups
except Exception:
    pass

# Make every deployed space usable by all workspace users out of the box:
# CAN_RUN on the Genie space for the workspace `users` group, and USE SCHEMA +
# SELECT on the backing schema for the account-level `account users` group
# (Genie runs queries as the asking user, so both the space grant AND the UC
# data grant are required). These have safe defaults baked into the library;
# the job params `user_groups` / `data_grant_groups` override (set to "" to
# disable). NOTE: users also need CAN_USE on a SQL warehouse — that is an
# environment-level grant a workspace admin must apply; the library can't.
try:
    user_groups = dbutils.widgets.get("user_groups")  # noqa: F821
    if user_groups:
        os.environ["GENIE_FACTORY_USER_GROUPS"] = user_groups
except Exception:
    pass
try:
    data_grant_groups = dbutils.widgets.get("data_grant_groups")  # noqa: F821
    if data_grant_groups:
        os.environ["GENIE_FACTORY_DATA_GRANT_GROUPS"] = data_grant_groups
except Exception:
    pass

# Optional: restrict the refresh to a comma-separated list of subindustry
# slugs (e.g. "logistics,machinery,oil_gas_upstream"). Empty / unset → all 88.
# Lets a workspace that only deployed a subset stay scoped to that subset on
# every monthly cycle.
subindustries: list[str] | None = None
try:
    raw_subs = dbutils.widgets.get("subindustries")  # noqa: F821
    if raw_subs:
        subindustries = [s.strip() for s in raw_subs.split(",") if s.strip()]
except Exception:
    pass

# Optional: pin the target Unity Catalog. Empty / unset → engine resolves via
# current_catalog() with fallback. Set to deploy a workspace's specs under a
# specific catalog (e.g. "manufacturing") instead of the workspace default.
catalog: str | None = None
try:
    raw_catalog = dbutils.widgets.get("catalog")  # noqa: F821
    if raw_catalog:
        catalog = raw_catalog.strip()
except Exception:
    pass

# Optional: "true" wipes every managed schema + Genie space (scoped to the same
# `subindustries` filter) BEFORE redeploying. Default off — the monthly cron is
# idempotent and does not need a destructive wipe; set "true" only for an
# intentional fresh redeploy.
teardown_first = False
try:
    teardown_first = dbutils.widgets.get("teardown_first").strip().lower() == "true"  # noqa: F821
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

from genie_factory.refresh import refresh_all, teardown_all

# Optional clean wipe before redeploy. Uses the same `subindustries` scope so a
# subset wipe stays scoped. A WorkspaceClient is needed to delete Genie spaces.
if teardown_first:
    from databricks.sdk import WorkspaceClient

    logging.getLogger("genie_factory").info(
        "teardown_first=true — wiping managed schemas + Genie spaces before redeploy"
    )
    teardown_manifest = teardown_all(  # noqa: F821
        concurrency=concurrency,
        spark=spark,  # noqa: F821
        subindustries=subindustries,
        workspace_client=WorkspaceClient(),
    )
    print("TEARDOWN:", json.dumps(  # noqa: F821
        {k: teardown_manifest.get(k) for k in ("total", "success", "error")},
    ))

# `spark` is auto-injected in Databricks notebook environments; pass it
# explicitly because SparkSession.getActiveSession() is thread-local and
# returns None inside refresh_all's ThreadPoolExecutor workers.
manifest = refresh_all(  # noqa: F821
    concurrency=concurrency,
    spark=spark,  # noqa: F821
    subindustries=subindustries,
    catalog=catalog,
)

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
