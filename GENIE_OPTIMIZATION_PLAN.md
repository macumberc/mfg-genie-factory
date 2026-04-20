# Genie Space Optimization Plan — All 88 Specs

## Goal

Drive all 88 deployed Genie Spaces in `mfg-genie-factory` to **≥80% benchmark pass rate** (Databricks internal target) using an eval-driven iteration loop. Implementation on branch `genie-optimization-v2`.

## What we know now

- **Coverage gap:** Of 88 deployed spaces, only 1 has been benchmarked (FreightSight: 58%, 5 fails). We're flying blind on the other 87.
- **Documented priority order (official AWS docs + internal Genie team)**: Data Modeling → Descriptions → Synonyms → Hide Columns → Joins → SQL Expressions → Entity Matching → Instructions (LAST resort).
- **Caps that constrain the plan:** 500 benchmarks/space, 200 snippets/space, 100 instructions, 30 tables, 120 entity-matched columns × 1024 values × 127 chars, **5 qpm/workspace** for the Conversation API (the eval engine — this is the throughput bottleneck).
- **Real failure patterns observed (FreightSight):** 3/5 fails were "missing context column" (gold SQL had more columns than Genie returned), 1/5 base-table vs metric-view ambiguity, 1/5 over-interpretation of "currently"/"top".
- **Assessment reason codes** map to specific remediations (table below).
- **Scoring was tightened in 2025** — extra rows / missing columns are now BAD (were NEEDS REVIEW). Old benchmarks judged today are stricter.

## Reason-code → fix matrix (the operational core)

| Code | Meaning | Highest-leverage remediation |
|---|---|---|
| `RESULT_MISSING_COLUMNS` | Genie returned fewer columns than gold | (a) Tighten gold SQL to minimal contract, OR (b) add **column synonym** + **measure snippet** for the missing column, OR (c) add an `example_question_sqls` entry whose title matches the user phrasing and whose SELECT lists the full column set |
| `RESULT_MISSING_ROWS` | Over-filtering | Enable **entity matching / value dictionaries** on the filter column; add `ILIKE` rule to instructions; convert recurring date predicates to **filter snippets** |
| `EMPTY_RESULT` | All rows filtered out | Same as MISSING_ROWS, plus loosen any over-broad default filter in `genie_instructions` |
| `LLM_JUDGE_INCORRECT_TABLE_OR_FIELD_USAGE` | Wrong source picked | Tighten table/column **descriptions**, **hide overlapping** columns, promote the right field to a **measure / dimension snippet**, add an **example SQL** demonstrating the correct table |
| `LLM_JUDGE_INCOMPLETE_OR_PARTIAL_OUTPUT` | Right shape, partial answer (e.g. compound question) | Add `example_question_sqls` with `usage_guidance` covering the compound pattern; for top-k-by-slice patterns consider a parameterized query + UC function (gets the **Trusted** badge) |

This matrix drives Phase 3 — every fix maps to one of these levers, in priority order.

## Plan

### Phase 0 — Data-model + payload fixes (single commit)

Pre-requisites for Phase 2 levers to work.

**`genie_factory/generator.py`** — extend dataclasses (all default-empty for backwards compat):
- `ColumnSpec.synonyms: list[str]` (re-add the field we lost on branch delete)
- `ColumnSpec.entity_values: list[str]` — categorical values for value-dictionary / entity matching (≤1024 per col, ≤127 chars each)
- `ExampleSQL.usage_guidance: str` — per-example-SQL hint that tells Genie WHEN to apply this template
- `SQLSnippets.filters[*]`/`.expressions[*]`/`.measures[*]` already accept dict-shape; ensure `instruction` and `synonyms` are persisted

**`genie_factory/genie.py::build_genie_payload`** — payload changes:
- Re-add `column_configs[].synonyms` when populated
- Add `column_configs[].sample_values` populated from `ColumnSpec.entity_values` (capped at 1024) — the documented entity-matching mechanism
- Set `column_configs[].enable_entity_matching: True` only when `entity_values` is non-empty (avoid empty-entity failures)
- Re-add `instructions.example_question_sqls[*].usage_guidance` from `ExampleSPC.usage_guidance`
- **Fix the join_specs schema (was the 400 error):** use the documented field names — `left_table`, `right_table`, **`condition`** (string SQL like `"a.id = b.a_id"`, not `predicate`), **`relationship_type`** (one of `One-to-One` / `One-to-Many` / `Many-to-One` / `Many-to-Many`, not `join_type`). Default to `Many-to-One` for FK joins inferred by `_derive_join_specs`.
- Add HTTP **429 retry with exponential backoff** (the version we had: 10 attempts, max 120s sleep, jitter)

**Validation gate (in `scripts/improve_specs.py::validate_spec`):**
- Round-trip `DomainSpec.from_dict` → `build_genie_payload` → JSON-decode `serialized_space`
- Confirm `join_specs[*]` has `condition` not `predicate`
- Confirm column synonyms/entity_values shape

Commit, then verify all 88 existing JSON specs still load + build payloads cleanly.

### Phase 1 — Baseline benchmark eval across all 88 spaces

Build the data foundation. Throws away no work — we use the existing 88 deployed spaces (currently sitting in the workspace from the persist-deploy run).

**New script `scripts/run_all_benchmarks.py`:**
- For each of the 88 deployed Genie spaces, POST `/api/2.0/genie/spaces/{space_id}/eval-runs` to kick off a benchmark eval (using all 12 benchmarks already loaded into the space)
- Throughput: **5 qpm/workspace** is the documented cap. With 88 × 12 = 1,056 questions, minimum wall time is ~3.5 hours sequential. Run with `max_workers=2-3` to stay under the cap.
- Poll each `eval_run_id` until `eval_run_status == "DONE"`
- For each result, fetch `/eval-runs/{id}/results/{result_id}` and persist:
  - `space_title`, `subindustry`, `use_case_slug`
  - `assessment` (GOOD/BAD/UGLY/NEEDS_REVIEW), `assessment_reasons` (list of codes)
  - `question`, `benchmark_answer` (gold SQL), `actual_response[0].response` (Genie SQL)
- Output: a single `benchmark_baseline_<timestamp>.jsonl` at the repo root

**Aggregator output (markdown report):**
- Pass rate per spec, sorted ascending (worst first)
- Failure reasons rolled up across all 88 — what's the most common reason? where are the structural pain points?
- Spec-level fingerprint: which specs share failure modes (suggests a global fix vs per-spec)

**Output artifact:** `benchmark_baseline.md` — single source of truth for what to fix.

### Phase 2 — Global structural improvements (one commit per lever)

These apply to all 88 specs uniformly. Order chosen so each commit is independently reviewable + verifiable via Phase-1 baseline.

**2a. Re-enable derived `join_specs` (with the documented schema)**
- `_derive_join_specs` in `genie.py` now emits `condition` and `relationship_type=Many-to-One` (cardinality assumption appropriate for FK joins between transaction/snapshot/forecast tables)
- No spec-JSON edit; payload-only change

**2b. Populate `entity_values` on every dimension column (88 × ~6 cols ≈ 500 columns)**
- Source: spec JSON already contains `tables[*].dimension_values` (the explicit list of company/category/region/etc. that drives synthetic data generation) — extract distinct values per column and persist to `ColumnSpec.entity_values`
- Cap at 1024 / column; truncate longest values to 127 chars
- Mechanical script pass over all 88 JSONs — no LLM needed

**2c. Re-add column synonyms (88 × ~6 cols ≈ 500 cols, lost on branch delete)**
- LLM pass via `databricks-claude-sonnet-4-6` — same prompt structure as before, ≤3 synonyms per column, must not be substring of column name
- Per-spec, validated by column-reference lint

**2d. Tighten existing `sql_snippets[*].instruction` strings**
- Current: generic `"Use when the user asks about <display_name>."`
- Replace with LLM-generated WHEN-to-use guidance derived from the snippet SQL + business context (e.g., for `WHERE severity_level = 'Critical'`: *"Use when the user asks about critical or safety-critical recalls only — this is stricter than 'high severity'"*)
- Also confirm every snippet has populated `synonyms` (re-add lost from branch delete)

**2e. Add `usage_guidance` to every `example_question_sqls` entry**
- LLM-generates a 1-line hint per example: WHEN to use this template, what columns it returns
- This is the per-question routing mechanism — Genie matches user phrasing → example title → applies the full SELECT pattern

**2f. Tighten benchmark gold SQL — the "missing context column" fix**
- For each benchmark currently triggering `RESULT_MISSING_COLUMNS`, two options chosen per case:
  - (i) Drop the secondary measure from gold SQL if it's truly optional (Genie's 2-column answer should pass)
  - (ii) Add a `genie_instructions` bullet: *"When asked about a primary measure, also include the related count/volume measure as context if available in the same metric view."*
- Decide based on Phase-1 baseline data — if the same pattern shows up in many specs, the global instruction wins; if isolated, tighten the gold SQL.

**2g. Disambiguate overlapping base-table vs metric-view columns**
- For specs where both surfaces expose similar columns (e.g. `forecast_count` exists on both `demand_forecasts` and `forecast_kpi_monthly`), update column `description` to specify when each is canonical
- New `genie_instructions` bullet: *"When the question is about totals/averages, prefer the metric view; only query the base table when the question requires a column not available as a metric-view dimension."*

**2h. Restore the prior text-instruction template (lost on branch delete)**
- Same 5-bullet format we had: industry/company opener + 4 directive bullets + status-field rule
- Mechanical regeneration from spec metadata
- Length ≤1000 chars, ≥3 `- When` bullets

### Phase 3 — Targeted per-spec tuning

Driven entirely by Phase-1 baseline + Phase-2-rerun results.

**Workflow per failing spec:**
1. Read its current pass rate + per-question failure reasons from the latest baseline
2. For each failure, apply the highest-leverage fix from the reason-code matrix
3. Re-run only that spec's benchmark via `eval-runs` POST
4. Confirm the fix moved the needle (or revert)

**Stop conditions:**
- Spec hits ≥80% — done
- Spec sits at <80% after 2 iterations — flag as structural; doc the reason; move on (avoid spending unbounded time on edge cases)

**Tooling:** small CLI `scripts/tune_spec.py` that:
- Takes spec slug + a single `result_id` to focus on
- Pulls the eval result, applies a chosen lever (snippet, synonym, example SQL, etc.) interactively or auto-applied
- Re-runs benchmark, prints before/after pass rate

### Phase 4 — Validation + sign-off

- Final benchmark eval across all 88
- `benchmark_final.md` with before/after pass rates, distribution of reason codes, list of specs still <80% (with documented why)
- Update `GENIE_SPEC_UPGRADE.md` with the optimization-pass diff (or write a new `GENIE_OPTIMIZATION_RESULTS.md`)
- Spot-check 2-3 specs by hand in the workspace

## Tooling map

| File | Role | Status |
|---|---|---|
| `genie_factory/generator.py` | Add `synonyms`, `entity_values` to `ColumnSpec`; `usage_guidance` to `ExampleSQL` | EDIT |
| `genie_factory/genie.py` | Payload: column synonyms/sample_values, `usage_guidance`, fixed `join_specs` schema, 429 retry | EDIT |
| `scripts/improve_specs.py` | Mechanical pass + validator (re-create from prior session, gitignored) | NEW |
| `scripts/improve_specs_llm.py` | Per-field LLM passes (synonyms, snippet instructions, usage_guidance) | NEW |
| `scripts/run_all_benchmarks.py` | Phase-1 + Phase-3 benchmark orchestrator (rate-limited, persists JSONL) | NEW |
| `scripts/aggregate_benchmarks.py` | JSONL → markdown rollup | NEW |
| `scripts/tune_spec.py` | Per-spec interactive tuner | NEW |
| `genie_factory/specs/*/*.json` | All 88 spec JSONs touched by Phase 2 mechanical + LLM passes | EDIT (88) |

`scripts/` directory is `.gitignore`d by repo convention — keep tools local-only.

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Conversation API rate cap (5 qpm) means 3+ hours wall time per full eval pass | Run baseline + final overnight; per-spec re-runs (Phase 3) hit only 12 questions each, fast |
| LLM hallucinated column references in synonyms/usage_guidance | Column-reference lint (already built last session) catches these pre-writeback; up to 2 retries with error echoed back |
| `entity_values` for high-cardinality dimensions could exceed 1024 cap | Truncate + log; for true high-cardinality cols (model IDs, SKUs) skip entity matching entirely (not the failure mode they help with) |
| `join_specs` schema still wrong after this fix | Validation: deploy 1 canary spec, inspect via `GET /api/2.0/genie/spaces/{id}` and confirm `join_specs` round-trips. If still rejected, fall back to `[]` and demote to text |
| Genie eval is non-deterministic — same spec might pass once and fail next run | Run baseline 2× and aggregate; flag specs with high run-to-run variance separately |
| 88 spaces currently deployed are from the prior wheel; need rebuild + redeploy after Phase 0 | Wheel rebuild + workspace upload step is in the existing tooling; redeploy runs concurrently with Phase 1 baseline (different specs vs different spaces — they don't conflict) |
| Spec changes drift away from data-generation correctness | `data.py` only reads `tables[*].columns[*].name/sql_type/generation_expr`; new fields (`synonyms`, `entity_values`) are payload-only and don't touch data gen. Verified by all-88 wheel-build + smoke deploy after each commit |

## Verification

End-to-end check that this plan worked:

1. Phase 0: `python3 -c "from genie_factory.generator import DomainSpec; ..."` round-trip on all 88 specs passes; `build_genie_payload` round-trip JSON-decodes
2. Phase 1: `benchmark_baseline.md` exists, has per-spec pass rate for all 88, reason-code rollup
3. Phase 2: rerun benchmark on 5 canary specs (different subindustries) — pass rate moves up vs baseline
4. Phase 3: every spec at ≥80% OR documented as a structural exception
5. Phase 4: a clean side-by-side baseline-vs-final comparison

## Acceptance criteria

- All 88 specs deploy cleanly via `scripts/test_all_use_cases.py`
- All 88 specs at **≥80% benchmark pass rate**, OR explicitly documented exceptions in `GENIE_OPTIMIZATION_RESULTS.md`
- All commits on branch `genie-optimization-v2`, atomic per Phase, each green via `--validate`
- The pre-existing `electric_utility/demand_forecasting` metric-view failure is unrelated to this plan and stays as-is

## Sources cited

- [Curate an effective Genie space](https://docs.databricks.com/aws/en/genie/best-practices)
- [Use benchmarks in a Genie space](https://docs.databricks.com/aws/en/genie/benchmarks)
- [Set up and manage a Genie space](https://docs.databricks.com/aws/en/genie/set-up)
- [Build a knowledge store](https://docs.databricks.com/aws/en/genie/knowledge-store)
- [Troubleshoot Genie spaces](https://docs.databricks.com/aws/en/genie/troubleshooting)
- [Building confidence in your Genie space: Benchmarks and Ask Review (blog)](https://www.databricks.com/blog/building-confidence-your-genie-space-benchmarks-and-ask-review)
- [From Data to Dialogue: Best Practices Guide (blog)](https://www.databricks.com/blog/data-dialogue-best-practices-guide-building-high-performing-genie-spaces)
- Internal: Genie Spaces Best Practices doc (Cai/Sun/Guo); Benchmarks v2 PRD (Sun/Guo, Aug 2025); Field Engineering Genie Playbook (Moser); Genie Space Field Engineering Guide (Jaeck, Mar 2026)
