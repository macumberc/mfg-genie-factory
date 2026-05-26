"""Run Genie's native benchmark eval-runs against deployed spaces.

Wraps the Databricks SDK's ``ws.genie.genie_create_eval_run`` /
``genie_get_eval_run`` / ``genie_list_eval_results`` /
``genie_get_eval_result_details`` methods. Genie's own judge produces the
GOOD / BAD / NEEDS_REVIEW assessments per question — identical to the
*Evaluation* tab in the Genie UI.

Module entry points:

    python -m genie_factory.benchmark run \\
        --subindustries logistics,machinery,... \\
        [--use-cases route_planning,asset_health,...] \\
        --output benchmark_<ts>.jsonl

    python -m genie_factory.benchmark aggregate <jsonl> \\
        [--markdown <md>]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from .genie import _TIMESTAMP_SUFFIX_RE, _default_workspace_client, _list_all_genie_spaces
from .presets import SUBINDUSTRIES, USE_CASES
from .specs import _slugify, load_spec

_logger = logging.getLogger(__name__)

_TERMINAL_STATUSES = {
    "DONE",
    "EVALUATION_FAILED",
    "EVALUATION_TIMEOUT",
    "EVALUATION_CANCELLED",
}


@dataclass
class SpaceRun:
    subindustry: str
    use_case: str
    space_id: Optional[str]
    space_title: Optional[str]
    eval_run_id: Optional[str]
    status: str
    num_questions: int = 0
    num_correct: int = 0
    num_needs_review: int = 0
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class QuestionResult:
    subindustry: str
    use_case: str
    space_id: str
    space_title: str
    eval_run_id: str
    result_id: str
    question: Optional[str]
    expected_sql: Optional[str]
    actual_sql: Optional[str]
    assessment: Optional[str]
    assessment_reasons: list[str] = field(default_factory=list)


def _subindustry_slug_map() -> dict[str, str]:
    """slug → display name (e.g. ``oil_gas_upstream`` → ``Oil & Gas Upstream``)."""
    return {_slugify(name): name for name in SUBINDUSTRIES}


def _expected_title(subindustry: str, use_case_label: str) -> Optional[str]:
    """Reproduce the deploy-time title shape: ``"<industry> - <space_title>"``."""
    spec = load_spec(subindustry, use_case_label)
    if spec is None:
        return None
    return f"{spec.industry} - {spec.space_title}"


def _build_title_index(spaces: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Map exact title AND timestamp-suffix-stripped title back to the space dict."""
    index: dict[str, dict[str, Any]] = {}
    for sp in spaces:
        title = (sp.get("title") or "").strip()
        if not title:
            continue
        index[title] = sp
        stripped = _TIMESTAMP_SUFFIX_RE.sub("", title)
        if stripped != title:
            index.setdefault(stripped, sp)
    return index


def _resolve_scope(
    subindustry_slugs: list[str],
    use_case_filter: Optional[set[str]] = None,
) -> list[tuple[str, str, str]]:
    """Return ``[(subindustry_slug, subindustry_display, use_case_label), ...]``.

    ``use_case_filter`` is an optional set of use-case **slugs** to keep.
    """
    slug_map = _subindustry_slug_map()
    scope: list[tuple[str, str, str]] = []
    for slug in subindustry_slugs:
        display = slug_map.get(slug)
        if display is None:
            raise ValueError(
                f"Unknown subindustry slug {slug!r}. Valid: {sorted(slug_map)}"
            )
        for entry in USE_CASES.get(display, []):
            label = entry["label"]  # type: ignore[index]
            uc_slug = _slugify(label)  # type: ignore[arg-type]
            if use_case_filter and uc_slug not in use_case_filter:
                continue
            scope.append((slug, display, label))  # type: ignore[arg-type]
    return scope


def _extract_sql(response_list: Any) -> Optional[str]:
    """Best-effort extraction of SQL string from a list of GenieEvalResponse dicts.

    The SDK returns ``actual_response`` / ``expected_response`` as lists of
    GenieEvalResponse objects; each may carry a ``query`` or text payload.
    """
    if not response_list:
        return None
    parts: list[str] = []
    for item in response_list:
        d = _to_dict(item)
        # GenieEvalResponse: {"response": "<SQL string>", "response_type": "SQL",
        # "sql_execution_result": {...}}. Older shapes also tried as fallbacks.
        for path in (("response",), ("query", "query"), ("sql",), ("content",), ("text",)):
            cur: Any = d
            ok = True
            for key in path:
                if isinstance(cur, dict) and key in cur:
                    cur = cur[key]
                else:
                    ok = False
                    break
            if ok and isinstance(cur, str) and cur.strip():
                parts.append(cur)
                break
    return "\n---\n".join(parts) if parts else None


def _to_dict(obj: Any) -> dict[str, Any]:
    """Convert an SDK dataclass-ish object to a plain dict (recursive)."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "as_dict"):
        try:
            return obj.as_dict()
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return {}


def _enum_value(obj: Any) -> Optional[str]:
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    val = getattr(obj, "value", None)
    if isinstance(val, str):
        return val
    name = getattr(obj, "name", None)
    if isinstance(name, str):
        return name
    return str(obj)


def _kick_off_one(ws: Any, scope_entry: tuple[str, str, str], title_index: dict[str, dict[str, Any]]) -> SpaceRun:
    sub_slug, sub_display, use_case_label = scope_entry
    title = _expected_title(sub_display, use_case_label)
    if title is None:
        return SpaceRun(
            subindustry=sub_slug,
            use_case=_slugify(use_case_label),
            space_id=None,
            space_title=None,
            eval_run_id=None,
            status="spec_not_found",
            error=f"No spec for {sub_display}/{use_case_label}",
        )
    space = title_index.get(title)
    if space is None:
        # Fall back to suffix-stripped lookup (defensive — already covered by index).
        stripped = _TIMESTAMP_SUFFIX_RE.sub("", title)
        space = title_index.get(stripped)
    if space is None:
        return SpaceRun(
            subindustry=sub_slug,
            use_case=_slugify(use_case_label),
            space_id=None,
            space_title=title,
            eval_run_id=None,
            status="space_not_found",
            error=f"No deployed Genie space with title {title!r}",
        )
    space_id = space.get("space_id")
    if not space_id:
        return SpaceRun(
            subindustry=sub_slug,
            use_case=_slugify(use_case_label),
            space_id=None,
            space_title=title,
            eval_run_id=None,
            status="space_not_found",
            error="Space dict missing space_id field",
        )
    try:
        resp = ws.genie.genie_create_eval_run(space_id=space_id)
    except Exception as exc:
        return SpaceRun(
            subindustry=sub_slug,
            use_case=_slugify(use_case_label),
            space_id=space_id,
            space_title=title,
            eval_run_id=None,
            status="create_failed",
            error=f"genie_create_eval_run failed: {exc}",
        )
    return SpaceRun(
        subindustry=sub_slug,
        use_case=_slugify(use_case_label),
        space_id=space_id,
        space_title=title,
        eval_run_id=resp.eval_run_id,
        status=_enum_value(resp.eval_run_status) or "NOT_STARTED",
        num_questions=resp.num_questions or 0,
    )


def _poll_runs(ws: Any, runs: list[SpaceRun], poll_interval: int) -> None:
    """Block until every run with an eval_run_id is in a terminal status.

    Mutates ``runs`` in place — updates ``status``, ``num_correct``,
    ``num_needs_review``, ``num_questions``, and ``duration_seconds``.
    """
    started_at = {r.eval_run_id: time.monotonic() for r in runs if r.eval_run_id}
    in_flight = {r.eval_run_id: r for r in runs if r.eval_run_id and r.status not in _TERMINAL_STATUSES}
    if not in_flight:
        return
    _logger.info("Polling %d in-flight eval runs every %ds", len(in_flight), poll_interval)
    while in_flight:
        time.sleep(poll_interval)
        finished_now: list[str] = []
        for eval_run_id, run in list(in_flight.items()):
            try:
                resp = ws.genie.genie_get_eval_run(
                    space_id=run.space_id, eval_run_id=eval_run_id
                )
            except Exception as exc:
                run.status = "poll_failed"
                run.error = f"genie_get_eval_run failed: {exc}"
                run.duration_seconds = time.monotonic() - started_at[eval_run_id]
                finished_now.append(eval_run_id)
                continue
            run.status = _enum_value(resp.eval_run_status) or run.status
            run.num_questions = resp.num_questions or run.num_questions
            run.num_correct = resp.num_correct or 0
            run.num_needs_review = resp.num_needs_review or 0
            if run.status in _TERMINAL_STATUSES:
                run.duration_seconds = time.monotonic() - started_at[eval_run_id]
                finished_now.append(eval_run_id)
        for k in finished_now:
            in_flight.pop(k, None)
        if in_flight:
            done_summary = ", ".join(
                f"{r.subindustry}/{r.use_case}={r.status}({r.num_correct}/{r.num_questions})"
                for r in in_flight.values()
            )
            _logger.info(
                "Still running: %d. %s", len(in_flight), done_summary[:300]
            )


def _fetch_details_for_run(ws: Any, run: SpaceRun) -> list[QuestionResult]:
    """List per-question results for a single run + fetch full detail per result."""
    if not run.space_id or not run.eval_run_id:
        return []
    # 1. Paginate genie_list_eval_results to enumerate result IDs + question text.
    listings: list[Any] = []
    page_token = None
    while True:
        try:
            resp = ws.genie.genie_list_eval_results(
                space_id=run.space_id,
                eval_run_id=run.eval_run_id,
                page_token=page_token,
            )
        except Exception as exc:
            _logger.warning(
                "genie_list_eval_results failed for %s: %s", run.eval_run_id, exc
            )
            return []
        listings.extend(resp.eval_results or [])
        page_token = getattr(resp, "next_page_token", None)
        if not page_token:
            break

    # 2. For each listing, fetch full details (expected / actual / assessment).
    out: list[QuestionResult] = []
    for item in listings:
        result_id = item.result_id
        try:
            detail = ws.genie.genie_get_eval_result_details(
                space_id=run.space_id,
                eval_run_id=run.eval_run_id,
                result_id=result_id,
            )
        except Exception as exc:
            out.append(
                QuestionResult(
                    subindustry=run.subindustry,
                    use_case=run.use_case,
                    space_id=run.space_id,
                    space_title=run.space_title or "",
                    eval_run_id=run.eval_run_id,
                    result_id=result_id,
                    question=item.question,
                    expected_sql=item.benchmark_answer,
                    actual_sql=None,
                    assessment=None,
                    assessment_reasons=[f"detail_fetch_failed: {exc}"],
                )
            )
            continue
        reasons: list[str] = []
        for r in detail.assessment_reasons or []:
            # ScoreReason is an SDK enum (e.g. <ScoreReason.EMPTY_RESULT: 'EMPTY_RESULT'>).
            val = _enum_value(r)
            if val:
                reasons.append(val)
        out.append(
            QuestionResult(
                subindustry=run.subindustry,
                use_case=run.use_case,
                space_id=run.space_id,
                space_title=run.space_title or "",
                eval_run_id=run.eval_run_id,
                result_id=result_id,
                question=item.question,
                expected_sql=_extract_sql(detail.expected_response)
                or item.benchmark_answer,
                actual_sql=_extract_sql(detail.actual_response),
                assessment=_enum_value(detail.assessment),
                assessment_reasons=reasons,
            )
        )
    return out


def run(
    subindustry_slugs: list[str],
    use_case_slugs: Optional[list[str]] = None,
    poll_interval: int = 15,
    output_jsonl: Optional[str] = None,
    summary_jsonl: Optional[str] = None,
    workspace_client: Any = None,
    detail_workers: int = 8,
) -> tuple[list[SpaceRun], list[QuestionResult]]:
    """Kick off + poll + fetch details for every space in scope.

    Writes per-question results to ``output_jsonl`` (one JSON line each) and
    optionally writes the per-space summary to ``summary_jsonl``.
    """
    ws = workspace_client or _default_workspace_client()
    use_case_filter = set(use_case_slugs) if use_case_slugs else None
    scope = _resolve_scope(subindustry_slugs, use_case_filter)
    _logger.info("Scope: %d spec(s) across %d subindustries", len(scope), len(subindustry_slugs))

    _logger.info("Listing all Genie spaces in workspace...")
    spaces = _list_all_genie_spaces(ws)
    _logger.info("Found %d total spaces; building title index", len(spaces))
    title_index = _build_title_index(spaces)

    runs: list[SpaceRun] = []
    for entry in scope:
        sr = _kick_off_one(ws, entry, title_index)
        runs.append(sr)
        _logger.info(
            "Kick-off %s/%s → %s (eval_run_id=%s, status=%s)",
            sr.subindustry, sr.use_case, sr.space_id or "—",
            sr.eval_run_id or "—", sr.status,
        )
        time.sleep(0.5)  # be gentle with the API

    _poll_runs(ws, runs, poll_interval)

    # Fetch detail for every run that has an eval_run_id (even failed ones —
    # partial results often present).
    detail_targets = [r for r in runs if r.eval_run_id]
    all_results: list[QuestionResult] = []
    if detail_targets:
        with ThreadPoolExecutor(max_workers=detail_workers) as pool:
            futures = {pool.submit(_fetch_details_for_run, ws, r): r for r in detail_targets}
            for fut in as_completed(futures):
                r = futures[fut]
                try:
                    qrs = fut.result()
                except Exception as exc:
                    _logger.warning(
                        "Detail fetch failed for %s/%s: %s",
                        r.subindustry, r.use_case, exc,
                    )
                    qrs = []
                _logger.info(
                    "Fetched %d result(s) for %s/%s", len(qrs), r.subindustry, r.use_case
                )
                all_results.extend(qrs)

    if output_jsonl:
        Path(output_jsonl).write_text(
            "\n".join(json.dumps(asdict(q), default=str) for q in all_results) + ("\n" if all_results else "")
        )
        _logger.info("Wrote %d question result(s) to %s", len(all_results), output_jsonl)
    if summary_jsonl:
        Path(summary_jsonl).write_text(
            "\n".join(json.dumps(asdict(s), default=str) for s in runs) + ("\n" if runs else "")
        )
        _logger.info("Wrote %d space summary line(s) to %s", len(runs), summary_jsonl)

    return runs, all_results


def aggregate(jsonl_path: str, markdown_path: Optional[str] = None) -> str:
    """Read the question-level JSONL, return a markdown rollup.

    If ``markdown_path`` is provided, also write the markdown to disk.
    """
    rows: list[dict[str, Any]] = []
    for line in Path(jsonl_path).read_text().splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))

    by_spec: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_spec[(r["subindustry"], r["use_case"])].append(r)

    overall = Counter(r.get("assessment") or "UNKNOWN" for r in rows)
    total = sum(overall.values()) or 1
    good = overall.get("GOOD", 0)
    bad = overall.get("BAD", 0)
    needs = overall.get("NEEDS_REVIEW", 0)

    lines: list[str] = []
    lines.append(f"# Genie Benchmark Results — {jsonl_path}")
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append(f"- Total questions: **{total}**")
    lines.append(f"- GOOD: **{good}** ({good/total*100:.1f}%)")
    lines.append(f"- NEEDS_REVIEW: **{needs}** ({needs/total*100:.1f}%)")
    lines.append(f"- BAD: **{bad}** ({bad/total*100:.1f}%)")
    other = total - good - bad - needs
    if other:
        lines.append(f"- Other / null: **{other}** ({other/total*100:.1f}%)")
    lines.append("")

    # Per-subindustry rollup
    by_sub: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        by_sub[r["subindustry"]][r.get("assessment") or "UNKNOWN"] += 1
    lines.append("## By subindustry")
    lines.append("")
    lines.append("| Subindustry | Total | GOOD | NEEDS_REVIEW | BAD | Pass% |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for sub in sorted(by_sub):
        c = by_sub[sub]
        tot = sum(c.values()) or 1
        g = c.get("GOOD", 0)
        n = c.get("NEEDS_REVIEW", 0)
        b = c.get("BAD", 0)
        lines.append(
            f"| {sub} | {tot} | {g} | {n} | {b} | {g/tot*100:.1f}% |"
        )
    lines.append("")

    # Per-spec rollup
    lines.append("## By spec")
    lines.append("")
    lines.append("| Subindustry | Use case | Total | GOOD | NEEDS_REVIEW | BAD | Pass% |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for (sub, uc) in sorted(by_spec):
        items = by_spec[(sub, uc)]
        c = Counter(i.get("assessment") or "UNKNOWN" for i in items)
        tot = len(items) or 1
        g = c.get("GOOD", 0)
        n = c.get("NEEDS_REVIEW", 0)
        b = c.get("BAD", 0)
        lines.append(
            f"| {sub} | {uc} | {tot} | {g} | {n} | {b} | {g/tot*100:.1f}% |"
        )
    lines.append("")

    # Failing questions detail
    fails = [r for r in rows if r.get("assessment") in {"BAD", "NEEDS_REVIEW"}]
    if fails:
        lines.append(f"## Failing / needs-review questions ({len(fails)})")
        lines.append("")
        for r in fails:
            lines.append(
                f"### {r['subindustry']}/{r['use_case']} — {r.get('assessment')}"
            )
            lines.append("")
            lines.append(f"**Q:** {r.get('question') or '—'}")
            lines.append("")
            if r.get("assessment_reasons"):
                lines.append("**Reasons:**")
                for reason in r["assessment_reasons"]:
                    lines.append(f"- {reason}")
                lines.append("")
            if r.get("expected_sql"):
                lines.append("**Expected SQL:**")
                lines.append("```sql")
                lines.append(r["expected_sql"])
                lines.append("```")
                lines.append("")
            if r.get("actual_sql"):
                lines.append("**Generated SQL:**")
                lines.append("```sql")
                lines.append(r["actual_sql"])
                lines.append("```")
                lines.append("")

    out = "\n".join(lines)
    if markdown_path:
        Path(markdown_path).write_text(out)
    return out


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m genie_factory.benchmark")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Kick off + poll Genie eval runs.")
    run_p.add_argument(
        "--subindustries", required=True,
        help="Comma-separated subindustry slugs (e.g. logistics,machinery,oil_gas_upstream).",
    )
    run_p.add_argument(
        "--use-cases", default=None,
        help="Optional comma-separated use_case slug filter (matches the directory filename basename).",
    )
    run_p.add_argument("--poll-interval", type=int, default=15)
    run_p.add_argument("--output", required=True, help="Path to write JSONL question results.")
    run_p.add_argument("--summary", default=None, help="Optional path for per-space summary JSONL.")

    agg_p = sub.add_parser("aggregate", help="Roll up a JSONL into markdown.")
    agg_p.add_argument("jsonl_path")
    agg_p.add_argument("--markdown", default=None)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = _build_parser().parse_args(argv)
    if args.cmd == "run":
        subs = [s.strip() for s in args.subindustries.split(",") if s.strip()]
        ucs = (
            [s.strip() for s in args.use_cases.split(",") if s.strip()]
            if args.use_cases else None
        )
        runs, results = run(
            subindustry_slugs=subs,
            use_case_slugs=ucs,
            poll_interval=args.poll_interval,
            output_jsonl=args.output,
            summary_jsonl=args.summary,
        )
        # Brief stdout summary.
        c = Counter(q.assessment or "UNKNOWN" for q in results)
        print(
            f"\nDone. Spaces: {len(runs)}, Questions: {len(results)}, "
            f"GOOD={c.get('GOOD',0)}, NEEDS_REVIEW={c.get('NEEDS_REVIEW',0)}, BAD={c.get('BAD',0)}"
        )
        return 0
    if args.cmd == "aggregate":
        md = aggregate(args.jsonl_path, markdown_path=args.markdown)
        if not args.markdown:
            print(md)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
