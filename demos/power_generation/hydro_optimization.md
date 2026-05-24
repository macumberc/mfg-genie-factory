# HydroFlow Energy — Demo Script

**Space:** Power Generation — HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Hydro Operations + Plant Manager, Hydrologist, CFO
**KPIs touched:** Turbine efficiency, Capacity factor, Water flow rate, Hydraulic head, Reservoir storage, Spill volume
**Big decision automated:** Whether to spill water now or hold it for peak pricing, which dams enter drought-conservation dispatch, and which turbines earn the next retrofit capex tranche.

---

## Pre-demo checklist

- Open the Genie space `HydroFlow Energy - Hydro Optimization & Reservoir Mgmt 💧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> HydroFlow Energy operates 20 turbines across 10 dams — six Francis units on canyon storage projects, six Kaplan units on river run-of-river, four Pelton high-head, and four Bulb units in tidal/low-head sites. Today the turbine-efficiency curves live in a Plant Manager's commissioning notebook, the inflow-versus-outflow balance lives in the Hydrologist's water-balance spreadsheet, and the drought-risk forward look sits in the trading desk's hedge-book workbook. Three artifacts, same 20 turbines, three different versions of how much water is on the table — and the spill-versus-hold call and the retrofit-capex priority both get made on whichever workbook the dispatcher saw last. This space ends that. One governed surface where efficiency, hydraulic head, storage percentage, and drought-risk band reconcile so the operations-meets-trading conversation finally happens on the same numbers.

---

## Key KPIs in scope

- Turbine efficiency (%) — Francis ~93-95%, Kaplan ~90-94%, Pelton ~90-92%, Bulb ~87-93%
- Capacity factor (hydro) — fleet target ~40%; varies with hydrology
- Water flow rate (m³/s) — dispatch headroom indicator
- Hydraulic head (m) — site-specific power potential driver
- Reservoir storage (%) — days-of-generation buffer
- Spill volume (m³) — unrecoverable energy loss
- Environmental flow compliance — regulatory and ESG metric
- Drought-risk band — forward generation risk

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **ESG** | Environmental, Social, Governance |

---

## Act 1 — The signal — sizing fleet output and finding the efficiency outliers *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Pull tomorrow's dispatchable hydro generation out of yesterday's turbine and flow data, and name the units that are running off-curve.

*This is the moment the dispatch curve and the maintenance queue both start to take shape for the week. Two questions in, the Plant Manager has the fleet-mix picture and the efficiency outliers ranked.*

### Question (Act 1.1)

> **Show monthly total hydro generation MWh by turbine type for the trailing 12 months.**

**What to say while it runs:** Monthly total_generation_mwh by turbine_type for the trailing 12 months is the seasonality story every hydro engineer is reading first — Francis units climb hard in the April-June snowmelt window, Pelton units smooth across the year on high-head reservoirs. If the spring peak is muted relative to last year, the drought conversation has already started without anybody saying the word.

**What to look for:** Monthly bars of total_generation_mwh stacked by Francis / Kaplan / Pelton / Bulb with `DATE_TRUNC('month', record_date)`. The shape of the spring shoulder is the hydrology signal — flatter than last year is the first chart in the drought-risk briefing.

**Land the point:** Now the Plant Manager can size fleet delivery against last year's hydrology in seconds instead of waiting for the monthly water-balance workbook — that's the *what's our water year going to look like* call that used to require the Hydrologist to compile the snowmelt sheet first.

### Question (Act 1.2)

> **Top 10 turbines by average efficiency percentage over the last 90 days.**

**What to say while it runs:** Top 10 turbines by avg_efficiency_pct over 90 days is the off-curve list. Francis benchmark is 93-95%, Kaplan 90-94%, Pelton 90-92%, Bulb 87-93% — anything 3 points below benchmark for sustained periods is a wear flag, a runner-blade fouling issue, or a head loss the engineering team needs to investigate before the next refueling window.

**What to look for:** Ranked table — turbine_name, turbine_type, avg_efficiency_pct. The bottom of the table is the retrofit-candidate list; the spread between top and bottom of the same turbine_type is the *recoverable efficiency* line item the CFO will ask about.

**Land the point:** Right there is the retrofit-prioritization conversation. Before this space, that list was rebuilt from runner-blade inspections quarterly. Now it's a one-line question — and the *which turbine earns the next $10M of capex* conversation starts from operating data, not anecdote.

---

## Act 2 — The decision — spill, hold, conserve, or retrofit *(≈4 min)*

**Persona:** Hydrologist • **Job to be done:** Decide which dams enter conservation-dispatch mode, which spill water this week because storage is at capacity, and which turbines get pulled offline for the retrofit window.

*Three questions that turn the fleet-mix and efficiency picture into the strategic water-management call. The middle question is the anchor — the spill-volume-to-dollars conversion that decides whether the engineering team wins a multi-turbine retrofit AFE.*

### Question (Act 2.1)

> **Which dams are currently at High or Severe drought risk, and what is their average days of storage?**

**What to say while it runs:** Dams sitting in High or Severe drought_risk with their avg_days_of_storage on the same row is the conservation-dispatch trigger view. Under 30 days of storage at any dam moves operations into conservation mode — daytime peaking only, no off-peak dispatch — which is a different revenue profile entirely.

**What to look for:** A short table — dam_name, drought_risk band, avg_days_of_storage, avg_storage_pct. The Highland and Summit dams (Pelton sites, smaller reservoirs) are where this typically lights up first; Eagle Falls and Cascade can buffer longer but are the canary for a multi-year dry trend.

**Land the point:** When the conservation-mode list lands on the dispatcher's screen the morning the storage line crosses 30 days, the revenue defense moves from reactive to programmatic — and the *hold-for-peak* discipline is enforced by the system, not by a Slack message from the Hydrologist.

### Question (Act 2.2)

> **How has total spill volume trended month-over-month, and which dams contribute most?**

**What to say while it runs:** Monthly trend in total_spill_volume by dam is the *energy we threw away* chart. Every cubic meter that goes over the spillway during a high-flow event is a turbine-hour of unrecoverable generation. The dams with the worst spill ratios are the candidates for either a runner upgrade or an upstream storage agreement.

**What to look for:** Monthly bars of total_spill_volume broken out by dam_name. Watch for the spring spike — that's when the snowmelt outpaces turbine capacity and water leaves through the spillway instead of the runner.

**Land the point:** That spill number used to live in a Hydrologist's spreadsheet and surface once a year in the AFE review. Now it's the *which turbine retrofit gets funded* anchor — when the spill volume converts to a revenue number, the runner upgrade pencils out or it doesn't.

> **Anchor moment.** Stop on the monthly spill-volume trend on screen. Pick the worst-spilling dam — call it Eagle Falls with 200,000 m³ of spillover during the snowmelt peak, on a site whose two Francis units carry 60% of that complex's annual generation.

> *Eagle Falls' 200,000 m³ at ~30 meters of head converts to roughly 15,000 MWh of foregone generation. At a peak-versus-off-peak spread of $50/MWh — modest, defensible — that's $750K of revenue left on the spillway in a single snowmelt season. A runner retrofit on those two Francis units runs $8-12M of capex with a 3-5 point efficiency lift; if that gains 4% on the dispatched MWh and recovers half the spill, the payback sits at 5-7 years on assets that live another 30. Across HydroFlow's six Francis-equipped dams, the retrofit AFE story isn't *can we justify*; it's *which two dams earn the first $20M*.*

> That's the decision this space automates. Not the slide. The decision. The retrofit AFE gets ranked on spill-driven dollars, not on equipment age — and the Plant Manager's runner case and the Hydrologist's water-balance case land in the same artifact.

### Question (Act 2.3)

> **Which flow readings show environmental flow non-compliance this year, and at which dams?**

**What to say while it runs:** Environmental flow non-compliance by dam and reading_date is the FERC-license risk view. Even a handful of Non-Compliant readings per year compounds into a license-amendment conversation and potential cease-dispatch orders. The pattern — which dams, what time of year — is what the compliance briefing actually needs.

**What to look for:** Flow readings where env_flow_compliance = 'Non-Compliant' grouped by dam_name with monthly counts. Concentrated breaches at one dam are an instrumentation or operational issue; spread across multiple dams in the dry season is a structural water-allocation problem.

**Land the point:** That compliance distribution used to surface in the FERC annual filing two months after the fact. Now the Hydrologist sees it the same week it happens — and the *do we adjust the dispatch curve or contest the gauge calibration* conversation actually happens in time to matter.

---

## Act 3 — The commitment — drought hedge and the multi-year retrofit AFE *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the hydro portfolio's contribution to fleet operating margin and lock in the multi-year retrofit AFE and drought-hedge book.

*The CFO doesn't need more dashboards; the CFO needs the same numbers the Hydrologist is using so the hedge-book defense at the board references operating reality, not a forward curve.*

### Question (Act 3.1)

> **Top 10 dams by total water level meters this quarter — and how does that compare to last quarter?**

**What to say while it runs:** Top 10 dams by total water_level_m this quarter with quarter-over-quarter delta is the storage-trajectory ranking. Dams losing storage faster than the fleet average are the leading indicator on next year's generation guide — and that's the conversation the trading desk needs before they layer in the hedge book.

**What to look for:** Ranked table of total_water_level_m by dam_name with prior-quarter delta. The dams with declining storage paired with high drought-risk band from Act 2 are the names the CFO needs to land in the board hedge defense.

**Land the point:** When the storage trajectory is on the CFO's screen with the same numbers the dispatcher acts on, the hedge book gets sized on operating reality — and the *how much fixed-price revenue we commit for next year* call stops being a forecasting exercise and starts being a position-management one.

### Question (Act 3.2)

> **What is the monthly trend in average reservoir storage percentage across the fleet?**

**What to say while it runs:** Monthly trend in avg_storage_pct across the fleet is the multi-year water-resource picture. The slope across consecutive years is the dry-trend signal — if average fleet storage is sliding 3-5 points year on year, the capex picture has to shift from runner retrofits to pumped-storage augmentation or off-season storage agreements.

**What to look for:** Monthly fleet-average storage_pct over 24+ months. The inflection points are the budget-cycle pivot moments; flat or declining across multiple years is a structural call the CFO has to land with the board.

**Land the point:** Triage in the morning dispatch room, capex commitment at the next quarterly board meeting. Same space, same numbers. The Plant Manager's retrofit list and the CFO's hedge defense are now the *same artifact* — and the board, the FERC filing, and the trading desk all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — HydroFlow Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total hydro generation MWh by turbine type for the trailing 12 months.
2. Top 10 turbines by average efficiency percentage over the last 90 days.
3. Which dams are currently at High or Severe drought risk, and what is their average days of storage?
4. How has total spill volume trended month-over-month, and which dams contribute most?
5. Which flow readings show environmental flow non-compliance this year, and at which dams?
6. Top 10 dams by total water level meters this quarter — and how does that compare to last quarter?
7. What is the monthly trend in average reservoir storage percentage across the fleet?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
