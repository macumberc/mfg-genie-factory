"""Load pre-generated DomainSpec JSON files from the specs/ directory."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from .generator import DomainSpec

_SPECS_DIR = Path(__file__).parent / "specs"


def _slugify(name: str) -> str:
    """Convert a display name to a filesystem-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    return slug.strip("_")


def _spec_path(subindustry: str, use_case_label: str) -> Path:
    return _SPECS_DIR / _slugify(subindustry) / f"{_slugify(use_case_label)}.json"


def load_spec(subindustry: str, use_case_label: str) -> Optional[DomainSpec]:
    """Load a pre-generated DomainSpec, or return None if it doesn't exist."""
    path = _spec_path(subindustry, use_case_label)
    if not path.exists():
        return None
    with open(path) as f:
        return DomainSpec.from_dict(json.load(f))


def spec_exists(subindustry: str, use_case_label: str) -> bool:
    """Check whether a pre-generated spec exists for this use case."""
    return _spec_path(subindustry, use_case_label).exists()


def save_spec(spec: DomainSpec, subindustry: str, use_case_label: str) -> Path:
    """Save a DomainSpec as JSON. Returns the path written."""
    path = _spec_path(subindustry, use_case_label)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(spec.to_dict(), f, indent=2)
    return path
