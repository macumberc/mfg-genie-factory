# Repo Cleanup + JIRA Project-Management Use Case — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the loose benchmark run-outputs from the repo root (hardening `.gitignore`), and add one new preset Genie space — "Software Delivery Project Management" (JIRA-style PM data) under the Electric Utility subindustry — deployable additively to the running app.

**Architecture:** The factory represents each use case as a `DomainSpec` JSON under `genie_factory/specs/<subindustry_slug>/<use_case_slug>.json` plus a one-line entry in `genie_factory/presets.py`. The app and notebook enrich from the spec at import and deploy exactly one schema + Genie space per card. No engine code changes; this is spec authoring + taxonomy registration + cleanup.

**Tech Stack:** Python 3.11 (for local Databricks Connect validation), `genie_factory` package, Spark SQL dialect for all generation/benchmark SQL, JSON specs.

## Global Constraints

- **Spec JSON must round-trip** through `genie_factory.generator.DomainSpec.from_dict()` / `to_dict()` without error.
- **3 tables** (archetypes transaction / snapshot / monthly-KPI), **2 metric views**. (Preset deploys do NOT run `_validate_domain_spec`, which would demand 3 metric views — the corpus ships 3 tables + 2 metric views and validates via the SQL builders instead.)
- **All SQL is Spark SQL dialect** — no T-SQL (`DATEADD`, `GETDATE`, `TOP N`). Use `DATE_TRUNC`, `CURRENT_DATE()`, `date_sub`, `LIMIT`.
- **`{seed}%N` is forbidden** in `generation_expr` — `_validate_no_seed_modulo` rejects it at build time. Use `{id_seq}%N` for per-row variation.
- **Monthly-trend benchmark/example questions** must wrap the date column in `DATE_TRUNC('month', <date_col>)`.
- **Top-N benchmark questions** must say "Top 10" and use `LIMIT 10`.
- **`benchmarks` / `example_sqls`** items are `{question, sql_lines}` where `sql_lines` is an array, one SQL keyword per line. NOT a `sql` string.
- **`sql_snippets`** items use keys `display_name` and `alias` (NOT `name`), plus `sql`, `synonyms`, `instruction`.
- **`space_description`** is rendered by `genie_factory.specs.render_space_description(scenario, questions)` — Scenario/Questions format, questions annotated `(agent)`; `sample_questions` = same questions minus `(agent)`.
- **Do NOT prepend anything to `genie_instructions`** beyond directive bullets.
- **No UC tags on schema/tables.** Tagging is Genie-space-only; the spec carries `mfg_subindustry` / `mfg_outcome_usecase` inline.
- **`ColumnSpec` extra fields** default `[]`: `synonyms`, `entity_values`. **`ExampleSQL`** extra field default `""`: `usage_guidance`.
- **Assignees are full names**; a `genie_instructions` bullet + column synonyms map bare first names (e.g. "Bob") to full names (e.g. "Bob Chen").
- **Commit identity:** personal GitHub identity `macumberc`; no `Co-authored-by` trailers.

---

## File Structure

- `genie_factory/specs/electric_utility/software_delivery_project_management.json` — **create.** The new DomainSpec.
- `genie_factory/presets.py` — **modify.** Add one use-case dict to `USE_CASES["Electric Utility"]`.
- `genie_factory/tagging.py` — **modify.** Add outcome to `ALLOWED_OUTCOMES` and to `OUTCOME_USECASE_MAP["electric_utility"]`.
- `.gitignore` — **modify.** Add `benchmark_*` output patterns.
- Repo root `benchmark_20260526_*` (28 files) — **delete.**

No test files: this repo has no pytest suite for specs. Verification is via importable Python checks (spec round-trip, SQL-builder run, presets resolution, populate dry-run) run as inline `python3 -c` / `python -m` commands.

---

## Task 1: Repo cleanup — delete benchmark outputs, harden .gitignore

**Files:**
- Delete: all repo-root `benchmark_20260526_*` (28 tracked files)
- Modify: `.gitignore`

**Interfaces:**
- Consumes: nothing.
- Produces: nothing consumed by later tasks. Independent.

- [ ] **Step 1: Confirm the exact set of files to delete**

Run:
```bash
cd /Users/chad.macumber/code/mfg-genie-factory
git ls-files | grep -c '^benchmark_20260526_'   # expect 28
git ls-files | grep '^benchmark_20260526_'
```
Expected: 28 files, all matching `benchmark_20260526_*` at the root. If the count differs, stop and reconcile against the design doc before deleting.

- [ ] **Step 2: Verify nothing in code/config references these files**

Run:
```bash
grep -rIl "benchmark_20260526" --include="*.py" --include="*.yml" --include="*.sh" --include="*.toml" . | grep -v '^./benchmark_20260526'
```
Expected: no output (the only cross-references are among the benchmark markdowns themselves, which are all being deleted).

- [ ] **Step 3: Delete the tracked benchmark output files**

Run:
```bash
git rm --quiet benchmark_20260526_*
```
Expected: 28 deletions staged.

- [ ] **Step 4: Harden `.gitignore`**

In `.gitignore`, under the `# Test runs & benchmark outputs` section, replace:
```
# Test runs & benchmark outputs
test_results_*.json
benchmark_baseline_*.jsonl
benchmark_baseline_*_summary.json
```
with:
```
# Test runs & benchmark outputs
test_results_*.json
benchmark_baseline_*.jsonl
benchmark_baseline_*_summary.json
benchmark_*.jsonl
benchmark_*.md
benchmark_*.json
benchmark_*.log
```

- [ ] **Step 5: Verify the ignore patterns catch a synthetic run file and don't catch tracked source**

Run:
```bash
git check-ignore benchmark_99999999_120000.jsonl benchmark_99999999_120000.md benchmark_99999999_120000_actions.json benchmark_99999999_120000.log
git check-ignore README.md databricks.yml 2>/dev/null; echo "exit=$?"
```
Expected: the four `benchmark_*` names are echoed back (ignored); `README.md`/`databricks.yml` produce no output and `exit=1` (NOT ignored).

- [ ] **Step 6: Commit**

Run:
```bash
git add .gitignore
git commit -m "chore: delete benchmark run outputs from repo root, harden .gitignore"
```

---

## Task 2: Register the new outcome in the tagging taxonomy

Do this **before** authoring the spec so the inline tag value is validated against a real allowlist entry and `--populate-specs` maps (not blanks) it.

**Files:**
- Modify: `genie_factory/tagging.py` — `ALLOWED_OUTCOMES` set (~line 71) and `OUTCOME_USECASE_MAP["electric_utility"]` dict (~line 135)

**Interfaces:**
- Consumes: nothing.
- Produces: taxonomy value string `"Software Delivery & Project Management"`, and the slug→outcome mapping `("electric_utility", "software_delivery_project_management") -> "Software Delivery & Project Management"`. Task 3 uses this exact string as the spec's `mfg_outcome_usecase`. Task 5 verifies the mapping.

- [ ] **Step 1: Add the outcome to `ALLOWED_OUTCOMES`**

In `genie_factory/tagging.py`, inside the `ALLOWED_OUTCOMES = { ... }` set, append after the last existing entry (`"Regulation Compliance, & External Reporting",`):
```python
    # Software-delivery / PMO use case (JIRA project-management space).
    "Software Delivery & Project Management",
```

- [ ] **Step 2: Add the slug mapping under `electric_utility`**

In `OUTCOME_USECASE_MAP`, the `"electric_utility": { ... }` dict currently has four entries. Add:
```python
        "software_delivery_project_management": "Software Delivery & Project Management",
```
so the block reads:
```python
    "electric_utility": {
        "demand_forecasting": "Demand Forecasting",
        "grid_management_energy_mix": "Operations Resource Efficiency",  # (loose)
        "outage_response": "Incident & Field Service Assistant",
        "transformer_asset_health": "Predictive Maintenance & Asset Health",
        "software_delivery_project_management": "Software Delivery & Project Management",
    },
```

- [ ] **Step 3: Verify the additions import cleanly and are wired**

Run:
```bash
python3 -c "
from genie_factory.tagging import ALLOWED_OUTCOMES, OUTCOME_USECASE_MAP
assert 'Software Delivery & Project Management' in ALLOWED_OUTCOMES
assert OUTCOME_USECASE_MAP['electric_utility']['software_delivery_project_management'] == 'Software Delivery & Project Management'
print('tagging taxonomy OK')
"
```
Expected: `tagging taxonomy OK`.

- [ ] **Step 4: Commit**

Run:
```bash
git add genie_factory/tagging.py
git commit -m "feat: register Software Delivery & Project Management outcome tag"
```

---

## Task 3: Author the JIRA project-management spec JSON

This is the core deliverable. Author the full `DomainSpec` JSON, then verify it round-trips and that its generation SQL + metric-view SQL build offline (which runs the expr and seed-modulo validators).

**Files:**
- Create: `genie_factory/specs/electric_utility/software_delivery_project_management.json`

**Interfaces:**
- Consumes: outcome string from Task 2 (`"Software Delivery & Project Management"`).
- Produces: a spec loadable via `genie_factory.specs.load_spec("Electric Utility", "Software Delivery Project Management")` (slug `software_delivery_project_management`). Task 4 and Task 5 depend on this file existing and round-tripping.

**Spec contract (top-level keys, all required):**
`company_name, industry, use_case, space_title, space_description, schema_basename, tables, metric_views, genie_instructions, sample_questions, example_sqls, sql_snippets, benchmarks, mfg_subindustry, mfg_outcome_usecase`.

Fixed top-level values:
```json
"company_name": "Meridian Grid",
"industry": "Electric Utility",
"use_case": "Software delivery portfolio tracking, sprint execution, and blocker/risk management across utility technology programs",
"space_title": "Meridian Grid - Software Delivery Project Management 🗂️",
"schema_basename": "utility_project_management",
"mfg_subindustry": "Electric Utility",
"mfg_outcome_usecase": "Software Delivery & Project Management"
```

- [ ] **Step 1: Build the spec dict in a scratch author script**

Author the spec in a Python script (not committed) so the arrays are generated consistently, then dump to JSON. Create `/tmp/author_jira_spec.py`. It must construct a dict with the structure below and write it via `json.dump(spec, f, indent=2)` (mirrors `save_spec`). Use these table definitions (per the design doc):

**Table 1 — `jira_worklogs`** (`entity_dimension: "transaction"`), 11 columns. Dimension columns (`is_dimension: true`, empty `generation_expr` — values come from `dimension_values`): `issue_key`, `project`, `epic`, `assignee`. Non-dimension columns with `generation_expr`:
```
worklog_id      STRING  CONCAT('WL-', LPAD(CAST({id_seq} AS STRING), 7, '0'))
work_date       DATE    d.dt
issue_type      STRING  CASE WHEN {status_noise} < 0.42 THEN 'Story' WHEN {status_noise} < 0.60 THEN 'Bug' WHEN {status_noise} < 0.74 THEN 'Task' WHEN {status_noise} < 0.86 THEN 'Feature' WHEN {status_noise} < 0.94 THEN 'Sub-task' ELSE 'Epic' END
team            STRING  CASE WHEN {alt_status_noise} < 0.24 THEN 'Platform' WHEN {alt_status_noise} < 0.44 THEN 'Data' WHEN {alt_status_noise} < 0.62 THEN 'Field Systems' WHEN {alt_status_noise} < 0.82 THEN 'Customer Apps' ELSE 'SRE' END
hours_logged    DOUBLE  ROUND(0.5 + ({qty_noise} * 7.5), 2)
status_at_log   STRING  CASE WHEN {alt_status_noise2} < 0.30 THEN 'In Progress' WHEN {alt_status_noise2} < 0.55 THEN 'In Review' WHEN {alt_status_noise2} < 0.75 THEN 'To Do' WHEN {alt_status_noise2} < 0.90 THEN 'Done' ELSE 'Blocked' END
is_resolved     INT     CAST(CASE WHEN {status_noise} < 0.18 THEN 1 ELSE 0 END AS INT)
```
`dimension_values`: 20 rows, each `{"issue_key": "GRID-1001", "project": "Grid Modernization", "epic": "<epic>", "assignee": "<full name>"}`. Spread across the 7 projects (Grid Modernization/GRID, AMI Rollout/AMI, Outage Management System/OMS, DERMS/DERMS, Customer Portal/PORTAL, SCADA Upgrade/SCADA, EV Charging Network/EVSE), each with a plausible epic, and assignees drawn from the full-name roster (include **"Bob Chen"**). Give the `assignee`, `project`, `issue_type`, and `epic` columns `synonyms` and `entity_values` (entity_values = the distinct values that appear).

**Table 2 — `jira_issue_snapshots`** (`entity_dimension: "snapshot"`), 12 columns. Dimension columns: `issue_key`, `project`, `epic`, `sprint`, `assignee`. Non-dimension:
```
snapshot_id     STRING  CONCAT('IS-', LPAD(CAST(ROW_NUMBER() OVER (ORDER BY d.dt, e.issue_key) AS STRING), 7, '0'))
snapshot_date   DATE    d.dt
status          STRING  CASE WHEN {status_noise} < 0.20 THEN 'Backlog' WHEN {status_noise} < 0.36 THEN 'To Do' WHEN {status_noise} < 0.60 THEN 'In Progress' WHEN {status_noise} < 0.74 THEN 'In Review' WHEN {status_noise} < 0.86 THEN 'Blocked' ELSE 'Done' END
priority        STRING  CASE WHEN {alt_status_noise} < 0.12 THEN 'Highest' WHEN {alt_status_noise} < 0.38 THEN 'High' WHEN {alt_status_noise} < 0.75 THEN 'Medium' ELSE 'Low' END
risk_level      STRING  CASE WHEN {alt_status_noise2} < 0.22 THEN 'High' WHEN {alt_status_noise2} < 0.55 THEN 'Medium' ELSE 'Low' END
is_blocker      INT     CAST(CASE WHEN {status_noise} < 0.14 THEN 1 ELSE 0 END AS INT)
days_in_status  INT     CAST(1 + FLOOR({qty_noise} * 44) AS INT)
story_points    INT     CAST(ELEMENT_AT(ARRAY(1,2,3,5,8,13), 1 + CAST(FLOOR({qty_noise2} * 6) AS INT)) AS INT)
```
`dimension_values`: 20 rows `{"issue_key": ..., "project": ..., "epic": ..., "sprint": "GRID Sprint 24", "assignee": ...}`. Reuse the same projects/epics/assignees; add a `sprint` per project. Add `synonyms`/`entity_values` on `project`, `sprint`, `assignee`, `epic`.

**Table 3 — `sprint_velocity_monthly`** (`entity_dimension: "forecast"`), 11 columns. Dimension columns: `project`, `sprint`, `team`. Non-dimension:
```
record_id             STRING  CONCAT('SV-', LPAD(CAST(ROW_NUMBER() OVER (ORDER BY d.dt, e.sprint) AS STRING), 7, '0'))
report_month          DATE    DATE_TRUNC('month', d.dt)
committed_points      INT     CAST(20 + FLOOR({qty_noise} * 40) AS INT)
completed_points      INT     CAST(15 + FLOOR({qty_noise2} * 40) AS INT)
velocity              DOUBLE  ROUND((15.0 + ({qty_noise2} * 40.0)) / (20.0 + ({qty_noise} * 40.0)) * 100.0, 1)
features_deployed     INT     CAST(FLOOR(({qty_noise} * {seasonal_mult}) * 6) AS INT)
bugs_closed           INT     CAST(2 + FLOOR({qty_noise2} * 18) AS INT)
avg_cycle_time_days   DOUBLE  ROUND(3.0 + (({qty_noise} * {seasonal_mult}) * 12.0), 1)
blocker_count         INT     CAST(FLOOR({status_noise} * 6) AS INT)
```
Give `avg_cycle_time_days` and `features_deployed` a `seasonal_amplitude: 0.15` (they use `{seasonal_mult}`, which resolves to `1.0` without it — set the amplitude so the trend is real). `dimension_values`: 20 rows `{"project": ..., "sprint": ..., "team": ...}`. Add `synonyms`/`entity_values` on `project`, `sprint`, `team`.

Each table also needs `seasonal_patterns` (dict; may be `{}`) and `category_distribution` (dict; may be `{}`) keys to match the corpus shape — set both to `{}` if not modeling seasonality on that table (table 3 carries its trend via `seasonal_amplitude` instead).

**Metric views (2):**
```
jira_worklogs_metrics       source jira_worklogs
  dimensions: work_date, project, epic, issue_type, assignee, team
  measures:
    worklog_count            COUNT(worklog_id)
    total_hours_logged       SUM(hours_logged)
    story_hours              SUM(CASE WHEN issue_type = 'Story' THEN hours_logged ELSE 0 END)
    resolved_issue_count     SUM(is_resolved)
    distinct_issue_count     COUNT(DISTINCT issue_key)
    distinct_assignee_count  COUNT(DISTINCT assignee)
jira_issue_snapshots_metrics  source jira_issue_snapshots
  dimensions: snapshot_date, project, epic, sprint, assignee, status, priority, risk_level
  measures:
    open_issue_count         COUNT(DISTINCT issue_key)
    blocker_count            SUM(is_blocker)
    high_risk_blocker_count  SUM(CASE WHEN is_blocker = 1 AND risk_level = 'High' THEN 1 ELSE 0 END)
    avg_days_in_status       AVG(days_in_status)
    max_days_in_status       MAX(days_in_status)
    total_story_points       SUM(story_points)
```
(The engine auto-synthesizes AVG companions for bare `SUM(col)` measures — do not add them manually.)

**`space_description`:** build it by calling `render_space_description(scenario, questions)` inside the author script, where:
- `scenario` = 2–3 second-person sentences putting the SA in the delivery-lead seat at Meridian Grid, ending in a provocative question. Example spine: "You run software delivery at Meridian Grid, where the Grid Modernization and AMI Rollout programs are both mid-sprint and the PUC-facing commitments don't move. Blockers are piling up on a handful of epics, tickets are aging in review, and your next steering readout is tomorrow. Where do you focus to protect the sprint?"
- `questions` = the 3-question arc (opener → composition → payoff):
  1. `DEMO_OPENER_QUESTION` (import it from `genie_factory.specs`)
  2. "What are the open blockers flagged High risk by project and epic, and how many days has each been stuck in its current status?"
  3. "Which epics have the most high-risk blockers and the longest average time-in-status, and how does that compare to their sprint velocity?"

**`sample_questions`:** the same 3 questions verbatim (opener + the two above), no `(agent)` suffix.

**`genie_instructions`:** a single string of directive bullets — DOMAIN CONTEXT (Meridian Grid software-delivery PMO on JIRA; stakeholders: delivery leads, scrum masters, program managers), METRIC DEFINITIONS (velocity = completed/committed points; blocker = is_blocker=1; high-risk blocker = is_blocker=1 AND risk_level='High'; cycle time = avg_cycle_time_days; "stuck" = high days_in_status), a bullet: "Assignees are stored as full names; map a bare first name to the full name (e.g. 'Bob' -> 'Bob Chen', 'Priya' -> 'Priya Nair').", and the standard bullet: "When the user's phrasing matches a SQL snippet display name (filters, expressions, or measures), prefer that snippet." Do NOT prepend any "Deployed by" text.

**`example_sqls` (7 items, `{question, sql_lines, usage_guidance}`):** 4 MEASURE-based over metric views + 3 plain-table (one per base table). Use `{fqn}` placeholder. Cover the corpus's canonical probes plus this domain. Include at least one monthly-trend example using `DATE_TRUNC('month', ...)`. The 3 plain-table queries: one per base table (`jira_worklogs`, `jira_issue_snapshots`, `sprint_velocity_monthly`); use AVG for rate/pct columns (velocity, avg_cycle_time_days) and SUM for counts/hours.

**`benchmarks` (7 items, `{question, sql_lines}`):** 4 MEASURE + 3 plain-table, covering the six demo questions + opener:
  1. (monthly trend) "What is the monthly trend in features deployed?" — `SELECT report_month, SUM(features_deployed) ... FROM {fqn}.sprint_velocity_monthly GROUP BY 1 ORDER BY 1` with `DATE_TRUNC` not needed since `report_month` is already month-grain (it IS the trunc'd column) — keep `report_month` as the group key.
  2. (blockers/risk) high_risk_blocker_count by project via `jira_issue_snapshots_metrics` with `MEASURE(...)`.
  3. (stuck) "Top 10 issues by days stuck in status" — plain table on `jira_issue_snapshots`, `ORDER BY days_in_status DESC`, `LIMIT 10`.
  4. (features last quarter) SUM(features_deployed) filtered to last quarter on `sprint_velocity_monthly`.
  5. (sprint progress) committed vs completed points by sprint on `sprint_velocity_monthly`.
  6. (Bob's story hours) MEASURE(story_hours) or SUM(hours_logged) where assignee='Bob Chen' AND issue_type='Story' AND work_date >= date_sub(current_date(), 14) on `jira_worklogs` / metrics.
  7. (a MEASURE aggregate) total_hours_logged by team via `jira_worklogs_metrics`.

**`sql_snippets` (dict with `filters`, `expressions`, `measures`):**
- filters (3): high-risk blockers (`jira_issue_snapshots.is_blocker = 1 AND jira_issue_snapshots.risk_level = 'High'`), stories (`jira_worklogs.issue_type = 'Story'`), stuck issues (`jira_issue_snapshots.days_in_status > 14`).
- expressions (3): report month (`DATE_TRUNC('month', jira_worklogs.work_date)`), sprint completion pct (`sprint_velocity_monthly.completed_points / sprint_velocity_monthly.committed_points * 100`), cycle-time bucket (a `CASE` on `sprint_velocity_monthly.avg_cycle_time_days`).
- measures (4): total_hours_logged, high_risk_blocker_count, avg_days_in_status, features_deployed — each `{display_name, alias, sql, synonyms, instruction}`.

- [ ] **Step 2: Generate the JSON file**

Run:
```bash
cd /Users/chad.macumber/code/mfg-genie-factory
PYTHONPATH=. python3 /tmp/author_jira_spec.py
```
Expected: writes `genie_factory/specs/electric_utility/software_delivery_project_management.json`, prints the path and byte size.

- [ ] **Step 3: Verify the spec round-trips through DomainSpec**

Run:
```bash
PYTHONPATH=. python3 -c "
import json
from genie_factory.generator import DomainSpec
from genie_factory.specs import load_spec
spec = load_spec('Electric Utility', 'Software Delivery Project Management')
assert spec is not None, 'load_spec returned None — slug mismatch'
assert len(spec.tables) == 3, f'{len(spec.tables)} tables'
assert len(spec.metric_views) == 2, f'{len(spec.metric_views)} metric views'
assert len(spec.sample_questions) == 3
assert len(spec.example_sqls) == 7
assert len(spec.benchmarks) == 7
assert spec.mfg_outcome_usecase == 'Software Delivery & Project Management'
# round-trip
d = spec.to_dict(); DomainSpec.from_dict(d)
print('spec round-trip OK')
"
```
Expected: `spec round-trip OK`. If `load_spec` returns None, the filename slug doesn't match `_slugify('Software Delivery Project Management')` = `software_delivery_project_management` — rename the file.

- [ ] **Step 4: Verify generation SQL and metric-view SQL build (runs expr + seed-modulo validators offline, no Spark)**

Run:
```bash
PYTHONPATH=. python3 -c "
from genie_factory.specs import load_spec
from genie_factory.data import build_table_sqls_from_spec, build_metric_view_sqls_from_spec
spec = load_spec('Electric Utility', 'Software Delivery Project Management')
t = build_table_sqls_from_spec(spec, 'cat.sch', seed=42, scale=3, target_rows=5000)
m = build_metric_view_sqls_from_spec(spec, 'cat.sch')
assert set(t) == {'jira_worklogs','jira_issue_snapshots','sprint_velocity_monthly'}, set(t)
assert set(m) == {'jira_worklogs_metrics','jira_issue_snapshots_metrics'}, set(m)
# forbidden pattern guard
import re
for name, sql in t.items():
    assert 'DATEADD' not in sql.upper() and 'GETDATE' not in sql.upper(), name
print('table+metric SQL build OK')
"
```
Expected: `table+metric SQL build OK`. Any `{seed}%N`, unbalanced expr, or bad placeholder raises here — fix the offending `generation_expr` in `/tmp/author_jira_spec.py` and regenerate.

- [ ] **Step 5: Verify SQL snippet keys and benchmark shape**

Run:
```bash
PYTHONPATH=. python3 -c "
from genie_factory.specs import load_spec
spec = load_spec('Electric Utility', 'Software Delivery Project Management')
d = spec.to_dict()
sn = d['sql_snippets']
for grp in ('filters','expressions','measures'):
    for item in sn[grp]:
        assert 'display_name' in item and 'sql' in item, (grp, item)
        if grp != 'filters':
            pass
for item in sn['measures']:
    assert 'alias' in item, item
for b in d['benchmarks'] + d['example_sqls']:
    assert isinstance(b['sql_lines'], list) and 'sql' not in b, b['question']
# top-N convention
tops = [b for b in d['benchmarks'] if 'top 10' in b['question'].lower()]
for b in tops:
    assert any('LIMIT 10' in ln.upper() for ln in b['sql_lines']), b['question']
print('snippet + benchmark shape OK')
"
```
Expected: `snippet + benchmark shape OK`.

- [ ] **Step 6: Commit**

Run:
```bash
git add genie_factory/specs/electric_utility/software_delivery_project_management.json
git commit -m "feat: add Software Delivery Project Management JIRA spec (Electric Utility)"
```

---

## Task 4: Wire the preset entry

**Files:**
- Modify: `genie_factory/presets.py` — `USE_CASES["Electric Utility"]` list

**Interfaces:**
- Consumes: the spec file from Task 3 (via slug match) and the label `"Software Delivery Project Management"`.
- Produces: a resolvable preset that the root app `presets.py` enriches into `SUBINDUSTRY_USE_CASES["Electric Utility"]`. Task 5 verifies enrichment.

- [ ] **Step 1: Add the use-case dict**

In `genie_factory/presets.py`, the `"Electric Utility"` list currently ends with the Outage Response entry. Append:
```python
        {"label": "Software Delivery Project Management", "use_case": "Software delivery portfolio tracking, sprint execution, and blocker/risk management across utility technology programs", "importance": 8},
```

- [ ] **Step 2: Verify the label resolves to the spec**

Run:
```bash
PYTHONPATH=. python3 -c "
from genie_factory.presets import USE_CASES
from genie_factory.specs import load_spec, spec_exists
labels = [uc['label'] for uc in USE_CASES['Electric Utility']]
assert 'Software Delivery Project Management' in labels, labels
assert spec_exists('Electric Utility', 'Software Delivery Project Management')
print('preset wired + spec resolves')
"
```
Expected: `preset wired + spec resolves`.

- [ ] **Step 3: Commit**

Run:
```bash
git add genie_factory/presets.py
git commit -m "feat: list Software Delivery Project Management under Electric Utility"
```

---

## Task 5: End-to-end verification of additive wiring

No new files. This task proves the app enrichment picks up the card and the tagging populate maps (not blanks) the new spec — the two things that would break additive deploy silently.

**Files:** none (verification only).

**Interfaces:**
- Consumes: everything from Tasks 2–4.
- Produces: confidence that a redeploy adds exactly one card / one deployable space. Terminal task.

- [ ] **Step 1: Verify the app-layer enrichment surfaces the new card**

Run (from repo root; the root `presets.py` imports the library and loads specs at import):
```bash
PYTHONPATH=. python3 -c "
import presets
eu = presets.SUBINDUSTRY_USE_CASES['Electric Utility']
match = [x for x in eu if x['label'] == 'Software Delivery Project Management']
assert match, [x['label'] for x in eu]
card = match[0]
assert card['has_preset_spec'] is True, card
assert card['company_name'] == 'Meridian Grid', card
print('app card present:', card['label'], '| company:', card['company_name'])
"
```
Expected: prints the card with company `Meridian Grid` and `has_preset_spec=True`.

- [ ] **Step 2: Verify tagging populate maps the new spec (dry-run, no writes)**

Run:
```bash
PYTHONPATH=. python3 -c "
from genie_factory.tagging import populate_specs
s = populate_specs(dry_run=True)
assert not s['errors'], s['errors']
assert 'electric_utility/software_delivery_project_management' not in s['unmapped'], s['unmapped']
print('populate dry-run: no errors, spec mapped')
"
```
Expected: `populate dry-run: no errors, spec mapped`. (If `populate_specs` isn't the exact public name, run `python -m genie_factory.tagging --populate-specs --dry-run` instead and confirm the new spec is not listed as unmapped and there are no errors.)

- [ ] **Step 3: Verify remediation invariants pass on the new spec (dry-run)**

Run:
```bash
PYTHONPATH=. python -m genie_factory.remediation --fix-seed-modulo --fix-flat-trend --subindustry electric_utility --use-case software_delivery_project_management --dry-run --diff
```
Expected: no changes proposed for the new spec (it already conforms — no `{seed}%N`, KPI trend columns already carry `seasonal_amplitude`). If a fix is proposed, apply it (drop `--dry-run`) and re-commit the spec.

- [ ] **Step 4: Confirm working tree is clean and summarize commits**

Run:
```bash
git status --short
git log --oneline -6
```
Expected: clean tree; commits for the design doc, cleanup, tagging, spec, and preset are present.

---

## Self-Review

**Spec coverage:**
- Cleanup (delete + gitignore) → Task 1. ✓
- New use case placement/framing → Tasks 3 (spec) + 4 (preset). ✓
- Taxonomy allowlist dependency → Task 2. ✓ (found during research; would silently blank the tag otherwise)
- All six demo questions → Task 3 benchmarks 2–6 + worklog #6; opener + question arc in `space_description`. ✓
- Full-name assignees + "Bob" mapping → Task 3 genie_instructions bullet + dimension_values include "Bob Chen". ✓
- Additive deploy → Task 5 verifies app card + populate mapping; deploy paths documented in design. ✓

**Placeholder scan:** All generation_expr, measures, dimensions, question texts, and verification commands are concrete. The only intentionally author-discretion items are the 20 `dimension_values` rows and exact benchmark SQL bodies — bounded by the explicit column/measure names and conventions given, and each is gated by a runnable verification step (round-trip, SQL build, shape check) that fails loudly on a mistake.

**Type/name consistency:** Table names (`jira_worklogs`, `jira_issue_snapshots`, `sprint_velocity_monthly`), metric-view names (`jira_worklogs_metrics`, `jira_issue_snapshots_metrics`), measure names, and the slug `software_delivery_project_management` / label `Software Delivery Project Management` are used identically across Tasks 2–5. The outcome string `"Software Delivery & Project Management"` matches between Task 2 (allowlist + map) and Task 3 (inline `mfg_outcome_usecase`).
