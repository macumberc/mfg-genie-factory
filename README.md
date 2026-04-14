<p align="center">
  <img src="assets/genie-icon.svg" width="72" alt="Genie">
</p>

<h1 align="center">Genie Factory</h1>

<p align="center">
  Deploy a fully configured <a href="https://docs.databricks.com/en/genie/index.html">Databricks Genie</a> room for any manufacturing use case — via the <b>Databricks App</b> or a notebook.<br>
  88 pre-built use cases across 18 subindustries. No configuration required — just pick and deploy.
</p>

<br>

## Get Started

### Option 1: Databricks App (recommended)

The app provides a web UI for browsing, deploying, and managing Genie rooms.

1. Open the app at your workspace URL (e.g. `https://genie-factory-<workspace-id>.aws.databricksapps.com`)
2. Pick a manufacturing subindustry and use case from the Quick Deploy grid
3. Click **Deploy Now** — your Genie room is ready in ~2 minutes

Each deployment creates a Unity Catalog schema with synthetic Delta tables, governed metric views, and a Genie space pre-configured with sample questions and benchmarks.

#### App Features

- **Quick Deploy** — pick a subindustry + use case, deploy in ~2 minutes with pre-built specs (no LLM)
- **Manage** — view, filter, and teardown your deployments
- **Admin** — deployment analytics, manager roles, warehouse policy, bulk teardown, backend table management
- **Request a Use Case** — submit a request for a new use case directly from the app

<details>
<summary>Deploy the app to your own workspace</summary>

The included deploy script handles everything: backend table creation, SP permission grants, admin bootstrap, and app deployment.

```bash
./scripts/deploy_app.sh --profile <your-cli-profile>
```

The script:
1. Creates the `genie_factory` metadata schema and 4 backend tables (managers, settings, deployment_log, audit_log)
2. Grants the app's Service Principal catalog access, schema privileges, warehouse `CAN_MANAGE`, and `/Users` directory access
3. Adds you as the first admin
4. Deploys the app

**Manual deploy** (without the script):
```bash
databricks apps deploy genie-factory \
  --source-code-path /Workspace/Users/<you>/genie-factory \
  --profile <profile>
```

Note: manual deploys require that backend tables and SP permissions were set up previously (via the script or manually).

</details>

### Option 2: Quickstart Notebook

1. Download [`notebooks/quickstart.py`](notebooks/quickstart.py) and import it into your Databricks workspace
2. Follow the step-by-step instructions — pick a subindustry, pick a use case, run deploy
3. Your Genie room will be ready in 2-4 minutes

<details>
<summary>Or install via pip and use directly</summary>

```python
%pip install git+https://github.com/macumberc/genie-factory.git@manufacturing
dbutils.library.restartPython()
```

```python
from genie_factory import deploy_use_case, teardown

result = deploy_use_case("Automotive", "Vehicle Recall Root Cause Analysis")

# When done:
# teardown(**result)
```

</details>

<br>

## What Gets Created

Each deployment creates:

- **Unity Catalog schema** scoped to your username (ownership transferred to you after creation)
- **3 Delta tables** with realistic synthetic data (~8,000 rows), column comments, and descriptions
- **2 metric views** with governed measures and dimensions
- **Genie space** with 7 sample questions, 7 example SQLs, and 7 benchmarks

Tables, views, and schema ownership are transferred to the deploying user. A separate [`notebooks/cleanup.py`](notebooks/cleanup.py) notebook is included for tearing down deployments.

> **Requirement:** Serverless compute or Databricks Runtime 14.3+ with Unity Catalog enabled.

<br>

## Available Use Cases

88 ready-to-deploy use cases across 18 manufacturing subindustries.

| Subindustry | Use Cases |
|:---|:---|
| **Automotive** | Vehicle Recall Root Cause Analysis · Vehicle Health & Maintenance Report · Product Feature Usage Analytics · Design Space Simulation for Safety |
| **Semiconductor** | Quality Event Root Cause Analysis · Design Space Simulation · Virtual Metrology Defect Detection · Demand Forecasting · Salable Inventory Optimization · Supply & Materials Capacity Allocation · Financial Analytics & Reporting |
| **Computer & Electronic** | Visual Defect Detection · Predictive Maintenance Troubleshoot · Design Space Simulation System on Chip |
| **Logistics** | Route Planning · Fleet Planning and Optimization · Load Demand Forecasting |
| **Chemicals & Materials** | Demand Forecasting · Autonomous Lab Experiments · Quality Event Root Cause Analysis · Product & Process Traceability |
| **Machinery** | Asset Health · Machining Process Defect Detection · Production Monitoring · Field Service Assistant · Quality Event Root Cause Analysis · Demand Forecasting · Spare Part Inventory Optimization · Manufacturing Resource Planning · Working Capital & Cash Flow Optimization · Financial Analytics & Reporting · Spend Intelligence |
| **Oil & Gas Integrated** | Predictive Maintenance & Asset Health · Production Monitoring & Control Center · Scenario Planning & Business Simulation · Capital Investment Simulation · Financial Analytics & Reporting · Working Capital & Cash Flow Optimization |
| **Oil & Gas Refining** | Predictive Maintenance & Asset Health · Quality Event Root Cause Analysis · Energy Use Monitoring Heat · Production Monitoring · Financial Analytics & Reporting · Working Capital & Cash Flow Optimization |
| **Oil & Gas Midstream** | Logistics Optimization · Regulation & Compliance · Scenario Planning & Business Simulation · Energy Trading · Financial Analytics & Reporting · Automated Reporting of Carbon Intensity · Working Capital & Cash Flow Optimization · Spend Intelligence |
| **Oil & Gas Upstream** | Predictive Maintenance & Asset Health · Reservoir Management · Well Production Monitoring & Flow |
| **Electric Utility** | Transformer Asset Health · Grid Management & Energy Mix · Demand Forecasting · Outage Response |
| **Aerospace** | Predictive Maintenance & Asset Health · Design Space Simulation for Fuel Efficiency · Quality Event Root Cause Analysis · Demand Forecasting · Supply & Materials Planning · Product Traceability Anti-counterfeit · Working Capital & Cash Flow Optimization · Financial Analytics & Reporting |
| **Power Generation** | Grid Management & Energy Mix · Outage Response · Nuclear Safety · Hydro Optimization · Solar Optimization Behind the Meter · Wind Optimization · Financial Analytics & Reporting |
| **Industrial Distribution** | Demand Forecasting · Inventory Optimization · Working Capital & Cash Flow Optimization |
| **Railroad** | Route Planning · Predictive Maintenance & Asset Health · Freight Demand Forecasting |
| **Mining** | Haul Vehicle Asset Health · Production Monitoring & Control Center |
| **Food & Beverage** | Quality Event Root Cause Analysis · Product & Process Traceability Recall · Inventory Optimization · Scenario Planning & Business Simulation |
| **Construction & Engineering** | Engineering Bid Creation · Production and Project Completion Monitoring |
