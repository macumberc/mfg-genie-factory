# RestorePower Systems — Demo Script

**Space:** Electric Utility — RestorePower Systems - Outage Response & Crew Dispatch 🔌
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP T&D + CFO, Grid Ops Director, Field Operations Lead
**KPIs touched:** SAIDI, SAIFI, CAIDI, Restoration rate vs. SLA, Customer-minutes interrupted, Response time
**Big decision automated:** Pre-position mutual-aid crews ahead of the next storm and commit to the SAIDI/SAIFI/CAIDI numbers we defend at the PUC rate case — plus which feeders earn the next $20M of hardening capex vs. vegetation-management spend.

---

## Pre-demo checklist

- Open the Genie space `RestorePower Systems - Outage Response & Crew Dispatch 🔌`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RestorePower Systems runs distribution across 20 feeders in five service districts — Metro Underground, North Overhead Rural, South Coastal Overhead, East Mixed Tech Park, West Underground Airport. Today the active-outage list lives in the Grid Ops Director's OMS console, the crew dispatch and response/travel/repair time data lives in the Field Operations Lead's mobile workforce report, and the SAIDI/SAIFI/CAIDI numbers get rebuilt every month from a stitched-together extract for the PUC reliability filing. Three systems, three reporting cadences, and a mutual-aid pre-staging decision that gets made when the storm is already 12 hours out — which is how a 200,000-customer event burns 18 hours of restoration that should have been 8. This space puts active outages, customer-minutes, crew utilization, response/travel/repair time, restoration-rate-vs-SLA, and SAIDI/SAIFI/CAIDI in one governed surface — so the storm playbook and the rate-case defense are built on the same data.

---

## Key KPIs in scope

- SAIDI (minutes) — IEEE 1366 industry median ~120 minutes/customer/year
- SAIFI (events) — industry median ~1.0-1.4 events/customer/year
- CAIDI (minutes) — SAIDI/SAIFI; industry median ~80-130 minutes/event
- Restoration rate vs. SLA (%) — % of outages restored within target time
- Customer-minutes interrupted — total reliability exposure ($/CMI is a regulatory currency)
- Response time (minutes) — report-to-dispatch; target <30 min for P1 events
- Travel + repair time (minutes) — field execution efficiency
- Crew utilization (%) — workforce productivity

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CAIDI** | Customer Average Interruption Duration Index |
| **ROI** | Return on Investment |
| **SAIDI** | System Average Interruption Duration Index |
| **SAIFI** | System Average Interruption Frequency Index |
| **SLA** | Service Level Agreement |

---

## Act 1 — The signal — reading the outage portfolio before the next storm hits *(≈4 min)*

**Persona:** Grid Ops Director • **Job to be done:** Identify the feeders and districts most exposed to the next storm cycle — and the leading-cause patterns that pre-stage crews and equipment.

*This is the conversation that should happen *before* the next NWS storm watch — not at hour two of the event. Two questions surface the structural exposure and tell Grid Ops where mutual-aid pre-staging actually moves the needle.*

### Question (Act 1.1)

> **Show monthly trend of total customer-minutes interrupted by district for the trailing 12 months.**

**What to say while it runs:** Monthly trend of total_customer_minutes by district over 12 months. CMI is the regulator's currency — it's what shows up in the rate-case filing and what the PUC compares against the industry median. Districts trending up are the ones the next reliability report explains; districts trending down are the success stories we cite.

**What to look for:** Monthly trend, total_customer_minutes by district. The room should notice North and South — typically the overhead-feeder districts — dominate the CMI exposure, especially in summer storm months and winter ice months.

**Land the point:** Right there is the conversation about whether the existing reliability program is moving the customer-minute number — in real terms, not in 'we did X interventions' terms.

### Question (Act 1.2)

> **Top 10 feeders by total outage count over the last 90 days — what is the leading cause for each?**

**What to say while it runs:** Top 10 feeders by total_outage_count over the last 90 days with their leading cause. Storm is the natural-event noise; Tree Contact and Equipment Failure are the *controllable* causes that vegetation-management and asset-replacement programs are supposed to address. Feeders where Tree Contact dominates and they're still in the top 10 — the veg program isn't working there.

**What to look for:** Ranked feeder table: feeder_name, total_outage_count, top cause. The room should notice the overhead-rural feeders (FD-N04, FD-E04) with Tree Contact as the leading cause.

**Land the point:** That list used to be the output of an OMS query plus a manual cross-reference to the cause-coding sheet. Now it's the *first* question of the reliability planning cycle — and the veg-management vs. hardening capex tradeoff has data behind it.

---

## Act 2 — The decision — pre-stage mutual aid, dispatch contractor crews, and commit to the PUC SAIDI number *(≈4 min)*

**Persona:** Field Operations Lead • **Job to be done:** Decide which mutual-aid agreements to activate ahead of the next storm, where to place contractor crews, and what the defendable SAIDI commitment is for the next PUC filing.

*Three questions translate the response and crew-utilization signal into a pre-staging plan with dollars attached. The middle question is the anchor — SAIDI minutes converted into the customer-minutes-interrupted dollars the rate case is going to challenge.*

### Question (Act 2.1)

> **How has SAIDI minutes trended month-over-month by district?**

**What to say while it runs:** saidi_minutes trended month-over-month by district. IEEE 1366 industry median is ~120 minutes/customer/year. Districts above 120 are the rate-case explainers; districts below 80 are the regulatory-incentive earners. The slope matters as much as the number — a district trending the wrong direction is a finding before next year's filing.

**What to look for:** Monthly trend, avg saidi_minutes by district. The room should notice the overhead-heavy districts hugging the upper bound — that's where the storm-season pre-staging concentrates.

**Land the point:** When SAIDI by district is on the same screen as the controllable-cause list, the conversation with the PUC moves from defensive ('here's why our number was high') to programmatic ('here's the targeted capex and crew-staging plan that brings it back').

### Question (Act 2.2)

> **Which districts have the worst CAIDI in the most recent month, and how does that compare to the IEEE 1366 industry median of ~120 minutes?**

**What to say while it runs:** Districts with the worst caidi_minutes in the most recent month vs. the IEEE 1366 ~120-minute industry median. CAIDI is SAIDI/SAIFI — it's the per-event restoration time. High CAIDI with low SAIFI means we have few outages but they take forever — that's a *response or crew* problem, not an asset problem. Different conversation, different fix.

**What to look for:** District-level table: caidi_minutes, saifi_events. The room should notice the underground-Metro districts — typically *low* SAIFI but *high* CAIDI because UG faults are harder to locate.

**Land the point:** That comparison is the difference between *we have too many outages* and *we take too long to fix the outages we have*. Different problem, different capital. The Field Operations Lead can now defend an investment in fault-locating tech vs. another tree-trimming contract.

> **Anchor moment.** Stop on the SAIDI district-trend and the response-time table. Pick the district running ~30 SAIDI minutes above the 120-minute target. Assume 200,000 customers in the district.

> *30 SAIDI minutes above the industry median × 200,000 customers = 6,000,000 customer-minutes of excess interruption per year. Estimated cost-of-unserved-energy is $5-50/MWh; even at the low end of $15/MWh for residential, 6M customer-minutes ≈ 100,000 customer-hours of interruption ≈ ~50 MWh of unserved energy at typical household demand — $750K-$2M in pure unserved-energy economic loss *plus* the PUC penalty exposure tied to missed reliability targets, which on a rate-case docket can run another $5-15M per year per material miss. A mutual-aid pre-staging contract that knocks 20% off CAIDI on storm days runs $200-500K/year; a feeder hardening program for the worst overhead feeder is $2-4M one-time. The CAIDI improvement pays back in under 18 months on penalty exposure alone, before counting the customer goodwill that doesn't show up on the rate case but does show up in the next ESG survey.*

> That's the decision this space automates. Mutual-aid pre-staging and feeder-hardening capex get set on the same screen as the live SAIDI trend and the response-time table — not in next month's PUC filing. The storm playbook and the rate-case defense are built from the same data.

### Question (Act 2.3)

> **Rank crew types by average response time — are any above the 30-minute P1 target?**

**What to say while it runs:** Crew types ranked by avg_response_time_min — are any above the 30-minute P1 target? Response time is report-to-dispatch; over 30 minutes on a P1-Critical event is the line item the PUC underlines in red ink. Crew types that consistently miss it need either more crews on shift or a dispatch-process change.

**What to look for:** Crew type table: Line / Underground / Tree / Substation / Contractor with avg_response_time_min. The room should notice whether Contractor crews are systematically slower — if so, that's a contract-renegotiation conversation, not an internal-process one.

**Land the point:** Now the staffing decision has a number behind it. The Field Ops Lead can defend either expanding internal crews or renegotiating the contractor SLA — not both, not neither, the *right* one.

---

## Act 3 — The commitment — reliability program and PUC rate-case filing *(≈4 min)*

**Persona:** VP T&D • **Job to be done:** Defend the reliability program and the SAIDI/SAIFI/CAIDI commitments to the CFO, the board, and the PUC at the rate case — lock in next year's hardening capex and veg-management spend.

*The VP doesn't need new dashboards. They need the same outage, crew, and reliability numbers the ops team is acting on, in PUC-filing form, so the rate-case narrative writes itself.*

### Question (Act 3.1)

> **What is the storm outage count and total customers affected by district this year vs. last year?**

**What to say while it runs:** Storm outage_count and total customers_affected by district this year vs. last year. Storms get excluded from reliability reporting under major-event-day rules — but *trending* storm exposure tells us where climate is changing the underlying risk profile. Districts where storm impact is growing year-over-year need hardening regardless of the IEEE exclusion.

**What to look for:** Year-over-year table: storm_outage_count and total_customers_affected by district. The room should notice the coastal and overhead-rural districts where storm impact is climbing — that's the climate-resilience capex case.

**Land the point:** When that comparison is in the VP's hand before the rate-case prep, the climate-resilience capex ask becomes data-driven and PUC-defensible — not 'because storms are bad now'.

### Question (Act 3.2)

> **Show monthly trend of restoration rate within SLA by feeder type.**

**What to say while it runs:** Monthly trend of restoration_rate_pct vs. SLA by feeder_type. Overhead, Underground, Mixed all have different restoration profiles. The rate that matters is the one we publish to the PUC; the *trend* in that rate is what tells the regulator whether the program is working.

**What to look for:** Monthly trend lines per feeder_type: avg restoration_rate_pct. The room should notice whether Overhead feeders are converging toward the Underground baseline as the hardening program matures.

**Land the point:** Triage at 7, dispatch decision at 9, rate-case defense at 2. Same space, same numbers. The Grid Ops Director's outage list, the Field Ops Lead's pre-staging plan, and the VP T&D's PUC filing are now the same artifact — and the regulator gets one story instead of three reconciliations.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RestorePower Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly trend of total customer-minutes interrupted by district for the trailing 12 months.
2. Top 10 feeders by total outage count over the last 90 days — what is the leading cause for each?
3. How has SAIDI minutes trended month-over-month by district?
4. Which districts have the worst CAIDI in the most recent month, and how does that compare to the IEEE 1366 industry median of ~120 minutes?
5. Rank crew types by average response time — are any above the 30-minute P1 target?
6. What is the storm outage count and total customers affected by district this year vs. last year?
7. Show monthly trend of restoration rate within SLA by feeder type.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
