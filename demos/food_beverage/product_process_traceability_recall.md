# TraceFood Systems — Demo Script

**Space:** Food & Beverage — TraceFood Systems - Product Traceability & Recall 📋
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Food Safety + Supply Chain VP, Plant Manager, Food Safety Lead
**KPIs touched:** Recall readiness hours, Trace success rate, Average trace time, FDA compliance, Fail-simulation count, Temperature compliance pass rate
**Big decision automated:** Whether to escalate to an FDA Class I recall and how tightly to scope it — which lots, which SKUs, which regions — plus which co-manufacturer/supplier gets dropped from the approved list this quarter.

---

## Pre-demo checklist

- Open the Genie space `TraceFood Systems - Product Traceability & Recall 📋`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> TraceFood Systems runs 20 SKUs across the cold and ambient chain with 5 active ingredient suppliers and FSMA 204 critical-tracking-event requirements in force. Today the lot-trace record lives in a Plant Manager's MES export, the supplier scorecard is a Quality team Excel, and the recall-readiness drill result is a Food Safety PowerPoint rebuilt before every SQF surveillance audit. Three artifacts, one chain of custody — and when a complaint comes in from a retailer at 4 PM, the recall-scoping call gets made on whichever spreadsheet someone can find first. This space ends that. One governed surface that collapses the SCADA temp log, the lot genealogy, and the supplier scorecard into the *escalate-or-contain, which lots, which regions* call before the press release writes itself.

---

## Key KPIs in scope

- Recall readiness hours — GFSI benchmark <4 hrs for full one-up/one-down trace
- Trace success rate (%) — % of mock-recall lots fully reconciled; target 100%
- Average trace time (hours) — speed-to-trace for live or simulated events
- FDA compliance (%) — alignment with FSMA 204 critical tracking events
- Fail-simulation count — failed mock recalls in the period
- Temperature compliance pass rate — cold-chain integrity at custody transfer
- Custody transfers per lot — handling complexity / risk indicator
- Lots traced — volume processed through the traceability platform

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **FDA** | Food and Drug Administration |
| **FSMA** | Food Safety Modernization Act |
| **GFSI** | Global Food Safety Initiative |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the traceability gaps before the FDA letter arrives *(≈4 min)*

**Persona:** Food Safety Lead • **Job to be done:** Surface the lots and categories where the chain of custody is weak — before they become the lot in question.

*This is the first 30 minutes of a real recall scenario. Two questions in, the Food Safety Lead has the gap-exposure list that used to take a half-day of paper-record reconciliation.*

### Question (Act 1.1)

> **Show the monthly trend in traceability gaps across all product categories for the last 12 months.**

**What to say while it runs:** Monthly traceability gaps across all categories. Each `gap_count` here is a record where we cannot answer the FSMA 204 one-up-one-down question — that's the FDA-exposure number. The trend matters more than the absolute count; a flat line is process discipline, a rising line is a systemic break.

**What to look for:** Monthly bars of `gap_count` by category. Look for the category where the gap line bent up — that's the supplier or co-manufacturer onboarding gone wrong.

**Land the point:** That number used to surface only when a regulator asked. Now Food Safety sees it before the inspector does — and the corrective-action conversation starts on the right week, not the week of the audit.

### Question (Act 1.2)

> **Top 10 product categories by fail-simulation count this year — what is the average trace time for each?**

**What to say while it runs:** Top categories by fail-simulation count this year with average trace time alongside. GFSI benchmark for full-trace is under 4 hours. Any category averaging above 4 hours is a category where, in a real recall, we'd miss the window — and the press cycle would write the story for us.

**What to look for:** Ranked top-10 on `fail_sim_count` with `avg_trace_time` beside it. Categories where both numbers are high are the mock-recall failures that would become real-recall failures.

**Land the point:** Now Food Safety can walk into the VP's office with the specific categories and a specific number — *we are 6.2 hours, the benchmark is 4* — instead of a heat-map and a hope. That changes the supplier-audit calendar from quarterly to monthly on those SKUs.

---

## Act 2 — The decision — scoping the recall and dropping the supplier *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Decide which lots get contained, which SKUs get pulled from retail, and which co-manufacturer comes off the approved list this quarter.

*Three questions that turn the gap inventory into a defensible recall-scoping decision. The middle question is the anchor — the lots-affected to recall-cost conversion that decides whether this is a contained product withdrawal or a Class I event.*

### Question (Act 2.1)

> **Which suppliers contribute the most traceability gaps, and how many lots are affected?**

**What to say while it runs:** Top suppliers by traceability gap volume with the lots affected. The supplier with the most gaps is rarely the supplier sending the most volume — that's the disconnect. A supplier with 5% of volume and 40% of the gaps is the supplier we need to drop, regardless of price.

**What to look for:** Aggregate from `products` table on `supplier_id` and `traceability_status='Gap'` with units_in_lot and lot counts. Watch for the supplier with disproportionate gap share.

**Land the point:** That's the supplier-consolidation conversation, ready for Procurement on Monday. The Quality scorecard finally has the same number as the spend report — and the approved-supplier list gets cut on evidence, not on relationship.

### Question (Act 2.2)

> **How has average recall readiness hours trended month-over-month — are we below the 4-hour GFSI benchmark?**

**What to say while it runs:** Average recall readiness hours month-over-month, with the 4-hour GFSI line. This is the one slide that gets shown at every SQF surveillance audit. If our trailing 6-month average is above 4 hours, we are not audit-ready — and the FDA Reportable Food Registry is one consumer complaint away.

**What to look for:** Monthly trend on `avg_trace_time` (or `recall_readiness_hours` from `lot_tracking_events`) with the 4-hour reference. The room should see whether the line is descending toward the benchmark or drifting above it.

**Land the point:** That curve is now the same artifact Food Safety, Plant Operations, and the VP all look at. The audit-readiness conversation stops being a slide cobbled together the night before and starts being a continuous KPI — and the VP signs off the SQF inspection on hard evidence.

> **Anchor moment.** Stop on the average-recall-readiness chart and the failed-temp count beside it. Pick the worst case — say one category running at 6 hours trace time with a temperature break on Line K affecting roughly 25,000 units across 5 lots.

> *At an industry blended $8 per recalled unit for parts, labor, logistics, and customer credits, 25,000 units is $200K of direct recall cost — manageable. But if it becomes a Class I event with plant shutdown for FDA inspection, lost production is $1M+ per day, and the brand-impact estimate on a major event runs $10-50M. The expected value of *getting the scoping right* — narrowing from 5 lots to 2, catching it inside 4 hours instead of 16 — is $5-20M per major event avoided.*

> That's the decision this space automates. Not the post-mortem. The scoping call. Containment radius, retailer notification language, FDA Reportable Food Registry threshold — all decided in the first hour, on the same data the regulator will see.

### Question (Act 2.3)

> **Top 10 product categories by total lots traced — show trace success rate and FDA compliance side by side.**

**What to say while it runs:** Production lines with the highest count of failed temperature compliance in the last 90 days. Cold-chain breaks are the recall trigger that doesn't make it to the morning briefing because the SCADA log lives in OT and the trace report lives in QA. Now they live in the same query.

**What to look for:** Ranked lines by `temp_compliant='No'` event count from `lot_tracking_events`. One line carrying the bulk of the cold-chain breaks is the line that gets the HACCP review.

**Land the point:** That's the HACCP-review call — which line gets pulled for a CCP redefinition next week. The Plant Manager makes the call on the same evidence the FDA inspector would use, and the corrective action goes into the file before the complaint arrives.

---

## Act 3 — The commitment — shaping the supplier scorecard and the next audit narrative *(≈4 min)*

**Persona:** VP of Food Safety (with Supply Chain VP) • **Job to be done:** Defend the recall-readiness program to the executive team and lock the supplier list, the audit calendar, and the FSMA 204 compliance commitment.

*The VP doesn't need another mock-recall PowerPoint; they need the same trace-success and FDA-compliance numbers their team is acting on, in the same language, so the FDA inspection prep and the supplier-consolidation case are built off one source.*

### Question (Act 3.1)

> **Which production lines have the highest count of failed temperature compliance events in the last 90 days?**

**What to say while it runs:** Top categories by total lots traced with trace success rate and FDA compliance side by side. This is the category-prioritization view for the FSMA 204 traceability list — high-volume categories with weaker compliance are where the audit and the recall risk concentrate.

**What to look for:** Ranked categories by `total_lots_traced` with `avg_trace_success` and `avg_fda_compliance`. The categories above 95% on both are the categories where we lead with strength; the categories below 90% are the ones we cap in volume until the score recovers.

**Land the point:** That ranking is the actual FSMA 204 priority list. The VP walks into the FDA inspection with the same artifact the plant team has been running for 12 months — not a stack of binders rebuilt for the audit.

### Question (Act 3.2)

> **What share of lots achieved Full traceability vs. Partial or Gap, by product category, this quarter?**

**What to say while it runs:** Share of lots achieving Full traceability vs. Partial or Gap by category for the quarter. This is the headline number for the board's risk committee — and the leading indicator that catches a structural break before the recall.

**What to look for:** Stacked share of `traceability_status` across categories for the trailing quarter. Categories where Full Trace is below 90% are the categories that get an executive-level CAPA in the next 30 days.

**Land the point:** The board's risk committee now sees the same number the Plant Manager sees on Tuesday morning. That's the difference between governance theater and actual risk reduction — and it's the conversation that determines whether FSMA 204 is a compliance cost or a competitive moat.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — TraceFood Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in traceability gaps across all product categories for the last 12 months.
2. Top 10 product categories by fail-simulation count this year — what is the average trace time for each?
3. Which suppliers contribute the most traceability gaps, and how many lots are affected?
4. How has average recall readiness hours trended month-over-month — are we below the 4-hour GFSI benchmark?
5. Top 10 product categories by total lots traced — show trace success rate and FDA compliance side by side.
6. Which production lines have the highest count of failed temperature compliance events in the last 90 days?
7. What share of lots achieved Full traceability vs. Partial or Gap, by product category, this quarter?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
