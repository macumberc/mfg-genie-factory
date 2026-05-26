"""Mass-rewrite spec JSONs to fix systemic data-quality issues identified by
``SPEC_DATA_AUDIT.md``.

Each ``--fix-*`` mode is idempotent: rerunning on a fixed spec is a no-op.
All modes support ``--dry-run`` and ``--diff`` for safe inspection.

Modes (Phase 1 — mechanical):

  --fix-seed-modulo       Replace ``{seed} % N`` (constant per deploy) with
                          ``{id_seq} % N`` (varies per row). Fixes
                          automotive/vehicle_recall constant-supplier bug.
  --fix-correlated-hash   Decorrelate sibling CASE columns that share the
                          {status_noise} band by reassigning 2nd+ uses to
                          {alt_status_noise} / {alt_status_noise2}.
  --fix-wrong-range       Widen generation_expr clamps so question
                          thresholds fall inside the achievable range
                          (driven by the curated WRONG_RANGE_FIXES map).
  --fix-flat-trend        Mark KPI columns referenced in monthly-trend
                          questions with seasonal_amplitude > 0 and wrap
                          their {qty_noise} with the {seasonal_mult}
                          placeholder so trends show real curves.
  --fix-topn-cardinality  When a question says "Top N X" but X has <N
                          values, rewrite to "Rank X" so the answer is
                          not misleading.

  --all                   Run all 5 mechanical modes in the safe order
                          documented at the bottom of this file.

Modes (Phase 2 — semantic):

  --fix-semantic          Drive per-spec hand-curated edits from
                          ``genie_factory/semantic_fixes.yaml`` (built later).

Examples:

  python -m genie_factory.remediation --fix-seed-modulo --dry-run --diff
  python -m genie_factory.remediation --fix-correlated-hash --diff
  python -m genie_factory.remediation --all
"""

from __future__ import annotations

import argparse
import difflib
import json
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = REPO_ROOT / "genie_factory" / "specs"


def iter_specs(
    subindustry: Optional[str] = None,
    use_case: Optional[str] = None,
) -> list[Path]:
    """Return spec JSON paths, optionally filtered to a subindustry / use-case."""
    paths = sorted(SPECS_DIR.glob("*/*.json"))
    if subindustry:
        paths = [p for p in paths if p.parent.name == subindustry]
    if use_case:
        paths = [p for p in paths if p.stem == use_case]
    return paths


def load_spec(path: Path) -> dict:
    """Load a spec JSON from disk."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_spec(path: Path, spec: dict) -> None:
    """Write a spec JSON with the canonical formatting (indent=2, UTF-8 emoji)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")


_logger = logging.getLogger("genie_factory.remediation")


# ---------------------------------------------------------------------------
# Fix 1 — {seed} % N → {id_seq} % N
# ---------------------------------------------------------------------------


_SEED_MOD_RE = re.compile(r"\{\s*seed\s*\}\s*%\s*(\d+)", re.IGNORECASE)


def apply_fix_seed_modulo(spec: dict) -> int:
    """Rewrite ``{seed} % N`` → ``{id_seq} % N`` in every generation_expr.

    Returns the number of substitutions made.
    """
    changes = 0
    for table in spec.get("tables", []):
        for col in table.get("columns", []):
            expr = col.get("generation_expr") or ""
            if not expr:
                continue
            new_expr, n = _SEED_MOD_RE.subn(r"{id_seq} % \1", expr)
            if n:
                col["generation_expr"] = new_expr
                changes += n
    return changes


# ---------------------------------------------------------------------------
# Fix 2 — decorrelate shared {status_noise} CASE columns
# ---------------------------------------------------------------------------


# Patterns that signal a CASE-on-noise column (vs. a numeric measure that
# merely scales by qty_noise).
_CASE_STATUS_NOISE_RE = re.compile(
    r"(WHEN|IF)[^A-Za-z_]+\{\s*status_noise\s*\}", re.IGNORECASE
)
_REPLACEMENT_PLACEHOLDERS = [
    "{alt_status_noise}",
    "{alt_status_noise2}",
    "{alt_status_noise3}",
    "{alt_status_noise4}",
    "{alt_status_noise5}",
]


def _uses_status_noise_in_case(expr: str) -> bool:
    return bool(_CASE_STATUS_NOISE_RE.search(expr or ""))


def apply_fix_correlated_hash(spec: dict) -> int:
    """For each table, if 2+ columns CASE on {status_noise}, reassign the
    2nd+ to {alt_status_noise}/{alt_status_noise2}. Returns total
    reassignments performed (across all tables in the spec).
    """
    changes = 0
    for table in spec.get("tables", []):
        case_cols = [
            col for col in table.get("columns", [])
            if _uses_status_noise_in_case(col.get("generation_expr") or "")
        ]
        if len(case_cols) < 2:
            continue
        # First column keeps {status_noise}; reassign 2nd, 3rd...
        for col, replacement in zip(case_cols[1:], _REPLACEMENT_PLACEHOLDERS):
            expr = col["generation_expr"]
            new_expr = re.sub(
                r"\{\s*status_noise\s*\}", replacement, expr, flags=re.IGNORECASE
            )
            if new_expr != expr:
                col["generation_expr"] = new_expr
                changes += 1
        # If more than 3 CASE columns, leave the rest on status_noise but log;
        # the human reviewer can decide whether they intentionally correlate.
        if len(case_cols) > 1 + len(_REPLACEMENT_PLACEHOLDERS):
            _logger.warning(
                "    %s has %d CASE-on-status_noise columns; only the first %d reassigned",
                table.get("table_name", "<unknown>"),
                len(case_cols),
                1 + len(_REPLACEMENT_PLACEHOLDERS),
            )
    return changes


# ---------------------------------------------------------------------------
# Fix 3 — widen generation_expr clamps to span question thresholds
# ---------------------------------------------------------------------------


# Each entry maps "<subindustry>/<use_case>" -> { column_name: (new_base, new_range) }
# where the new generation_expr becomes:
#   ROUND(GREATEST(<min>, <new_base> + qty_noise * <new_range>), <decimals>)
# (decimals + LEAST/clamp shape are preserved from the original expression.)
WRONG_RANGE_FIXES: dict[str, dict[str, tuple[float, float]]] = {
    "electric_utility/transformer_asset_health": {
        # Q: "above 1000 ppm Warning threshold" — original max=500.
        "dissolved_gas_ppm": (10.0, 2990.0),
    },
    "power_generation/solar_optimization_behind_the_meter": {
        # Q: "battery health < 80%" — original floor=80.
        "health_pct": (60.0, 40.0),
    },
    "power_generation/nuclear_safety": {
        # Q: "past 90-day surveillance window" — original ceiling=90.
        "days_since_last_inspection": (7.0, 200.0),
    },
    "industrial_distribution/inventory_optimization": {
        # Q: "days_of_supply > 120" — original ceiling=90.
        "days_of_supply": (5.0, 200.0),
    },
    "industrial_distribution/working_capital_cash_flow_optimization": {
        # Q: "CCC > 75 days" — original avg=60, max=90.
        "cash_conversion_cycle_days": (15.0, 120.0),
    },
    "semiconductor/salable_inventory_optimization": {
        # Q: ">180 days of supply" — original ceiling=150.
        "days_of_supply": (5.0, 250.0),
    },
    "oil_gas_refining/financial_analytics_reporting": {
        # Q: "operating_margin < 35%" — original ceiling=35.
        "operating_margin_pct": (-10.0, 55.0),
    },
    "oil_gas_refining/working_capital_cash_flow_optimization": {
        # Q: "current ratio < 1.0" — original floor=0.8.
        "current_ratio": (0.5, 2.5),
    },
    "mining/haul_vehicle_asset_health": {
        # Q: "vs ~240t nameplate" — original gen produced 500-5000.
        "payload_tons": (100.0, 300.0),
    },
    "machinery/financial_analytics_reporting": {
        # Q references posting_status='Open' which the CASE never emits.
        # Categorical fix — left for --fix-semantic stage. (No range entry.)
    },
}


# Match the three shapes that appear in real specs (alternatives, ordered
# from most-specific to least-specific so we don't accidentally consume an
# outer clamp's closing paren):
#   FLOOR  : `<base> + FLOOR({qty_noise} * <range>)`
#   PAREN  : `<base> + ({qty_noise} * <range>)`
#   BARE   : `<base> + {qty_noise} * <range>`
# Each alternative balances its own parens internally.
_BASE_RANGE_RE = re.compile(
    r"""(?P<base>-?\d+(?:\.\d+)?)\s*\+\s*
        (?:
            FLOOR\(\s*\{\s*qty_noise\s*\}\s*\*\s*(?P<range_floor>-?\d+(?:\.\d+)?)\s*\)
            |
            \(\s*\{\s*qty_noise\s*\}\s*\*\s*(?P<range_paren>-?\d+(?:\.\d+)?)\s*\)
            |
            \{\s*qty_noise\s*\}\s*\*\s*(?P<range_bare>-?\d+(?:\.\d+)?)
        )""",
    re.IGNORECASE | re.VERBOSE,
)


def apply_fix_wrong_range(spec: dict, spec_key: str) -> int:
    """Apply curated clamp widenings for ``spec_key`` (subindustry/use_case)."""
    overrides = WRONG_RANGE_FIXES.get(spec_key)
    if not overrides:
        return 0
    changes = 0
    for table in spec.get("tables", []):
        for col in table.get("columns", []):
            name = col.get("name")
            if name not in overrides:
                continue
            new_base, new_range = overrides[name]
            expr = col.get("generation_expr") or ""

            def _sub(match: re.Match[str]) -> str:
                if match.group("range_floor") is not None:
                    # Keep FLOOR(...) wrapping; cast range to int.
                    return f"{int(new_base)} + FLOOR({{qty_noise}} * {int(new_range)})"
                # No extra parens — `*` binds tighter than `+` and adding
                # parens can unbalance an outer ROUND/GREATEST clamp.
                return f"{new_base} + {{qty_noise}} * {new_range}"

            new_expr, n = _BASE_RANGE_RE.subn(_sub, expr, count=1)
            if n:
                col["generation_expr"] = new_expr
                changes += 1
    return changes


# ---------------------------------------------------------------------------
# Fix 4 — flat-trend KPI columns get seasonal_amplitude and {seasonal_mult}
# ---------------------------------------------------------------------------


# KPI column-name patterns that should ride a monthly seasonal curve.
# Most patterns are unanchored substring matches so suffixes like _ppm,
# _celsius, _per_bbl, _days, _btu_kwh don't accidentally block a match.
# Kept narrow enough to avoid cumulative counters or identifiers; explicit
# exclusions below are stripped after the substring check.
_KPI_NAME_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r".*_pct\b", r".*_ratio\b", r".*_rate\b",  # _rate / _rate_per_*
        r".*_score\b", r".*_efficiency\b", r".*_accuracy\b", r".*_uptime\b",
        r".*_oee\b", r".*_health\b", r".*margin.*",  # margin_pct / egt_margin_celsius
        r".*_yield\b", r".*_factor\b", r".*_index\b",
        r"^mtbf.*", r"^mttr.*", r".*rul.*", r"^ccc.*",
        r".*availability.*", r".*utilization.*",
        r".*compliance.*", r".*throughput.*", r".*intensity.*",
        r"^saidi.*", r"^saifi.*", r"^caidi.*",
        r".*gor.*", r".*water_cut.*", r".*recovery.*",
        r".*velocity.*", r".*dwell.*",
        # Oil & gas production rates (bbl/day, mcf/day) and physical
        # measurements (heat rate, flow rate) — period rates, NOT cumulative.
        r".*_bopd\b", r".*_bpd\b", r".*_mcfpd\b",
        r".*heat_rate.*", r".*flow_rate.*",
        # ppm / dpmo defect rates are demo-trend-relevant.
        r".*_ppm\b", r".*_dpmo\b",
    ]
]

# Columns that match a KPI pattern but should NOT get seasonality (cumulative
# counters, identifiers, or values where seasonal lift would be misleading).
_KPI_NAME_EXCLUSIONS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"^cumulative_", r"_total$", r"_count$", r"_id$",
    ]
]


_TREND_KEYWORDS_RE = re.compile(
    r"\b(monthly\s+trend|month[ -]over[ -]month|trended monthly|"
    r"trended over time|year[ -]over[ -]year|trend in|trend across)\b",
    re.IGNORECASE,
)


def _spec_has_trend_question(spec: dict) -> bool:
    for q in spec.get("sample_questions", []) or []:
        if _TREND_KEYWORDS_RE.search(q):
            return True
    for b in spec.get("benchmarks", []) or []:
        if _TREND_KEYWORDS_RE.search(b.get("question", "")):
            return True
    return False


def _is_kpi_column_name(name: str) -> bool:
    if not name:
        return False
    if any(p.match(name) for p in _KPI_NAME_EXCLUSIONS):
        return False
    return any(p.match(name) for p in _KPI_NAME_PATTERNS)


def apply_fix_flat_trend(spec: dict) -> int:
    """For every KPI-named column in a spec that has at least one trend
    question, set seasonal_amplitude=0.15 and wrap {qty_noise} with
    ({qty_noise} * {seasonal_mult}) so monthly trends show a real curve.
    Idempotent: skip columns that already have non-zero amplitude.
    """
    if not _spec_has_trend_question(spec):
        return 0
    changes = 0
    for table in spec.get("tables", []):
        for col in table.get("columns", []):
            if col.get("is_dimension"):
                continue
            name = col.get("name") or ""
            if not _is_kpi_column_name(name):
                continue
            amp = float(col.get("seasonal_amplitude") or 0.0)
            if amp > 0.0:
                continue  # already seasonal — skip
            expr = col.get("generation_expr") or ""
            if "{qty_noise}" not in expr.lower():
                continue
            if "{seasonal_mult}" in expr.lower():
                # Already references seasonal_mult — only set amplitude.
                col["seasonal_amplitude"] = 0.15
                changes += 1
                continue
            # Wrap the first {qty_noise} occurrence with the seasonal multiplier.
            new_expr = re.sub(
                r"\{\s*qty_noise\s*\}",
                "({qty_noise} * {seasonal_mult})",
                expr,
                count=1,
                flags=re.IGNORECASE,
            )
            col["generation_expr"] = new_expr
            col["seasonal_amplitude"] = 0.15
            changes += 1
    return changes


# ---------------------------------------------------------------------------
# Fix 5 — right-size "Top N" to actual dim cardinality
# ---------------------------------------------------------------------------


_TOPN_RE = re.compile(r"\btop\s+(\d+)\s+([a-z][a-z ]+?)\b", re.IGNORECASE)


# Map of question-noun patterns to candidate dimension column names.
# We resolve cardinality from table.dimension_values uniqueness on the
# chosen column. Plurals are normalized.
_NOUN_TO_COLUMNS = {
    "supplier": ["supplier_id", "supplier_name"],
    "suppliers": ["supplier_id", "supplier_name"],
    "region": ["region", "supplier_region", "service_region", "customer_region"],
    "regions": ["region", "supplier_region", "service_region", "customer_region"],
    "department": ["department", "department_name"],
    "departments": ["department", "department_name"],
    "tool": ["tool_id", "tool_name", "machine_id"],
    "tools": ["tool_id", "tool_name", "machine_id"],
    "product line": ["product_line", "product_line_name"],
    "product lines": ["product_line", "product_line_name"],
    "product family": ["product_family", "product_family_name"],
    "product families": ["product_family", "product_family_name"],
    "gl category": ["gl_category"],
    "gl categories": ["gl_category"],
    "crew type": ["crew_type"],
    "crew types": ["crew_type"],
}


def _dimension_cardinality(spec: dict, candidates: list[str]) -> int:
    """Return the distinct count of the first matching column across tables."""
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
    # Also check CASE values in generation_expr for that column.
    for table in spec.get("tables", []):
        for col in table.get("columns", []):
            if (col.get("name") or "").lower() in [c.lower() for c in candidates]:
                expr = col.get("generation_expr") or ""
                # Count distinct 'THEN <literal>' values.
                literals = set(re.findall(r"THEN\s+'([^']+)'", expr, re.IGNORECASE))
                if literals:
                    return len(literals)
    return 0


def _rewrite_topn(question: str, spec: dict) -> tuple[str, bool]:
    """Return (rewritten_question, changed)."""
    def _sub(match: re.Match[str]) -> str:
        n = int(match.group(1))
        noun = match.group(2).strip().lower()
        # Strip trailing prepositions that the regex sometimes catches.
        noun = re.sub(r"\s+(by|with|and|in|having|where|for)$", "", noun).strip()
        candidates = _NOUN_TO_COLUMNS.get(noun)
        if not candidates:
            return match.group(0)
        card = _dimension_cardinality(spec, candidates)
        if card == 0 or card >= n:
            return match.group(0)
        # Cardinality is below N — rewrite to "Rank <noun>".
        return f"Rank {match.group(2).strip()}"

    new_q = _TOPN_RE.sub(_sub, question)
    return new_q, new_q != question


def apply_fix_topn_cardinality(spec: dict) -> int:
    """Rewrite "Top N X" where X has fewer than N distinct values."""
    changes = 0
    new_samples = []
    for q in spec.get("sample_questions", []) or []:
        new_q, changed = _rewrite_topn(q, spec)
        if changed:
            changes += 1
        new_samples.append(new_q)
    spec["sample_questions"] = new_samples

    for b in spec.get("benchmarks", []) or []:
        new_q, changed = _rewrite_topn(b.get("question", ""), spec)
        if changed:
            b["question"] = new_q
            changes += 1

    for ex in spec.get("example_sqls", []) or []:
        new_q, changed = _rewrite_topn(ex.get("question", ""), spec)
        if changed:
            ex["question"] = new_q
            changes += 1
    return changes


# ---------------------------------------------------------------------------
# Fix 6 — Promote Genie-judged-good SQL to be the new gold (from an actions
# JSON produced by ``scripts/analyze_benchmark_failures.py``).
# ---------------------------------------------------------------------------


# Module-level state set by main() before run_modes() begins iterating.
# Keyed by ``"<subindustry>/<use_case>"`` → list of action dicts that have
# ``category == "PROMOTE_GENIE_SQL_TO_GOLD"`` for that spec.
_PROMOTE_ACTIONS: dict[str, list[dict]] = {}


_CLAUSE_SPLIT_RE = re.compile(
    r"(?i)\s+(?=(?:LEFT\s+|RIGHT\s+|FULL\s+|INNER\s+|OUTER\s+|CROSS\s+)?JOIN\b"
    r"|FROM\b|WHERE\b|GROUP\s+BY\b|HAVING\b|ORDER\s+BY\b|LIMIT\b|UNION\b)"
)


def _normalize_genie_sql(sql: str, schema_basename: str) -> list[str]:
    """Convert a Genie-produced SQL string into the spec ``sql_lines`` shape.

    - Strip surrounding whitespace + trailing semicolons.
    - Drop backtick identifier quotes (Spark accepts both).
    - Replace any ``<catalog>.<schema_basename>`` occurrences with ``{fqn}``.
    - Split on top-level clause keywords so each clause is its own line.
    """
    s = sql.strip().rstrip(";").strip()
    s = s.replace("`", "")
    # Substitute any `<catalog>.<schema_basename>` (e.g.
    # ``logistics_demos_catalog.route_planning``) with ``{fqn}``.
    if schema_basename:
        s = re.sub(
            r"\b[A-Za-z_][A-Za-z0-9_]*\." + re.escape(schema_basename) + r"\b",
            "{fqn}",
            s,
        )
    parts = _CLAUSE_SPLIT_RE.split(s)
    # Collapse ALL whitespace runs (including embedded \n from Genie's CTE
    # formatting) to a single space — keeps each spec sql_lines entry on one
    # physical line, which is the convention elsewhere in the corpus.
    cleaned = [re.sub(r"\s+", " ", p).strip() for p in parts if p and p.strip()]
    # Stdlib re's variable-width lookbehind limitation means our split also
    # fires between "LEFT" and "JOIN". Rejoin any modifier-only line with the
    # following JOIN clause.
    join_modifiers = {"LEFT", "RIGHT", "FULL", "INNER", "OUTER", "CROSS"}
    merged: list[str] = []
    i = 0
    while i < len(cleaned):
        token = cleaned[i]
        if token.upper() in join_modifiers and i + 1 < len(cleaned):
            merged.append(f"{token} {cleaned[i+1]}")
            i += 2
        else:
            merged.append(token)
            i += 1
    return merged


def apply_fix_bench_promote_genie(spec: dict, spec_key: str) -> int:
    """Replace gold ``sql_lines`` for benchmark questions whose paired
    action says ``PROMOTE_GENIE_SQL_TO_GOLD``.

    Matches by exact ``question`` text within the spec's ``benchmarks``.
    Skipped silently when there's no action for this spec or no matching
    question, so the mode is safe to run alongside others.
    """
    actions = _PROMOTE_ACTIONS.get(spec_key) or []
    if not actions:
        return 0
    schema_basename = spec.get("schema_basename") or ""
    # Build a question→suggested_sql map for O(1) lookup.
    by_q: dict[str, str] = {}
    for a in actions:
        sg = a.get("suggested_gold_sql")
        q = a.get("question")
        if sg and q and a.get("category") == "PROMOTE_GENIE_SQL_TO_GOLD":
            by_q[q] = sg
    if not by_q:
        return 0
    changes = 0
    for b in spec.get("benchmarks", []) or []:
        q = b.get("question")
        if not q or q not in by_q:
            continue
        new_lines = _normalize_genie_sql(by_q[q], schema_basename)
        if not new_lines:
            continue
        # Idempotence: skip if already identical.
        if b.get("sql_lines") == new_lines:
            continue
        b["sql_lines"] = new_lines
        changes += 1
    return changes


# ---------------------------------------------------------------------------
# Fix 7 — "Monthly trend" questions must have DATE_TRUNC('month', ...) in gold.
# ---------------------------------------------------------------------------


_MONTHLY_TREND_RE = re.compile(r"\bmonthly\b", re.IGNORECASE)
_DATE_TOKEN_RE = re.compile(
    r"\b(\w*(?:_date|_timestamp|snapshot_month|_month|_time|order_dt|ticket_dt))\b",
    re.IGNORECASE,
)


def _rewrite_monthly_trend(sql_lines: list[str]) -> tuple[list[str], bool]:
    """If gold SELECT references a bare date column, wrap in DATE_TRUNC('month', …).

    Skips lines that already contain ``DATE_TRUNC(``.
    """
    if not sql_lines:
        return sql_lines, False
    if any("DATE_TRUNC(" in line.upper() for line in sql_lines):
        return sql_lines, False

    select_line_idx = None
    for i, line in enumerate(sql_lines):
        if re.match(r"^\s*SELECT\b", line, re.IGNORECASE):
            select_line_idx = i
            break
    if select_line_idx is None:
        return sql_lines, False

    select_line = sql_lines[select_line_idx]
    m = _DATE_TOKEN_RE.search(select_line)
    if not m:
        return sql_lines, False
    date_col = m.group(1)
    # Replace the first occurrence of "<date_col>" (not when prefixed with
    # ``.`` to avoid touching qualified references mid-string).
    rewritten_select = re.sub(
        r"(?<![A-Za-z0-9_.])" + re.escape(date_col) + r"(?![A-Za-z0-9_])",
        f"DATE_TRUNC('month', {date_col}) AS month",
        select_line,
        count=1,
    )
    if rewritten_select == select_line:
        return sql_lines, False
    new_lines = list(sql_lines)
    new_lines[select_line_idx] = rewritten_select
    # Rewrite ORDER BY <date_col> → ORDER BY month
    for j, line in enumerate(new_lines):
        if re.match(r"^\s*ORDER\s+BY\b", line, re.IGNORECASE):
            new_lines[j] = re.sub(
                r"(?<![A-Za-z0-9_.])" + re.escape(date_col) + r"(?![A-Za-z0-9_])",
                "month",
                line,
            )
    return new_lines, True


def apply_fix_bench_monthly_trend(spec: dict) -> int:
    """Wrap bare date columns in DATE_TRUNC('month', …) for monthly-trend Qs."""
    changes = 0
    for item_key in ("benchmarks", "example_sqls"):
        for item in spec.get(item_key, []) or []:
            q = item.get("question") or ""
            if not _MONTHLY_TREND_RE.search(q):
                continue
            new_lines, ch = _rewrite_monthly_trend(item.get("sql_lines") or [])
            if ch:
                item["sql_lines"] = new_lines
                changes += 1
    return changes


# ---------------------------------------------------------------------------
# Fix 8 — "Top X" / "highest" / "lowest" questions need explicit LIMIT.
# ---------------------------------------------------------------------------


# Match cardinality-style superlatives that ask for an ordered list of
# entities, not "most recent X" (singular event) which uses a different
# shape.  Require a noun following the superlative (5 chars+) to skip
# things like "the lowest" alone.
_TOPN_PHRASE_RE = re.compile(
    r"\b(?:top\s+\d+|top\s+\w+|highest|lowest|largest|smallest|worst|best)\b\s+\w{3,}",
    re.IGNORECASE,
)


def _has_limit_clause(sql_lines: list[str]) -> bool:
    return any(re.match(r"^\s*LIMIT\b", l, re.IGNORECASE) for l in sql_lines)


def apply_fix_bench_top_limit(spec: dict) -> int:
    """Append ``LIMIT 10`` to gold SQL for "top X" / "highest …" benchmarks."""
    changes = 0
    for item_key in ("benchmarks", "example_sqls"):
        for item in spec.get(item_key, []) or []:
            q = item.get("question") or ""
            if not _TOPN_PHRASE_RE.search(q):
                continue
            lines = item.get("sql_lines") or []
            if not lines or _has_limit_clause(lines):
                continue
            item["sql_lines"] = list(lines) + ["LIMIT 10"]
            changes += 1
    return changes


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


FixFn = Callable[[dict, str], int]


def _wrap(fn: Callable[[dict], int]) -> FixFn:
    """Adapter for fixes that don't need spec_key."""
    return lambda spec, key: fn(spec)


# Mode name -> applicator (takes spec dict + "<subindustry>/<use_case>" key).
MODES: dict[str, FixFn] = {
    "fix-seed-modulo": _wrap(apply_fix_seed_modulo),
    "fix-correlated-hash": _wrap(apply_fix_correlated_hash),
    "fix-wrong-range": apply_fix_wrong_range,
    "fix-flat-trend": _wrap(apply_fix_flat_trend),
    "fix-topn-cardinality": _wrap(apply_fix_topn_cardinality),
    "fix-bench-promote-genie": apply_fix_bench_promote_genie,
    "fix-bench-monthly-trend": _wrap(apply_fix_bench_monthly_trend),
    "fix-bench-top-limit": _wrap(apply_fix_bench_top_limit),
}

# Documented safe order (smaller, more targeted fixes first).
_MODE_ORDER = [
    "fix-seed-modulo",
    "fix-wrong-range",
    "fix-correlated-hash",
    "fix-flat-trend",
    "fix-topn-cardinality",
    # Benchmark-driven fixes (run after Phase-1 mechanical fixes).
    "fix-bench-promote-genie",
    "fix-bench-monthly-trend",
    "fix-bench-top-limit",
]


def _spec_key(path: Path) -> str:
    return f"{path.parent.name}/{path.stem}"


def _show_diff(before: str, after: str, label: str, lines: int = 80) -> None:
    diff = list(difflib.unified_diff(
        before.splitlines(), after.splitlines(),
        fromfile=f"{label} (before)", tofile=f"{label} (after)", lineterm="",
    ))
    if not diff:
        return
    print(f"\n=== {label} ===")
    print("\n".join(diff[:lines]))
    if len(diff) > lines:
        print(f"... ({len(diff) - lines} more diff lines)")


def run_modes(modes: list[str], paths: Iterable[Path], *, dry_run: bool, show_diff: bool) -> int:
    total_changes: dict[str, int] = defaultdict(int)
    files_changed = 0
    for path in paths:
        key = _spec_key(path)
        spec = load_spec(path)
        before = json.dumps(spec, indent=2, ensure_ascii=False, sort_keys=False)
        per_mode_changes: dict[str, int] = {}
        for mode in modes:
            fn = MODES[mode]
            n = fn(spec, key)
            per_mode_changes[mode] = n
            total_changes[mode] += n
        after = json.dumps(spec, indent=2, ensure_ascii=False, sort_keys=False)
        if before != after:
            files_changed += 1
            tag = ", ".join(f"{m}={n}" for m, n in per_mode_changes.items() if n)
            _logger.info("[%s] %s", key, tag)
            if show_diff:
                _show_diff(before, after, key)
            if not dry_run:
                write_spec(path, spec)
    print()
    print("=" * 70)
    print(f"Files changed: {files_changed} / {sum(1 for _ in paths)}")
    for mode in modes:
        if total_changes[mode]:
            print(f"  {mode}: {total_changes[mode]} substitution(s)")
    print("=" * 70)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for mode in MODES:
        parser.add_argument(f"--{mode}", action="store_true", help=MODES[mode].__doc__ or mode)
    parser.add_argument("--all", action="store_true",
                        help="run all Phase 1 mechanical modes in the safe order")
    parser.add_argument("--subindustry", help="filter to one subindustry folder")
    parser.add_argument("--use-case", help="filter to one use-case file stem")
    parser.add_argument("--dry-run", action="store_true", help="do not write changes")
    parser.add_argument("--diff", action="store_true", help="show short diffs per spec")
    parser.add_argument(
        "--actions",
        help=(
            "Path to JSON produced by scripts/analyze_benchmark_failures.py — "
            "required for --fix-bench-promote-genie."
        ),
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    selected = [m for m in _MODE_ORDER if getattr(args, m.replace("-", "_"))]
    if args.all:
        selected = list(_MODE_ORDER)
    if not selected:
        parser.error("provide one of --fix-* or --all")
        return 2

    # Load actions JSON if the promote mode is selected.
    if "fix-bench-promote-genie" in selected:
        if not args.actions:
            parser.error("--fix-bench-promote-genie requires --actions <path.json>")
            return 2
        with open(args.actions, encoding="utf-8") as f:
            manifest = json.load(f)
        global _PROMOTE_ACTIONS
        _PROMOTE_ACTIONS = defaultdict(list)
        for a in manifest.get("actions", []):
            key = f"{a['subindustry']}/{a['use_case']}"
            _PROMOTE_ACTIONS[key].append(a)
        _logger.info(
            "Loaded %d action(s) covering %d spec(s) from %s",
            len(manifest.get("actions", [])), len(_PROMOTE_ACTIONS), args.actions,
        )

    paths = iter_specs(args.subindustry, args.use_case)
    if not paths:
        _logger.error("no specs matched filter")
        return 2
    _logger.info("selected %d specs and modes %s", len(paths), selected)
    return run_modes(selected, paths, dry_run=args.dry_run, show_diff=args.diff)


if __name__ == "__main__":
    sys.exit(main())
