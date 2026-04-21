# Benchmark Baseline Report

Source: `benchmark_baseline_20260420_214900.jsonl`  ·  Spaces: **88**  ·  Questions: **616**

## Summary

- **Overall pass rate:** 568/616 (92.2%)
- **Bad:** 48  ·  **Needs review:** 0

## Failure reason codes (across all 88 spaces)

| Reason | Count | Specs affected |
|---|---:|---:|
| `RESULT_MISSING_COLUMNS` | 41 | 34 |
| `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` | 31 | 31 |
| `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` | 8 | 8 |
| `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` | 7 | 6 |
| `RESULT_MISSING_ROWS` | 5 | 5 |
| `EMPTY_RESULT` | 2 | 1 |

## Per-spec pass rate (worst first)

| Pass rate | Spec | Primary failure reasons |
|---|---|---|
| 57% (4/7) | CapitalFlow Machinery - Working Capital Optimization 💰 | `RESULT_MISSING_COLUMNS` (3), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 71% (5/7) | AeroCapital Finance - Working Capital & Cash Flow 💰 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1) |
| 71% (5/7) | AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1) |
| 71% (5/7) | CargoSight Analytics - Load Demand & Shipment Forecasting 📈 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1) |
| 71% (5/7) | HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | LedgerView Industrial - Financial Analytics 💰 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 71% (5/7) | LoadCast Energy - Demand Forecasting & Capacity Planning 📈 | `EMPTY_RESULT` (2) |
| 71% (5/7) | TrackGuard Systems - Predictive Maintenance & Asset Health 🔧 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | AeroLedger Corp - Financial Analytics & Cost Reporting 💰 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | BuildBid Engineering - Bid Creation & Cost Estimation 📝 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1) |
| 86% (6/7) | CapVenture Energy - Capital Investment Simulation 💰 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1) |
| 86% (6/7) | CarbonTrack Midstream - Carbon Intensity Reporting 🌱 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1) |
| 86% (6/7) | ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | ChipFlow - Demand Forecasting 📈 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | FactoryPulse Systems - Production Monitoring 📊 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | FleetEdge Solutions - Fleet Planning & Optimization 🚚 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1) |
| 86% (6/7) | FoodPlan Analytics - Scenario Planning & Simulation 🎯 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | FreshGuard Foods - Quality Event Root Cause Analysis 🔍 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | FreshStock Solutions - Perishable Inventory Optimization 📦 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | IronPulse Manufacturing - Asset Health Monitor 🔧 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | MidStream Dynamics - Scenario Planning & Simulation 🎯 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1) |
| 86% (6/7) | MineOps Central - Production Monitoring Control Center 📊 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | MineTruck Analytics - Haul Vehicle Asset Health 🔧 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | NucleoSafe Systems - Nuclear Safety & Compliance ☢️ | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | PlanWorks Manufacturing - Resource Planning 🏭 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | PowerMix Dynamics - Grid Management & Energy Mix ⚡ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | PureChem Analytics - Quality Event Root Cause Analysis 🔍 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | RailRoute Logistics - Route Planning & Optimization 🗺️ | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | RestorePower Gen - Outage Response & Restoration 🔌 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | SemiLedger - Financial Analytics & Reporting 💰 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | SiliconPath - Design Space Simulation 🧪 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | SiteTrack Construction - Project Completion Monitoring 🏗️ | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | SpendLens Manufacturing - Spend Intelligence 💰 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | StockSmart Distribution - Inventory Optimization 📦 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | TraceCore Materials - Product & Process Traceability 📋 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1) |
| 86% (6/7) | TraceFood Systems - Product Traceability & Recall 📋 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️ | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1) |
| 86% (6/7) | WaferVault - Salable Inventory Optimization 📦 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | WindPeak Energy - Wind Farm Optimization 💨 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 100% (7/7) | AeroChain Logistics - Supply & Materials Planning 🔗 |  |
| 100% (7/7) | AeroGuard Systems - Predictive Maintenance & Asset Health 🔧 |  |
| 100% (7/7) | AeroParts Supply - Demand Forecasting & Backlog 📈 |  |
| 100% (7/7) | AeroQuality Corp - Quality Event Root Cause Analysis 🔍 |  |
| 100% (7/7) | AeroTrace Systems - Product Traceability & Anti-Counterfeit 🛡️ |  |
| 100% (7/7) | Apex Motor Group - Recall & Defect Analytics 🚨 |  |
| 100% (7/7) | AssemblyGuard Systems - Predictive Maintenance 🔧 |  |
| 100% (7/7) | AutoMetrics - Feature Usage & Adoption Analytics 📱 |  |
| 100% (7/7) | CapAlloc - Supply & Capacity Allocation 🔗 |  |
| 100% (7/7) | CashFlow Energy - Working Capital & Cash Flow Optimization 💰 |  |
| 100% (7/7) | ChipArchitect Labs - SoC Design Space Simulation 🧪 |  |
| 100% (7/7) | CompliFlow Systems - Regulation & Compliance 📋 |  |
| 100% (7/7) | DeepHorizon Energy - Predictive Maintenance & Asset Health 🔧 |  |
| 100% (7/7) | DistroCapital Finance - Working Capital & Cash Flow 💰 |  |
| 100% (7/7) | DistroForecast Systems - Demand Forecasting & Backlog 📈 |  |
| 100% (7/7) | DriveWell - Vehicle Health & Maintenance Analytics 🚗 |  |
| 100% (7/7) | FabSight - Virtual Metrology & Defect Detection 🔬 |  |
| 100% (7/7) | FieldForce Machinery - Field Service Assistant 🛠️ |  |
| 100% (7/7) | ForecastPro Machinery - Demand Forecasting 📈 |  |
| 100% (7/7) | FreightSight Analytics - Freight Demand Forecasting 📈 |  |
| 100% (7/7) | GridGuard Utilities - Transformer Asset Health ⚡ |  |
| 100% (7/7) | HeatTrack Refining - Energy Use Monitoring & Heat Optimization 🌡️ |  |
| 100% (7/7) | LabAuto Sciences - Autonomous Lab Experiments & Optimization 🧪 |  |
| 100% (7/7) | MidCapital Systems - Working Capital & Cash Flow Optimization 💰 |  |
| 100% (7/7) | MidLedger Analytics - Financial Analytics & Reporting 💰 |  |
| 100% (7/7) | MidSpend Analytics - Spend Intelligence 💰 |  |
| 100% (7/7) | NanoVista - Quality Event RCA 🔍 |  |
| 100% (7/7) | PartsVault Industrial - Spare Parts Optimization 📦 |  |
| 100% (7/7) | PetroLedger Corp - Financial Analytics & Reporting 💰 |  |
| 100% (7/7) | PetroPulse Integrated - Production Monitoring Control Center 📊 |  |
| 100% (7/7) | PipeRoute Midstream - Logistics Optimization 🚚 |  |
| 100% (7/7) | PowerGrid Analytics - Grid Management & Energy Mix ⚡ |  |
| 100% (7/7) | PowerLedger Corp - Financial Analytics & Reporting 💰 |  |
| 100% (7/7) | PrecisionEdge Corp - Machining Defect Detection ⚙️ |  |
| 100% (7/7) | QualityFirst Manufacturing - Quality RCA 🔍 |  |
| 100% (7/7) | QualityRefine Analytics - Quality Event Root Cause Analysis 🔍 |  |
| 100% (7/7) | RefineCapital Systems - Working Capital & Cash Flow Optimization 💰 |  |
| 100% (7/7) | RefineGuard Systems - Predictive Maintenance & Asset Health 🔧 |  |
| 100% (7/7) | RefineLedger Corp - Financial Analytics & Reporting 💰 |  |
| 100% (7/7) | RefineOps Central - Production Monitoring 📊 |  |
| 100% (7/7) | ReservoirSight Analytics - Reservoir Management 🛢️ |  |
| 100% (7/7) | RestorePower Systems - Outage Response & Crew Dispatch 🔌 |  |
| 100% (7/7) | SafeDesign - Safety Simulation Analytics 🧪 |  |
| 100% (7/7) | SolarEdge Power - Solar & Storage Optimization ☀️ |  |
| 100% (7/7) | StratOil Dynamics - Scenario Planning & Business Simulation 🎯 |  |
| 100% (7/7) | TradeFlow Energy - Energy Trading Analytics ⚡ |  |
| 100% (7/7) | VisionTech Electronics - Visual Defect Detection 🔬 |  |
| 100% (7/7) | WellFlow Monitoring - Well Production Monitoring 📊 |  |
| 100% (7/7) | WellGuard Upstream - Predictive Maintenance & Asset Health 🔧 |  |

## Failing questions (per spec)

### CapitalFlow Machinery - Working Capital Optimization 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique business units?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: How has total outflow count changed over time?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What is the monthly trend in total inflow count?

### AeroCapital Finance - Working Capital & Cash Flow 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique programs?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What is the monthly trend in total inflows count?

### AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique configs changed over time?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: How has unique simulations changed over time?

### CargoSight Analytics - Load Demand & Shipment Forecasting 📈  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How many records are there per month being forecasted?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: How has total weight delivered lbs count changed over time?

### HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total turbines changed over time?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in generating turbine count?

### LedgerView Industrial - Financial Analytics 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What is the average variance percentage by cost center type?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in total monthly revenue?

### LoadCast Energy - Demand Forecasting & Capacity Planning 📈  —  5/7 pass

- **BAD** (EMPTY_RESULT)
  - Q: How has unique territorys changed over time?
- **BAD** (EMPTY_RESULT)
  - Q: What is the monthly trend in unique readings?

### TrackGuard Systems - Predictive Maintenance & Asset Health 🔧  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: How has unique events changed over time?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique assets changed over time?

### AeroLedger Corp - Financial Analytics & Cost Reporting 💰  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique cost centers?

### BuildBid Engineering - Bid Creation & Cost Estimation 📝  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: How has unique bids changed over time?

### CapVenture Energy - Capital Investment Simulation 💰  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total transactionss?

### CarbonTrack Midstream - Carbon Intensity Reporting 🌱  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest monthly co2e tons?

### ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How many records are there per month being forecasted?

### ChipFlow - Demand Forecasting 📈  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique skus changed over time?

### FactoryPulse Systems - Production Monitoring 📊  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in total output units?

### FleetEdge Solutions - Fleet Planning & Optimization 🚚  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: How has unique operations changed over time?

### FoodPlan Analytics - Scenario Planning & Simulation 🎯  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique categorys changed over time?

### FreshGuard Foods - Quality Event Root Cause Analysis 🔍  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique products changed over time?

### FreshStock Solutions - Perishable Inventory Optimization 📦  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique items?

### IronPulse Manufacturing - Asset Health Monitor 🔧  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique assets?

### MidStream Dynamics - Scenario Planning & Simulation 🎯  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What are the top 10 scenario id by total revenue impact millions usd?

### MineOps Central - Production Monitoring Control Center 📊  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total units changed over time?

### MineTruck Analytics - Haul Vehicle Asset Health 🔧  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique vehicles changed over time?

### NucleoSafe Systems - Nuclear Safety & Compliance ☢️  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique components changed over time?

### PlanWorks Manufacturing - Resource Planning 🏭  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique work centers changed over time?

### PowerMix Dynamics - Grid Management & Energy Mix ⚡  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total plants changed over time?

### PureChem Analytics - Quality Event Root Cause Analysis 🔍  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has total quality events per month changed over time?

### RailRoute Logistics - Route Planning & Optimization 🗺️  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique corridors?

### RestorePower Gen - Outage Response & Restoration 🔌  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total units changed over time?

### SemiLedger - Financial Analytics & Reporting 💰  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique cost centers changed over time?

### SiliconPath - Design Space Simulation 🧪  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How many records are there per month of the optimization result?

### SiteTrack Construction - Project Completion Monitoring 🏗️  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique projects?

### SpendLens Manufacturing - Spend Intelligence 💰  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique suppliers?

### StockSmart Distribution - Inventory Optimization 📦  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique items?

### TraceCore Materials - Product & Process Traceability 📋  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: How has failed quality checks count changed over time?

### TraceFood Systems - Product Traceability & Recall 📋  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique products changed over time?

### TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What are the top 10 unique vehicle by total maximum load capacity in kilograms?

### WaferVault - Salable Inventory Optimization 📦  —  6/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has highest on hand units changed over time?

### WindPeak Energy - Wind Farm Optimization 💨  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total turbines changed over time?
