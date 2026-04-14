"""Deterministic SQL builders driven by a DomainSpec."""

from __future__ import annotations

import re
from typing import Any


def _fix_boolean_arithmetic(expr: str) -> str:
    """Fix boolean * number patterns that Spark SQL doesn't support.

    Replaces patterns like ``(boolean_expr) * value`` with
    ``CASE WHEN (boolean_expr) THEN value ELSE 0 END``.
    Spark SQL does not implicitly cast BOOLEAN to INT.

    Handles compound expressions like:
    - ``(col IN (...)) * 8.0``
    - ``((month(dt) IN (6,7,8)) AND (category = 'X')) * 8.0``
    """

    def _find_matching_paren(s: str, start: int) -> int:
        """Find the index of the closing paren matching the one at `start`."""
        depth = 0
        for i in range(start, len(s)):
            if s[i] == '(':
                depth += 1
            elif s[i] == ')':
                depth -= 1
                if depth == 0:
                    return i
        return -1

    result = expr
    # Iterate until no more matches (handles nested cases)
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(result):
            if result[i] == '(':
                close = _find_matching_paren(result, i)
                if close == -1:
                    i += 1
                    continue
                inner = result[i + 1:close]
                # Check if what follows is ` * number`
                after = result[close + 1:].lstrip()
                mul_match = re.match(r'\*\s*([\d.]+)', after)
                if mul_match and re.search(r'\bIN\b|\bAND\b|\bOR\b|[<>=!]', inner, re.IGNORECASE):
                    value = mul_match.group(1)
                    end_pos = close + 1 + (len(result[close + 1:]) - len(result[close + 1:].lstrip())) + len(mul_match.group(0))
                    replacement = f"CASE WHEN ({inner}) THEN {value} ELSE 0 END"
                    result = result[:i] + replacement + result[end_pos:]
                    changed = True
                    break  # restart scan from beginning
            i += 1
    return result


def _fix_malformed_function_calls(expr: str) -> str:
    """Fix LLM-generated SQL where function names run into keywords.

    Common patterns: ``NULLIFCASE`` → ``NULLIF(CASE``,
    ``COALESCECASE`` → ``COALESCE(CASE``, ``IFFCASE`` → ``IFF(CASE``,
    and similar concatenations where the opening paren is missing.
    """
    _FUNCTIONS = r"(?:NULLIF|COALESCE|IFF|IFNULL|NVL|GREATEST|LEAST|ROUND|ABS|CAST|CONCAT|SUBSTRING|TRIM|UPPER|LOWER|DATE_FORMAT|DATEDIFF|DATE_ADD|DATE_SUB)"
    _KEYWORDS = r"(?:CASE|SELECT|WHEN|IF|VALUES)"
    result = re.sub(
        rf"\b({_FUNCTIONS})({_KEYWORDS})\b",
        r"\1(\2",
        expr,
        flags=re.IGNORECASE,
    )
    return result


def _check_balanced_parens(expr: str) -> bool:
    """Return True if parentheses are balanced (ignoring string literals)."""
    depth = 0
    in_string = False
    for i, c in enumerate(expr):
        if c == "'" and not in_string:
            in_string = True
        elif c == "'" and in_string:
            # Check for escaped quote ''
            if i + 1 < len(expr) and expr[i + 1] == "'":
                continue
            in_string = False
        elif not in_string:
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth < 0:
                    return False
    return depth == 0


def _strip_string_literals(expr: str) -> str:
    """Remove SQL string literals from an expression for keyword analysis."""
    return re.sub(r"'(?:''|[^'])*'", "''", expr)


def _check_balanced_case(expr: str) -> bool:
    """Return True if every CASE has a matching END (ignoring string literals)."""
    stripped = _strip_string_literals(expr).upper()
    cases = len(re.findall(r"\bCASE\b", stripped))
    ends = len(re.findall(r"\bEND\b", stripped))
    return cases == ends


def _check_balanced_quotes(expr: str) -> bool:
    """Return True if single quotes are balanced."""
    # Count unescaped single quotes ('' is an escape, counts as 0)
    cleaned = expr.replace("''", "")
    return cleaned.count("'") % 2 == 0


def _validate_expression(expr: str, context: str = "") -> str | None:
    """Validate a SQL expression for common LLM mistakes.

    Returns an error message if invalid, None if OK.
    """
    if not expr:
        return None
    if not _check_balanced_parens(expr):
        return f"Unbalanced parentheses in {context}: {expr[:100]}"
    if not _check_balanced_case(expr):
        return f"Unbalanced CASE/END in {context}: {expr[:100]}"
    if not _check_balanced_quotes(expr):
        return f"Unbalanced quotes in {context}: {expr[:100]}"
    return None


# SQL reserved words that need backtick-quoting when used as column names
_SQL_RESERVED = frozenset({
    "select", "from", "where", "case", "when", "then", "else", "end",
    "and", "or", "not", "in", "is", "as", "by", "on", "join", "left",
    "right", "inner", "outer", "full", "cross", "group", "order", "having",
    "limit", "union", "all", "distinct", "into", "values", "set", "update",
    "delete", "insert", "create", "drop", "alter", "table", "view",
    "index", "schema", "database", "catalog", "between", "like", "exists",
    "null", "true", "false", "date", "time", "timestamp", "interval",
    "with", "recursive", "window", "partition", "rows", "range",
})


def build_table_sqls_from_spec(
    domain_spec: Any,
    fqn: str,
    seed: int,
    scale: int = 1,
    target_rows: int | None = None,
) -> dict[str, str]:
    """Build all deterministic CTAS statements from a DomainSpec."""

    sqls: dict[str, str] = {}
    for table in domain_spec.tables:
        sqls[table.table_name] = _build_table_sql(table, fqn, seed, scale, target_rows=target_rows)
    return sqls


def build_metric_view_sqls_from_spec(
    domain_spec: Any,
    fqn: str,
) -> dict[str, str]:
    """Build all CREATE VIEW WITH METRICS statements from a DomainSpec."""

    sqls: dict[str, str] = {}
    for mv in domain_spec.metric_views:
        sqls[mv.view_name] = _build_metric_view_sql(mv, fqn)
    return sqls


def get_table_column_comments(domain_spec: Any) -> dict[str, dict[str, str]]:
    """Extract column comments from a DomainSpec for ALTER TABLE statements."""

    comments: dict[str, dict[str, str]] = {}
    for table in domain_spec.tables:
        cols: dict[str, str] = {}
        for col in table.columns:
            if col.comment:
                cols[col.name] = col.comment
        comments[table.table_name] = cols
    return comments


def get_table_descriptions(domain_spec: Any) -> dict[str, str]:
    """Extract table descriptions from a DomainSpec for table-level comments."""

    return {t.table_name: t.description for t in domain_spec.tables if t.description}


def table_fqdns(domain_spec: Any, fqn: str) -> dict[str, str]:
    """Return fully qualified names for all managed tables."""

    return {t.table_name: f"{fqn}.{t.table_name}" for t in domain_spec.tables}


def metric_view_fqdns(domain_spec: Any, fqn: str) -> dict[str, str]:
    """Return fully qualified names for all metric views."""

    return {mv.view_name: f"{fqn}.{mv.view_name}" for mv in domain_spec.metric_views}


# ---------------------------------------------------------------------------
# Internal SQL builders
# ---------------------------------------------------------------------------


def _start_year(scale: int) -> int:
    """Compute the start year based on scale (scale=1 -> 2025 only)."""
    return 2025 - (scale - 1)


def _build_table_sql(table: Any, fqn: str, seed: int, scale: int, target_rows: int | None = None) -> str:
    """Build a deterministic CTAS for a single table from its TableSpec."""

    start_year = _start_year(scale)
    archetype = table.entity_dimension  # "transaction", "snapshot", or "forecast"

    # Build VALUES blocks for dimension data
    entities = table.dimension_values
    if not entities:
        raise ValueError(f"Table {table.table_name} has no dimension_values")

    # Determine the value columns from the first entity's keys
    entity_keys = list(entities[0].keys())
    entity_rows = [[e[k] for k in entity_keys] for e in entities]
    entity_values = _values_sql(entity_rows)
    entity_aliases = ", ".join(f"`{k}`" for k in entity_keys)

    # Determine the category key (first key that contains 'category' or 'type',
    # or fall back to the second key)
    category_key = None
    for k in entity_keys:
        if "category" in k.lower() or "type" in k.lower():
            category_key = k
            break
    if not category_key and len(entity_keys) > 1:
        category_key = entity_keys[1]
    if not category_key:
        category_key = entity_keys[0]

    # Build the primary key column reference for the entity
    entity_pk = entity_keys[0]

    # Compute probability multiplier for row scaling.
    # Only transaction (fact) tables get scaled to target_rows.
    # Snapshot/forecast (dimension-like) tables skip the selection
    # filter entirely — their pair_filter alone produces natural sizes.
    num_entities = len(entities)
    if archetype in ("snapshot", "forecast"):
        # High probability effectively disables the selection filter;
        # the pair_filter (hash % 100 < 52) is the sole row limiter.
        prob_multiplier = 1.0 / 0.03  # makes effective prob ≈ 1.0
    elif target_rows and target_rows > 0:
        date_points = int(scale * 365 * 5 / 7)  # weekdays
        skeleton_size = date_points * num_entities
        base_prob = 0.03
        needed_prob = target_rows / max(skeleton_size, 1)
        prob_multiplier = needed_prob / base_prob
        prob_multiplier = max(0.1, min(prob_multiplier, 50.0))
    else:
        prob_multiplier = 1.0

    # Build seasonal probability CASE expression
    seasonal = table.seasonal_patterns or {}
    category_dist = table.category_distribution or {}

    # Backtick-quote the category key for safe use in SQL
    cat_col = f"`{category_key}`"

    case_lines = []
    for cat, month_probs in seasonal.items():
        if isinstance(month_probs, dict):
            for months_str, prob in month_probs.items():
                months = _parse_months(months_str)
                if months:
                    month_list = ", ".join(str(m) for m in months)
                    scaled_prob = min(prob * prob_multiplier, 1.0)
                    case_lines.append(
                        f"      WHEN {cat_col} = '{_sql_escape(cat)}' "
                        f"AND mo IN ({month_list}) THEN {scaled_prob:.4f}"
                    )
        # Default probability for this category
        default_prob = min(category_dist.get(cat, 0.03) * prob_multiplier, 1.0)
        case_lines.append(
            f"      WHEN {cat_col} = '{_sql_escape(cat)}' THEN {default_prob:.4f}"
        )

    fallback_prob = min(0.03 * prob_multiplier, 1.0)
    if not case_lines:
        # No seasonal/category data; use a flat probability for all rows
        case_expr = f"    {fallback_prob:.4f}"
    else:
        case_expr = "    CASE\n" + "\n".join(case_lines) + f"\n      ELSE {fallback_prob:.4f}\n    END"

    # Hash-based noise columns (backtick-quote entity PK for safety)
    pk_ref = f"e.`{entity_pk}`"
    qty_noise = _hash_fraction(seed, "qty_noise", "d.dt", pk_ref)
    status_noise = _hash_fraction(seed, "status_noise", "d.dt", pk_ref)
    select_noise = _hash_fraction(seed, "select_noise", "d.dt", pk_ref)
    id_seq = _hash_int(seed, "id_seq", "d.dt", pk_ref, modulo=500)

    # Determine date interval based on archetype
    if archetype == "snapshot":
        interval = "INTERVAL 7 DAY"
    elif archetype == "forecast":
        interval = "INTERVAL 1 MONTH"
    else:
        interval = "INTERVAL 1 DAY"

    # Build column SELECT expressions
    # In the final SELECT, reference the pre-computed column names from skeleton,
    # not the raw hash expressions (which contain d./e. aliases that don't exist here).
    select_cols = []
    expression_errors = []
    for col in table.columns:
        expr = col.generation_expr
        if expr:
            # Case-insensitive placeholder replacement
            for placeholder, replacement in [
                ("{fqn}", fqn), ("{table}", table.table_name),
                ("{qty_noise}", "qty_noise"), ("{status_noise}", "status_noise"),
                ("{select_noise}", "select_noise"), ("{id_seq}", "id_seq"),
                ("{seed}", str(seed)),
            ]:
                expr = re.sub(re.escape(placeholder), replacement, expr, flags=re.IGNORECASE)
            # Strip d./e. table aliases — columns are flat in filtered CTE
            expr = _strip_cte_aliases(expr)
            # Fix boolean arithmetic patterns Spark doesn't support
            expr = _fix_boolean_arithmetic(expr)
            # Fix LLM concatenations like NULLIFCASE → NULLIF(CASE
            expr = _fix_malformed_function_calls(expr)
            # Validate expression structure
            err = _validate_expression(expr, context=col.name)
            if err:
                expression_errors.append(err)
            # Backtick-quote column name if it's a SQL reserved word
            col_name = f"`{col.name}`" if col.name.lower() in _SQL_RESERVED else col.name
            select_cols.append(f"  {expr} AS {col_name}")
        else:
            col_name = f"`{col.name}`" if col.name.lower() in _SQL_RESERVED else col.name
            select_cols.append(f"  {col_name}")

    # If any expressions have structural errors, raise before building SQL
    if expression_errors:
        raise ValueError(
            f"LLM generated invalid SQL expressions for table '{table.table_name}':\n"
            + "\n".join(f"  - {e}" for e in expression_errors)
        )

    select_clause = ",\n".join(select_cols)

    # Weekday filter for transaction tables
    weekday_filter = ""
    if archetype == "transaction":
        weekday_filter = "  WHERE DAYOFWEEK(d.dt) BETWEEN 2 AND 6\n"

    # Pair hash filter for snapshot/forecast tables
    pair_filter = ""
    if archetype in ("snapshot", "forecast"):
        pair_hash = _hash_int(seed, "pair_hash", pk_ref, modulo=100)
        pair_filter = f"  WHERE {pair_hash} < 52\n"

    sql = f"""CREATE OR REPLACE TABLE {fqn}.{table.table_name} AS
WITH
entities AS (
  SELECT * FROM VALUES
{entity_values}
  AS t({entity_aliases})
),
date_range AS (
  SELECT EXPLODE(SEQUENCE(DATE'{start_year}-01-01', DATE'2025-12-31', {interval})) AS dt
),
skeleton AS (
  SELECT
    d.dt,
    e.*,
    {qty_noise} AS qty_noise,
    {status_noise} AS status_noise,
    {select_noise} AS select_noise,
    {id_seq} AS id_seq,
    MONTH(d.dt) AS mo
  FROM date_range d
  CROSS JOIN entities e
{weekday_filter}{pair_filter}),
filtered AS (
  SELECT *,
{case_expr} AS selection_prob
  FROM skeleton
)
SELECT
{select_clause}
FROM filtered
WHERE select_noise < selection_prob"""

    return sql.strip()


def _yaml_safe(value: str) -> str:
    """Quote a YAML value if it contains special characters."""
    if not value:
        return "''"
    # Characters that need quoting in YAML values
    if any(c in value for c in (":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`")):
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    return value


def _build_metric_view_sql(mv: Any, fqn: str) -> str:
    """Build a CREATE VIEW WITH METRICS statement from a MetricViewSpec."""

    dim_lines = []
    for dim in mv.dimensions:
        dim_lines.append(f"  - name: {dim['name']}")
        dim_lines.append(f"    expr: {_yaml_safe(dim['expr'])}")

    measure_lines = []
    for m in mv.measures:
        measure_lines.append(f"  - name: {m['name']}")
        measure_lines.append(f"    expr: {_yaml_safe(m['expr'])}")
        if m.get("comment"):
            measure_lines.append(f"    comment: {_yaml_safe(m['comment'])}")

    dims_yaml = "\n".join(dim_lines)
    measures_yaml = "\n".join(measure_lines)

    return f"""CREATE OR REPLACE VIEW {fqn}.{mv.view_name}
WITH METRICS
LANGUAGE YAML
AS $$
version: 1.1
source: {fqn}.{mv.source_table}

dimensions:
{dims_yaml}

measures:
{measures_yaml}
$$""".strip()


# ---------------------------------------------------------------------------
# SQL helpers (replicated from reference)
# ---------------------------------------------------------------------------


def _strip_cte_aliases(expr: str) -> str:
    """Remove d. and e. table alias prefixes from a SQL expression.

    In the skeleton CTE, columns come from ``date_range d`` and ``entities e``.
    By the time the final SELECT runs over ``filtered``, all columns are flat
    so references like ``d.dt`` or ``e.patient_id`` must become ``dt`` / ``patient_id``.

    This version is quote-aware: it only strips aliases outside of single-quoted
    SQL string literals, so patterns like ``'d.value'`` are preserved.
    """
    import re

    # Split on single-quoted segments (including escaped quotes '')
    parts = re.split(r"('(?:''|[^'])*')", expr)
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Not inside quotes
            parts[i] = re.sub(r'\b([de])\.(\w+)', r'\2', part)
    return "".join(parts)


def _values_sql(rows: list[list[object]]) -> str:
    """Render rows into a deterministic SQL VALUES block."""

    lines = []
    for idx, row in enumerate(rows):
        prefix = "    " if idx == 0 else "  , "
        rendered = ", ".join(_sql_value(value) for value in row)
        lines.append(f"{prefix}({rendered})")
    return "\n".join(lines)


def _sql_value(value: object) -> str:
    """Render a scalar as a SQL literal."""

    if value is None:
        return "NULL"
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    return str(value)


def _sql_escape(value: str) -> str:
    """Escape single quotes in a SQL string."""
    return value.replace("'", "''")


def _hash_fraction(seed: int, salt: str, *parts: str, scale: int = 10000) -> str:
    """Create a deterministic pseudo-random decimal in the range [0, 1)."""

    sql_parts = ", ".join([f"'{seed}'", f"'{salt}'", *parts])
    return f"(CAST(pmod(hash({sql_parts}), {scale}) AS DOUBLE) / {scale}.0)"


def _hash_int(
    seed: int,
    salt: str,
    *parts: str,
    modulo: int,
    offset: int = 0,
) -> str:
    """Create a deterministic pseudo-random integer."""

    sql_parts = ", ".join([f"'{seed}'", f"'{salt}'", *parts])
    base = f"pmod(hash({sql_parts}), {modulo})"
    if offset == 0:
        return base
    if offset > 0:
        return f"({base} + {offset})"
    return f"({base} - {abs(offset)})"


def _parse_months(months_str: str) -> list[int]:
    """Parse a months string like '11,12' or '1-3' into a list of ints."""

    result = []
    for part in str(months_str).split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            try:
                result.extend(range(int(start), int(end) + 1))
            except ValueError:
                pass
        else:
            try:
                result.append(int(part))
            except ValueError:
                pass
    return result
