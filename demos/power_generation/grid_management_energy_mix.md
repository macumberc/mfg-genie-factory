# PowerMix Dynamics — Demo Script

**Space:** Power Generation — PowerMix Dynamics - Grid Management & Energy Mix ⚡
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Trading + Dispatch Manager, Fleet Performance lead, CFO
**KPIs touched:** Capacity factor, Heat rate, Total generation, Curtailment, Reserve margin, Dispatch cost
**Big decision automated:** Which plants to dispatch versus curtail next week, which PPAs to renew versus exit, and how big the next battery-storage capex tranche needs to be to monetize today's curtailment.

---

## Pre-demo checklist

- Open the Genie space `PowerMix Dynamics - Grid Management & Energy Mix ⚡`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PowerMix Dynamics runs 20 plants spanning gas combined-cycle, coal steam, nuclear baseload, utility-scale solar, onshore and offshore wind, and three hydro stations — roughly 8 GW of nameplate across five operating regions. Today the merit-order ranking lives in the trading desk's day-ahead optimizer spreadsheet, the curtailment leakage in the Fleet Performance team's weekly Excel, and the heat-rate degradation trend in the Plant Engineering monthly. Three workbooks, same fleet, three different versions of which plants are 'on the bubble' — and the dispatch call and the next PPA renewal recommendation get shaped by whichever desk's number landed in the CEO's morning email. This space ends that. One governed surface where capacity factor, heat rate, curtailment, and reserve margin reconcile so the dispatch-versus-curtail call and the PPA-renew-versus-exit recommendation come from the same numbers.

---

## Key KPIs in scope

- Capacity factor (%) — fleet benchmark ~55% gas CCGT, ~90% nuclear, ~25% solar, ~35% onshore wind
- Heat rate (BTU/kWh) — thermal efficiency; CCGT best-in-class ~6,400, coal ~10,500
- Total generation (MWh) — top-line throughput by fuel type
- Curtailment (MWh) — lost renewable energy value
- Reserve margin (%) — NERC target 13-15%
- Dispatch cost ($/MWh) — merit-order and operating-margin input
- Forecast accuracy (%) — day-ahead market settlement risk
- Grid frequency deviation (Hz) — reliability and ancillary-services qualifier

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MW** | Megawatt |
| **NERC** | North American Electric Reliability Corporation |

---

## Act 1 — The signal — sizing the fleet mix and finding the under-dispatched units *(≈4 min)*

**Persona:** Dispatch Manager • **Job to be done:** Pull the next day-ahead merit order out of yesterday's generation data and name which units the trading desk should clear, hold in standby, or curtail.

*This is the moment the dispatch stack starts forming for the next clearing cycle. Two questions in, the dispatch manager has the fuel-mix delivery and the top capacity-factor performers ranked — that's the spine of the day-ahead bid.*

### Question (Act 1.1)

> **Show monthly total generation MWh by fuel type for the trailing 12 months.**

**What to say while it runs:** Monthly total_generation_mwh by fuel type is the merit-order context every trader needs before they bid. Watch the renewable share over the last 12 months — if Solar plus Wind plus Hydro is climbing toward 30%, the next dispatch question is less about who runs and more about who *doesn't* curtail.

**What to look for:** Monthly bars of total_generation_mwh stacked by fuel_type with `DATE_TRUNC('month', record_date)`. The widening or narrowing of the gas wedge against the renewables wedge is the strategic picture — that's the conversation the trading floor and the Fleet Performance lead have been having across two different spreadsheets.

**Land the point:** Now the dispatch manager can size the renewables-versus-thermal mix in seconds instead of waiting for the weekly fleet-mix workbook — that's the *which fuels carry tomorrow's load* call that used to need a Monday morning sync.

### Question (Act 1.2)

> **Top 10 plants by average capacity factor over the last 90 days.**

**What to say while it runs:** Top 10 plants by avg_capacity_factor over 90 days is the dispatched-economics ranking. Nuclear sits ~90%, CCGT ~55%, onshore wind ~35%, utility solar ~25% — anything significantly below benchmark is either a dispatch decision or a degradation flag, and the trading desk treats those two very differently.

**What to look for:** Ranked table — plant_name, fuel_type, avg_capacity_factor. The story is in the gas plants below 50% and the wind farms below 30% — those are the bottom of the merit order and the candidates for either a maintenance window or a PPA-renegotiation conversation.

**Land the point:** Right there is the merit-order tail the trading desk has to make a call on this week. Before this space, that list was rebuilt from raw SCADA every Sunday night for Monday's bid. Now it's the first question of the morning — and the dispatch-versus-standby call moves from gut-feel to ranking-driven.

---

## Act 2 — The decision — curtail, redispatch, or commit storage capex *(≈4 min)*

**Persona:** Fleet Performance Lead • **Job to be done:** Decide which plants get dispatched, which renewables get curtailed because the grid won't take them, and how much battery-storage capex is justified by the curtailment loss the fleet is already taking.

*Three questions that turn the day-ahead merit-order picture into the strategic capex commitment. The middle question is the anchor — the curtailment-to-dollars conversion that decides whether the next storage tranche gets sized in the tens or hundreds of MWh.*

### Question (Act 2.1)

> **Which fuel types had the highest curtailment last quarter, and what was the dispatch cost impact?**

**What to say while it runs:** Curtailment by fuel type last quarter is the *energy we couldn't sell* number — Solar and Wind dominate the column on a windy spring afternoon when load is low. Pair it with total_dispatch_cost and you have the leakage-to-spend ratio that justifies storage capex.

**What to look for:** A short table — fuel_type, total_curtailment_mwh, total_dispatch_cost. The renewables curtailment line is the one the Fleet Performance lead has been quoting from a spreadsheet for two years; here it reconciles to dispatch cost in one query.

**Land the point:** That curtailment number used to be the output of a half-day pull from the dispatch logs. Now it's the input to the *battery sizing* conversation that happens with the CFO at 10 AM Monday — the leakage line and the storage business case sit on the same screen.

### Question (Act 2.2)

> **How has average heat rate trended month-over-month for our gas and coal plants?**

**What to say while it runs:** Average heat_rate month over month for gas and coal plants is the thermal-efficiency picture. CCGT best-in-class is ~6,400 BTU/kWh, coal sits closer to 10,500 — anything north of 11,000 on a coal unit, or 7,500 on a CCGT, is the early-warning chart for a major-maintenance call or a unit-retirement candidate.

**What to look for:** Monthly trend of avg_heat_rate broken out by fuel_type for Gas and Coal only. Watch for the coal units climbing through 11,000 — those are the units the rating agencies and the IRP filing will both ask about.

**Land the point:** When the heat-rate trend is in the Fleet Performance lead's hand a quarter before the unit derates, the maintenance-versus-retirement call moves from reactive to strategic — and that's an IRP-shaping decision, not a maintenance ticket.

> **Anchor moment.** Stop on the curtailment-by-fuel table from the first question and the heat-rate trend on screen. Pick the worst renewable curtailment block — call it 20,000 MWh of solar and wind curtailment in the last quarter alone across the four worst plants.

> *At $40-50/MWh of foregone PPA revenue, 20,000 MWh of curtailment is roughly $800K-$1M per quarter, or $3-4M per year of leakage on those four plants. A 50 MWh four-hour battery tranche runs $50-80M of capex but recovers most of that curtailment plus captures roughly $100-200/MWh of peak-versus-off-peak spread on the other side — call it $5-8M of annual margin pickup. Payback inside seven years on storage that lives 15. Across the eight renewables plants in PowerMix's fleet, the storage business case isn't *do we build*; it's *which sites earn the first 100 MWh of capex*.*

> That's the decision this space automates. Not the slide. The decision. The battery-storage capex tranche gets sized from curtailment dollars actually leaking out today, not from a vendor's deck. The dispatch desk and the capital-planning desk close on the same artifact.

### Question (Act 2.3)

> **Which regions are running below a 13% reserve margin, and how often this year?**

**What to say while it runs:** Regions below the 13% NERC reserve-margin target are the reliability watchlist. Reserve margin under 10% is a PUC conversation; under 5% is an emergency-procedures conversation. The frequency-of-breach across the year is what the resource-adequacy filing actually needs.

**What to look for:** Reserve-margin breach count by region by month. The pattern matters more than the snapshot — a region breaching one week per quarter is seasonal; one breaching one week per month is a structural shortfall that needs new generation, new contracts, or new storage.

**Land the point:** That breach pattern is the difference between a footnote in the resource-adequacy filing and a $200M new-build recommendation. The reliability story now writes itself from operating data instead of forecasting models.

---

## Act 3 — The commitment — shaping next year's IRP and the PPA renewal book *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the fleet's resource mix to the board and the regulators, and commit to which PPAs get renewed, which get exited, and where the next storage tranche lands.

*The CFO doesn't need more dashboards; the CFO needs the same numbers the dispatch desk is already running on so the PPA-renewal recommendations and the IRP filing both reconcile to operating data.*

### Question (Act 3.1)

> **Top 10 plants by total dispatch cost USD year-to-date — and how does that compare to last year?**

**What to say while it runs:** Top 10 plants by total_dispatch_cost year-to-date paired with year-on-year change is the merit-order economics view. Plants where dispatch cost is climbing faster than fleet average are the renewal-versus-exit candidates — those are PPAs that either need a price renegotiation or a non-renewal letter.

**What to look for:** Ranked table of total_dispatch_cost with YoY delta by plant_name. The Coal units climbing fastest are the early-retirement candidates; the renewables with rising dispatch cost are the ones flagging O&M-contract slippage.

**Land the point:** When this list is on the CFO's screen in the same space the trading desk uses, the PPA portfolio gets reshaped on data rather than negotiation history — and the *which contracts roll off in 2027* conversation becomes a programmatic decision instead of a relationship call.

### Question (Act 3.2)

> **What is the monthly trend in renewable (Solar, Wind, Hydro) generation as a share of total fleet output?**

**What to say while it runs:** Monthly trend in renewables share of total fleet output is the decarbonization defense line. State-by-state RPS targets sit at 50-80% by 2030 for most jurisdictions PowerMix operates in — if the share is flat or falling, the IRP filing needs new renewable contracts; if it's climbing, the curtailment line in Act 2 becomes the binding constraint.

**What to look for:** Monthly share of (Solar + Wind + Hydro) over total fleet generation_mwh. The slope is the regulatory story — a rising line is RPS compliance; a flat line above 13% curtailment is a storage capex story.

**Land the point:** Triage at 8 AM on the dispatch desk, board narrative at 8 PM. Same space. Same numbers. The Fleet Performance lead's curtailment leakage and the CFO's IRP commitment are now the *same artifact* — and the board, the PUC, and the rating agencies all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PowerMix Dynamics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total generation MWh by fuel type for the trailing 12 months.
2. Top 10 plants by average capacity factor over the last 90 days.
3. Which fuel types had the highest curtailment last quarter, and what was the dispatch cost impact?
4. How has average heat rate trended month-over-month for our gas and coal plants?
5. Which regions are running below a 13% reserve margin, and how often this year?
6. Top 10 plants by total dispatch cost USD year-to-date — and how does that compare to last year?
7. What is the monthly trend in renewable (Solar, Wind, Hydro) generation as a share of total fleet output?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
