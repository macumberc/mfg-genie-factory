# FreightSight Analytics — Demo Script

**Space:** Railroad — FreightSight Analytics - Freight Demand Forecasting 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Sales + Network Planning Director, Sales VP, CFO
**KPIs touched:** Total carloads, Freight revenue and revenue per carload, Forecast accuracy, Lane utilization, Average rate per car, Delayed-shipment rate
**Big decision automated:** Which 3-5 lanes to grow, which 2-3 to exit, where to put the next $50M of terminal capex, and which commodity-mix shift the network plan locks in for next year's operating ratio.

---

## Pre-demo checklist

- Open the Genie space `FreightSight Analytics - Freight Demand Forecasting 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FreightSight Analytics is a Class I rail planning surface covering 20 lanes across Intermodal, Coal, Chemicals, Agricultural, Automotive, Metals, Forest Products, and General merchandise. Today the carload-and-revenue trend lives in the Sales VP's RMI export, the lane utilization view sits in a Network Planning spreadsheet refreshed every Monday, and the forecast-accuracy / MAPE numbers come out of the data-science team's Jupyter notebook once a month. Three artifacts, same network — and the lane-exit decision, the intermodal-vs-carload mix call, and the terminal capex prioritization get made in three different rooms with three different versions of the truth. This space changes that. It puts the volume, the yield, and the model error in the same governed surface so the *grow / hold / exit* call on any lane is a one-question conversation, not a quarter-long planning cycle.

---

## Key KPIs in scope

- Total carloads — primary volume metric (carload + intermodal)
- Freight revenue ($) and revenue per carload — top-line and yield
- Forecast accuracy (MAPE %) — model quality, world-class rail forecasting ~3-5%, acceptable <10%
- Lane utilization (%) — capacity allocation efficiency
- Average rate per car ($) — pricing discipline by commodity
- Delayed-shipment rate (%) — service reliability for customers
- Demand trend mix (Growing / Stable / Declining / Volatile) — lane-level strategy signal
- Average transit days — service competitiveness vs truck

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MAPE** | Mean Absolute Percentage Error |

---

## Act 1 — The signal — separating real demand growth from forecast noise *(≈4 min)*

**Persona:** Network Planning Director • **Job to be done:** Find which commodities are actually moving versus which ones the forecast is just chasing — before the resource-allocation conversation starts.

*This is where the lane-strategy meeting begins. Two questions in, the planner has the commodity-trend picture and the top-revenue lanes ranked against each other, side by side.*

### Question (Act 1.1)

> **Show monthly total carloads by commodity for the trailing 12 months.**

**What to say while it runs:** Monthly total_carloads by commodity for the trailing 12 months. Coal is structurally declining 5-10% a year, intermodal is the growth lane, ag is weather-bound and lumpy. The shape of those curves is the shape of next year's resource plan. Anything diverging from those archetypes is either an opportunity or a problem.

**What to look for:** Stacked area or grouped bar by commodity. Watch for the inflection — the month intermodal crossed coal in carloads is the month the capex story changed.

**Land the point:** Before this space, that chart was rebuilt monthly for the Sales VP's executive review. Now it's the network planner's open — and the resource conversation about *which lanes get the locomotives next quarter* starts an hour earlier in the cycle.

### Question (Act 1.2)

> **Top 10 lanes by freight revenue over the last quarter.**

**What to say while it runs:** Top 10 lanes by freight revenue over the last quarter. Revenue concentration matters. If the top 3 lanes are 40% of revenue, that's a portfolio risk conversation; if it's 70%, that's a customer-concentration conversation. The Class I benchmark is roughly half of revenue in the top 10-15 lanes.

**What to look for:** Ranked table — lane_name, total_revenue. The shape of the distribution — flat or steep — is the strategic posture conversation.

**Land the point:** That ranking used to be the output of three days of RMI exports plus reconciliation. Now it's the input to the lane-strategy conversation — and the lanes at the top of that list are the ones we defend, the lanes at the bottom are the ones we look at again in act 2.

---

## Act 2 — The decision — grow, hold, exit, and where capacity goes *(≈4 min)*

**Persona:** Sales VP • **Job to be done:** Commit to a lane-by-lane grow / hold / exit posture for next year and signal where terminal capex goes.

*Three questions that turn lane trends into a capital and resource plan. The middle question is the anchor — the rate-per-car movement is the yield conversation that locks in pricing for the next contract cycle.*

### Question (Act 2.1)

> **Which commodities have the highest average forecast error (MAPE) over the last 6 months, and which need a model refresh?**

**What to say while it runs:** Commodities with the highest avg_forecast_error over the last 6 months. World-class rail forecasting is MAPE around 3-5%; anything north of 10% is a model that's costing us — under-forecasting means missed equipment, over-forecasting means stranded crews. The commodities at the top of this list are where we either retrain the model or change the planning assumption.

**What to look for:** Bar by commodity sorted by avg_forecast_error. The bars above 10% are the model-refresh queue; the bars above 20% are the *we cannot plan against this* conversation.

**Land the point:** When the data-science team and Network Planning both read forecast error from the same governed surface, the *should we refresh this model* conversation stops being a tickets-and-priorities debate. It becomes a yield conversation — every percentage point of MAPE on a $200M lane is real money.

### Question (Act 2.2)

> **How has the share of delayed shipments trended month-over-month by origin region?**

**What to say while it runs:** Top 10 lanes by avg_rate_per_car this month vs last quarter. This is the yield conversation. Rate per car is the pricing-discipline metric — lanes where it's drifting down without a contract change are leakage; lanes where it's holding above peer benchmark are the ones we put resources behind.

**What to look for:** Side-by-side bars — avg_rate_per_car this month vs last quarter, per lane. Lanes with declining rate but flat carloads are the leakage story; lanes with rising rate are the keepers.

**Land the point:** Now the Sales VP and the CFO are reading the same yield trend from the same surface. The lane-pricing conversation that used to be a six-week study is the answer to one question — and the contract-renewal posture for the next cycle gets set on Tuesday, not at the planning offsite.

> **Anchor moment.** Stop on the rate-per-car chart and the high-utilization growing-demand list together. Pick the top 3 lanes in the *Growing + over-utilized* segment — these are the lanes where adding capacity converts forecast revenue into booked carloads.

> *Call the top 3 lanes a combined 200,000 forecasted carloads next year at a $2,800 rate per car — that's $560M of top-line revenue at stake. A 1-point Operating Ratio improvement on a Class I is worth roughly $150-200M of EBIT against $12-14B of revenue, and capacity-led OR improvement is the cleanest version of it. Even capturing 10% incremental carloads on those three lanes — through siding investment and terminal capacity — is $50-60M of revenue at high incremental margin. Inversely, the 3 bottom lanes with Declining demand and avg_rate_per_car under benchmark are a $30-50M revenue exit and a 0.3-0.5 point OR improvement just from releasing the equipment.*

> That is the lane-portfolio decision this space automates. The capex list and the exit list come out of the same question set, ranked on dollars and OR points — not on which Sales Director made the loudest case at the planning offsite.

### Question (Act 2.3)

> **Top 10 lanes by average rate per car this month, and how does that compare to last quarter?**

**What to say while it runs:** Lanes flagged as Growing demand with utilization_pct above 90%, and their forecasted_revenue_usd. Utilization above 90% with Growing demand is where capacity becomes the binding constraint — those are the lanes that earn the next siding, the next terminal expansion, or the next intermodal lift.

**What to look for:** Filtered table — lane_id, demand_trend = 'Growing', utilization_pct > 90, forecasted_revenue. That short list is the terminal-capex prioritization view for next year's plan.

**Land the point:** That table is the capex prioritization slide the planning team used to spend three weeks building. Now it's a question — and the conversation about *where does the next $50M go* moves from a planning study to a one-meeting decision.

---

## Act 3 — The commitment — locking in the network plan and the model investment *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the operating ratio commitment to the board and lock the capex envelope behind the lane plan.

*The CFO doesn't need another dashboard; they need the lane economics, the forecast credibility, and the service reliability in one surface — that's the operating-ratio story.*

### Question (Act 3.1)

> **Which lanes are flagged as Growing demand with utilization above 90%, and what is their forecasted revenue?**

**What to say while it runs:** Share of delayed shipments month over month by origin region. Service reliability is the lane-loss leading indicator — if delays are climbing in a region, the revenue follows downward within two contract cycles. This is the chart the CFO uses to size the service-recovery investment.

**What to look for:** Monthly trend of delayed_count / shipment_count by origin_region. Regions where the line is climbing are revenue-at-risk; the dollars are the next chart over.

**Land the point:** When service reliability and lane revenue live in the same governed surface, the conversation about *do we invest in network velocity or pricing* becomes a number, not an instinct. The investment case for the operations group writes itself out of this view.

### Question (Act 3.2)

> **Show monthly forecasted versus actual carloads by commodity to identify systematic over- or under-forecasting bias.**

**What to say while it runs:** Monthly forecasted vs actual carloads by commodity. Systematic bias is the killer here — a model that's been over-forecasting coal for 9 months has been parking equipment we should have redeployed to intermodal. This is the chart that justifies either a model refresh or a planning override.

**What to look for:** Dual line per commodity — total_forecasted_carloads vs total_actual_carloads. The persistent gap is the policy decision; one-month gaps are noise.

**Land the point:** Same space the network planner used at the start. Same numbers. The lane plan, the model investment, and the OR commitment are now the *same artifact* — and the board gets one story about freight strategy, not three reconciled decks.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FreightSight Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total carloads by commodity for the trailing 12 months.
2. Top 10 lanes by freight revenue over the last quarter.
3. Which commodities have the highest average forecast error (MAPE) over the last 6 months, and which need a model refresh?
4. How has the share of delayed shipments trended month-over-month by origin region?
5. Top 10 lanes by average rate per car this month, and how does that compare to last quarter?
6. Which lanes are flagged as Growing demand with utilization above 90%, and what is their forecasted revenue?
7. Show monthly forecasted versus actual carloads by commodity to identify systematic over- or under-forecasting bias.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
