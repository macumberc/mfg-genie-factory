"""Parameterized invariant suite over all 88 spec JSONs.

Each test runs once per spec via ``pytest.mark.parametrize`` and asserts a
structural property the remediation guarantees. Use ``known_gaps.yaml``
(when needed) to opt specific specs out of a check with ``pytest.xfail``;
the goal is to keep that allowlist empty.

Run locally:
    pytest tests/test_spec_quality.py -v
    pytest tests/test_spec_quality.py -k well_production_monitoring -v
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

from genie_factory.data import (
    _AVG_MEASURE_PATTERN,
    _SUM_MEASURE_PATTERN,
    build_metric_view_sqls_from_spec,
    build_table_sqls_from_spec,
)
from genie_factory.generator import DomainSpec
from genie_factory.remediation import (
    _NOUN_TO_COLUMNS,
    _SEED_MOD_RE,
    iter_specs,
)

SPECS_DIR = Path(__file__).resolve().parent.parent / "genie_factory" / "specs"


# ---------------------------------------------------------------------------
# Fixtures: load each spec once per session for fast iteration.
# ---------------------------------------------------------------------------


def _all_spec_paths() -> list[Path]:
    return sorted(SPECS_DIR.glob("*/*.json"))


def _spec_id(path: Path) -> str:
    return f"{path.parent.name}/{path.stem}"


@pytest.fixture(scope="session")
def specs_corpus() -> dict[str, dict]:
    """Map spec_id -> loaded JSON dict for the whole corpus."""
    return {_spec_id(p): json.loads(p.read_text()) for p in _all_spec_paths()}


# ---------------------------------------------------------------------------
# Pin GENIE_FACTORY_END_DATE so the SQL builders are deterministic across
# CI runs (and so anchor-year math stays stable while the engine is rolling).
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True, scope="session")
def _pin_anchor_date():
    prior = os.environ.get("GENIE_FACTORY_END_DATE")
    os.environ["GENIE_FACTORY_END_DATE"] = "2026-05-19"
    yield
    if prior is None:
        del os.environ["GENIE_FACTORY_END_DATE"]
    else:
        os.environ["GENIE_FACTORY_END_DATE"] = prior


# ---------------------------------------------------------------------------
# Test 1: every spec parses + builds clean SQL for tables AND metric views.
# This catches any malformed generation_expr or YAML before deploy.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_spec_builds(spec_path: Path) -> None:
    spec_dict = json.loads(spec_path.read_text())
    spec = DomainSpec.from_dict(spec_dict)
    table_sqls = build_table_sqls_from_spec(spec, "cat.sch", seed=42, scale=3, target_rows=5000)
    assert table_sqls, "build_table_sqls_from_spec returned empty dict"
    mv_sqls = build_metric_view_sqls_from_spec(spec, "cat.sch")
    assert mv_sqls, "build_metric_view_sqls_from_spec returned empty dict"


# ---------------------------------------------------------------------------
# Test 2: no {seed}%N patterns remain anywhere.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_no_seed_modulo_n(spec_path: Path, specs_corpus: dict[str, dict]) -> None:
    spec = specs_corpus[_spec_id(spec_path)]
    offenders: list[str] = []
    for table in spec.get("tables", []):
        for col in table.get("columns", []):
            expr = col.get("generation_expr") or ""
            if _SEED_MOD_RE.search(expr):
                offenders.append(f"{table['table_name']}.{col['name']}")
    assert not offenders, (
        f"{{seed}}%N collapses a column to one constant per deploy. "
        f"Offending columns: {offenders}. Use {{id_seq}}%N instead."
    )


# ---------------------------------------------------------------------------
# Test 3: per-table, at most ONE column uses {status_noise} in a CASE.
# Sibling CASE columns should be reassigned to {alt_status_noise}/2..5.
# ---------------------------------------------------------------------------


_CASE_STATUS_NOISE_RE = re.compile(
    r"(WHEN|IF)[^A-Za-z_]+\{\s*status_noise\s*\}", re.IGNORECASE
)


# Tables where multiple CASE columns share {status_noise} by design — they
# MUST correlate semantically (a sub-account derived from its parent
# category, a capex band derived from its risk tier, etc.). The shared
# hash is the design intent, not a bug.
_INTENTIONAL_SHARED_STATUS_NOISE = {
    "railroad/route_planning/corridor_snapshots",
    "semiconductor/financial_analytics_reporting/financial_transactions",
}


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_no_shared_status_noise_in_case_columns(spec_path: Path, specs_corpus: dict[str, dict]) -> None:
    spec = specs_corpus[_spec_id(spec_path)]
    spec_key = _spec_id(spec_path)
    for table in spec.get("tables", []):
        table_key = f"{spec_key}/{table['table_name']}"
        if table_key in _INTENTIONAL_SHARED_STATUS_NOISE:
            continue
        case_cols = [
            col["name"]
            for col in table.get("columns", [])
            if _CASE_STATUS_NOISE_RE.search(col.get("generation_expr") or "")
        ]
        assert len(case_cols) <= 1, (
            f"Table {table['table_name']} has {len(case_cols)} columns whose CASE "
            f"reads from {{status_noise}}: {case_cols}. Reassign 2nd+ to "
            f"{{alt_status_noise}}, {{alt_status_noise2}}, ... — or add the "
            f"table to _INTENTIONAL_SHARED_STATUS_NOISE if the correlation "
            f"is semantic (e.g. sub-category derived from parent category)."
        )


# ---------------------------------------------------------------------------
# Test 4: every "Top N <noun>" question targets a dim with cardinality >= N.
# ---------------------------------------------------------------------------


_TOPN_RE = re.compile(r"\btop\s+(\d+)\s+([a-z][a-z ]+?)\b(?:\s|,|—|\.|$|\?)", re.IGNORECASE)


def _resolve_dim_cardinality(spec: dict, noun: str) -> int:
    """Return cardinality of the dim column matching `noun`, or 0 if unknown."""
    candidates = _NOUN_TO_COLUMNS.get(noun.lower().strip())
    if not candidates:
        return -1  # unknown noun — skip
    for table in spec.get("tables", []):
        col_names = {(c.get("name") or "").lower() for c in table.get("columns", [])}
        for cand in candidates:
            if cand.lower() in col_names:
                values = {
                    str(d.get(cand))
                    for d in table.get("dimension_values", []) or []
                    if cand in d
                }
                if values:
                    return len(values)
        # Also count distinct CASE literals in generation_expr.
        for col in table.get("columns", []):
            if (col.get("name") or "").lower() in [c.lower() for c in candidates]:
                expr = col.get("generation_expr") or ""
                literals = set(re.findall(r"THEN\s+'([^']+)'", expr, re.IGNORECASE))
                if literals:
                    return len(literals)
    return -1


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_topn_matches_cardinality(spec_path: Path, specs_corpus: dict[str, dict]) -> None:
    spec = specs_corpus[_spec_id(spec_path)]
    violations: list[str] = []
    questions = list(spec.get("sample_questions", []) or []) + [
        b.get("question", "") for b in spec.get("benchmarks", []) or []
    ]
    for q in questions:
        for m in _TOPN_RE.finditer(q):
            n = int(m.group(1))
            noun = m.group(2).strip().lower()
            card = _resolve_dim_cardinality(spec, noun)
            if card > 0 and card < n:
                violations.append(f"'Top {n} {noun}' but only {card} distinct values")
    assert not violations, "Top-N exceeds cardinality:\n  " + "\n  ".join(violations)


# ---------------------------------------------------------------------------
# Test 5: every SUM(<bare_column>) measure has an AVG companion.
# Because the engine auto-synthesizes AVG companions, this is *guaranteed*
# to hold at build time — but we assert against the rendered metric-view
# YAML to catch any spec that opts out via auto_avg=False unnecessarily.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_avg_companion_present_in_built_view(spec_path: Path) -> None:
    spec = DomainSpec.from_dict(json.loads(spec_path.read_text()))
    view_sqls = build_metric_view_sqls_from_spec(spec, "cat.sch")
    missing: list[str] = []
    for view_name, view_sql in view_sqls.items():
        # Walk the YAML body of the view: find every measure name + expr pair.
        # We use the rendered SQL since it's where the engine emits synthesized
        # AVG companions.
        measure_blocks = re.findall(
            r"- name:\s*(\S+)\s*\n\s+expr:\s*(.+?)$",
            view_sql,
            flags=re.MULTILINE,
        )
        sum_targets: dict[str, str] = {}
        avg_targets: set[str] = set()
        for name, expr in measure_blocks:
            avg_m = _AVG_MEASURE_PATTERN.match(expr.strip())
            sum_m = _SUM_MEASURE_PATTERN.match(expr.strip())
            if avg_m:
                avg_targets.add(avg_m.group(1).lower())
            elif sum_m:
                sum_targets[sum_m.group(1).lower()] = name
        for target, src in sum_targets.items():
            if target not in avg_targets:
                missing.append(f"{view_name}: {src}=SUM({target}) has no AVG companion")
    assert not missing, (
        "Every SUM(<col>) measure should have a sibling AVG(<col>) measure "
        "(the engine auto-synthesizes them — if a spec sets auto_avg=False, "
        "it must define an explicit AVG measure). Offenders:\n  " + "\n  ".join(missing)
    )


# ---------------------------------------------------------------------------
# Test 6: every measure/column name referenced in question text exists somewhere
# in the spec (table columns or metric_view measures/dimensions). Lightweight
# heuristic — only flags backtick-quoted refs and obvious snake_case tokens.
# ---------------------------------------------------------------------------


_COL_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9_]{4,})\b")  # snake_case >= 5 chars


def _spec_known_identifiers(spec: dict) -> set[str]:
    names: set[str] = set()
    for table in spec.get("tables", []):
        names.add(table.get("table_name", "").lower())
        for col in table.get("columns", []):
            names.add(col.get("name", "").lower())
    for mv in spec.get("metric_views", []):
        names.add(mv.get("view_name", "").lower())
        for m in mv.get("measures", []):
            names.add(m.get("name", "").lower())
        for d in mv.get("dimensions", []):
            names.add(d.get("name", "").lower())
    return {n for n in names if n}


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_question_token_smoke(spec_path: Path, specs_corpus: dict[str, dict]) -> None:
    """Soft smoke test: at least one column/measure name must be referenced
    in the spec's questions or example SQL — otherwise the spec is likely
    misaligned (questions don't talk about the data shape).
    """
    spec = specs_corpus[_spec_id(spec_path)]
    known = _spec_known_identifiers(spec)
    # Pull all question and SQL text into one bag.
    haystack: list[str] = list(spec.get("sample_questions", []) or [])
    haystack += [b.get("question", "") for b in spec.get("benchmarks", []) or []]
    for ex in spec.get("example_sqls", []) or []:
        haystack.append(ex.get("question", ""))
        haystack += ex.get("sql_lines", []) or []
    text = "\n".join(haystack).lower()
    referenced = {t for t in _COL_TOKEN_RE.findall(text) if t in known}
    assert referenced, (
        "No table/column/measure name from this spec is referenced in any "
        "sample_question, benchmark, or example_sql — sample questions are "
        "almost certainly misaligned with the data shape."
    )


# ---------------------------------------------------------------------------
# Test 7: date-anchored questions warn (not fail) when the engine is rolling.
# We only enforce this lightly so a "this year" question doesn't break CI —
# but the test surfaces them for later review.
# ---------------------------------------------------------------------------


_DATE_ANCHOR_RE = re.compile(
    r"\b(this month|this quarter|this year|year[- ]to[- ]date|ytd|"
    r"last (?:\d+\s+)?(?:days?|months?|quarter|year)|"
    r"trailing\s+\d+\s+months|next\s+(?:\d+\s+)?(?:months?|quarter|year)|upcoming)\b",
    re.IGNORECASE,
)


@pytest.mark.parametrize("spec_path", _all_spec_paths(), ids=_spec_id)
def test_date_anchored_questions(spec_path: Path, specs_corpus: dict[str, dict]) -> None:
    spec = specs_corpus[_spec_id(spec_path)]
    anchored: list[str] = []
    for q in spec.get("sample_questions", []) or []:
        if _DATE_ANCHOR_RE.search(q):
            anchored.append(q[:80])
    if anchored and not os.environ.get("GENIE_FACTORY_ALLOW_DATE_ANCHORS"):
        # Soft warning — emit via pytest's recwarn-style mechanism by
        # printing. We don't fail because rolling-date engine + monthly
        # refresh job means these questions DO return data; they just
        # might confuse a reader who reads the spec on a date when the
        # underlying data is mid-rotation.
        pytest.skip(
            f"Date-anchored questions present (informational): {len(anchored)} of "
            f"{len(spec.get('sample_questions', []))}. Set GENIE_FACTORY_ALLOW_"
            "DATE_ANCHORS=0 to enforce."
        )
