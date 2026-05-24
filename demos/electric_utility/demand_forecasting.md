# LoadCast Energy — Demo Script

**Space:** Electric Utility — LoadCast Energy - Demand Forecasting & Capacity Planning 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP T&D + CFO, Resource Planner, Load Forecaster
**KPIs touched:** Forecast MAPE, Reserve margin, Capacity margin, Load factor, Peak demand, Weather sensitivity score
**Big decision automated:** Sign off on the next 5-year T&D capex plan — which territories earn substation upgrades, which can defer with DER programs, and what reserve-margin number we defend to NERC and the PUC at the next rate case.

---

## Pre-demo checklist

- Open the Genie space `LoadCast Energy - Demand Forecasting & Capacity Planning 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> LoadCast Energy serves 20 service territories across five climate zones — hot-humid coast, hot-dry desert, cold north, temperate metro, mixed inland. Today the day-ahead MAPE lives in the Load Forecaster's R Markdown report, the territory peak-MW trajectory lives in the Resource Planner's PowerPoint, and the reserve-margin and EV/DER impact slides get rebuilt every IRP cycle for the CFO and PUC filings. Three workflows, three model versions in flight (v2.0, v2.1, v2.2), and a $200M-$500M T&D capex plan that gets signed off on a reserve-margin number that's two quarters out of date by the time it's defended. This space puts forecast MAPE by model version, territory peak demand, capacity margin, load factor, EV load, and behind-the-meter solar offsets in one governed surface — so the capex decision tracks the load shape that's actually happening.

---

## Key KPIs in scope

- Forecast MAPE (%) — short-term load forecast benchmark <3%, day-ahead <5%
- Reserve margin (%) — NERC reliability target typically 15-20% above peak
- Capacity margin (%) — available headroom for contingencies
- Load factor (%) — avg / peak; higher = more efficient asset utilization
- Peak demand (MW) — drives capacity planning and demand charges
- Weather sensitivity score — load-temp elasticity by territory
- EV load contribution (MW) — emerging demand driver
- Distributed solar offset (MW) — behind-the-meter generation reducing net load

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **MAPE** | Mean Absolute Percentage Error |
| **MW** | Megawatt |
| **NERC** | North American Electric Reliability Corporation |

---

## Act 1 — The signal — which forecast we're betting $300M of capex on *(≈4 min)*

**Persona:** Load Forecaster • **Job to be done:** Confirm the forecast model is accurate enough to be the basis for capacity decisions — and surface where it's not, before the IRP is filed.

*This is the conversation that should happen *before* the IRP draft circulates. Two questions tell the Load Forecaster whether v2.2 is ready for filing or whether the territory-by-territory error is hiding a systemic miss.*

### Question (Act 1.1)

> **Show monthly trend of average forecast error percentage by model version for the trailing 12 months.**

**What to say while it runs:** Monthly trend of avg_forecast_error_pct by model_version over 12 months. Short-term forecasts should run under 3% MAPE, day-ahead under 5%, monthly under 7%. v2.2 is the newest model — if its error trend is flat or rising vs. v2.1, we have a model-acceptance problem before we put it under the capex plan.

**What to look for:** Three lines, one per model version. The room should notice whether v2.2 is genuinely outperforming or whether v2.1 has been holding the line and v2.2 is a regression dressed up as progress.

**Land the point:** Now the Load Forecaster can defend the *model* choice on numbers, not on the most recent model-build memo — that's the IRP-input conversation that used to require three calibration runs and a slide deck.

### Question (Act 1.2)

> **Top 10 territories by maximum peak demand MW over the last 90 days.**

**What to say while it runs:** Top 10 territories by maximum peak_demand_mw over the last 90 days. Peak is what drives capacity planning and demand-charge revenue. The territories at the top of this list are the ones where the next substation upgrade gets funded — if the peak trajectory there is climbing faster than expected, the capacity-margin number is going to look uncomfortable.

**What to look for:** Ranked table: territory_name, max_peak_demand_mw, territory_type. Data Center Corridor and Sunbelt Towers typically lead this list — hyperscale and AC-driven peak.

**Land the point:** That list used to be the output of a half-day pulling SCADA peaks across 20 territories. Now it's the input to the substation-upgrade prioritization conversation — and the capex sequence gets set on actual peak, not on last year's load duration curve.

---

## Act 2 — The decision — where the next $300M of T&D capex goes, and what reserve margin we defend *(≈4 min)*

**Persona:** Resource Planner • **Job to be done:** Commit to the next 5-year capex sequence by territory and the reserve-margin number that backs it — with NERC reliability targets and PUC rate-case defensibility intact.

*Three questions convert the territory-peak signal and the DER offsets into a defensible capex order-of-magnitude. The middle question is the anchor — reserve-margin shortfall translated into capacity-MW that has to be funded.*

### Question (Act 2.1)

> **Which territories have the highest weather sensitivity score and what is their EV load contribution?**

**What to say while it runs:** Territories with the highest weather_sensitivity_score and their ev_load_mw contribution. Sensitivity above 7 means peak is heavily weather-driven — a hot summer pushes those territories first into capacity-margin trouble. EV load stacks on top; high sensitivity + high EV is the territory that needs both a substation upgrade AND a managed-charging program.

**What to look for:** Table: territory_name, weather_sensitivity_score, ev_load_mw, climate_zone. Hot-Humid and Hot-Dry residential territories typically dominate.

**Land the point:** Now the capex conversation has *two* dimensions — the substation upgrade AND the demand-side program. The Resource Planner can defend a $50M DER investment as a capex deferral, not as an ESG line item.

### Question (Act 2.2)

> **How has reserve margin trended month-over-month by territory type?**

**What to say while it runs:** Reserve_margin_pct trended month-over-month by territory_type. NERC reliability targets sit at 15-20% above peak. Anything under 15% is a tight-capacity flag; under 10% is a capacity-emergency declaration. The territory_types where margin is eroding are the ones the next IRP has to address.

**What to look for:** Monthly trend, avg reserve_margin by territory_type. Watch for the Urban and Industrial lines crossing below 15% — that's where the rate-case justification has to start.

**Land the point:** When this trend is in the Resource Planner's hand before the IRP draft, the conversation with the PUC moves from defensive ('explain your number') to programmatic ('here's the capex plan that gets us back to 17%').

> **Anchor moment.** Stop on the reserve-margin trend and the territory peak-demand leaderboard. Pick the worst-margin Urban territory — call it 12% reserve margin against a 17% NERC target, peak demand at 1,200 MW.

> *A 5-point reserve-margin shortfall on 1,200 MW of peak is 60 MW of capacity we need to add (or shave through DSM) before the next planning horizon. A new substation upgrade runs $1-5M per substation; covering 60 MW of capacity additions typically requires 4-6 substation upgrades plus transmission reinforcement — call it $30-50M per Urban territory. Across the three territories trending below NERC target, that's $100-150M of justified capex over five years — *and* the floor of the PUC ask. The downside of getting it wrong: NERC reliability violations carry penalties up to $1M per day per violation. One summer of forced load-shed at the wrong level and you're paying $30-100M in penalties before anyone breaks ground on the substation we should have built.*

> That's the decision this space automates. Capex sequence and reserve-margin commitment get set on the same screen as the day-ahead MAPE and the DER trajectory — not in an IRP appendix six months out of date. The 5-year T&D plan gets built on actual territory-peak data, not on last cycle's averaged forecast.

### Question (Act 2.3)

> **Top 10 territories by capacity margin shortfall — which are below the 15% NERC reliability target?**

**What to say while it runs:** Monthly trend of distributed_solar_mw and ev_load_mw over 12 months. Behind-the-meter solar is *negative* load on the grid; EV is *new* load. The net is whether the territory is getting easier or harder to serve. Solar growth ahead of EV growth is the rare case where capex can actually be deferred.

**What to look for:** Two-line trend: ev_load_mw climbing, distributed_solar_mw climbing or flat. The room should notice whether net DER impact is reducing or accelerating gross-load growth.

**Land the point:** That net-DER comparison is the difference between knowing a territory is growing and knowing it's growing in a way that *requires* more iron in the ground vs. one that can be programmed away.

---

## Act 3 — The commitment — IRP filing and rate-case defense *(≈4 min)*

**Persona:** VP T&D • **Job to be done:** Defend the capex plan to the CFO and the PUC — lock in which substations, which DSM programs, and what reserve-margin number we hold the line on.

*The VP isn't asking for new dashboards; they need the same MAPE, peak, reserve-margin, and DER numbers the planning team is acting on, in IRP and rate-case-ready form.*

### Question (Act 3.1)

> **What is the average load factor by climate zone, and how does it compare across territory types?**

**What to say while it runs:** Avg load_factor_pct by climate_zone and how it compares across territory_types. Load factor is avg/peak — the higher it is, the more efficiently we're sweating the existing assets. Industrial territories typically hit 70-80%; Urban residential under 50% means we're sizing for hours of peak each year, paying for the rest. That's the conversation about whether capex is the only lever, or whether time-of-use rate design pulls the load factor up cheaper.

**What to look for:** Climate_zone × territory_type matrix of load_factor_pct. The Urban residential / Hot-Humid cell typically shows the worst load factor — high peak, low average — which is exactly the territory where dynamic pricing has the most room to work.

**Land the point:** When the load factor is on the same screen as the reserve margin, the rate-case ask stops being 'fund the iron' and becomes 'fund the iron AND the program that defers the next round'. That's the regulator-facing story that earns trust.

### Question (Act 3.2)

> **Show monthly trend of distributed solar MW and EV load MW for the trailing 12 months.**

**What to say while it runs:** Top 10 territories by capacity_margin_pct shortfall — which are below the 15% NERC reliability target. This is the prioritization slide for the IRP. The territories in this list are the named investments; the territories *not* in this list are the deferral candidates.

**What to look for:** Ranked table: territory_name, avg capacity_margin_pct ascending. The room should notice which territories are *just* below 15% (programmable) vs. which are below 10% (must-build).

**Land the point:** Triage at 9, capex plan at noon, rate-case strategy at 4. Same space, same numbers. The Load Forecaster's MAPE check, the Resource Planner's territory ranking, and the VP T&D's PUC filing are now the same artifact — and the board gets one capex story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — LoadCast Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly trend of average forecast error percentage by model version for the trailing 12 months.
2. Top 10 territories by maximum peak demand MW over the last 90 days.
3. Which territories have the highest weather sensitivity score and what is their EV load contribution?
4. How has reserve margin trended month-over-month by territory type?
5. Top 10 territories by capacity margin shortfall — which are below the 15% NERC reliability target?
6. What is the average load factor by climate zone, and how does it compare across territory types?
7. Show monthly trend of distributed solar MW and EV load MW for the trailing 12 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
