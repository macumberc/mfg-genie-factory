#!/usr/bin/env bash
# deploy_app.sh — Deploy the Mfg Genie Factory Databricks App
#
# Creates backend tables, grants SP permissions, and deploys the app.
# Usage: ./scripts/deploy_app.sh [--profile PROFILE] [--app-name NAME]
#
# Prerequisites: databricks CLI authenticated with the target workspace.

set -euo pipefail

PROFILE="${DATABRICKS_PROFILE:-mfg-genie-factory}"
APP_NAME="genie-factory"
SCHEMA="genie_factory"
BRANCH="main"
WORKSPACE_PATH=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --app-name) APP_NAME="$2"; shift 2 ;;
    --workspace-path) WORKSPACE_PATH="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

echo "=== Mfg Genie Factory Deploy ==="
echo "Profile:  $PROFILE"
echo "App:      $APP_NAME"

# -------------------------------------------------------------------------
# 1. Get or create the app — find the SP
# -------------------------------------------------------------------------
echo ""
echo "--- Checking app status ---"
APP_JSON=$(databricks apps get "$APP_NAME" --profile "$PROFILE" 2>/dev/null || echo "{}")
SP_CLIENT_ID=$(echo "$APP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('service_principal_client_id',''))" 2>/dev/null)

if [ -z "$SP_CLIENT_ID" ]; then
  echo "App '$APP_NAME' not found. It will be created on first deploy."
  echo "Run the deploy first, then re-run this script to set up permissions."
else
  echo "SP Client ID: $SP_CLIENT_ID"
fi

# -------------------------------------------------------------------------
# 2. Find a running SQL warehouse
# -------------------------------------------------------------------------
echo ""
echo "--- Finding SQL warehouse ---"
WH_ID=$(databricks api get /api/2.0/sql/warehouses --profile "$PROFILE" 2>/dev/null | \
  python3 -c "
import sys, json
whs = json.load(sys.stdin).get('warehouses', [])
running = [w['id'] for w in whs if w.get('state') == 'RUNNING']
print(running[0] if running else (whs[0]['id'] if whs else ''))
" 2>/dev/null)

if [ -z "$WH_ID" ]; then
  echo "ERROR: No SQL warehouses found on workspace."
  exit 1
fi
echo "Warehouse: $WH_ID"

# -------------------------------------------------------------------------
# Helper: run SQL via Statement Execution API
# -------------------------------------------------------------------------
run_sql() {
  local stmt="$1"
  local result
  result=$(databricks api post /api/2.0/sql/statements \
    --profile "$PROFILE" \
    --json "$(python3 -c "import json; print(json.dumps({'warehouse_id': '$WH_ID', 'statement': stmt, 'wait_timeout': '30s'}))" <<< "")" 2>&1)

  # Use python to build the JSON properly
  result=$(python3 -c "
import json, subprocess, sys
stmt = sys.argv[1]
wh = sys.argv[2]
payload = json.dumps({'warehouse_id': wh, 'statement': stmt, 'wait_timeout': '30s'})
proc = subprocess.run(
    ['databricks', 'api', 'post', '/api/2.0/sql/statements', '--profile', '$PROFILE', '--json', payload],
    capture_output=True, text=True
)
print(proc.stdout)
" "$stmt" "$WH_ID" 2>&1)

  local state
  state=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',{}).get('state','?'))" 2>/dev/null)
  local err
  err=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',{}).get('error',{}).get('message',''))" 2>/dev/null)
  if [ "$state" = "SUCCEEDED" ]; then
    echo "  ✓ OK"
  else
    echo "  ✗ $state: $err"
  fi
}

# -------------------------------------------------------------------------
# 3. Find current catalog and create schema + tables
# -------------------------------------------------------------------------
echo ""
echo "--- Finding catalog ---"
CATALOG=$(python3 -c "
import json, subprocess
proc = subprocess.run(
    ['databricks', 'api', 'post', '/api/2.0/sql/statements', '--profile', '$PROFILE',
     '--json', json.dumps({'warehouse_id': '$WH_ID', 'statement': 'SELECT current_catalog()', 'wait_timeout': '30s'})],
    capture_output=True, text=True
)
r = json.loads(proc.stdout)
print(r.get('result',{}).get('data_array',[['']])[0][0])
")
FQN="${CATALOG}.${SCHEMA}"
echo "Catalog:  $CATALOG"
echo "Schema:   $FQN"

echo ""
echo "--- Creating schema and tables ---"
run_sql "CREATE SCHEMA IF NOT EXISTS ${FQN}"
run_sql "CREATE TABLE IF NOT EXISTS ${FQN}.app_managers (email STRING, role STRING, added_by STRING, added_at STRING) USING DELTA"
run_sql "CREATE TABLE IF NOT EXISTS ${FQN}.app_settings (setting_key STRING, setting_value STRING, updated_by STRING, updated_at STRING) USING DELTA"
run_sql "CREATE TABLE IF NOT EXISTS ${FQN}.deployment_log (deployment_id STRING, deployed_by STRING, deployed_at STRING, industry STRING, company_name STRING, use_case STRING, business_context STRING, catalog STRING, schema_name STRING, fqn STRING, warehouse_id STRING, genie_space_id STRING, genie_space_url STRING, genie_space_title STRING, tables_json STRING, total_rows LONG, status STRING, torn_down_at STRING, error_category STRING, error_message STRING, started_at STRING, completed_at STRING, warnings_json STRING, deploy_params_json STRING, torn_down_by STRING) USING DELTA"
run_sql "CREATE TABLE IF NOT EXISTS ${FQN}.audit_log (event_id STRING, event_type STRING, actor_email STRING, target_deployment_id STRING, target_email STRING, details STRING, event_at STRING) USING DELTA"

# -------------------------------------------------------------------------
# 4. Grant SP permissions (if app exists)
# -------------------------------------------------------------------------
if [ -n "$SP_CLIENT_ID" ]; then
  echo ""
  echo "--- Granting SP catalog/schema permissions ---"
  run_sql "GRANT USE CATALOG ON CATALOG \`${CATALOG}\` TO \`${SP_CLIENT_ID}\`"
  run_sql "GRANT USE SCHEMA ON SCHEMA ${FQN} TO \`${SP_CLIENT_ID}\`"
  run_sql "GRANT ALL PRIVILEGES ON SCHEMA ${FQN} TO \`${SP_CLIENT_ID}\`"

  echo ""
  echo "--- Granting SP warehouse permissions ---"
  # SP needs CAN_MANAGE on SQL warehouses to create Genie spaces
  databricks api patch /api/2.0/permissions/sql/warehouses/$WH_ID \
    --profile "$PROFILE" \
    --json "{\"access_control_list\": [{\"service_principal_name\": \"$SP_CLIENT_ID\", \"permission_level\": \"CAN_MANAGE\"}]}" \
    >/dev/null 2>&1 && echo "  ✓ CAN_MANAGE on warehouse $WH_ID" || echo "  ✗ Failed to grant warehouse permission"

  # Grant on ALL warehouses (Genie space creation requires access to the assigned warehouse)
  ALL_WH_IDS=$(databricks api get /api/2.0/sql/warehouses --profile "$PROFILE" 2>/dev/null | \
    python3 -c "import sys,json; [print(w['id']) for w in json.load(sys.stdin).get('warehouses',[])]" 2>/dev/null)
  for wid in $ALL_WH_IDS; do
    if [ "$wid" != "$WH_ID" ]; then
      databricks api patch /api/2.0/permissions/sql/warehouses/$wid \
        --profile "$PROFILE" \
        --json "{\"access_control_list\": [{\"service_principal_name\": \"$SP_CLIENT_ID\", \"permission_level\": \"CAN_MANAGE\"}]}" \
        >/dev/null 2>&1 && echo "  ✓ CAN_MANAGE on warehouse $wid" || true
    fi
  done
fi

# -------------------------------------------------------------------------
# 5. Bootstrap first admin (current user)
# -------------------------------------------------------------------------
echo ""
echo "--- Bootstrapping first admin ---"
DEPLOYER_EMAIL=$(databricks current-user me --profile "$PROFILE" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('userName',''))" 2>/dev/null || echo "")
if [ -n "$DEPLOYER_EMAIL" ]; then
  echo "Deployer: $DEPLOYER_EMAIL"
  NOW=$(date -u +"%Y-%m-%d %H:%M:%S")
  run_sql "MERGE INTO ${FQN}.app_managers AS t USING (SELECT '${DEPLOYER_EMAIL}' AS email) AS s ON t.email = s.email WHEN NOT MATCHED THEN INSERT (email, role, added_by, added_at) VALUES (s.email, 'manager', 'deploy-script', '${NOW}')"
else
  echo "  Could not determine deployer email — add admin manually."
fi

# -------------------------------------------------------------------------
# 6. Deploy the app
# -------------------------------------------------------------------------
echo ""
echo "--- Deploying app ---"
databricks apps deploy "$APP_NAME" \
  --source-code-path "${WORKSPACE_PATH:-/Workspace/Users/$(databricks current-user me --profile "$PROFILE" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('userName',''))" 2>/dev/null)/$APP_NAME}" \
  --profile "$PROFILE"

echo ""
echo "=== Done ==="
echo "App URL: $(echo "$APP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('url','(check Databricks UI)'))" 2>/dev/null)"
