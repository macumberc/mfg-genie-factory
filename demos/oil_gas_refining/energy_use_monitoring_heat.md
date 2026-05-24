# HeatTrack Refining — Demo Script

**Space:** Oil & Gas Refining — HeatTrack Refining - Energy Use Monitoring & Heat Optimization 🌡️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Refining + Energy Manager, Refinery Manager, Sustainability Lead
**KPIs touched:** Solomon Energy Efficiency Index, Heat recovery on crude preheat train, Thermal efficiency of fired heaters, Fouling factor and actual/clean UA ratio, Energy intensity, CO2 intensity
**Big decision automated:** Which 3-5 heat exchangers to pull and clean this cycle, which fired heaters earn a tuning campaign, and whether the Hydrogen Plant retrofit goes in this year's capex slate — defended against the Solomon EII top-quartile target.

---

## Pre-demo checklist

- Open the Genie space `HeatTrack Refining - Energy Use Monitoring & Heat Optimization 🌡️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> HeatTrack Refining runs 20 heat exchangers and fired heaters across the Crude Preheat Train, FCC Heat Recovery, Hydrotreating, Catalytic Reforming, and Hydrogen Plant. Today the fouling factor and clean-UA ratio live in the Energy Manager's exchanger spreadsheet, the Solomon EII number arrives by email from the third-party benchmark consultant once a quarter, and CO2 intensity gets reconciled by Sustainability against the ESG report tracker. Three artifacts, three update cadences — so the cleaning queue, the fired-heater tuning list, and the Hydrogen Plant retrofit business case never line up in the same conversation. This space ends that. Daily fouling and effectiveness become the same data the Refinery Manager defends in front of the executive team — and the EII top-quartile push stops being a quarterly surprise.

---

## Key KPIs in scope

- Solomon Energy Efficiency Index (EII) — top-quartile target <85, industry average ~100
- Heat recovery (%) on crude preheat train — best-in-class >85%
- Thermal efficiency (%) of fired heaters — modern designs hit 90%+
- Fouling factor and actual/clean UA ratio — proxy for cleaning-cycle ROI
- Energy intensity (BTU per barrel processed)
- CO2 intensity (kg per barrel) — ESG / Scope 1 reporting
- Total energy cost ($) by process unit
- Heat exchanger effectiveness (%) by category

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **ESG** | Environmental, Social, Governance |
| **ROI** | Return on Investment |

---

## Act 1 — The signal — finding the fouled exchangers and untuned heaters before the EII letter arrives *(≈4 min)*

**Persona:** Energy Manager • **Job to be done:** Pull this week's cleaning candidates and heater-tuning candidates from the daily fouling and thermal-efficiency stream — not from the next quarterly benchmark report.

*This is where the cleaning queue and the tuning campaign get rebuilt every week. Two questions in and the Energy Manager has the ranked list that used to require pulling exchanger files one at a time.*

### Question (Act 1.1)

> **Top 10 exchangers by total energy consumption (MMBTU) over the last 12 months.**

**What to say while it runs:** Total energy consumption in MMBTU is the headline number Sustainability and Finance both care about — Sustainability for Scope 1, Finance for the fuel-gas P&L line. The top 10 exchangers and heaters typically drive 60-70% of the refinery's total energy spend.

**What to look for:** A ranked table of the top 10 assets by `total_energy_mmbtu` over 12 months. The room should notice the long-tail shape — and that two or three names will look familiar to anyone who has read last quarter's Solomon report.

**Land the point:** Now the Energy Manager can isolate the 3-5 assets that move the EII needle in minutes — that's the cleaning-priority and heater-tuning conversation that used to wait for the next benchmark cycle.

### Question (Act 1.2)

> **Show monthly trend of average Solomon Energy Efficiency Index for the trailing 12 months.**

**What to say while it runs:** Solomon EII is the number the Refinery Manager defends to the executive committee. Industry average is 100, top-quartile is below 85, and every point you move is worth $5-15M a year in fuel-gas savings on a refinery our size. The trend matters more than the snapshot — direction is what tells you whether the energy program is winning.

**What to look for:** A 12-month line of `avg_thermal_efficiency` rolled monthly with the Solomon-equivalent EII commentary. Watch for the inflection where heat-recovery slippage started bleeding into the index.

**Land the point:** Before this space, that chart was rebuilt by hand for the quarterly benchmark review. Now it's the Energy Manager's *first question of the day* — and the EII defense to the executive team writes itself.

---

## Act 2 — The decision — which exchangers get cleaned, which heaters get tuned, which units lose the budget fight *(≈4 min)*

**Persona:** Refinery Manager • **Job to be done:** Lock the cleaning-cycle schedule for the next turnaround window and decide which fired heaters earn a tuning campaign vs. a deferred-action note in the year-end review.

*Three questions that turn the daily fouling stream into a defensible cleaning AFE and a defensible CO2 commentary. The middle question is the anchor — fouled-UA-ratio dollars.*

### Question (Act 2.1)

> **Which fired heaters have thermal efficiency below 70% and need tuning?**

**What to say while it runs:** Modern fired heaters should hit 90%+ thermal efficiency — anything below 70% is leaking fuel gas into the stack. Each 1% efficiency gap on a 100 MMBTU/hr heater is worth roughly $300K a year in fuel-gas burn at $5/MMBtu. Below 70% isn't a tuning question, it's a *combustion-air-control or excess-O2 controller* question.

**What to look for:** A short table of fired heaters with `avg_thermal_efficiency` below 70% and their process unit. The list is short — and it is the tuning-campaign queue for the next two months.

**Land the point:** That list used to be the output of a half-day comparing heater performance test sheets. Now it's the input to the maintenance-planning meeting that happens at 8 AM Monday.

### Question (Act 2.2)

> **Top 10 process units by total CO2 emissions year-to-date.**

**What to say while it runs:** Actual-over-clean UA ratio below 0.7 means the exchanger has lost more than 30% of its design heat transfer to fouling. That's the textbook trigger for pulling and cleaning — typically $50-200K of work that pays back in 2-8 weeks via fuel-gas savings on the downstream heater.

**What to look for:** A ranked table of exchangers by `avg_ua_ratio` below 0.7, with process unit. The cluster pattern matters — if three of them are on the Crude Preheat Train, that's a sequenced cleaning campaign, not three separate work orders.

**Land the point:** When the Energy Manager, the Refinery Manager, and the Sustainability Lead all see the same fouling ranking, the conversation stops being about whose spreadsheet is most current and starts being about *which exchangers get pulled in which slot*.

> **Anchor moment.** Stop on the UA-ratio table from the second question. Pick the three worst exchangers — call them all on the Crude Preheat Train, average UA ratio around 0.6.

> *Three fouled exchangers at 0.6 actual/clean UA means roughly 40% lost heat recovery on each. On a 200K BPD refinery, the crude preheat train moves enough duty that a 5% heat-recovery loss is about $4M/year in additional fired-heater fuel-gas burn at $5/MMBtu. Cleaning all three is $200-600K of work. Payback under 6 weeks. Now stack the EII upside — one Solomon EII point on a 200 KBD refinery is worth $5-15M/year. Pull two points out of this cleaning campaign and the Hydrogen Plant retrofit AFE just paid for itself before it even gets approved.*

> That's the decision this space automates. Not the Sustainability slide. The cleaning AFE list, the heater-tuning campaign, and the EII-defense narrative — all on the same data the Refinery Manager defends to the executive committee.

### Question (Act 2.3)

> **Which heat exchangers have actual/clean UA ratio below 0.7 — candidates for cleaning?**

**What to say while it runs:** CO2 intensity per barrel processed is what Sustainability defends to the board and what the EU CBAM regime is going to start charging us on. The top units by CO2 emissions are almost always the same units that have the EII headroom — that's the lucky alignment we want to exploit.

**What to look for:** Top 10 process units by `total_co2_tons` YTD. The ranking should look almost identical to the fuel-gas burners list — which is exactly the point.

**Land the point:** That overlap is the difference between treating ESG as a reporting problem and treating it as a P&L lever. Same units, same data, two budget defenses.

---

## Act 3 — The commitment — locking the EII target defense and the Hydrogen Plant retrofit slot *(≈4 min)*

**Persona:** Sustainability Lead • **Job to be done:** Make the CO2 intensity story defensible to the board and slot the Hydrogen Plant retrofit into the right capex cycle.

*Sustainability doesn't need another data feed; they need the same numbers the Energy Manager is acting on, in the same language, so the Scope 1 narrative and the EII defense are the same artifact.*

### Question (Act 3.1)

> **How has heat recovery percentage trended month-over-month across the crude preheat train?**

**What to say while it runs:** Heat-recovery percentage on the Crude Preheat Train is the leading indicator for both EII and CO2 intensity. Best-in-class is above 85%. Anything sliding below 80% on a monthly basis is the early warning that another cleaning campaign is overdue — *before* the fired-heater fuel-gas burn shows up in the quarterly report.

**What to look for:** Monthly trend of heat recovery on Crude Preheat Train. Inflection points are exactly the months the cleaning schedule slipped. The room should be able to read which quarter the next slippage is coming.

**Land the point:** When that curve is in the Sustainability Lead's hand a quarter before the EII letter arrives, the board narrative moves from reactive to programmatic — and the executive team stops asking why the benchmark moved.

### Question (Act 3.2)

> **Which equipment categories have the highest average energy intensity per barrel?**

**What to say while it runs:** Energy intensity per barrel by equipment category is the *which technology bucket gets the next capex dollar* view. Fired heaters, exchangers, compressors — the rank order tells you whether the Hydrogen Plant retrofit is the right next bet or whether the FCC Heat Recovery integration moves first.

**What to look for:** Categories ranked by `avg_energy_intensity`. The dollar-conversion is the part that breaks the tie when two categories look operationally similar.

**Land the point:** Daily cleaning queue at 8 AM, capex slate at 10 — same space, same numbers. The Energy Manager's tuning list, the Refinery Manager's cleaning AFE, and the Sustainability Lead's CO2 commentary are now the *same artifact* — and the executive team gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — HeatTrack Refining — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 exchangers by total energy consumption (MMBTU) over the last 12 months.
2. Show monthly trend of average Solomon Energy Efficiency Index for the trailing 12 months.
3. Which fired heaters have thermal efficiency below 70% and need tuning?
4. Top 10 process units by total CO2 emissions year-to-date.
5. Which heat exchangers have actual/clean UA ratio below 0.7 — candidates for cleaning?
6. How has heat recovery percentage trended month-over-month across the crude preheat train?
7. Which equipment categories have the highest average energy intensity per barrel?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
