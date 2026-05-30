"""Genie payload construction and workspace API helpers."""

from __future__ import annotations

import json
import logging
import os
import re
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

    # Text instructions (no deployer prefix — pure directive content only)
    text_instructions = [
        {
            "id": next_id(),
            "content": [domain_spec.genie_instructions],
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

    title = f"{domain_spec.industry} - {domain_spec.space_title}"

    return {
        "title": title,
        "description": description,
        "parent_path": f"/Workspace/Users/{username}",
        "warehouse_id": warehouse_id,
        "curated": True,
        "serialized_space": json.dumps(serialized_space),
    }


def _interpolate_fqn(sql_lines: list[str], fqn: str) -> list[str]:
    """Replace {fqn} placeholders in SQL lines."""
    return [line.replace("{fqn}", fqn) for line in sql_lines]


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


def create_or_preserve_genie_space(
    spark,
    domain_spec: Any,
    fqn: str,
    warehouse_id: str,
    username: str,
    excluded_views: Optional[set[str]] = None,
    workspace_client: Any = None,
) -> GenieSpaceResult:
    """Provision the managed Genie space for a deploy — preserve-only.

    If a managed space already exists for this title, keep it as-is (stable
    ``space_id``) and return it; the surrounding deploy still
    CREATE-OR-REPLACEs the backing tables/views, so the preserved space simply
    serves refreshed data. Only when none exists is a space created. There is
    no delete-and-recreate path: space_ids never change on refresh, so their
    tags and ACLs persist across cycles.

    Note: a preserved space does NOT pick up spec changes (new questions/
    instructions/columns). To rebuild after a spec change, first delete the
    space (e.g. the monthly_refresh ``teardown_first`` wipe), then deploy —
    with none present, this creates a fresh one.
    """

    ws = workspace_client or _default_workspace_client()

    # 1. Find existing managed spaces for this title.
    final_title = f"{domain_spec.industry} - {domain_spec.space_title}"
    existing = find_managed_spaces(spark, fqn, final_title, workspace_client=ws)

    # 2. Preserve: keep the existing space (stable space_id). The deploy has
    # already refreshed the backing tables/views it points at.
    if existing:
        keep = existing[0]
        space_id = keep.get("space_id")
        host = ws.config.host.rstrip("/")
        leftover = [s.get("space_id") for s in existing[1:] if s.get("space_id")]
        if leftover:
            _logger.warning(
                "Preserve: %d duplicate managed spaces for %r; keeping %s, "
                "leaving %s untouched", len(leftover), final_title, space_id, leftover,
            )
        return GenieSpaceResult(
            status="preserved",
            requested=True,
            warehouse_id=warehouse_id,
            title=keep.get("title", final_title),
            space_id=space_id,
            url=f"{host}/genie/rooms/{space_id}?isDbOne=true&utm_source=databricks-one",
        )

    # 3. None exists — create a fresh space.
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

    # 3b. Best-effort: grant configured admin groups CAN_MANAGE on the new
    # space. With preserve-only refresh, space_id is stable, so this grant
    # persists and is only applied on first creation.
    _grant_configured_admin_groups(ws, space_id)

    return GenieSpaceResult(
        status="created",
        requested=True,
        warehouse_id=warehouse_id,
        title=payload["title"],
        parent_path=payload["parent_path"],
        space_id=space_id,
        url=f"{host}/genie/rooms/{space_id}?isDbOne=true&utm_source=databricks-one",
    )


_TIMESTAMP_SUFFIX_RE = re.compile(r"\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*$")


def _list_all_genie_spaces(ws: Any) -> list[dict[str, Any]]:
    """List every Genie space in the workspace, walking all pagination pages.

    The /api/2.0/genie/spaces endpoint caps responses at ~100 spaces per
    page and returns a ``next_page_token``; without pagination, large
    workspaces (175+ spaces) silently truncate.
    """
    spaces: list[dict[str, Any]] = []
    page_token: Optional[str] = None
    seen_tokens: set[str] = set()
    while True:
        path = "/api/2.0/genie/spaces"
        if page_token:
            path = f"{path}?page_token={page_token}"
        data = _api_request(ws, "GET", path)
        if not isinstance(data, dict):
            break
        spaces.extend(data.get("spaces", []))
        page_token = data.get("next_page_token")
        if not page_token or page_token in seen_tokens:
            break
        seen_tokens.add(page_token)
    return spaces


def find_managed_spaces(
    spark, fqn: str, title: Optional[str] = None, workspace_client: Any = None,
) -> list[dict[str, Any]]:
    """List spaces owned by this package for the target namespace.

    Matches on three signals so that previous deploys are reliably found
    even when Databricks auto-renamed them on title-conflict:

      1. Exact title equality.
      2. Title equality after stripping a trailing " YYYY-MM-DD HH:MM:SS"
         suffix the Databricks Genie API appends on title collisions.
      3. Legacy ``fqn=<...>`` marker in the description (pre-2026 deploys).
    """

    ws = workspace_client or _default_workspace_client()
    spaces = _list_all_genie_spaces(ws)

    legacy_marker = f"fqn={fqn}"
    expected_title = title or ""
    results: list[dict[str, Any]] = []
    for space in spaces:
        space_title = space.get("title", "") or ""
        if expected_title:
            if space_title == expected_title:
                results.append(space)
                continue
            # Databricks auto-renames duplicates with a timestamp suffix.
            stripped = _TIMESTAMP_SUFFIX_RE.sub("", space_title)
            if stripped == expected_title:
                results.append(space)
                continue
        if legacy_marker in (space.get("description", "") or ""):
            results.append(space)
    return results


def _grant_configured_admin_groups(ws: Any, space_id: str) -> None:
    """PATCH CAN_MANAGE for each group named in GENIE_FACTORY_ADMIN_GROUPS.

    Comma-separated env var, e.g. ``"genie-factory-admins,demo-leads"``.
    Empty/unset → no-op. Failures are logged but never raised — the space
    was created successfully and a permission grant should not abort deploy.
    """
    raw = os.environ.get("GENIE_FACTORY_ADMIN_GROUPS", "").strip()
    if not raw:
        return
    groups = [g.strip() for g in raw.split(",") if g.strip()]
    if not groups:
        return
    try:
        grant_space_permissions(
            ws,
            space_id,
            [{"group_name": g, "permission_level": "CAN_MANAGE"} for g in groups],
        )
    except Exception as exc:
        _logger.warning(
            "Failed to grant Genie space permissions on %s: %s", space_id, exc
        )


def grant_space_permissions(
    ws: Any,
    space_id: str,
    acl_entries: list[dict[str, Any]],
) -> None:
    """PATCH /api/2.0/permissions/genie/{space_id} with the given ACL entries.

    PATCH appends to the existing ACL (PUT would replace it). Idempotent for
    the same principal+level. Raises on failure — callers that want
    best-effort behavior should catch and log themselves.
    """
    if not acl_entries:
        return
    _api_request(
        ws,
        "PATCH",
        f"/api/2.0/permissions/genie/{space_id}",
        payload={"access_control_list": acl_entries},
    )


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

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status_code = response.getcode()
            response_text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"{method} {path} failed with status {exc.code}: {error_body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {path} failed: {exc}") from exc

    if status_code not in expected_statuses:
        raise RuntimeError(
            f"{method} {path} failed with status {status_code}: {response_text}"
        )

    if not response_text:
        return {}
    return json.loads(response_text)
