# Benchmark Baseline Report

Source: `benchmark_baseline_20260420_164338.jsonl`  ·  Spaces: **88**  ·  Questions: **616**

## Summary

- **Overall pass rate:** 425/616 (69.0%)
- **Bad:** 191  ·  **Needs review:** 0

## Failure reason codes (across all 88 spaces)

| Reason | Count | Specs affected |
|---|---:|---:|
| `RESULT_MISSING_ROWS` | 88 | 77 |
| `RESULT_MISSING_COLUMNS` | 87 | 62 |
| `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` | 57 | 57 |
| `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` | 55 | 42 |
| `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` | 53 | 48 |
| `RESULT_EXTRA_ROWS` | 14 | 13 |
| `LLM_JUDGE_FORMATTING_ERROR` | 11 | 11 |
| `LLM_JUDGE_OTHER` | 7 | 7 |
| `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` | 3 | 3 |
| `LLM_JUDGE_MISINTERPRETATION_OF_USER_REQUEST` | 2 | 2 |
| `EMPTY_RESULT` | 2 | 1 |
| `LLM_JUDGE_MISSING_OR_INCORRECT_FILTER` | 1 | 1 |

## Per-spec pass rate (worst first)

| Pass rate | Spec | Primary failure reasons |
|---|---|---|
| 43% (3/7) | AutoMetrics - Feature Usage & Adoption Analytics 📱 | `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1) |
| 43% (3/7) | CapAlloc - Supply & Capacity Allocation 🔗 | `RESULT_MISSING_ROWS` (3), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (3), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 43% (3/7) | RefineOps Central - Production Monitoring 📊 | `RESULT_EXTRA_ROWS` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (2), `RESULT_MISSING_COLUMNS` (2) |
| 43% (3/7) | RestorePower Systems - Outage Response & Crew Dispatch 🔌 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_EXTRA_ROWS` (1) |
| 57% (4/7) | AeroCapital Finance - Working Capital & Cash Flow 💰 | `RESULT_MISSING_COLUMNS` (2), `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1) |
| 57% (4/7) | AeroChain Logistics - Supply & Materials Planning 🔗 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | AeroGuard Systems - Predictive Maintenance & Asset Health 🔧 | `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 57% (4/7) | AeroLedger Corp - Financial Analytics & Cost Reporting 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_EXTRA_ROWS` (1) |
| 57% (4/7) | CapitalFlow Machinery - Working Capital Optimization 💰 | `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_MISINTERPRETATION_OF_USER_REQUEST` (1) |
| 57% (4/7) | CarbonTrack Midstream - Carbon Intensity Reporting 🌱 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | CargoSight Analytics - Load Demand & Shipment Forecasting 📈 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | CashFlow Energy - Working Capital & Cash Flow Optimization 💰 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | ChipFlow - Demand Forecasting 📈 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 57% (4/7) | CompliFlow Systems - Regulation & Compliance 📋 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | FreshGuard Foods - Quality Event Root Cause Analysis 🔍 | `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 57% (4/7) | GridGuard Utilities - Transformer Asset Health ⚡ | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | HeatTrack Refining - Energy Use Monitoring & Heat Optimization 🌡️ | `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (3), `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | LedgerView Industrial - Financial Analytics 💰 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | LoadCast Energy - Demand Forecasting & Capacity Planning 📈 | `EMPTY_RESULT` (2), `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 57% (4/7) | MidSpend Analytics - Spend Intelligence 💰 | `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 57% (4/7) | MineOps Central - Production Monitoring Control Center 📊 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 57% (4/7) | PetroPulse Integrated - Production Monitoring Control Center 📊 | `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (2), `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | PipeRoute Midstream - Logistics Optimization 🚚 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_EXTRA_ROWS` (1) |
| 57% (4/7) | PlanWorks Manufacturing - Resource Planning 🏭 | `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 57% (4/7) | PowerGrid Analytics - Grid Management & Energy Mix ⚡ | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | QualityRefine Analytics - Quality Event Root Cause Analysis 🔍 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | RefineCapital Systems - Working Capital & Cash Flow Optimization 💰 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | RefineGuard Systems - Predictive Maintenance & Asset Health 🔧 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 57% (4/7) | SemiLedger - Financial Analytics & Reporting 💰 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 57% (4/7) | TradeFlow Energy - Energy Trading Analytics ⚡ | `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (2), `RESULT_MISSING_COLUMNS` (2), `RESULT_MISSING_ROWS` (1) |
| 57% (4/7) | WellGuard Upstream - Predictive Maintenance & Asset Health 🔧 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (2), `RESULT_MISSING_ROWS` (1) |
| 71% (5/7) | AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_EXTRA_ROWS` (1) |
| 71% (5/7) | BuildBid Engineering - Bid Creation & Cost Estimation 📝 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | CapVenture Energy - Capital Investment Simulation 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_ROWS` (1) |
| 71% (5/7) | DistroCapital Finance - Working Capital & Cash Flow 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | DriveWell - Vehicle Health & Maintenance Analytics 🚗 | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | FabSight - Virtual Metrology & Defect Detection 🔬 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | FactoryPulse Systems - Production Monitoring 📊 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | FieldForce Machinery - Field Service Assistant 🛠️ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | FleetEdge Solutions - Fleet Planning & Optimization 🚚 | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | FoodPlan Analytics - Scenario Planning & Simulation 🎯 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | ForecastPro Machinery - Demand Forecasting 📈 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | FreshStock Solutions - Perishable Inventory Optimization 📦 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | IronPulse Manufacturing - Asset Health Monitor 🔧 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | MidCapital Systems - Working Capital & Cash Flow Optimization 💰 | `RESULT_MISSING_COLUMNS` (2), `LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION` (1), `LLM_JUDGE_INCORRECT_METRIC_CALCULATION` (1) |
| 71% (5/7) | MidLedger Analytics - Financial Analytics & Reporting 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | MidStream Dynamics - Scenario Planning & Simulation 🎯 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | MineTruck Analytics - Haul Vehicle Asset Health 🔧 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | NanoVista - Quality Event RCA 🔍 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | NucleoSafe Systems - Nuclear Safety & Compliance ☢️ | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 71% (5/7) | PetroLedger Corp - Financial Analytics & Reporting 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | PrecisionEdge Corp - Machining Defect Detection ⚙️ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | PureChem Analytics - Quality Event Root Cause Analysis 🔍 | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | RailRoute Logistics - Route Planning & Optimization 🗺️ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | RefineLedger Corp - Financial Analytics & Reporting 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | ReservoirSight Analytics - Reservoir Management 🛢️ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | RestorePower Gen - Outage Response & Restoration 🔌 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | SiliconPath - Design Space Simulation 🧪 | `RESULT_MISSING_COLUMNS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1), `RESULT_MISSING_ROWS` (1) |
| 71% (5/7) | SiteTrack Construction - Project Completion Monitoring 🏗️ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_MISINTERPRETATION_OF_USER_REQUEST` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | SolarEdge Power - Solar & Storage Optimization ☀️ | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1), `RESULT_MISSING_ROWS` (1) |
| 71% (5/7) | SpendLens Manufacturing - Spend Intelligence 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | TraceFood Systems - Product Traceability & Recall 📋 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | TrackGuard Systems - Predictive Maintenance & Asset Health 🔧 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 71% (5/7) | TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | VisionTech Electronics - Visual Defect Detection 🔬 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | WaferVault - Salable Inventory Optimization 📦 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 71% (5/7) | WellFlow Monitoring - Well Production Monitoring 📊 | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `RESULT_MISSING_COLUMNS` (1) |
| 71% (5/7) | WindPeak Energy - Wind Farm Optimization 💨 | `RESULT_MISSING_ROWS` (2), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | AeroParts Supply - Demand Forecasting & Backlog 📈 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | AeroQuality Corp - Quality Event Root Cause Analysis 🔍 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | Apex Motor Group - Recall & Defect Analytics 🚨 | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1) |
| 86% (6/7) | AssemblyGuard Systems - Predictive Maintenance 🔧 | `RESULT_EXTRA_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1) |
| 86% (6/7) | ChipArchitect Labs - SoC Design Space Simulation 🧪 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | DeepHorizon Energy - Predictive Maintenance & Asset Health 🔧 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | DistroForecast Systems - Demand Forecasting & Backlog 📈 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | FreightSight Analytics - Freight Demand Forecasting 📈 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | LabAuto Sciences - Autonomous Lab Experiments & Optimization 🧪 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_FORMATTING_ERROR` (1) |
| 86% (6/7) | PartsVault Industrial - Spare Parts Optimization 📦 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | PowerLedger Corp - Financial Analytics & Reporting 💰 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | PowerMix Dynamics - Grid Management & Energy Mix ⚡ | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` (1) |
| 86% (6/7) | QualityFirst Manufacturing - Quality RCA 🔍 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | SafeDesign - Safety Simulation Analytics 🧪 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | StockSmart Distribution - Inventory Optimization 📦 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | StratOil Dynamics - Scenario Planning & Business Simulation 🎯 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 86% (6/7) | TraceCore Materials - Product & Process Traceability 📋 | `RESULT_MISSING_ROWS` (1), `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` (1) |
| 100% (7/7) | AeroTrace Systems - Product Traceability & Anti-Counterfeit 🛡️ |  |

## Failing questions (per spec)

### AutoMetrics - Feature Usage & Adoption Analytics 📱  —  3/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What is the average average session duration in seconds for the week by vehicle model name?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top unique vehicle identifier by total number of user interactions during the session?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in high churn risk count?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in failed activation count?

### CapAlloc - Supply & Capacity Allocation 🔗  —  3/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top material or component identifier by total quantity ordered (units vary by material)?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest utilization percent?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in critical bottleneck count?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in delayed order count?

### RefineOps Central - Production Monitoring 📊  —  3/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the average average utilization pct by process unit name?
- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top process unit id by total throughput in barrels per day?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in highest avg throughput bpd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total readingss?

### RestorePower Systems - Outage Response & Crew Dispatch 🔌  —  3/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the average crew utilization percentage for the day by service district?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top distribution feeder identifier by total number of customers without power?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total restoration jobs completed?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in storm outage count?

### AeroCapital Finance - Working Capital & Cash Flow 💰  —  4/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top aerospace program identifier by total transaction amount in usd (positive = inflow, negative = outflow)?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique programs?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in total inflows count?

### AeroChain Logistics - Supply & Materials Planning 🔗  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top material identifier by total order quantity in kilograms?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in critical material count?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in late delivery count?

### AeroGuard Systems - Predictive Maintenance & Asset Health 🔧  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top engine serial identifier by total exhaust gas temperature in celsius?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unscheduled removal count?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in critical alert count?

### AeroLedger Corp - Financial Analytics & Cost Reporting 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top cost center identifier by total transaction amount in usd (revenue positive, expenses negative)?
- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique cost centers?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total revenue count?

### CapitalFlow Machinery - Working Capital Optimization 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISINTERPRETATION_OF_USER_REQUEST)
  - Q: What are the top business unit identifier by total transaction amount in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique business units?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_FILTER)
  - Q: What is the monthly trend in total inflow count?

### CarbonTrack Midstream - Carbon Intensity Reporting 🌱  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top emission source id by total co2 equivalent metric tons?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest monthly co2e tons?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest co2e metric tons?

### CargoSight Analytics - Load Demand & Shipment Forecasting 📈  —  4/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How many records are there per month being forecasted?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top shipping lane identifier by total shipment weight in pounds?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total freight revenue count?

### CashFlow Energy - Working Capital & Cash Flow Optimization 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top business unit identifier by total cash flow amount in usd (positive = inflow)?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest accounts receivable?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total inflows usd count?

### ChipFlow - Demand Forecasting 📈  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product sku identifier by total number of units ordered?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique skus changed over time?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total forecast recordss?

### CompliFlow Systems - Regulation & Compliance 📋  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top regulation id by total fine/penalty amount usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest compliance score?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in violation count?

### FreshGuard Foods - Quality Event Root Cause Analysis 🔍  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product id by total units affected?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique products changed over time?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in critical events count?

### GridGuard Utilities - Transformer Asset Health ⚡  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top transformer asset identifier by total top oil temperature in celsius?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total failure events count?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in critical alert count?

### HeatTrack Refining - Energy Use Monitoring & Heat Optimization 🌡️  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top heat exchanger identifier by total energy consumption in mmbtu?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in highest clean ua btu hr f?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in highest energy consumption mmbtu?

### LedgerView Industrial - Financial Analytics 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What is the average variance percentage by cost center type?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top cost center identifier by total transaction amount in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in total monthly revenue?

### LoadCast Energy - Demand Forecasting & Capacity Planning 📈  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top service territory identifier by total daily peak demand in mw?
- **BAD** (EMPTY_RESULT)
  - Q: How has unique territorys changed over time?
- **BAD** (EMPTY_RESULT)
  - Q: What is the monthly trend in unique readings?

### MidSpend Analytics - Spend Intelligence 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top supplier id by total transaction amount usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest quality score?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in unique total transactionss?

### MineOps Central - Production Monitoring Control Center 📊  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top unit id by total throughput tons per hour?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in bottleneck count?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total units changed over time?

### PetroPulse Integrated - Production Monitoring Control Center 📊  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top well identifier by total daily oil production in barrels?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique total eventss?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest oil bbl?

### PipeRoute Midstream - Logistics Optimization 🚚  —  4/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top pipeline segment id by total throughput in bpd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total eventss?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total readingss?

### PlanWorks Manufacturing - Resource Planning 🏭  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top work center identifier by total planned production quantity?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique work centers changed over time?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total work orderss?

### PowerGrid Analytics - Grid Management & Energy Mix ⚡  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top grid zone identifier by total curtailed generation in mw (renewable only)?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest peak demand mw?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique readings?

### QualityRefine Analytics - Quality Event Root Cause Analysis 🔍  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top process unit identifier by total off-spec product volume in barrels?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total batchess?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total eventss?

### RefineCapital Systems - Working Capital & Cash Flow Optimization 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top business unit id by total cash flow amount usd (positive=inflow)?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest accounts receivable?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total inflows usd count?

### RefineGuard Systems - Predictive Maintenance & Asset Health 🔧  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top refinery equipment identifier by total raw sensor measurement value?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total eventss?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: Which reading timestamps have the most unique total readingss?

### SemiLedger - Financial Analytics & Reporting 💰  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top cost center identifier by total transaction amount in usd (positive = credit/revenue, negative = debit/expense)?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique cost centers changed over time?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in critical overrun count?

### TradeFlow Energy - Energy Trading Analytics ⚡  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top contract id by total volume in bbl equivalent?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in highest net position bbl?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total tradess?

### WellGuard Upstream - Predictive Maintenance & Asset Health 🔧  —  4/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top equipment id by total sensor value?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total eventss?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in alarm trip count?

### AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top design configuration identifier by total total drag coefficient cd?
- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique configs changed over time?

### BuildBid Engineering - Bid Creation & Cost Estimation 📝  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top project id by total estimated project cost usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in total bids submitted?

### CapVenture Energy - Capital Investment Simulation 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top project identifier by total transaction amount in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total transactionss?

### ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How many records are there per month being forecasted?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top chemical product identifier by total order quantity in kilograms?

### DistroCapital Finance - Working Capital & Cash Flow 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top business unit identifier by total cash inflow in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique transactions?

### DriveWell - Vehicle Health & Maintenance Analytics 🚗  —  5/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top unique vehicle identifier by total engine coolant temperature in celsius?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in critical alert count?

### FabSight - Virtual Metrology & Defect Detection 🔬  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top process recipe identifier by total film thickness measurement in nanometers?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in out of spec count?

### FactoryPulse Systems - Production Monitoring 📊  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top production line identifier by total planned production quantity?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique lines?

### FieldForce Machinery - Field Service Assistant 🛠️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top equipment model at customer site by total time to resolution in hours?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in first time fix count?

### FleetEdge Solutions - Fleet Planning & Optimization 🚚  —  5/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top vehicle asset identifier by total total route distance in kilometers?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in on time operation count?

### FoodPlan Analytics - Scenario Planning & Simulation 🎯  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top category id by total simulated revenue usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique categorys changed over time?

### ForecastPro Machinery - Demand Forecasting 📈  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top equipment model ordered by total units ordered?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in unique total orderss?

### FreshStock Solutions - Perishable Inventory Optimization 📦  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product id by total units moved?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique items?

### IronPulse Manufacturing - Asset Health Monitor 🔧  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top industrial asset identifier by total bearing temperature in celsius?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique assets?

### MidCapital Systems - Working Capital & Cash Flow Optimization 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest accounts receivable?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_METRIC_CALCULATION)
  - Q: What is the monthly trend in total inflows usd count?

### MidLedger Analytics - Financial Analytics & Reporting 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top cost center identifier by total transaction amount usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total transactionss?

### MidStream Dynamics - Scenario Planning & Simulation 🎯  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top scenario id by total revenue impact millions usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total runss?

### MineTruck Analytics - Haul Vehicle Asset Health 🔧  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top vehicle id by total loads completed?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique vehicles changed over time?

### NanoVista - Quality Event RCA 🔍  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product identifier by total number of wafers affected by the event?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in critical event count?

### NucleoSafe Systems - Nuclear Safety & Compliance ☢️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top reactor component identifier by total component temperature in celsius?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique components changed over time?

### PetroLedger Corp - Financial Analytics & Reporting 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top cost center identifier by total transaction amount in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total transactionss?

### PrecisionEdge Corp - Machining Defect Detection ⚙️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top cnc machine identifier by total surface roughness ra in micrometers?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_OTHER)
  - Q: What is the monthly trend in defect count?

### PureChem Analytics - Quality Event Root Cause Analysis 🔍  —  5/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top chemical product identifier by total estimated cost of the quality event in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has total quality events per month changed over time?

### RailRoute Logistics - Route Planning & Optimization 🗺️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top rail corridor identifier by total number of trains on corridor?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique corridors?

### RefineLedger Corp - Financial Analytics & Reporting 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top cost center identifier by total transaction amount usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique total transactionss?

### ReservoirSight Analytics - Reservoir Management 🛢️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What are the top reservoir id by total oil bpd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest cumulative oil bbl?

### RestorePower Gen - Outage Response & Restoration 🔌  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top generator unit identifier by total hours of operation in the day?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in forced outage count?

### SiliconPath - Design Space Simulation 🧪  —  5/7 pass

- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How many records are there per month of the optimization result?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top chip design identifier by total target process node in nanometers?

### SiteTrack Construction - Project Completion Monitoring 🏗️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_MISINTERPRETATION_OF_USER_REQUEST)
  - Q: What are the top project id by total work hours logged?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique projects?

### SolarEdge Power - Solar & Storage Optimization ☀️  —  5/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top solar+storage site identifier by total solar irradiance in kwh/m2?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total sites changed over time?

### SpendLens Manufacturing - Spend Intelligence 💰  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top supplier identifier by total purchase order amount in usd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in unique suppliers?

### TraceFood Systems - Product Traceability & Recall 📋  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product id by total units in lot?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique products changed over time?

### TrackGuard Systems - Predictive Maintenance & Asset Health 🔧  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top rolling stock asset id by total bearing temperature celsius?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique assets changed over time?

### TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top unique vehicle identifier by total maximum load capacity in kilograms?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in unique segments?

### VisionTech Electronics - Visual Defect Detection 🔬  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top pcb or component model inspected by total time to complete inspection in seconds?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in total defects found count?

### WaferVault - Salable Inventory Optimization 📦  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product identifier by total transaction quantity in units?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: What is the monthly trend in total units on hand?

### WellFlow Monitoring - Well Production Monitoring 📊  —  5/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top well id by total oil bpd?
- **BAD** (RESULT_MISSING_COLUMNS, LLM_JUDGE_MISSING_OR_INCORRECT_AGGREGATION)
  - Q: What is the monthly trend in highest cumulative oil bbl?

### WindPeak Energy - Wind Farm Optimization 💨  —  5/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top wind turbine identifier by total average wind speed in meters per second?
- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total turbines changed over time?

### AeroParts Supply - Demand Forecasting & Backlog 📈  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top part number identifier by total units ordered?

### AeroQuality Corp - Quality Event Root Cause Analysis 🔍  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top component part number by total cost of quality (rework, scrap, warranty) in usd?

### Apex Motor Group - Recall & Defect Analytics 🚨  —  6/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top vehicle model identifier (fk to dimension) by total number of vehicles affected by the recall?

### AssemblyGuard Systems - Predictive Maintenance 🔧  —  6/7 pass

- **BAD** (RESULT_EXTRA_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top assembly line machine identifier by total operating temperature in celsius?

### ChipArchitect Labs - SoC Design Space Simulation 🧪  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top soc design identifier by total simulated clock frequency in ghz?

### DeepHorizon Energy - Predictive Maintenance & Asset Health 🔧  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top equipment asset identifier by total raw sensor measurement value?

### DistroForecast Systems - Demand Forecasting & Backlog 📈  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product sku code by total units ordered?

### FreightSight Analytics - Freight Demand Forecasting 📈  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top freight lane identifier by total number of carloads?

### HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top turbine unit identifier by total water flow rate in cubic meters per second?

### LabAuto Sciences - Autonomous Lab Experiments & Optimization 🧪  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_FORMATTING_ERROR)
  - Q: What are the top target formulation identifier by total reaction temperature in celsius?

### PartsVault Industrial - Spare Parts Optimization 📦  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top spare part number by total transaction quantity?

### PowerLedger Corp - Financial Analytics & Reporting 💰  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top cost center identifier by total transaction amount in usd?

### PowerMix Dynamics - Grid Management & Energy Mix ⚡  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE)
  - Q: How has unique total plants changed over time?

### QualityFirst Manufacturing - Quality RCA 🔍  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product line identifier by total number of units affected?

### SafeDesign - Safety Simulation Analytics 🧪  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top vehicle configuration identifier by total impact speed in km/h?

### StockSmart Distribution - Inventory Optimization 📦  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top warehouse-product combo identifier by total units moved (positive=receipt, negative=issue)?

### StratOil Dynamics - Scenario Planning & Business Simulation 🎯  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top scenario identifier by total assumed wti oil price usd per barrel?

### TraceCore Materials - Product & Process Traceability 📋  —  6/7 pass

- **BAD** (RESULT_MISSING_ROWS, LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT)
  - Q: What are the top product identifier by total input material quantity in kg?
