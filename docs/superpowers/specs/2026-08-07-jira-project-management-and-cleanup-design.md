# Design: Repo Cleanup + JIRA Project-Management Use Case

**Date:** 2026-08-07
**Author:** Chad Macumber (with Isaac)
**Status:** Approved design — pending implementation plan

---

## Overview

Two independent workstreams in one pass:

1. **Repo cleanup.** Remove the ~2.6 MB of loose benchmark run-output files that
   accumulated at the repo root, and harden `.gitignore` so future runs never get
   committed loosely again. The benchmark *engine* modules stay.
2. **New use case: JIRA-style software-delivery project management.** Add one new
   preset Genie space under the existing **Electric Utility** subindustry, framed as a
   utility's internal digital-delivery PMO running on JIRA, with energy/grid-relevant
   projects. It must be deployable **additively** to the already-deployed
   `mfg-genie-factory` app — a single new schema + Genie space, with zero disruption to
   the existing 88 spaces.

---

## Part 1 — Repo Cleanup

### Delete

All 28 tracked run-output files at the repo root matching `benchmark_20260526_*`:

- `*.jsonl` (raw eval results) and `*_summary.jsonl`
- `*.md` (aggregate reports), `*_analysis*.md`, `*_pass3_recommendations.md`
- `*_actions*.json` (remediation action files)
- `*.log`

Rationale: these are regenerable via the runner, and the durable learnings are already
captured in `CLAUDE.md` ("Benchmark Optimization" / "Benchmark Eval Tooling" sections).
They remain recoverable from git history. The user explicitly chose delete over
relocating to a `benchmarks/` folder.

### Keep (engine, not outputs)

- `genie_factory/benchmark.py` — the eval-run runner/aggregator
- `genie_factory/remediation.py` — spec fixers + invariants
- `genie_factory/refresh.py` — the 88-spec parallel deploy used by the monthly job

### Harden `.gitignore`

The current file only ignores `benchmark_baseline_*.jsonl` / `_summary.json`. Add
patterns that cover the actual runner output naming so future runs stay untracked:

```
benchmark_*.jsonl
benchmark_*.md
benchmark_*.json
benchmark_*.log
```

(Placed under the existing "Test runs & benchmark outputs" section.)

### Untracked files — leave as-is

- `AGENTS.md` (root) — a byte-mirror of the gitignored `CLAUDE.md`; already untracked,
  keep it untracked. Not staged, not deleted.
- `.isaac/config.json` — Isaac Review local config; leave alone.

---

## Part 2 — JIRA Project-Management Use Case

### Placement & framing

| Field | Value |
|---|---|
| Subindustry (bucket) | **Electric Utility** (existing) |
| Use-case label | **Software Delivery Project Management** |
| Slug (file) | `software_delivery_project_management.json` |
| Company | **Meridian Grid** (fictional utility, digital-delivery org) |
| `schema_basename` | `utility_project_management` |
| `mfg_subindustry` | `Electric Utility` |
| `mfg_outcome_usecase` | `Software Delivery & Project Management` (NEW taxonomy value) |
| `importance` | 8 |

Framed as Meridian Grid's internal software/digital-delivery PMO tracking work in JIRA.
The JIRA projects are energy/utility-relevant so the space stays on-theme with the
factory while demoing pure PM questions:

- Grid Modernization (GRID)
- AMI / Smart-Meter Rollout (AMI)
- Outage Management System (OMS)
- DERMS / DER Integration (DERMS)
- Customer Self-Service Portal (PORTAL)
- SCADA / Control-System Upgrade (SCADA)
- EV Charging Network (EVSE)

### Demo questions this must answer

The Summit-demo PM questions, mapped to the data model:

| # | Question | Backing table + shape |
|---|---|---|
| 1 | (opener) Showcase visualization options | any / metric view |
| 2 | What are the blockers with risks we need to address today? | snapshot: `is_blocker = true AND risk_level = 'High'`, open status |
| 3 | Which tickets have been stuck extensively in a status? | snapshot: top `days_in_status` (LIMIT 10) |
| 4 | What is the status of the <X> effort? | snapshot filtered by project/epic |
| 5 | How many features have been deployed in the last quarter? | monthly KPI: `SUM(features_deployed)` last quarter |
| 6 | Can I see a visual of the progress of this sprint? | monthly KPI: committed vs completed points by sprint |
| 7 | How much time has Bob logged on stories in the last two weeks? | worklog: `SUM(hours_logged)` where assignee = 'Bob Chen', issue_type = 'Story', last 14 days |

Assignees use **full names** (Bob Chen, Priya Nair, Marcus Reed, Sofia Alvarez, …). To
keep question 7 working when a demoer types just "Bob", the `assignee` column carries a
synonym/entity hint and a `genie_instructions` bullet mapping first names to full names.

### Data model — 3 tables (standard archetypes)

**`jira_worklogs`** (transaction, ~5,000 rows) — one time-logging entry per row.

| Column | Type | Dim? | Notes |
|---|---|---|---|
| worklog_id | STRING | no | `WL-#######` |
| work_date | DATE | no | `d.dt` |
| issue_key | STRING | yes | e.g. `GRID-1423` |
| project | STRING | yes | Grid Modernization, AMI Rollout, … |
| epic | STRING | yes | epic name within project |
| issue_type | STRING | no | Story / Bug / Task / Feature / Epic / Sub-task |
| assignee | STRING | yes | full name (Bob Chen, …) |
| team | STRING | no | Platform / Data / Field Systems / Customer Apps / SRE |
| hours_logged | DOUBLE | no | 0.5–8.0 |
| status_at_log | STRING | no | status when work logged |
| is_resolved | INT | no | 1 if the underlying issue resolved that day |

**`jira_issue_snapshots`** (snapshot, ~1,500 rows) — daily state of each open issue.

| Column | Type | Dim? | Notes |
|---|---|---|---|
| snapshot_id | STRING | no | `IS-#######` |
| snapshot_date | DATE | no | `d.dt` |
| issue_key | STRING | yes | |
| project | STRING | yes | |
| epic | STRING | yes | |
| sprint | STRING | yes | e.g. `GRID Sprint 24` |
| assignee | STRING | yes | full name |
| status | STRING | no | Backlog / To Do / In Progress / In Review / Blocked / Done |
| priority | STRING | no | Highest / High / Medium / Low |
| risk_level | STRING | no | High / Medium / Low |
| is_blocker | INT | no | 1 if flagged as blocker |
| days_in_status | INT | no | days stuck in current status |
| story_points | INT | no | 1,2,3,5,8,13 |

**`sprint_velocity_monthly`** (monthly KPI, ~700 rows) — per-sprint/month rollup.

| Column | Type | Dim? | Notes |
|---|---|---|---|
| record_id | STRING | no | `SV-#######` |
| report_month | DATE | no | `DATE_TRUNC('month', d.dt)` |
| project | STRING | yes | |
| sprint | STRING | yes | |
| team | STRING | yes | |
| committed_points | INT | no | sprint commitment |
| completed_points | INT | no | delivered |
| velocity | DOUBLE | no | completed / committed *100 |
| features_deployed | INT | no | features shipped that period |
| bugs_closed | INT | no | |
| avg_cycle_time_days | DOUBLE | no | seasonal_amplitude for a real trend |
| blocker_count | INT | no | blockers active in period |

### Metric views — 2

- **`jira_worklogs_metrics`** on `jira_worklogs`: dims (work_date, project, epic,
  issue_type, assignee, team); measures total_hours_logged (SUM), avg_hours_per_entry
  (AVG), worklog_count, resolved_issue_count, story_hours (SUM CASE issue_type='Story'),
  distinct_issue_count. AVG companions auto-synthesized by the engine.
- **`jira_issue_snapshots_metrics`** on `jira_issue_snapshots`: dims (snapshot_date,
  project, epic, sprint, assignee, status, priority, risk_level); measures open_issue_count,
  blocker_count (COUNT CASE is_blocker=1), high_risk_blocker_count, avg_days_in_status,
  max_days_in_status, total_story_points, done_issue_count.

Sprint burndown/velocity questions (5, 6) read `sprint_velocity_monthly` as a plain
table (it is already a rollup); a metric view over it is optional and omitted to keep to
the 2-metric-view convention used across the corpus.

### Genie config

Following corpus conventions exactly:

- `space_description` in the standard `render_space_description(scenario, questions)`
  Scenario/Questions format (post-2026-06). Scenario is a 2–3 sentence second-person
  narrative ending in a provocative question; 3 demo questions annotated `(agent)`.
- `sample_questions`: the same 3 (opener → composition → payoff) without `(agent)`.
- `genie_instructions`: DOMAIN CONTEXT + METRIC DEFINITIONS + a bullet mapping common
  first names to full assignee names + the standard SQL-snippet-preference bullet.
- `example_sqls`: 7 items — 4 MEASURE-based over metric views + 3 plain-table (one per
  base table). `{fqn}` placeholder. Monthly-trend questions use `DATE_TRUNC('month', …)`.
- `benchmarks`: 7 items — 4 MEASURE + 3 plain-table. Top-N questions say "Top 10" and use
  `LIMIT 10`. Covers all six demo questions + opener.
- `sql_snippets`: 3 filters (high-risk blockers, stuck > N days, Story issues),
  3 expressions (report month, cycle-time bucket, sprint completion %),
  4 measures (total_hours_logged, high_risk_blocker_count, avg_days_in_status,
  features_deployed). Keys: `display_name`, `alias`, `sql`, `synonyms`, `instruction`.
- Column `synonyms` and `entity_values` on every dimension column.

### Taxonomy registration (REQUIRED — not optional)

`genie_factory/tagging.py` validates outcome tags against a fixed allowlist and
re-derives them on `--populate-specs`. Two edits are mandatory or the tag will be
rejected / blanked:

1. Add `"Software Delivery & Project Management"` to `ALLOWED_OUTCOMES`.
2. Add `"software_delivery_project_management": "Software Delivery & Project Management"`
   under `OUTCOME_USECASE_MAP["electric_utility"]`.

The spec JSON itself also carries `mfg_subindustry` / `mfg_outcome_usecase` inline so
`deploy()` tags correctly without a populate run.

### Presets wiring

Add to `genie_factory/presets.py` under `USE_CASES["Electric Utility"]`:

```python
{"label": "Software Delivery Project Management",
 "use_case": "Software delivery portfolio tracking, sprint execution, and blocker/risk management across utility technology programs",
 "importance": 8},
```

The root `presets.py` (app) enriches from the spec at import, so the new card appears in
the Electric Utility group automatically. No app-code change needed.

---

## Additive Deployment

The whole point: this drops in without disturbing the existing deployment.

- **App (Dash UI):** After the spec JSON + presets entry land on `@main` and the app is
  redeployed, `SUBINDUSTRY_USE_CASES` (built from specs at import) gains one card in the
  Electric Utility group. A user clicks that single card → Quick Deploy →
  `load_spec(...)` → `deploy(domain_spec=spec)` creates **one** new schema
  (`utility_project_management`) + **one** new Genie space. Nothing else is touched.
- **Notebook / CLI:** `deploy_use_case("Electric Utility", "Software Delivery Project
  Management")` deploys exactly this one space, no full refresh.
- **Monthly refresh:** `refresh_all` deploys all specs including this one; it is
  create-or-replace and idempotent, so the new spec simply joins the cycle. No conflict
  with, or replacement of, any existing space.

Existing 88 spaces are never re-created, re-tagged, or torn down by adding this use case.

---

## Validation

Before commit:

1. `DomainSpec.from_dict(json.load(...))` round-trips the new spec without error.
2. `python -m genie_factory.remediation` invariant checks pass (no `{seed}%N`, monthly-
   trend/top-limit conventions, snippet keys).
3. `from genie_factory.presets import USE_CASES; from genie_factory.specs import
   load_spec` → the new label resolves to a spec (slug match).
4. Root `presets.SUBINDUSTRY_USE_CASES["Electric Utility"]` contains the new enriched
   entry with `has_preset_spec=True`.
5. `tagging.populate_specs(dry_run=True)` reports the new spec mapped (not in `unmapped`,
   no `errors`).

A live deploy against the workspace is out of scope for this change-set (author will
deploy from the app / notebook after merge); the validation above confirms the spec is
structurally correct and wired.

---

## Out of Scope

- Real JIRA API ingestion (data is synthetic, engine-generated — consistent with the
  whole factory).
- Any change to the benchmark engine behavior.
- Renaming or re-tagging existing spaces.
- New subindustry creation (reusing Electric Utility per decision).
