"""Genie payload construction and workspace API helpers."""

from __future__ import annotations

import json
import logging
import random
import time
from typing import Any, Optional
import urllib.error
import urllib.request


from .config import AUTO_WAREHOUSE, HTTP_TIMEOUT_SECONDS
from .results import GenieSpaceResult

_logger = logging.getLogger("genie_factory")


def build_genie_payload(
    domain_spec: Any,
    fqn: str,
    warehouse_id: str,
    username: str,
    excluded_views: Optional[set[str]] = None,
) -> dict[str, Any]:
    """Build the Genie REST payload from a DomainSpec."""

    # Counter for generating unique IDs
    id_counter = [0]

    def next_id() -> str:
        id_counter[0] += 1
        return f"01f12000000000000000000000000{id_counter[0]:03d}"

    # Sample questions
    sample_questions = []
    for q in domain_spec.sample_questions:
        sample_questions.append({"id": next_id(), "question": [q]})

    # Data sources: base tables + metric views, sorted by identifier
    data_sources = []
    for table in domain_spec.tables:
        identifier = f"{fqn}.{table.table_name}"
        column_configs = []
        for col in table.columns:
            if col.is_dimension:
                if "date" in col.name.lower() or col.sql_type == "DATE":
                    column_configs.append(
                        {"column_name": col.name, "enable_format_assistance": True}
                    )
                else:
                    column_configs.append(
                        {
                            "column_name": col.name,
                            "enable_format_assistance": True,
                            "enable_entity_matching": True,
                        }
                    )
        entry: dict[str, Any] = {
            "identifier": identifier,
            "description": [table.description],
        }
        if column_configs:
            column_configs.sort(key=lambda c: c["column_name"])
            entry["column_configs"] = column_configs
        data_sources.append(entry)

    _excluded = excluded_views or set()
    for mv in domain_spec.metric_views:
        if mv.view_name in _excluded:
            continue
        identifier = f"{fqn}.{mv.view_name}"
        measures_list = ", ".join(m["name"] for m in mv.measures)
        dims_list = ", ".join(d["name"] for d in mv.dimensions)
        entry: dict[str, Any] = {
            "identifier": identifier,
            "description": [
                f"Metric view for {mv.source_table}. "
                f"Dimensions: {dims_list}. "
                f"Measures: {measures_list}. "
                f"Query with MEASURE() and GROUP BY ALL."
            ],
        }
        mv_col_configs = []
        for dim in mv.dimensions:
            if "date" in dim["name"].lower() or "month" in dim["name"].lower():
                mv_col_configs.append(
                    {"column_name": dim["name"], "enable_format_assistance": True}
                )
            else:
                mv_col_configs.append(
                    {
                        "column_name": dim["name"],
                        "enable_format_assistance": True,
                        "enable_entity_matching": True,
                    }
                )
        if mv_col_configs:
            mv_col_configs.sort(key=lambda c: c["column_name"])
            entry["column_configs"] = mv_col_configs
        data_sources.append(entry)

    data_sources.sort(key=lambda x: x["identifier"])

    # Text instructions
    deployer_prefix = f"Deployed by {username} using Genie Factory.\n\n"
    text_instructions = [
        {
            "id": next_id(),
            "content": [f"{deployer_prefix}{domain_spec.genie_instructions}"],
        }
    ]

    # Example question SQLs
    example_question_sqls = []
    for ex in domain_spec.example_sqls:
        sql_lines = _interpolate_fqn(ex.sql_lines, fqn)
        example_question_sqls.append(
            {"id": next_id(), "question": [ex.question], "sql": ["\n".join(sql_lines)]}
        )

    # SQL snippets
    filters = []
    for f in domain_spec.sql_snippets.filters:
        filters.append(
            {
                "id": next_id(),
                "sql": [f["sql"]],
                "display_name": f["display_name"],
                "synonyms": f.get("synonyms", []),
                "instruction": [f.get("instruction", "")],
            }
        )

    expressions = []
    for e in domain_spec.sql_snippets.expressions:
        expressions.append(
            {
                "id": next_id(),
                "alias": e["alias"],
                "sql": [e["sql"]],
                "display_name": e["display_name"],
                "synonyms": e.get("synonyms", []),
            }
        )

    measures = []
    for m in domain_spec.sql_snippets.measures:
        measures.append(
            {
                "id": next_id(),
                "alias": m["alias"],
                "sql": [m["sql"]],
                "display_name": m["display_name"],
                "synonyms": m.get("synonyms", []),
            }
        )

    # Benchmarks
    benchmarks = []
    for b in domain_spec.benchmarks:
        sql_lines = _interpolate_fqn(b.sql_lines, fqn)
        benchmarks.append(
            {
                "id": next_id(),
                "question": [b.question],
                "answer": [{"format": "SQL", "content": ["\n".join(sql_lines)]}],
            }
        )

    # join_specs stays empty: the JoinSpec protobuf schema is not publicly
    # documented and schema probes revealed an undocumented required field
    # beyond {id, left.identifier, right.identifier}. Join hints are conveyed
    # via genie_instructions text instead. _derive_join_specs is retained as
    # dead code so we can flip this back once the real schema is known.
    _ = _derive_join_specs  # keep referenced to avoid "unused" linter warning
    serialized_space = {
        "version": 2,
        "config": {"sample_questions": sample_questions},
        "data_sources": {"tables": data_sources},
        "instructions": {
            "text_instructions": text_instructions,
            "example_question_sqls": example_question_sqls,
            "join_specs": [],
            "sql_snippets": {
                "filters": filters,
                "expressions": expressions,
                "measures": measures,
            },
        },
        "benchmarks": {"questions": benchmarks},
    }

    description = domain_spec.space_description

    return {
        "title": domain_spec.space_title,
        "description": description,
        "parent_path": f"/Workspace/Users/{username}",
        "warehouse_id": warehouse_id,
        "curated": True,
        "serialized_space": json.dumps(serialized_space),
    }


def _interpolate_fqn(sql_lines: list[str], fqn: str) -> list[str]:
    """Replace {fqn} placeholders in SQL lines."""
    return [line.replace("{fqn}", fqn) for line in sql_lines]


# FK-looking column suffixes used to derive joins between base tables.
_JOIN_KEY_SUFFIXES = ("_id", "_sku", "_code", "_number")
# Columns that share names across tables but are NOT FK relationships.
_JOIN_KEY_EXCLUDE = {
    "status", "region", "model_year", "make", "model",
    "month_date", "metric_period", "recall_date", "claim_date", "order_date",
}


def _derive_join_specs(domain_spec: Any, fqn: str, next_id: Any) -> list[dict[str, Any]]:
    """Derive Many-to-One join hints from FK-looking columns shared across base tables.

    Field names follow the documented Genie API schema:
      - left_table / right_table: fully qualified table identifiers
      - condition: SQL boolean expression (e.g. "a.id = b.a_id")
      - relationship_type: "Many-to-One" (default for inferred FK joins)

    Metric views are skipped — joins are structural hints for base tables only.
    """
    tables = list(domain_spec.tables)
    col_to_tables: dict[str, list[str]] = {}
    for table in tables:
        seen = set()
        for col in table.columns:
            name = col.name.lower()
            if name in seen:
                continue
            seen.add(name)
            if name in _JOIN_KEY_EXCLUDE:
                continue
            if not any(name.endswith(suf) for suf in _JOIN_KEY_SUFFIXES):
                continue
            col_to_tables.setdefault(name, []).append(table.table_name)

    join_specs: list[dict[str, Any]] = []
    for col_name, table_names in col_to_tables.items():
        if len(table_names) < 2:
            continue
        ordered = sorted(set(table_names))
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                left = f"{fqn}.{ordered[i]}"
                right = f"{fqn}.{ordered[j]}"
                join_specs.append(
                    {
                        "id": next_id(),
                        "left_table": left,
                        "right_table": right,
                        "condition": f"{left}.{col_name} = {right}.{col_name}",
                        "relationship_type": "Many-to-One",
                    }
                )
    return join_specs


def resolve_warehouse_id(
    spark, warehouse_id: Optional[str], workspace_client: Any = None,
) -> tuple[Optional[str], Optional[str]]:
    """Resolve a warehouse id or return a skip reason."""

    if warehouse_id in (None, ""):
        return None, "Genie creation skipped because no warehouse_id was provided."

    if warehouse_id != AUTO_WAREHOUSE:
        return warehouse_id, None

    ws = workspace_client or _default_workspace_client()
    try:
        data = _api_request(ws, "GET", "/api/2.0/sql/warehouses")
    except RuntimeError as exc:
        return None, f"Warehouse auto-discovery failed: {exc}"

    warehouses = data.get("warehouses", []) if isinstance(data, dict) else []
    if not warehouses:
        return None, "No accessible SQL warehouses were found."

    ordered = sorted(warehouses, key=_warehouse_sort_key)
    candidate = ordered[0]
    return candidate.get("id"), None


def create_or_replace_genie_space(
    spark,
    domain_spec: Any,
    fqn: str,
    warehouse_id: str,
    username: str,
    excluded_views: Optional[set[str]] = None,
    workspace_client: Any = None,
) -> GenieSpaceResult:
    """Create a new Genie space, then delete any prior managed spaces.

    Atomic ordering: the new space is created first so that on failure the
    old spaces remain intact and the user still has a working Genie room.
    Old spaces are only cleaned up after the new one succeeds.
    """

    ws = workspace_client or _default_workspace_client()

    # 1. Find existing spaces (before creation, for later cleanup)
    existing = find_managed_spaces(spark, fqn, domain_spec.space_title, workspace_client=ws)

    # 2. Build payload and create new space FIRST
    payload = build_genie_payload(
        domain_spec, fqn, warehouse_id, username, excluded_views=excluded_views
    )
    created = _api_request(
        ws,
        "POST",
        "/api/2.0/genie/spaces",
        payload=payload,
        expected_statuses=(200, 201),
    )
    space_id = created["space_id"]
    host = ws.config.host.rstrip("/")

    # 3. New space succeeded — now safe to delete old spaces
    replaced_ids: list[str] = []
    for space in existing:
        old_id = space.get("space_id")
        if old_id:
            try:
                delete_genie_space(spark, old_id, workspace_client=ws)
                replaced_ids.append(old_id)
            except Exception as exc:
                _logger.warning(
                    "Failed to delete old Genie space %s: %s", old_id, exc
                )

    return GenieSpaceResult(
        status="replaced" if replaced_ids else "created",
        requested=True,
        warehouse_id=warehouse_id,
        title=payload["title"],
        parent_path=payload["parent_path"],
        space_id=space_id,
        url=f"{host}/genie/rooms/{space_id}?isDbOne=true&utm_source=databricks-one",
        replaced_space_ids=replaced_ids,
    )


def find_managed_spaces(
    spark, fqn: str, title: Optional[str] = None, workspace_client: Any = None,
) -> list[dict[str, Any]]:
    """List spaces owned by this package for the target namespace."""

    ws = workspace_client or _default_workspace_client()
    data = _api_request(ws, "GET", "/api/2.0/genie/spaces")
    spaces = data.get("spaces", []) if isinstance(data, dict) else []

    # Primary: match by title (current spaces use clean descriptions)
    # Secondary fallback: match by fqn marker in description (legacy spaces)
    legacy_marker = f"fqn={fqn}"
    results = []
    for space in spaces:
        if title and space.get("title") == title:
            results.append(space)
        elif legacy_marker in (space.get("description", "") or ""):
            results.append(space)
    return results


def delete_genie_space(spark, space_id: str, workspace_client: Any = None) -> None:
    """Delete a Genie space."""

    ws = workspace_client or _default_workspace_client()
    _api_request(
        ws,
        "DELETE",
        f"/api/2.0/genie/spaces/{space_id}",
        expected_statuses=(200, 202, 204),
    )


def _warehouse_sort_key(warehouse: dict[str, Any]) -> tuple[Any, ...]:
    """Prefer running, serverless, Pro, and smaller warehouses."""

    size_rank = {
        "2X-Small": 0,
        "X-Small": 1,
        "Small": 2,
        "Medium": 3,
        "Large": 4,
        "X-Large": 5,
        "2X-Large": 6,
    }
    name = (warehouse.get("name") or "").lower()
    is_serverless = warehouse.get("enable_serverless_compute", False)
    wh_type = (warehouse.get("warehouse_type") or "").upper()
    return (
        warehouse.get("state") != "RUNNING",
        not is_serverless,
        wh_type != "PRO",
        "serverless" not in name,  # fallback heuristic for older API responses
        "starter" not in name,
        "shared" not in name,
        size_rank.get(warehouse.get("cluster_size"), 99),
        name,
    )


def _default_workspace_client():
    """Create a WorkspaceClient from the default auth chain.

    In notebooks, auto-discovers auth from dbutils/env. In the app,
    callers should pass an explicit workspace_client instead.
    """
    from databricks.sdk import WorkspaceClient

    return WorkspaceClient()


def _get_auth_headers(workspace_client) -> dict[str, str]:
    """Get authorization headers from a WorkspaceClient."""
    result = workspace_client.config.authenticate()
    return result() if callable(result) else result


def _api_request(
    workspace_client,
    method: str,
    path: str,
    payload: Optional[dict[str, Any]] = None,
    expected_statuses: tuple[int, ...] = (200,),
    timeout: int = HTTP_TIMEOUT_SECONDS,
) -> Any:
    """Issue a Databricks workspace REST request using WorkspaceClient auth."""

    host = workspace_client.config.host.rstrip("/")
    headers = _get_auth_headers(workspace_client)
    headers["Content-Type"] = "application/json"

    request_body = None
    if payload is not None:
        request_body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url=f"{host}{path}",
        data=request_body,
        method=method,
        headers=headers,
    )

    # Retry with exponential backoff on 429 RESOURCE_EXHAUSTED. The Genie
    # Spaces and Conversation APIs enforce sustained rate limits (5 qpm on the
    # Conversation API free tier) and batch workloads easily produce minutes
    # of backlog. Backoff: 1, 2, 4, 8, 16, 30, 60, 120, 120, 120 seconds plus
    # jitter — ~8 min cumulative across 10 attempts.
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status_code = response.getcode()
                response_text = response.read().decode("utf-8")
            break
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429 and attempt < max_attempts - 1:
                sleep_seconds = min(2 ** attempt, 120) + random.uniform(0, 2.0)
                _logger.warning(
                    "%s %s returned 429; retrying in %.1fs (attempt %d/%d)",
                    method, path, sleep_seconds, attempt + 1, max_attempts,
                )
                time.sleep(sleep_seconds)
                # Rebuild the request — body bytes can be consumed by urlopen.
                request = urllib.request.Request(
                    url=f"{host}{path}", data=request_body,
                    method=method, headers=headers,
                )
                continue
            raise RuntimeError(
                f"{method} {path} failed with status {exc.code}: {error_body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{method} {path} failed: {exc}") from exc
    else:
        raise RuntimeError(f"{method} {path} failed after {max_attempts} attempts")

    if status_code not in expected_statuses:
        raise RuntimeError(
            f"{method} {path} failed with status {status_code}: {response_text}"
        )

    if not response_text:
        return {}
    return json.loads(response_text)
