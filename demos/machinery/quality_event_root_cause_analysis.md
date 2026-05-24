# QualityFirst Manufacturing — Demo Script

**Space:** Machinery — QualityFirst Manufacturing - Quality RCA 🔍
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Quality + Quality Engineer, CAPA Owner, CFO partner
**KPIs touched:** Defect PPM, Cost of Poor Quality, First-pass yield, CAPA closure rate, Open critical quality events, Customer complaints
**Big decision automated:** Which 1-2 suppliers to put on a qualification hold, which work cells to pull off-line for re-certification, and whether to escalate the open Critical lot to containment or release.

---

## Pre-demo checklist

- Open the Genie space `QualityFirst Manufacturing - Quality RCA 🔍`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> QualityFirst Manufacturing tracks defects and CAPA across multiple product lines and categories. Today the defect data lives in three places: the Quality Engineer's daily nonconformance log in the QMS, the CAPA Owner's open-action spreadsheet, and the VP Quality's monthly Cost-of-Poor-Quality slide built by finance. When a Critical event lands, nobody can answer the question that actually matters — *is this supplier, this work cell, or this lot drift?* — without an afternoon of cross-referencing. So the lot gets released, or contained, on intuition. This space replaces that with one governed surface where defect PPM, root cause, CAPA aging, and customer-complaint volume all reconcile against the same monthly KPI table — and the supplier-qualification call becomes a 10-minute conversation, not a two-week investigation.

---

## Key KPIs in scope

- Defect PPM (parts per million) — Six Sigma target 3.4 PPM, world-class <100 PPM
- Cost of Poor Quality ($) — typical 5–10% of revenue, leaders <2%
- First-pass yield (%) — world-class ≥99%
- CAPA closure rate (%) — target ≥90% within SLA
- Open critical quality events — escalation indicator
- Customer complaints (count) — voice-of-customer KPI
- Audit findings (count) — regulatory and ISO 9001 health
- Units affected per event — severity and recall-risk indicator

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **KPI** | Key Performance Indicator |
| **PPM** | Parts Per Million (defect rate) |
| **SLA** | Service Level Agreement |
| **VP** | Vice President |

---

## Act 1 — The signal — is this PPM spike noise or the start of a recall? *(≈4 min)*

**Persona:** Quality Engineer • **Job to be done:** Tell the difference between random variation and a structural shift in defect PPM before the customer complaint hits.

*This is the moment the quality team decides whether the Tuesday spike is statistical noise or a containment trigger. Two questions in, the engineer has the trend and the cost ranking that used to take a half-day in the QMS.*

### Question (Act 1.1)

> **What is the monthly trend in defect PPM by product category over the trailing 12 months?**

**What to say while it runs:** Six Sigma target is 3.4 defects per million; world-class is under 100 PPM. The chart we care about isn't the absolute level — it's the inflection. A category that was running at 200 PPM for six months and is now at 800 PPM has changed *something*. That's the signal we have to catch before the customer does.

**What to look for:** Monthly `avg_defect_ppm` trend by product category over 12 months — `DATE_TRUNC('month', kpi_month)` shape from `quality_kpi_metrics`. Watch for categories where the curve has bent up in the last 2-3 months. That's the containment-vs-release conversation.

**Land the point:** Before this space, that inflection point showed up in a finance-built deck 30 days after it happened. Now the Quality Engineer flags it in real time — and the conversation about pulling a lot off the dock starts on the same day the defect data lands.

### Question (Act 1.2)

> **Top 10 root causes by total cost impact in the last quarter.**

**What to say while it runs:** Top root causes by total dollar impact, last quarter. The interesting answer isn't *what's most common* — it's *what's most expensive*. Operator error is usually most frequent; supplier defects and tooling wear are usually most costly. That's the prioritization split.

**What to look for:** Ranked table from `quality_events_metrics` with `total_cost_impact` by `root_cause`. Click *Show generated code* once to make the point — the engineer is querying a metric view, not joining tables in a notebook.

**Land the point:** That ranking is the agenda for next week's CAPA review. The room walks in already aligned on which root cause is bleeding the most dollars — and which CAPA closure absolutely cannot slip past SLA.

---

## Act 2 — The decision — supplier hold, work-cell re-cert, or release the lot *(≈4 min)*

**Persona:** CAPA Owner • **Job to be done:** Commit on which suppliers to put on qualification hold, which work cells to pull for re-cert, and whether the open Critical events warrant lot containment.

*Three questions that turn the daily defect log into a defensible quality-action recommendation. The middle question is the anchor — the units-affected-to-cost conversion that justifies the containment call.*

### Question (Act 2.1)

> **Which product lines have the most open Critical quality events right now?**

**What to say while it runs:** Open Critical quality events by product line. Severity = Critical is the field-failure / recall-risk tier — these can't sit in 'Open' status for weeks. Industry rule of thumb is closure within 30 days; anything older is escalation territory.

**What to look for:** A table from `quality_events_metrics` with `open_quality_event_count` and `critical_event_count` by `product_line`. The eye should land on product lines with multiple open Criticals — those are the candidate lots for containment.

**Land the point:** That table used to be a printout the CAPA owner manually reconciled against the QMS each Monday. Now it's the first slide of the daily quality stand-up — and the call on whether to escalate a Critical to the recall committee is grounded in one number the whole room sees.

### Question (Act 2.2)

> **Rank product categories by CAPA closure rate — which are below the 90% target?**

**What to say while it runs:** CAPA closure rate by product category, against the 90% within-SLA target. Categories below 90% don't just look bad on the scorecard — they're the categories where customer complaints will keep arriving, because the root cause is sitting unfixed.

**What to look for:** Ranked categories by `avg_capa_closure` from `quality_kpi_metrics`. Watch for categories below 75% — those are structurally broken, not just behind on paperwork.

**Land the point:** When the CAPA owner can show *exactly* which categories are dragging the closure rate, the conversation about reassigning CAPA workload or hiring another engineer becomes a budget conversation, not a hand-waving one.

> **Anchor moment.** Stop on the top-10-defect-types view and the trend in `total_copq`. Pick the worst defect type — call it 15,000 units affected this year, traced to one supplier, at an average dispositioning cost of $200 per unit.

> *15,000 units × $200 disposition cost = $3M per year on one defect mode. Cost of Poor Quality typically runs 5-10% of revenue at companies that *aren't* paying attention; leaders run under 2%. Even a 1-point reduction in supplier rejection rate on this one line is roughly $2-3M/year of recovered COPQ. Across all product lines, the supplier-rationalization conversation is a $10-20M/year addressable number — not a procurement footnote.*

> That's the decision this space automates. Not the audit prep. The decision. The supplier qualification hold gets issued with the dollars on the page, the lot containment call gets made before the customer sees the defect, and the CAPA workload gets resourced against measured backlog instead of squeaky-wheel anecdotes.

### Question (Act 2.3)

> **Show monthly trend in Cost of Poor Quality vs customer complaints.**

**What to say while it runs:** Top 10 defect types by units affected this year, with the root cause attached to each. This is the supplier-qualification view — if 'incoming material' is the root cause on three of the top 10 defect types and they all trace to the same supplier, you have a qualification-revocation case.

**What to look for:** Defect types ranked by `total_units_affected`, joined to root cause. Look for clustering — the same root cause appearing on multiple high-impact defect types is the smoking gun.

**Land the point:** That clustering is the difference between *suspecting* a supplier is the problem and *proving* it. The supplier-quality engineer walks into the next QBR with the evidence already on screen.

---

## Act 3 — The commitment — board-grade COPQ narrative and the supplier slate *(≈4 min)*

**Persona:** VP Quality • **Job to be done:** Defend the Cost-of-Poor-Quality trajectory to the executive team and commit to the supplier rationalization and certification plan for the next year.

*The VP Quality has to tell the board a coherent story about defect dollars, customer impact, and audit readiness. The supplier slate and the COPQ narrative have to land in the same conversation.*

### Question (Act 3.1)

> **Top 10 defect types by units affected this year, and which root cause is driving each?**

**What to say while it runs:** Monthly Cost of Poor Quality vs customer complaints. The dollar curve and the voice-of-customer curve usually lead each other by a quarter — when complaints spike, COPQ catches up 60-90 days later as warranty claims roll in. That offset is the early-warning system.

**What to look for:** Two trend lines from `quality_kpi_metrics`: `total_copq` and `total_customer_complaints` over 12 months, monthly granularity. Eye lands on the offset — where complaints surge before COPQ does. That's the upcoming P&L hit nobody's reserved for.

**Land the point:** When the VP Quality can show that next quarter's COPQ surprise is *already visible* in this quarter's complaint volume, the board conversation shifts from explaining variance to pre-emptively reserving for it — and the quality-leadership credibility resets in one slide.

### Question (Act 3.2)

> **Which inspection types have the highest rejection rate, and what findings volume do they generate?**

**What to say while it runs:** Inspection types ranked by rejection rate and findings volume. This is the audit-readiness view — high rejection plus high findings means the inspection process is catching defects, which is good, but it also means the upstream supplier or work cell is producing them, which is the structural problem.

**What to look for:** From `inspection_records` — rejection rate (`units_rejected / units_inspected`) by `inspection_type` with `findings_count` next to it. The combinations to watch are *high rejection AND high findings* — those are the inspection touchpoints holding the line.

**Land the point:** Same space, same numbers, same data model — the Quality Engineer's daily defect log and the VP's audit-readiness narrative are now the same artifact. The ISO surveillance audit walks in to a system that's already telling the truth, instead of a binder pulled together the week before.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — QualityFirst Manufacturing — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

---

## Anticipated questions

**"How do we know it isn't making the SQL up?"**
Every answer ships with the generated SQL one click away. It runs against your governed tables in Unity Catalog. If it's wrong, it's auditable wrong — and you can correct the metric definition once and have every future answer benefit. Genie can only return what the SQL returns.

**"What about row-level and column-level security?"**
Unity Catalog's row filters and column masks apply automatically. If a regional manager only sees their region today, that's exactly what Genie answers about — same governance you already have.

**"Can we add our own KPIs?"**
Yes. The KPI definitions live in metric views as YAML. Version-controlled, peer-reviewed, authored once. New KPI = a pull request, not a new dashboard.

**"How fresh is the data?"**
Whatever your ingestion cadence is. Genie always queries current state — there's no separate semantic cache to refresh.

**"Who else uses this pattern?"**
Happy to share specific references after the call. The triage + ranking + monthly review shape is the standard analytics arc across this industry.

---

## Quick-reference card (read off-screen)

1. What is the monthly trend in defect PPM by product category over the trailing 12 months?
2. Top 10 root causes by total cost impact in the last quarter.
3. Which product lines have the most open Critical quality events right now?
4. Rank product categories by CAPA closure rate — which are below the 90% target?
5. Show monthly trend in Cost of Poor Quality vs customer complaints.
6. Top 10 defect types by units affected this year, and which root cause is driving each?
7. Which inspection types have the highest rejection rate, and what findings volume do they generate?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
