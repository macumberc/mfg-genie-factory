"""Notebook convenience functions for browsing and deploying manufacturing use cases."""

from __future__ import annotations

from typing import Any, Optional

from .presets import SUBINDUSTRIES, USE_CASES


def list_use_cases(subindustry: Optional[str] = None) -> None:
    """Pretty-print available manufacturing subindustries and use cases.

    Parameters
    ----------
    subindustry : str, optional
        If given, show only use cases for that subindustry.
        If omitted, show all subindustries with their use cases.
    """
    if subindustry:
        key = _resolve_subindustry(subindustry)
        cases = USE_CASES[key]
        print(f"\n{key} ({len(cases)} use cases)")
        print("-" * 60)
        for i, uc in enumerate(cases):
            imp = uc.get("importance", "")
            imp_str = f"  [importance: {imp}]" if imp else ""
            print(f"  {i}. {uc['label']}{imp_str}")
        print()
        return

    total = sum(len(v) for v in USE_CASES.values())
    print(f"\nManufacturing Use Cases ({total} total across {len(SUBINDUSTRIES)} subindustries)")
    print("=" * 60)
    for sub in SUBINDUSTRIES:
        cases = USE_CASES.get(sub, [])
        if not cases:
            continue
        print(f"\n{sub} ({len(cases)} use cases)")
        print("-" * 60)
        for i, uc in enumerate(cases):
            imp = uc.get("importance", "")
            imp_str = f"  [importance: {imp}]" if imp else ""
            print(f"  {i}. {uc['label']}{imp_str}")
    print()


def deploy_use_case(
    subindustry: str,
    use_case: str | int,
    **overrides: Any,
) -> dict[str, Any]:
    """Deploy a Genie room for a preset manufacturing use case.

    Parameters
    ----------
    subindustry : str
        Subindustry name (e.g. "Automotive", "Semiconductor").
        Case-insensitive partial matching is supported.
    use_case : str or int
        Use case label (e.g. "Vehicle Recall Root Cause Analysis")
        or 0-based index from ``list_use_cases()``.
    **overrides
        Additional keyword arguments passed to ``deploy()``
        (e.g. catalog, schema, warehouse_id).

    Returns
    -------
    dict
        Deployment result. Pass as ``**result`` to ``teardown()``.
    """
    from . import deploy
    from .specs import load_spec

    sub_key = _resolve_subindustry(subindustry)
    cases = USE_CASES[sub_key]
    preset = _resolve_use_case(cases, use_case, sub_key)

    # Load pre-generated spec if available
    spec = load_spec(sub_key, preset["label"])
    if spec:
        overrides["domain_spec"] = spec

    params: dict[str, Any] = {
        "industry": sub_key,
        "use_case": preset["use_case"],
    }
    if "company_name" in preset:
        params["company_name"] = preset["company_name"]
    if "business_context" in preset:
        params["business_context"] = preset["business_context"]

    params.update(overrides)
    return deploy(**params)


def _resolve_subindustry(name: str) -> str:
    """Resolve a subindustry name with case-insensitive partial matching."""
    lower = name.lower()
    # Exact match first
    for sub in SUBINDUSTRIES:
        if sub.lower() == lower:
            return sub
    # Partial match
    matches = [sub for sub in SUBINDUSTRIES if lower in sub.lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(
            f"Ambiguous subindustry '{name}'. Matches: {matches}"
        )
    raise ValueError(
        f"Unknown subindustry '{name}'. Available: {SUBINDUSTRIES}"
    )


def _resolve_use_case(
    cases: list[dict], identifier: str | int, subindustry: str
) -> dict:
    """Resolve a use case by label (partial match) or index."""
    if isinstance(identifier, int):
        if 0 <= identifier < len(cases):
            return cases[identifier]
        raise ValueError(
            f"Use case index {identifier} out of range for {subindustry} "
            f"(0-{len(cases) - 1})"
        )
    lower = identifier.lower()
    for uc in cases:
        if uc["label"].lower() == lower:
            return uc
    matches = [uc for uc in cases if lower in uc["label"].lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        labels = [m["label"] for m in matches]
        raise ValueError(
            f"Ambiguous use case '{identifier}'. Matches: {labels}"
        )
    labels = [uc["label"] for uc in cases]
    raise ValueError(
        f"Unknown use case '{identifier}' in {subindustry}. Available: {labels}"
    )
