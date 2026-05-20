# Spec / Data Coverage Audit — All 88 Use Cases

**Date:** 2026-05-19
**Auditors:** 18 parallel subagents (one per subindustry)
**Scope:** Every `sample_question` (7) and `benchmark` (7) across all 88 spec JSONs vs. the actual data the deploy generates (tables + dimension_values + CASE/generation_expr).

---

## Headline

| Verdict | Use cases | Share |
|---|---|---|
| **CLEAN** (data answers every question) | **0** | 0% |
| **MINOR-GAPS** (1–4 weak/flat-trend Qs, demo still works) | **39** | 44% |
| **SIGNIFICANT-GAPS** (≥5 weak Qs, or ≥1 hard structural failure) | **49** | 56% |

**Total questions audited:** 1,232 (88 use cases × 14 questions)
**Total problematic questions:** **~531 / 1,232 (43%)**

Not a single use case produces demo-quality answers to all of its own sample + benchmark questions. The user-observed GOR=3 SCF/BBL result in `oil_gas_upstream / well_production_monitoring_flow` is one instance of a *systemic* issue, not a one-off.

---

## Root-cause patterns (in order of demo impact)

### 1. FLAT_TREND — pure `{qty_noise}` measures with no temporal dependency
Almost every spec puts rate/avg/percent KPIs (health_score, OEE, margin_pct, accuracy_pct, fill_rate, MTBF, RUL, GOR, CCC, etc.) through `ROUND(base + qty_noise * range, n)`. `qty_noise` is `hash(seed, salt, dt, entity) % 10000 / 10000.0` — uniform random per (date, entity), **no MONTH/YEAR dependency**. `seasonal_patterns` only changes *row selection probability*, not measure values. So:
- `AVG(measure)` by month → flat horizontal line
- `MAX(measure)` by month → saturates at the upper clamp every month
- `SUM(measure)` by month → tracks row count only

**Affected:** ~250 questions across all 88 use cases ask "monthly trend" / "month-over-month" / "trended" on a flat-noise measure. The user's GOR question is exactly this.

### 2. CORRELATED_HASH — multiple CASE columns sharing `{status_noise}`
When a spec defines several status/category columns via `CASE WHEN {status_noise} < x THEN ...`, all those columns share the same per-row hash → degenerate intersections. Worst offenders:
- **machinery/machining_process_defect_detection**: `defect_detected=true` ↔ `defect_type='None'` (inverse correlated)
- **automotive/vehicle_recall_root_cause_analysis**: `supplier_id`, `root_cause_category`, and `warranty_claims.component_code` use `{seed} % N` (no row key) — collapse to a *single constant value per deploy*
- **machinery/working_capital_cash_flow**: `direction` and `txn_type` share status_noise → Revenue rows labeled Outflow, AP Payment labeled Inflow
- **industrial_distribution/demand_forecasting**: 100% of `Backordered` orders are `MRO` segment; 0% of EMEA/APAC/LATAM are backorders
- **railroad/predictive_maintenance**: `failure_probability > 25%` AND `RUL < 90 days` are mutually exclusive by construction (same qty_noise hash, opposite bands → empty result)
- **oil_gas_midstream/working_capital**: `flow_type='Collection'` ↔ `counterparty='Customer'` ↔ positive `amount_usd` — perfectly correlated, no cross-tab variation
- **oil_gas_integrated/capital_investment_simulation**: `approval_status`+`spend_category`+`phase` cube collapses (Approved+Procurement always 0 rows)

### 3. WRONG_RANGE — filter thresholds outside the data's clamp
Questions filter on thresholds the generation_expr structurally can't produce:
- **electric_utility/transformer_asset_health**: "dissolved_gas > 1000 ppm" — clamp is `[10, 500]`
- **power_generation/solar**: "battery health < 80%" — floor is 80
- **power_generation/nuclear**: "days_since_last_inspection > 90" — ceiling is 90
- **industrial_distribution/inventory**: "days_of_supply > 120" — ceiling is 90
- **industrial_distribution/working_capital**: "CCC > 75 days" — AVG is 60, range 30–90
- **semiconductor/salable_inventory**: "days_of_supply > 180" — ceiling is 150
- **oil_gas_refining/financial**: "operating_margin < 35%" — clamp is `[-10, 35]`, all rows ≤ 35
- **oil_gas_refining/working_capital**: "current_ratio < 1.0" — clamp is `[0.8, 2.3]`, near-empty
- **mining/haul_vehicle**: "payload vs nameplate ~240t" — generated values are 500–5000 t/load (10× spec)
- **mining/production_monitoring**: throughput 100–1000 tph vs stated SAG benchmark 3–4 ktph

### 4. NO_FORECAST_DATA / WRONG_RANGE on date windows
Data ends 2025-12-31; today is 2026-05-19. Every question with "this month / this year / YTD / trailing 12 months / last 90 days / upcoming N months / next year" returns empty or sparse results. Worst-hit subindustries: **railroad** (every spec, every sample question), **power_generation/solar+wind**, **semiconductor/all**.

### 5. AGGREGATION_MISMATCH / MISSING_COLUMN
- **oil_gas_upstream/well_production_monitoring**: metric view exposes `total_gor_scf_bbl` (SUM) but no `avg_gor` — Genie computes SUM(gor)/SUM(cum_oil) ≈ 3 instead of AVG(gor) ≈ 2750. **This is the user's reported issue.**
- **computer_electronic/visual_defect_detection**: `false_positive_count` on snapshots, `inspection_station` on events — no shared key, "FP by station" unanswerable
- **machinery/production_monitoring**: OEE on `oee_monthly` has no `shift` column — "OEE by shift" unanswerable
- **machinery/field_service**: no per-ticket SLA-breach flag — "unresolved beyond SLA" unanswerable
- **virtual_metrology**: no "CD uniformity %" column
- **electric_utility/transformer**: no "customer-minutes interrupted" column
- **semiconductor/financial**: SUM(amount_usd) mixes positive Revenue + negative expense rows → ranking incoherent
- **machinery/financial**: `open_financial_transaction_count` filters `posting_status='Open'` but that value is never generated

### 6. Top-N vs cardinality mismatch
"Top 10 X" where the dim has ≤ 7 values: top-10 suppliers (7), top-10 product lines (5), top-10 regions (5), top-10 tools (6), top-10 GL categories (5), top-10 departments (5), top-10 crew types (5).

---

## Subindustry summary

| Subindustry | Use cases | Problematic Qs / Total | Significant | Minor |
|---|---:|---:|---:|---:|
| aerospace | 8 | 49 / 112 | 1 | 7 |
| automotive | 4 | 16 / 56 | 1 | 2 |
| chemicals_materials | 4 | 13 / 56 | 0 | 4 |
| computer_electronic | 3 | 15 / 42 | 1 | 2 |
| construction_engineering | 2 | 15 / 28 | 1 | 1 |
| electric_utility | 4 | 34 / 56 | 4 | 0 |
| food_beverage | 4 | 23 / 56 | 1 | 3 |
| industrial_distribution | 3 | 17 / 42 | 3 | 0 |
| logistics | 3 | 21 / 42 | 0 | 3 |
| machinery | 11 | 27 / 154 | 4 | 7 |
| mining | 2 | 14 / 28 | 2 | 0 |
| oil_gas_integrated | 6 | 28 / 84 | 2 | 4 |
| oil_gas_midstream | 8 | 51 / 112 | 6 | 2 |
| oil_gas_refining | 6 | 26 / 84 | 3 | 3 |
| oil_gas_upstream | 3 | 26 / 42 | 3 | 0 |
| power_generation | 7 | 55 / 98 | 6 | 1 |
| railroad | 3 | 28 / 42 | 3 | 0 |
| semiconductor | 7 | 73 / 98 | 7 | 0 |
| **TOTAL** | **88** | **~531 / 1,232 (43%)** | **49** | **39** |

---

## Hard-failure use cases (SIGNIFICANT-GAPS — 49 of 88)

These have ≥1 structural failure beyond just flat-trend noise — questions that produce empty results, wrong answers, or aggregation contradictions:

### Tier 1: Multi-failure (priority to fix first)
1. **semiconductor / all 7** — universal flat-noise KPIs, 73/98 questions weak/broken
2. **power_generation / solar_optimization_behind_the_meter** — battery health<80% empty (floor=80), inverter status enum mismatch, 7/7 sample Qs problematic
3. **power_generation / wind_optimization** — filter thresholds match ~80% of rows, no temporal multipliers, SUM(avg_wind_speed) benchmark is meaningless
4. **power_generation / nuclear_safety** — days_since_inspection>90 empty (ceiling=90), 8/14 Qs flat
5. **railroad / all 3** — every sample question anchored to 2026 dates (no data); pred_maint Q3 mutually-exclusive filter (empty by construction)
6. **electric_utility / all 4** — pervasive flat-noise on SAIDI/SAIFI/carbon/curtailment/renewable share; transformer dissolved_gas threshold unreachable; "customer-minutes interrupted" column missing
7. **oil_gas_midstream / 6 of 8** — no seasonal_patterns at all in financial/regulation/scenario/spend/working_capital specs → every trend is flat
8. **oil_gas_upstream / all 3** — well_production GOR aggregation mismatch (user's reported issue); LOE YTD empty (2026); reservoir trends flat
9. **mining / both** — haul_vehicle payload ~2750t vs 240t nameplate; production throughput an order of magnitude below stated benchmarks
10. **industrial_distribution / all 3** — shared qty_noise across measures (on_hand=reorder, AR=AP=inventory, inflow=outflow); empty threshold filters

### Tier 2: Single hard failure
- **automotive / vehicle_recall_root_cause_analysis** — supplier_id, root_cause, component_code use `{seed} % N` (no row key) → constant value per deploy → "top suppliers" returns 1 row
- **computer_electronic / visual_defect_detection** — false_positive by station is structurally impossible (different tables, no key)
- **construction_engineering / engineering_bid_creation** — most domain KPIs uniform across categories/regions, no signal
- **food_beverage / scenario_planning** — demand_elasticity always positive (engineered backwards), genie_instructions name wrong investment_priority values
- **aerospace / supply_materials_planning** — lead time / DOS / OTD all uniform across regions/materials
- **machinery / 4 specs** — defect_detected↔defect_type inversion, OEE-by-shift impossible, cancellation-by-region single bucket, direction↔txn_type backwards
- **oil_gas_integrated / 2 specs** — MAX-of-noise trends saturate; per-snapshot flicker on "which X exceeds threshold"
- **oil_gas_refining / 3 specs** — bounded floors invalidate threshold filters, planned/actual share qty_noise (variance is fake)

---

## Specific answer to the user's example

> *"How has average GOR trended month over month across horizontal wells?" returned ~3 SCF/BBL flat*

**Root cause:** `oil_gas_upstream/well_production_monitoring_flow.json`'s `well_status_snapshots_metrics` metric view exposes `total_gor_scf_bbl` (SUM) but **no `avg_gor` measure**. Genie's planner saw the only GOR aggregate available was a SUM, and likely emitted something like `SUM(gor_scf_bbl) / COUNT(*)` or `SUM(gor_scf_bbl) / SUM(cumulative_oil_bbl)` — the latter gives ~3 because cumulative oil is ~1M and GOR sums to ~3M. The correct AVG would be ~2750 SCF/BBL.

**Fix:** add `avg_gor_scf_bbl` measure (`AVG(gor_scf_bbl)`) to the metric view; also add MONTH-based seasonality to `gor_scf_bbl` if you want a real *trend* (currently uniform noise → trend would still be flat even with correct AVG).

---

## Recommended remediation themes

1. **Add temporal dependency to headline KPIs** — multiply `qty_noise` by `(1 + 0.15 * sin(2π * MONTH(dt) / 12))` or similar for measures referenced in "trend" questions. Cheap, high impact.
2. **Replace `{seed} % N` generation patterns with `{status_noise}`-thresholded CASEs** — fixes the vehicle_recall constant-supplier bug.
3. **Split shared `{status_noise}` across CASE columns** — use a second hash salt (e.g. `pmod(hash(seed, 'altstatus', dt, entity), 10000)/10000.0`) for the second column in any spec that has two correlated CASEs. Fixes ~30 use cases.
4. **Adjust generation_expr clamps to span the thresholds questions ask about** — battery health < 80, days_since_inspection > 90, payload nameplate, dissolved gas warning, current ratio < 1.0, etc.
5. **Add `avg_*` measures wherever a `total_*` measure is the only aggregate exposed** — fixes the GOR issue and several others.
6. **Replace date-anchored questions** ("this month / last 90 days / YTD / next year") with windows that land inside 2023–2025 — OR extend the data range to current year (`start_year = current_year() - scale + 1` in `_start_year`).
7. **Remove `MAX(*)` benchmark trends** — they saturate at the clamp every period and produce flat lines.
8. **Right-size "Top 10" to actual dim cardinality** — say "rank suppliers" instead of "top 10 suppliers" when only 7 exist.

Detailed per-spec findings preserved in agent reports above.
