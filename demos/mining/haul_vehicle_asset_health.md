# MineTruck Analytics — Demo Script

**Space:** Mining — MineTruck Analytics - Haul Vehicle Asset Health 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Reliability + Fleet Manager, Mine Manager, CFO partner
**KPIs touched:** Mechanical availability, Daily payload, Cycle time, Fleet health score, Critical / Warning alert count, Mean time between failures
**Big decision automated:** Which 3-5 ultra-class haul trucks to refurbish, which to run-to-failure, and whether the $5M-per-unit replacement cycle gets accelerated or deferred 12 months.

---

## Pre-demo checklist

- Open the Genie space `MineTruck Analytics - Haul Vehicle Asset Health 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> MineTruck Analytics manages 20 ultra-class haul trucks — Cat 797F, Komatsu 930E, Liebherr T284, Hitachi EH5000, BelAZ 75710, and Cat 794AC — operating across four pits, with each unit carrying roughly $5M of replacement value. Today the daily availability picture lives in the Fleet Manager's morning dispatch sheet, the sensor-driven health scores in the Reliability VP's weekly condition-monitoring report, and the repair-cost and RUL view in the CFO partner's quarterly capex book. Three artifacts, three cadences, same fleet — and the refurbish-vs-replace conversation on a $5M asset gets made on whichever number was most recent in someone's email. This space ends that. One governed surface where availability, sensor health, failure probability, and unplanned-downtime dollars sit in the same conversation that locks the AFE.

---

## Key KPIs in scope

- Mechanical availability (%) — target 85-92% for ultra-class trucks
- Daily payload (tons) — total tons hauled per truck-day, typical range 100-400 tons across the fleet
- Cycle time (minutes) — primary tons-per-operating-hour driver
- Fleet health score (0-100) — composite from sensor telemetry
- Critical / Warning alert count — leading indicator of unplanned downtime
- Mean time between failures (MTBF, hours) — industry benchmark 200-400 hrs
- Remaining useful life (RUL, days) — component changeout planning input
- Repair cost ($) and unplanned downtime hours — opex and lost-production impact

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **MTBF** | Mean Time Between Failures |
| **RUL** | Remaining Useful Life |

---

## Act 1 — The signal — finding the trucks that are quietly failing *(≈4 min)*

**Persona:** Fleet Manager • **Job to be done:** Pull the units whose health scores are deteriorating out of the telemetry — not by gut, by trended fleet health and 30-day failure probability.

*This is where the refurbish-vs-retire shortlist starts forming. Two questions in, the Fleet Manager already has the per-model health picture that used to take a day of stitching against the OEM condition-monitoring reports.*

### Question (Act 1.1)

> **Show monthly fleet health score trend by vehicle model for the trailing 12 months.**

**What to say while it runs:** Monthly fleet health score by model for the last 12 months. The 797Fs and 930Es should sit in the 80-95 band when they're healthy. A model whose average health score is sliding into the 60s over two quarters is a fleet-wide flag — that's an engineering investigation, not a single-unit fix.

**What to look for:** Twelve months of avg_health_score by model. Watch for the model whose curve has bent downward — that's the model whose component-changeout cycle needs to be revisited.

**Land the point:** Before this space that picture was rebuilt by hand against six OEM portals. Now it's the Fleet Manager's first question of the day — and the model-level reliability conversation starts from a trend, not from a single unit's bad week.

### Question (Act 1.2)

> **Which 10 haul trucks have the highest 30-day failure probability right now, and what is each one's RUL?**

**What to say while it runs:** Top 10 trucks by 30-day failure probability and their remaining useful life. >40% probability with RUL under 60 days is run-to-failure territory; >60% probability with RUL under 30 days is an emergency component changeout that can't wait for the planned shutdown.

**What to look for:** A ranked list of 10 trucks by high_risk_count or 30-day failure probability with avg_rul next to them. The top of the list is the immediate scheduling decision; the middle of the list is the AFE candidate set.

**Land the point:** Now the Fleet Manager can rank failure risk across 20 ultra-class trucks in seconds — that's the input to the refurbish-vs-run-to-failure conversation that used to require an OEM service rep on a Zoom call.

---

## Act 2 — Refurbish, retire, or run-to-failure — locking the AFE list *(≈4 min)*

**Persona:** Mine Manager • **Job to be done:** Decide which 3-5 ultra-class trucks get the $1.5-2.5M refurbishment slot, which get the $5M replacement, and which the team runs into the ground for the rest of the production year.

*Three questions that move the unit-level shortlist into a defensible capex recommendation. The middle question is the anchor — unplanned-downtime hours converted to lost-production dollars is the conversation the CFO came to see.*

### Question (Act 2.1)

> **Top 10 vehicle models by total unplanned downtime hours this year — rank by lost production impact.**

**What to say while it runs:** Top 10 vehicle models by total unplanned downtime hours this year. Ultra-class unplanned downtime runs $8-15K per hour in lost production. A model with 400+ hours of unplanned downtime is structurally costing us $3M+ a year — that's a capex conversation, not a maintenance conversation.

**What to look for:** Models ranked by total_downtime. The top of the list is the model whose entire refurbishment cadence needs to be revisited — not unit-by-unit, model-by-model.

**Land the point:** That used to be the Reliability VP's quarterly slide. Now it's the input to the AFE shortlist the Mine Manager and CFO partner argue about every capex cycle.

### Question (Act 2.2)

> **How has total repair cost trended month-over-month by failure type across the fleet?**

**What to say while it runs:** Monthly repair cost by failure type across the fleet. Engine and powertrain failures dominate the spend; tire failures are the surprise — off-the-road tires are $40-80K each with 4-8 week lead times. A tire-failure-cost trend that's climbing is a procurement and rotation problem, not a maintenance one.

**What to look for:** Monthly total_repair_cost by failure type. Watch for the failure type whose share is growing — that's where the next component-strategy investment goes.

**Land the point:** Before this space the failure-type breakdown was a manual SAP query that took two days. Now it's a single chart — and the procurement conversation about tire spend, hydraulic kits, and powertrain rebuilds happens against actual data.

> **Anchor moment.** Stop on the unplanned-downtime ranking. Pick the worst model — call it 350 hours of unplanned downtime this year across 4 units, each unit carrying $5M of replacement value.

> *350 hours of unplanned downtime at $10K/hour of lost production = $3.5M/year of recoverable production on one model — across just 4 units. A full unit replacement is roughly $5M; a refurbishment is $1.5-2.5M with a 4-6 month return-to-service. Refurbishing two of those four units recovers ~$1.75M/year of lost production at a $3-5M capex outlay — sub-3-year payback on capital we were going to spend anyway. Across the 20-truck fleet, this conversation is a $10-15M capex re-prioritization that lives in one screen.*

> That's the decision this space automates. Not the AFE slide. The decision. The refurbishment list gets built on hours-of-downtime dollars, not on the OEM rep's pitch in the most recent service meeting.

### Question (Act 2.3)

> **Which pits have the most Critical alerts in the last 90 days, and which vehicle models are driving them?**

**What to say while it runs:** Pits with the most Critical alerts in the last 90 days, broken out by vehicle model. Critical alerts are the leading indicator of unplanned downtime — if Pit 3 is generating 60% of the Criticals and they're concentrated on the Komatsu 930Es, that's a haul-profile issue, not a fleet-wide issue.

**What to look for:** critical_count by pit with model breakdown. Watch for the pit-model combination that concentrates the alerts — that's the conversation about haul routes, ramp grades, and operator coaching.

**Land the point:** That ranked picture turns into the pit-level operating decision. Not 'we need to reduce Criticals' — 'we are rotating the 930Es out of Pit 3 next quarter and accelerating the refurb on these two units'.

---

## Act 3 — The commitment — locking the AFE and the component-changeout calendar *(≈4 min)*

**Persona:** VP Reliability • **Job to be done:** Defend the refurbish-vs-replace recommendation to the CFO and the executive committee, and reshape next year's component-changeout calendar.

*The VP needs the same numbers the planners are acting on, framed so the AFE narrative and the component-strategy update tell the same story.*

### Question (Act 3.1)

> **What is the average daily payload by vehicle model across the fleet?**

**What to say while it runs:** Average daily payload by model across the fleet. This is the productivity number — a 930E carrying 320 tons against a benchmark of 340 is leaving ~6% of revenue tons on the table. Combined with the health-score trend, this is the *is the asset still earning its keep* question.

**What to look for:** Per-model avg daily payload. Watch for the model running structurally below benchmark — that's the model whose refurbishment ROI looks worst and whose replacement priority looks highest.

**Land the point:** When the VP can put payload, health score, and unplanned-downtime dollars on one screen, the AFE conversation moves from 'we need new trucks' to 'these two units get refurbished, these three move to run-to-failure, and the $5M replacement on unit 17 is deferred 12 months'.

### Question (Act 3.2)

> **Top 10 vehicles by repair cost over the last 6 months — and what failure types are most common on each?**

**What to say while it runs:** Top 10 trucks by repair cost over the last 6 months and the failure types driving each. This is the unit-level closing argument — repair cost combined with failure pattern tells us whether the next dollar is best spent on this unit or on its successor.

**What to look for:** Trucks ranked by total_repair_cost with failure-type breakdown attached. The top units with concentrated failure types (e.g., repeated hydraulics) are the candidates for kit-based refurb; units with scattered failure modes are retirement candidates.

**Land the point:** Daily ops at 7 AM, refurbishment shortlist at 9, AFE pitch at 11. Same space. The Fleet Manager's watchlist and the VP Reliability's capex story are now the same artifact — and the executive committee gets one number, not three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — MineTruck Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly fleet health score trend by vehicle model for the trailing 12 months.
2. Which 10 haul trucks have the highest 30-day failure probability right now, and what is each one's RUL?
3. Top 10 vehicle models by total unplanned downtime hours this year — rank by lost production impact.
4. How has total repair cost trended month-over-month by failure type across the fleet?
5. Which pits have the most Critical alerts in the last 90 days, and which vehicle models are driving them?
6. What is the average daily payload by vehicle model across the fleet?
7. Top 10 vehicles by repair cost over the last 6 months — and what failure types are most common on each?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
