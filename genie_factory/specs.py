"""Load pre-generated DomainSpec JSON files from the specs/ directory."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from .generator import DomainSpec

_SPECS_DIR = Path(__file__).parent / "specs"

# The universal warm-up question that opens every demo's question arc. It works
# for any space and gets the room comfortable with Genie before the bespoke
# composition + payoff questions.
DEMO_OPENER_QUESTION = (
    "Showcase the different visualization options with interesting aspects "
    "of the dataset"
)


def render_space_description(scenario: str, questions: list[str]) -> str:
    """Render a Genie space description in the standard Scenario/Questions format.

    ``scenario`` is a 2-3 sentence, second-person narrative that puts the SA in
    the operator's seat and ends in a provocative question. ``questions`` are
    the demo questions in arc order (typically opener -> composition -> payoff);
    each is annotated with ``(agent)`` in the rendered prose to cue the demoer
    to run it in agent / deep-research mode.

    The annotation lives only in this prose. The clickable starter chips
    (``sample_questions``) carry the same questions *without* the suffix, since
    chip text is sent to Genie verbatim as a query.
    """
    lines = [f"**Scenario:** {scenario.strip()}", "", "**Questions:**", ""]
    for i, q in enumerate(questions, start=1):
        lines.append(f"{i}. {q.strip()} (agent)")
    return "\n".join(lines)


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
