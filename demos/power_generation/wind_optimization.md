# WindPeak Energy — Demo Script

**Space:** Power Generation — WindPeak Energy - Wind Farm Optimization 💨
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Wind Operations + Turbine Engineer, Plant Manager, Trading desk / CFO
**KPIs touched:** Capacity factor, Turbine availability, Power curve deviation, Wake loss, Wind speed, Curtailment
**Big decision automated:** Whether each underperforming turbine earns a pitch/yaw retrofit, a blade replacement, or a full repower — and how the curtailment loss reshapes next year's PPA hedge book.

---

## Pre-demo checklist

- Open the Genie space `WindPeak Energy - Wind Farm Optimization 💨`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> WindPeak Energy operates 20 turbines across multiple wind farms — a mix of legacy 1.5-2.0 MW machines and newer 3.5-4.5 MW units, typically 60-100 MW of nameplate across three to five sites. Today the daily capacity-factor and wind-speed picture lives in a Turbine Engineer's SCADA monitoring system, the power-curve-deviation and vibration trend lives in the OEM's condition-monitoring portal, and the day-ahead-versus-actual MWh reconciliation lives in the Trading desk's settlement spreadsheet. Three artifacts, same 20 turbines, three different versions of *which turbines are off-curve* — and the retrofit-versus-repower call and the next PPA hedge get shaped by whichever workbook landed in the Plant Manager's email first. This space ends that. One governed surface where capacity factor, power-curve deviation, curtailment, and PPA revenue reconcile so the lifecycle-capex call and the day-ahead settlement defense both come from the same numbers.

---

## Key KPIs in scope

- Capacity factor (%) — onshore wind benchmark ~35%, offshore ~45%
- Turbine availability (%) — IEC 61400-26 target >97%
- Power curve deviation (%) — degradation or wake-loss indicator
- Wake loss (%) — typical 5-15% across a wind farm
- Wind speed (m/s) — primary dispatch driver; cut-in ~3 m/s, rated ~12 m/s
- Curtailment (MWh) — grid-imposed losses
- Forecast accuracy — PPA settlement risk
- Vibration level (g) — leading indicator of gearbox/bearing failure

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **PPA** | Power Purchase Agreement |

---

## Act 1 — The signal — finding the off-curve turbines and the underperforming farms *(≈4 min)*

**Persona:** Turbine Engineer • **Job to be done:** Pull tomorrow's pitch-and-yaw calibration list out of yesterday's SCADA and condition-monitoring data, and name the turbines whose power curve has slid out of the manufacturer band.

*This is the moment the daily condition-monitoring stops being a portal-by-portal scroll and becomes a one-screen ranking. Two questions in, the Turbine Engineer has the farm-level yield picture and the capacity-factor outlier list.*

### Question (Act 1.1)

> **Show monthly total wind generation MWh by wind farm for the trailing 12 months.**

**What to say while it runs:** Monthly total wind generation_mwh by wind_farm for the trailing 12 months is the comparative yield read every wind engineer opens with. Farms with similar nameplate that diverge over the year are either wake-loss, terrain, or aging-fleet stories — and the year-over-year compare points to whether the divergence is structural or one-off.

**What to look for:** Monthly bars of total_generation_mwh stacked by wind_farm with `DATE_TRUNC('month', record_date)`. Look for the autumn-winter peak — that's when onshore-Midwest farms typically carry the fleet; if a farm that historically led in that window slid, the conversation has already started.

**Land the point:** Now the Turbine Engineer can size farm-level performance against historical baseline in seconds instead of running comparative pulls in the OEM portal — that's the *which farm dragged the fleet this season* conversation that used to need a Saturday spent stitching SCADA exports.

### Question (Act 1.2)

> **Top 10 turbines by average capacity factor over the last 90 days.**

**What to say while it runs:** Top 10 turbines by avg_capacity_factor over 90 days is the off-curve ranking. Onshore benchmark sits around 35%, offshore closer to 45%. Turbines materially below benchmark are either under-bid by the dispatch desk, hitting wake from neighbors, or running through pitch-yaw drift or blade degradation — and the bottom of the list is the retrofit-candidate shortlist.

**What to look for:** Ranked table — turbine_name, wind_farm, avg_capacity_factor. The spread between the top and bottom of the same farm is the *recoverable performance* line; if the worst three turbines on a farm sit 8 points below the leaders, that's a real capex-recovery story.

**Land the point:** Right there is the retrofit shortlist. Before this space, that list was the output of cross-referencing SCADA against the OEM condition-monitoring portal once a quarter. Now it's the first question of the morning — and the *which turbine earns the next retrofit window* conversation starts from data, not from vendor recommendations.

---

## Act 2 — The decision — retrofit, blade replacement, or repower *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Decide which turbines get a pitch/yaw retrofit window, which need a full blade replacement, and which legacy machines move onto the repower study list ahead of the next IPP capital cycle.

*Three questions that turn the off-curve ranking into a defensible lifecycle-capex recommendation. The middle question is the anchor — the curtailment-versus-revenue conversion that decides whether the next $10-30M of plant capex goes to retrofits or to a full repower study.*

### Question (Act 2.1)

> **Which wind farms had the largest gap between forecasted and actual MWh this quarter?**

**What to say while it runs:** Wind farms with the largest gap between forecasted and actual MWh this quarter is the day-ahead-settlement risk view. Forecast accuracy is the binding PPA-settlement constraint; a farm running a consistent under-delivery against the day-ahead curve is taking imbalance penalties every clearing — and that's a dispatch-desk conversation as much as a turbine-engineering one.

**What to look for:** A short table — wind_farm, total_forecasted_mwh, total_actual_mwh, delta. Farms with a persistent shortfall in the same direction are the ones costing the Trading desk imbalance dollars; farms with a wide variance in both directions are an instrumentation or forecast-model issue.

**Land the point:** That settlement-gap rollup used to live in the Trading desk's spreadsheet and surface in the monthly reconciliation. Now it's a one-line query the Plant Manager and the Trading desk see the same week — and the *do we retune the forecast or fix the asset* call happens in time to matter for the next PPA-renewal cycle.

### Question (Act 2.2)

> **How has total curtailment MWh trended month-over-month, and what is the implied revenue loss?**

**What to say while it runs:** Turbines with sustained power_curve_deviation above 5% or vibration_level_g above 0.7g is the *condition-monitoring-meets-economics* watchlist. Power-curve deviation above 5% sustained is either aerodynamic — blade soiling, leading-edge erosion — or mechanical — drivetrain wear, pitch-system drift. Vibration above 0.7g is a leading indicator on gearbox or main-bearing failure that, untreated, ends with a $1-2M unplanned event.

**What to look for:** Turbines filtered to power_curve_deviation_pct > 5 OR vibration_level_g > 0.7. The combination matters; a turbine that's both off-curve *and* vibrating is the must-do retrofit; vibration alone is the watch-and-walk-down list; deviation alone is the cleaning-and-retune candidate.

**Land the point:** When this list is in the Plant Manager's hand a quarter before the gearbox actually fails, the maintenance-versus-retrofit-versus-replacement call moves from reactive to scheduled — and the *which turbines get the crane window* conversation becomes a planned commitment instead of a war-room scramble.

> **Anchor moment.** Stop on the off-curve watchlist and the curtailment trend on screen. Pick the worst cluster — call it three turbines on one farm running 6-7% power-curve deviation with vibration drifting toward 0.8g, while the farm itself is taking 1,500 MWh of curtailment per quarter.

> *Three turbines at 6-7% power-curve deviation is roughly 5-8% of nameplate generation foregone — call it 1,500 MWh per quarter combined, or 6,000 MWh per year. At a PPA price of $40-50/MWh, that's $240-300K per year just on the deviation. Add another 6,000 MWh of curtailment on the same farm at the same price — another $240-300K. A pitch-and-yaw retrofit on those three turbines runs $200-500K with a 2-3 percentage point recovery, payback inside two years. A full blade replacement runs $300-500K per turbine plus 2-5 days of downtime each — call it $1-1.5M for the three and a 3-4 year payback. A full repower of the worst legacy machines, at $2-3M per MW and a 25-50% capacity-factor lift, sits at $10-30M of capex with payback in the 6-9 year window. Across the WindPeak fleet of 20 turbines, the retrofit-versus-repower call isn't *can we justify*; it's *which three turbines earn the first $1.5M and which farm enters the repower study*.*

> That's the decision this space automates. Not the slide. The decision. The retrofit AFE gets ranked on power-curve dollars and curtailment dollars actually leaking out today, not on vendor brochures — and the Turbine Engineer's condition-monitoring list and the Plant Manager's lifecycle AFE land in the same artifact.

### Question (Act 2.3)

> **Which turbines show sustained power curve deviation above 5% or vibration above 0.7g this year?**

**What to say while it runs:** Monthly trend in total_curtailment_mwh is the *energy we couldn't sell* picture, paired with the implied revenue loss at PPA price. Curtailment in wind is grid-driven — the grid couldn't take the energy at that moment — but the trajectory tells you whether the bottleneck is structural or seasonal, and whether storage co-location is the answer or whether a different PPA structure is.

**What to look for:** Monthly total_curtailment_mwh by wind_farm with the PPA-price overlay. Watch for the spring shoulder seasons — that's when curtailment typically spikes on midwest wind farms, and the dollars-per-MWh on the unbuilt energy add up fast.

**Land the point:** That curtailment number used to surface in the quarterly Operations review. Now it's a live anchor for the *do we co-locate storage or renegotiate the interconnection* conversation — which is a multi-million-dollar capex framing, not an operations footnote.

---

## Act 3 — The commitment — PPA hedge book and the multi-year repower study *(≈4 min)*

**Persona:** Trading desk / CFO • **Job to be done:** Defend the wind portfolio's PPA-settlement performance to the off-takers and the board, and lock in the multi-year repower-versus-retrofit capex program.

*The Trading desk and the CFO don't need more dashboards; they need the same numbers the Plant Manager is acting on so the PPA-renewal pitch and the repower-AFE defense both reconcile to operating data.*

### Question (Act 3.1)

> **Top 10 wind farms by total revenue USD year-to-date — and how does that compare to last year?**

**What to say while it runs:** Top 10 wind farms by total revenue_usd year-to-date with year-over-year comparison is the portfolio-economics view. Farms where revenue is growing on the same nameplate are operating discipline wins; farms where revenue is sliding despite a flat year on wind speed are the PPA-renegotiation or repower-study candidates.

**What to look for:** Ranked table of total revenue by wind_farm with YoY delta. The trajectory matters more than the level; a smaller farm with rising revenue is shaping the next PPA renewal favorably, while a larger farm with declining revenue is the repower study that needs to start now to land in the next budget cycle.

**Land the point:** When this list lands in the same space the Plant Manager and the Trading desk just used, the PPA-renewal recommendation and the repower-study green-light land in one conversation — and the *which farms earn the next $50-150M of capex* call becomes a programmatic ranking instead of a vendor competition.

### Question (Act 3.2)

> **What is the monthly trend in average wind speed across all turbines, by farm?**

**What to say while it runs:** Monthly trend in avg_wind_speed across all turbines, broken out by farm, is the resource-quality baseline that anchors the hedge book and the repower business case. A flat or rising wind resource against declining performance is unambiguous — the asset is the problem. A declining wind resource needs a more careful read; that's a hedge-book conversation and a forward-curve repricing.

**What to look for:** Monthly avg_wind_speed_ms by wind_farm over 24+ months. The slope is the resource story; pair it with the capacity-factor trend from Act 1 to separate weather-driven softness from asset-driven softness.

**Land the point:** Morning condition-monitoring sweep, settlement reconciliation on the trading floor, repower AFE at the next board meeting. Same space, same numbers. The Turbine Engineer's retrofit list, the Plant Manager's lifecycle-capex AFE, and the CFO's hedge-book defense are now the *same artifact* — and the off-takers, the rating agencies, and the board all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — WindPeak Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total wind generation MWh by wind farm for the trailing 12 months.
2. Top 10 turbines by average capacity factor over the last 90 days.
3. Which wind farms had the largest gap between forecasted and actual MWh this quarter?
4. How has total curtailment MWh trended month-over-month, and what is the implied revenue loss?
5. Which turbines show sustained power curve deviation above 5% or vibration above 0.7g this year?
6. Top 10 wind farms by total revenue USD year-to-date — and how does that compare to last year?
7. What is the monthly trend in average wind speed across all turbines, by farm?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
