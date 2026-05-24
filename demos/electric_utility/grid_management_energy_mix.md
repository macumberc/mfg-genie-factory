# PowerGrid Analytics — Demo Script

**Space:** Electric Utility — PowerGrid Analytics - Grid Management & Energy Mix ⚡
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP T&D + ESG Lead + CFO, Grid Operations Manager, Resource Planner
**KPIs touched:** Renewable share, Curtailment, Carbon intensity, Capacity factor, Grid frequency, SAIDI
**Big decision automated:** Commit to the next 12-month generation dispatch and PPA-renewal policy — which fossil assets we curtail in favor of renewables, which renewables we curtail vs. firm with storage, which coal PPAs we exit, and what carbon-intensity number we publish to ESG investors.

---

## Pre-demo checklist

- Open the Genie space `PowerGrid Analytics - Grid Management & Energy Mix ⚡`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PowerGrid Analytics dispatches across 20 grid zones in five regions — Northern Wind Corridor, Southern Solar Belt, Eastern Nuclear, Western Hydro Basin, Central Gas. Today the renewable-share number lives in the Grid Operations Manager's EMS console, the curtailment-MWh and LMP-by-zone roll-up lives in the Resource Planner's market-ops sheet, and the SAIDI/SAIFI and carbon-intensity slide gets rebuilt every month for the ESG report. Three artifacts, three update cadences, and a dispatch decision that gets made on yesterday's EMS snapshot — which is how a Solar Belt zone curtails 3,000 MWh in a month that the Hydro Basin was importing from Central Gas. This space puts generation by fuel type, curtailment, carbon intensity, capacity factor, renewable share, SAIDI/SAIFI, and LMP in one governed surface — so the dispatch and PPA decisions track the actual generation stack, not the planning assumption.

---

## Key KPIs in scope

- Renewable share (%) — generation mix and clean energy target tracking
- Curtailment (MW / MWh) — wasted renewable energy; healthy <5% of renewable output
- Carbon intensity (kg CO2/MWh) — sub-200 = mostly clean, 400+ = heavy fossil
- Capacity factor (%) — asset productivity (solar ~20-25%, wind ~35-45%, nuclear ~90%)
- Grid frequency (Hz) — target 60.00; deviation >0.05 Hz triggers reliability concerns
- SAIDI (minutes) — IEEE 1366 industry median ~120 minutes/customer/year
- SAIFI (events) — industry median ~1.0-1.4 events/customer/year
- LMP ($/MWh) — locational marginal price; market and congestion signal

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **ESG** | Environmental, Social, Governance |
| **MW** | Megawatt |
| **SAIDI** | System Average Interruption Duration Index |
| **SAIFI** | System Average Interruption Frequency Index |

---

## Act 1 — The signal — reading the actual generation stack, not the planning assumption *(≈4 min)*

**Persona:** Grid Operations Manager • **Job to be done:** Confirm the dispatch stack is matching the planned generation mix — surface zones where curtailment or fossil share is running off-plan before the month closes.

*This is the conversation that should happen mid-month, not in the post-mortem. Two questions tell the Grid Ops Manager whether the renewables we built are actually being delivered to load.*

### Question (Act 1.1)

> **Show monthly trend of total generation MW by fuel type for the trailing 12 months.**

**What to say while it runs:** Monthly trend of total_generation_mw by fuel_type over 12 months. The mix tells us the structural story — Solar and Wind share climbing means the renewable build-out is reaching the meter; Natural Gas share flat or growing means we're still leaning on fossil for ramping and night load.

**What to look for:** Stacked monthly trend, generation_mw by Solar / Wind / Nuclear / Hydro / Natural Gas / Coal. The room should notice whether the renewable wedge is actually getting bigger or whether it's being offset by fossil baseload that's not retiring on schedule.

**Land the point:** Right there is the conversation about whether the decarbonization commitment is on track or whether the next ESG filing has a gap to explain — in real time, on the data, not in a slide built three weeks after the fact.

### Question (Act 1.2)

> **Top 10 zones by total renewable curtailment MW over the last 90 days.**

**What to say while it runs:** Top 10 zones by total_curtailment_mw over the last 90 days. Curtailment is wasted renewable energy — healthy is under 5% of renewable output; over 10% means we have congestion or oversupply we're not monetizing. Solar Belt and Wind Corridor zones at the top of this list mean we built generation we can't deliver — that's a storage or transmission-upgrade conversation.

**What to look for:** Ranked zone table: zone_name, total_curtailment_mw, fuel_type filtered to renewables. Southern Solar Belt and Northern Wind Corridor typically dominate.

**Land the point:** Before this space, that list got assembled from EMS logs once a quarter. Now it's the *first* question of the dispatch cycle — and the storage / transmission capex argument gets built on dollars of curtailed energy, not on a hypothetical capacity factor.

---

## Act 2 — The decision — dispatch, curtail, store, or exit the PPA *(≈4 min)*

**Persona:** Resource Planner • **Job to be done:** Commit to the next-12-month dispatch policy and the PPA renewal/exit decisions — which fossil PPAs we walk away from, which storage we sign, which renewable PPAs we cap.

*Three questions turn the curtailment and carbon signal into a defensible commercial decision. The middle question is the anchor — curtailed MWh converted into the foregone-revenue conversation that justifies storage or transmission.*

### Question (Act 2.1)

> **How has average carbon intensity trended month-over-month by region?**

**What to say while it runs:** Average carbon_intensity_kg_mwh trended month-over-month by region. Sub-200 is mostly clean; 400+ is heavy fossil. The slope is the decarbonization velocity — if a region's carbon intensity is flat or rising, the renewable build there isn't translating into delivered clean energy. That's where the ESG report has a gap.

**What to look for:** Monthly trend, avg carbon_intensity_kg_mwh by region. The Central region (Central Gas Corridor zone) typically anchors the high end; the Western region (Hydro Basin) anchors the low.

**Land the point:** When the carbon-intensity trend is on the same screen as the curtailment data, the conversation moves from 'are we hitting our renewable target' to 'are we *delivering* the renewable target' — those are very different ESG defenses.

### Question (Act 2.2)

> **Which regions have the highest SAIDI minutes and SAIFI events in the most recent month?**

**What to say while it runs:** Regions with the highest saidi_minutes and saifi_events in the most recent month. SAIDI median is around 120 min/customer/year, SAIFI 1.0-1.4 events. Anything materially above is a reliability conversation with the PUC — *and* a constraint on aggressive renewable integration, because reliability tolerance is what limits how far we can push intermittent share.

**What to look for:** Region-level ranked table: saidi_minutes, saifi_events. The room should notice whether the regions with the highest renewable share are also the ones with the worst reliability — that's the trade-off the executive team has to defend.

**Land the point:** Now the renewable-integration debate is grounded. The Resource Planner can defend pulling back on Wind in one zone *or* doubling down on storage in another — with the reliability number on the same screen as the renewable share.

> **Anchor moment.** Hold the curtailment leaderboard and the LMP-by-zone table on screen. Pick the worst-curtailed Solar Belt zone — call it 4,500 MWh of curtailment last month, monthly average LMP in the importing zones at $55/MWh.

> *4,500 MWh of curtailed renewable output at $55/MWh of monetizable value (foregone PPA revenue + REC value) is $250K of stranded value in *one zone in one month*. Across the 12 months on screen that's $3M of foregone revenue per high-curtailment zone; with 4-5 zones in this category that's $12-15M/year. A battery-storage build to firm that output and serve it into the evening peak runs $500-800/kWh installed — a 50 MWh battery at $600/kWh is $30M, paying back on curtailed-energy recovery in 2-3 years even before the ancillary-services revenue. On the *other* lever: a fossil PPA renewal at 400 kg CO2/MWh × 100 MW × 5,000 hours = 200,000 tons of CO2 × carbon-pricing exposure of $30-50/ton = $6-10M/year of carbon liability the board doesn't want on the books.*

> That's the decision this space automates. PPA renewal, storage sign-off, and curtailment policy get set on the same screen as the carbon intensity and the reliability number — not in three separate market-ops, ESG, and reliability reports. The dispatch policy gets built on delivered MWh and dollars, not on planning-stack assumptions.

### Question (Act 2.3)

> **What is the average renewable share by region this year, and how does it compare to last year?**

**What to say while it runs:** Top 10 zones by congestion_index with their avg_lmp_usd_mwh. Congestion above 7 means the transmission is the binding constraint; high LMP in a congested zone means we're paying market premium for power we should be generating locally. That's the transmission-upgrade or local-storage business case in one query.

**What to look for:** Zone ranked table: zone_name, avg congestion_index, avg LMP. Eastern Port District and Central Data Center Hub typically anchor the high-congestion list.

**Land the point:** That comparison is the difference between knowing a zone is congested and knowing the *cost* of that congestion. The first is an operating note; the second is a $50-200M transmission capex case.

---

## Act 3 — The commitment — decarbonization plan and PPA portfolio for the next year *(≈4 min)*

**Persona:** VP T&D + ESG Lead • **Job to be done:** Defend the generation mix, curtailment program, and reliability trade-offs to the CFO, the board, and the ESG investors — lock in next year's PPA portfolio and storage capex.

*The VP doesn't need a new dashboard. They need the same generation, curtailment, carbon, reliability, and LMP numbers the ops team is acting on, in board-ready and 10-K-ready form.*

### Question (Act 3.1)

> **Top 10 zones by congestion index — what is the average LMP for those zones?**

**What to say while it runs:** Avg renewable_share_pct by region this year vs. last year. The year-over-year delta *is* the decarbonization story for the ESG report. Regions where renewable share grew despite curtailment headwinds are the success cases; regions where it grew because fossil curtailed for maintenance and not policy reasons — those need to be flagged before the auditor finds them.

**What to look for:** Region table: renewable_share_pct this year, last year, delta. The room should notice the regions where the year-over-year story is *real* (capacity added) vs. *artifact* (fossil down for maintenance).

**Land the point:** When that delta is in the VP's hand before the ESG investor day, the story is defensible at the line-item level — not at the press-release level.

### Question (Act 3.2)

> **Show monthly trend of total carbon emissions tons against renewable share % across the network.**

**What to say while it runs:** Monthly trend of total_carbon_tons against renewable_share_pct over 12 months. The two lines tell the actual decarbonization curve. If carbon-tons is flat while renewable-share grew, the renewable additions are mostly displacing other renewables, not fossil — which is a portfolio-design problem.

**What to look for:** Two-axis monthly trend: total_carbon_tons descending (ideally), renewable_share_pct ascending. The room should notice whether the two lines are moving in lockstep or whether one is leading and the other is stuck.

**Land the point:** Triage at 9, dispatch decision at noon, board pitch at 5. Same space, same numbers. The Grid Ops Manager's curtailment list, the Resource Planner's PPA recommendation, and the VP/ESG's investor narrative are now the same artifact — and the board gets one story instead of three reconciliations.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PowerGrid Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly trend of total generation MW by fuel type for the trailing 12 months.
2. Top 10 zones by total renewable curtailment MW over the last 90 days.
3. How has average carbon intensity trended month-over-month by region?
4. Which regions have the highest SAIDI minutes and SAIFI events in the most recent month?
5. What is the average renewable share by region this year, and how does it compare to last year?
6. Top 10 zones by congestion index — what is the average LMP for those zones?
7. Show monthly trend of total carbon emissions tons against renewable share % across the network.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
