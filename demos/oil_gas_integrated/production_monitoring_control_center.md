# PetroPulse Integrated — Demo Script

**Space:** Oil & Gas Integrated — PetroPulse Integrated - Production Monitoring Control Center 📊
**Runtime:** ~15 minutes • 7 questions
**Audience:** Upstream VP and Asset Managers + Control Center Supervisor, Production Operations Lead, Field Asset Manager
**KPIs touched:** Total oil and gas, Well uptime, Water cut, GOR, Deferred oil, Wellhead pressure and choke position
**Big decision automated:** Which wells across the 6 Gulf platforms get ramped, which get constrained, and which get prioritized for intervention this week — and how the hurricane-evac deferred-volume story gets owned by the Upstream VP before the monthly report lands.

---

## Pre-demo checklist

- Open the Genie space `PetroPulse Integrated - Production Monitoring Control Center 📊`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PetroPulse Integrated runs 20 wells across 6 deepwater Gulf platforms — Thunder Horse, Mars, Atlantis and three others — producing roughly 500,000 BOE/d combined. Today the control center watches choke and wellhead pressure off the SCADA HMI in real time, the water-cut and GOR trend lives in a reservoir engineer's monthly book, and the hurricane-evac deferred-volume number is reconciled out of the Production Operations weekly report. Three artifacts, same wells — and when a major storm forces an evac of two platforms, the Upstream VP gets three slightly different deferred-oil estimates from three teams over three days. This space ends that. Oil, gas, water cut, GOR, uptime, deferred volume, choke position — one governed surface, same conversation, in time to actually change a flow allocation.

---

## Key KPIs in scope

- Total oil (bbl/d) and gas (MCF/d) — top-line production volume
- Well uptime (%) — IOGP top-quartile >95%
- Water cut (%) — reservoir maturity / waterflood indicator
- GOR (SCF/bbl) — reservoir pressure / gas breakthrough signal
- Deferred oil (bbl) — production lost to events vs. potential
- Wellhead pressure (PSI) and choke position (%) — operating envelope
- Event severity mix — High/Critical vs Low/Medium event share
- BOE (oil + gas/6) — combined hydrocarbon throughput

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **BOE** | Barrels of Oil Equivalent |
| **GOR** | Gas-Oil Ratio (SCF/BBL) |
| **MCF** | Thousand Cubic Feet (gas volume) |
| **PSI** | Pounds per Square Inch |
| **SCF** | Standard Cubic Feet |
| **VP** | Vice President |

---

## Act 1 — The signal — which wells are carrying the platform print *(≈4 min)*

**Persona:** Production Operations Lead • **Job to be done:** Anchor the platform production picture for the morning operations call — which wells deserve attention, which deserve protection, which deserve a flow tweak.

*This is the production lead's first hour. Two questions in, the well-level oil ranking and the field-level oil-plus-gas trend are on screen — the same numbers that used to require pulling three separate reports.*

### Question (Act 1.1)

> **Top 10 wells by total oil production in barrels over the last 90 days.**

**What to say while it runs:** Top 10 wells by total oil production over the last 90 days. The point isn't the rank — it's the *concentration*. In a typical Gulf platform fleet, 6-8 wells carry over half the production. If a single well at the top falls 10%, the platform print misses by 4-5%. The ranking is the asset-protection list.

**What to look for:** Ranked table of 10 wells by total_oil_bbl over 90 days. Watch the spread top-to-bottom and look for any platform whose top contributors cluster — that's concentration risk that needs an intervention plan.

**Land the point:** Now the Production Lead can hand the morning ops call the concentration view that used to take half a day of allocation-system pulls. That's the well-protection conversation that used to happen too late.

### Question (Act 1.2)

> **Show monthly total oil and gas production by field for the trailing 12 months.**

**What to say while it runs:** Monthly total oil and gas production by field over 12 months. This is the chart the Asset Manager and the Upstream VP both look at — but historically they look at slightly different versions. The field-level view shows where production is structurally up vs. where it's drifting; gas trend separately because gas-handling capacity is the actual constraint on a lot of deepwater platforms.

**What to look for:** Monthly total_oil_bbl and total_gas_mcf by field_name. Watch for fields where gas is climbing faster than oil — that's GOR drift showing up at the field level, and it's a gas-handling constraint conversation.

**Land the point:** When the same field trend is in the control center's hand, the Asset Manager's deck, and the Upstream VP's monthly review, the platform-level rate-optimization conversation stops being about whose number is current.

---

## Act 2 — Ramp, constrain, or shut in — locking this week's flow allocation *(≈4 min)*

**Persona:** Control Center Supervisor • **Job to be done:** Set the platform-by-platform flow allocation for the week: which wells get the choke opened, which get constrained, and which trigger an intervention.

*Three questions that turn the well-level data into a flow-allocation decision. The middle question — hurricane-evac deferred volume — is the anchor that converts the storm response from a status report into a financial story.*

### Question (Act 2.1)

> **Which wells have water cut above 60%, and what platforms are they on?**

**What to say while it runs:** Wells with water cut above 60%, and what platforms they're on. Water cut over 60% means we start prioritizing water-handling capacity; over 75% the well is near its economic limit. On deepwater platforms, water-handling capacity is a hard ceiling — a single well climbing fast can starve the rest of the platform on processing capacity.

**What to look for:** Table of wells with snapshot water_cut_pct > 60 grouped by platform_name. Look for platforms with multiple high-water-cut wells — those are platforms where the rate allocation is actually a water-handling allocation.

**Land the point:** Now the Control Center supervisor can take this list straight into the rate-allocation conversation with the platform engineer — which wells get choked back this week to protect the rest of the platform's production.

### Question (Act 2.2)

> **What was the total deferred oil from Hurricane Evac events this year, by field?**

**What to say while it runs:** Total deferred oil from Hurricane Evac events this year, by field. Hurricane-season deferred production is the single most-disputed number in deepwater operations — every team has a different reconciliation. This is the governed view. At Gulf platform scale, a single Cat-3 evac can defer 100-300K BBL across a field.

**What to look for:** Sum of deferred_oil_bbl filtered to event_category = Hurricane Evac, grouped by field_name. Watch which fields carry the most evac exposure — those are the fields where weather-resilience capex earns the most defensible return.

**Land the point:** When the Upstream VP gets one number for hurricane deferred volume — not three — the conversation with corporate Finance becomes about the response plan, not about reconciling the data.

> **Anchor moment.** Hold on the hurricane-evac deferred-oil chart and pick the worst-hit field — call it 250,000 BBL deferred across two platforms in one major storm event this season.

> *250,000 BBL of deferred production at $70/BBL realized is $17.5M of lost revenue from one storm event on one field. Multiply across a Gulf season where 2-3 evacs is normal at this kind of platform exposure and you're looking at $40-60M of weather-driven deferred production per year. On top of that, every day of unplanned platform downtime — storm-related or not — runs $250K-1M depending on platform size. The choice is no longer 'absorb the deferred volume' — it's deciding whether weather-resilience capex (storm-hardened risers, pre-positioned spares, accelerated re-start protocols) at $10-30M earns its return against $40-60M of recurring annual exposure. At PetroPulse's scale, the answer is structurally yes.*

> That's the conversation this space converts from a post-event reconciliation into a forward capex case. Hurricane-resilience moves from a recurring write-down into a quantifiable investment decision.

### Question (Act 2.3)

> **Top 10 wells by uptime percentage this quarter — and how does that compare to last quarter?**

**What to say while it runs:** Top 10 wells by uptime this quarter versus last quarter. IOGP top-quartile uptime is over 95%. The quarter-on-quarter comparison is the part the weekly report usually skips. A well dropping from 98% to 92% uptime isn't broken — it's drifting — and drift is what becomes downtime two quarters later.

**What to look for:** Top 10 by uptime_pct with last quarter alongside. Look for the negative deltas; those are the wells where the next event originates and where pre-emptive work should be scheduled.

**Land the point:** Uptime drift, quarter-on-quarter, in one view. That's the difference between a wells-need-attention report and a wells-need-an-AFE recommendation.

---

## Act 3 — Defending the portfolio rate plan to the Upstream VP *(≈4 min)*

**Persona:** Field Asset Manager • **Job to be done:** Take the wells-level signal up to a portfolio-level rate-optimization recommendation against the production target and the safety-event posture.

*The Field Asset Manager is the one who has to defend the portfolio rate plan against the corporate production target. The wellhead-pressure trend and the high-severity event count are the two views that frame that conversation.*

### Question (Act 3.1)

> **How has average wellhead pressure trended month-over-month for Thunder Horse wells?**

**What to say while it runs:** Wellhead pressure trend on Thunder Horse wells, month over month. Wellhead pressure decline is the leading indicator of reservoir-energy depletion. In a mature deepwater field like Thunder Horse, sustained pressure decline 3-6 months ahead of production decline is what shapes the next infill or recompletion AFE — wait for the production decline to show up and you're already a year late.

**What to look for:** Monthly avg_wellhead_pressure_psi trend on Thunder Horse wells. Look for inflection points or sustained decline — those are the leading indicators that frame the next reservoir-management decision.

**Land the point:** When wellhead-pressure decline shows up here a quarter before the production decline shows up in the rate report, the Field Asset Manager has a real shot at moving the next AFE into the planning cycle before the asset starts hurting EBITDA.

### Question (Act 3.2)

> **Which platforms had the highest count of High and Critical severity events this year?**

**What to say while it runs:** Platforms ranked by High and Critical severity event count this year. Platform severity-event count is the safety and reliability posture that the Board now reads alongside the production print — investor-grade ESG disclosure requires it. Platforms with rising critical-event counts get the next reliability capex and the next operational scrutiny, in that order.

**What to look for:** Grouped count of events where severity IN ('High','Critical') by platform_name. Watch for platforms whose count is materially higher than peers — those are the platforms where the safety-case story drives the next decision.

**Land the point:** Severity-event count by platform, governed, every cycle. That's the difference between a safety report that lands a week late and a safety posture the Upstream VP can defend in real time to the Board safety committee.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PetroPulse Integrated — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 wells by total oil production in barrels over the last 90 days.
2. Show monthly total oil and gas production by field for the trailing 12 months.
3. Which wells have water cut above 60%, and what platforms are they on?
4. What was the total deferred oil from Hurricane Evac events this year, by field?
5. Top 10 wells by uptime percentage this quarter — and how does that compare to last quarter?
6. How has average wellhead pressure trended month-over-month for Thunder Horse wells?
7. Which platforms had the highest count of High and Critical severity events this year?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
