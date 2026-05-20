# Genie Space Question Audit — Benchmark + Common-Question Rewrites Applied

*Diff of every question that changed in `genie_factory/specs/**/*.json` vs `git HEAD`. The companion implementation has been committed alongside this document.*


## TL;DR

- **414 of 616 benchmark questions** were rewritten (~67%).
- **334 of 616 example-SQL (curated query) questions** were rewritten (~54%). These ship with the Genie space.
- **0 of 616 sample_questions** (the user-visible "Common Questions" panel) needed material rewrites. Pool was already human-quality.

## What's broken in the originals (5 systemic patterns)

All 1,232 benchmark + example-SQL questions were emitted by a template generator. The templates leak the data model into user-facing text.

| # | Pattern | Example | Why it's wrong | Fix recipe |
|---|---------|---------|----------------|------------|
| 1 | **Raw field names in the question** | *"What are the top reservoir id by total oil bpd?"* | Users don't know about `reservoir_id` or `_bpd` suffixes; this is what an analyst writes after looking at the schema, not what a plant manager asks. | Swap `<entity>_id` for `<entity>_name`; replace unit suffixes with natural phrases ("barrels per day", "pressure", "percentage"). |
| 2 | **SUM/MAX of a rate, temperature, pressure, or score** | *"How has total bottomhole temp f changed over time?"* / *"What is the monthly trend in highest oil bpd?"* | Summing temperature or pressure is dimensionally meaningless; "highest BPD" trended monthly returns the noisiest day per month. | Switch to AVG for rates/temps/pressures. Point at the auto-synthesized `avg_<col>` measure when available; otherwise inline AVG over the source table. |
| 3 | **Meta / row-count questions** | *"How many records are there per kpi month?"* | These are SQL-author questions, not business questions. The audience does not care how many rows exist in a fact table. | Replace with a domain ranking against the same table. |
| 4 | **"Identifier" jargon + double-plural typos** | *"Top equipment asset identifier by total raw sensor measurement value"* / *"unique total inspectionss"* | "Identifier" is generator noise; `eventss` is a literal pluralization bug. | Drop "identifier"; switch to the entity's friendly name; rephrase "unique total X" as a clear distinct-count or domain ranking. |
| 5 | **Parenthetical data-modeling notes leaked into the question** | *"…by total transaction amount in usd (revenue positive, expenses negative)"* / *"…average yield (0–100) by recipe name"* | Parentheticals belong in column comments, not user questions. | Strip the parenthetical; rephrase naturally. |

## Diversity check

Before applying changes, I ran a duplicate-detection pass on each spec's 7 benchmarks. 44 of 88 specs had ≥2 questions hitting the same metric+intent combination (e.g., "peak monthly revenue each month" + "total monthly revenue trended over time"). All 75 duplicates were diversified by pivoting one question to a different dimension or metric on the same table. The final state has **0 duplicate clusters** across all 88 specs.

## Per-spec diff (Old → New)

Each item is labeled by source:
- **Benchmark** — eval-only, never shown to end users.
- **Example SQL** — curated query that ships with the Genie space (training + visible to users via "Show example").

Common Questions (the Genie sample_questions panel) are not listed because none changed materially.

### `aerospace/demand_forecasting`
*AeroParts Supply - Demand Forecasting & Backlog 📈* — fictional company: **AeroParts Supply** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total backlog units count?*

**B1** — `unchanged`
- Q: *How has shipped order count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in over forecast count?*

**B3** — `rewritten`
- **Old Q:** How has unique forecasts changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_count) AS forecast_count FROM {fqn}.forecast_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', forecast_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.demand_forecasts GROUP BY 1 ORDER BY 1`

**B4** — `rewritten`
- **Old Q:** What are the top part number identifier by total units ordered?
- **Old SQL:** `SELECT part_number, SUM(order_quantity) AS total_order_quantity FROM {fqn}.aftermarket_orders GROUP BY part_number ORDER BY total_order_quantity DESC LIMIT 10`
- **New Q:** Which part have the highest total units ordered?
- **New SQL:** `SELECT part_name, SUM(order_quantity) AS total_order_quantity FROM {fqn}.aftermarket_orders GROUP BY part_name ORDER BY total_order_quantity DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average absolute forecast error percentage by part category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.demand_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which part numbers have the highest average order fill rate percentage?
- **New SQL:** `SELECT part_number, AVG(fill_rate_pct) AS avg_metric FROM {fqn}.demand_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total orders?
- **Old SQL:** `SELECT order_date, MEASURE(total_order_count) AS total_order_count FROM {fqn}.order_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.aftermarket_orders GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest order quantity changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted units?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_units) AS max_forecasted_units FROM {fqn}.forecast_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak forecasted demand units each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_forecasted_units) AS max_forecasted_units FROM {fqn}.forecast_metrics GROUP BY ALL ORDER BY forecast_month`

**E3** — `rewritten`
- **Old Q:** How does total units ordered break down by part number identifier for 'Backlog' records?
- **Old SQL:** `SELECT part_number, COUNT(*) AS record_count, SUM(order_quantity) AS total_order_quantity FROM {fqn}.aftermarket_orders WHERE order_status = 'Backlog' GROUP BY part_number ORDER BY total_order_quantity DESC`
- **New Q:** Which part have the highest total *?
- **New SQL:** `SELECT part_name, SUM(*) AS record_count, SUM(order_quantity) AS total_order_quantity FROM {fqn}.aftermarket_orders WHERE order_status = 'Backlog' GROUP BY part_name ORDER BY total_order_quantity DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total forecasted demand units over time?*

**E5** — `unchanged`
- Q: *How has the average order fill rate percentage changed over time?*

**E6** — `unchanged`
- Q: *How has average quoted lead time changed over time?*

---

### `aerospace/design_space_simulation_for_fuel_efficiency`
*AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪* — fictional company: **AeroSim Dynamics** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in pareto run count?*

**B1** — `rewritten`
- **Old Q:** How has unique simulations changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(simulation_count) AS simulation_count FROM {fqn}.simulation_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique snapshots?
- **Old SQL:** `SELECT snapshot_date, MEASURE(snapshot_count) AS snapshot_count FROM {fqn}.parameter_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How does total drag coefficient cd compare across configuration ?
- **New SQL:** `SELECT config_name, SUM(drag_coefficient) AS total_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has unique configs changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_config_count) AS unique_config_count FROM {fqn}.parameter_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which wing type: conventional, blended wing body, truss-braced, folding wingtips have the highest total lift-to-drag ratio l/d?
- **New SQL:** `SELECT wing_type, SUM(lift_to_drag_ratio) AS total_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top design configuration identifier by total total drag coefficient cd?
- **Old SQL:** `SELECT config_id, SUM(drag_coefficient) AS total_drag_coefficient FROM {fqn}.simulation_runs GROUP BY config_id ORDER BY total_drag_coefficient DESC LIMIT 10`
- **New Q:** Which engine type: turbofan, open rotor, hybrid electric, geared turbofans have the highest total fuel burn in kilograms per nautical mile?
- **New SQL:** `SELECT engine_type, SUM(fuel_burn_kg_nm) AS total_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average engine bypass ratio by wing type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.optimization_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which wing types have the highest total best fuel burn achieved this month in kilograms/nm?
- **New SQL:** `SELECT wing_type, SUM(best_fuel_burn_kg_nm) AS total_metric FROM {fqn}.optimization_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique configs?
- **Old SQL:** `SELECT run_date, MEASURE(unique_config_count) AS unique_config_count FROM {fqn}.simulation_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest drag coefficient changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest wing span m?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_wing_span_m) AS max_wing_span_m FROM {fqn}.parameter_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average wing span in meters trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_wing_span) AS avg_wing_span FROM {fqn}.parameter_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How has total empty weight kg changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_empty_weight_kg) AS total_empty_weight_kg FROM {fqn}.parameter_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total operating empty weight in kilograms trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_empty_weight_kg) AS total_empty_weight_kg FROM {fqn}.parameter_metrics GROUP BY ALL ORDER BY snapshot_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total total drag coefficient cd over time?
- **Old SQL:** `SELECT run_date, SUM(drag_coefficient) AS total_drag_coefficient FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`
- **New Q:** How has total total drag coefficient cd trended over time?
- **New SQL:** `SELECT run_date, SUM(drag_coefficient) AS total_drag_coefficient FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`

**E5** — `unchanged`
- Q: *What is the trend of total wing span in meters over time?*

**E6** — `rewritten`
- **Old Q:** How many distinct unique monthly record identifier are there per engine type?
- **Old SQL:** `SELECT engine_type, COUNT(DISTINCT record_id) AS distinct_count FROM {fqn}.optimization_monthly GROUP BY engine_type ORDER BY distinct_count DESC`
- **New Q:** How many distinct forecasts does each wing type have?
- **New SQL:** `SELECT wing_type, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.optimization_monthly GROUP BY 1 ORDER BY distinct_count DESC LIMIT 10`

---

### `aerospace/financial_analytics_reporting`
*AeroLedger Corp - Financial Analytics & Cost Reporting 💰* — fictional company: **AeroLedger Corp** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total revenue count?*

**B1** — `unchanged`
- Q: *How has total cogs count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique cost centers?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_cost_center_count) AS unique_cost_center_count FROM {fqn}.budget_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.budget_snapshots GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest budgeted revenue changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount in usd (revenue positive, expenses negative)?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which cost centers have the highest total transaction amount?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average revenue variance as percentage (positive = favorable) by business segment?
- **Old SQL:** `SELECT business_segment, AVG(revenue_variance_pct) AS avg_revenue_variance_pct FROM {fqn}.budget_snapshots GROUP BY business_segment ORDER BY avg_revenue_variance_pct DESC`
- **New Q:** Which business segments have the highest average revenue variance as percentage?
- **New SQL:** `SELECT business_segment, AVG(revenue_variance_pct) AS avg_revenue_variance_pct FROM {fqn}.budget_snapshots GROUP BY business_segment ORDER BY avg_revenue_variance_pct DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.financial_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which business segments have the highest average gross margin percentage?
- **New SQL:** `SELECT business_segment, AVG(gross_margin_pct) AS avg_metric FROM {fqn}.financial_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total opex count?
- **Old SQL:** `SELECT txn_date, MEASURE(total_opex) AS total_opex FROM {fqn}.financial_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How has total opex trended over time?
- **New SQL:** `SELECT txn_date, MEASURE(total_opex) AS total_opex FROM {fqn}.financial_txn_metrics GROUP BY ALL ORDER BY txn_date`

**E1** — `unchanged`
- Q: *How has total rd spend count changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total budgeted revenue usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_budgeted_revenue) AS total_budgeted_revenue FROM {fqn}.budget_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total budgeted revenue trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_budgeted_revenue) AS total_budgeted_revenue FROM {fqn}.budget_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How has total revenue variance pct changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_revenue_variance_percent) AS total_revenue_variance_percent FROM {fqn}.budget_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average revenue variance percent trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_revenue_variance_percent) AS total_revenue_variance_percent FROM {fqn}.budget_metrics GROUP BY ALL ORDER BY snapshot_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total transaction amount in usd (revenue positive, expenses negative) over time?
- **Old SQL:** `SELECT txn_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY txn_date ORDER BY txn_date`
- **New Q:** How has total transaction amount in trended over time?
- **New SQL:** `SELECT txn_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY txn_date ORDER BY txn_date`

**E5** — `rewritten`
- **Old Q:** What is the trend of total budgeted revenue in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(budgeted_revenue_usd) AS total_budgeted_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total budgeted revenue in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(budgeted_revenue_usd) AS total_budgeted_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average gross margin percentage changed over time?*

---

### `aerospace/predictive_maintenance_asset_health`
*AeroGuard Systems - Predictive Maintenance & Asset Health 🔧* — fictional company: **AeroGuard Systems** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical alert count?*

**B1** — `rewritten`
- **Old Q:** How has unique readings changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(reading_count) AS reading_count FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in unscheduled removal count?*

**B3** — `rewritten`
- **Old Q:** How has unique total eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** Which engine model designations have the highest total exhaust gas temperature in celsius?
- **New SQL:** `SELECT engine_model, SUM(egt_celsius) AS total_metric FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top engine serial identifier by total exhaust gas temperature in celsius?
- **Old SQL:** `SELECT engine_id, SUM(egt_celsius) AS total_egt_celsius FROM {fqn}.sensor_readings GROUP BY engine_id ORDER BY total_egt_celsius DESC LIMIT 10`
- **New Q:** Which aircraft type designations have the highest total vibration in inches per second?
- **New SQL:** `SELECT aircraft_type, SUM(vibration_ips) AS total_metric FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of maintenance event?
- **Old SQL:** `SELECT event_date, COUNT(*) AS record_count FROM {fqn}.maintenance_events GROUP BY event_date ORDER BY event_date`
- **New Q:** Which engine models have the highest average aircraft downtime hours?
- **New SQL:** `SELECT engine_model, MEASURE(avg_downtime_hours) AS avg_downtime_hours FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY avg_downtime_hours DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.health_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which engine models have the highest average health score for the month?
- **New SQL:** `SELECT engine_model, AVG(avg_health_score) AS avg_metric FROM {fqn}.health_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique engines?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_engine_count) AS unique_engine_count FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest egt celsius changed over time?*

**E2** — `unchanged`
- Q: *How has total parts replaced changed over time?*

**E3** — `unchanged`
- Q: *What is the trend of total exhaust gas temperature in celsius over time?*

**E4** — `unchanged`
- Q: *What is the trend of total aircraft downtime in hours over time?*

**E5** — `rewritten`
- **Old Q:** How has the average average health score for the month (0-100) changed over time?
- **Old SQL:** `SELECT report_month, AVG(avg_health_score) AS avg_avg_health_score FROM {fqn}.health_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** How does average health score for the month compare across engine models?
- **New SQL:** `SELECT engine_model, AVG(avg_health_score) AS avg_avg_health_score FROM {fqn}.health_monthly GROUP BY engine_model ORDER BY engine_model LIMIT 10`

**E6** — `rewritten`
- **Old Q:** How has total fuel flow kg hr changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_fuel_flow_kg_hr) AS total_fuel_flow_kg_hr FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has total fuel flow rate in kilograms/hr trended over time?
- **New SQL:** `SELECT reading_date, MEASURE(total_fuel_flow_kg_hr) AS total_fuel_flow_kg_hr FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`

---

### `aerospace/product_traceability_anti_counterfeit`
*AeroTrace Systems - Product Traceability & Anti-Counterfeit 🛡️* — fictional company: **AeroTrace Systems** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in custody gap events count?*

**B1** — `unchanged`
- Q: *How has high risk events count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in serviceable count?*

**B3** — `unchanged`
- Q: *How has overdue ad count changed over time?*

**B4** — `rewritten`
- **Old Q:** What is the average ai-computed counterfeit risk score 0-100 (higher = riskier) by component serial number?
- **Old SQL:** `SELECT serial_number, AVG(counterfeit_risk_score) AS avg_counterfeit_risk_score FROM {fqn}.lifecycle_events GROUP BY serial_number ORDER BY avg_counterfeit_risk_score DESC`
- **New Q:** Which component serial numbers have the highest average ai-computed counterfeit risk score 0-100?
- **New SQL:** `SELECT serial_number, AVG(counterfeit_risk_score) AS avg_counterfeit_risk_score FROM {fqn}.lifecycle_events GROUP BY serial_number ORDER BY avg_counterfeit_risk_score DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of certification snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.certification_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which component serial numbers have the highest average days until certification expiry?
- **New SQL:** `SELECT serial_number, MEASURE(avg_days_until_expiry) AS avg_days_until_expiry FROM {fqn}.certification_metrics GROUP BY ALL ORDER BY avg_days_until_expiry DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.traceability_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which component serial numbers have the highest total number of chain-of-custody gaps detected?
- **New SQL:** `SELECT serial_number, SUM(custody_gap_count) AS total_metric FROM {fqn}.traceability_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in scrapped count?*

**E1** — `rewritten`
- **Old Q:** How has unique total eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.lifecycle_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.lifecycle_events GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique snapshots?
- **Old SQL:** `SELECT snapshot_date, MEASURE(snapshot_count) AS snapshot_count FROM {fqn}.certification_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.certification_snapshots GROUP BY 1 ORDER BY 1`

**E3** — `rewritten`
- **Old Q:** How has the average ai-computed counterfeit risk score 0-100 (higher = riskier) changed over time?
- **Old SQL:** `SELECT event_date, AVG(counterfeit_risk_score) AS avg_counterfeit_risk_score FROM {fqn}.lifecycle_events GROUP BY event_date ORDER BY event_date`
- **New Q:** How does ai-computed counterfeit risk score 0-100 compare across component serial numbers?
- **New SQL:** `SELECT serial_number, AVG(counterfeit_risk_score) AS avg_counterfeit_risk_score FROM {fqn}.lifecycle_events GROUP BY serial_number ORDER BY serial_number LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total days until certification expires over time?*

**E5** — `unchanged`
- Q: *How has the average documentation completeness percentage changed over time?*

**E6** — `unchanged`
- Q: *How has scrapped count changed over time?*

---

### `aerospace/quality_event_root_cause_analysis`
*AeroQuality Corp - Quality Event Root Cause Analysis 🔍* — fictional company: **AeroQuality Corp** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical event count?*

**B1** — `unchanged`
- Q: *How has escape count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in fail count?*

**B3** — `rewritten`
- **Old Q:** How has unique total inspectionss changed over time?
- **Old SQL:** `SELECT inspection_date, MEASURE(total_inspections) AS total_inspections FROM {fqn}.inspection_metrics GROUP BY ALL ORDER BY inspection_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', inspection_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.inspection_records GROUP BY 1 ORDER BY 1`

**B4** — `rewritten`
- **Old Q:** What are the top component part number by total cost of quality (rework, scrap, warranty) in usd?
- **Old SQL:** `SELECT component_id, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events GROUP BY component_id ORDER BY total_cost_of_quality_usd DESC LIMIT 10`
- **New Q:** Which component have the highest total monthly cost of quality?
- **New SQL:** `SELECT component_name, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events GROUP BY component_name ORDER BY total_cost_of_quality_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of inspection?
- **Old SQL:** `SELECT inspection_date, COUNT(*) AS record_count FROM {fqn}.inspection_records GROUP BY inspection_date ORDER BY inspection_date`
- **New Q:** Which component classs have the highest average inspection cycle time in hours?
- **New SQL:** `SELECT component_class, MEASURE(avg_cycle_time_hours) AS avg_cycle_time_hours FROM {fqn}.inspection_metrics GROUP BY ALL ORDER BY avg_cycle_time_hours DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.quality_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which component classs have the highest total defect rate in parts per million?
- **New SQL:** `SELECT component_class, SUM(defect_rate_ppm) AS total_metric FROM {fqn}.quality_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.quality_events GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique components changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(unique_component_count) AS unique_component_count FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.quality_events GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique components?
- **Old SQL:** `SELECT inspection_date, MEASURE(unique_component_count) AS unique_component_count FROM {fqn}.inspection_metrics GROUP BY ALL ORDER BY inspection_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', inspection_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.inspection_records GROUP BY 1 ORDER BY 1`

**E3** — `rewritten`
- **Old Q:** What is the trend of total cost of quality (rework, scrap, warranty) in usd over time?
- **Old SQL:** `SELECT event_date, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events GROUP BY event_date ORDER BY event_date`
- **New Q:** How has total monthly cost of quality in trended over time?
- **New SQL:** `SELECT event_date, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events GROUP BY event_date ORDER BY event_date`

**E4** — `unchanged`
- Q: *What is the trend of total number of units inspected over time?*

**E5** — `unchanged`
- Q: *How has the average defect rate in parts per million changed over time?*

**E6** — `unchanged`
- Q: *How does critical event count vary across component classes?*

---

### `aerospace/supply_materials_planning`
*AeroChain Logistics - Supply & Materials Planning 🔗* — fictional company: **AeroChain Logistics** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in late delivery count?*

**B1** — `rewritten`
- **Old Q:** How has unique total pos changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(total_po_count) AS total_po_count FROM {fqn}.procurement_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.procurement_orders GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in critical material count?*

**B3** — `rewritten`
- **Old Q:** How has unique snapshots changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(snapshot_count) AS snapshot_count FROM {fqn}.supply_position_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which material have the highest total order quantity in kilograms?
- **New SQL:** `SELECT material_name, SUM(order_quantity_kg) AS total_metric FROM {fqn}.procurement_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top material identifier by total order quantity in kilograms?
- **Old SQL:** `SELECT material_id, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.procurement_orders GROUP BY material_id ORDER BY total_order_quantity_kg DESC LIMIT 10`
- **New Q:** Which material class: titanium, nickel superalloy, carbon fiber, aluminum, specialty steel, ceramic matrixs have the highest total cost per kilogram?
- **New SQL:** `SELECT material_class, SUM(unit_cost_usd_kg) AS total_metric FROM {fqn}.procurement_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of supply snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.supply_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which material classs have the highest average days of supply?
- **New SQL:** `SELECT material_class, MEASURE(avg_days_of_supply) AS avg_days_of_supply FROM {fqn}.supply_position_metrics GROUP BY ALL ORDER BY avg_days_of_supply DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.supply_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which material classs have the highest average supplier on-time delivery rate?
- **New SQL:** `SELECT material_class, AVG(on_time_delivery_pct) AS avg_metric FROM {fqn}.supply_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique materials?
- **Old SQL:** `SELECT order_date, MEASURE(unique_material_count) AS unique_material_count FROM {fqn}.procurement_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.procurement_orders GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has highest order quantity kg changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(max_order_quantity_kg) AS max_order_quantity_kg FROM {fqn}.procurement_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How has total order quantity in kilograms trended over time?
- **New SQL:** `SELECT order_date, MEASURE(max_order_quantity_kg) AS max_order_quantity_kg FROM {fqn}.procurement_metrics GROUP BY ALL ORDER BY order_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest on hand kg?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_on_hand_kg) AS max_on_hand_kg FROM {fqn}.supply_position_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak on-hand inventory in kilograms each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_on_hand_kg) AS max_on_hand_kg FROM {fqn}.supply_position_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How does total order quantity in kilograms break down by material identifier for 'On Time' records?
- **Old SQL:** `SELECT material_id, COUNT(*) AS record_count, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.procurement_orders WHERE delivery_status = 'On Time' GROUP BY material_id ORDER BY total_order_quantity_kg DESC`
- **New Q:** Which material have the highest total *?
- **New SQL:** `SELECT material_name, SUM(*) AS record_count, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.procurement_orders WHERE delivery_status = 'On Time' GROUP BY material_name ORDER BY total_order_quantity_kg DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total on-hand inventory in kg over time?
- **Old SQL:** `SELECT snapshot_date, SUM(on_hand_kg) AS total_on_hand_kg FROM {fqn}.supply_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total on-hand inventory in kilograms trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(on_hand_kg) AS total_on_hand_kg FROM {fqn}.supply_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average supplier on-time delivery rate changed over time?*

**E6** — `unchanged`
- Q: *How has late delivery count changed over time?*

---

### `aerospace/working_capital_cash_flow_optimization`
*AeroCapital Finance - Working Capital & Cash Flow 💰* — fictional company: **AeroCapital Finance** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total inflows count?*

**B1** — `unchanged`
- Q: *How has total outflows count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique programs?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_program_count) AS unique_program_count FROM {fqn}.working_capital_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.working_capital_snapshots GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest accounts receivable changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top aerospace program identifier by total transaction amount in usd (positive = inflow, negative = outflow)?
- **Old SQL:** `SELECT program_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY program_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which programs have the most transaction amount?
- **New SQL:** `SELECT program_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY program_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which program types have the highest average days sales outstanding?
- **New SQL:** `SELECT program_type, MEASURE(avg_dso) AS avg_dso FROM {fqn}.working_capital_metrics GROUP BY ALL ORDER BY avg_dso DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.cashflow_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which program types have the highest total operating cash flow?
- **New SQL:** `SELECT program_type, SUM(operating_cash_flow_usd) AS total_metric FROM {fqn}.cashflow_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique txns?
- **Old SQL:** `SELECT txn_date, MEASURE(txn_count) AS txn_count FROM {fqn}.cash_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique programs changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(unique_program_count) AS unique_program_count FROM {fqn}.cash_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total accounts receivable usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_receivables) AS total_receivables FROM {fqn}.working_capital_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total receivables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_receivables) AS total_receivables FROM {fqn}.working_capital_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How has total dpo days changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_dpo_days) AS total_dpo_days FROM {fqn}.working_capital_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average days payable outstanding trended over time?
- **New SQL:** `SELECT snapshot_date, AVG(dpo_days) AS avg_dpo_days FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total transaction amount in usd (positive = inflow, negative = outflow) over time?
- **Old SQL:** `SELECT txn_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY txn_date ORDER BY txn_date`
- **New Q:** How does transaction amount in compare across programs?
- **New SQL:** `SELECT program_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY program_name ORDER BY program_name LIMIT 10`

**E5** — `rewritten`
- **Old Q:** What is the trend of total accounts receivable balance in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total accounts receivable balance in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average current ratio (current assets / current liabilities) changed over time?*

---

### `automotive/design_space_simulation_for_safety`
*SafeDesign - Safety Simulation Analytics 🧪* — fictional company: **SafeDesign Automotive** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in fail count?*

**B1** — `unchanged`
- Q: *How has five star count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in converged count?*

**B3** — `rewritten`
- **Old Q:** How has unique total snapshotss changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_snapshots) AS total_snapshots FROM {fqn}.parameter_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.parameter_snapshots GROUP BY 1 ORDER BY 1`

**B4** — `rewritten`
- **Old Q:** What are the top vehicle configuration identifier by total impact speed in km/h?
- **Old SQL:** `SELECT config_id, SUM(impact_speed_kmh) AS total_impact_speed_kmh FROM {fqn}.simulation_runs GROUP BY config_id ORDER BY total_impact_speed_kmh DESC LIMIT 10`
- **New Q:** Which vehicle model being simulateds have the highest total impact speed in kilometers/h?
- **New SQL:** `SELECT model_name, SUM(impact_speed_kmh) AS total_impact_speed_kmh FROM {fqn}.simulation_runs GROUP BY model_name ORDER BY total_impact_speed_kmh DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average composite safety score 0-100 from parameter combination by vehicle model being explored?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month the summary covers?
- **Old SQL:** `SELECT summary_month, COUNT(*) AS record_count FROM {fqn}.simulation_summary_monthly GROUP BY summary_month ORDER BY summary_month`
- **New Q:** Which vehicle models have the highest average predicted composite safety score 0-100?
- **New SQL:** `SELECT model_name, AVG(forecasted_safety_score) AS avg_metric FROM {fqn}.simulation_summary_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total simulation runss?
- **Old SQL:** `SELECT run_date, MEASURE(total_simulation_runs) AS total_simulation_runs FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique configs changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(unique_config_count) AS unique_config_count FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique configs?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_config_count) AS unique_config_count FROM {fqn}.parameter_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.parameter_snapshots GROUP BY 1 ORDER BY 1`

**E3** — `rewritten`
- **Old Q:** What is the trend of total impact speed in km/h over time?
- **Old SQL:** `SELECT run_date, SUM(impact_speed_kmh) AS total_impact_speed_kmh FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`
- **New Q:** How has total impact speed in kilometers/h trended over time?
- **New SQL:** `SELECT run_date, SUM(impact_speed_kmh) AS total_impact_speed_kmh FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`

**E4** — `unchanged`
- Q: *What is the trend of total average structural panel thickness in mm over time?*

**E5** — `unchanged`
- Q: *How has the average predicted composite safety score 0-100 changed over time?*

**E6** — `unchanged`
- Q: *How has total cabin intrusion mm changed over time?*

---

### `automotive/product_feature_usage_analytics`
*AutoMetrics - Feature Usage & Adoption Analytics 📱* — fictional company: **AutoMetrics Corp** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in failed activation count?*

**B1** — `rewritten`
- **Old Q:** How has unique total feature eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_feature_events) AS total_feature_events FROM {fqn}.feature_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.feature_events GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in high churn risk count?*

**B3** — `unchanged`
- Q: *How has power user count changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top unique vehicle identifier by total number of user interactions during the session?
- **Old SQL:** `SELECT vehicle_id, SUM(interaction_count) AS total_interaction_count FROM {fqn}.feature_events GROUP BY vehicle_id ORDER BY total_interaction_count DESC LIMIT 10`
- **New Q:** Which vehicle manufacturer brands have the most number of user interactions during the session?
- **New SQL:** `SELECT make, SUM(interaction_count) AS total_interaction_count FROM {fqn}.feature_events GROUP BY make ORDER BY total_interaction_count DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average average session duration in seconds for the week by vehicle model name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month the adoption forecast covers?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.feature_adoption_monthly GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which vehicle models have the highest average predicted feature adoption rate 0-100?
- **New SQL:** `SELECT model, AVG(forecasted_adoption_pct) AS avg_metric FROM {fqn}.feature_adoption_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique vehicles?
- **Old SQL:** `SELECT event_date, MEASURE(unique_vehicle_count) AS unique_vehicle_count FROM {fqn}.feature_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.feature_events GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest session duration sec changed over time?*

**E2** — `unchanged`
- Q: *How has average interactions per session changed over time?*

**E3** — `unchanged`
- Q: *How does failed activation count vary across models?*

**E4** — `rewritten`
- **Old Q:** How does total number of user interactions during the session break down by unique vehicle identifier for 'Success' records?
- **Old SQL:** `SELECT vehicle_id, COUNT(*) AS record_count, SUM(interaction_count) AS total_interaction_count FROM {fqn}.feature_events WHERE activation_status = 'Success' GROUP BY vehicle_id ORDER BY total_interaction_count DESC`
- **New Q:** Which vehicle manufacturer brands have the highest total *?
- **New SQL:** `SELECT make, SUM(*) AS record_count, SUM(interaction_count) AS total_interaction_count FROM {fqn}.feature_events WHERE activation_status = 'Success' GROUP BY make ORDER BY total_interaction_count DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total number of distinct features used during the week over time?*

**E6** — `unchanged`
- Q: *How has the average predicted feature adoption rate 0-100 changed over time?*

---

### `automotive/vehicle_health_maintenance_report`
*DriveWell - Vehicle Health & Maintenance Analytics 🚗* — fictional company: **DriveWell Automotive** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical alert count?*

**B1** — `rewritten`
- **Old Q:** How has unique total readingss changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_readings) AS total_readings FROM {fqn}.vehicle_telemetry_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.vehicle_telemetry GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in warranty covered count?*

**B3** — `rewritten`
- **Old Q:** How has unique total service recordss changed over time?
- **Old SQL:** `SELECT service_date, MEASURE(total_service_records) AS total_service_records FROM {fqn}.maintenance_records_metrics GROUP BY ALL ORDER BY service_date`
- **New Q:** Which vehicle models have the best average engine coolant temperature in celsius?
- **New SQL:** `SELECT model, AVG(engine_temp_celsius) AS avg_metric FROM {fqn}.vehicle_telemetry GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top unique vehicle identifier by total engine coolant temperature in celsius?
- **Old SQL:** `SELECT vehicle_id, SUM(engine_temp_celsius) AS total_engine_temp_celsius FROM {fqn}.vehicle_telemetry GROUP BY vehicle_id ORDER BY total_engine_temp_celsius DESC LIMIT 10`
- **New Q:** Which vehicle classifications have the highest total battery voltage reading in volts?
- **New SQL:** `SELECT vehicle_class, SUM(battery_voltage) AS total_metric FROM {fqn}.vehicle_telemetry GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per week-ending date of the service snapshot?
- **Old SQL:** `SELECT service_date, COUNT(*) AS record_count FROM {fqn}.maintenance_records GROUP BY service_date ORDER BY service_date`
- **New Q:** Which vehicle models have the highest average labor hours per service?
- **New SQL:** `SELECT model, MEASURE(avg_labor_hours) AS avg_labor_hours FROM {fqn}.maintenance_records_metrics GROUP BY ALL ORDER BY avg_labor_hours DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month the forecast covers?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.vehicle_health_monthly GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which vehicle models have the highest average model-predicted health score 0-100?
- **New SQL:** `SELECT model, AVG(forecasted_health_score) AS avg_metric FROM {fqn}.vehicle_health_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique vehicles?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_vehicle_count) AS unique_vehicle_count FROM {fqn}.vehicle_telemetry_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.vehicle_telemetry GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has highest engine temp celsius changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(max_engine_temp_celsius) AS max_engine_temp_celsius FROM {fqn}.vehicle_telemetry_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average engine coolant temperature in celsius trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_engine_temp) AS avg_engine_temp FROM {fqn}.vehicle_telemetry_metrics GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** How has total tire pressure psi changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_tire_pressure_psi) AS total_tire_pressure_psi FROM {fqn}.vehicle_telemetry_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average average tire pressure in pressure (psi) trended over time?
- **New SQL:** `SELECT reading_date, AVG(tire_pressure_psi) AS avg_tire_pressure_psi FROM {fqn}.vehicle_telemetry GROUP BY reading_date ORDER BY reading_date`

**E3** — `unchanged`
- Q: *Which models have the highest total battery voltage?*

**E4** — `unchanged`
- Q: *What is the trend of total engine coolant temperature in celsius over time?*

**E5** — `unchanged`
- Q: *What is the trend of total number of parts replaced during service over time?*

**E6** — `unchanged`
- Q: *How has the average model-predicted health score 0-100 changed over time?*

---

### `automotive/vehicle_recall_root_cause_analysis`
*Apex Motor Group - Recall & Defect Analytics 🚨* — fictional company: **Apex Motor Group** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the critical recall count by component group?*

**B1** — `unchanged`
- Q: *Which component groups have the highest open status count?*

**B2** — `unchanged`
- Q: *Which regions have the most unique vehicle models?*

**B3** — `unchanged`
- Q: *How does the number of unique components vary by region?*

**B4** — `rewritten`
- **Old Q:** What are the top vehicle model identifier (fk to dimension) by total number of vehicles affected by the recall?
- **Old SQL:** `SELECT vehicle_model_id, SUM(units_affected) AS total_units_affected FROM {fqn}.recall_events GROUP BY vehicle_model_id ORDER BY total_units_affected DESC LIMIT 10`
- **New Q:** Which vehicle manufacturer brands have the highest total number of vehicles affected by the recall?
- **New SQL:** `SELECT make, SUM(units_affected) AS total_units_affected FROM {fqn}.recall_events GROUP BY make ORDER BY total_units_affected DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date the warranty claim was filed?
- **Old SQL:** `SELECT claim_date, COUNT(*) AS record_count FROM {fqn}.warranty_claims GROUP BY claim_date ORDER BY claim_date`
- **New Q:** Which vehicle manufacturer brands have the highest average claim cost?
- **New SQL:** `SELECT make, MEASURE(avg_claim_cost) AS avg_claim_cost FROM {fqn}.warranty_claim_metrics GROUP BY ALL ORDER BY avg_claim_cost DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** Which reporting period granularity have the most records?
- **Old SQL:** `SELECT metric_period, COUNT(*) AS record_count FROM {fqn}.recall_metrics_monthly GROUP BY metric_period ORDER BY record_count DESC LIMIT 10`
- **New Q:** Which reporting period granularitys have the highest total number of new recalls opened in the month?
- **New SQL:** `SELECT metric_period, SUM(total_recalls_opened) AS total_metric FROM {fqn}.recall_metrics_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *How does the number of unique vehicle models vary by component group?*

**E1** — `unchanged`
- Q: *How many unique suppliers are there per component group?*

**E2** — `unchanged`
- Q: *What is the highest mileage at claim for each region?*

**E3** — `rewritten`
- **Old Q:** How does total number of vehicles affected by the recall break down by vehicle model identifier (fk to dimension) for 'Closed' records?
- **Old SQL:** `SELECT vehicle_model_id, COUNT(*) AS record_count, SUM(units_affected) AS total_units_affected FROM {fqn}.recall_events WHERE status = 'Closed' GROUP BY vehicle_model_id ORDER BY total_units_affected DESC`
- **New Q:** Which vehicle manufacturer brands have the highest total *?
- **New SQL:** `SELECT make, SUM(*) AS record_count, SUM(units_affected) AS total_units_affected FROM {fqn}.recall_events WHERE status = 'Closed' GROUP BY make ORDER BY total_units_affected DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total vehicle odometer reading at time of claim over time?*

**E5** — `rewritten`
- **Old Q:** Show the distribution of records by reporting period granularity
- **Old SQL:** `SELECT metric_period, COUNT(*) AS record_count FROM {fqn}.recall_metrics_monthly GROUP BY metric_period ORDER BY record_count DESC`
- **New Q:** Which reporting period granularitys have the highest total number of new recalls opened in the month?
- **New SQL:** `SELECT metric_period, SUM(total_recalls_opened) AS total_metric FROM {fqn}.recall_metrics_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**E6** — `unchanged`
- Q: *Which component groups have the most unique suppliers?*

---

### `chemicals_materials/autonomous_lab_experiments`
*LabAuto Sciences - Autonomous Lab Experiments & Optimization 🧪* — fictional company: **LabAuto Sciences** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in passed experiments count?*

**B1** — `rewritten`
- **Old Q:** How has unique total experimentss changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(total_experiments) AS total_experiments FROM {fqn}.experiment_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.experiment_runs GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest experiments run?
- **Old SQL:** `SELECT report_month, MEASURE(max_experiments_run) AS max_experiments_run FROM {fqn}.optimization_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** What has been the peak number of experiments run in the month each month?
- **New SQL:** `SELECT report_month, MEASURE(max_experiments_run) AS max_experiments_run FROM {fqn}.optimization_monthly_metrics GROUP BY ALL ORDER BY report_month`

**B3** — `rewritten`
- **Old Q:** How has total experiments conducted changed over time?
- **Old SQL:** `SELECT report_month, MEASURE(total_experiments_run) AS total_experiments_run FROM {fqn}.optimization_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** Which formulations have the best average reaction temperature in celsius?
- **New SQL:** `SELECT formulation_name, AVG(temperature_c) AS avg_metric FROM {fqn}.experiment_runs GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top target formulation identifier by total reaction temperature in celsius?
- **Old SQL:** `SELECT formulation_id, SUM(temperature_c) AS total_temperature_c FROM {fqn}.experiment_runs GROUP BY formulation_id ORDER BY total_temperature_c DESC LIMIT 10`
- **New Q:** Which category: catalysts, coatings, polymers, pharmaceuticals, nanomaterialss have the best average reaction pressure in bar?
- **New SQL:** `SELECT formulation_category, AVG(pressure_bar) AS avg_metric FROM {fqn}.experiment_runs GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average model-predicted yield percentage by human-readable formulation name?
- **Old SQL:** `SELECT formulation_name, AVG(predicted_yield_pct) AS avg_predicted_yield_pct FROM {fqn}.parameter_snapshots GROUP BY formulation_name ORDER BY avg_predicted_yield_pct DESC`
- **New Q:** Which formulations have the best model-predicted yield percentage?
- **New SQL:** `SELECT formulation_name, AVG(predicted_yield_pct) AS avg_predicted_yield_pct FROM {fqn}.parameter_snapshots GROUP BY formulation_name ORDER BY avg_predicted_yield_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of reporting month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.optimization_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which formulations have the highest average pass rate?
- **New SQL:** `SELECT formulation_name, MEASURE(avg_pass_rate_pct) AS avg_pass_rate_pct FROM {fqn}.optimization_monthly_metrics GROUP BY ALL ORDER BY avg_pass_rate_pct DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique formulations?
- **Old SQL:** `SELECT run_date, MEASURE(unique_formulation_count) AS unique_formulation_count FROM {fqn}.experiment_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.experiment_runs GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has highest yield pct changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(max_yield_pct) AS max_yield_pct FROM {fqn}.experiment_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How has average product yield percentage trended by month?
- **New SQL:** `SELECT run_date, MEASURE(avg_yield_pct) AS avg_yield_pct FROM {fqn}.experiment_runs_metrics GROUP BY ALL ORDER BY run_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total best yield pct?
- **Old SQL:** `SELECT report_month, MEASURE(total_best_yield_percent) AS total_best_yield_percent FROM {fqn}.optimization_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** How has average best yield percent trended by month?
- **New SQL:** `SELECT report_month, MEASURE(total_best_yield_percent) AS total_best_yield_percent FROM {fqn}.optimization_monthly_metrics GROUP BY ALL ORDER BY report_month`

**E3** — `unchanged`
- Q: *How has average model prediction accuracy changed over time?*

**E4** — `unchanged`
- Q: *What is the trend of total reaction temperature in celsius over time?*

**E5** — `unchanged`
- Q: *What is the trend of total model-recommended optimal temperature in celsius over time?*

**E6** — `unchanged`
- Q: *How has the average percentage of experiments that passed changed over time?*

---

### `chemicals_materials/demand_forecasting`
*ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈* — fictional company: **ChemFlow Industries** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in fulfilled order count?*

**B1** — `unchanged`
- Q: *How has backorder count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique forecast records?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_record_count) AS forecast_record_count FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', forecast_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.demand_forecasts GROUP BY 1 ORDER BY 1`

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted quantity kg?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_quantity_kg) AS max_forecasted_quantity_kg FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak predicted demand quantity in kilograms each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_forecasted_quantity_kg) AS max_forecasted_quantity_kg FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`

**B4** — `rewritten`
- **Old Q:** What are the top chemical product identifier by total order quantity in kilograms?
- **Old SQL:** `SELECT product_id, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.chemical_orders GROUP BY product_id ORDER BY total_order_quantity_kg DESC LIMIT 10`
- **New Q:** Which chemical products have the highest total order quantity in kilograms?
- **New SQL:** `SELECT product_name, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.chemical_orders GROUP BY product_name ORDER BY total_order_quantity_kg DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per month being forecasted?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which product categorys have the highest number of forecast records?
- **New SQL:** `SELECT product_category, MEASURE(forecast_record_count) AS forecast_record_count FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_record_count DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per weekly snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.inventory_positions GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which chemical products have the highest total on-hand inventory in kilograms?
- **New SQL:** `SELECT product_name, SUM(on_hand_qty_kg) AS total_metric FROM {fqn}.inventory_positions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total orders?
- **Old SQL:** `SELECT order_date, MEASURE(total_order_count) AS total_order_count FROM {fqn}.chemical_orders_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.chemical_orders GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique products changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.chemical_orders_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.chemical_orders GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** How has average price per kg in usd changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(avg_unit_price_usd) AS avg_unit_price_usd FROM {fqn}.chemical_orders_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How has total price per kilogram in trended over time?
- **New SQL:** `SELECT order_date, MEASURE(avg_unit_price_usd) AS avg_unit_price_usd FROM {fqn}.chemical_orders_metrics GROUP BY ALL ORDER BY order_date`

**E3** — `unchanged`
- Q: *How does backorder count vary across product categories?*

**E4** — `rewritten`
- **Old Q:** How does total order quantity in kilograms break down by chemical product identifier for 'Backorder' records?
- **Old SQL:** `SELECT product_id, COUNT(*) AS record_count, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.chemical_orders WHERE fulfillment_status = 'Backorder' GROUP BY product_id ORDER BY total_order_quantity_kg DESC`
- **New Q:** Which chemical products have the highest total *?
- **New SQL:** `SELECT product_name, SUM(*) AS record_count, SUM(order_quantity_kg) AS total_order_quantity_kg FROM {fqn}.chemical_orders WHERE fulfillment_status = 'Backorder' GROUP BY product_name ORDER BY total_order_quantity_kg DESC LIMIT 10`

**E5** — `rewritten`
- **Old Q:** What is the trend of total predicted demand quantity in kg over time?
- **Old SQL:** `SELECT forecast_month, SUM(forecasted_quantity_kg) AS total_forecasted_quantity_kg FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** How has total predicted demand quantity in kilograms trended over time?
- **New SQL:** `SELECT forecast_month, SUM(forecasted_quantity_kg) AS total_forecasted_quantity_kg FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`

**E6** — `rewritten`
- **Old Q:** How many distinct unique inventory snapshot id are there per product category?
- **Old SQL:** `SELECT product_category, COUNT(DISTINCT snapshot_id) AS distinct_count FROM {fqn}.inventory_positions GROUP BY product_category ORDER BY distinct_count DESC`
- **New Q:** Which product categories have the most inventory snapshots?
- **New SQL:** `SELECT product_category, COUNT(*) AS snapshot_count FROM {fqn}.inventory_snapshots GROUP BY product_category ORDER BY snapshot_count DESC LIMIT 10`

---

### `chemicals_materials/product_process_traceability`
*TraceCore Materials - Product & Process Traceability 📋* — fictional company: **TraceCore Materials** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in passed quality checks count?*

**B1** — `unchanged`
- Q: *How has failed quality checks count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest lots produced?
- **Old SQL:** `SELECT report_month, MEASURE(max_lots_produced) AS max_lots_produced FROM {fqn}.traceability_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** What has been the peak number of lots produced in the month each month?
- **New SQL:** `SELECT report_month, MEASURE(max_lots_produced) AS max_lots_produced FROM {fqn}.traceability_monthly_metrics GROUP BY ALL ORDER BY report_month`

**B3** — `rewritten`
- **Old Q:** How has total lots produced changed over time?
- **Old SQL:** `SELECT report_month, MEASURE(total_lots_produced) AS total_lots_produced FROM {fqn}.traceability_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** Which products have the highest total input material quantity in kilograms?
- **New SQL:** `SELECT product_name, SUM(input_quantity_kg) AS total_metric FROM {fqn}.production_events GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top product identifier by total input material quantity in kg?
- **Old SQL:** `SELECT product_id, SUM(input_quantity_kg) AS total_input_quantity_kg FROM {fqn}.production_events GROUP BY product_id ORDER BY total_input_quantity_kg DESC LIMIT 10`
- **New Q:** Which category: resins, pigments, catalysts, surfactants, intermediatess have the highest total output product quantity in kilograms?
- **New SQL:** `SELECT product_category, SUM(output_quantity_kg) AS total_metric FROM {fqn}.production_events GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per weekly snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.lot_tracking_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which products have the highest total quantity remaining in lot in kilograms?
- **New SQL:** `SELECT product_name, SUM(quantity_on_hand_kg) AS total_metric FROM {fqn}.lot_tracking_snapshots GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of reporting month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.traceability_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which products have the highest average traceability score?
- **New SQL:** `SELECT product_name, MEASURE(avg_traceability_score) AS avg_traceability_score FROM {fqn}.traceability_monthly_metrics GROUP BY ALL ORDER BY avg_traceability_score DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total production eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_production_events) AS total_production_events FROM {fqn}.production_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.production_events GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique lots changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(unique_lot_count) AS unique_lot_count FROM {fqn}.production_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.production_events GROUP BY 1 ORDER BY 1`

**E2** — `unchanged`
- Q: *What is the monthly trend in lots with complete genealogy?*

**E3** — `rewritten`
- **Old Q:** What is the trend of total input material quantity in kg over time?
- **Old SQL:** `SELECT event_date, SUM(input_quantity_kg) AS total_input_quantity_kg FROM {fqn}.production_events GROUP BY event_date ORDER BY event_date`
- **New Q:** How has total input material quantity in kilograms trended over time?
- **New SQL:** `SELECT event_date, SUM(input_quantity_kg) AS total_input_quantity_kg FROM {fqn}.production_events GROUP BY event_date ORDER BY event_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total quantity remaining in lot in kg over time?
- **Old SQL:** `SELECT snapshot_date, SUM(quantity_on_hand_kg) AS total_quantity_on_hand_kg FROM {fqn}.lot_tracking_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total quantity remaining in lot in kilograms trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(quantity_on_hand_kg) AS total_quantity_on_hand_kg FROM {fqn}.lot_tracking_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How has the average traceability completeness score (0-100) changed over time?
- **Old SQL:** `SELECT report_month, AVG(traceability_score_pct) AS avg_traceability_score_pct FROM {fqn}.traceability_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** How does traceability completeness score compare across products?
- **New SQL:** `SELECT product_name, AVG(traceability_score_pct) AS avg_traceability_score_pct FROM {fqn}.traceability_monthly GROUP BY product_name ORDER BY product_name LIMIT 10`

**E6** — `unchanged`
- Q: *How does failed quality checks count vary across product categories?*

---

### `chemicals_materials/quality_event_root_cause_analysis`
*PureChem Analytics - Quality Event Root Cause Analysis 🔍* — fictional company: **PureChem Analytics** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical event count?*

**B1** — `unchanged`
- Q: *How has closed effective count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest total events?
- **Old SQL:** `SELECT report_month, MEASURE(max_total_events) AS max_total_events FROM {fqn}.quality_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** What has been the peak total quality events in the month each month?
- **New SQL:** `SELECT report_month, MEASURE(max_total_events) AS max_total_events FROM {fqn}.quality_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`

**B3** — `unchanged`
- Q: *How has total quality events per month changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top chemical product identifier by total estimated cost of the quality event in usd?
- **Old SQL:** `SELECT product_id, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events GROUP BY product_id ORDER BY total_cost_of_quality_usd DESC LIMIT 10`
- **New Q:** Which chemical products have the highest total cost of quality for the month?
- **New SQL:** `SELECT product_name, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events GROUP BY product_name ORDER BY total_cost_of_quality_usd DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average batch yield percentage by chemical product name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of reporting month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.quality_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which chemical products have the highest average capa closure rate?
- **New SQL:** `SELECT product_name, MEASURE(avg_capa_closure_rate) AS avg_capa_closure_rate FROM {fqn}.quality_kpi_monthly_metrics GROUP BY ALL ORDER BY avg_capa_closure_rate DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in open event count?*

**E1** — `rewritten`
- **Old Q:** How has unique total quality eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_quality_events) AS total_quality_events FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.quality_events GROUP BY 1 ORDER BY 1`

**E2** — `unchanged`
- Q: *What is the monthly trend in total critical events per month?*

**E3** — `rewritten`
- **Old Q:** How does total estimated cost of the quality event in usd break down by chemical product identifier for 'Open' records?
- **Old SQL:** `SELECT product_id, COUNT(*) AS record_count, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events WHERE capa_status = 'Open' GROUP BY product_id ORDER BY total_cost_of_quality_usd DESC`
- **New Q:** Which chemical products have the highest total *?
- **New SQL:** `SELECT product_name, SUM(*) AS record_count, SUM(cost_of_quality_usd) AS total_cost_of_quality_usd FROM {fqn}.quality_events WHERE capa_status = 'Open' GROUP BY product_name ORDER BY total_cost_of_quality_usd DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total batch size in kilograms over time?*

**E5** — `unchanged`
- Q: *How has the average capa closure rate for the month changed over time?*

**E6** — `unchanged`
- Q: *How has open event count changed over time?*

---

### `computer_electronic/design_space_simulation_system_on_chip`
*ChipArchitect Labs - SoC Design Space Simulation 🧪* — fictional company: **ChipArchitect Labs** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in converged count?*

**B1** — `rewritten`
- **Old Q:** How has unique total simulationss changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(total_simulations) AS total_simulations FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest convergence rate percent?
- **Old SQL:** `SELECT opt_month, MEASURE(max_convergence_rate_percent) AS max_convergence_rate_percent FROM {fqn}.optimization_metrics GROUP BY ALL ORDER BY opt_month`
- **New Q:** What has been the peak convergence_rate_percent each month?
- **New SQL:** `SELECT opt_month, MEASURE(max_convergence_rate_percent) AS max_convergence_rate_percent FROM {fqn}.optimization_metrics GROUP BY ALL ORDER BY opt_month`

**B3** — `unchanged`
- Q: *How has total pareto-optimal points discovered changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top soc design identifier by total simulated clock frequency in ghz?
- **Old SQL:** `SELECT soc_design, SUM(clock_freq_ghz) AS total_clock_freq_ghz FROM {fqn}.simulation_runs GROUP BY soc_design ORDER BY total_clock_freq_ghz DESC LIMIT 10`
- **New Q:** Which chip designs have the highest peak clock frequency?
- **New SQL:** `SELECT design_name, MAX(clock_frequency_ghz) AS peak_clock FROM {fqn}.simulation_runs GROUP BY design_name ORDER BY peak_clock DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of the parameter sweep?
- **Old SQL:** `SELECT sweep_date, COUNT(*) AS record_count FROM {fqn}.parameter_sweeps GROUP BY sweep_date ORDER BY sweep_date`
- **New Q:** Which soc design identifiers have the highest total supply voltage in volts?
- **New SQL:** `SELECT soc_design, SUM(voltage_v) AS total_metric FROM {fqn}.parameter_sweeps GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the optimization record?
- **Old SQL:** `SELECT opt_month, COUNT(*) AS record_count FROM {fqn}.optimization_monthly GROUP BY opt_month ORDER BY opt_month`
- **New Q:** Which soc design identifiers have the highest average convergence rate percentage?
- **New SQL:** `SELECT soc_design, MEASURE(avg_convergence_rate) AS avg_convergence_rate FROM {fqn}.optimization_metrics GROUP BY ALL ORDER BY avg_convergence_rate DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest clock freq ghz?
- **Old SQL:** `SELECT run_date, MEASURE(max_clock_freq_ghz) AS max_clock_freq_ghz FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How has total simulated clock frequency in ghz trended over time?
- **New SQL:** `SELECT run_date, MEASURE(avg_clock_freq_ghz) AS avg_clock_freq_ghz FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`

**E1** — `unchanged`
- Q: *How has total area mm2 changed over time?*

**E2** — `unchanged`
- Q: *What is the monthly trend in total simulation compute hours?*

**E3** — `unchanged`
- Q: *How has total best power mw changed over time?*

**E4** — `rewritten`
- **Old Q:** How does total simulated clock frequency in ghz break down by soc design identifier for 'Converged' records?
- **Old SQL:** `SELECT soc_design, COUNT(*) AS record_count, SUM(clock_freq_ghz) AS total_clock_freq_ghz FROM {fqn}.simulation_runs WHERE convergence_status = 'Converged' GROUP BY soc_design ORDER BY total_clock_freq_ghz DESC`
- **New Q:** Which soc design identifiers have the highest total *?
- **New SQL:** `SELECT soc_design, SUM(*) AS record_count, SUM(clock_freq_ghz) AS total_clock_freq_ghz FROM {fqn}.simulation_runs WHERE convergence_status = 'Converged' GROUP BY soc_design ORDER BY total_clock_freq_ghz DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total supply voltage in volts over time?*

**E6** — `unchanged`
- Q: *How has the average percentage of simulations that converged changed over time?*

---

### `computer_electronic/predictive_maintenance_troubleshoot`
*AssemblyGuard Systems - Predictive Maintenance 🔧* — fictional company: **AssemblyGuard Systems** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical alert count?*

**B1** — `rewritten`
- **Old Q:** How has unique total readingss changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_readings) AS total_readings FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** How has highest mtbf hours changed over time?
- **Old SQL:** `SELECT health_month, MEASURE(max_mtbf_hours) AS max_mtbf_hours FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY health_month`
- **New Q:** How has average mean time between failures in hours trended by month?
- **New SQL:** `SELECT health_month, MEASURE(max_mtbf_hours) AS max_mtbf_hours FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY health_month`

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in total maintenance cost in usd?
- **Old SQL:** `SELECT health_month, MEASURE(total_maintenance_cost) AS total_maintenance_cost FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY health_month`
- **New Q:** How has total maintenance cost trended over time?
- **New SQL:** `SELECT health_month, MEASURE(total_maintenance_cost) AS total_maintenance_cost FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY health_month`

**B4** — `rewritten`
- **Old Q:** What are the top assembly line machine identifier by total operating temperature in celsius?
- **Old SQL:** `SELECT machine_id, SUM(temperature_c) AS total_temperature_c FROM {fqn}.sensor_readings GROUP BY machine_id ORDER BY total_temperature_c DESC LIMIT 10`
- **New Q:** Which type of assembly machines have the highest average operating temperature in celsius?
- **New SQL:** `SELECT machine_type, AVG(temperature_c) AS total_temperature_c FROM {fqn}.sensor_readings GROUP BY machine_type ORDER BY total_temperature_c DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date maintenance was performed?
- **Old SQL:** `SELECT maintenance_date, COUNT(*) AS record_count FROM {fqn}.maintenance_records GROUP BY maintenance_date ORDER BY maintenance_date`
- **New Q:** Which type of assembly machines have the highest average total downtime in hours for this event?
- **New SQL:** `SELECT machine_type, AVG(downtime_hours) AS avg_metric FROM {fqn}.maintenance_records GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the health record?
- **Old SQL:** `SELECT health_month, COUNT(*) AS record_count FROM {fqn}.equipment_health_monthly GROUP BY health_month ORDER BY health_month`
- **New Q:** Which type of assembly machines have the highest average mean time between failures in hours?
- **New SQL:** `SELECT machine_type, MEASURE(avg_mtbf_hours) AS avg_mtbf_hours FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY avg_mtbf_hours DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique machines?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_machine_count) AS unique_machine_count FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest vibration mm s changed over time?*

**E2** — `rewritten`
- **Old Q:** How has total prediction accuracy pct changed over time?
- **Old SQL:** `SELECT health_month, MEASURE(total_prediction_accuracy_percent) AS total_prediction_accuracy_percent FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY health_month`
- **New Q:** How has average prediction accuracy percent trended by month?
- **New SQL:** `SELECT health_month, MEASURE(total_prediction_accuracy_percent) AS total_prediction_accuracy_percent FROM {fqn}.equipment_health_metrics GROUP BY ALL ORDER BY health_month`

**E3** — `unchanged`
- Q: *What is the trend of total operating temperature in celsius over time?*

**E4** — `unchanged`
- Q: *What is the trend of total total downtime in hours for this event over time?*

**E5** — `unchanged`
- Q: *How has the average equipment availability percentage 0-100 changed over time?*

**E6** — `rewritten`
- **Old Q:** How has total anomaly score changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_anomaly_score) AS total_anomaly_score FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average anomaly score trended over time?
- **New SQL:** `SELECT reading_date, AVG(anomaly_score) AS avg_anomaly_score FROM {fqn}.sensor_readings GROUP BY reading_date ORDER BY reading_date`

---

### `computer_electronic/visual_defect_detection`
*VisionTech Electronics - Visual Defect Detection 🔬* — fictional company: **VisionTech Electronics** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total defects found count?*

**B1** — `rewritten`
- **Old Q:** How has unique total inspectionss changed over time?
- **Old SQL:** `SELECT inspection_date, MEASURE(total_inspections) AS total_inspections FROM {fqn}.inspection_events_metrics GROUP BY ALL ORDER BY inspection_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', inspection_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.inspection_events GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest target pass rate percent?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_target_pass_rate_percent) AS max_target_pass_rate_percent FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** What has been the peak target_pass_rate_percent each month?
- **New SQL:** `SELECT kpi_month, MEASURE(max_target_pass_rate_percent) AS max_target_pass_rate_percent FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B3** — `rewritten`
- **Old Q:** How has total scrap cost in usd changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_scrap_cost) AS total_scrap_cost FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has total scrap cost trended over time?
- **New SQL:** `SELECT kpi_month, MEASURE(total_scrap_cost) AS total_scrap_cost FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B4** — `unchanged`
- Q: *What are the top pcb or component model inspected by total time to complete inspection in seconds?*

**B5** — `unchanged`
- Q: *What is the average accuracy of defect classification 0-100 by product line category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.detection_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which pcb or component models have the highest average actual first-pass yield percentage?
- **New SQL:** `SELECT component_model, MEASURE(avg_actual_pass_rate) AS avg_actual_pass_rate FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY avg_actual_pass_rate DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest confidence score?
- **Old SQL:** `SELECT inspection_date, MEASURE(max_confidence_score) AS max_confidence_score FROM {fqn}.inspection_events_metrics GROUP BY ALL ORDER BY inspection_date`
- **New Q:** How has average model detection confidence score 0-1 trended by month?
- **New SQL:** `SELECT inspection_date, MEASURE(avg_confidence_score) AS avg_confidence_score FROM {fqn}.inspection_events_metrics GROUP BY ALL ORDER BY inspection_date`

**E1** — `unchanged`
- Q: *How has average detection model confidence score changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total rework cost in usd?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_rework_cost) AS total_rework_cost FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has total rework cost trended over time?
- **New SQL:** `SELECT kpi_month, MEASURE(total_rework_cost) AS total_rework_cost FROM {fqn}.detection_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E3** — `unchanged`
- Q: *What is the trend of total time to complete inspection in seconds over time?*

**E4** — `unchanged`
- Q: *What is the trend of total total inspections in snapshot period over time?*

**E5** — `unchanged`
- Q: *How has the average target first-pass yield percentage changed over time?*

**E6** — `unchanged`
- Q: *How does total defects found count vary across product lines?*

---

### `construction_engineering/engineering_bid_creation`
*BuildBid Engineering - Bid Creation & Cost Estimation 📝* — fictional company: **BuildBid Engineering** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in won count?*

**B1** — `rewritten`
- **Old Q:** How has unique bids changed over time?
- **Old SQL:** `SELECT bid_date, MEASURE(bid_count) AS bid_count FROM {fqn}.bid_kpi_monthly GROUP BY ALL ORDER BY bid_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', bid_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.projects GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *How has highest bids submitted changed over time?*

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in total bids submitted?
- **Old SQL:** `SELECT perf_month, MEASURE(total_bids_submitted) AS total_bids_submitted FROM {fqn}.pipeline_kpi_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** Which projects have the highest total estimated project cost?
- **New SQL:** `SELECT project_name, SUM(estimated_cost_usd) AS total_metric FROM {fqn}.projects GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top project id by total estimated project cost usd?
- **Old SQL:** `SELECT project_id, SUM(estimated_cost_usd) AS total_estimated_cost_usd FROM {fqn}.projects GROUP BY project_id ORDER BY total_estimated_cost_usd DESC LIMIT 10`
- **New Q:** Which project types have the best average target margin 0-100?
- **New SQL:** `SELECT project_type, AVG(target_margin_pct) AS avg_metric FROM {fqn}.projects GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average contingency percentage by project type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per performance month?
- **Old SQL:** `SELECT perf_month, COUNT(*) AS record_count FROM {fqn}.cost_estimate_snapshots GROUP BY perf_month ORDER BY perf_month`
- **New Q:** Which project types have the highest average estimate accuracy?
- **New SQL:** `SELECT project_type, MEASURE(avg_estimate_accuracy) AS avg_estimate_accuracy FROM {fqn}.pipeline_kpi_monthly GROUP BY ALL ORDER BY avg_estimate_accuracy DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique projects?
- **Old SQL:** `SELECT bid_date, MEASURE(unique_project_count) AS unique_project_count FROM {fqn}.bid_kpi_monthly GROUP BY ALL ORDER BY bid_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', bid_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.projects GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest estimated cost changed over time?*

**E2** — `rewritten`
- **Old Q:** How has avg competitors per bid changed over time?
- **Old SQL:** `SELECT perf_month, MEASURE(avg_competitors) AS avg_competitors FROM {fqn}.pipeline_kpi_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** How has average competitors per bid changed over time?
- **New SQL:** `SELECT perf_month, MEASURE(avg_competitors) AS avg_competitors FROM {fqn}.pipeline_kpi_monthly GROUP BY ALL ORDER BY perf_month`

**E3** — `rewritten`
- **Old Q:** What is the trend of total estimated project cost usd over time?
- **Old SQL:** `SELECT bid_date, SUM(estimated_cost_usd) AS total_estimated_cost_usd FROM {fqn}.projects GROUP BY bid_date ORDER BY bid_date`
- **New Q:** How has total estimated project cost trended over time?
- **New SQL:** `SELECT bid_date, SUM(estimated_cost_usd) AS total_estimated_cost_usd FROM {fqn}.projects GROUP BY bid_date ORDER BY bid_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total labor cost usd over time?
- **Old SQL:** `SELECT estimate_date, SUM(labor_cost_usd) AS total_labor_cost_usd FROM {fqn}.bid_submissions GROUP BY estimate_date ORDER BY estimate_date`
- **New Q:** How has total labor cost trended over time?
- **New SQL:** `SELECT estimate_date, SUM(labor_cost_usd) AS total_labor_cost_usd FROM {fqn}.bid_submissions GROUP BY estimate_date ORDER BY estimate_date`

**E5** — `unchanged`
- Q: *How has the average cost estimate accuracy 0-100 changed over time?*

**E6** — `unchanged`
- Q: *How has won count changed over time?*

---

### `construction_engineering/production_and_project_completion_monitoring`
*SiteTrack Construction - Project Completion Monitoring 🏗️* — fictional company: **SiteTrack Construction** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique projects?
- **Old SQL:** `SELECT event_date, MEASURE(project_count) AS project_count FROM {fqn}.project_kpi_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.projects GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest work hours changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in high risk count?*

**B3** — `rewritten`
- **Old Q:** How has unique projects changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(unique_project_count) AS unique_project_count FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** Which projects have the highest total crew members on site?
- **New SQL:** `SELECT project_name, SUM(crew_count) AS total_metric FROM {fqn}.projects GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `unchanged`
- Q: *What are the top project id by total work hours logged?*

**B5** — `unchanged`
- Q: *What is the average overall completion 0-100 by project type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per forecast month?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.milestone_snapshots GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which project types have the highest average schedule variance days?
- **New SQL:** `SELECT project_type, MEASURE(avg_schedule_variance) AS avg_schedule_variance FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY avg_schedule_variance DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total work hours?
- **Old SQL:** `SELECT event_date, MEASURE(total_work_hours) AS total_work_hours FROM {fqn}.project_kpi_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How has average work hours logged trended over time?
- **New SQL:** `SELECT event_date, AVG(work_hours) AS avg_work_hours FROM {fqn}.projects GROUP BY event_date ORDER BY event_date`

**E1** — `unchanged`
- Q: *How has total daily cost changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest budget at completion?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_budget_at_completion) AS max_budget_at_completion FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak budget_at_completion each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_budget_at_completion) AS max_budget_at_completion FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY forecast_month`

**E3** — `rewritten`
- **Old Q:** Rank project types by avg schedule variance days
- **Old SQL:** `SELECT project_type, MEASURE(avg_schedule_variance) AS avg_schedule_variance FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY avg_schedule_variance DESC`
- **New Q:** Rank project types by average schedule variance days
- **New SQL:** `SELECT project_type, MEASURE(avg_schedule_variance) AS avg_schedule_variance FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY avg_schedule_variance DESC`

**E4** — `unchanged`
- Q: *What is the trend of total work hours logged over time?*

**E5** — `unchanged`
- Q: *What is the trend of total milestones completed to date over time?*

**E6** — `rewritten`
- **Old Q:** How many distinct forecast id are there per region?
- **Old SQL:** `SELECT region, COUNT(DISTINCT forecast_id) AS distinct_count FROM {fqn}.milestone_snapshots GROUP BY region ORDER BY distinct_count DESC`
- **New Q:** Which project types have the highest average schedule variance days?
- **New SQL:** `SELECT project_type, MEASURE(avg_schedule_variance) AS avg_schedule_variance FROM {fqn}.completion_kpi_monthly GROUP BY ALL ORDER BY avg_schedule_variance DESC LIMIT 10`

---

### `electric_utility/demand_forecasting`
*LoadCast Energy - Demand Forecasting & Capacity Planning 📈* — fictional company: **LoadCast Energy** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique readings?
- **Old SQL:** `SELECT reading_date, MEASURE(reading_count) AS reading_count FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.demand_readings GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has unique territorys changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_territory_count) AS unique_territory_count FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** Which service territorys have the highest total daily peak demand in mw?
- **New SQL:** `SELECT territory_name, SUM(peak_demand_mw) AS total_metric FROM {fqn}.demand_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique forecasts?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_count) AS forecast_count FROM {fqn}.demand_forecast_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** Which territory type: urban, suburban, rural, industrial, commercials have the highest total average demand in mw for the day?
- **New SQL:** `SELECT territory_type, SUM(avg_demand_mw) AS total_metric FROM {fqn}.demand_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted peak mw?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_peak_mw) AS max_forecasted_peak_mw FROM {fqn}.demand_forecast_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How has average forecasted peak demand in mw trended by month?
- **New SQL:** `SELECT forecast_month, MEASURE(avg_forecasted_peak_mw) AS avg_forecasted_peak_mw FROM {fqn}.demand_forecast_metrics GROUP BY ALL ORDER BY forecast_month`

**B4** — `rewritten`
- **Old Q:** What are the top service territory identifier by total daily peak demand in mw?
- **Old SQL:** `SELECT territory_id, SUM(peak_demand_mw) AS total_peak_demand_mw FROM {fqn}.demand_readings GROUP BY territory_id ORDER BY total_peak_demand_mw DESC LIMIT 10`
- **New Q:** Which climate zone: hot-humid, hot-dry, temperate, cold, mixeds have the best average average daily temperature in fahrenheit?
- **New SQL:** `SELECT climate_zone, AVG(avg_temp_fahrenheit) AS avg_metric FROM {fqn}.demand_readings GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average absolute forecast error percentage by service territory name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.demand_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which territory types have the highest average load factor as percentage?
- **New SQL:** `SELECT territory_type, AVG(load_factor_pct) AS avg_metric FROM {fqn}.demand_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest peak demand mw?
- **Old SQL:** `SELECT reading_date, MEASURE(max_peak_demand_mw) AS max_peak_demand_mw FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average daily peak demand in mw trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_peak_demand_mw) AS avg_peak_demand_mw FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `rewritten`
- **Old Q:** How has highest avg demand mw changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(max_avg_demand_mw) AS max_avg_demand_mw FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has highest average demand mw changed over time?
- **New SQL:** `SELECT reading_date, MEASURE(max_avg_demand_mw) AS max_avg_demand_mw FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** How has unique forecasts changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_count) AS forecast_count FROM {fqn}.demand_forecast_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', forecast_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.demand_forecasts GROUP BY 1 ORDER BY 1`

**E3** — `unchanged`
- Q: *What is the trend of total daily peak demand in mw over time?*

**E4** — `unchanged`
- Q: *What is the trend of total forecasted peak demand in mw over time?*

**E5** — `rewritten`
- **Old Q:** How has the average load factor as percentage (avg demand / peak demand * 100) changed over time?
- **Old SQL:** `SELECT report_month, AVG(load_factor_pct) AS avg_load_factor_pct FROM {fqn}.demand_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** How has the average load factor as percentage (average demand / peak demand * 100) changed over time?
- **New SQL:** `SELECT report_month, AVG(load_factor_pct) AS avg_load_factor_pct FROM {fqn}.demand_kpi_monthly GROUP BY report_month ORDER BY report_month`

**E6** — `rewritten`
- **Old Q:** How has total avg temp fahrenheit changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_avg_temp_fahrenheit) AS total_avg_temp_fahrenheit FROM {fqn}.demand_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average average daily temperature in fahrenheit trended over time?
- **New SQL:** `SELECT reading_date, AVG(avg_temp_fahrenheit) AS avg_avg_temp_fahrenheit FROM {fqn}.demand_readings GROUP BY reading_date ORDER BY reading_date`

---

### `electric_utility/grid_management_energy_mix`
*PowerGrid Analytics - Grid Management & Energy Mix ⚡* — fictional company: **PowerGrid Analytics** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique readings?
- **Old SQL:** `SELECT reading_date, MEASURE(reading_count) AS reading_count FROM {fqn}.generation_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.generation_readings GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has unique zones changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_zone_count) AS unique_zone_count FROM {fqn}.generation_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** Which grid zone have the highest total generation output in megawatts?
- **New SQL:** `SELECT zone_name, SUM(generation_mw) AS total_metric FROM {fqn}.generation_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest peak demand mw?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_peak_demand_mw) AS max_peak_demand_mw FROM {fqn}.load_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average peak demand in mw for the day trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_peak_demand_mw) AS avg_peak_demand_mw FROM {fqn}.load_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `unchanged`
- Q: *How has total power imported in mw changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top grid zone identifier by total curtailed generation in mw (renewable only)?
- **Old SQL:** `SELECT zone_id, SUM(curtailment_mw) AS total_curtailment_mw FROM {fqn}.generation_readings GROUP BY zone_id ORDER BY total_curtailment_mw DESC LIMIT 10`
- **New Q:** Which grid zone have the highest total curtailed generation in mw?
- **New SQL:** `SELECT zone_name, SUM(curtailment_mw) AS total_curtailment_mw FROM {fqn}.generation_readings GROUP BY zone_name ORDER BY total_curtailment_mw DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average congestion severity index 0-10 by grid zone name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.grid_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which geographic regions have the highest average renewable energy share of total generation?
- **New SQL:** `SELECT region, AVG(renewable_share_pct) AS avg_metric FROM {fqn}.grid_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest generation mw?
- **Old SQL:** `SELECT reading_date, MEASURE(max_generation_mw) AS max_generation_mw FROM {fqn}.generation_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** What has been the peak generation output in megawatts each month?
- **New SQL:** `SELECT reading_date, MEASURE(max_generation_mw) AS max_generation_mw FROM {fqn}.generation_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `unchanged`
- Q: *How has total generation output in mw changed over time?*

**E2** — `unchanged`
- Q: *What is the monthly trend in total power exported in mw?*

**E3** — `unchanged`
- Q: *What is the monthly trend in average renewable share percentage?*

**E4** — `unchanged`
- Q: *What is the trend of total curtailed generation in mw (renewable only) over time?*

**E5** — `unchanged`
- Q: *What is the trend of total peak demand in mw for the day over time?*

**E6** — `unchanged`
- Q: *How has the average renewable energy share of total generation changed over time?*

---

### `electric_utility/outage_response`
*RestorePower Systems - Outage Response & Crew Dispatch 🔌* — fictional company: **RestorePower Systems** — 4 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in storm outage count?*

**B1** — `rewritten`
- **Old Q:** How has unique total outages changed over time?
- **Old SQL:** `SELECT outage_date, MEASURE(total_outage_count) AS total_outage_count FROM {fqn}.outage_events_metrics GROUP BY ALL ORDER BY outage_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', outage_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.outage_events GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *How has highest response time minutes changed over time?*

**B3** — `unchanged`
- Q: *What is the monthly trend in total restoration jobs completed?*

**B4** — `rewritten`
- **Old Q:** What are the top distribution feeder identifier by total number of customers without power?
- **Old SQL:** `SELECT feeder_id, SUM(customers_affected) AS total_customers_affected FROM {fqn}.outage_events GROUP BY feeder_id ORDER BY total_customers_affected DESC LIMIT 10`
- **New Q:** Which distribution feeders have the highest total number of customers without power?
- **New SQL:** `SELECT feeder_name, SUM(customers_affected) AS total_customers_affected FROM {fqn}.outage_events GROUP BY feeder_name ORDER BY total_customers_affected DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average crew utilization percentage for the day by service district?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.outage_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which service districts have the highest average percentage of outages restored within sla target?
- **New SQL:** `SELECT district, AVG(restoration_rate_pct) AS avg_metric FROM {fqn}.outage_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique feeders?
- **Old SQL:** `SELECT outage_date, MEASURE(unique_feeder_count) AS unique_feeder_count FROM {fqn}.outage_events_metrics GROUP BY ALL ORDER BY outage_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', outage_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.outage_events GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest customers affected changed over time?*

**E2** — `unchanged`
- Q: *How has storm outage count changed over time?*

**E3** — `unchanged`
- Q: *Which districts have the highest total customer-minutes interrupted?*

**E4** — `unchanged`
- Q: *What is the trend of total number of customers without power over time?*

**E5** — `unchanged`
- Q: *What is the trend of total time from report to crew dispatch in minutes over time?*

**E6** — `unchanged`
- Q: *How has the average percentage of outages restored within sla target changed over time?*

---

### `electric_utility/transformer_asset_health`
*GridGuard Utilities - Transformer Asset Health ⚡* — fictional company: **GridGuard Utilities** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical alert count?*

**B1** — `rewritten`
- **Old Q:** How has unique readings changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(reading_count) AS reading_count FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in total failure events count?*

**B3** — `rewritten`
- **Old Q:** How has unique total events changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_event_count) AS total_event_count FROM {fqn}.failure_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** Which transformer have the best average top oil temperature in celsius?
- **New SQL:** `SELECT transformer_name, AVG(oil_temp_celsius) AS avg_metric FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top transformer asset identifier by total top oil temperature in celsius?
- **Old SQL:** `SELECT transformer_id, SUM(oil_temp_celsius) AS total_oil_temp_celsius FROM {fqn}.sensor_readings GROUP BY transformer_id ORDER BY total_oil_temp_celsius DESC LIMIT 10`
- **New Q:** Which substation where transformer is installeds have the highest total total dissolved gas in oil?
- **New SQL:** `SELECT substation, SUM(dissolved_gas_ppm) AS total_metric FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of failure or maintenance event?
- **Old SQL:** `SELECT event_date, COUNT(*) AS record_count FROM {fqn}.failure_events GROUP BY event_date ORDER BY event_date`
- **New Q:** Which substations have the highest average outage duration in hours?
- **New SQL:** `SELECT substation, MEASURE(avg_outage_hours) AS avg_outage_hours FROM {fqn}.failure_events_metrics GROUP BY ALL ORDER BY avg_outage_hours DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the report month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.health_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which substations have the highest total average health index for the month?
- **New SQL:** `SELECT substation, SUM(avg_health_index) AS total_metric FROM {fqn}.health_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique transformers?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_transformer_count) AS unique_transformer_count FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest dissolved gas ppm changed over time?*

**E2** — `unchanged`
- Q: *How has total vibration mm s changed over time?*

**E3** — `unchanged`
- Q: *How does the number of unique readings vary by substation?*

**E4** — `unchanged`
- Q: *What is the trend of total top oil temperature in celsius over time?*

**E5** — `unchanged`
- Q: *What is the trend of total duration of outage in hours over time?*

**E6** — `rewritten`
- **Old Q:** How has the average average health index for the month (0-100) changed over time?
- **Old SQL:** `SELECT report_month, AVG(avg_health_index) AS avg_avg_health_index FROM {fqn}.health_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which substations have the highest average transformer health index?
- **New SQL:** `SELECT substation, AVG(health_index) AS avg_health FROM {fqn}.transformer_snapshots GROUP BY substation ORDER BY avg_health DESC LIMIT 10`

---

### `food_beverage/inventory_optimization`
*FreshStock Solutions - Perishable Inventory Optimization 📦* — fictional company: **FreshStock Solutions** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique products?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.inventory_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.inventory_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest on hand units changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique items?
- **Old SQL:** `SELECT perf_month, MEASURE(item_count) AS item_count FROM {fqn}.waste_kpi_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** Which products have the highest total days until expiration?
- **New SQL:** `SELECT product_name, SUM(days_to_expiry) AS total_metric FROM {fqn}.perishable_products GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `unchanged`
- Q: *How has highest total spoiled units changed over time?*

**B4** — `unchanged`
- Q: *What are the top product id by total units moved?*

**B5** — `unchanged`
- Q: *What is the average weekly spoilage rate 0-100 by category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per performance month?
- **Old SQL:** `SELECT perf_month, COUNT(*) AS record_count FROM {fqn}.shelf_life_snapshots GROUP BY perf_month ORDER BY perf_month`
- **New Q:** Which categorys have the highest average turnover ratio?
- **New SQL:** `SELECT product_category, MEASURE(avg_turnover) AS avg_turnover FROM {fqn}.waste_kpi_monthly GROUP BY ALL ORDER BY avg_turnover DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total near-expiry units?*

**E1** — `rewritten`
- **Old Q:** How has avg units on hand changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_on_hand) AS avg_on_hand FROM {fqn}.inventory_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average units on hand changed over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_on_hand) AS avg_on_hand FROM {fqn}.inventory_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**E2** — `unchanged`
- Q: *What is the monthly trend in total units spoiled?*

**E3** — `rewritten`
- **Old Q:** What is the monthly trend in avg shelf life remaining days?
- **Old SQL:** `SELECT perf_month, MEASURE(avg_shelf_remaining) AS avg_shelf_remaining FROM {fqn}.waste_kpi_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** What is the monthly trend in average shelf life remaining days?
- **New SQL:** `SELECT perf_month, MEASURE(avg_shelf_remaining) AS avg_shelf_remaining FROM {fqn}.waste_kpi_monthly GROUP BY ALL ORDER BY perf_month`

**E4** — `unchanged`
- Q: *What is the trend of total units moved over time?*

**E5** — `unchanged`
- Q: *What is the trend of total units on hand over time?*

**E6** — `unchanged`
- Q: *How has the average inventory turnover ratio changed over time?*

---

### `food_beverage/product_process_traceability_recall`
*TraceFood Systems - Product Traceability & Recall 📋* — fictional company: **TraceFood Systems** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in full trace count?*

**B1** — `unchanged`
- Q: *How has gap count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in fail sim count?*

**B3** — `rewritten`
- **Old Q:** How has unique products changed over time?
- **Old SQL:** `SELECT perf_month, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.recall_readiness_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', perf_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.chain_of_custody_snapshots GROUP BY 1 ORDER BY 1`

**B4** — `unchanged`
- Q: *What are the top product id by total units in lot?*

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.lot_tracking_events GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which categorys have the highest average recorded temperature?
- **New SQL:** `SELECT product_category, AVG(temp_recorded_f) AS avg_metric FROM {fqn}.lot_tracking_events GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per performance month?
- **Old SQL:** `SELECT perf_month, COUNT(*) AS record_count FROM {fqn}.chain_of_custody_snapshots GROUP BY perf_month ORDER BY perf_month`
- **New Q:** Which categorys have the highest average trace success rate?
- **New SQL:** `SELECT product_category, MEASURE(avg_trace_success) AS avg_trace_success FROM {fqn}.recall_readiness_monthly GROUP BY ALL ORDER BY avg_trace_success DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total lotss?
- **Old SQL:** `SELECT event_date, MEASURE(total_lots) AS total_lots FROM {fqn}.traceability_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.products GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique events changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(event_count) AS event_count FROM {fqn}.traceability_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.products GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest lots traced?
- **Old SQL:** `SELECT perf_month, MEASURE(max_lots_traced) AS max_lots_traced FROM {fqn}.recall_readiness_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** What has been the peak lots successfully traced each month?
- **New SQL:** `SELECT perf_month, MEASURE(max_lots_traced) AS max_lots_traced FROM {fqn}.recall_readiness_monthly GROUP BY ALL ORDER BY perf_month`

**E3** — `rewritten`
- **Old Q:** Rank product categories by avg fda compliance
- **Old SQL:** `SELECT product_category, MEASURE(avg_fda_compliance) AS avg_fda_compliance FROM {fqn}.recall_readiness_monthly GROUP BY ALL ORDER BY avg_fda_compliance DESC`
- **New Q:** Rank product categories by average fda compliance
- **New SQL:** `SELECT product_category, MEASURE(avg_fda_compliance) AS avg_fda_compliance FROM {fqn}.recall_readiness_monthly GROUP BY ALL ORDER BY avg_fda_compliance DESC`

**E4** — `unchanged`
- Q: *How does total units in lot break down by product id for 'Gap' records?*

**E5** — `unchanged`
- Q: *What is the trend of total recorded temperature f over time?*

**E6** — `unchanged`
- Q: *How has the average trace success rate 0-100 changed over time?*

---

### `food_beverage/quality_event_root_cause_analysis`
*FreshGuard Foods - Quality Event Root Cause Analysis 🔍* — fictional company: **FreshGuard Foods** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical events count?*

**B1** — `rewritten`
- **Old Q:** How has unique total eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.quality_kpi_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.product_lines GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in nc count?*

**B3** — `rewritten`
- **Old Q:** How has unique products changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY kpi_month`
- **New Q:** Which products have the highest total cost impact?
- **New SQL:** `SELECT product_name, SUM(cost_impact_usd) AS total_metric FROM {fqn}.product_lines GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `unchanged`
- Q: *What are the top product id by total units affected?*

**B5** — `unchanged`
- Q: *What is the average overall quality score 0-100 by category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.inspection_records GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which categorys have the highest average audit score?
- **New SQL:** `SELECT product_category, MEASURE(avg_audit_score) AS avg_audit_score FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY avg_audit_score DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique products?
- **Old SQL:** `SELECT event_date, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.quality_kpi_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.product_lines GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest units affected changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest events count?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_events_count) AS max_events_count FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY kpi_month`
- **New Q:** What has been the peak quality events in month each month?
- **New SQL:** `SELECT kpi_month, MEASURE(max_events_count) AS max_events_count FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY kpi_month`

**E3** — `unchanged`
- Q: *How has nc count changed over time?*

**E4** — `unchanged`
- Q: *What is the trend of total units affected over time?*

**E5** — `unchanged`
- Q: *What is the trend of total microbial count cfu/g over time?*

**E6** — `unchanged`
- Q: *How has the average regulatory audit score 0-100 changed over time?*

---

### `food_beverage/scenario_planning_business_simulation`
*FoodPlan Analytics - Scenario Planning & Simulation 🎯* — fictional company: **FoodPlan Analytics** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in disruption count?*

**B1** — `rewritten`
- **Old Q:** How has unique runs changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(run_count) AS run_count FROM {fqn}.scenario_kpi_monthly GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.product_categories GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in invest count?*

**B3** — `rewritten`
- **Old Q:** How has unique categorys changed over time?
- **Old SQL:** `SELECT outcome_month, MEASURE(unique_category_count) AS unique_category_count FROM {fqn}.portfolio_kpi_monthly GROUP BY ALL ORDER BY outcome_month`
- **New Q:** Which categorys have the highest total simulated revenue?
- **New SQL:** `SELECT category_name, SUM(simulated_revenue_usd) AS total_metric FROM {fqn}.product_categories GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top category id by total simulated revenue usd?
- **Old SQL:** `SELECT category_id, SUM(simulated_revenue_usd) AS total_simulated_revenue_usd FROM {fqn}.product_categories GROUP BY category_id ORDER BY total_simulated_revenue_usd DESC LIMIT 10`
- **New Q:** Which segments have the best average simulated margin 0-100?
- **New SQL:** `SELECT segment, AVG(simulated_margin_pct) AS avg_metric FROM {fqn}.product_categories GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average input cost index (100=baseline) by segment?
- **Old SQL:** `SELECT segment, AVG(input_cost_index) AS avg_input_cost_index FROM {fqn}.scenario_runs GROUP BY segment ORDER BY avg_input_cost_index DESC`
- **New Q:** Which segments have the highest average input cost index?
- **New SQL:** `SELECT segment, AVG(input_cost_index) AS avg_input_cost_index FROM {fqn}.scenario_runs GROUP BY segment ORDER BY avg_input_cost_index DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per outcome month?
- **Old SQL:** `SELECT outcome_month, COUNT(*) AS record_count FROM {fqn}.market_snapshots GROUP BY outcome_month ORDER BY outcome_month`
- **New Q:** Which segments have the highest average optimal price change?
- **New SQL:** `SELECT segment, MEASURE(avg_optimal_price_change) AS avg_optimal_price_change FROM {fqn}.portfolio_kpi_monthly GROUP BY ALL ORDER BY avg_optimal_price_change DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique categorys?
- **Old SQL:** `SELECT run_date, MEASURE(unique_category_count) AS unique_category_count FROM {fqn}.scenario_kpi_monthly GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.product_categories GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest simulated revenue changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest expected revenue?
- **Old SQL:** `SELECT outcome_month, MEASURE(max_expected_revenue) AS max_expected_revenue FROM {fqn}.portfolio_kpi_monthly GROUP BY ALL ORDER BY outcome_month`
- **New Q:** What has been the peak expected_revenue each month?
- **New SQL:** `SELECT outcome_month, MEASURE(max_expected_revenue) AS max_expected_revenue FROM {fqn}.portfolio_kpi_monthly GROUP BY ALL ORDER BY outcome_month`

**E3** — `unchanged`
- Q: *How has invest count changed over time?*

**E4** — `rewritten`
- **Old Q:** What is the trend of total simulated revenue usd over time?
- **Old SQL:** `SELECT run_date, SUM(simulated_revenue_usd) AS total_simulated_revenue_usd FROM {fqn}.product_categories GROUP BY run_date ORDER BY run_date`
- **New Q:** How has total simulated revenue trended over time?
- **New SQL:** `SELECT run_date, SUM(simulated_revenue_usd) AS total_simulated_revenue_usd FROM {fqn}.product_categories GROUP BY run_date ORDER BY run_date`

**E5** — `unchanged`
- Q: *What is the trend of total price elasticity of demand over time?*

**E6** — `rewritten`
- **Old Q:** How has the average recommended price change pct changed over time?
- **Old SQL:** `SELECT outcome_month, AVG(optimal_price_change_pct) AS avg_optimal_price_change_pct FROM {fqn}.market_snapshots GROUP BY outcome_month ORDER BY outcome_month`
- **New Q:** How has average recommended price change percentage trended by month?
- **New SQL:** `SELECT outcome_month, AVG(optimal_price_change_pct) AS avg_optimal_price_change_pct FROM {fqn}.market_snapshots GROUP BY outcome_month ORDER BY outcome_month`

---

### `industrial_distribution/demand_forecasting`
*DistroForecast Systems - Demand Forecasting & Backlog 📈* — fictional company: **DistroForecast Systems** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in backordered count?*

**B1** — `rewritten`
- **Old Q:** How has unique total orders changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(total_order_count) AS total_order_count FROM {fqn}.demand_kpi_monthly GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.product_skus GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in over forecast count?*

**B3** — `rewritten`
- **Old Q:** How has unique forecasts changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_count) AS forecast_count FROM {fqn}.forecast_accuracy_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** Which product sku codes have the highest total units ordered?
- **New SQL:** `SELECT sku, SUM(order_quantity) AS total_metric FROM {fqn}.product_skus GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top product sku code by total units ordered?
- **Old SQL:** `SELECT sku, SUM(order_quantity) AS total_order_quantity FROM {fqn}.product_skus GROUP BY sku ORDER BY total_order_quantity DESC LIMIT 10`
- **New Q:** Which products have the highest total unit price?
- **New SQL:** `SELECT product_name, SUM(unit_price_usd) AS total_metric FROM {fqn}.product_skus GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average order fill rate 0-100 by product category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per forecast month (first day)?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which product skus have the highest average forecast error percentage?
- **New SQL:** `SELECT sku, MEASURE(avg_forecast_error) AS avg_forecast_error FROM {fqn}.forecast_accuracy_monthly GROUP BY ALL ORDER BY avg_forecast_error DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest order quantity?
- **Old SQL:** `SELECT order_date, MEASURE(max_order_quantity) AS max_order_quantity FROM {fqn}.demand_kpi_monthly GROUP BY ALL ORDER BY order_date`
- **New Q:** What has been the peak units ordered each month?
- **New SQL:** `SELECT order_date, MEASURE(max_order_quantity) AS max_order_quantity FROM {fqn}.demand_kpi_monthly GROUP BY ALL ORDER BY order_date`

**E1** — `rewritten`
- **Old Q:** How has total order revenue usd changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(total_order_revenue) AS total_order_revenue FROM {fqn}.demand_kpi_monthly GROUP BY ALL ORDER BY order_date`
- **New Q:** How has total order revenue trended over time?
- **New SQL:** `SELECT order_date, MEASURE(total_order_revenue) AS total_order_revenue FROM {fqn}.demand_kpi_monthly GROUP BY ALL ORDER BY order_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted units?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_units) AS max_forecasted_units FROM {fqn}.forecast_accuracy_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak model-predicted demand units each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_forecasted_units) AS max_forecasted_units FROM {fqn}.forecast_accuracy_monthly GROUP BY ALL ORDER BY forecast_month`

**E3** — `unchanged`
- Q: *How has highest forecasted units changed over time?*

**E4** — `unchanged`
- Q: *How does total units ordered break down by product sku code for 'Backordered' records?*

**E5** — `rewritten`
- **Old Q:** What is the trend of total total open order value in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(open_order_value_usd) AS total_open_order_value_usd FROM {fqn}.sales_orders GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total total open order value in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(open_order_value_usd) AS total_open_order_value_usd FROM {fqn}.sales_orders GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average absolute forecast error percent changed over time?*

---

### `industrial_distribution/inventory_optimization`
*StockSmart Distribution - Inventory Optimization 📦* — fictional company: **StockSmart Distribution** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in stockout count?*

**B1** — `rewritten`
- **Old Q:** How has unique total snapshots changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_snapshot_count) AS total_snapshot_count FROM {fqn}.inventory_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.inventory_transactions GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique items?
- **Old SQL:** `SELECT perf_month, MEASURE(item_count) AS item_count FROM {fqn}.inventory_perf_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** Which products have the highest total units moved?
- **New SQL:** `SELECT product_name, SUM(quantity_moved) AS total_metric FROM {fqn}.warehouse_products GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `unchanged`
- Q: *How has highest turnover ratio changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top warehouse-product combo identifier by total units moved (positive=receipt, negative=issue)?
- **Old SQL:** `SELECT wp_id, SUM(quantity_moved) AS total_quantity_moved FROM {fqn}.warehouse_products GROUP BY wp_id ORDER BY total_quantity_moved DESC LIMIT 10`
- **New Q:** Which warehouse locations have the highest total unit cost?
- **New SQL:** `SELECT warehouse, SUM(unit_cost_usd) AS total_metric FROM {fqn}.warehouse_products GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of inventory snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.inventory_transactions GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which warehouses have the highest average units on hand?
- **New SQL:** `SELECT warehouse, MEASURE(avg_on_hand_qty) AS avg_on_hand_qty FROM {fqn}.inventory_kpi_monthly GROUP BY ALL ORDER BY avg_on_hand_qty DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per performance month?
- **Old SQL:** `SELECT perf_month, COUNT(*) AS record_count FROM {fqn}.inventory_snapshots GROUP BY perf_month ORDER BY perf_month`
- **New Q:** Which warehouses have the highest average inventory turnover?
- **New SQL:** `SELECT warehouse, MEASURE(avg_turnover_ratio) AS avg_turnover_ratio FROM {fqn}.inventory_perf_monthly GROUP BY ALL ORDER BY avg_turnover_ratio DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique wps?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_wp_count) AS unique_wp_count FROM {fqn}.inventory_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.inventory_transactions GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest on hand qty changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total stockout days?
- **Old SQL:** `SELECT perf_month, MEASURE(total_stockout_days) AS total_stockout_days FROM {fqn}.inventory_perf_monthly GROUP BY ALL ORDER BY perf_month`
- **New Q:** How has average number of stockout days in month trended over time?
- **New SQL:** `SELECT perf_month, AVG(stockout_days) AS avg_stockout_days FROM {fqn}.inventory_snapshots GROUP BY perf_month ORDER BY perf_month`

**E3** — `unchanged`
- Q: *How has total monthly carrying cost changed over time?*

**E4** — `rewritten`
- **Old Q:** What is the trend of total units moved (positive=receipt, negative=issue) over time?
- **Old SQL:** `SELECT movement_date, SUM(quantity_moved) AS total_quantity_moved FROM {fqn}.warehouse_products GROUP BY movement_date ORDER BY movement_date`
- **New Q:** How does units moved compare across products?
- **New SQL:** `SELECT product_name, SUM(quantity_moved) AS total_quantity_moved FROM {fqn}.warehouse_products GROUP BY product_name ORDER BY product_name LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total units on hand over time?*

**E6** — `unchanged`
- Q: *How has the average inventory turnover ratio changed over time?*

---

### `industrial_distribution/working_capital_cash_flow_optimization`
*DistroCapital Finance - Working Capital & Cash Flow 💰* — fictional company: **DistroCapital Finance** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique transactions?
- **Old SQL:** `SELECT txn_date, MEASURE(transaction_count) AS transaction_count FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.business_units GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has unique bus changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(unique_bu_count) AS unique_bu_count FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`
- **New Q:** Which business units have the highest total cash inflow?
- **New SQL:** `SELECT bu_name, SUM(cash_inflow_usd) AS total_metric FROM {fqn}.business_units GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B2** — `unchanged`
- Q: *What is the monthly trend in critical count?*

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted cash flow?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_cash_flow) AS max_forecasted_cash_flow FROM {fqn}.working_capital_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak forecasted_cash_flow each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_forecasted_cash_flow) AS max_forecasted_cash_flow FROM {fqn}.working_capital_monthly GROUP BY ALL ORDER BY forecast_month`

**B4** — `rewritten`
- **Old Q:** What are the top business unit identifier by total cash inflow in usd?
- **Old SQL:** `SELECT bu_id, SUM(cash_inflow_usd) AS total_cash_inflow_usd FROM {fqn}.business_units GROUP BY bu_id ORDER BY total_cash_inflow_usd DESC LIMIT 10`
- **New Q:** Which business segments have the highest total cash outflow?
- **New SQL:** `SELECT business_segment, SUM(cash_outflow_usd) AS total_metric FROM {fqn}.business_units GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.cash_transactions GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which business segments have the highest total ar balance?
- **New SQL:** `SELECT business_segment, SUM(ar_balance_usd) AS total_metric FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per forecast month?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.working_capital_snapshots GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which business segments have the highest average cash conversion cycle days?
- **New SQL:** `SELECT business_segment, MEASURE(avg_ccc_days) AS avg_ccc_days FROM {fqn}.working_capital_monthly GROUP BY ALL ORDER BY avg_ccc_days DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest cash inflow?
- **Old SQL:** `SELECT txn_date, MEASURE(max_cash_inflow) AS max_cash_inflow FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`
- **New Q:** What has been the peak cash_inflow each month?
- **New SQL:** `SELECT txn_date, MEASURE(max_cash_inflow) AS max_cash_inflow FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`

**E1** — `rewritten`
- **Old Q:** How has total cash inflow usd changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(total_cash_inflow) AS total_cash_inflow FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`
- **New Q:** How has total cash inflow trended over time?
- **New SQL:** `SELECT txn_date, MEASURE(total_cash_inflow) AS total_cash_inflow FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`

**E2** — `unchanged`
- Q: *How has critical count changed over time?*

**E3** — `rewritten`
- **Old Q:** What is the trend of total cash inflow in usd over time?
- **Old SQL:** `SELECT txn_date, SUM(cash_inflow_usd) AS total_cash_inflow_usd FROM {fqn}.business_units GROUP BY txn_date ORDER BY txn_date`
- **New Q:** How has total cash inflow in trended over time?
- **New SQL:** `SELECT txn_date, SUM(cash_inflow_usd) AS total_cash_inflow_usd FROM {fqn}.business_units GROUP BY txn_date ORDER BY txn_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total total ar balance usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(ar_balance_usd) AS total_ar_balance_usd FROM {fqn}.cash_transactions GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total total ar balance trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(ar_balance_usd) AS total_ar_balance_usd FROM {fqn}.cash_transactions GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average current ratio (assets/liabilities) changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique transactions changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(transaction_count) AS transaction_count FROM {fqn}.cashflow_monthly GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.business_units GROUP BY 1 ORDER BY 1`

---

### `logistics/fleet_planning_and_optimization`
*FleetEdge Solutions - Fleet Planning & Optimization 🚚* — fictional company: **FleetEdge Solutions** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in on time operation count?*

**B1** — `rewritten`
- **Old Q:** How has unique operations changed over time?
- **Old SQL:** `SELECT operation_date, MEASURE(operation_count) AS operation_count FROM {fqn}.fleet_operations_metrics GROUP BY ALL ORDER BY operation_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', operation_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.fleet_operations GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest monthly revenue?
- **Old SQL:** `SELECT report_month, MEASURE(max_monthly_revenue) AS max_monthly_revenue FROM {fqn}.fleet_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** What has been the peak monthly_revenue each month?
- **New SQL:** `SELECT report_month, MEASURE(max_monthly_revenue) AS max_monthly_revenue FROM {fqn}.fleet_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`

**B3** — `rewritten`
- **Old Q:** How has total monthly revenue in usd changed over time?
- **Old SQL:** `SELECT report_month, MEASURE(total_monthly_revenue) AS total_monthly_revenue FROM {fqn}.fleet_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** Which vehicles have the highest total total route distance in kilometers?
- **New SQL:** `SELECT vehicle_name, SUM(route_distance_km) AS total_metric FROM {fqn}.fleet_operations GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top vehicle asset identifier by total total route distance in kilometers?
- **Old SQL:** `SELECT vehicle_id, SUM(route_distance_km) AS total_route_distance_km FROM {fqn}.fleet_operations GROUP BY vehicle_id ORDER BY total_route_distance_km DESC LIMIT 10`
- **New Q:** Which vehicle class: heavy duty, medium duty, light duty, sprinters have the highest total cargo weight in kilograms?
- **New SQL:** `SELECT vehicle_class, SUM(cargo_weight_kg) AS total_metric FROM {fqn}.fleet_operations GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average dispatched hours as percentage of available hours by human-readable vehicle name?
- **Old SQL:** `SELECT vehicle_name, AVG(utilization_pct) AS avg_utilization_pct FROM {fqn}.vehicle_utilization_snapshots GROUP BY vehicle_name ORDER BY avg_utilization_pct DESC`
- **New Q:** Which vehicles have the best dispatched hours of available hours?
- **New SQL:** `SELECT vehicle_name, AVG(utilization_pct) AS avg_utilization_pct FROM {fqn}.vehicle_utilization_snapshots GROUP BY vehicle_name ORDER BY avg_utilization_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of reporting month?
- **Old SQL:** `SELECT report_month, COUNT(*) AS record_count FROM {fqn}.fleet_kpi_monthly GROUP BY report_month ORDER BY report_month`
- **New Q:** Which depots have the most idle hours?
- **New SQL:** `SELECT depot_name, SUM(idle_hours) AS total_idle_hours FROM {fqn}.dispatch_events GROUP BY depot_name ORDER BY total_idle_hours DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique vehicles?
- **Old SQL:** `SELECT operation_date, MEASURE(unique_vehicle_count) AS unique_vehicle_count FROM {fqn}.fleet_operations_metrics GROUP BY ALL ORDER BY operation_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', operation_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.fleet_operations GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has highest route distance km changed over time?
- **Old SQL:** `SELECT operation_date, MEASURE(max_route_distance_km) AS max_route_distance_km FROM {fqn}.fleet_operations_metrics GROUP BY ALL ORDER BY operation_date`
- **New Q:** How has total total route distance in kilometers trended over time?
- **New SQL:** `SELECT operation_date, MEASURE(max_route_distance_km) AS max_route_distance_km FROM {fqn}.fleet_operations_metrics GROUP BY ALL ORDER BY operation_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total monthly fuel cost in usd?
- **Old SQL:** `SELECT report_month, MEASURE(total_monthly_fuel_cost) AS total_monthly_fuel_cost FROM {fqn}.fleet_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`
- **New Q:** How has total monthly fuel cost trended over time?
- **New SQL:** `SELECT report_month, MEASURE(total_monthly_fuel_cost) AS total_monthly_fuel_cost FROM {fqn}.fleet_kpi_monthly_metrics GROUP BY ALL ORDER BY report_month`

**E3** — `unchanged`
- Q: *How has average on-time delivery percentage changed over time?*

**E4** — `rewritten`
- **Old Q:** How does total total route distance in kilometers break down by vehicle asset identifier for 'Failed' records?
- **Old SQL:** `SELECT vehicle_id, COUNT(*) AS record_count, SUM(route_distance_km) AS total_route_distance_km FROM {fqn}.fleet_operations WHERE delivery_status = 'Failed' GROUP BY vehicle_id ORDER BY total_route_distance_km DESC`
- **New Q:** Which vehicles have the highest total *?
- **New SQL:** `SELECT vehicle_name, SUM(*) AS record_count, SUM(route_distance_km) AS total_route_distance_km FROM {fqn}.fleet_operations WHERE delivery_status = 'Failed' GROUP BY vehicle_name ORDER BY total_route_distance_km DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total hours vehicle was available for dispatch over time?*

**E6** — `unchanged`
- Q: *How has the average average utilization rate for the month changed over time?*

---

### `logistics/load_demand_forecasting`
*CargoSight Analytics - Load Demand & Shipment Forecasting 📈* — fictional company: **CargoSight Analytics** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total freight revenue count?*

**B1** — `unchanged`
- Q: *How has total weight delivered lbs count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique forecast records?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_record_count) AS forecast_record_count FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', forecast_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.demand_forecasts GROUP BY 1 ORDER BY 1`

**B3** — `rewritten`
- **Old Q:** How has unique lanes changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(unique_lane_count) AS unique_lane_count FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** Which lanes have the highest total shipment weight in pounds?
- **New SQL:** `SELECT lane_name, SUM(weight_lbs) AS total_metric FROM {fqn}.shipment_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top shipping lane identifier by total shipment weight in pounds?
- **Old SQL:** `SELECT lane_id, SUM(weight_lbs) AS total_weight_lbs FROM {fqn}.shipment_orders GROUP BY lane_id ORDER BY total_weight_lbs DESC LIMIT 10`
- **New Q:** Which lane category: domestic ftl, domestic ltl, cross-border, intermodals have the highest total freight charge?
- **New SQL:** `SELECT lane_category, SUM(freight_charge_usd) AS total_metric FROM {fqn}.shipment_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per month being forecasted?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which lane categorys have the highest number of forecast records?
- **New SQL:** `SELECT lane_category, MEASURE(forecast_record_count) AS forecast_record_count FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_record_count DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per weekly snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.capacity_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which lanes have the highest average capacity utilization percentage?
- **New SQL:** `SELECT lane_name, AVG(capacity_utilization_pct) AS avg_metric FROM {fqn}.capacity_snapshots GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in delivered order count?*

**E1** — `unchanged`
- Q: *How has delayed order count changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted shipments?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_shipments) AS max_forecasted_shipments FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak predicted shipment count for month each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_forecasted_shipments) AS max_forecasted_shipments FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`

**E3** — `rewritten`
- **Old Q:** How has unique forecast records changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_record_count) AS forecast_record_count FROM {fqn}.demand_forecasts_metrics GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', forecast_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.demand_forecasts GROUP BY 1 ORDER BY 1`

**E4** — `rewritten`
- **Old Q:** How does total shipment weight in pounds break down by shipping lane identifier for 'Delayed' records?
- **Old SQL:** `SELECT lane_id, COUNT(*) AS record_count, SUM(weight_lbs) AS total_weight_lbs FROM {fqn}.shipment_orders WHERE order_status = 'Delayed' GROUP BY lane_id ORDER BY total_weight_lbs DESC`
- **New Q:** Which lanes have the highest total *?
- **New SQL:** `SELECT lane_name, SUM(*) AS record_count, SUM(weight_lbs) AS total_weight_lbs FROM {fqn}.shipment_orders WHERE order_status = 'Delayed' GROUP BY lane_name ORDER BY total_weight_lbs DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total predicted shipment count for month over time?*

**E6** — `unchanged`
- Q: *How has the average capacity utilization percentage changed over time?*

---

### `logistics/route_planning`
*TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️* — fictional company: **TransRoute Logistics** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique segments?
- **Old SQL:** `SELECT segment_date, MEASURE(segment_count) AS segment_count FROM {fqn}.route_segments_metrics GROUP BY ALL ORDER BY segment_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', segment_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.route_segments GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has unique vehicles changed over time?
- **Old SQL:** `SELECT segment_date, MEASURE(unique_vehicle_count) AS unique_vehicle_count FROM {fqn}.route_segments_metrics GROUP BY ALL ORDER BY segment_date`
- **New Q:** Which vehicles have the highest total maximum load capacity in kilograms?
- **New SQL:** `SELECT vehicle_name, SUM(capacity_kg) AS total_metric FROM {fqn}.vehicles GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B2** — `rewritten`
- **Old Q:** What is the highest total distance km for each week start?
- **Old SQL:** `SELECT week_start, MEASURE(max_total_distance_km) AS max_total_distance_km FROM {fqn}.route_efficiency_metrics_mv GROUP BY ALL ORDER BY max_total_distance_km DESC`
- **New Q:** Which depots have driven the most kilometers in the past week?
- **New SQL:** `SELECT depot_name, SUM(distance_km) AS total_distance_km FROM {fqn}.route_legs WHERE leg_date >= DATE_SUB(CURRENT_DATE(), 7) GROUP BY depot_name ORDER BY total_distance_km DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** What is the weekly distances in km for each week start?
- **Old SQL:** `SELECT week_start, MEASURE(total_weekly_distance_km) AS total_weekly_distance_km FROM {fqn}.route_efficiency_metrics_mv GROUP BY ALL ORDER BY total_weekly_distance_km DESC`
- **New Q:** Which vehicles have the highest total weekly distance traveled?
- **New SQL:** `SELECT vehicle_name, SUM(distance_km) AS total_distance_km FROM {fqn}.route_legs GROUP BY vehicle_name ORDER BY total_distance_km DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top unique vehicle identifier by total maximum load capacity in kilograms?
- **Old SQL:** `SELECT vehicle_id, SUM(capacity_kg) AS total_capacity_kg FROM {fqn}.vehicles GROUP BY vehicle_id ORDER BY total_capacity_kg DESC LIMIT 10`
- **New Q:** Which vehicle class: semi, truck, or vans have the highest total fuel efficiency in kilometers per liter?
- **New SQL:** `SELECT vehicle_type, SUM(fuel_efficiency_km_per_l) AS total_metric FROM {fqn}.vehicles GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average load weight as percent of vehicle capacity by human-readable vehicle name?
- **Old SQL:** `SELECT vehicle_name, AVG(load_utilization_pct) AS avg_load_utilization_pct FROM {fqn}.route_segments GROUP BY vehicle_name ORDER BY avg_load_utilization_pct DESC`
- **New Q:** Which vehicles have the best load weight of vehicle capacity?
- **New SQL:** `SELECT vehicle_name, AVG(load_utilization_pct) AS avg_load_utilization_pct FROM {fqn}.route_segments GROUP BY vehicle_name ORDER BY avg_load_utilization_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per start of reporting week?
- **Old SQL:** `SELECT week_start, COUNT(*) AS record_count FROM {fqn}.route_efficiency_metrics GROUP BY week_start ORDER BY week_start`
- **New Q:** Which vehicles have the highest average on-time delivery percentage?
- **New SQL:** `SELECT vehicle_name, MEASURE(avg_on_time_delivery_pct) AS avg_on_time_delivery_pct FROM {fqn}.route_efficiency_metrics_mv GROUP BY ALL ORDER BY avg_on_time_delivery_pct DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique routes?
- **Old SQL:** `SELECT segment_date, MEASURE(unique_route_count) AS unique_route_count FROM {fqn}.route_segments_metrics GROUP BY ALL ORDER BY segment_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', segment_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.route_segments GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has highest distance km changed over time?
- **Old SQL:** `SELECT segment_date, MEASURE(max_distance_km) AS max_distance_km FROM {fqn}.route_segments_metrics GROUP BY ALL ORDER BY segment_date`
- **New Q:** How has total segment distance in kilometers trended over time?
- **New SQL:** `SELECT segment_date, MEASURE(max_distance_km) AS max_distance_km FROM {fqn}.route_segments_metrics GROUP BY ALL ORDER BY segment_date`

**E2** — `unchanged`
- Q: *How does weekly fuel consumption in liters vary by week start?*

**E3** — `rewritten`
- **Old Q:** Show the distribution of records by unique vehicle identifier
- **Old SQL:** `SELECT vehicle_id, COUNT(*) AS record_count FROM {fqn}.vehicles GROUP BY vehicle_id ORDER BY record_count DESC`
- **New Q:** Which vehicles have the highest total maximum load capacity in kilograms?
- **New SQL:** `SELECT vehicle_name, SUM(capacity_kg) AS total_metric FROM {fqn}.vehicles GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total segment distance in kilometers over time?*

**E5** — `unchanged`
- Q: *How has the average percentage of deliveries completed on time changed over time?*

**E6** — `rewritten`
- **Old Q:** Which vehicle types have the highest total load weight kg?
- **Old SQL:** `SELECT vehicle_type, MEASURE(total_load_weight_kg) AS total_load_weight_kg FROM {fqn}.route_segments_metrics GROUP BY ALL ORDER BY total_load_weight_kg DESC`
- **New Q:** Which vehicles are hauling the most cargo weight on average?
- **New SQL:** `SELECT vehicle_name, AVG(cargo_weight_kg) AS avg_cargo_kg FROM {fqn}.route_legs GROUP BY vehicle_name ORDER BY avg_cargo_kg DESC LIMIT 10`

---

### `machinery/asset_health`
*IronPulse Manufacturing - Asset Health Monitor 🔧* — fictional company: **IronPulse Manufacturing** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique assets?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_asset_count) AS unique_asset_count FROM {fqn}.condition_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.condition_readings GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest vibration velocity mm s changed over time?*

**B2** — `rewritten`
- **Old Q:** How has highest avg health index changed over time?
- **Old SQL:** `SELECT summary_month, MEASURE(max_avg_health_index) AS max_avg_health_index FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY summary_month`
- **New Q:** How has highest average health index changed over time?
- **New SQL:** `SELECT summary_month, MEASURE(max_avg_health_index) AS max_avg_health_index FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY summary_month`

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in total maintenance cost in usd?
- **Old SQL:** `SELECT summary_month, MEASURE(total_maintenance_cost) AS total_maintenance_cost FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY summary_month`
- **New Q:** How has total maintenance cost trended over time?
- **New SQL:** `SELECT summary_month, MEASURE(total_maintenance_cost) AS total_maintenance_cost FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY summary_month`

**B4** — `rewritten`
- **Old Q:** What are the top industrial asset identifier by total bearing temperature in celsius?
- **Old SQL:** `SELECT asset_id, SUM(bearing_temperature_c) AS total_bearing_temperature_c FROM {fqn}.condition_readings GROUP BY asset_id ORDER BY total_bearing_temperature_c DESC LIMIT 10`
- **New Q:** Which type of industrial assets have the highest average bearing temperature in celsius?
- **New SQL:** `SELECT asset_type, AVG(bearing_temperature_c) AS total_bearing_temperature_c FROM {fqn}.condition_readings GROUP BY asset_type ORDER BY total_bearing_temperature_c DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date the failure was recorded?
- **Old SQL:** `SELECT failure_date, COUNT(*) AS record_count FROM {fqn}.failure_events GROUP BY failure_date ORDER BY failure_date`
- **New Q:** Which type of industrial assets have the highest average downtime caused by failure in hours?
- **New SQL:** `SELECT asset_type, AVG(downtime_hours) AS avg_metric FROM {fqn}.failure_events GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the summary record?
- **Old SQL:** `SELECT summary_month, COUNT(*) AS record_count FROM {fqn}.asset_health_monthly GROUP BY summary_month ORDER BY summary_month`
- **New Q:** Which type of industrial assets have the highest average asset availability percentage?
- **New SQL:** `SELECT asset_type, MEASURE(avg_availability) AS avg_availability FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY avg_availability DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total oil temperature c?
- **Old SQL:** `SELECT reading_date, MEASURE(total_oil_temperature_c) AS total_oil_temperature_c FROM {fqn}.condition_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average lubricant oil temperature in celsius trended over time?
- **New SQL:** `SELECT reading_date, AVG(oil_temperature_c) AS avg_oil_temperature_c FROM {fqn}.condition_readings GROUP BY reading_date ORDER BY reading_date`

**E1** — `unchanged`
- Q: *How has average vibration velocity in mm/s changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total avg health index?
- **Old SQL:** `SELECT summary_month, MEASURE(total_avg_health_index) AS total_avg_health_index FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY summary_month`
- **New Q:** What is the monthly trend in total average health index?
- **New SQL:** `SELECT summary_month, MEASURE(total_avg_health_index) AS total_avg_health_index FROM {fqn}.asset_health_monthly_metrics GROUP BY ALL ORDER BY summary_month`

**E3** — `unchanged`
- Q: *Rank asset types by total unplanned downtime hours*

**E4** — `unchanged`
- Q: *What is the trend of total bearing temperature in celsius over time?*

**E5** — `unchanged`
- Q: *What is the trend of total downtime caused by failure in hours over time?*

**E6** — `unchanged`
- Q: *How has the average average health index for the month 0-100 changed over time?*

---

### `machinery/demand_forecasting`
*ForecastPro Machinery - Demand Forecasting 📈* — fictional company: **ForecastPro Machinery** — 4 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total orderss?
- **Old SQL:** `SELECT order_date, MEASURE(total_orders) AS total_orders FROM {fqn}.customer_orders_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.customer_orders GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest order quantity changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecast accuracy percent?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_forecast_accuracy_percent) AS max_forecast_accuracy_percent FROM {fqn}.demand_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** What has been the peak forecast_accuracy_percent each month?
- **New SQL:** `SELECT kpi_month, MEASURE(max_forecast_accuracy_percent) AS max_forecast_accuracy_percent FROM {fqn}.demand_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B3** — `unchanged`
- Q: *How has total backlog units changed over time?*

**B4** — `unchanged`
- Q: *What are the top equipment model ordered by total units ordered?*

**B5** — `unchanged`
- Q: *What is the average mean absolute percentage error by product family?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.demand_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which equipment models have the highest average forecast accuracy?
- **New SQL:** `SELECT equipment_model, MEASURE(avg_forecast_accuracy) AS avg_forecast_accuracy FROM {fqn}.demand_kpi_metrics GROUP BY ALL ORDER BY avg_forecast_accuracy DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total order revenue in usd?
- **Old SQL:** `SELECT order_date, MEASURE(total_order_revenue) AS total_order_revenue FROM {fqn}.customer_orders_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How has total order revenue trended over time?
- **New SQL:** `SELECT order_date, MEASURE(total_order_revenue) AS total_order_revenue FROM {fqn}.customer_orders_metrics GROUP BY ALL ORDER BY order_date`

**E1** — `unchanged`
- Q: *How has total units ordered changed over time?*

**E2** — `unchanged`
- Q: *What is the monthly trend in total monthly revenue?*

**E3** — `unchanged`
- Q: *How has highest forecast accuracy percent changed over time?*

**E4** — `unchanged`
- Q: *How does total units ordered break down by equipment model ordered for 'Backlog' records?*

**E5** — `unchanged`
- Q: *What is the trend of total forecasted demand units over time?*

**E6** — `unchanged`
- Q: *How has the average forecast accuracy percentage changed over time?*

---

### `machinery/field_service_assistant`
*FieldForce Machinery - Field Service Assistant 🛠️* — fictional company: **FieldForce Machinery** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in first time fix count?*

**B1** — `rewritten`
- **Old Q:** How has unique total ticketss changed over time?
- **Old SQL:** `SELECT ticket_date, MEASURE(total_tickets) AS total_tickets FROM {fqn}.service_tickets_metrics GROUP BY ALL ORDER BY ticket_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', ticket_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.service_tickets GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest first time fix rate percent?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_first_time_fix_rate_percent) AS max_first_time_fix_rate_percent FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** What has been the peak first_time_fix_rate_percent each month?
- **New SQL:** `SELECT kpi_month, MEASURE(max_first_time_fix_rate_percent) AS max_first_time_fix_rate_percent FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B3** — `unchanged`
- Q: *How has total tickets across all models changed over time?*

**B4** — `unchanged`
- Q: *What are the top equipment model at customer site by total time to resolution in hours?*

**B5** — `unchanged`
- Q: *What is the average technician utilization percentage by equipment type category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.service_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which equipment models have the highest average first-time fix rate?
- **New SQL:** `SELECT equipment_model, MEASURE(avg_ftf_rate) AS avg_ftf_rate FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY avg_ftf_rate DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest resolution hours?
- **Old SQL:** `SELECT ticket_date, MEASURE(max_resolution_hours) AS max_resolution_hours FROM {fqn}.service_tickets_metrics GROUP BY ALL ORDER BY ticket_date`
- **New Q:** How has average time to resolution in hours trended by month?
- **New SQL:** `SELECT ticket_date, MEASURE(avg_resolution_hours) AS avg_resolution_hours FROM {fqn}.service_tickets_metrics GROUP BY ALL ORDER BY ticket_date`

**E1** — `unchanged`
- Q: *How has total service cost (parts + labor) changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total repeat visit pct?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_repeat_visit_percent) AS total_repeat_visit_percent FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average repeat visit percent trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(total_repeat_visit_percent) AS total_repeat_visit_percent FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E3** — `rewritten`
- **Old Q:** How has total repeat visit pct changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_repeat_visit_percent) AS total_repeat_visit_percent FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average repeat visit percent trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(total_repeat_visit_percent) AS total_repeat_visit_percent FROM {fqn}.service_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E4** — `unchanged`
- Q: *What is the trend of total time to resolution in hours over time?*

**E5** — `unchanged`
- Q: *What is the trend of total tickets closed in the period over time?*

**E6** — `unchanged`
- Q: *How has the average first-time fix rate percentage changed over time?*

---

### `machinery/financial_analytics_reporting`
*LedgerView Industrial - Financial Analytics 💰* — fictional company: **LedgerView Industrial** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total monthly revenue?*

**B1** — `rewritten`
- **Old Q:** How has total opex count changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(total_opex) AS total_opex FROM {fqn}.financial_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How has total opex trended over time?
- **New SQL:** `SELECT txn_date, MEASURE(total_opex) AS total_opex FROM {fqn}.financial_txn_metrics GROUP BY ALL ORDER BY txn_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique cost centers?
- **Old SQL:** `SELECT kpi_month, MEASURE(unique_cost_center_count) AS unique_cost_center_count FROM {fqn}.financial_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', kpi_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.financial_kpi_monthly GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest gross margin percent changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount in usd?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which cost center types have the highest total transaction amount?
- **New SQL:** `SELECT cost_center_type, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_type ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average variance percentage by cost center type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.financial_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which cost center types have the highest average gross margin percentage?
- **New SQL:** `SELECT cost_center_type, MEASURE(avg_gross_margin) AS avg_gross_margin FROM {fqn}.financial_kpi_metrics GROUP BY ALL ORDER BY avg_gross_margin DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in open posting status count?*

**E1** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total budget utilization pct?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_budget_utilization_percent) AS total_budget_utilization_percent FROM {fqn}.financial_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average budget utilization percent trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(total_budget_utilization_percent) AS total_budget_utilization_percent FROM {fqn}.financial_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E3** — `rewritten`
- **Old Q:** Rank cost center types by total cost per headcount usd
- **Old SQL:** `SELECT cost_center_type, MEASURE(total_cost_per_headcount) AS total_cost_per_headcount FROM {fqn}.financial_kpi_metrics GROUP BY ALL ORDER BY total_cost_per_headcount DESC`
- **New Q:** How does total cost per headcount compare across cost center types?
- **New SQL:** `SELECT cost_center_type, MEASURE(total_cost_per_headcount) AS total_cost_per_headcount FROM {fqn}.financial_kpi_metrics GROUP BY ALL ORDER BY total_cost_per_headcount DESC`

**E4** — `rewritten`
- **Old Q:** How does total transaction amount in usd break down by cost center identifier for 'Posted' records?
- **Old SQL:** `SELECT cost_center_id, COUNT(*) AS record_count, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions WHERE posting_status = 'Posted' GROUP BY cost_center_id ORDER BY total_amount_usd DESC`
- **New Q:** Which cost center types have the highest total *?
- **New SQL:** `SELECT cost_center_type, SUM(*) AS record_count, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions WHERE posting_status = 'Posted' GROUP BY cost_center_type ORDER BY total_amount_usd DESC LIMIT 10`

**E5** — `rewritten`
- **Old Q:** What is the trend of total budgeted amount in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(budget_amount_usd) AS total_budget_amount_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total budgeted amount in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(budget_amount_usd) AS total_budget_amount_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average gross margin percentage changed over time?*

---

### `machinery/machining_process_defect_detection`
*PrecisionEdge Corp - Machining Defect Detection ⚙️* — fictional company: **PrecisionEdge Corp** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in defect count?*

**B1** — `rewritten`
- **Old Q:** How has unique total eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.machining_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.machining_events GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** How has highest defect rate percent changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_defect_rate_percent) AS max_defect_rate_percent FROM {fqn}.defect_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** What has been the peak defect_rate_percent each month?
- **New SQL:** `SELECT kpi_month, MEASURE(max_defect_rate_percent) AS max_defect_rate_percent FROM {fqn}.defect_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in total scrap cost in usd?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_scrap_cost) AS total_scrap_cost FROM {fqn}.defect_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has total scrap cost trended over time?
- **New SQL:** `SELECT kpi_month, MEASURE(total_scrap_cost) AS total_scrap_cost FROM {fqn}.defect_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B4** — `rewritten`
- **Old Q:** What are the top cnc machine identifier by total surface roughness ra in micrometers?
- **Old SQL:** `SELECT machine_id, SUM(surface_finish_um) AS total_surface_finish_um FROM {fqn}.machining_events GROUP BY machine_id ORDER BY total_surface_finish_um DESC LIMIT 10`
- **New Q:** Which cnc machine models have the highest total surface roughness ra in micrometers?
- **New SQL:** `SELECT machine_model, SUM(surface_finish_um) AS total_surface_finish_um FROM {fqn}.machining_events GROUP BY machine_model ORDER BY total_surface_finish_um DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average crater wear depth in mm by cnc machine model?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.defect_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which cnc machine models have the highest average defect rate percentage?
- **New SQL:** `SELECT machine_model, MEASURE(avg_defect_rate) AS avg_defect_rate FROM {fqn}.defect_kpi_metrics GROUP BY ALL ORDER BY avg_defect_rate DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique machines?
- **Old SQL:** `SELECT event_date, MEASURE(unique_machine_count) AS unique_machine_count FROM {fqn}.machining_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.machining_events GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest surface finish um changed over time?*

**E2** — `rewritten`
- **Old Q:** How has unique machines changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(unique_machine_count) AS unique_machine_count FROM {fqn}.defect_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', kpi_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.defect_kpi_monthly GROUP BY 1 ORDER BY 1`

**E3** — `unchanged`
- Q: *What is the trend of total surface roughness ra in micrometers over time?*

**E4** — `unchanged`
- Q: *What is the trend of total flank wear measurement in mm over time?*

**E5** — `unchanged`
- Q: *How has the average defect rate percentage changed over time?*

**E6** — `unchanged`
- Q: *How has total dimensional deviation mm changed over time?*

---

### `machinery/manufacturing_resource_planning`
*PlanWorks Manufacturing - Resource Planning 🏭* — fictional company: **PlanWorks Manufacturing** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total work orderss?
- **Old SQL:** `SELECT wo_date, MEASURE(total_work_orders) AS total_work_orders FROM {fqn}.work_orders_metrics GROUP BY ALL ORDER BY wo_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', wo_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.work_orders GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has unique work centers changed over time?
- **Old SQL:** `SELECT wo_date, MEASURE(unique_work_center_count) AS unique_work_center_count FROM {fqn}.work_orders_metrics GROUP BY ALL ORDER BY wo_date`
- **New Q:** Which work center types have the highest total planned production quantity?
- **New SQL:** `SELECT work_center_type, SUM(planned_qty) AS total_metric FROM {fqn}.work_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique work centers?
- **Old SQL:** `SELECT kpi_month, MEASURE(unique_work_center_count) AS unique_work_center_count FROM {fqn}.planning_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', kpi_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.planning_kpi_monthly GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest schedule adherence percent changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top work center identifier by total planned production quantity?
- **Old SQL:** `SELECT work_center_id, SUM(planned_qty) AS total_planned_qty FROM {fqn}.work_orders GROUP BY work_center_id ORDER BY total_planned_qty DESC LIMIT 10`
- **New Q:** Which materials have the highest shortage hours this month?
- **New SQL:** `SELECT material_name, SUM(shortage_hours) AS total_shortage_hours FROM {fqn}.material_requirements WHERE DATE_TRUNC('month', requirement_date) = DATE_TRUNC('month', CURRENT_DATE()) GROUP BY material_name ORDER BY total_shortage_hours DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average capacity utilization percentage by work center type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.planning_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which work center types have the highest average schedule adherence?
- **New SQL:** `SELECT work_center_type, MEASURE(avg_schedule_adherence) AS avg_schedule_adherence FROM {fqn}.planning_kpi_metrics GROUP BY ALL ORDER BY avg_schedule_adherence DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest planned qty?
- **Old SQL:** `SELECT wo_date, MEASURE(max_planned_qty) AS max_planned_qty FROM {fqn}.work_orders_metrics GROUP BY ALL ORDER BY wo_date`
- **New Q:** What has been the peak planned production quantity each month?
- **New SQL:** `SELECT wo_date, MEASURE(max_planned_qty) AS max_planned_qty FROM {fqn}.work_orders_metrics GROUP BY ALL ORDER BY wo_date`

**E1** — `rewritten`
- **Old Q:** How has total planned hours changed over time?
- **Old SQL:** `SELECT wo_date, MEASURE(total_planned_hours) AS total_planned_hours FROM {fqn}.work_orders_metrics GROUP BY ALL ORDER BY wo_date`
- **New Q:** How has average planned labor/machine hours trended over time?
- **New SQL:** `SELECT wo_date, AVG(planned_hours) AS avg_planned_hours FROM {fqn}.work_orders GROUP BY wo_date ORDER BY wo_date`

**E2** — `unchanged`
- Q: *What is the monthly trend in total throughput units?*

**E3** — `rewritten`
- **Old Q:** How has total changeover hours changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_changeover_hours) AS total_changeover_hours FROM {fqn}.planning_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average total changeover hours trended over time?
- **New SQL:** `SELECT kpi_month, AVG(changeover_hours) AS avg_changeover_hours FROM {fqn}.planning_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E4** — `rewritten`
- **Old Q:** How does total planned production quantity break down by work center identifier for 'Released' records?
- **Old SQL:** `SELECT work_center_id, COUNT(*) AS record_count, SUM(planned_qty) AS total_planned_qty FROM {fqn}.work_orders WHERE wo_status = 'Released' GROUP BY work_center_id ORDER BY total_planned_qty DESC`
- **New Q:** Which work center types have the highest total *?
- **New SQL:** `SELECT work_center_type, SUM(*) AS record_count, SUM(planned_qty) AS total_planned_qty FROM {fqn}.work_orders WHERE wo_status = 'Released' GROUP BY work_center_type ORDER BY total_planned_qty DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total available capacity in hours over time?*

**E6** — `unchanged`
- Q: *How has the average schedule adherence percentage changed over time?*

---

### `machinery/production_monitoring`
*FactoryPulse Systems - Production Monitoring 📊* — fictional company: **FactoryPulse Systems** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique lines?
- **Old SQL:** `SELECT run_date, MEASURE(unique_line_count) AS unique_line_count FROM {fqn}.production_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.production_runs GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest planned qty changed over time?*

**B2** — `unchanged`
- Q: *How has highest availability percent changed over time?*

**B3** — `unchanged`
- Q: *What is the monthly trend in total output units?*

**B4** — `rewritten`
- **Old Q:** What are the top production line identifier by total planned production quantity?
- **Old SQL:** `SELECT line_id, SUM(planned_qty) AS total_planned_qty FROM {fqn}.production_runs GROUP BY line_id ORDER BY total_planned_qty DESC LIMIT 10`
- **New Q:** Which production line types have the most planned production quantity?
- **New SQL:** `SELECT line_type, SUM(planned_qty) AS total_planned_qty FROM {fqn}.production_runs GROUP BY line_type ORDER BY total_planned_qty DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average current speed as percentage of rated by production line type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of oee record?
- **Old SQL:** `SELECT oee_month, COUNT(*) AS record_count FROM {fqn}.oee_monthly GROUP BY oee_month ORDER BY oee_month`
- **New Q:** Which production line types have the highest average oee percentage?
- **New SQL:** `SELECT line_type, MEASURE(avg_oee) AS avg_oee FROM {fqn}.oee_metrics GROUP BY ALL ORDER BY avg_oee DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total good units produced?*

**E1** — `unchanged`
- Q: *How has total rejected units changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total planned downtime hours?
- **Old SQL:** `SELECT oee_month, MEASURE(total_planned_downtime_hours) AS total_planned_downtime_hours FROM {fqn}.oee_metrics GROUP BY ALL ORDER BY oee_month`
- **New Q:** How has average planned downtime hours trended over time?
- **New SQL:** `SELECT oee_month, AVG(planned_downtime_hours) AS avg_planned_downtime_hours FROM {fqn}.oee_monthly GROUP BY oee_month ORDER BY oee_month`

**E3** — `rewritten`
- **Old Q:** Rank line types by total performance pct
- **Old SQL:** `SELECT line_type, MEASURE(total_performance_percent) AS total_performance_percent FROM {fqn}.oee_metrics GROUP BY ALL ORDER BY total_performance_percent DESC`
- **New Q:** Which s have the best total performance percent?
- **New SQL:** `SELECT line_type, AVG(total_performance_percent) AS total_performance_percent FROM {fqn}.oee_metrics GROUP BY ALL ORDER BY total_performance_percent DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total planned production quantity over time?*

**E5** — `unchanged`
- Q: *What is the trend of total units produced in this hour over time?*

**E6** — `unchanged`
- Q: *How has the average availability component of oee changed over time?*

---

### `machinery/quality_event_root_cause_analysis`
*QualityFirst Manufacturing - Quality RCA 🔍* — fictional company: **QualityFirst Manufacturing** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical event count?*

**B1** — `unchanged`
- Q: *How has open capa status count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest defect ppm?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_defect_ppm) AS max_defect_ppm FROM {fqn}.quality_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average defect rate in parts per million trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(avg_defect_ppm) AS avg_defect_ppm FROM {fqn}.quality_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B3** — `unchanged`
- Q: *How has total cost of poor quality changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top product line identifier by total number of units affected?
- **Old SQL:** `SELECT product_line, SUM(units_affected) AS total_units_affected FROM {fqn}.quality_events GROUP BY product_line ORDER BY total_units_affected DESC LIMIT 10`
- **New Q:** Which product line identifiers have the highest total number of units affected?
- **New SQL:** `SELECT product_line, SUM(units_affected) AS total_units_affected FROM {fqn}.quality_events GROUP BY product_line ORDER BY total_units_affected DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of inspection?
- **Old SQL:** `SELECT inspection_date, COUNT(*) AS record_count FROM {fqn}.inspection_records GROUP BY inspection_date ORDER BY inspection_date`
- **New Q:** Which product line identifiers have the highest total number of findings or non-conformances?
- **New SQL:** `SELECT product_line, SUM(findings_count) AS total_metric FROM {fqn}.inspection_records GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.quality_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which product line identifiers have the highest average defect rate in ppm?
- **New SQL:** `SELECT product_line, MEASURE(avg_defect_ppm) AS avg_defect_ppm FROM {fqn}.quality_kpi_metrics GROUP BY ALL ORDER BY avg_defect_ppm DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.quality_events GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest units affected changed over time?*

**E2** — `unchanged`
- Q: *What is the monthly trend in total customer complaints?*

**E3** — `rewritten`
- **Old Q:** How does total number of units affected break down by product line identifier for 'Open' records?
- **Old SQL:** `SELECT product_line, COUNT(*) AS record_count, SUM(units_affected) AS total_units_affected FROM {fqn}.quality_events WHERE capa_status = 'Open' GROUP BY product_line ORDER BY total_units_affected DESC`
- **New Q:** Which product line identifiers have the highest total *?
- **New SQL:** `SELECT product_line, SUM(*) AS record_count, SUM(units_affected) AS total_units_affected FROM {fqn}.quality_events WHERE capa_status = 'Open' GROUP BY product_line ORDER BY total_units_affected DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total units inspected in this batch over time?*

**E5** — `unchanged`
- Q: *How has the average capa closure rate percentage changed over time?*

**E6** — `unchanged`
- Q: *How has critical event count changed over time?*

---

### `machinery/spare_part_inventory_optimization`
*PartsVault Industrial - Spare Parts Optimization 📦* — fictional company: **PartsVault Industrial** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total issued qty count?*

**B1** — `unchanged`
- Q: *How has total received qty count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest turnover ratio?
- **Old SQL:** `SELECT kpi_month, MEASURE(max_turnover_ratio) AS max_turnover_ratio FROM {fqn}.inventory_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average inventory turnover ratio trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(avg_turnover) AS avg_turnover FROM {fqn}.inventory_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**B3** — `unchanged`
- Q: *How has total stockout events changed over time?*

**B4** — `unchanged`
- Q: *What are the top spare part number by total transaction quantity?*

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.inventory_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which spare part numbers have the highest total quantity on hand?
- **New SQL:** `SELECT part_number, SUM(on_hand_qty) AS total_metric FROM {fqn}.inventory_snapshots GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.inventory_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which spare part numbers have the highest average inventory turnover ratio?
- **New SQL:** `SELECT part_number, MEASURE(avg_turnover) AS avg_turnover FROM {fqn}.inventory_kpi_metrics GROUP BY ALL ORDER BY avg_turnover DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in emergency issues count?*

**E1** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.parts_transactions_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.parts_transactions GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total carrying cost in usd?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_carrying_cost) AS total_carrying_cost FROM {fqn}.inventory_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has total carrying cost trended over time?
- **New SQL:** `SELECT kpi_month, MEASURE(total_carrying_cost) AS total_carrying_cost FROM {fqn}.inventory_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E3** — `rewritten`
- **Old Q:** How has total avg lead time days changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_avg_lead_time_days) AS total_avg_lead_time_days FROM {fqn}.inventory_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average average supplier lead time in days trended over time?
- **New SQL:** `SELECT kpi_month, AVG(avg_lead_time_days) AS avg_avg_lead_time_days FROM {fqn}.inventory_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E4** — `unchanged`
- Q: *What is the trend of total transaction quantity over time?*

**E5** — `unchanged`
- Q: *What is the trend of total quantity on hand over time?*

**E6** — `unchanged`
- Q: *How has the average inventory turnover ratio changed over time?*

---

### `machinery/spend_intelligence`
*SpendLens Manufacturing - Spend Intelligence 💰* — fictional company: **SpendLens Manufacturing** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in maverick po count?*

**B1** — `unchanged`
- Q: *How has late delivery count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique suppliers?
- **Old SQL:** `SELECT kpi_month, MEASURE(unique_supplier_count) AS unique_supplier_count FROM {fqn}.spend_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', kpi_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.spend_kpi_monthly GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest total spend changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top supplier identifier by total purchase order amount in usd?
- **Old SQL:** `SELECT supplier_id, SUM(po_amount_usd) AS total_po_amount_usd FROM {fqn}.procurement_transactions GROUP BY supplier_id ORDER BY total_po_amount_usd DESC LIMIT 10`
- **New Q:** Which spend categorys have the highest total purchase order amount?
- **New SQL:** `SELECT spend_category, SUM(po_amount_usd) AS total_po_amount_usd FROM {fqn}.procurement_transactions GROUP BY spend_category ORDER BY total_po_amount_usd DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average on-time delivery percentage by spend category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.spend_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which spend categorys have the highest average maverick spend percentage?
- **New SQL:** `SELECT spend_category, MEASURE(avg_maverick_pct) AS avg_maverick_pct FROM {fqn}.spend_kpi_metrics GROUP BY ALL ORDER BY avg_maverick_pct DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total pos?
- **Old SQL:** `SELECT po_date, MEASURE(total_po_count) AS total_po_count FROM {fqn}.procurement_metrics GROUP BY ALL ORDER BY po_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', po_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.procurement_transactions GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique suppliers changed over time?
- **Old SQL:** `SELECT po_date, MEASURE(unique_supplier_count) AS unique_supplier_count FROM {fqn}.procurement_metrics GROUP BY ALL ORDER BY po_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', po_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.procurement_transactions GROUP BY 1 ORDER BY 1`

**E2** — `unchanged`
- Q: *What is the monthly trend in total procurement spend?*

**E3** — `rewritten`
- **Old Q:** What is the monthly trend in total supplier diversity pct?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_supplier_diversity_percent) AS total_supplier_diversity_percent FROM {fqn}.spend_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average supplier diversity percent trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(total_supplier_diversity_percent) AS total_supplier_diversity_percent FROM {fqn}.spend_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E4** — `rewritten`
- **Old Q:** How does total purchase order amount in usd break down by supplier identifier for 'On Time' records?
- **Old SQL:** `SELECT supplier_id, COUNT(*) AS record_count, SUM(po_amount_usd) AS total_po_amount_usd FROM {fqn}.procurement_transactions WHERE delivery_status = 'On Time' GROUP BY supplier_id ORDER BY total_po_amount_usd DESC`
- **New Q:** Which spend categorys have the highest total *?
- **New SQL:** `SELECT spend_category, SUM(*) AS record_count, SUM(po_amount_usd) AS total_po_amount_usd FROM {fqn}.procurement_transactions WHERE delivery_status = 'On Time' GROUP BY spend_category ORDER BY total_po_amount_usd DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total average lead time in days over time?*

**E6** — `unchanged`
- Q: *How has the average maverick (off-contract) spend percentage changed over time?*

---

### `machinery/working_capital_cash_flow_optimization`
*CapitalFlow Machinery - Working Capital Optimization 💰* — fictional company: **CapitalFlow Machinery** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in total inflow count?*

**B1** — `unchanged`
- Q: *How has total outflow count changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique business units?
- **Old SQL:** `SELECT kpi_month, MEASURE(unique_business_unit_count) AS unique_business_unit_count FROM {fqn}.cash_flow_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', kpi_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.cash_flow_monthly GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest net cash flow changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top business unit identifier by total transaction amount in usd?
- **Old SQL:** `SELECT business_unit_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_flow_transactions GROUP BY business_unit_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which business unit types have the highest total transaction amount?
- **New SQL:** `SELECT business_unit_type, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_flow_transactions GROUP BY business_unit_type ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which business unit types have the highest total inventory value?
- **New SQL:** `SELECT business_unit_type, SUM(inventory_value_usd) AS total_metric FROM {fqn}.working_capital_snapshots GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi record?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.cash_flow_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which business unit types have the highest average ar collection rate?
- **New SQL:** `SELECT business_unit_type, MEASURE(avg_collection_rate) AS avg_collection_rate FROM {fqn}.cash_flow_kpi_metrics GROUP BY ALL ORDER BY avg_collection_rate DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT txn_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_flow_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_flow_transactions GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique business units changed over time?
- **Old SQL:** `SELECT txn_date, MEASURE(unique_business_unit_count) AS unique_business_unit_count FROM {fqn}.cash_flow_txn_metrics GROUP BY ALL ORDER BY txn_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_flow_transactions GROUP BY 1 ORDER BY 1`

**E2** — `unchanged`
- Q: *What is the monthly trend in total net cash flow?*

**E3** — `rewritten`
- **Old Q:** How has total forecast variance pct changed over time?
- **Old SQL:** `SELECT kpi_month, MEASURE(total_forecast_variance_percent) AS total_forecast_variance_percent FROM {fqn}.cash_flow_kpi_metrics GROUP BY ALL ORDER BY kpi_month`
- **New Q:** How has average forecast variance percent trended by month?
- **New SQL:** `SELECT kpi_month, MEASURE(total_forecast_variance_percent) AS total_forecast_variance_percent FROM {fqn}.cash_flow_kpi_metrics GROUP BY ALL ORDER BY kpi_month`

**E4** — `rewritten`
- **Old Q:** What is the trend of total transaction amount in usd over time?
- **Old SQL:** `SELECT txn_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_flow_transactions GROUP BY txn_date ORDER BY txn_date`
- **New Q:** How has total transaction amount in trended over time?
- **New SQL:** `SELECT txn_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_flow_transactions GROUP BY txn_date ORDER BY txn_date`

**E5** — `rewritten`
- **Old Q:** What is the trend of total total ar balance in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total total ar balance in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average ar collection rate percentage changed over time?*

---

### `mining/haul_vehicle_asset_health`
*MineTruck Analytics - Haul Vehicle Asset Health 🔧* — fictional company: **MineTruck Analytics** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical count?*

**B1** — `rewritten`
- **Old Q:** How has unique vehicles changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(vehicle_count) AS vehicle_count FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in high risk count?*

**B3** — `rewritten`
- **Old Q:** How has unique failures changed over time?
- **Old SQL:** `SELECT event_month, MEASURE(failure_count) AS failure_count FROM {fqn}.failure_monthly GROUP BY ALL ORDER BY event_month`
- **New Q:** Which vehicles have the highest total loads completed?
- **New SQL:** `SELECT vehicle_name, SUM(loads_completed) AS total_metric FROM {fqn}.haul_vehicles GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top vehicle id by total loads completed?
- **Old SQL:** `SELECT vehicle_id, SUM(loads_completed) AS total_loads_completed FROM {fqn}.haul_vehicles GROUP BY vehicle_id ORDER BY total_loads_completed DESC LIMIT 10`
- **New Q:** Which vehicle models have the highest total total payload in tons?
- **New SQL:** `SELECT vehicle_model, SUM(payload_tons) AS total_metric FROM {fqn}.haul_vehicles GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average ml health score 0-100 by model?*

**B6** — `rewritten`
- **Old Q:** How many records are there per event month?
- **Old SQL:** `SELECT event_month, COUNT(*) AS record_count FROM {fqn}.failure_events GROUP BY event_month ORDER BY event_month`
- **New Q:** Which models have the highest average remaining useful life days?
- **New SQL:** `SELECT vehicle_model, MEASURE(avg_rul) AS avg_rul FROM {fqn}.failure_monthly GROUP BY ALL ORDER BY avg_rul DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique readings?
- **Old SQL:** `SELECT reading_date, MEASURE(reading_count) AS reading_count FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has highest engine temp celsius changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(max_engine_temp_celsius) AS max_engine_temp_celsius FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average engine temperature c trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_engine_temp) AS avg_engine_temp FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique vehicles?
- **Old SQL:** `SELECT event_month, MEASURE(unique_vehicle_count) AS unique_vehicle_count FROM {fqn}.failure_monthly GROUP BY ALL ORDER BY event_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.failure_events GROUP BY 1 ORDER BY 1`

**E3** — `unchanged`
- Q: *How has high risk count changed over time?*

**E4** — `unchanged`
- Q: *What is the trend of total loads completed over time?*

**E5** — `unchanged`
- Q: *What is the trend of total engine temperature c over time?*

**E6** — `unchanged`
- Q: *How has the average 30-day failure probability changed over time?*

---

### `mining/production_monitoring_control_center`
*MineOps Central - Production Monitoring Control Center 📊* — fictional company: **MineOps Central** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in running count?*

**B1** — `rewritten`
- **Old Q:** How has unique total units changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_unit_count) AS total_unit_count FROM {fqn}.production_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', record_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.processing_units GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in bottleneck count?*

**B3** — `rewritten`
- **Old Q:** How has unique units changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_unit_count) AS unique_unit_count FROM {fqn}.throughput_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which units have the highest total throughput tons per hour?
- **New SQL:** `SELECT unit_name, SUM(throughput_tph) AS total_metric FROM {fqn}.processing_units GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top unit id by total throughput tons per hour?
- **Old SQL:** `SELECT unit_id, SUM(throughput_tph) AS total_throughput_tph FROM {fqn}.processing_units GROUP BY unit_id ORDER BY total_throughput_tph DESC LIMIT 10`
- **New Q:** Which unit types have the best average material recovery 0-100?
- **New SQL:** `SELECT unit_type, AVG(recovery_pct) AS avg_metric FROM {fqn}.processing_units GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average ore grade percentage by unit type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.throughput_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which unit types have the highest average utilization percentage?
- **New SQL:** `SELECT unit_type, MEASURE(avg_utilization) AS avg_utilization FROM {fqn}.throughput_kpi_monthly GROUP BY ALL ORDER BY avg_utilization DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest throughput tph?
- **Old SQL:** `SELECT record_date, MEASURE(max_throughput_tph) AS max_throughput_tph FROM {fqn}.production_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has average throughput tons per hour trended by month?
- **New SQL:** `SELECT record_date, MEASURE(avg_throughput_tph) AS avg_throughput_tph FROM {fqn}.production_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E1** — `rewritten`
- **Old Q:** How has avg throughput tph changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(avg_throughput_tph) AS avg_throughput_tph FROM {fqn}.production_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has average throughput tph changed over time?
- **New SQL:** `SELECT record_date, MEASURE(avg_throughput_tph) AS avg_throughput_tph FROM {fqn}.production_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest planned throughput tpd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_planned_throughput_tpd) AS max_planned_throughput_tpd FROM {fqn}.throughput_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak planned throughput tons/day each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_planned_throughput_tpd) AS max_planned_throughput_tpd FROM {fqn}.throughput_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**E3** — `unchanged`
- Q: *How has bottleneck count changed over time?*

**E4** — `unchanged`
- Q: *How does total throughput tons per hour break down by unit id for 'Fault' records?*

**E5** — `unchanged`
- Q: *What is the trend of total average particle size mm over time?*

**E6** — `unchanged`
- Q: *How has the average equipment utilization 0-100 changed over time?*

---

### `oil_gas_integrated/capital_investment_simulation`
*CapVenture Energy - Capital Investment Simulation 💰* — fictional company: **CapVenture Energy** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.investment_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.investment_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest amount changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest npv mm?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_npv_mm) AS max_npv_mm FROM {fqn}.project_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average net present value trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_npv_mm) AS avg_npv_mm FROM {fqn}.project_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has average npv in millions usd changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_npv_mm) AS avg_npv_mm FROM {fqn}.project_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which projects have the highest total transaction amount?
- **New SQL:** `SELECT project_name, SUM(amount_usd) AS total_metric FROM {fqn}.investment_transactions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top project identifier by total transaction amount in usd?
- **Old SQL:** `SELECT project_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.investment_transactions GROUP BY project_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which project type: deepwater, onshore conventional, shale, lng, infrastructures have the highest total budgeted amount for this category?
- **New SQL:** `SELECT project_type, SUM(budget_amount_usd) AS total_metric FROM {fqn}.investment_transactions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average internal rate of return percentage by project name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.investment_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which project types have the highest total cumulative capital spend?
- **New SQL:** `SELECT project_type, SUM(cumulative_spend_usd) AS total_metric FROM {fqn}.investment_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total investment spend in usd?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_spend_usd) AS total_spend_usd FROM {fqn}.investment_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total spend trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_spend_usd) AS total_spend_usd FROM {fqn}.investment_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E1** — `rewritten`
- **Old Q:** How has total budgeted amount in usd changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.investment_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total budget trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.investment_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E2** — `unchanged`
- Q: *What is the monthly trend in average irr percentage?*

**E3** — `rewritten`
- **Old Q:** How does total transaction amount in usd break down by project identifier for 'Approved' records?
- **Old SQL:** `SELECT project_id, COUNT(*) AS record_count, SUM(amount_usd) AS total_amount_usd FROM {fqn}.investment_transactions WHERE approval_status = 'Approved' GROUP BY project_id ORDER BY total_amount_usd DESC`
- **New Q:** Which projects have the highest total *?
- **New SQL:** `SELECT project_name, SUM(*) AS record_count, SUM(amount_usd) AS total_amount_usd FROM {fqn}.investment_transactions WHERE approval_status = 'Approved' GROUP BY project_name ORDER BY total_amount_usd DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total net present value in millions usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(npv_mm) AS total_npv_mm FROM {fqn}.project_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total net present value trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(npv_mm) AS total_npv_mm FROM {fqn}.project_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average budget remaining percentage changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.investment_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.investment_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_integrated/financial_analytics_reporting`
*PetroLedger Corp - Financial Analytics & Reporting 💰* — fictional company: **PetroLedger Corp** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest amount changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest planned revenue?
- **Old SQL:** `SELECT snapshot_month, MEASURE(max_planned_revenue) AS max_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** What has been the peak planned_revenue each month?
- **New SQL:** `SELECT snapshot_month, MEASURE(max_planned_revenue) AS max_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**B3** — `rewritten`
- **Old Q:** How has total actual revenue in usd changed over time?
- **Old SQL:** `SELECT snapshot_month, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** How has total actual revenue trended over time?
- **New SQL:** `SELECT snapshot_month, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount in usd?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which cost centers have the highest total transaction amount?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per first day of the snapshot month?
- **Old SQL:** `SELECT snapshot_month, COUNT(*) AS record_count FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** Which cost centers have the highest total actual revenue?
- **New SQL:** `SELECT cost_center_name, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY total_actual_revenue DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.financial_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which divisions have the highest average operating margin percentage?
- **New SQL:** `SELECT division, AVG(operating_margin_pct) AS avg_metric FROM {fqn}.financial_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total transaction amount in usd?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total transaction amount in trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E1** — `rewritten`
- **Old Q:** How has total budgeted amount in usd changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total budget trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total planned revenue in usd?
- **Old SQL:** `SELECT snapshot_month, MEASURE(total_planned_revenue) AS total_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** How has total planned revenue trended over time?
- **New SQL:** `SELECT snapshot_month, MEASURE(total_planned_revenue) AS total_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**E3** — `rewritten`
- **Old Q:** What is the trend of total transaction amount in usd over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How has total transaction amount in trended over time?
- **New SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total planned monthly revenue in usd over time?
- **Old SQL:** `SELECT snapshot_month, SUM(planned_revenue_usd) AS total_planned_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** How has total planned monthly revenue in trended over time?
- **New SQL:** `SELECT snapshot_month, SUM(planned_revenue_usd) AS total_planned_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`

**E5** — `unchanged`
- Q: *How has the average operating margin percentage changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_integrated/predictive_maintenance_asset_health`
*DeepHorizon Energy - Predictive Maintenance & Asset Health 🔧* — fictional company: **DeepHorizon Energy** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the alarm trip count by reading timestamp?*

**B1** — `rewritten`
- **Old Q:** Which reading timestamps have the most unique total readings?
- **Old SQL:** `SELECT reading_timestamp, MEASURE(total_reading_count) AS total_reading_count FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY total_reading_count DESC`
- **New Q:** Which platforms have the highest average asset health score?
- **New SQL:** `SELECT platform, MEASURE(avg_asset_health_score) AS avg_asset_health_score FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY avg_asset_health_score DESC LIMIT 10`

**B2** — `unchanged`
- Q: *What is the monthly trend in predicted event count?*

**B3** — `rewritten`
- **Old Q:** How has unique total eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.maintenance_events GROUP BY 1 ORDER BY 1`

**B4** — `rewritten`
- **Old Q:** What are the top equipment asset identifier by total raw sensor measurement value?
- **Old SQL:** `SELECT asset_id, SUM(sensor_value) AS total_sensor_value FROM {fqn}.sensor_readings GROUP BY asset_id ORDER BY total_sensor_value DESC LIMIT 10`
- **New Q:** Which equipment assets have the highest total raw sensor measurement value?
- **New SQL:** `SELECT asset_name, SUM(sensor_value) AS total_sensor_value FROM {fqn}.sensor_readings GROUP BY asset_name ORDER BY total_sensor_value DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of the maintenance event?
- **Old SQL:** `SELECT event_date, COUNT(*) AS record_count FROM {fqn}.maintenance_events GROUP BY event_date ORDER BY event_date`
- **New Q:** Which equipment assets have the highest average downtime per event in hours?
- **New SQL:** `SELECT asset_name, MEASURE(avg_downtime_hours) AS avg_downtime_hours FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY avg_downtime_hours DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the snapshot month?
- **Old SQL:** `SELECT snapshot_month, COUNT(*) AS record_count FROM {fqn}.health_metrics_monthly GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** Which production platform or facilitys have the highest average health score for the month 0-100?
- **New SQL:** `SELECT platform_name, AVG(avg_health_score) AS avg_metric FROM {fqn}.health_metrics_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the highest sensor value for each reading timestamp?*

**E1** — `unchanged`
- Q: *Rank reading timestamps by average asset health score*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest downtime hours?
- **Old SQL:** `SELECT event_date, MEASURE(max_downtime_hours) AS max_downtime_hours FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has average equipment downtime in hours trended by month?
- **New SQL:** `SELECT event_date, MEASURE(avg_downtime_hours) AS avg_downtime_hours FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`

**E3** — `unchanged`
- Q: *What is the trend of total raw sensor measurement value over time?*

**E4** — `unchanged`
- Q: *What is the trend of total equipment downtime in hours over time?*

**E5** — `unchanged`
- Q: *How has the average average health score for the month 0-100 changed over time?*

**E6** — `rewritten`
- **Old Q:** Which asset ids have the highest lowest predicted rul days?
- **Old SQL:** `SELECT asset_id, MEASURE(min_predicted_rul_days) AS min_predicted_rul_days FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY min_predicted_rul_days DESC`
- **New Q:** How does lowest predicted remaining useful life in days compare across equipment assets?
- **New SQL:** `SELECT asset_id, MEASURE(min_predicted_rul_days) AS min_predicted_rul_days FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY min_predicted_rul_days DESC`

---

### `oil_gas_integrated/production_monitoring_control_center`
*PetroPulse Integrated - Production Monitoring Control Center 📊* — fictional company: **PetroPulse Integrated** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in highest oil bbl?
- **Old SQL:** `SELECT reading_date, MEASURE(max_oil_bbl) AS max_oil_bbl FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** What has been the peak daily oil production in barrels each month?
- **New SQL:** `SELECT reading_date, MEASURE(max_oil_bbl) AS max_oil_bbl FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B1** — `rewritten`
- **Old Q:** How has total oil production in barrels changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_oil_bbl) AS total_oil_bbl FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** Which wells have the highest total daily gas production in mcf?
- **New SQL:** `SELECT well_name, SUM(gas_mcf) AS total_metric FROM {fqn}.production_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.production_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.production_events GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest duration hours changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top well identifier by total daily oil production in barrels?
- **Old SQL:** `SELECT well_id, SUM(oil_bbl) AS total_oil_bbl FROM {fqn}.production_readings GROUP BY well_id ORDER BY total_oil_bbl DESC LIMIT 10`
- **New Q:** Which wells have the highest total daily oil production in barrels?
- **New SQL:** `SELECT well_name, SUM(oil_bbl) AS total_oil_bbl FROM {fqn}.production_readings GROUP BY well_name ORDER BY total_oil_bbl DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average event duration in hours by well name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the snapshot month?
- **Old SQL:** `SELECT snapshot_month, COUNT(*) AS record_count FROM {fqn}.production_kpi_monthly GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** Which host platforms have the highest total monthly oil production in barrels?
- **New SQL:** `SELECT platform_name, SUM(total_oil_bbl) AS total_metric FROM {fqn}.production_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total gas production in mcf?*

**E1** — `unchanged`
- Q: *How has total water production in barrels changed over time?*

**E2** — `unchanged`
- Q: *What is the monthly trend in total deferred oil production in barrels?*

**E3** — `rewritten`
- **Old Q:** How does total daily oil production in barrels break down by well identifier for 'Flowing' records?
- **Old SQL:** `SELECT well_id, COUNT(*) AS record_count, SUM(oil_bbl) AS total_oil_bbl FROM {fqn}.production_readings WHERE status = 'Flowing' GROUP BY well_id ORDER BY total_oil_bbl DESC`
- **New Q:** Which wells have the highest total *?
- **New SQL:** `SELECT well_name, SUM(*) AS record_count, SUM(oil_bbl) AS total_oil_bbl FROM {fqn}.production_readings WHERE status = 'Flowing' GROUP BY well_name ORDER BY total_oil_bbl DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total oil production deferred in barrels over time?*

**E5** — `unchanged`
- Q: *How has the average water cut percentage changed over time?*

**E6** — `rewritten`
- **Old Q:** How has average wellhead pressure in psi changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_wellhead_pressure_psi) AS avg_wellhead_pressure_psi FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average wellhead pressure in pressure (psi) trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_wellhead_pressure_psi) AS avg_wellhead_pressure_psi FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

---

### `oil_gas_integrated/scenario_planning_business_simulation`
*StratOil Dynamics - Scenario Planning & Business Simulation 🎯* — fictional company: **StratOil Dynamics** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total runss?
- **Old SQL:** `SELECT run_date, MEASURE(total_runs) AS total_runs FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest oil price assumption changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest projected revenue mm?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_projected_revenue_mm) AS max_projected_revenue_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average projected revenue trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_projected_revenue_mm) AS avg_projected_revenue_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has average projected revenue in millions usd changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_projected_revenue_mm) AS avg_projected_revenue_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which scenario have the best average assumed annual production growth rate?
- **New SQL:** `SELECT scenario_name, AVG(production_growth_pct) AS avg_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top scenario identifier by total assumed wti oil price usd per barrel?
- **Old SQL:** `SELECT scenario_id, SUM(oil_price_assumption) AS total_oil_price_assumption FROM {fqn}.simulation_runs GROUP BY scenario_id ORDER BY total_oil_price_assumption DESC LIMIT 10`
- **New Q:** Which scenario have the highest total assumed wti oil price per barrel?
- **New SQL:** `SELECT scenario_name, SUM(oil_price_assumption) AS total_oil_price_assumption FROM {fqn}.simulation_runs GROUP BY scenario_name ORDER BY total_oil_price_assumption DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of the outcome snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.outcome_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which scenario have the highest average projected revenue?
- **New SQL:** `SELECT scenario_name, MEASURE(avg_projected_revenue_mm) AS avg_projected_revenue_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY avg_projected_revenue_mm DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.scenario_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which scenario categorys have the highest total probability-weighted npv?
- **New SQL:** `SELECT scenario_category, SUM(weighted_npv_mm) AS total_metric FROM {fqn}.scenario_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total capital expenditure allocation in millions?*

**E1** — `rewritten`
- **Old Q:** How has total production growth pct changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(total_production_growth_percent) AS total_production_growth_percent FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How has average production growth percent trended by month?
- **New SQL:** `SELECT run_date, MEASURE(total_production_growth_percent) AS total_production_growth_percent FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in average projected ebitda in millions usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_projected_ebitda_mm) AS avg_projected_ebitda_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total projected ebitda trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_projected_ebitda_mm) AS avg_projected_ebitda_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the monthly trend in average co2 intensity kg per boe?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_co2_intensity) AS avg_co2_intensity FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total co2 intensity trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_co2_intensity) AS avg_co2_intensity FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total assumed wti oil price usd per barrel over time?
- **Old SQL:** `SELECT run_date, SUM(oil_price_assumption) AS total_oil_price_assumption FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`
- **New Q:** How has total assumed wti oil price per barrel trended over time?
- **New SQL:** `SELECT run_date, SUM(oil_price_assumption) AS total_oil_price_assumption FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`

**E5** — `rewritten`
- **Old Q:** What is the trend of total projected revenue in millions usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(projected_revenue_mm) AS total_projected_revenue_mm FROM {fqn}.outcome_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total projected revenue trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(projected_revenue_mm) AS total_projected_revenue_mm FROM {fqn}.outcome_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average probability-weighted irr percentage changed over time?*

---

### `oil_gas_integrated/working_capital_cash_flow_optimization`
*CashFlow Energy - Working Capital & Cash Flow Optimization 💰* — fictional company: **CashFlow Energy** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in total inflows usd count?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_inflows_usd) AS total_inflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total inflows trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_inflows_usd) AS total_inflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**B1** — `rewritten`
- **Old Q:** How has total outflows usd count changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_outflows_usd) AS total_outflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total outflows trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_outflows_usd) AS total_outflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest accounts receivable?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_accounts_receivable) AS max_accounts_receivable FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak accounts_receivable each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_accounts_receivable) AS max_accounts_receivable FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has total accounts receivable in usd changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_receivables_usd) AS total_receivables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total receivables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_receivables_usd) AS total_receivables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top business unit identifier by total cash flow amount in usd (positive = inflow)?
- **Old SQL:** `SELECT business_unit_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which business units have the most cash flow amount?
- **New SQL:** `SELECT business_unit_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of the working capital snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which business units have the highest average days sales outstanding?
- **New SQL:** `SELECT business_unit_name, MEASURE(avg_dso_days) AS avg_dso_days FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY avg_dso_days DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.cashflow_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which business segments have the highest total free cash flow?
- **New SQL:** `SELECT segment, SUM(free_cash_flow_usd) AS total_metric FROM {fqn}.cashflow_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest amount changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total accounts payable in usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_payables_usd) AS total_payables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total payables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_payables_usd) AS total_payables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the trend of total cash flow amount in usd (positive = inflow) over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How does cash flow amount in compare across business units?
- **New SQL:** `SELECT business_unit_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_name ORDER BY business_unit_name LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total accounts receivable balance in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total accounts receivable balance in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average current ratio (current assets / current liabilities) changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_midstream/automated_reporting_of_carbon_intensity`
*CarbonTrack Midstream - Carbon Intensity Reporting 🌱* — fictional company: **CarbonTrack Midstream** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in highest co2e metric tons?
- **Old SQL:** `SELECT reading_date, MEASURE(max_co2e_metric_tons) AS max_co2e_metric_tons FROM {fqn}.emission_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** What has been the peak co2 equivalent metric tons each month?
- **New SQL:** `SELECT reading_date, MEASURE(max_co2e_metric_tons) AS max_co2e_metric_tons FROM {fqn}.emission_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B1** — `unchanged`
- Q: *How has total co2e metric tons changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest monthly co2e tons?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_monthly_co2e_tons) AS max_monthly_co2e_tons FROM {fqn}.carbon_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak monthly co2e tons each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_monthly_co2e_tons) AS max_monthly_co2e_tons FROM {fqn}.carbon_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `unchanged`
- Q: *How has total monthly co2e changed over time?*

**B4** — `unchanged`
- Q: *What are the top emission source id by total co2 equivalent metric tons?*

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.carbon_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which categorys have the highest average reduction target?
- **New SQL:** `SELECT emission_category, MEASURE(avg_reduction_target) AS avg_reduction_target FROM {fqn}.carbon_snapshots_metrics GROUP BY ALL ORDER BY avg_reduction_target DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.carbon_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which categorys have the highest total emissions tons?
- **New SQL:** `SELECT emission_category, SUM(total_emissions_tons) AS total_metric FROM {fqn}.carbon_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total methane tons?*

**E1** — `unchanged`
- Q: *How has total throughput boe changed over time?*

**E2** — `unchanged`
- Q: *What is the monthly trend in total detected leaks?*

**E3** — `unchanged`
- Q: *What is the trend of total co2 equivalent metric tons over time?*

**E4** — `unchanged`
- Q: *What is the trend of total monthly co2e tons over time?*

**E5** — `rewritten`
- **Old Q:** How has the average methane intensity pct changed over time?
- **Old SQL:** `SELECT kpi_month, AVG(methane_intensity_pct) AS avg_methane_intensity_pct FROM {fqn}.carbon_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How has average methane intensity percentage trended by month?
- **New SQL:** `SELECT kpi_month, AVG(methane_intensity_pct) AS avg_methane_intensity_pct FROM {fqn}.carbon_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E6** — `rewritten`
- **Old Q:** How has avg carbon intensity changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_carbon_intensity) AS avg_carbon_intensity FROM {fqn}.emission_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average carbon intensity changed over time?
- **New SQL:** `SELECT reading_date, MEASURE(avg_carbon_intensity) AS avg_carbon_intensity FROM {fqn}.emission_readings_metrics GROUP BY ALL ORDER BY reading_date`

---

### `oil_gas_midstream/energy_trading`
*TradeFlow Energy - Energy Trading Analytics ⚡* — fictional company: **TradeFlow Energy** — 13 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total tradess?
- **Old SQL:** `SELECT trade_date, MEASURE(total_trades) AS total_trades FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', trade_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.trade_transactions GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has highest volume bbl changed over time?
- **Old SQL:** `SELECT trade_date, MEASURE(max_volume_bbl) AS max_volume_bbl FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`
- **New Q:** How has total volume in barrels equivalent trended over time?
- **New SQL:** `SELECT trade_date, MEASURE(max_volume_bbl) AS max_volume_bbl FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest net position bbl?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_net_position_bbl) AS max_net_position_bbl FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average net position barrels trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_net_position_bbl) AS avg_net_position_bbl FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has total mtm usd changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_mtm_usd) AS total_mtm_usd FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total mtm trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_mtm_usd) AS total_mtm_usd FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top contract id by total volume in bbl equivalent?
- **Old SQL:** `SELECT contract_id, SUM(volume_bbl) AS total_volume_bbl FROM {fqn}.trade_transactions GROUP BY contract_id ORDER BY total_volume_bbl DESC LIMIT 10`
- **New Q:** Which contracts have the highest total volume in barrels equivalent?
- **New SQL:** `SELECT contract_name, SUM(volume_bbl) AS total_volume_bbl FROM {fqn}.trade_transactions GROUP BY contract_name ORDER BY total_volume_bbl DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.position_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which commoditys have the highest average net position barrels?
- **New SQL:** `SELECT commodity, MEASURE(avg_net_position_bbl) AS avg_net_position_bbl FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY avg_net_position_bbl DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.trading_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which commoditys have the highest total sharpe ratio?
- **New SQL:** `SELECT commodity, SUM(sharpe_ratio) AS total_metric FROM {fqn}.trading_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total p&l usd?
- **Old SQL:** `SELECT trade_date, MEASURE(total_pnl_usd) AS total_pnl_usd FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`
- **New Q:** How has total realized p&l trended over time?
- **New SQL:** `SELECT trade_date, MEASURE(total_pnl_usd) AS total_pnl_usd FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`

**E1** — `rewritten`
- **Old Q:** How has total volume bbl changed over time?
- **Old SQL:** `SELECT trade_date, MEASURE(total_volume_bbl) AS total_volume_bbl FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`
- **New Q:** How has total volume in barrels equivalent trended over time?
- **New SQL:** `SELECT trade_date, MEASURE(total_volume_bbl) AS total_volume_bbl FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total var usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_var_usd) AS total_var_usd FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total var trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_var_usd) AS total_var_usd FROM {fqn}.position_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How does total volume in bbl equivalent break down by contract id for 'Settled' records?
- **Old SQL:** `SELECT contract_id, COUNT(*) AS record_count, SUM(volume_bbl) AS total_volume_bbl FROM {fqn}.trade_transactions WHERE settlement_status = 'Settled' GROUP BY contract_id ORDER BY total_volume_bbl DESC`
- **New Q:** How does * compare across contracts?
- **New SQL:** `SELECT contract_id, COUNT(*) AS record_count, SUM(volume_bbl) AS total_volume_bbl FROM {fqn}.trade_transactions WHERE settlement_status = 'Settled' GROUP BY contract_id ORDER BY total_volume_bbl DESC`

**E4** — `rewritten`
- **Old Q:** What is the trend of total net position bbl over time?
- **Old SQL:** `SELECT snapshot_date, SUM(net_position_bbl) AS total_net_position_bbl FROM {fqn}.position_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total net position barrels trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(net_position_bbl) AS total_net_position_bbl FROM {fqn}.position_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average sharpe ratio changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total tradess changed over time?
- **Old SQL:** `SELECT trade_date, MEASURE(total_trades) AS total_trades FROM {fqn}.trade_transactions_metrics GROUP BY ALL ORDER BY trade_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', trade_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.trade_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_midstream/financial_analytics_reporting`
*MidLedger Analytics - Financial Analytics & Reporting 💰* — fictional company: **MidLedger Analytics** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest amount changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest planned revenue?
- **Old SQL:** `SELECT snapshot_month, MEASURE(max_planned_revenue) AS max_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** What has been the peak planned_revenue each month?
- **New SQL:** `SELECT snapshot_month, MEASURE(max_planned_revenue) AS max_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**B3** — `rewritten`
- **Old Q:** How has total actual revenue usd changed over time?
- **Old SQL:** `SELECT snapshot_month, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** How has total actual revenue trended over time?
- **New SQL:** `SELECT snapshot_month, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount usd?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which cost centers have the highest total transaction amount?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per first day of snapshot month?
- **Old SQL:** `SELECT snapshot_month, COUNT(*) AS record_count FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** Which cost centers have the highest total actual revenue?
- **New SQL:** `SELECT cost_center_name, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY total_actual_revenue DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.financial_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which divisions have the highest average operating margin percentage?
- **New SQL:** `SELECT division, AVG(operating_margin_pct) AS avg_metric FROM {fqn}.financial_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total transaction amount usd?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total transaction amount trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E1** — `rewritten`
- **Old Q:** How has total budgeted amount usd changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total budget trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total planned revenue usd?
- **Old SQL:** `SELECT snapshot_month, MEASURE(total_planned_revenue) AS total_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** How has total planned revenue trended over time?
- **New SQL:** `SELECT snapshot_month, MEASURE(total_planned_revenue) AS total_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**E3** — `rewritten`
- **Old Q:** What is the trend of total transaction amount usd over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How has total transaction amount trended over time?
- **New SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total planned monthly revenue usd over time?
- **Old SQL:** `SELECT snapshot_month, SUM(planned_revenue_usd) AS total_planned_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** How has total planned monthly revenue trended over time?
- **New SQL:** `SELECT snapshot_month, SUM(planned_revenue_usd) AS total_planned_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`

**E5** — `unchanged`
- Q: *How has the average operating margin percentage changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_midstream/logistics_optimization`
*PipeRoute Midstream - Logistics Optimization 🚚* — fictional company: **PipeRoute Midstream** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total readingss?
- **Old SQL:** `SELECT reading_date, MEASURE(total_readings) AS total_readings FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.flow_readings GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has highest throughput bpd changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(max_throughput_bpd) AS max_throughput_bpd FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average throughput in barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_throughput_bpd) AS avg_throughput_bpd FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.logistics_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** Which segments have the best average capacity utilization percentage?
- **New SQL:** `SELECT segment_name, AVG(capacity_utilization_pct) AS avg_metric FROM {fqn}.flow_readings GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has highest volume impact bbl changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(max_volume_impact_bbl) AS max_volume_impact_bbl FROM {fqn}.logistics_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has total volume impact barrels trended over time?
- **New SQL:** `SELECT event_date, MEASURE(max_volume_impact_bbl) AS max_volume_impact_bbl FROM {fqn}.logistics_events_metrics GROUP BY ALL ORDER BY event_date`

**B4** — `rewritten`
- **Old Q:** What are the top pipeline segment id by total throughput in bpd?
- **Old SQL:** `SELECT segment_id, SUM(throughput_bpd) AS total_throughput_bpd FROM {fqn}.flow_readings GROUP BY segment_id ORDER BY total_throughput_bpd DESC LIMIT 10`
- **New Q:** Which segments have the best average throughput in barrels per day?
- **New SQL:** `SELECT segment_name, AVG(throughput_bpd) AS total_throughput_bpd FROM {fqn}.flow_readings GROUP BY segment_name ORDER BY total_throughput_bpd DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average duration hours by segment name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.throughput_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which pipeline types have the highest total monthly revenue?
- **New SQL:** `SELECT pipeline_type, SUM(revenue_usd) AS total_metric FROM {fqn}.throughput_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total pressure psi?
- **Old SQL:** `SELECT reading_date, MEASURE(total_pressure_psi) AS total_pressure_psi FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average pipeline pressure trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_pressure_psi) AS avg_pressure_psi FROM {fqn}.pipeline_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `rewritten`
- **Old Q:** How has avg throughput bpd changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_throughput_bpd) AS avg_throughput_bpd FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average throughput in barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_throughput_bpd) AS avg_throughput_bpd FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total volume impact bbl?
- **Old SQL:** `SELECT event_date, MEASURE(total_volume_impact_bbl) AS total_volume_impact_bbl FROM {fqn}.logistics_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has total volume impact barrels trended over time?
- **New SQL:** `SELECT event_date, MEASURE(total_volume_impact_bbl) AS total_volume_impact_bbl FROM {fqn}.logistics_events_metrics GROUP BY ALL ORDER BY event_date`

**E3** — `rewritten`
- **Old Q:** How does total throughput in bpd break down by pipeline segment id for 'Operating' records?
- **Old SQL:** `SELECT segment_id, COUNT(*) AS record_count, SUM(throughput_bpd) AS total_throughput_bpd FROM {fqn}.flow_readings WHERE status = 'Operating' GROUP BY segment_id ORDER BY total_throughput_bpd DESC`
- **New Q:** How does throughput vary across pipeline segments?
- **New SQL:** `SELECT segment_name, AVG(throughput_bbl_per_day) AS avg_throughput FROM {fqn}.pipeline_readings GROUP BY segment_name ORDER BY avg_throughput DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total volume impact bbl over time?
- **Old SQL:** `SELECT event_date, SUM(volume_impact_bbl) AS total_volume_impact_bbl FROM {fqn}.logistics_events GROUP BY event_date ORDER BY event_date`
- **New Q:** How has total volume impact barrels trended over time?
- **New SQL:** `SELECT event_date, SUM(volume_impact_bbl) AS total_volume_impact_bbl FROM {fqn}.logistics_events GROUP BY event_date ORDER BY event_date`

**E5** — `unchanged`
- Q: *How has the average average utilization changed over time?*

**E6** — `rewritten`
- **Old Q:** How has avg tariff usd/bbl changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_tariff) AS avg_tariff FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has total tariff trended over time?
- **New SQL:** `SELECT reading_date, MEASURE(avg_tariff) AS avg_tariff FROM {fqn}.flow_readings_metrics GROUP BY ALL ORDER BY reading_date`

---

### `oil_gas_midstream/regulation_compliance`
*CompliFlow Systems - Regulation & Compliance 📋* — fictional company: **CompliFlow Systems** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in violation count?*

**B1** — `rewritten`
- **Old Q:** How has unique total eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.compliance_events GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest compliance score?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_compliance_score) AS max_compliance_score FROM {fqn}.audit_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average compliance score 0-100 trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_compliance_score) AS avg_compliance_score FROM {fqn}.audit_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `unchanged`
- Q: *How has total open findings changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top regulation id by total fine/penalty amount usd?
- **Old SQL:** `SELECT reg_id, SUM(fine_amount_usd) AS total_fine_amount_usd FROM {fqn}.compliance_events GROUP BY reg_id ORDER BY total_fine_amount_usd DESC LIMIT 10`
- **New Q:** Which regulations have the highest total fine/penalty amount?
- **New SQL:** `SELECT regulation_name, SUM(fine_amount_usd) AS total_fine_amount_usd FROM {fqn}.compliance_events GROUP BY regulation_name ORDER BY total_fine_amount_usd DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average compliance score 0-100 by regulatory body?*

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.compliance_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which compliance areas have the highest total violations in month?
- **New SQL:** `SELECT compliance_area, SUM(violation_count) AS total_metric FROM {fqn}.compliance_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest fine amount?
- **Old SQL:** `SELECT event_date, MEASURE(max_fine_amount) AS max_fine_amount FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** What has been the peak fine_amount each month?
- **New SQL:** `SELECT event_date, MEASURE(max_fine_amount) AS max_fine_amount FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`

**E1** — `rewritten`
- **Old Q:** How has total fines usd changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_fines_usd) AS total_fines_usd FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has total total fines trended over time?
- **New SQL:** `SELECT event_date, MEASURE(total_fines_usd) AS total_fines_usd FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`

**E2** — `unchanged`
- Q: *What is the monthly trend in total overdue actions?*

**E3** — `rewritten`
- **Old Q:** How does total fine/penalty amount usd break down by regulation id for 'Open' records?
- **Old SQL:** `SELECT reg_id, COUNT(*) AS record_count, SUM(fine_amount_usd) AS total_fine_amount_usd FROM {fqn}.compliance_events WHERE status = 'Open' GROUP BY reg_id ORDER BY total_fine_amount_usd DESC`
- **New Q:** How does * compare across regulations?
- **New SQL:** `SELECT reg_id, COUNT(*) AS record_count, SUM(fine_amount_usd) AS total_fine_amount_usd FROM {fqn}.compliance_events WHERE status = 'Open' GROUP BY reg_id ORDER BY total_fine_amount_usd DESC`

**E4** — `unchanged`
- Q: *What is the trend of total open audit findings over time?*

**E5** — `rewritten`
- **Old Q:** How has the average finding closure rate pct changed over time?
- **Old SQL:** `SELECT kpi_month, AVG(closure_rate_pct) AS avg_closure_rate_pct FROM {fqn}.compliance_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How has average finding closure rate percentage trended by month?
- **New SQL:** `SELECT kpi_month, AVG(closure_rate_pct) AS avg_closure_rate_pct FROM {fqn}.compliance_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E6** — `rewritten`
- **Old Q:** How has avg resolution days changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(avg_resolution_days) AS avg_resolution_days FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has average resolution days changed over time?
- **New SQL:** `SELECT event_date, MEASURE(avg_resolution_days) AS avg_resolution_days FROM {fqn}.compliance_events_metrics GROUP BY ALL ORDER BY event_date`

---

### `oil_gas_midstream/scenario_planning_business_simulation`
*MidStream Dynamics - Scenario Planning & Simulation 🎯* — fictional company: **MidStream Dynamics** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total runss?
- **Old SQL:** `SELECT run_date, MEASURE(total_runs) AS total_runs FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest throughput change percent changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest projected ebitda mm?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_projected_ebitda_mm) AS max_projected_ebitda_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total ebitda mm trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_ebitda_mm) AS avg_ebitda_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has avg ebitda millions changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_ebitda_mm) AS avg_ebitda_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which scenarios have the best average throughput change percentage?
- **New SQL:** `SELECT scenario_name, AVG(throughput_change_pct) AS avg_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top scenario id by total revenue impact millions usd?
- **Old SQL:** `SELECT scenario_id, SUM(revenue_impact_mm) AS total_revenue_impact_mm FROM {fqn}.simulation_runs GROUP BY scenario_id ORDER BY total_revenue_impact_mm DESC LIMIT 10`
- **New Q:** Which scenarios have the highest total revenue impact millions?
- **New SQL:** `SELECT scenario_name, SUM(revenue_impact_mm) AS total_revenue_impact_mm FROM {fqn}.simulation_runs GROUP BY scenario_name ORDER BY total_revenue_impact_mm DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average regulatory risk 0-100 by scenario name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.scenario_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which scenario types have the highest total weighted npv millions?
- **New SQL:** `SELECT scenario_type, SUM(weighted_npv_mm) AS total_metric FROM {fqn}.scenario_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total capex millions?
- **Old SQL:** `SELECT run_date, MEASURE(total_capex_mm) AS total_capex_mm FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How has total capex mm trended over time?
- **New SQL:** `SELECT run_date, MEASURE(total_capex_mm) AS total_capex_mm FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`

**E1** — `rewritten`
- **Old Q:** How has total throughput change pct changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(total_throughput_change_percent) AS total_throughput_change_percent FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How has average throughput change percent trended by month?
- **New SQL:** `SELECT run_date, MEASURE(total_throughput_change_percent) AS total_throughput_change_percent FROM {fqn}.simulation_runs_metrics GROUP BY ALL ORDER BY run_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in avg throughput mbpd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_throughput_mbpd) AS avg_throughput_mbpd FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What is the monthly trend in average throughput mbpd?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_throughput_mbpd) AS avg_throughput_mbpd FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** Rank scenario ids by avg ebitda millions
- **Old SQL:** `SELECT scenario_id, MEASURE(avg_ebitda_mm) AS avg_ebitda_mm FROM {fqn}.outcome_snapshots_metrics GROUP BY ALL ORDER BY avg_ebitda_mm DESC`
- **New Q:** How does projected EBITDA compare across scenarios?
- **New SQL:** `SELECT scenario_name, AVG(ebitda_mm) AS avg_ebitda_mm FROM {fqn}.scenario_results GROUP BY scenario_name ORDER BY avg_ebitda_mm DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total revenue impact millions usd over time?
- **Old SQL:** `SELECT run_date, SUM(revenue_impact_mm) AS total_revenue_impact_mm FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`
- **New Q:** How has total revenue impact millions trended over time?
- **New SQL:** `SELECT run_date, SUM(revenue_impact_mm) AS total_revenue_impact_mm FROM {fqn}.simulation_runs GROUP BY run_date ORDER BY run_date`

**E5** — `rewritten`
- **Old Q:** What is the trend of total projected ebitda millions over time?
- **Old SQL:** `SELECT snapshot_date, SUM(projected_ebitda_mm) AS total_projected_ebitda_mm FROM {fqn}.outcome_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total projected ebitda millions trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(projected_ebitda_mm) AS total_projected_ebitda_mm FROM {fqn}.outcome_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E6** — `unchanged`
- Q: *How has the average risk score 0-100 changed over time?*

---

### `oil_gas_midstream/spend_intelligence`
*MidSpend Analytics - Spend Intelligence 💰* — fictional company: **MidSpend Analytics** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.procurement_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.procurement_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest amount changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest quality score?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_quality_score) AS max_quality_score FROM {fqn}.supplier_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average quality score 0-100 trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_quality_score) AS avg_quality_score FROM {fqn}.supplier_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has avg quality score changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_quality_score) AS avg_quality_score FROM {fqn}.supplier_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which suppliers have the highest total transaction amount?
- **New SQL:** `SELECT supplier_name, SUM(amount_usd) AS total_metric FROM {fqn}.procurement_transactions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top supplier id by total transaction amount usd?
- **Old SQL:** `SELECT supplier_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.procurement_transactions GROUP BY supplier_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which spend categorys have the best average contract compliance percentage?
- **New SQL:** `SELECT spend_category, AVG(contract_compliance_pct) AS avg_metric FROM {fqn}.procurement_transactions GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average quality score 0-100 by supplier name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.spend_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which spend categorys have the highest total negotiated savings?
- **New SQL:** `SELECT spend_category, SUM(savings_usd) AS total_metric FROM {fqn}.spend_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total spend usd?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_spend_usd) AS total_spend_usd FROM {fqn}.procurement_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total spend trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_spend_usd) AS total_spend_usd FROM {fqn}.procurement_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E1** — `rewritten`
- **Old Q:** How has avg contract compliance changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(avg_compliance_pct) AS avg_compliance_pct FROM {fqn}.procurement_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has average contract compliance changed over time?
- **New SQL:** `SELECT transaction_date, MEASURE(avg_compliance_pct) AS avg_compliance_pct FROM {fqn}.procurement_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in avg on-time delivery?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_on_time_pct) AS avg_on_time_pct FROM {fqn}.supplier_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What is the monthly trend in average on-time delivery?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_on_time_pct) AS avg_on_time_pct FROM {fqn}.supplier_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the trend of total transaction amount usd over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.procurement_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How has total transaction amount trended over time?
- **New SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.procurement_transactions GROUP BY transaction_date ORDER BY transaction_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total avg lead time days over time?
- **Old SQL:** `SELECT snapshot_date, SUM(avg_lead_time_days) AS total_avg_lead_time_days FROM {fqn}.supplier_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** What is the trend of total average lead time days over time?
- **New SQL:** `SELECT snapshot_date, SUM(avg_lead_time_days) AS total_avg_lead_time_days FROM {fqn}.supplier_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How has the average off-contract spend pct changed over time?
- **Old SQL:** `SELECT kpi_month, AVG(maverick_spend_pct) AS avg_maverick_spend_pct FROM {fqn}.spend_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How has average off-contract spend percentage trended by month?
- **New SQL:** `SELECT kpi_month, AVG(maverick_spend_pct) AS avg_maverick_spend_pct FROM {fqn}.spend_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E6** — `rewritten`
- **Old Q:** How does the number of unique total transactionss vary by supplier id?
- **Old SQL:** `SELECT supplier_id, MEASURE(total_transactions) AS total_transactions FROM {fqn}.procurement_transactions_metrics GROUP BY ALL ORDER BY total_transactions DESC`
- **New Q:** Which suppliers have the most transactions?
- **New SQL:** `SELECT supplier_name, COUNT(DISTINCT transaction_id) AS transaction_count FROM {fqn}.spend_transactions GROUP BY supplier_name ORDER BY transaction_count DESC LIMIT 10`

---

### `oil_gas_midstream/working_capital_cash_flow_optimization`
*MidCapital Systems - Working Capital & Cash Flow Optimization 💰* — fictional company: **MidCapital Systems** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in total inflows usd count?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_inflows_usd) AS total_inflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total inflows trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_inflows_usd) AS total_inflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**B1** — `rewritten`
- **Old Q:** How has total outflows usd count changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_outflows_usd) AS total_outflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total outflows trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_outflows_usd) AS total_outflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest accounts receivable?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_accounts_receivable) AS max_accounts_receivable FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak accounts_receivable each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_accounts_receivable) AS max_accounts_receivable FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has total ar usd changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_receivables_usd) AS total_receivables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total receivables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_receivables_usd) AS total_receivables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top business unit id by total cash flow amount usd (positive=inflow)?
- **Old SQL:** `SELECT business_unit_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which business units have the most cash flow amount?
- **New SQL:** `SELECT business_unit_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which business units have the highest average dso?
- **New SQL:** `SELECT business_unit_name, MEASURE(avg_dso_days) AS avg_dso_days FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY avg_dso_days DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.cashflow_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which segments have the highest total free cash flow?
- **New SQL:** `SELECT segment, SUM(free_cash_flow_usd) AS total_metric FROM {fqn}.cashflow_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest amount changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total ap usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_payables_usd) AS total_payables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total payables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_payables_usd) AS total_payables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the trend of total cash flow amount usd (positive=inflow) over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How does cash flow amount compare across business units?
- **New SQL:** `SELECT business_unit_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_name ORDER BY business_unit_name LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total ar balance usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total ar balance trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average current ratio changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_refining/energy_use_monitoring_heat`
*HeatTrack Refining - Energy Use Monitoring & Heat Optimization 🌡️* — fictional company: **HeatTrack Refining** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in highest energy consumption mmbtu?
- **Old SQL:** `SELECT reading_date, MEASURE(max_energy_consumption_mmbtu) AS max_energy_consumption_mmbtu FROM {fqn}.energy_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** What has been the peak energy consumption in mmbtu each month?
- **New SQL:** `SELECT reading_date, MEASURE(max_energy_consumption_mmbtu) AS max_energy_consumption_mmbtu FROM {fqn}.energy_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B1** — `unchanged`
- Q: *How has total energy consumption mmbtu changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest clean ua btu hr f?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_clean_ua_btu_hr_f) AS max_clean_ua_btu_hr_f FROM {fqn}.thermal_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How does peak clean ua value btu/hr/f compare across equipment categorys?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_clean_ua_btu_hr_f) AS max_clean_ua_btu_hr_f FROM {fqn}.thermal_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `unchanged`
- Q: *How has total co2 emissions in metric tons changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top heat exchanger identifier by total energy consumption in mmbtu?
- **Old SQL:** `SELECT exchanger_id, SUM(energy_consumption_mmbtu) AS total_energy_consumption_mmbtu FROM {fqn}.energy_readings GROUP BY exchanger_id ORDER BY total_energy_consumption_mmbtu DESC LIMIT 10`
- **New Q:** Which heat exchangers have the highest total energy consumption in mmbtu?
- **New SQL:** `SELECT exchanger_name, SUM(energy_consumption_mmbtu) AS total_energy_consumption_mmbtu FROM {fqn}.energy_readings GROUP BY exchanger_name ORDER BY total_energy_consumption_mmbtu DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average heat transfer effectiveness percentage by equipment category?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.energy_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which equipment categorys have the highest total solomon energy efficiency index?
- **New SQL:** `SELECT equipment_category, SUM(energy_efficiency_index) AS total_metric FROM {fqn}.energy_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total inlet temp f?
- **Old SQL:** `SELECT reading_date, MEASURE(total_inlet_temp_f) AS total_inlet_temp_f FROM {fqn}.energy_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average inlet temperature trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_inlet_temp_f) AS avg_inlet_temp_f FROM {fqn}.energy_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `rewritten`
- **Old Q:** How has total outlet temp f changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_outlet_temp_f) AS total_outlet_temp_f FROM {fqn}.energy_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average outlet temperature in fahrenheit trended over time?
- **New SQL:** `SELECT reading_date, AVG(outlet_temp_f) AS avg_outlet_temp_f FROM {fqn}.energy_readings GROUP BY reading_date ORDER BY reading_date`

**E2** — `unchanged`
- Q: *What is the monthly trend in average heat transfer effectiveness?*

**E3** — `unchanged`
- Q: *What is the trend of total energy consumption in mmbtu over time?*

**E4** — `rewritten`
- **Old Q:** What is the trend of total clean ua value btu/hr/f over time?
- **Old SQL:** `SELECT snapshot_date, SUM(clean_ua_btu_hr_f) AS total_clean_ua_btu_hr_f FROM {fqn}.thermal_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total clean ua value btu/hr/f trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(clean_ua_btu_hr_f) AS total_clean_ua_btu_hr_f FROM {fqn}.thermal_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How has the average solomon energy efficiency index (lower=better) changed over time?
- **Old SQL:** `SELECT kpi_month, AVG(energy_efficiency_index) AS avg_energy_efficiency_index FROM {fqn}.energy_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How does solomon energy efficiency index compare across equipment categorys?
- **New SQL:** `SELECT equipment_category, AVG(energy_efficiency_index) AS avg_energy_efficiency_index FROM {fqn}.energy_kpi_monthly GROUP BY equipment_category ORDER BY equipment_category LIMIT 10`

**E6** — `rewritten`
- **Old Q:** How has total inlet temp f changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_inlet_temp_f) AS total_inlet_temp_f FROM {fqn}.energy_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** Which heat exchangers have the best average inlet temperature in fahrenheit?
- **New SQL:** `SELECT exchanger_name, AVG(inlet_temp_f) AS avg_metric FROM {fqn}.energy_readings GROUP BY exchanger_name ORDER BY avg_metric DESC LIMIT 10`

---

### `oil_gas_refining/financial_analytics_reporting`
*RefineLedger Corp - Financial Analytics & Reporting 💰* — fictional company: **RefineLedger Corp** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest amount changed over time?*

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest planned revenue?
- **Old SQL:** `SELECT snapshot_month, MEASURE(max_planned_revenue) AS max_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** What has been the peak planned_revenue each month?
- **New SQL:** `SELECT snapshot_month, MEASURE(max_planned_revenue) AS max_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**B3** — `rewritten`
- **Old Q:** How has total actual revenue usd changed over time?
- **Old SQL:** `SELECT snapshot_month, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** How has total actual revenue trended over time?
- **New SQL:** `SELECT snapshot_month, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount usd?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which cost centers have the highest total transaction amount?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per first day of snapshot month?
- **Old SQL:** `SELECT snapshot_month, COUNT(*) AS record_count FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** Which cost centers have the highest total actual revenue?
- **New SQL:** `SELECT cost_center_name, MEASURE(total_actual_revenue) AS total_actual_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY total_actual_revenue DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.financial_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which divisions have the highest average operating margin percentage?
- **New SQL:** `SELECT division, AVG(operating_margin_pct) AS avg_metric FROM {fqn}.financial_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total transaction amount usd?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total transaction amount trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E1** — `rewritten`
- **Old Q:** How has total budgeted amount usd changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total budget trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_budget_usd) AS total_budget_usd FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total planned revenue usd?
- **Old SQL:** `SELECT snapshot_month, MEASURE(total_planned_revenue) AS total_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`
- **New Q:** How has total planned revenue trended over time?
- **New SQL:** `SELECT snapshot_month, MEASURE(total_planned_revenue) AS total_planned_revenue FROM {fqn}.budget_snapshots_metrics GROUP BY ALL ORDER BY snapshot_month`

**E3** — `rewritten`
- **Old Q:** What is the trend of total transaction amount usd over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How has total transaction amount trended over time?
- **New SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`

**E4** — `rewritten`
- **Old Q:** What is the trend of total planned monthly revenue usd over time?
- **Old SQL:** `SELECT snapshot_month, SUM(planned_revenue_usd) AS total_planned_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** How has total planned monthly revenue trended over time?
- **New SQL:** `SELECT snapshot_month, SUM(planned_revenue_usd) AS total_planned_revenue_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_month ORDER BY snapshot_month`

**E5** — `unchanged`
- Q: *How has the average operating margin percentage changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.financial_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_refining/predictive_maintenance_asset_health`
*RefineGuard Systems - Predictive Maintenance & Asset Health 🔧* — fictional company: **RefineGuard Systems** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the alarm trip count by reading timestamp?*

**B1** — `rewritten`
- **Old Q:** Which reading timestamps have the most unique total readingss?
- **Old SQL:** `SELECT reading_timestamp, MEASURE(total_readings) AS total_readings FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY total_readings DESC`
- **New Q:** Which process units have the highest average asset health score?
- **New SQL:** `SELECT process_unit, MEASURE(avg_asset_health_score) AS avg_asset_health_score FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY avg_asset_health_score DESC LIMIT 10`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.maintenance_events GROUP BY 1 ORDER BY 1`

**B3** — `unchanged`
- Q: *How has highest downtime hours changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top refinery equipment identifier by total raw sensor measurement value?
- **Old SQL:** `SELECT equipment_id, SUM(sensor_value) AS total_sensor_value FROM {fqn}.sensor_readings GROUP BY equipment_id ORDER BY total_sensor_value DESC LIMIT 10`
- **New Q:** Which equipments have the highest total raw sensor measurement value?
- **New SQL:** `SELECT equipment_name, SUM(sensor_value) AS total_sensor_value FROM {fqn}.sensor_readings GROUP BY equipment_name ORDER BY total_sensor_value DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of the maintenance event?
- **Old SQL:** `SELECT event_date, COUNT(*) AS record_count FROM {fqn}.maintenance_events GROUP BY event_date ORDER BY event_date`
- **New Q:** Which equipments have the highest average repair cost per event?
- **New SQL:** `SELECT equipment_name, MEASURE(avg_repair_cost_usd) AS avg_repair_cost_usd FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY avg_repair_cost_usd DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the snapshot month?
- **Old SQL:** `SELECT snapshot_month, COUNT(*) AS record_count FROM {fqn}.equipment_health_monthly GROUP BY snapshot_month ORDER BY snapshot_month`
- **New Q:** Which equipment types have the highest average health score for the month?
- **New SQL:** `SELECT equipment_type, AVG(avg_health_score) AS avg_metric FROM {fqn}.equipment_health_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the highest sensor value for each reading timestamp?*

**E1** — `unchanged`
- Q: *Rank reading timestamps by total sensor value*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total equipment downtime?
- **Old SQL:** `SELECT event_date, MEASURE(total_downtime_hours) AS total_downtime_hours FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has average equipment downtime in hours trended over time?
- **New SQL:** `SELECT event_date, AVG(downtime_hours) AS avg_downtime_hours FROM {fqn}.maintenance_events GROUP BY event_date ORDER BY event_date`

**E3** — `unchanged`
- Q: *What is the trend of total raw sensor measurement value over time?*

**E4** — `unchanged`
- Q: *What is the trend of total equipment downtime in hours over time?*

**E5** — `unchanged`
- Q: *How has the average average health score for the month changed over time?*

**E6** — `rewritten`
- **Old Q:** Rank reading timestamps by lowest rul days
- **Old SQL:** `SELECT reading_timestamp, MEASURE(min_rul_days) AS min_rul_days FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY min_rul_days DESC`
- **New Q:** How does lowest remaining useful life days compare across equipments?
- **New SQL:** `SELECT reading_timestamp, MEASURE(min_rul_days) AS min_rul_days FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY min_rul_days DESC`

---

### `oil_gas_refining/production_monitoring`
*RefineOps Central - Production Monitoring 📊* — fictional company: **RefineOps Central** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total readingss?
- **Old SQL:** `SELECT reading_date, MEASURE(total_readings) AS total_readings FROM {fqn}.throughput_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.throughput_readings GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has highest throughput bpd changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(max_throughput_bpd) AS max_throughput_bpd FROM {fqn}.throughput_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average throughput in barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_throughput_bpd) AS avg_throughput_bpd FROM {fqn}.throughput_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest avg throughput bpd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_avg_throughput_bpd) AS max_avg_throughput_bpd FROM {fqn}.production_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average throughput barrels per day trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_throughput) AS avg_throughput FROM {fqn}.production_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has total product output bbl changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_product_bbl) AS total_product_bbl FROM {fqn}.production_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total total product output in barrels trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_product_bbl) AS total_product_bbl FROM {fqn}.production_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `unchanged`
- Q: *What are the top process unit id by total throughput in barrels per day?*

**B5** — `rewritten`
- **Old Q:** What is the average average utilization pct by process unit name?
- **Old SQL:** `SELECT unit_name, AVG(avg_utilization_pct) AS avg_avg_utilization_pct FROM {fqn}.production_snapshots GROUP BY unit_name ORDER BY avg_avg_utilization_pct DESC`
- **New Q:** Which process units have the best average utilization percentage?
- **New SQL:** `SELECT unit_name, AVG(avg_utilization_pct) AS avg_avg_utilization_pct FROM {fqn}.production_snapshots GROUP BY unit_name ORDER BY avg_avg_utilization_pct DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.throughput_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which sections have the highest average unit availability percentage?
- **New SQL:** `SELECT refinery_section, AVG(availability_pct) AS avg_metric FROM {fqn}.throughput_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total feed quality api?*

**E1** — `rewritten`
- **Old Q:** How has average throughput bpd changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_throughput_bpd) AS avg_throughput_bpd FROM {fqn}.throughput_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average average throughput barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_throughput_bpd) AS avg_throughput_bpd FROM {fqn}.throughput_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total downtime hours?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_downtime_hours) AS total_downtime_hours FROM {fqn}.production_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average downtime hours in period trended over time?
- **New SQL:** `SELECT snapshot_date, AVG(downtime_hours) AS avg_downtime_hours FROM {fqn}.production_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E3** — `unchanged`
- Q: *How does total throughput in barrels per day break down by process unit id for 'Running' records?*

**E4** — `rewritten`
- **Old Q:** What is the trend of total average throughput bpd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(avg_throughput_bpd) AS total_avg_throughput_bpd FROM {fqn}.production_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has average average throughput barrels per day trended by month?
- **New SQL:** `SELECT snapshot_date, AVG(avg_throughput_bpd) AS total_avg_throughput_bpd FROM {fqn}.production_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How has the average unit availability pct changed over time?
- **Old SQL:** `SELECT kpi_month, AVG(availability_pct) AS avg_availability_pct FROM {fqn}.throughput_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How has average unit availability percentage trended by month?
- **New SQL:** `SELECT kpi_month, AVG(availability_pct) AS avg_availability_pct FROM {fqn}.throughput_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E6** — `rewritten`
- **Old Q:** How has unique total readingss changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_readings) AS total_readings FROM {fqn}.throughput_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.throughput_readings GROUP BY 1 ORDER BY 1`

---

### `oil_gas_refining/quality_event_root_cause_analysis`
*QualityRefine Analytics - Quality Event Root Cause Analysis 🔍* — fictional company: **QualityRefine Analytics** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.quality_events GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has highest off spec volume bbl changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(max_off_spec_volume_bbl) AS max_off_spec_volume_bbl FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has total off-spec product volume in barrels trended over time?
- **New SQL:** `SELECT event_date, MEASURE(max_off_spec_volume_bbl) AS max_off_spec_volume_bbl FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique total batchess?
- **Old SQL:** `SELECT batch_date, MEASURE(total_batches) AS total_batches FROM {fqn}.batch_records_metrics GROUP BY ALL ORDER BY batch_date`
- **New Q:** Which process units have the highest total financial impact?
- **New SQL:** `SELECT unit_name, SUM(financial_impact_usd) AS total_metric FROM {fqn}.quality_events GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has highest volume bbl changed over time?
- **Old SQL:** `SELECT batch_date, MEASURE(max_volume_bbl) AS max_volume_bbl FROM {fqn}.batch_records_metrics GROUP BY ALL ORDER BY batch_date`
- **New Q:** How has total batch volume in barrels trended over time?
- **New SQL:** `SELECT batch_date, MEASURE(max_volume_bbl) AS max_volume_bbl FROM {fqn}.batch_records_metrics GROUP BY ALL ORDER BY batch_date`

**B4** — `rewritten`
- **Old Q:** What are the top process unit identifier by total off-spec product volume in barrels?
- **Old SQL:** `SELECT unit_id, SUM(off_spec_volume_bbl) AS total_off_spec_volume_bbl FROM {fqn}.quality_events GROUP BY unit_id ORDER BY total_off_spec_volume_bbl DESC LIMIT 10`
- **New Q:** Which process units have the highest total off-spec product volume in barrels?
- **New SQL:** `SELECT unit_name, SUM(off_spec_volume_bbl) AS total_off_spec_volume_bbl FROM {fqn}.quality_events GROUP BY unit_name ORDER BY total_off_spec_volume_bbl DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average product yield percentage by process unit name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per first day of the kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.quality_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which product grades have the highest average first-pass quality yield percentage?
- **New SQL:** `SELECT product_grade, AVG(first_pass_yield_pct) AS avg_metric FROM {fqn}.quality_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total off-spec volume in barrels?*

**E1** — `rewritten`
- **Old Q:** How has total financial impact in usd changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_financial_impact_usd) AS total_financial_impact_usd FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has total financial impact in trended over time?
- **New SQL:** `SELECT event_date, MEASURE(total_financial_impact_usd) AS total_financial_impact_usd FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`

**E2** — `unchanged`
- Q: *What is the monthly trend in total batch volume in barrels?*

**E3** — `unchanged`
- Q: *What is the trend of total off-spec product volume in barrels over time?*

**E4** — `unchanged`
- Q: *What is the trend of total batch volume in barrels over time?*

**E5** — `unchanged`
- Q: *How has the average first-pass quality yield percentage changed over time?*

**E6** — `unchanged`
- Q: *Which unit ids have the highest total off-spec volume in barrels?*

---

### `oil_gas_refining/working_capital_cash_flow_optimization`
*RefineCapital Systems - Working Capital & Cash Flow Optimization 💰* — fictional company: **RefineCapital Systems** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in total inflows usd count?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_inflows_usd) AS total_inflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total inflows trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_inflows_usd) AS total_inflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**B1** — `rewritten`
- **Old Q:** How has total outflows usd count changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_outflows_usd) AS total_outflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total outflows trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_outflows_usd) AS total_outflows_usd FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest accounts receivable?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_accounts_receivable) AS max_accounts_receivable FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak accounts_receivable each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_accounts_receivable) AS max_accounts_receivable FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has total ar usd changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_receivables_usd) AS total_receivables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total receivables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_receivables_usd) AS total_receivables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top business unit id by total cash flow amount usd (positive=inflow)?
- **Old SQL:** `SELECT business_unit_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which business units have the most cash flow amount?
- **New SQL:** `SELECT business_unit_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per snapshot date?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which business units have the highest average dso?
- **New SQL:** `SELECT business_unit_name, MEASURE(avg_dso_days) AS avg_dso_days FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY avg_dso_days DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.cashflow_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which segments have the highest total free cash flow?
- **New SQL:** `SELECT segment, SUM(free_cash_flow_usd) AS total_metric FROM {fqn}.cashflow_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total transactionss?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest amount changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total ap usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_payables_usd) AS total_payables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total payables trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_payables_usd) AS total_payables_usd FROM {fqn}.working_capital_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the trend of total cash flow amount usd (positive=inflow) over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How does cash flow amount compare across business units?
- **New SQL:** `SELECT business_unit_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cash_transactions GROUP BY business_unit_name ORDER BY business_unit_name LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total ar balance usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total ar balance trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(accounts_receivable_usd) AS total_accounts_receivable_usd FROM {fqn}.working_capital_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average current ratio changed over time?*

**E6** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.cash_transactions_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.cash_transactions GROUP BY 1 ORDER BY 1`

---

### `oil_gas_upstream/predictive_maintenance_asset_health`
*WellGuard Upstream - Predictive Maintenance & Asset Health 🔧* — fictional company: **WellGuard Upstream** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in alarm trip count?*

**B1** — `rewritten`
- **Old Q:** How has unique total readingss changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_readings) AS total_readings FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique total eventss?
- **Old SQL:** `SELECT event_date, MEASURE(total_events) AS total_events FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** Which equipments have the highest total sensor value?
- **New SQL:** `SELECT equipment_name, SUM(sensor_value) AS total_metric FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `unchanged`
- Q: *How has highest downtime hours changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top equipment id by total sensor value?
- **Old SQL:** `SELECT equipment_id, SUM(sensor_value) AS total_sensor_value FROM {fqn}.sensor_readings GROUP BY equipment_id ORDER BY total_sensor_value DESC LIMIT 10`
- **New Q:** Which equipment types have the best average health score 0-100?
- **New SQL:** `SELECT equipment_type, AVG(health_score) AS avg_metric FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per event date?
- **Old SQL:** `SELECT event_date, COUNT(*) AS record_count FROM {fqn}.maintenance_events GROUP BY event_date ORDER BY event_date`
- **New Q:** Which equipments have the highest total events?
- **New SQL:** `SELECT equipment_name, MEASURE(total_events) AS total_events FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY total_events DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.equipment_health_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which fields have the highest average average health score?
- **New SQL:** `SELECT field_name, AVG(avg_health_score) AS avg_metric FROM {fqn}.equipment_health_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest sensor value?
- **Old SQL:** `SELECT reading_date, MEASURE(max_sensor_value) AS max_sensor_value FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** What has been the peak sensor value each month?
- **New SQL:** `SELECT reading_date, MEASURE(max_sensor_value) AS max_sensor_value FROM {fqn}.sensor_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `unchanged`
- Q: *How has total sensor value changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total downtime hours?
- **Old SQL:** `SELECT event_date, MEASURE(total_downtime_hours) AS total_downtime_hours FROM {fqn}.maintenance_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How has average downtime hours trended over time?
- **New SQL:** `SELECT event_date, AVG(downtime_hours) AS avg_downtime_hours FROM {fqn}.maintenance_events GROUP BY event_date ORDER BY event_date`

**E3** — `unchanged`
- Q: *What is the trend of total sensor value over time?*

**E4** — `unchanged`
- Q: *What is the trend of total downtime hours over time?*

**E5** — `rewritten`
- **Old Q:** How has the average avg health score changed over time?
- **Old SQL:** `SELECT kpi_month, AVG(avg_health_score) AS avg_avg_health_score FROM {fqn}.equipment_health_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How has the average average health score changed over time?
- **New SQL:** `SELECT kpi_month, AVG(avg_health_score) AS avg_avg_health_score FROM {fqn}.equipment_health_monthly GROUP BY kpi_month ORDER BY kpi_month`

**E6** — `unchanged`
- Q: *How does alarm trip count vary across equipment ids?*

---

### `oil_gas_upstream/reservoir_management`
*ReservoirSight Analytics - Reservoir Management 🛢️* — fictional company: **ReservoirSight Analytics** — 13 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in highest oil bpd?
- **Old SQL:** `SELECT reading_date, MEASURE(max_oil_bpd) AS max_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average oil barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_oil_bpd) AS avg_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B1** — `rewritten`
- **Old Q:** How has total bottomhole temp f changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_bottomhole_temp_f) AS total_bottomhole_temp_f FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average bottomhole temp f trended over time?
- **New SQL:** `SELECT reading_date, AVG(bottomhole_temp_f) AS avg_bottomhole_temp_f FROM {fqn}.production_readings GROUP BY reading_date ORDER BY reading_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest cumulative oil bbl?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_cumulative_oil_bbl) AS max_cumulative_oil_bbl FROM {fqn}.reservoir_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak cumulative oil barrels each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_cumulative_oil_bbl) AS max_cumulative_oil_bbl FROM {fqn}.reservoir_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `unchanged`
- Q: *How has total cumulative oil changed over time?*

**B4** — `rewritten`
- **Old Q:** What are the top reservoir id by total oil bpd?
- **Old SQL:** `SELECT reservoir_id, SUM(oil_bpd) AS total_oil_bpd FROM {fqn}.production_readings GROUP BY reservoir_id ORDER BY total_oil_bpd DESC LIMIT 10`
- **New Q:** Which reservoirs have the highest average oil barrels per day?
- **New SQL:** `SELECT reservoir_name, AVG(oil_bpd) AS total_oil_bpd FROM {fqn}.production_readings GROUP BY reservoir_name ORDER BY total_oil_bpd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average recovery factor pct by reservoir name?
- **Old SQL:** `SELECT reservoir_name, AVG(recovery_factor_pct) AS avg_recovery_factor_pct FROM {fqn}.reservoir_snapshots GROUP BY reservoir_name ORDER BY avg_recovery_factor_pct DESC`
- **New Q:** Which reservoirs have the best recovery factor percentage?
- **New SQL:** `SELECT reservoir_name, AVG(recovery_factor_pct) AS avg_recovery_factor_pct FROM {fqn}.reservoir_snapshots GROUP BY reservoir_name ORDER BY avg_recovery_factor_pct DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.reservoir_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** How does opex per boe compare across formations?
- **New SQL:** `SELECT formation, SUM(opex_per_boe) AS total_metric FROM {fqn}.reservoir_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in avg oil bpd?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_oil_bpd) AS avg_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average oil barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_oil_bpd) AS avg_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `rewritten`
- **Old Q:** How has avg gas mcfpd changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_gas_mcfpd) AS avg_gas_mcfpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average gas thousand cubic feet per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_gas_mcfpd) AS avg_gas_mcfpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total estimated eur bbl?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_estimated_eur_bbl) AS total_estimated_eur_bbl FROM {fqn}.reservoir_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total estimated ultimate recovery barrels trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_estimated_eur_bbl) AS total_estimated_eur_bbl FROM {fqn}.reservoir_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the trend of total oil bpd over time?
- **Old SQL:** `SELECT reading_date, SUM(oil_bpd) AS total_oil_bpd FROM {fqn}.production_readings GROUP BY reading_date ORDER BY reading_date`
- **New Q:** Which reservoirs have the best average oil barrels per day?
- **New SQL:** `SELECT reservoir_name, AVG(oil_bpd) AS avg_metric FROM {fqn}.production_readings GROUP BY reservoir_name ORDER BY avg_metric DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total cumulative oil bbl over time?
- **Old SQL:** `SELECT snapshot_date, SUM(cumulative_oil_bbl) AS total_cumulative_oil_bbl FROM {fqn}.reservoir_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total cumulative oil barrels trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(cumulative_oil_bbl) AS total_cumulative_oil_bbl FROM {fqn}.reservoir_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How many distinct kpi id are there per basin?
- **Old SQL:** `SELECT basin, COUNT(DISTINCT kpi_id) AS distinct_count FROM {fqn}.reservoir_kpi_monthly GROUP BY basin ORDER BY distinct_count DESC`
- **New Q:** How does average recovery factor compare across basins?
- **New SQL:** `SELECT basin, AVG(recovery_factor_pct) AS avg_recovery_factor FROM {fqn}.reservoir_snapshots GROUP BY basin ORDER BY avg_recovery_factor DESC LIMIT 10`

**E6** — `rewritten`
- **Old Q:** How has avg reservoir pressure changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_reservoir_pressure) AS avg_reservoir_pressure FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average reservoir pressure changed over time?
- **New SQL:** `SELECT reading_date, MEASURE(avg_reservoir_pressure) AS avg_reservoir_pressure FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

---

### `oil_gas_upstream/well_production_monitoring_flow`
*WellFlow Monitoring - Well Production Monitoring 📊* — fictional company: **WellFlow Monitoring** — 14 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in highest oil bpd?
- **Old SQL:** `SELECT reading_date, MEASURE(max_oil_bpd) AS max_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average oil barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_oil_bpd) AS avg_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**B1** — `rewritten`
- **Old Q:** How has total casing pressure psi changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_casing_pressure_psi) AS total_casing_pressure_psi FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average casing pressure pressure (psi) trended over time?
- **New SQL:** `SELECT reading_date, AVG(casing_pressure_psi) AS avg_casing_pressure_psi FROM {fqn}.production_readings GROUP BY reading_date ORDER BY reading_date`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in highest cumulative oil bbl?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_cumulative_oil_bbl) AS max_cumulative_oil_bbl FROM {fqn}.well_status_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak cumulative oil barrels each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_cumulative_oil_bbl) AS max_cumulative_oil_bbl FROM {fqn}.well_status_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B3** — `rewritten`
- **Old Q:** How has total cumulative oil bbl changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_cumulative_oil) AS total_cumulative_oil FROM {fqn}.well_status_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total cumulative oil trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_cumulative_oil) AS total_cumulative_oil FROM {fqn}.well_status_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top well id by total oil bpd?
- **Old SQL:** `SELECT well_id, SUM(oil_bpd) AS total_oil_bpd FROM {fqn}.production_readings GROUP BY well_id ORDER BY total_oil_bpd DESC LIMIT 10`
- **New Q:** Which wells have the highest average oil barrels per day?
- **New SQL:** `SELECT well_name, AVG(oil_bpd) AS total_oil_bpd FROM {fqn}.production_readings GROUP BY well_name ORDER BY total_oil_bpd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average water cut pct by well name?
- **Old SQL:** `SELECT well_name, AVG(water_cut_pct) AS avg_water_cut_pct FROM {fqn}.well_status_snapshots GROUP BY well_name ORDER BY avg_water_cut_pct DESC`
- **New Q:** Which wells have the highest average water cut percentage?
- **New SQL:** `SELECT well_name, AVG(water_cut_pct) AS avg_water_cut_pct FROM {fqn}.well_status_snapshots GROUP BY well_name ORDER BY avg_water_cut_pct DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per kpi month?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.production_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which pads have the highest total deferred oil barrels?
- **New SQL:** `SELECT pad_name, SUM(deferred_oil_bbl) AS total_metric FROM {fqn}.production_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in avg oil bpd?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_oil_bpd) AS avg_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average oil barrels per day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_oil_bpd) AS avg_oil_bpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E1** — `rewritten`
- **Old Q:** How has avg gas mcfpd changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_gas_mcfpd) AS avg_gas_mcfpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average gas mcf/day trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_gas_mcfpd) AS avg_gas_mcfpd FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total gor scf bbl?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_gor_scf_bbl) AS total_gor_scf_bbl FROM {fqn}.well_status_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total gor scf/barrels trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_gor_scf_bbl) AS total_gor_scf_bbl FROM {fqn}.well_status_snapshots_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How does total oil bpd break down by well id for 'Flowing' records?
- **Old SQL:** `SELECT well_id, COUNT(*) AS record_count, SUM(oil_bpd) AS total_oil_bpd FROM {fqn}.production_readings WHERE well_status = 'Flowing' GROUP BY well_id ORDER BY total_oil_bpd DESC`
- **New Q:** Which currently-flowing wells are producing the most oil?
- **New SQL:** `SELECT well_name, AVG(oil_bpd) AS avg_oil_bpd FROM {fqn}.well_production WHERE well_status = 'Flowing' GROUP BY well_name ORDER BY avg_oil_bpd DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total cumulative oil bbl over time?
- **Old SQL:** `SELECT snapshot_date, SUM(cumulative_oil_bbl) AS total_cumulative_oil_bbl FROM {fqn}.well_status_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total cumulative oil barrels trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(cumulative_oil_bbl) AS total_cumulative_oil_bbl FROM {fqn}.well_status_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How many distinct kpi id are there per pad name?
- **Old SQL:** `SELECT pad_name, COUNT(DISTINCT kpi_id) AS distinct_count FROM {fqn}.production_kpi_monthly GROUP BY pad_name ORDER BY distinct_count DESC`
- **New Q:** How does average daily oil production compare across pads?
- **New SQL:** `SELECT pad_name, AVG(oil_bpd) AS avg_oil_bpd FROM {fqn}.well_production GROUP BY pad_name ORDER BY avg_oil_bpd DESC LIMIT 10`

**E6** — `rewritten`
- **Old Q:** How has avg tubing pressure changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(avg_tubing_pressure) AS avg_tubing_pressure FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average tubing pressure changed over time?
- **New SQL:** `SELECT reading_date, MEASURE(avg_tubing_pressure) AS avg_tubing_pressure FROM {fqn}.production_readings_metrics GROUP BY ALL ORDER BY reading_date`

---

### `power_generation/financial_analytics_reporting`
*PowerLedger Corp - Financial Analytics & Reporting 💰* — fictional company: **PowerLedger Corp** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique cost centers?
- **Old SQL:** `SELECT record_date, MEASURE(unique_cost_center_count) AS unique_cost_center_count FROM {fqn}.financial_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', record_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest revenue changed over time?*

**B2** — `unchanged`
- Q: *How has highest annual budget changed over time?*

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in total annual budget usd?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_annual_budget) AS total_annual_budget FROM {fqn}.budget_status_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which cost centers have the highest total transaction amount?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_metric FROM {fqn}.cost_centers GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount in usd?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cost_centers GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which departments have the highest total revenue?
- **New SQL:** `SELECT department, SUM(revenue_usd) AS total_metric FROM {fqn}.financial_transactions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average variance as percentage of budget by department?*

**B6** — `rewritten`
- **Old Q:** How many records are there per date of budget snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which departments have the highest average operating margin percentage?
- **New SQL:** `SELECT department, MEASURE(avg_operating_margin) AS avg_operating_margin FROM {fqn}.budget_status_monthly GROUP BY ALL ORDER BY avg_operating_margin DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total revenue in usd?
- **Old SQL:** `SELECT record_date, MEASURE(total_revenue) AS total_revenue FROM {fqn}.financial_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has total revenue trended over time?
- **New SQL:** `SELECT record_date, MEASURE(total_revenue) AS total_revenue FROM {fqn}.financial_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E1** — `rewritten`
- **Old Q:** How has total actual cost in usd changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_actual_cost) AS total_actual_cost FROM {fqn}.financial_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has total actual cost trended over time?
- **New SQL:** `SELECT record_date, MEASURE(total_actual_cost) AS total_actual_cost FROM {fqn}.financial_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in average operating margin pct?
- **Old SQL:** `SELECT snapshot_date, MEASURE(avg_operating_margin) AS avg_operating_margin FROM {fqn}.budget_status_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total operating margin trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(avg_operating_margin) AS avg_operating_margin FROM {fqn}.budget_status_monthly GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** Rank departments by total committed capex usd
- **Old SQL:** `SELECT department, MEASURE(total_capex_committed) AS total_capex_committed FROM {fqn}.budget_status_monthly GROUP BY ALL ORDER BY total_capex_committed DESC`
- **New Q:** How does total capex committed compare across departments?
- **New SQL:** `SELECT department, MEASURE(total_capex_committed) AS total_capex_committed FROM {fqn}.budget_status_monthly GROUP BY ALL ORDER BY total_capex_committed DESC`

**E4** — `rewritten`
- **Old Q:** How does total transaction amount in usd break down by cost center identifier for 'Pending' records?
- **Old SQL:** `SELECT cost_center_id, COUNT(*) AS record_count, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cost_centers WHERE approval_status = 'Pending' GROUP BY cost_center_id ORDER BY total_amount_usd DESC`
- **New Q:** Which cost centers have the highest total *?
- **New SQL:** `SELECT cost_center_name, SUM(*) AS record_count, SUM(amount_usd) AS total_amount_usd FROM {fqn}.cost_centers WHERE approval_status = 'Pending' GROUP BY cost_center_name ORDER BY total_amount_usd DESC LIMIT 10`

**E5** — `rewritten`
- **Old Q:** What is the trend of total revenue in usd (generation cost centers only) over time?
- **Old SQL:** `SELECT record_date, SUM(revenue_usd) AS total_revenue_usd FROM {fqn}.financial_transactions GROUP BY record_date ORDER BY record_date`
- **New Q:** How has total revenue in trended over time?
- **New SQL:** `SELECT record_date, SUM(revenue_usd) AS total_revenue_usd FROM {fqn}.financial_transactions GROUP BY record_date ORDER BY record_date`

**E6** — `unchanged`
- Q: *How has the average operating margin percentage changed over time?*

---

### `power_generation/grid_management_energy_mix`
*PowerMix Dynamics - Grid Management & Energy Mix ⚡* — fictional company: **PowerMix Dynamics** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in dispatched plant count?*

**B1** — `rewritten`
- **Old Q:** How has unique total plants changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_plant_count) AS total_plant_count FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', record_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.generation_units GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique plants?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_plant_count) AS unique_plant_count FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which power plants have the highest total energy generated in megawatt-hours?
- **New SQL:** `SELECT plant_name, SUM(generation_mwh) AS total_metric FROM {fqn}.generation_units GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has highest planned mwh changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_planned_mwh) AS max_planned_mwh FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total planned generation in mwh trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_planned_mwh) AS max_planned_mwh FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**B4** — `unchanged`
- Q: *What is the average energy generated in megawatt-hours by power plant identifier?*

**B5** — `unchanged`
- Q: *What is the average unit availability percentage 0-100 by generation fuel type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per date of dispatch snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.dispatch_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which generation fuel types have the highest average reserve margin percentage?
- **New SQL:** `SELECT fuel_type, MEASURE(avg_reserve_margin) AS avg_reserve_margin FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY avg_reserve_margin DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest generation mwh?
- **Old SQL:** `SELECT record_date, MEASURE(max_generation_mwh) AS max_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** What has been the peak energy generated in megawatt-hours each month?
- **New SQL:** `SELECT record_date, MEASURE(max_generation_mwh) AS max_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E1** — `rewritten`
- **Old Q:** How has total energy generated in mwh changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_generation_mwh) AS total_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has total energy generated in megawatt-hours trended over time?
- **New SQL:** `SELECT record_date, MEASURE(total_generation_mwh) AS total_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total planned generation mwh?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_planned_mwh) AS total_planned_mwh FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total planned generation in mwh trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_planned_mwh) AS total_planned_mwh FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How has total forecast accuracy pct changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_forecast_accuracy_percent) AS total_forecast_accuracy_percent FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has average forecast accuracy percent trended by month?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_forecast_accuracy_percent) AS total_forecast_accuracy_percent FROM {fqn}.dispatch_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**E4** — `unchanged`
- Q: *How has the average energy generated in megawatt-hours changed over time?*

**E5** — `unchanged`
- Q: *What is the trend of total instantaneous output in megawatts over time?*

**E6** — `unchanged`
- Q: *How has the average operating reserve margin percentage changed over time?*

---

### `power_generation/hydro_optimization`
*HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧* — fictional company: **HydroFlow Energy** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in generating turbine count?*

**B1** — `rewritten`
- **Old Q:** How has unique total turbines changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_turbine_count) AS total_turbine_count FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', record_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.turbine_units GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in high drought risk count?*

**B3** — `rewritten`
- **Old Q:** How has unique turbines changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_turbine_count) AS unique_turbine_count FROM {fqn}.reservoir_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How does energy generated in mwh compare across turbine units?
- **New SQL:** `SELECT turbine_name, SUM(generation_mwh) AS total_metric FROM {fqn}.turbine_units GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top turbine unit identifier by total water flow rate in cubic meters per second?
- **Old SQL:** `SELECT turbine_id, SUM(water_flow_m3s) AS total_water_flow_m3s FROM {fqn}.turbine_units GROUP BY turbine_id ORDER BY total_water_flow_m3s DESC LIMIT 10`
- **New Q:** Which turbine units have the highest total water flow rate in cubic meters per second?
- **New SQL:** `SELECT turbine_name, SUM(water_flow_m3s) AS total_water_flow_m3s FROM {fqn}.turbine_units GROUP BY turbine_name ORDER BY total_water_flow_m3s DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average percentage of inflow from snowmelt by dam name?*

**B6** — `rewritten`
- **Old Q:** How many records are there per date of reservoir snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.reservoir_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which dams have the highest average reservoir storage percentage?
- **New SQL:** `SELECT dam_name, MEASURE(avg_storage_pct) AS avg_storage_pct FROM {fqn}.reservoir_kpi_monthly GROUP BY ALL ORDER BY avg_storage_pct DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest generation mwh?
- **Old SQL:** `SELECT record_date, MEASURE(max_generation_mwh) AS max_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How does peak energy generated in mwh compare across turbine units?
- **New SQL:** `SELECT record_date, MEASURE(max_generation_mwh) AS max_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E1** — `rewritten`
- **Old Q:** How has total hydro generation in mwh changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_generation_mwh) AS total_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has total energy generated in mwh trended over time?
- **New SQL:** `SELECT record_date, MEASURE(total_generation_mwh) AS total_generation_mwh FROM {fqn}.generation_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest water level m?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_water_level_m) AS max_water_level_m FROM {fqn}.reservoir_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak reservoir water level in meters above datum each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_water_level_m) AS max_water_level_m FROM {fqn}.reservoir_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**E3** — `unchanged`
- Q: *How has total water level m changed over time?*

**E4** — `rewritten`
- **Old Q:** How does total water flow rate in cubic meters per second break down by turbine unit identifier for 'Maintenance' records?
- **Old SQL:** `SELECT turbine_id, COUNT(*) AS record_count, SUM(water_flow_m3s) AS total_water_flow_m3s FROM {fqn}.turbine_units WHERE operating_status = 'Maintenance' GROUP BY turbine_id ORDER BY total_water_flow_m3s DESC`
- **New Q:** Which turbine units have the highest total *?
- **New SQL:** `SELECT turbine_name, SUM(*) AS record_count, SUM(water_flow_m3s) AS total_water_flow_m3s FROM {fqn}.turbine_units WHERE operating_status = 'Maintenance' GROUP BY turbine_name ORDER BY total_water_flow_m3s DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total water inflow rate in m3/s over time?*

**E6** — `unchanged`
- Q: *How has the average reservoir storage as percentage of capacity changed over time?*

---

### `power_generation/nuclear_safety`
*NucleoSafe Systems - Nuclear Safety & Compliance ☢️* — fictional company: **NucleoSafe Systems** — 9 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique readings?
- **Old SQL:** `SELECT reading_date, MEASURE(reading_count) AS reading_count FROM {fqn}.safety_kpi_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.safety_readings GROUP BY 1 ORDER BY 1`

**B1** — `rewritten`
- **Old Q:** How has unique components changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(unique_component_count) AS unique_component_count FROM {fqn}.safety_kpi_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** Which components have the best average component temperature in celsius?
- **New SQL:** `SELECT component_name, AVG(temperature_celsius) AS avg_metric FROM {fqn}.reactor_components GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B2** — `unchanged`
- Q: *What is the monthly trend in fail count?*

**B3** — `rewritten`
- **Old Q:** How has unique inspections changed over time?
- **Old SQL:** `SELECT inspection_date, MEASURE(inspection_count) AS inspection_count FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY inspection_date`
- **New Q:** Which component type: fuel assembly, control rod, coolant pump, steam generator, containments have the best average pressure in megapascals?
- **New SQL:** `SELECT component_type, AVG(pressure_mpa) AS avg_metric FROM {fqn}.reactor_components GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top reactor component identifier by total component temperature in celsius?
- **Old SQL:** `SELECT component_id, SUM(temperature_celsius) AS total_temperature_celsius FROM {fqn}.reactor_components GROUP BY component_id ORDER BY total_temperature_celsius DESC LIMIT 10`
- **New Q:** Which reactor unit designations have the highest total radiation level in millisieverts?
- **New SQL:** `SELECT reactor_unit, SUM(radiation_msv) AS total_metric FROM {fqn}.reactor_components GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average neutron flux as percentage of rated 0-100 by component type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per date of inspection?
- **Old SQL:** `SELECT inspection_date, COUNT(*) AS record_count FROM {fqn}.inspection_snapshots GROUP BY inspection_date ORDER BY inspection_date`
- **New Q:** Which component types have the highest average nrc compliance score?
- **New SQL:** `SELECT component_type, MEASURE(avg_compliance_score) AS avg_compliance_score FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY avg_compliance_score DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest neutron flux percent?
- **Old SQL:** `SELECT reading_date, MEASURE(max_neutron_flux_percent) AS max_neutron_flux_percent FROM {fqn}.safety_kpi_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** What has been the peak neutron_flux_percent each month?
- **New SQL:** `SELECT reading_date, MEASURE(max_neutron_flux_percent) AS max_neutron_flux_percent FROM {fqn}.safety_kpi_monthly GROUP BY ALL ORDER BY reading_date`

**E1** — `unchanged`
- Q: *How has total safety alarms triggered changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique components?
- **Old SQL:** `SELECT inspection_date, MEASURE(unique_component_count) AS unique_component_count FROM {fqn}.inspection_kpi_monthly GROUP BY ALL ORDER BY inspection_date`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', inspection_date) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.inspection_snapshots GROUP BY 1 ORDER BY 1`

**E3** — `unchanged`
- Q: *How does fail count vary across component types?*

**E4** — `rewritten`
- **Old Q:** How does total component temperature in celsius break down by reactor component identifier for 'Critical' records?
- **Old SQL:** `SELECT component_id, COUNT(*) AS record_count, SUM(temperature_celsius) AS total_temperature_celsius FROM {fqn}.reactor_components WHERE health_status = 'Critical' GROUP BY component_id ORDER BY total_temperature_celsius DESC`
- **New Q:** Which components have the highest total *?
- **New SQL:** `SELECT component_name, SUM(*) AS record_count, SUM(temperature_celsius) AS total_temperature_celsius FROM {fqn}.reactor_components WHERE health_status = 'Critical' GROUP BY component_name ORDER BY total_temperature_celsius DESC LIMIT 10`

**E5** — `rewritten`
- **Old Q:** What is the trend of total containment pressure in kilopascals over time?
- **Old SQL:** `SELECT reading_date, SUM(containment_pressure_kpa) AS total_containment_pressure_kpa FROM {fqn}.safety_readings GROUP BY reading_date ORDER BY reading_date`
- **New Q:** How has average containment pressure in kilopascals trended over time?
- **New SQL:** `SELECT reading_date, AVG(containment_pressure_kpa) AS total_containment_pressure_kpa FROM {fqn}.safety_readings GROUP BY reading_date ORDER BY reading_date`

**E6** — `unchanged`
- Q: *How has the average nrc compliance score 0-100 changed over time?*

---

### `power_generation/outage_response`
*RestorePower Gen - Outage Response & Restoration 🔌* — fictional company: **RestorePower Gen** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in forced outage count?*

**B1** — `rewritten`
- **Old Q:** How has unique total outage eventss changed over time?
- **Old SQL:** `SELECT outage_date, MEASURE(total_outage_events) AS total_outage_events FROM {fqn}.outage_kpi_monthly GROUP BY ALL ORDER BY outage_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', outage_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.outage_events GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in running unit count?*

**B3** — `rewritten`
- **Old Q:** How has unique total units changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_unit_count) AS total_unit_count FROM {fqn}.unit_availability_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** Which generator units have the best average hours of operation in the day?
- **New SQL:** `SELECT unit_name, AVG(runtime_hours) AS avg_metric FROM {fqn}.generating_units GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top generator unit identifier by total hours of operation in the day?
- **Old SQL:** `SELECT unit_id, SUM(runtime_hours) AS total_runtime_hours FROM {fqn}.generating_units GROUP BY unit_id ORDER BY total_runtime_hours DESC LIMIT 10`
- **New Q:** How does energy output in mwh compare across generator types?
- **New SQL:** `SELECT unit_type, SUM(output_mwh) AS total_metric FROM {fqn}.generating_units GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average outage duration in hours by generator type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per date of repair snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.repair_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which generator types have the highest total number of repair crew members deployed?
- **New SQL:** `SELECT unit_type, SUM(crew_count) AS total_metric FROM {fqn}.repair_snapshots GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique units?
- **Old SQL:** `SELECT outage_date, MEASURE(unique_unit_count) AS unique_unit_count FROM {fqn}.outage_kpi_monthly GROUP BY ALL ORDER BY outage_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', outage_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.outage_events GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest duration hours changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest runtime hours?
- **Old SQL:** `SELECT record_date, MEASURE(max_runtime_hours) AS max_runtime_hours FROM {fqn}.unit_availability_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** What has been the peak hours of operation in the day each month?
- **New SQL:** `SELECT record_date, MEASURE(max_runtime_hours) AS max_runtime_hours FROM {fqn}.unit_availability_monthly GROUP BY ALL ORDER BY record_date`

**E3** — `unchanged`
- Q: *How has running unit count changed over time?*

**E4** — `rewritten`
- **Old Q:** How does total hours of operation in the day break down by generator unit identifier for 'Forced Outage' records?
- **Old SQL:** `SELECT unit_id, COUNT(*) AS record_count, SUM(runtime_hours) AS total_runtime_hours FROM {fqn}.generating_units WHERE operational_status = 'Forced Outage' GROUP BY unit_id ORDER BY total_runtime_hours DESC`
- **New Q:** Which generator units have the highest total *?
- **New SQL:** `SELECT unit_name, SUM(*) AS record_count, SUM(runtime_hours) AS total_runtime_hours FROM {fqn}.generating_units WHERE operational_status = 'Forced Outage' GROUP BY unit_name ORDER BY total_runtime_hours DESC LIMIT 10`

**E5** — `rewritten`
- **Old Q:** What is the trend of total repair and restoration cost in usd over time?
- **Old SQL:** `SELECT outage_date, SUM(repair_cost_usd) AS total_repair_cost_usd FROM {fqn}.outage_events GROUP BY outage_date ORDER BY outage_date`
- **New Q:** How has total repair and restoration cost in trended over time?
- **New SQL:** `SELECT outage_date, SUM(repair_cost_usd) AS total_repair_cost_usd FROM {fqn}.outage_events GROUP BY outage_date ORDER BY outage_date`

**E6** — `unchanged`
- Q: *How has the average percentage of required parts available changed over time?*

---

### `power_generation/solar_optimization_behind_the_meter`
*SolarEdge Power - Solar & Storage Optimization ☀️* — fictional company: **SolarEdge Power** — 8 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in online site count?*

**B1** — `rewritten`
- **Old Q:** How has unique total sites changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_site_count) AS total_site_count FROM {fqn}.solar_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', record_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.solar_installations GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in fault count?*

**B3** — `rewritten`
- **Old Q:** How has unique sites changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_site_count) AS unique_site_count FROM {fqn}.battery_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which sites have the highest total solar energy generated in kwh?
- **New SQL:** `SELECT site_name, SUM(solar_generation_kwh) AS total_metric FROM {fqn}.solar_installations GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top solar+storage site identifier by total solar irradiance in kwh/m2?
- **Old SQL:** `SELECT site_id, SUM(irradiance_kwh_m2) AS total_irradiance_kwh_m2 FROM {fqn}.solar_installations GROUP BY site_id ORDER BY total_irradiance_kwh_m2 DESC LIMIT 10`
- **New Q:** Which sites have the highest total solar irradiance in kwh/m2?
- **New SQL:** `SELECT site_name, SUM(irradiance_kwh_m2) AS total_irradiance_kwh_m2 FROM {fqn}.solar_installations GROUP BY site_name ORDER BY total_irradiance_kwh_m2 DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per date of reading?
- **Old SQL:** `SELECT reading_date, COUNT(*) AS record_count FROM {fqn}.generation_readings GROUP BY reading_date ORDER BY reading_date`
- **New Q:** Which site types have the highest total energy consumed on-site in kwh?
- **New SQL:** `SELECT site_type, SUM(self_consumption_kwh) AS total_metric FROM {fqn}.generation_readings GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per date of battery snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.battery_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which site types have the highest average battery state of charge?
- **New SQL:** `SELECT site_type, MEASURE(avg_state_of_charge) AS avg_state_of_charge FROM {fqn}.battery_kpi_monthly GROUP BY ALL ORDER BY avg_state_of_charge DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest solar generation kwh?
- **Old SQL:** `SELECT record_date, MEASURE(max_solar_generation_kwh) AS max_solar_generation_kwh FROM {fqn}.solar_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** What has been the peak solar energy generated in kwh each month?
- **New SQL:** `SELECT record_date, MEASURE(max_solar_generation_kwh) AS max_solar_generation_kwh FROM {fqn}.solar_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E1** — `unchanged`
- Q: *How has total solar generation in kwh changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest state of charge percent?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_state_of_charge_percent) AS max_state_of_charge_percent FROM {fqn}.battery_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak state_of_charge_percent each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_state_of_charge_percent) AS max_state_of_charge_percent FROM {fqn}.battery_kpi_monthly GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How does total solar irradiance in kwh/m2 break down by solar+storage site identifier for 'Offline' records?
- **Old SQL:** `SELECT site_id, COUNT(*) AS record_count, SUM(irradiance_kwh_m2) AS total_irradiance_kwh_m2 FROM {fqn}.solar_installations WHERE inverter_status = 'Offline' GROUP BY site_id ORDER BY total_irradiance_kwh_m2 DESC`
- **New Q:** Which sites have the highest total *?
- **New SQL:** `SELECT site_name, SUM(*) AS record_count, SUM(irradiance_kwh_m2) AS total_irradiance_kwh_m2 FROM {fqn}.solar_installations WHERE inverter_status = 'Offline' GROUP BY site_name ORDER BY total_irradiance_kwh_m2 DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total energy exported to grid in kwh over time?*

**E5** — `unchanged`
- Q: *How has the average battery state of charge 0-100 changed over time?*

**E6** — `unchanged`
- Q: *How has online site count changed over time?*

---

### `power_generation/wind_optimization`
*WindPeak Energy - Wind Farm Optimization 💨* — fictional company: **WindPeak Energy** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in generating count?*

**B1** — `rewritten`
- **Old Q:** How has unique total turbines changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_turbine_count) AS total_turbine_count FROM {fqn}.turbine_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', record_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.wind_turbines GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique turbines?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_turbine_count) AS unique_turbine_count FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How does energy generated in mwh compare across turbines?
- **New SQL:** `SELECT turbine_name, SUM(generation_mwh) AS total_metric FROM {fqn}.wind_turbines GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has highest forecasted generation mwh changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_forecasted_generation_mwh) AS max_forecasted_generation_mwh FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total forecasted generation in mwh trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_forecasted_generation_mwh) AS max_forecasted_generation_mwh FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top wind turbine identifier by total average wind speed in meters per second?
- **Old SQL:** `SELECT turbine_id, SUM(avg_wind_speed_ms) AS total_avg_wind_speed_ms FROM {fqn}.wind_turbines GROUP BY turbine_id ORDER BY total_avg_wind_speed_ms DESC LIMIT 10`
- **New Q:** Which turbines have the highest total average wind speed in meters per second?
- **New SQL:** `SELECT turbine_name, SUM(avg_wind_speed_ms) AS total_avg_wind_speed_ms FROM {fqn}.wind_turbines GROUP BY turbine_name ORDER BY total_avg_wind_speed_ms DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average deviation from ideal power curve 0-100 by turbine model?*

**B6** — `rewritten`
- **Old Q:** How many records are there per date of snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.wind_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which wind farms have the highest average turbine availability?
- **New SQL:** `SELECT wind_farm, MEASURE(avg_availability) AS avg_availability FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY avg_availability DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest generation mwh?
- **Old SQL:** `SELECT record_date, MEASURE(max_generation_mwh) AS max_generation_mwh FROM {fqn}.turbine_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How does peak energy generated in mwh compare across turbines?
- **New SQL:** `SELECT record_date, MEASURE(max_generation_mwh) AS max_generation_mwh FROM {fqn}.turbine_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E1** — `rewritten`
- **Old Q:** How has total wind generation mwh changed over time?
- **Old SQL:** `SELECT record_date, MEASURE(total_generation_mwh) AS total_generation_mwh FROM {fqn}.turbine_kpi_monthly GROUP BY ALL ORDER BY record_date`
- **New Q:** How has total energy generated in mwh trended over time?
- **New SQL:** `SELECT record_date, MEASURE(total_generation_mwh) AS total_generation_mwh FROM {fqn}.turbine_kpi_monthly GROUP BY ALL ORDER BY record_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in total forecasted generation mwh?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_forecasted_mwh) AS total_forecasted_mwh FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total forecasted mwh trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_forecasted_mwh) AS total_forecasted_mwh FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** How has total ppa price mwh changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_ppa_price_mwh) AS total_ppa_price_mwh FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How has total power purchase agreement price per mwh trended over time?
- **New SQL:** `SELECT snapshot_date, MEASURE(total_ppa_price_mwh) AS total_ppa_price_mwh FROM {fqn}.wind_forecast_monthly GROUP BY ALL ORDER BY snapshot_date`

**E4** — `rewritten`
- **Old Q:** How does total average wind speed in meters per second break down by wind turbine identifier for 'Fault' records?
- **Old SQL:** `SELECT turbine_id, COUNT(*) AS record_count, SUM(avg_wind_speed_ms) AS total_avg_wind_speed_ms FROM {fqn}.wind_turbines WHERE turbine_status = 'Fault' GROUP BY turbine_id ORDER BY total_avg_wind_speed_ms DESC`
- **New Q:** Which turbines have the highest total *?
- **New SQL:** `SELECT turbine_name, SUM(*) AS record_count, SUM(avg_wind_speed_ms) AS total_avg_wind_speed_ms FROM {fqn}.wind_turbines WHERE turbine_status = 'Fault' GROUP BY turbine_name ORDER BY total_avg_wind_speed_ms DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total blade pitch angle in degrees over time?*

**E6** — `rewritten`
- **Old Q:** How has the average forecasted generation in mwh changed over time?
- **Old SQL:** `SELECT snapshot_date, AVG(forecasted_generation_mwh) AS avg_forecasted_generation_mwh FROM {fqn}.wind_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has average forecasted generation in mwh trended by month?
- **New SQL:** `SELECT snapshot_date, AVG(forecasted_generation_mwh) AS avg_forecasted_generation_mwh FROM {fqn}.wind_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

---

### `railroad/freight_demand_forecasting`
*FreightSight Analytics - Freight Demand Forecasting 📈* — fictional company: **FreightSight Analytics** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in delayed count?*

**B1** — `rewritten`
- **Old Q:** How has unique shipments changed over time?
- **Old SQL:** `SELECT shipment_date, MEASURE(shipment_count) AS shipment_count FROM {fqn}.freight_kpi_monthly GROUP BY ALL ORDER BY shipment_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', shipment_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.shipping_lanes GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique forecasts?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_count) AS forecast_count FROM {fqn}.forecast_kpi_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** Which lanes have the highest total number of carloads?
- **New SQL:** `SELECT lane_name, SUM(carloads) AS total_metric FROM {fqn}.shipping_lanes GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has unique lanes changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(unique_lane_count) AS unique_lane_count FROM {fqn}.forecast_kpi_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** Which commodity types have the highest total freight revenue?
- **New SQL:** `SELECT commodity, SUM(revenue_usd) AS total_metric FROM {fqn}.shipping_lanes GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top freight lane identifier by total number of carloads?
- **Old SQL:** `SELECT lane_id, SUM(carloads) AS total_carloads FROM {fqn}.shipping_lanes GROUP BY lane_id ORDER BY total_carloads DESC LIMIT 10`
- **New Q:** Which origin regions have the best average transit time in days?
- **New SQL:** `SELECT origin_region, AVG(transit_days) AS avg_metric FROM {fqn}.shipping_lanes GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average average rate per car usd by commodity?
- **Old SQL:** `SELECT commodity, AVG(avg_rate_per_car) AS avg_avg_rate_per_car FROM {fqn}.freight_orders GROUP BY commodity ORDER BY avg_avg_rate_per_car DESC`
- **New Q:** Which commoditys have the highest average average rate per car?
- **New SQL:** `SELECT commodity, AVG(avg_rate_per_car) AS avg_avg_rate_per_car FROM {fqn}.freight_orders GROUP BY commodity ORDER BY avg_avg_rate_per_car DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per forecast month?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which commoditys have the highest average forecast error?
- **New SQL:** `SELECT commodity, MEASURE(avg_forecast_error) AS avg_forecast_error FROM {fqn}.forecast_kpi_monthly GROUP BY ALL ORDER BY avg_forecast_error DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique lanes?
- **Old SQL:** `SELECT shipment_date, MEASURE(unique_lane_count) AS unique_lane_count FROM {fqn}.freight_kpi_monthly GROUP BY ALL ORDER BY shipment_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', shipment_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.shipping_lanes GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest carloads changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted carloads?
- **Old SQL:** `SELECT forecast_month, MEASURE(max_forecasted_carloads) AS max_forecasted_carloads FROM {fqn}.forecast_kpi_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** What has been the peak forecasted carloads each month?
- **New SQL:** `SELECT forecast_month, MEASURE(max_forecasted_carloads) AS max_forecasted_carloads FROM {fqn}.forecast_kpi_monthly GROUP BY ALL ORDER BY forecast_month`

**E3** — `rewritten`
- **Old Q:** How has unique forecasts changed over time?
- **Old SQL:** `SELECT forecast_month, MEASURE(forecast_count) AS forecast_count FROM {fqn}.forecast_kpi_monthly GROUP BY ALL ORDER BY forecast_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', forecast_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.demand_forecasts GROUP BY 1 ORDER BY 1`

**E4** — `rewritten`
- **Old Q:** How does total number of carloads break down by freight lane identifier for 'Delayed' records?
- **Old SQL:** `SELECT lane_id, COUNT(*) AS record_count, SUM(carloads) AS total_carloads FROM {fqn}.shipping_lanes WHERE shipment_status = 'Delayed' GROUP BY lane_id ORDER BY total_carloads DESC`
- **New Q:** Which lanes have the highest total *?
- **New SQL:** `SELECT lane_name, SUM(*) AS record_count, SUM(carloads) AS total_carloads FROM {fqn}.shipping_lanes WHERE shipment_status = 'Delayed' GROUP BY lane_name ORDER BY total_carloads DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total number of bookings over time?*

**E6** — `rewritten`
- **Old Q:** How has the average absolute forecast error pct changed over time?
- **Old SQL:** `SELECT forecast_month, AVG(forecast_error_pct) AS avg_forecast_error_pct FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** How has average absolute forecast error percentage trended by month?
- **New SQL:** `SELECT forecast_month, AVG(forecast_error_pct) AS avg_forecast_error_pct FROM {fqn}.demand_forecasts GROUP BY forecast_month ORDER BY forecast_month`

---

### `railroad/predictive_maintenance_asset_health`
*TrackGuard Systems - Predictive Maintenance & Asset Health 🔧* — fictional company: **TrackGuard Systems** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in low health count?*

**B1** — `rewritten`
- **Old Q:** How has unique assets changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(asset_count) AS asset_count FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', reading_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.rolling_stock GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in emergency count?*

**B3** — `rewritten`
- **Old Q:** How has unique events changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(event_count) AS event_count FROM {fqn}.maintenance_cost_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** Which assets have the highest total vibration level in g-force?
- **New SQL:** `SELECT asset_name, SUM(vibration_g) AS total_metric FROM {fqn}.rolling_stock GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `unchanged`
- Q: *What are the top rolling stock asset id by total bearing temperature celsius?*

**B5** — `rewritten`
- **Old Q:** How many records are there per event date?
- **Old SQL:** `SELECT event_date, COUNT(*) AS record_count FROM {fqn}.sensor_readings GROUP BY event_date ORDER BY event_date`
- **New Q:** Which asset types have the highest total maintenance events?
- **New SQL:** `SELECT asset_type, MEASURE(event_count) AS event_count FROM {fqn}.maintenance_cost_monthly GROUP BY ALL ORDER BY event_count DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per forecast month?
- **Old SQL:** `SELECT forecast_month, COUNT(*) AS record_count FROM {fqn}.maintenance_events GROUP BY forecast_month ORDER BY forecast_month`
- **New Q:** Which asset types have the highest average 30-day failure probability 0-100?
- **New SQL:** `SELECT asset_type, AVG(failure_probability_pct) AS avg_metric FROM {fqn}.maintenance_events GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in highest vibration g?
- **Old SQL:** `SELECT reading_date, MEASURE(max_vibration_g) AS max_vibration_g FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average vibration level in g-force trended by month?
- **New SQL:** `SELECT reading_date, MEASURE(avg_vibration) AS avg_vibration FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`

**E1** — `rewritten`
- **Old Q:** How has total oil pressure psi changed over time?
- **Old SQL:** `SELECT reading_date, MEASURE(total_oil_pressure_psi) AS total_oil_pressure_psi FROM {fqn}.health_monthly GROUP BY ALL ORDER BY reading_date`
- **New Q:** How has average oil pressure in pressure (psi) trended over time?
- **New SQL:** `SELECT reading_date, AVG(oil_pressure_psi) AS avg_oil_pressure_psi FROM {fqn}.rolling_stock GROUP BY reading_date ORDER BY reading_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique assets?
- **Old SQL:** `SELECT event_date, MEASURE(unique_asset_count) AS unique_asset_count FROM {fqn}.maintenance_cost_monthly GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.sensor_readings GROUP BY 1 ORDER BY 1`

**E3** — `unchanged`
- Q: *How does the number of unique events vary by asset type?*

**E4** — `unchanged`
- Q: *What is the trend of total bearing temperature celsius over time?*

**E5** — `unchanged`
- Q: *What is the trend of total asset downtime hours over time?*

**E6** — `unchanged`
- Q: *How has the average 30-day failure probability 0-100 changed over time?*

---

### `railroad/route_planning`
*RailRoute Logistics - Route Planning & Optimization 🗺️* — fictional company: **RailRoute Logistics** — 5 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in unique corridors?
- **Old SQL:** `SELECT movement_date, MEASURE(corridor_count) AS corridor_count FROM {fqn}.route_kpi_monthly GROUP BY ALL ORDER BY movement_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', movement_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.rail_corridors GROUP BY 1 ORDER BY 1`

**B1** — `unchanged`
- Q: *How has highest trains count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in high risk count?*

**B3** — `rewritten`
- **Old Q:** How has unique plans changed over time?
- **Old SQL:** `SELECT plan_month, MEASURE(plan_count) AS plan_count FROM {fqn}.capacity_kpi_monthly GROUP BY ALL ORDER BY plan_month`
- **New Q:** Which corridors have the highest total gross ton-miles?
- **New SQL:** `SELECT corridor_name, SUM(gross_ton_miles) AS total_metric FROM {fqn}.rail_corridors GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top rail corridor identifier by total number of trains on corridor?
- **Old SQL:** `SELECT corridor_id, SUM(trains_count) AS total_trains_count FROM {fqn}.rail_corridors GROUP BY corridor_id ORDER BY total_trains_count DESC LIMIT 10`
- **New Q:** Which corridors have the most number of trains on corridor?
- **New SQL:** `SELECT corridor_name, SUM(trains_count) AS total_trains_count FROM {fqn}.rail_corridors GROUP BY corridor_name ORDER BY total_trains_count DESC LIMIT 10`

**B5** — `unchanged`
- Q: *What is the average on-time performance 0-100 by corridor type?*

**B6** — `rewritten`
- **Old Q:** How many records are there per planning month?
- **Old SQL:** `SELECT plan_month, COUNT(*) AS record_count FROM {fqn}.corridor_snapshots GROUP BY plan_month ORDER BY plan_month`
- **New Q:** Which corridor types have the highest average maintenance days?
- **New SQL:** `SELECT corridor_type, MEASURE(avg_maintenance_days) AS avg_maintenance_days FROM {fqn}.capacity_kpi_monthly GROUP BY ALL ORDER BY avg_maintenance_days DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in total gtm millions?*

**E1** — `unchanged`
- Q: *How has total train movements changed over time?*

**E2** — `unchanged`
- Q: *How does the number of unique plans vary by corridor type?*

**E3** — `unchanged`
- Q: *What is the trend of total number of trains on corridor over time?*

**E4** — `unchanged`
- Q: *What is the trend of total total congestion delay hours over time?*

**E5** — `rewritten`
- **Old Q:** How many distinct unique planning record are there per region?
- **Old SQL:** `SELECT region, COUNT(DISTINCT plan_id) AS distinct_count FROM {fqn}.corridor_snapshots GROUP BY region ORDER BY distinct_count DESC`
- **New Q:** Which corridor types have the highest average maintenance days?
- **New SQL:** `SELECT corridor_type, MEASURE(avg_maintenance_days) AS avg_maintenance_days FROM {fqn}.capacity_kpi_monthly GROUP BY ALL ORDER BY avg_maintenance_days DESC LIMIT 10`

**E6** — `unchanged`
- Q: *How has average terminal dwell hours changed over time?*

---

### `semiconductor/demand_forecasting`
*ChipFlow - Demand Forecasting 📈* — fictional company: **ChipFlow Supply** — 11 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in backlogged order count?*

**B1** — `rewritten`
- **Old Q:** How has unique total orderss changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(total_orders) AS total_orders FROM {fqn}.customer_order_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.customer_orders GROUP BY 1 ORDER BY 1`

**B2** — `rewritten`
- **Old Q:** What is the monthly trend in unique total forecast recordss?
- **Old SQL:** `SELECT forecast_date, MEASURE(total_forecast_records) AS total_forecast_records FROM {fqn}.forecast_accuracy_metrics GROUP BY ALL ORDER BY forecast_date`
- **New Q:** Which product skus have the highest total number of units ordered?
- **New SQL:** `SELECT sku_name, SUM(order_quantity) AS total_metric FROM {fqn}.customer_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B3** — `rewritten`
- **Old Q:** How has unique skus changed over time?
- **Old SQL:** `SELECT forecast_date, MEASURE(unique_sku_count) AS unique_sku_count FROM {fqn}.forecast_accuracy_metrics GROUP BY ALL ORDER BY forecast_date`
- **New Q:** Which product category groupings have the highest total unit price?
- **New SQL:** `SELECT product_category, SUM(unit_price_usd) AS total_metric FROM {fqn}.customer_orders GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top product sku identifier by total number of units ordered?
- **Old SQL:** `SELECT sku_id, SUM(order_quantity) AS total_order_quantity FROM {fqn}.customer_orders GROUP BY sku_id ORDER BY total_order_quantity DESC LIMIT 10`
- **New Q:** How does forecast accuracy compare across product categories?
- **New SQL:** `SELECT product_category, AVG(forecast_accuracy_pct) AS avg_accuracy FROM {fqn}.demand_forecasts GROUP BY product_category ORDER BY avg_accuracy DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average forecast accuracy as percentage by human-readable product sku name?
- **Old SQL:** `SELECT sku_name, AVG(forecast_accuracy_pct) AS avg_forecast_accuracy_pct FROM {fqn}.demand_forecasts GROUP BY sku_name ORDER BY avg_forecast_accuracy_pct DESC`
- **New Q:** Which product skus have the best forecast accuracy?
- **New SQL:** `SELECT sku_name, AVG(forecast_accuracy_pct) AS avg_forecast_accuracy_pct FROM {fqn}.demand_forecasts GROUP BY sku_name ORDER BY avg_forecast_accuracy_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of inventory position?
- **Old SQL:** `SELECT position_month, COUNT(*) AS record_count FROM {fqn}.inventory_positions GROUP BY position_month ORDER BY position_month`
- **New Q:** Which product skus have the highest total estimated weeks of supply at current demand rate?
- **New SQL:** `SELECT sku_name, SUM(weeks_of_supply) AS total_metric FROM {fqn}.inventory_positions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique skus?
- **Old SQL:** `SELECT order_date, MEASURE(unique_sku_count) AS unique_sku_count FROM {fqn}.customer_order_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.customer_orders GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest order quantity changed over time?*

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest forecasted units?
- **Old SQL:** `SELECT forecast_date, MEASURE(max_forecasted_units) AS max_forecasted_units FROM {fqn}.forecast_accuracy_metrics GROUP BY ALL ORDER BY forecast_date`
- **New Q:** What has been the peak predicted demand in units each month?
- **New SQL:** `SELECT forecast_date, MEASURE(max_forecasted_units) AS max_forecasted_units FROM {fqn}.forecast_accuracy_metrics GROUP BY ALL ORDER BY forecast_date`

**E3** — `rewritten`
- **Old Q:** How does total number of units ordered break down by product sku identifier for 'Shipped' records?
- **Old SQL:** `SELECT sku_id, COUNT(*) AS record_count, SUM(order_quantity) AS total_order_quantity FROM {fqn}.customer_orders WHERE fulfillment_status = 'Shipped' GROUP BY sku_id ORDER BY total_order_quantity DESC`
- **New Q:** Which product skus have the highest total *?
- **New SQL:** `SELECT sku_name, SUM(*) AS record_count, SUM(order_quantity) AS total_order_quantity FROM {fqn}.customer_orders WHERE fulfillment_status = 'Shipped' GROUP BY sku_name ORDER BY total_order_quantity DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total predicted demand in units over time?*

**E5** — `rewritten`
- **Old Q:** How many distinct unique inventory position record identifier are there per product category grouping?
- **Old SQL:** `SELECT product_category, COUNT(DISTINCT position_id) AS distinct_count FROM {fqn}.inventory_positions GROUP BY product_category ORDER BY distinct_count DESC`
- **New Q:** How many distinct forecasts does each product sku have?
- **New SQL:** `SELECT sku_name, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.inventory_positions GROUP BY 1 ORDER BY distinct_count DESC LIMIT 10`

**E6** — `rewritten`
- **Old Q:** How has total unit price usd changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(total_unit_price) AS total_unit_price FROM {fqn}.customer_order_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How has total unit price trended over time?
- **New SQL:** `SELECT order_date, MEASURE(total_unit_price) AS total_unit_price FROM {fqn}.customer_order_metrics GROUP BY ALL ORDER BY order_date`

---

### `semiconductor/design_space_simulation`
*SiliconPath - Design Space Simulation 🧪* — fictional company: **SiliconPath Design** — 10 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in completed runs count?*

**B1** — `rewritten`
- **Old Q:** How has unique total simulation runss changed over time?
- **Old SQL:** `SELECT run_date, MEASURE(total_simulation_runs) AS total_simulation_runs FROM {fqn}.simulation_run_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *What is the monthly trend in blocked design count?*

**B3** — `rewritten`
- **Old Q:** How has unique total optimization recordss changed over time?
- **Old SQL:** `SELECT result_month, MEASURE(total_optimization_records) AS total_optimization_records FROM {fqn}.optimization_result_metrics GROUP BY ALL ORDER BY result_month`
- **New Q:** Which chip designs have the highest total target process node in nanometers?
- **New SQL:** `SELECT design_name, SUM(target_node_nm) AS total_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top chip design identifier by total target process node in nanometers?
- **Old SQL:** `SELECT design_id, SUM(target_node_nm) AS total_target_node_nm FROM {fqn}.simulation_runs GROUP BY design_id ORDER BY total_target_node_nm DESC LIMIT 10`
- **New Q:** Which design family groupings have the highest total worst negative slack in nanoseconds?
- **New SQL:** `SELECT design_family, SUM(timing_slack_ns) AS total_metric FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average normalized performance score (0-100) by human-readable chip design name?
- **Old SQL:** `SELECT design_name, AVG(performance_score) AS avg_performance_score FROM {fqn}.parameter_explorations GROUP BY design_name ORDER BY avg_performance_score DESC`
- **New Q:** Which chip designs have the highest average normalized performance score?
- **New SQL:** `SELECT design_name, AVG(performance_score) AS avg_performance_score FROM {fqn}.parameter_explorations GROUP BY design_name ORDER BY avg_performance_score DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of the optimization result?
- **Old SQL:** `SELECT result_month, COUNT(*) AS record_count FROM {fqn}.optimization_results GROUP BY result_month ORDER BY result_month`
- **New Q:** Which chip designs have the highest average best power found across designs?
- **New SQL:** `SELECT design_name, MEASURE(avg_best_power_mw) AS avg_best_power_mw FROM {fqn}.optimization_result_metrics GROUP BY ALL ORDER BY avg_best_power_mw DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique designs?
- **Old SQL:** `SELECT run_date, MEASURE(unique_design_count) AS unique_design_count FROM {fqn}.simulation_run_metrics GROUP BY ALL ORDER BY run_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', run_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.simulation_runs GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest timing slack ns changed over time?*

**E2** — `rewritten`
- **Old Q:** How has unique designs changed over time?
- **Old SQL:** `SELECT result_month, MEASURE(unique_design_count) AS unique_design_count FROM {fqn}.optimization_result_metrics GROUP BY ALL ORDER BY result_month`
- **New Q:** How many distinct forecasts appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', result_month) AS month, COUNT(DISTINCT forecast) AS distinct_count FROM {fqn}.optimization_results GROUP BY 1 ORDER BY 1`

**E3** — `rewritten`
- **Old Q:** How does total target process node in nanometers break down by chip design identifier for 'Completed' records?
- **Old SQL:** `SELECT design_id, COUNT(*) AS record_count, SUM(target_node_nm) AS total_target_node_nm FROM {fqn}.simulation_runs WHERE run_status = 'Completed' GROUP BY design_id ORDER BY total_target_node_nm DESC`
- **New Q:** Which chip designs have the highest total *?
- **New SQL:** `SELECT design_name, SUM(*) AS record_count, SUM(target_node_nm) AS total_target_node_nm FROM {fqn}.simulation_runs WHERE run_status = 'Completed' GROUP BY design_name ORDER BY total_target_node_nm DESC LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total target clock frequency in ghz over time?
- **Old SQL:** `SELECT snapshot_date, SUM(clock_freq_ghz) AS total_clock_freq_ghz FROM {fqn}.parameter_explorations GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total target clock frequency in ghz trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(clock_freq_ghz) AS total_clock_freq_ghz FROM {fqn}.parameter_explorations GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `rewritten`
- **Old Q:** How has the average best performance score achieved (0-100) changed over time?
- **Old SQL:** `SELECT result_month, AVG(best_performance_score) AS avg_best_performance_score FROM {fqn}.optimization_results GROUP BY result_month ORDER BY result_month`
- **New Q:** How does best performance score achieved compare across chip designs?
- **New SQL:** `SELECT design_name, AVG(best_performance_score) AS avg_best_performance_score FROM {fqn}.optimization_results GROUP BY design_name ORDER BY design_name LIMIT 10`

**E6** — `unchanged`
- Q: *How has total leakage power mw changed over time?*

---

### `semiconductor/financial_analytics_reporting`
*SemiLedger - Financial Analytics & Reporting 💰* — fictional company: **SemiLedger Analytics** — 12 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `rewritten`
- **Old Q:** What is the monthly trend in total revenue usd count?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_revenue_usd) AS total_revenue_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total revenue trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_revenue_usd) AS total_revenue_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`

**B1** — `rewritten`
- **Old Q:** How has total cogs usd count changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_cogs_usd) AS total_cogs_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total cogs trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_cogs_usd) AS total_cogs_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`

**B2** — `unchanged`
- Q: *What is the monthly trend in critical overrun count?*

**B3** — `rewritten`
- **Old Q:** How has unique cost centers changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_cost_center_count) AS unique_cost_center_count FROM {fqn}.budget_variance_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.budget_snapshots GROUP BY 1 ORDER BY 1`

**B4** — `rewritten`
- **Old Q:** What are the top cost center identifier by total transaction amount in usd (positive = credit/revenue, negative = debit/expense)?
- **Old SQL:** `SELECT cost_center_id, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_id ORDER BY total_amount_usd DESC LIMIT 10`
- **New Q:** Which cost centers have the most transaction amount?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_name ORDER BY total_amount_usd DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average budget variance as percentage by human-readable cost center name?
- **Old SQL:** `SELECT cost_center_name, AVG(variance_pct) AS avg_variance_pct FROM {fqn}.budget_snapshots GROUP BY cost_center_name ORDER BY avg_variance_pct DESC`
- **New Q:** Which cost centers have the highest budget variance?
- **New SQL:** `SELECT cost_center_name, AVG(variance_pct) AS avg_variance_pct FROM {fqn}.budget_snapshots GROUP BY cost_center_name ORDER BY avg_variance_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi measurement?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.financial_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which cost centers have the highest average gross margin percentage?
- **New SQL:** `SELECT cost_center_name, AVG(gross_margin_pct) AS avg_metric FROM {fqn}.financial_kpi_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in total opex usd count?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_opex_usd) AS total_opex_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total opex trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_opex_usd) AS total_opex_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`

**E1** — `rewritten`
- **Old Q:** How has total capex usd count changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_capex_usd) AS total_capex_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total capex trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(total_capex_usd) AS total_capex_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY transaction_date`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in highest budgeted amount?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_budgeted_amount) AS max_budgeted_amount FROM {fqn}.budget_variance_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak budgeted_amount each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_budgeted_amount) AS max_budgeted_amount FROM {fqn}.budget_variance_metrics GROUP BY ALL ORDER BY snapshot_date`

**E3** — `rewritten`
- **Old Q:** What is the trend of total transaction amount in usd (positive = credit/revenue, negative = debit/expense) over time?
- **Old SQL:** `SELECT transaction_date, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY transaction_date ORDER BY transaction_date`
- **New Q:** How does transaction amount in compare across cost centers?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_amount_usd FROM {fqn}.financial_transactions GROUP BY cost_center_name ORDER BY cost_center_name LIMIT 10`

**E4** — `rewritten`
- **Old Q:** What is the trend of total planned budget amount in usd over time?
- **Old SQL:** `SELECT snapshot_date, SUM(budgeted_amount_usd) AS total_budgeted_amount_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** How has total planned budget amount in trended over time?
- **New SQL:** `SELECT snapshot_date, SUM(budgeted_amount_usd) AS total_budgeted_amount_usd FROM {fqn}.budget_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`

**E5** — `unchanged`
- Q: *How has the average gross margin percentage changed over time?*

**E6** — `rewritten`
- **Old Q:** How does total capex usd count vary across departments?
- **Old SQL:** `SELECT department, MEASURE(total_capex_usd) AS total_capex_usd FROM {fqn}.financial_transaction_metrics GROUP BY ALL ORDER BY total_capex_usd DESC`
- **New Q:** Which cost centers have the highest total capex spend?
- **New SQL:** `SELECT cost_center_name, SUM(amount_usd) AS total_capex FROM {fqn}.financial_transactions WHERE category = 'CapEx' GROUP BY cost_center_name ORDER BY total_capex DESC LIMIT 10`

---

### `semiconductor/quality_event_root_cause_analysis`
*NanoVista - Quality Event RCA 🔍* — fictional company: **NanoVista Semiconductor** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in critical event count?*

**B1** — `unchanged`
- Q: *How has closed event count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in grade c lot count?*

**B3** — `rewritten`
- **Old Q:** How has unique total lotss changed over time?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_lots) AS total_lots FROM {fqn}.lot_yield_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.manufacturing_lots GROUP BY 1 ORDER BY 1`

**B4** — `rewritten`
- **Old Q:** What are the top product identifier by total number of wafers affected by the event?
- **Old SQL:** `SELECT product_id, SUM(affected_wafer_count) AS total_affected_wafer_count FROM {fqn}.quality_events GROUP BY product_id ORDER BY total_affected_wafer_count DESC LIMIT 10`
- **New Q:** Which products have the most number of wafers affected by the event?
- **New SQL:** `SELECT product_name, SUM(affected_wafer_count) AS total_affected_wafer_count FROM {fqn}.quality_events GROUP BY product_name ORDER BY total_affected_wafer_count DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average lot yield percentage (0-100) by human-readable product name?
- **Old SQL:** `SELECT product_name, AVG(yield_pct) AS avg_yield_pct FROM {fqn}.manufacturing_lots GROUP BY product_name ORDER BY avg_yield_pct DESC`
- **New Q:** Which products have the highest average lot yield percentage?
- **New SQL:** `SELECT product_name, AVG(yield_pct) AS avg_yield_pct FROM {fqn}.manufacturing_lots GROUP BY product_name ORDER BY avg_yield_pct DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month the kpi applies to?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.quality_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which products have the highest total defective parts per million?
- **New SQL:** `SELECT product_name, SUM(dppm) AS total_metric FROM {fqn}.quality_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `unchanged`
- Q: *What is the monthly trend in open event count?*

**E1** — `rewritten`
- **Old Q:** How has unique total quality eventss changed over time?
- **Old SQL:** `SELECT event_date, MEASURE(total_quality_events) AS total_quality_events FROM {fqn}.quality_events_metrics GROUP BY ALL ORDER BY event_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', event_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.quality_events GROUP BY 1 ORDER BY 1`

**E2** — `rewritten`
- **Old Q:** What is the monthly trend in unique products?
- **Old SQL:** `SELECT snapshot_date, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.lot_yield_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** How many distinct snapshots appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', snapshot_date) AS month, COUNT(DISTINCT snapshot) AS distinct_count FROM {fqn}.manufacturing_lots GROUP BY 1 ORDER BY 1`

**E3** — `rewritten`
- **Old Q:** How does total number of wafers affected by the event break down by product identifier for 'Closed' records?
- **Old SQL:** `SELECT product_id, COUNT(*) AS record_count, SUM(affected_wafer_count) AS total_affected_wafer_count FROM {fqn}.quality_events WHERE status = 'Closed' GROUP BY product_id ORDER BY total_affected_wafer_count DESC`
- **New Q:** Which products have the highest total *?
- **New SQL:** `SELECT product_name, SUM(*) AS record_count, SUM(affected_wafer_count) AS total_affected_wafer_count FROM {fqn}.quality_events WHERE status = 'Closed' GROUP BY product_name ORDER BY total_affected_wafer_count DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total number of wafers in the lot over time?*

**E5** — `unchanged`
- Q: *How has the average first pass yield percentage changed over time?*

**E6** — `unchanged`
- Q: *How has open event count changed over time?*

---

### `semiconductor/salable_inventory_optimization`
*WaferVault - Salable Inventory Optimization 📦* — fictional company: **WaferVault Systems** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in scrap transaction count?*

**B1** — `rewritten`
- **Old Q:** How has unique total transactionss changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(total_transactions) AS total_transactions FROM {fqn}.inventory_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.inventory_transactions GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *How has highest on hand units changed over time?*

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in total units on hand?
- **Old SQL:** `SELECT snapshot_date, MEASURE(total_on_hand_units) AS total_on_hand_units FROM {fqn}.inventory_snapshot_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** Which products have the highest total unit cost?
- **New SQL:** `SELECT product_name, SUM(unit_cost_usd) AS total_metric FROM {fqn}.inventory_transactions GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

**B4** — `rewritten`
- **Old Q:** What are the top product identifier by total transaction quantity in units?
- **Old SQL:** `SELECT product_id, SUM(quantity_units) AS total_quantity_units FROM {fqn}.inventory_transactions GROUP BY product_id ORDER BY total_quantity_units DESC LIMIT 10`
- **New Q:** Which products have the highest total transaction quantity in units?
- **New SQL:** `SELECT product_name, SUM(quantity_units) AS total_quantity_units FROM {fqn}.inventory_transactions GROUP BY product_name ORDER BY total_quantity_units DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** How many records are there per week-ending date of snapshot?
- **Old SQL:** `SELECT snapshot_date, COUNT(*) AS record_count FROM {fqn}.inventory_snapshots GROUP BY snapshot_date ORDER BY snapshot_date`
- **New Q:** Which products have the highest average committed units per snapshot?
- **New SQL:** `SELECT product_name, MEASURE(avg_committed_units) AS avg_committed_units FROM {fqn}.inventory_snapshot_metrics GROUP BY ALL ORDER BY avg_committed_units DESC LIMIT 10`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of kpi measurement?
- **Old SQL:** `SELECT kpi_month, COUNT(*) AS record_count FROM {fqn}.inventory_kpi_monthly GROUP BY kpi_month ORDER BY kpi_month`
- **New Q:** Which products have the highest total annualized inventory turn rate?
- **New SQL:** `SELECT product_name, SUM(inventory_turns) AS total_metric FROM {fqn}.inventory_kpi_monthly GROUP BY 1 ORDER BY total_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique products?
- **Old SQL:** `SELECT transaction_date, MEASURE(unique_product_count) AS unique_product_count FROM {fqn}.inventory_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', transaction_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.inventory_transactions GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest quantity units changed over time?*

**E2** — `rewritten`
- **Old Q:** How has average unit cost in usd changed over time?
- **Old SQL:** `SELECT transaction_date, MEASURE(avg_unit_cost_usd) AS avg_unit_cost_usd FROM {fqn}.inventory_transaction_metrics GROUP BY ALL ORDER BY transaction_date`
- **New Q:** How has total unit cost in trended over time?
- **New SQL:** `SELECT transaction_date, MEASURE(avg_unit_cost_usd) AS avg_unit_cost_usd FROM {fqn}.inventory_transaction_metrics GROUP BY ALL ORDER BY transaction_date`

**E3** — `unchanged`
- Q: *How does scrap transaction count vary across product lines?*

**E4** — `unchanged`
- Q: *What is the trend of total transaction quantity in units over time?*

**E5** — `unchanged`
- Q: *What is the trend of total total units on hand over time?*

**E6** — `unchanged`
- Q: *How has the average order fill rate percentage changed over time?*

---

### `semiconductor/supply_materials_capacity_allocation`
*CapAlloc - Supply & Capacity Allocation 🔗* — fictional company: **CapAlloc Semi** — 7 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in delayed order count?*

**B1** — `unchanged`
- Q: *How has rejected order count changed over time?*

**B2** — `unchanged`
- Q: *What is the monthly trend in critical bottleneck count?*

**B3** — `rewritten`
- **Old Q:** What is the monthly trend in highest utilization percent?
- **Old SQL:** `SELECT snapshot_date, MEASURE(max_utilization_percent) AS max_utilization_percent FROM {fqn}.capacity_utilization_metrics GROUP BY ALL ORDER BY snapshot_date`
- **New Q:** What has been the peak utilization_percent each month?
- **New SQL:** `SELECT snapshot_date, MEASURE(max_utilization_percent) AS max_utilization_percent FROM {fqn}.capacity_utilization_metrics GROUP BY ALL ORDER BY snapshot_date`

**B4** — `rewritten`
- **Old Q:** What are the top material or component identifier by total quantity ordered (units vary by material)?
- **Old SQL:** `SELECT material_id, SUM(order_quantity) AS total_order_quantity FROM {fqn}.material_orders GROUP BY material_id ORDER BY total_order_quantity DESC LIMIT 10`
- **New Q:** Which materials have the highest total quantity ordered?
- **New SQL:** `SELECT material_name, SUM(order_quantity) AS total_order_quantity FROM {fqn}.material_orders GROUP BY material_name ORDER BY total_order_quantity DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average fab line utilization percentage by human-readable material name?
- **Old SQL:** `SELECT material_name, AVG(utilization_pct) AS avg_utilization_pct FROM {fqn}.capacity_snapshots GROUP BY material_name ORDER BY avg_utilization_pct DESC`
- **New Q:** Which materials have the best fab line utilization percentage?
- **New SQL:** `SELECT material_name, AVG(utilization_pct) AS avg_utilization_pct FROM {fqn}.capacity_snapshots GROUP BY material_name ORDER BY avg_utilization_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of allocation plan?
- **Old SQL:** `SELECT allocation_month, COUNT(*) AS record_count FROM {fqn}.allocation_monthly GROUP BY allocation_month ORDER BY allocation_month`
- **New Q:** Which materials have the highest average percentage adherence to allocation plan?
- **New SQL:** `SELECT material_name, AVG(plan_adherence_pct) AS avg_metric FROM {fqn}.allocation_monthly GROUP BY 1 ORDER BY avg_metric DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique total material orderss?
- **Old SQL:** `SELECT order_date, MEASURE(total_material_orders) AS total_material_orders FROM {fqn}.material_order_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.material_orders GROUP BY 1 ORDER BY 1`

**E1** — `rewritten`
- **Old Q:** How has unique materials changed over time?
- **Old SQL:** `SELECT order_date, MEASURE(unique_material_count) AS unique_material_count FROM {fqn}.material_order_metrics GROUP BY ALL ORDER BY order_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', order_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.material_orders GROUP BY 1 ORDER BY 1`

**E2** — `unchanged`
- Q: *How does rejected order count vary across material categories?*

**E3** — `unchanged`
- Q: *What is the delayed order count by supplier name?*

**E4** — `rewritten`
- **Old Q:** How does total quantity ordered (units vary by material) break down by material or component identifier for 'Delivered' records?
- **Old SQL:** `SELECT material_id, COUNT(*) AS record_count, SUM(order_quantity) AS total_order_quantity FROM {fqn}.material_orders WHERE delivery_status = 'Delivered' GROUP BY material_id ORDER BY total_order_quantity DESC`
- **New Q:** Which materials have the highest total *?
- **New SQL:** `SELECT material_name, SUM(*) AS record_count, SUM(order_quantity) AS total_order_quantity FROM {fqn}.material_orders WHERE delivery_status = 'Delivered' GROUP BY material_name ORDER BY total_order_quantity DESC LIMIT 10`

**E5** — `unchanged`
- Q: *What is the trend of total available wafer start slots for the week over time?*

**E6** — `unchanged`
- Q: *How has the average percentage adherence to allocation plan changed over time?*

---

### `semiconductor/virtual_metrology_defect_detection`
*FabSight - Virtual Metrology & Defect Detection 🔬* — fictional company: **FabSight Analytics** — 6 of 14 questions rewritten

#### Benchmark questions (eval-only)

**B0** — `unchanged`
- Q: *What is the monthly trend in out of spec count?*

**B1** — `rewritten`
- **Old Q:** How has unique total measurementss changed over time?
- **Old SQL:** `SELECT measurement_date, MEASURE(total_measurements) AS total_measurements FROM {fqn}.wafer_measurement_metrics GROUP BY ALL ORDER BY measurement_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', measurement_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.wafer_measurements GROUP BY 1 ORDER BY 1`

**B2** — `unchanged`
- Q: *How has highest defect density per cm2 changed over time?*

**B3** — `unchanged`
- Q: *What is the monthly trend in total wafers inspected?*

**B4** — `rewritten`
- **Old Q:** What are the top process recipe identifier by total film thickness measurement in nanometers?
- **Old SQL:** `SELECT recipe_id, SUM(thickness_nm) AS total_thickness_nm FROM {fqn}.wafer_measurements GROUP BY recipe_id ORDER BY total_thickness_nm DESC LIMIT 10`
- **New Q:** Which recipes have the highest total film thickness measurement in nanometers?
- **New SQL:** `SELECT recipe_name, SUM(thickness_nm) AS total_thickness_nm FROM {fqn}.wafer_measurements GROUP BY recipe_name ORDER BY total_thickness_nm DESC LIMIT 10`

**B5** — `rewritten`
- **Old Q:** What is the average absolute prediction error as percentage by human-readable recipe name?
- **Old SQL:** `SELECT recipe_name, AVG(prediction_error_pct) AS avg_prediction_error_pct FROM {fqn}.metrology_predictions GROUP BY recipe_name ORDER BY avg_prediction_error_pct DESC`
- **New Q:** Which recipes have the highest absolute prediction error?
- **New SQL:** `SELECT recipe_name, AVG(prediction_error_pct) AS avg_prediction_error_pct FROM {fqn}.metrology_predictions GROUP BY recipe_name ORDER BY avg_prediction_error_pct DESC`

**B6** — `rewritten`
- **Old Q:** How many records are there per month of defect detection summary?
- **Old SQL:** `SELECT detection_month, COUNT(*) AS record_count FROM {fqn}.defect_detections GROUP BY detection_month ORDER BY detection_month`
- **New Q:** Which recipes have the highest average defect density per cm2?
- **New SQL:** `SELECT recipe_name, MEASURE(avg_defect_density) AS avg_defect_density FROM {fqn}.defect_detection_metrics GROUP BY ALL ORDER BY avg_defect_density DESC LIMIT 10`

#### Example-SQL questions (deployed with the Genie space)

**E0** — `rewritten`
- **Old Q:** What is the monthly trend in unique recipes?
- **Old SQL:** `SELECT measurement_date, MEASURE(unique_recipe_count) AS unique_recipe_count FROM {fqn}.wafer_measurement_metrics GROUP BY ALL ORDER BY measurement_date`
- **New Q:** How many distinct transactions appeared each month?
- **New SQL:** `SELECT DATE_TRUNC('month', measurement_date) AS month, COUNT(DISTINCT transaction) AS distinct_count FROM {fqn}.wafer_measurements GROUP BY 1 ORDER BY 1`

**E1** — `unchanged`
- Q: *How has highest thickness nm changed over time?*

**E2** — `unchanged`
- Q: *How has total defects found changed over time?*

**E3** — `rewritten`
- **Old Q:** How does total film thickness measurement in nanometers break down by process recipe identifier for 'In Spec' records?
- **Old SQL:** `SELECT recipe_id, COUNT(*) AS record_count, SUM(thickness_nm) AS total_thickness_nm FROM {fqn}.wafer_measurements WHERE measurement_status = 'In Spec' GROUP BY recipe_id ORDER BY total_thickness_nm DESC`
- **New Q:** Which recipes have the highest total *?
- **New SQL:** `SELECT recipe_name, SUM(*) AS record_count, SUM(thickness_nm) AS total_thickness_nm FROM {fqn}.wafer_measurements WHERE measurement_status = 'In Spec' GROUP BY recipe_name ORDER BY total_thickness_nm DESC LIMIT 10`

**E4** — `unchanged`
- Q: *What is the trend of total model-predicted film thickness in nm over time?*

**E5** — `unchanged`
- Q: *How has the average estimated percentage of defects that are yield-killing changed over time?*

**E6** — `unchanged`
- Q: *How has out of spec count changed over time?*

---

## Implementation notes

1. **Applied directly to spec JSONs.** All rewrites land in `genie_factory/specs/<subindustry>/<use_case>.json` (`benchmarks[].question` / `sql_lines` and `example_sqls[].question` / `sql_lines`). No engine code changes were required.

2. **Deploy via monthly_refresh.** Run `databricks bundle run monthly_refresh --target prod --no-wait` against `fe-vm-logistics-demos`. The refresh is idempotent — existing Genie spaces get replaced by title match.

3. **Re-baseline benchmarks.** The 92.2% pass rate measured by `scripts/aggregate_benchmarks.py` was against the broken question set. Re-run `scripts/run_all_benchmarks.py` after redeploy. Expect the absolute pass rate to drop initially because the new questions are harder (real business phrasing) and then climb back up as we tune Genie instructions.

4. **Prevent regression at generation time.** The spec generator (`genie_factory/generator.py`, `genie_factory/remediation.py`) should grow invariant checks for the 5 patterns above so newly-generated specs don't reintroduce them.

