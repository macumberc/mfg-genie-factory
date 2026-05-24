# AeroQuality Corp — Demo Script

**Space:** Aerospace — AeroQuality Corp - Quality Event Root Cause Analysis 🔍
**Runtime:** ~15 minutes • 7 questions
**Audience:** COO + Quality Engineer, VP of Quality
**KPIs touched:** Defect rate, Escape rate %, First-pass yield %, Cost of quality, Days to CAPA closure, Corrective-action closure %
**Big decision automated:** Which 2-3 process areas earn a CAPA investment and which production runs to re-inspect — before the next Airbus/Boeing supplier-scorecard review.

---

## Pre-demo checklist

- Open the Genie space `AeroQuality Corp - Quality Event Root Cause Analysis 🔍`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroQuality Corp runs AS9100-aligned quality analytics across 20 serialized components flowing through 6 manufacturing process areas — CNC machining, composite layup, heat treatment, surface treatment, assembly, and test. Today the defect-rate PPM lives in the Quality Engineer's CAPA tracker, the escape-rate-vs-customer-scorecard number lives in the VP of Quality's monthly slide, and the cost-of-quality rollup lives in the COO's operating review binder. Three artifacts, same components — and the next CAPA investment gets prioritized by whichever defect category caused the most recent customer complaint, not by total dollar exposure. This space ends that. One governed surface where defect rate, escape rate, first-pass yield, and cost-of-quality sit together, so the CAPA-allocation decision becomes a defensible engineering investment, not a reactive response to the loudest customer.

---

## Key KPIs in scope

- Defect rate (PPM) — AS9100 supplier target <500 PPM, world-class <100 PPM
- Escape rate % — customer-detected defects / total shipped (target <0.1%)
- First-pass yield % (target >95% on machined parts, >98% on assembly)
- Cost of quality (USD) — internal failure + external failure + appraisal + prevention
- Days to CAPA closure (target <30 days for major NCRs)
- Corrective-action closure % (target >90% on-time)
- Critical event count — Severity = Critical
- Inspection fail rate — fail_count / total_inspections

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **COO** | Chief Operating Officer |
| **FPY** | First Pass Yield |
| **PPM** | Parts Per Million (defect rate) |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the failure modes that are quietly bleeding margin *(≈4 min)*

**Persona:** Quality Engineer • **Job to be done:** Identify which root causes are driving cost of quality and which need an immediate CAPA before the next customer scorecard cycle.

*This is the moment the CAPA prioritization list starts forming. Two queries in, the engineer already has the root causes that earn an 8D investigation versus the noise that gets logged and closed.*

### Question (Act 1.1)

> **Top 10 root causes by total cost of quality over the last 12 months.**

**What to say while it runs:** Root causes ranked by total cost of quality over 12 months. COQ is internal failure plus external failure plus appraisal plus prevention — the four-bucket model. Anything where a single root cause carries six- or seven-figure annual cost is a CAPA investment, not a memo. The ranking IS the investment priority.

**What to look for:** A ranked table of 10 root causes by total_cost_of_quality_usd. The room should see that the top three usually carry 60-70% of the total — that's the Pareto the CAPA budget targets.

**Land the point:** Right there is the CAPA backlog reset. The engineer can name three root causes that earn full-8D investigations this quarter — and the conversation with engineering moves from 'we keep finding the same defects' to 'these three failure modes get fixed by Q-end.'

### Question (Act 1.2)

> **Show monthly trend in critical event count by component class.**

**What to say while it runs:** Now critical event count by component class over 12 months. Critical-severity events are the AS9100 escalation threshold — every one triggers customer notification under the supplier agreements with Airbus and Boeing. A rising line on any component class is a supplier-scorecard problem before it's a quality problem.

**What to look for:** Monthly critical_event_count by component_class using `DATE_TRUNC('month', ...)`. Watch for component classes where the line is climbing — those are the customer-scorecard exposures.

**Land the point:** Before this space, that chart was a monthly artifact for the customer scorecard meeting. Now it's the engineer's first question of the morning — and the conversation about which CAPA to accelerate starts weeks earlier.

---

## Act 2 — The decision — funding the CAPAs, naming the re-inspection lots, defending the supplier scorecard *(≈4 min)*

**Persona:** VP of Quality • **Job to be done:** Commit a CAPA investment plan and a re-inspection lot list — naming exactly where engineering hours and inspection capacity go this quarter.

*Three questions that turn the defect-rate watchlist into a defensible CAPA-funding recommendation. The middle question is the anchor — converting escape rate into the customer-scorecard and recall-cost math the COO will sign off on.*

### Question (Act 2.1)

> **Which component classes have the worst escape rate this quarter, and what is their cost of quality?**

**What to say while it runs:** Component classes with the worst escape rate this quarter and their cost of quality. Escape rate target is below 0.1% on AS9100; anything above 0.5% is a supplier-scorecard problem. Cost of quality alongside it tells you whether the escape is a single big-dollar event or a systemic pattern.

**What to look for:** Component classes ranked by escape_rate_pct alongside cost_of_quality_usd. The combination tells you whether to fund a single-process CAPA (one big event) or a process-area-wide redesign (systemic pattern).

**Land the point:** That ranking is the customer-scorecard defense. Two queries in, the VP of Quality has a defensible CAPA plan to walk into the supplier review — and the conversation with Airbus/Boeing moves from 'we acknowledge the escape' to 'here's the CAPA, here's the close-out date.'

### Question (Act 2.2)

> **Top 10 components by days-to-closure on quality events — flag any over 30 days.**

**What to say while it runs:** Top 10 components by days-to-closure on quality events — anything over 30 is flagged. AS9100 target on major NCRs is 30-day closure. A growing tail on time-to-closure means CAPAs aren't getting resourced; the same defects keep showing up because the root cause is still in the process.

**What to look for:** Components ranked by avg_days_to_closure with 30+ days highlighted. Watch for components where closure days are climbing — those are the structural CAPAs the team isn't getting to.

**Land the point:** That table is the CAPA-resourcing case. The first is a metric; the second is a budget conversation. The VP of Quality needs the second to defend engineering hours.

> **Anchor moment.** Park on the component-class escape-rate-with-COQ view. Pick the worst component class — say composite primary structure running at 0.6% escape rate with $4M annual cost of quality.

> *Aero supplier-scorecard targets are PPM below 500 and escape rate below 0.1%. At 0.6% escape on a high-volume composite line, AeroQuality is shipping roughly 6,000 escapes per million units. At $1-3K per defective unit in customer recall/rework cost — typical for flight-hardware containment — that's $6-18M of annual customer-borne exposure that comes back as chargebacks, score downgrades, and lost share-of-wallet on the next program award. A targeted process-area CAPA — automated inspection, layup-process monitoring, operator certification — runs $1-2M and typically drops escape rate 60-80%. Payback is one quarter; the scorecard recovery is the real prize.*

> That's the decision this space defends. The CAPA budget goes to the process areas backing the biggest scorecard exposure, not to the last customer complaint. Re-inspection capacity gets booked from defect-pattern data, not from gut. The next supplier review opens with a defensible posture.

### Question (Act 2.3)

> **How has inspection fail rate trended month-over-month by process area?**

**What to say while it runs:** Process areas driving the most critical non-conformances with their top findings. Six process areas, but typically two carry 70% of the critical events. That concentration is the CAPA-investment target.

**What to look for:** Process areas ranked by critical_event_count with top findings listed. Watch for areas where one or two findings dominate — those are single-CAPA wins.

**Land the point:** That comparison is the difference between knowing process drift exists and knowing exactly which process step to fund. The first is monthly-review filler; the second is the engineering capex case.

---

## Act 3 — The commitment — defending cost of quality to the COO and locking next year's quality capex *(≈4 min)*

**Persona:** COO • **Job to be done:** Defend the cost-of-quality trajectory against the operating plan and lock in next year's quality capex — automated inspection, CAPA engineering hours, supplier-quality investment.

*The COO doesn't need a new report — they need the same defect-rate and escape-rate numbers the engineering team is acting on, packaged for the operating review and the supplier-scorecard conversation.*

### Question (Act 3.1)

> **Which process areas drive the most critical non-conformances, and what are the top findings?**

**What to say while it runs:** Inspection fail rate trend by process area over 12 months. This is the leading indicator the COO watches — if fail rate is climbing inside the plant, escape rate at the customer is six months behind it. The shape determines whether quality capex goes into inspection capacity or process control.

**What to look for:** Monthly fail_count vs. total_inspections by process_area. Watch for process areas where the fail rate is climbing — those are the CAPA-acceleration targets.

**Land the point:** When that view is in the COO's hand a quarter before the next escape, the customer scorecard conversation becomes a leading-indicator story, not a lagging-indicator apology. That's how supplier scorecards stop slipping.

### Question (Act 3.2)

> **Show monthly first-pass yield % by component class for the trailing 12 months.**

**What to say while it runs:** Monthly first-pass yield by component class over 12 months. FPY target is above 95% on machined parts and above 98% on assembly. The slope tells you whether the quality investments from last year are paying off — or whether next year's quality capex needs to be redirected.

**What to look for:** Monthly first_pass_yield_pct by component_class. Watch for component classes where FPY is below benchmark or trending down — those are the next-cycle capex priorities.

**Land the point:** Quality engineering, the VP of Quality, and the COO now share one view. The CAPA plan, the supplier-scorecard defense, and the quality capex case are written from the same data. One space. One quality story. Same answers across three audiences.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroQuality Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 root causes by total cost of quality over the last 12 months.
2. Show monthly trend in critical event count by component class.
3. Which component classes have the worst escape rate this quarter, and what is their cost of quality?
4. Top 10 components by days-to-closure on quality events — flag any over 30 days.
5. How has inspection fail rate trended month-over-month by process area?
6. Which process areas drive the most critical non-conformances, and what are the top findings?
7. Show monthly first-pass yield % by component class for the trailing 12 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
