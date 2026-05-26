"""Generate per-use-case sales demo scripts from spec JSONs.

Run via:
    PYTHONPATH=. python -m genie_factory.demos

Writes one markdown file per spec to demos/<subindustry>/<use_case_slug>.md
mirroring the genie_factory/specs/ layout. The script structure mirrors the
hand-crafted WellFlow demo: at-a-glance card, pre-demo checklist, scenario
framing, acronyms glossary, three-act script, strategic close, anticipated
questions, quick-reference card.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

SPECS_ROOT = "genie_factory/specs"
DEMOS_ROOT = "demos"

# Files held back from auto-regeneration because they're hand-crafted
# reference scripts. Paths are relative to DEMOS_ROOT.
HAND_CRAFTED = frozenset({
    "oil_gas_upstream/well_production_monitoring_flow.md",
})


# ---------------------------------------------------------------------------
# Acronym glossary
# ---------------------------------------------------------------------------
# Hand-curated for the 18 manufacturing subindustries. Anything caught by the
# ALL-CAPS regex but not in this dict is omitted from the glossary (rather than
# emitting a placeholder).
ACRONYMS: dict[str, str] = {
    # Generic business
    "VP": "Vice President",
    "CFO": "Chief Financial Officer",
    "COO": "Chief Operating Officer",
    "CIO": "Chief Information Officer",
    "CEO": "Chief Executive Officer",
    "AOP": "Annual Operating Plan",
    "AFE": "Authorization for Expenditure",
    "JIB": "Joint Interest Billing",
    "P&L": "Profit and Loss statement",
    "EBITDA": "Earnings Before Interest, Taxes, Depreciation, and Amortization",
    "KPI": "Key Performance Indicator",
    "SLA": "Service Level Agreement",
    "ROI": "Return on Investment",
    "TCO": "Total Cost of Ownership",
    "BI": "Business Intelligence",
    "ERP": "Enterprise Resource Planning",
    "MES": "Manufacturing Execution System",
    "PLM": "Product Lifecycle Management",
    "SCADA": "Supervisory Control and Data Acquisition",
    "API": "Application Programming Interface",
    # Oil & gas
    "BOPD": "Barrels of Oil Per Day",
    "BPD": "Barrels Per Day",
    "MCF": "Thousand Cubic Feet (gas volume)",
    "BOE": "Barrels of Oil Equivalent",
    "BBL": "Barrels",
    "GOR": "Gas-Oil Ratio (SCF/BBL)",
    "SCF": "Standard Cubic Feet",
    "LOE": "Lease Operating Expense",
    "ESP": "Electric Submersible Pump",
    "PSI": "Pounds per Square Inch",
    "LNG": "Liquefied Natural Gas",
    "NGL": "Natural Gas Liquids",
    "OPEX": "Operating Expense",
    "CAPEX": "Capital Expenditure",
    "OOIP": "Original Oil In Place",
    "EUR": "Estimated Ultimate Recovery",
    # Aerospace
    "AOG": "Aircraft on Ground",
    "EGT": "Exhaust Gas Temperature",
    "EFH": "Engine Flight Hours",
    "RUL": "Remaining Useful Life",
    "MRO": "Maintenance, Repair & Overhaul",
    "ATA": "Air Transport Association (chapter)",
    "FOD": "Foreign Object Damage",
    "OEM": "Original Equipment Manufacturer",
    # Semiconductor
    "CD": "Critical Dimension",
    "CMP": "Chemical Mechanical Planarization",
    "VM": "Virtual Metrology",
    "MAPE": "Mean Absolute Percentage Error",
    "WIP": "Work In Process",
    "OEE": "Overall Equipment Effectiveness",
    "SPC": "Statistical Process Control",
    "ESD": "Electrostatic Discharge",
    "PFE": "Process First Engagement",
    # Food & beverage / pharma
    "FSMA": "Food Safety Modernization Act",
    "GFSI": "Global Food Safety Initiative",
    "FDA": "Food and Drug Administration",
    "HACCP": "Hazard Analysis and Critical Control Points",
    "SKU": "Stock Keeping Unit",
    "CCP": "Critical Control Point",
    "GMP": "Good Manufacturing Practice",
    "USDA": "U.S. Department of Agriculture",
    # Mining / heavy industry
    "SAG": "Semi-Autogenous Grinding (mill)",
    "TPH": "Tons Per Hour",
    "TPD": "Tons Per Day",
    "ROM": "Run of Mine",
    "ESG": "Environmental, Social, Governance",
    "HSE": "Health, Safety, Environment",
    # Utilities / power
    "SAIDI": "System Average Interruption Duration Index",
    "SAIFI": "System Average Interruption Frequency Index",
    "CAIDI": "Customer Average Interruption Duration Index",
    "NERC": "North American Electric Reliability Corporation",
    "FERC": "Federal Energy Regulatory Commission",
    "MWh": "Megawatt-hour",
    "kWh": "Kilowatt-hour",
    "MW": "Megawatt",
    "GW": "Gigawatt",
    "PPA": "Power Purchase Agreement",
    "T&D": "Transmission and Distribution",
    "DER": "Distributed Energy Resource",
    # Logistics / supply chain
    "OTIF": "On-Time In-Full",
    "DOH": "Days On Hand",
    "DIO": "Days Inventory Outstanding",
    "MAPE_SCOR": "Forecast accuracy (1 - MAPE)",
    "TMS": "Transportation Management System",
    "WMS": "Warehouse Management System",
    "FTL": "Full Truckload",
    "LTL": "Less than Truckload",
    "ETA": "Estimated Time of Arrival",
    # Automotive / industrial
    "PPM": "Parts Per Million (defect rate)",
    "DPMO": "Defects Per Million Opportunities",
    "FPY": "First Pass Yield",
    "MTBF": "Mean Time Between Failures",
    "MTTR": "Mean Time To Repair",
    "JIT": "Just In Time",
    "EMS": "Electronic Manufacturing Services",
    # Construction / engineering
    "RFI": "Request For Information",
    "EPC": "Engineering, Procurement, Construction",
    "PMP": "Project Management Plan",
    # Railroad
    "OS": "On Schedule",
    "FRA": "Federal Railroad Administration",
    "TOFC": "Trailer On Flat Car",
    "COFC": "Container On Flat Car",
    # Misc industry
    "EHS": "Environment, Health, Safety",
    "QA": "Quality Assurance",
    "QC": "Quality Control",
    "RCA": "Root Cause Analysis",
    "RCM": "Reliability-Centered Maintenance",
    "PdM": "Predictive Maintenance",
    "PM": "Preventive Maintenance",
}


# ---------------------------------------------------------------------------
# Parsed-spec dataclass
# ---------------------------------------------------------------------------
@dataclass
class ParsedSpec:
    company: str
    industry: str
    use_case: str
    title: str
    schema: str
    narrative: str
    kpis: list[str]
    sources: list[str]
    personas: list[tuple[str, str]]  # (persona, job_to_be_done)
    sample_questions: list[str]
    benchmarks: list[str]
    tables: list[dict]
    metric_views: list[dict]
    acronyms: dict[str, str]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
_BULLET_RE = re.compile(r"^[\-•]\s*(.+)$", re.MULTILINE)
# ALL-CAPS token detector — 2-6 chars, optionally with lowercase tail
# (e.g. PdM), optional slash for AOG/EFH-style compounds.
_ACRONYM_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,5}(?:/[A-Z0-9]{1,5})?)\b")


def _section_text(desc: str, header: str, next_header: str | None) -> str:
    """Pull the body of a `**Header**` section out of space_description."""
    pat = rf"\*\*{re.escape(header)}\*\*\s*\n+(.*?)"
    if next_header:
        pat += rf"(?=\n\*\*{re.escape(next_header)}\*\*)"
    else:
        pat += r"\Z"
    m = re.search(pat, desc, re.DOTALL)
    return m.group(1).strip() if m else ""


def _bullets(text: str) -> list[str]:
    return [b.strip() for b in _BULLET_RE.findall(text)]


def _narrative(desc: str) -> str:
    """Paragraph between '**Use case:** ...' and '**Key KPIs**'."""
    m = re.search(
        r"\*\*Use case:\*\*[^\n]*\n\n(.*?)(?=\n\*\*Key KPIs\*\*)",
        desc,
        re.DOTALL,
    )
    return m.group(1).strip() if m else ""


# Verb cues that indicate "persona X does Y" inside a narrative segment.
_VERB_CUES = re.compile(
    r"\b(uses?|tracks?|monitors?|owns?|drives?|runs?|balances?|coordinates?"
    r"|plans?|reviews?|manages?|optimizes?|operates?|leads?|oversees?"
    r"|forecasts?|allocates?|prioritizes?|rehearses?)\b",
    re.IGNORECASE,
)


def _personas(narrative: str) -> list[tuple[str, str]]:
    """Parse persona-segments out of the spec narrative.

    Drops the opening overview sentence, then splits the rest on '; ' which
    is the consistent spec-author separator between persona segments.
    """
    # Drop the company-overview lead sentence (everything up to first '. ').
    parts = re.split(r"(?<=[a-z])\.\s+", narrative, maxsplit=1)
    body = parts[1] if len(parts) > 1 else narrative

    out: list[tuple[str, str]] = []
    # Split on '; ' AND on sentence boundaries — some narratives put
    # secondary personas in a follow-up sentence rather than a semicolon clause.
    for seg in re.split(r";\s*|(?<=[a-z])\.\s+(?=[A-Z])", body):
        seg = seg.strip().rstrip(".;,")
        if not seg:
            continue
        m = _VERB_CUES.search(seg)
        if not m:
            continue
        persona = seg[: m.start()].strip()
        persona = re.sub(r"^(?:and|the)\s+", "", persona, flags=re.IGNORECASE).strip()
        persona = persona.rstrip(",;.")
        rest = seg[m.end():].strip()
        # Strip "this space to / for", "it to / for", "this space in / for"
        rest = re.sub(
            r"^(?:this\s+space|it)\s+(?:day-to-day\s+)?(?:to|for|in)\s+",
            "",
            rest,
            flags=re.IGNORECASE,
        )
        rest = rest.strip().rstrip(",;.")
        if persona and rest:
            out.append((persona, rest))

    # De-dupe while preserving order.
    seen: set[str] = set()
    dedup: list[tuple[str, str]] = []
    for p, j in out:
        key = p.lower()
        if key in seen:
            continue
        seen.add(key)
        dedup.append((p, j))
    return dedup


def _acronyms_in(*texts: str) -> dict[str, str]:
    found: dict[str, str] = {}
    seen: set[str] = set()
    for t in texts:
        for m in _ACRONYM_RE.finditer(t or ""):
            tok = m.group(1)
            if tok in seen:
                continue
            seen.add(tok)
            if tok in ACRONYMS:
                found[tok] = ACRONYMS[tok]
    return dict(sorted(found.items()))


def parse_spec(spec: dict) -> ParsedSpec:
    desc = spec.get("space_description", "")
    kpi_text = _section_text(desc, "Key KPIs", "Data sources")
    src_text = _section_text(desc, "Data sources", None)
    narrative = _narrative(desc)
    personas = _personas(narrative)
    bench_questions = [b["question"] for b in spec.get("benchmarks", []) if "question" in b]
    sample_qs = spec.get("sample_questions", [])
    acros = _acronyms_in(desc, " ".join(sample_qs), narrative)
    return ParsedSpec(
        company=spec["company_name"],
        industry=spec["industry"],
        use_case=spec["use_case"],
        title=spec["space_title"],
        schema=spec["schema_basename"],
        narrative=narrative,
        kpis=_bullets(kpi_text),
        sources=_bullets(src_text),
        personas=personas,
        sample_questions=sample_qs,
        benchmarks=bench_questions,
        tables=spec.get("tables", []),
        metric_views=spec.get("metric_views", []),
        acronyms=acros,
    )


# ---------------------------------------------------------------------------
# Question typing for talk-track variation
# ---------------------------------------------------------------------------
def _question_type(q: str) -> str:
    ql = q.lower()
    if re.search(r"\btop\s+\d", ql) or re.search(
        r"which\s+[\w\s/&\-]+?\s+(?:have\s+the\s+(?:highest|most|lowest|worst|best|fewest)|are\s+driving|are\s+the\s+(?:highest|most|lowest|worst|best))",
        ql,
    ):
        return "ranking"
    if re.search(r"\b(rank|ranking|biggest|largest|smallest|leading|lagging)\b", ql):
        return "ranking"
    if any(k in ql for k in ("trend", "month over month", "monthly", "over time", "trailing")):
        return "trend"
    if any(k in ql for k in ("compare", " vs ", "versus", "year to date", "ytd")):
        return "comparison"
    if any(k in ql for k in ("below", "above", "less than", "greater than", "right now", "currently")):
        return "threshold"
    return "aggregate"


_LOSS_WORDS = (
    "deferred", "downtime", "defect", "scrap", "loss", "excursion", "recall",
    "shortage", "waste", "leak", "fail", "missed", "outage", "shut-in",
    "unscheduled", "off-spec", "spoilage", "rework", "shrinkage",
)


def _is_loss_question(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in _LOSS_WORDS)


_TALK_TRACK_BY_TYPE = {
    "ranking": (
        "This is the prioritization view — rank order tells the team where to spend the next hour, the next shift, the next AFE.",
        "A ranked table, top down. Click *Show generated code* — they should see governed columns from the metric views, not free-form math.",
        "That list used to take a half-day to assemble across systems. Now it's a question they can ask at the start of every standup.",
    ),
    "trend": (
        "Trends are where you separate signal from noise — one bad week looks like a problem, three bad months is the problem.",
        "A monthly line or bar — `DATE_TRUNC('month', ...)` shape. Easy to screenshot into the board deck.",
        "This is the kind of chart that used to live in a quarterly slide. Now it's live and current the moment something shifts.",
    ),
    "comparison": (
        "Comparison is the move that turns a number into a decision. *Worse than last quarter* means something. *In line* means something else.",
        "Two periods side-by-side, or a grouped breakdown. The deltas are what the room will read first.",
        "That side-by-side is the answer to *'is this actually worse, or are we noticing it more?'* — a question your team probably asks every week.",
    ),
    "threshold": (
        "Thresholds are the team's own working rules — anything below X gets reviewed. Watch how the model encodes that directly into the answer.",
        "A short watchlist. This is the morning triage view in one click.",
        "First 30 minutes of someone's day, returned in 8 seconds. And nobody had to build a dashboard for it.",
    ),
    "aggregate": (
        "Simple aggregate, but useful — this is the number people are usually quoting from memory in the standup.",
        "Single value or short table — the kind of number that anchors the rest of the meeting.",
        "When everyone is working from the same governed number, half the debate goes away.",
    ),
}


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------
def _kpi_short(k: str) -> str:
    """Strip parentheticals and split at the first em-dash/hyphen/colon so the
    inline KPIs list reads as short labels, not full bullet text."""
    s = re.sub(r"\s*\([^)]*\)", "", k)
    s = re.split(r"\s+[—:]\s+|\s+-\s+", s, maxsplit=1)[0]
    return s.strip()


def _at_a_glance(p: ParsedSpec) -> list[str]:
    kpi_inline = ", ".join(_kpi_short(k) for k in p.kpis[:6])
    return [
        f"# {p.company} — Demo Script",
        "",
        f"**Space:** {p.industry} — {p.title}",
        "**Runtime:** ~15 minutes • 7 questions",
        "**Audience:** Operations leadership + the practitioners on their team",
        f"**KPIs touched:** {kpi_inline}",
        "",
        "---",
        "",
    ]


def _checklist(p: ParsedSpec) -> list[str]:
    return [
        "## Pre-demo checklist",
        "",
        f"- Open the Genie space `{p.title}`.",
        "- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.",
        "- Click the SQL panel once and close it, so you know where it is when someone asks \"is it making this up?\"",
        "- Have one customer-specific opener ready: *\"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question.\"*",
        "",
        "---",
        "",
    ]


def _scenario(p: ParsedSpec) -> list[str]:
    return [
        "## Scenario framing (60 seconds, verbal)",
        "",
        f"> {p.narrative}",
        "",
        "> Today that data lives across multiple systems — operational historians, the ERP, the financial system, a stack of spreadsheets. Every morning, somebody spends the first hour stitching it together. We put one governed space on top of it. Let me show you what their day looks like with it.",
        "",
        "---",
        "",
    ]


def _kpi_card(p: ParsedSpec) -> list[str]:
    lines = ["## Key KPIs in scope", ""]
    for k in p.kpis:
        lines.append(f"- {k}")
    lines += ["", "---", ""]
    return lines


def _acronym_glossary(p: ParsedSpec) -> list[str]:
    if not p.acronyms:
        return []
    lines = [
        "## Acronyms & domain terms",
        "",
        "*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*",
        "",
        "| Term | Meaning |",
        "| --- | --- |",
    ]
    for term, mean in p.acronyms.items():
        lines.append(f"| **{term}** | {mean} |")
    lines += ["", "---", ""]
    return lines


def _distribute_questions(qs: list[str]) -> list[list[str]]:
    """Split into 3 acts (2 / 3 / 2). Falls back gracefully on <7 questions."""
    qs = list(qs)[:7]
    while len(qs) < 7:
        qs.append(qs[-1] if qs else "Show overall performance by category.")
    return [qs[:2], qs[2:5], qs[5:7]]


def _act(act_no: int, title: str, persona: str, jtbd: str, questions: list[str], anchor: bool = False) -> list[str]:
    lines = [
        f"## Act {act_no} — {title} *(≈4 min)*",
        "",
        f"**Persona:** {persona} • **Job to be done:** {jtbd}",
        "",
    ]
    # Pick the first loss/deferred-type question for the anchor moment, if any.
    anchor_idx = next((i for i, q in enumerate(questions) if _is_loss_question(q)), -1) if anchor else -1

    for i, q in enumerate(questions, start=1):
        qtype = _question_type(q)
        say, look, land = _TALK_TRACK_BY_TYPE[qtype]
        sub = f"### Question (Act {act_no}.{i}) — {qtype}"
        lines += [
            sub,
            "",
            f"> **{q}**",
            "",
            f"**What to say while it runs:** {say}",
            "",
            f"**What to look for:** {look}",
            "",
            f"**Land the point:** {land}",
            "",
        ]
        if anchor and (i - 1) == anchor_idx:
            lines += [
                "> **Anchor moment** — do the math out loud. Pick the worst row on screen, multiply by the unit value (price per barrel, dollar per defective unit, hours × loaded labor rate — whatever fits) and the period count. *\"That's roughly $X of recoverable value on one [pad / line / route / circuit] in this window. Multiply across the portfolio and this conversation pays for the platform several times over.\"* This is the moment that converts the room.",
                "",
            ]
    lines += ["---", ""]
    return lines


def _three_acts(p: ParsedSpec) -> list[str]:
    parts = _distribute_questions(p.sample_questions)

    # pick personas (fall back to generic if narrative didn't parse 3)
    personas = list(p.personas)
    while len(personas) < 3:
        defaults = [
            ("Frontline practitioner", "triage today's issues against working thresholds"),
            ("Operations manager", "rank and prioritize across sites or lines"),
            ("Executive sponsor", "drive the monthly business review and shape the next investment cycle"),
        ]
        personas.append(defaults[len(personas)])

    titles = [
        "Daily triage",
        "Site / line ranking and prioritization",
        "Monthly business review",
    ]
    out: list[str] = []
    for i, (qs, (persona, jtbd), title) in enumerate(zip(parts, personas[:3], titles), start=1):
        out += _act(i, title, persona, jtbd, qs, anchor=(i == 2))
    return out


def _close(p: ParsedSpec) -> list[str]:
    return [
        "## Strategic close (~60 seconds)",
        "",
        "Three things to lock in before you stop sharing your screen:",
        "",
        "1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.",
        "2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.",
        "3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.",
        "",
        "**Soft CTA:**",
        "",
        f"> \"This is one space — {p.company} — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next.\"",
        "",
        "---",
        "",
    ]


def _faq() -> list[str]:
    return [
        "## Anticipated questions",
        "",
        "**\"How do we know it isn't making the SQL up?\"**",
        "Every answer ships with the generated SQL one click away. It runs against your governed tables in Unity Catalog. If it's wrong, it's auditable wrong — and you can correct the metric definition once and have every future answer benefit. Genie can only return what the SQL returns.",
        "",
        "**\"What about row-level and column-level security?\"**",
        "Unity Catalog's row filters and column masks apply automatically. If a regional manager only sees their region today, that's exactly what Genie answers about — same governance you already have.",
        "",
        "**\"Can we add our own KPIs?\"**",
        "Yes. The KPI definitions live in metric views as YAML. Version-controlled, peer-reviewed, authored once. New KPI = a pull request, not a new dashboard.",
        "",
        "**\"How fresh is the data?\"**",
        "Whatever your ingestion cadence is. Genie always queries current state — there's no separate semantic cache to refresh.",
        "",
        "**\"Who else uses this pattern?\"**",
        "Happy to share specific references after the call. The triage + ranking + monthly review shape is the standard analytics arc across this industry.",
        "",
        "---",
        "",
    ]


def _quick_card(p: ParsedSpec) -> list[str]:
    lines = [
        "## Quick-reference card (read off-screen)",
        "",
    ]
    for i, q in enumerate(p.sample_questions[:7], start=1):
        lines.append(f"{i}. {q}")
    lines += [
        "",
        "**Three \"land the point\" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).",
        "",
    ]
    return lines


def render_demo(spec: dict) -> str:
    p = parse_spec(spec)
    parts: list[str] = []
    parts += _at_a_glance(p)
    parts += _checklist(p)
    parts += _scenario(p)
    parts += _kpi_card(p)
    parts += _acronym_glossary(p)
    parts += _three_acts(p)
    parts += _close(p)
    parts += _faq()
    parts += _quick_card(p)
    return "\n".join(parts).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def generate_all(specs_root: str = SPECS_ROOT, demos_root: str = DEMOS_ROOT) -> tuple[list[str], list[str]]:
    """Generate a demo script for every spec.

    Returns (written, skipped). Hand-crafted reference scripts in HAND_CRAFTED
    are skipped so a regeneration run doesn't blow away curated content.
    """
    written: list[str] = []
    skipped: list[str] = []
    for sub in sorted(os.listdir(specs_root)):
        sub_dir = os.path.join(specs_root, sub)
        if not os.path.isdir(sub_dir):
            continue
        out_dir = os.path.join(demos_root, sub)
        os.makedirs(out_dir, exist_ok=True)
        for fname in sorted(os.listdir(sub_dir)):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(sub_dir, fname)) as f:
                spec = json.load(f)
            out_name = fname.replace(".json", ".md")
            rel_path = f"{sub}/{out_name}"
            out_path = os.path.join(out_dir, out_name)
            if rel_path in HAND_CRAFTED and os.path.exists(out_path):
                skipped.append(out_path)
                continue
            md = render_demo(spec)
            with open(out_path, "w") as f:
                f.write(md)
            written.append(out_path)
    return written, skipped


def main() -> None:
    written, skipped = generate_all()
    print(f"Wrote {len(written)} demo scripts.")
    for w in written[:5]:
        print(" -", w)
    if len(written) > 5:
        print(f"   ... and {len(written) - 5} more")
    if skipped:
        print(f"Skipped {len(skipped)} hand-crafted reference script(s):")
        for s in skipped:
            print(" -", s)


if __name__ == "__main__":
    main()
