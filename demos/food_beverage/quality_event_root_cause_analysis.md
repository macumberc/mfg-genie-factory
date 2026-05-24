# FreshGuard Foods — Demo Script

**Space:** Food & Beverage — FreshGuard Foods - Quality Event Root Cause Analysis 🔍
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Food Safety + CFO, Plant Manager, Quality VP
**KPIs touched:** Critical event count, Total cost impact, Units affected per event, CAPA closure rate, Regulatory audit score, Non-conformance count
**Big decision automated:** Which production line gets shut for a HACCP review this week, which CCP gets redefined, and which root-cause category absorbs the next COPQ-reduction capex.

---

## Pre-demo checklist

- Open the Genie space `FreshGuard Foods - Quality Event Root Cause Analysis 🔍`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FreshGuard Foods runs 12 production lines and 20 SKUs across bakery, dairy, deli, produce, protein, seafood, beverage, and frozen — heading into the next FSSC 22000 and SQF surveillance cycle. Today the critical-event log lives in the MES, the CAPA tracker is a Quality team SharePoint Excel, and the cost-of-poor-quality rollup is rebuilt by Finance from the scrap and rework GL accounts. Three artifacts, one production floor — and when a critical NC fires at 2 AM, the shut-or-run call gets made on whichever spreadsheet the on-call Plant Manager can pull up on their phone. This space ends that. One governed surface that converts the daily QA event stream into the *which line shuts, which CCP gets redefined, which capex moves* decision before the next SQF auditor walks the floor.

---

## Key KPIs in scope

- Critical event count — zero-tolerance threshold; any critical NC can fail an SQF audit
- Total cost impact ($) — COPQ rolled up by line, category, and root cause
- Units affected per event — scale of containment / recall exposure
- CAPA closure rate (%) — closed / (open + closed); target 90%+ on-time
- Regulatory audit score — surveillance audit health vs. 85+ benchmark
- Non-conformance count — monthly trend across compliance status
- Pass rate on temperature compliance — cold-chain control indicator
- Overall quality score — blended lot-release health 0–100

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **KPI** | Key Performance Indicator |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the critical events and the COPQ centers of gravity *(≈4 min)*

**Persona:** Quality VP • **Job to be done:** Locate the lines and categories driving critical events and cost-of-poor-quality before the audit narrative gets written for us.

*This is the first stop on a real food-safety review. Two questions in, the Quality VP has the Pareto and the dollar exposure that used to take a week of MES + Finance pulls.*

### Question (Act 1.1)

> **Show the monthly trend in critical events across all product categories for the trailing 12 months.**

**What to say while it runs:** Monthly critical events across all categories. Critical is the zero-tolerance bucket — any one critical NC can fail an SQF audit. This chart is the leading indicator of whether the surveillance audit goes smoothly or the corrective-action package writes itself in real time.

**What to look for:** Monthly trend on `critical_events` measure from `quality_kpi_monthly`. Watch for the category that bent up two months ago — that's the systemic issue building toward the audit.

**Land the point:** Critical-event trending used to surface in the monthly quality review — three weeks late. Now the Quality VP sees the inflection point as it happens, and the corrective action lands inside the same month the event fires.

### Question (Act 1.2)

> **Top 10 product categories by total cost impact this year — which root causes are driving the loss?**

**What to say while it runs:** Top 10 categories by total cost impact YTD with the root-cause mix beside it. Cost impact is the COPQ language Finance cares about — scrap, rework, customer credit, line downtime, all rolled in. The root-cause column tells you whether the dollars are concentrated in Equipment, Process, Ingredient, or Contamination — and that determines whether the fix is capex, training, supplier, or sanitation.

**What to look for:** Ranked top-10 on `total_cost_impact` with `root_cause` distribution. Look for the category where one root cause dominates — that's the surgical fix; categories with a spread are the structural problem.

**Land the point:** Now the Quality VP and the CFO are reading the same COPQ number with the same root-cause attribution. The annual quality-improvement budget stops being argued on slide bullets and starts being argued on dollars by root cause.

---

## Act 2 — The decision — which line shuts and which CCP gets rewritten *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Decide which line gets pulled for a HACCP re-evaluation this week, which CCP gets redefined, and which CAPA jumps the queue.

*Three questions that turn the COPQ rollup into a specific shut-the-line, rewrite-the-CCP commitment. The middle question is the anchor — the units-affected to recall-exposure conversion that decides whether a Major event becomes a Critical one.*

### Question (Act 2.1)

> **Which production lines have the lowest average audit score, and how many non-conformances did they generate last quarter?**

**What to say while it runs:** Production lines with the lowest average audit score and their non-conformance count last quarter. The 85+ benchmark is the SQF surveillance floor — any line averaging below that is a line where the next inspection is going to surface something. The NC count tells you whether it's one fluky event or a structural process problem.

**What to look for:** Lines ranked by `avg_audit_score` ascending with `nc_count` beside. A line below 85 with double-digit NCs is the shut-and-review candidate; a line below 85 with two NCs is the line where one CCP needs a rewrite.

**Land the point:** That table is the actual shut-the-line decision. The Plant Manager makes the call on the same numbers the SQF auditor will see in 30 days — and the HACCP plan gets the surgical update instead of a wholesale rewrite the night before the audit.

### Question (Act 2.2)

> **How has total cost impact trended month-over-month across the network?**

**What to say while it runs:** Cost impact trended month-over-month across the network. This is the chart the CFO opens at month-end. A flat line is COPQ under control; a rising line is dollars escaping the floor that nobody is catching in the monthly review.

**What to look for:** Monthly trend on `total_cost_impact`. Look for the inflection — and whether it matches a known root cause or shows up unexplained.

**Land the point:** When the CFO's COPQ chart and the Plant Manager's daily quality view are the same artifact, the gap between *we have a quality issue* and *we have a $400K quality issue* closes. That's the difference between an ops debate and a budget decision.

> **Anchor moment.** Stop on the cost-impact trend and the root-cause Pareto on screen. Pick the worst category — say protein with 8 critical events this quarter, 35,000 units affected, contamination as the lead root cause.

> *At a blended $3 per defective unit for scrap, rework, and customer credit, 35,000 units is $105K of direct COPQ this quarter — $420K annualized on one category. But the recall-cost exposure if any of those events had escaped the plant is $8-12 per recalled unit plus the brand impact — $300-500K of direct exposure per *prevented* recall. And one Class I FDA event with plant shutdown is $1M+ per day of lost production on top. Catching contamination upstream of a Critical NC, even once, is the multi-million-dollar avoidance case.*

> That's the decision this space automates. Not the post-incident report. The intervention. Line K shuts on Tuesday for a CCP rewrite, the sanitation capex moves to the head of the queue, and the surveillance audit becomes a forward-looking conversation instead of a damage assessment.

### Question (Act 2.3)

> **Which root causes account for the highest share of critical events in the last 90 days?**

**What to say while it runs:** Root causes by share of critical events in the last 90 days. This is the Pareto that determines next quarter's quality-improvement spend. If Contamination is 40% of critical events, the capex goes to sanitation upgrades; if Equipment is the headline, it's PM-cycle and refurbish capex; if Ingredient is the headline, it's a supplier-qualification fight.

**What to look for:** Aggregate on `root_cause` with `severity='Critical'`. The top 2-3 root causes are where 80% of the audit risk and 80% of the COPQ live.

**Land the point:** That ranking *is* the quality-capex prioritization. Sanitation refurb vs. equipment upgrade vs. supplier-change vs. operator training — the dollars get assigned by root-cause share, not by whoever made the most compelling slide.

---

## Act 3 — The commitment — shaping the CAPA portfolio and the audit narrative *(≈4 min)*

**Persona:** VP of Food Safety (with CFO) • **Job to be done:** Defend the food-safety program to the executive team and lock the next-cycle CAPA portfolio, audit-readiness commitment, and COPQ target.

*The VP doesn't need another quality slide; they need the same critical-event and audit-score numbers the plant is acting on, in the same language, so the COPQ target and the audit story for the board both write themselves.*

### Question (Act 3.1)

> **Top 10 product categories by units affected — show severity mix and total cost impact.**

**What to say while it runs:** Top categories by units affected with the severity mix and total cost impact. This is the recall-exposure view — the categories where one more critical event tips us into a recall conversation are the categories that get executive-attention CAPAs.

**What to look for:** Ranked top-10 on `total_units_affected` with `severity` distribution and `total_cost_impact`. Categories with high units affected and a Critical-heavy severity mix are the *one event away from a recall* list.

**Land the point:** That list is the executive food-safety dashboard. Not a stoplight graphic — the actual categories, the actual dollars, the actual severity mix. The VP's report to the board has the same precision the plant team has on Tuesday.

### Question (Act 3.2)

> **What is the monthly trend in CAPA open vs. closed, and which production lines have the lowest closure rate?**

**What to say while it runs:** Monthly CAPA open vs. closed by production line with the closure rate. Target is 90% on-time. Any line below 80% on closure rate is a line where the audit narrative writes itself badly — open CAPAs are findings waiting to be documented.

**What to look for:** Monthly trend of `total_capa_open` vs. `total_capa_closed` with closure rate calculated. Lines below 80% closure are the executive-attention queue.

**Land the point:** Now the CAPA discipline lives in the same surface as the COPQ dollars and the audit score. The Quality VP, the Plant Managers, and the CFO are all reading the same chart — and the next surveillance audit becomes an evidence walk-through, not an evidence hunt.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FreshGuard Foods — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in critical events across all product categories for the trailing 12 months.
2. Top 10 product categories by total cost impact this year — which root causes are driving the loss?
3. Which production lines have the lowest average audit score, and how many non-conformances did they generate last quarter?
4. How has total cost impact trended month-over-month across the network?
5. Which root causes account for the highest share of critical events in the last 90 days?
6. Top 10 product categories by units affected — show severity mix and total cost impact.
7. What is the monthly trend in CAPA open vs. closed, and which production lines have the lowest closure rate?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
