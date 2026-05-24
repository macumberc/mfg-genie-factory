# DistroForecast Systems — Demo Script

**Space:** Industrial Distribution — DistroForecast Systems - Demand Forecasting & Backlog 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Supply Chain + CFO, Category Manager, Supply Planner
**KPIs touched:** Forecast accuracy / MAPE, Fill rate, Order backlog units and open-order value, Backorder rate, Lead time, Forecast bias
**Big decision automated:** Which 5-10 SKUs get expedited via air freight this week vs. accept the backorder, and which customer tiers earn a guaranteed-fill service-level commitment going into next year's contract cycle.

---

## Pre-demo checklist

- Open the Genie space `DistroForecast Systems - Demand Forecasting & Backlog 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> DistroForecast Systems forecasts demand across 20 industrial SKUs in fasteners, bearings, valves, electrical, and safety — serving MRO, OEM, contractor, and government segments with line-fill commitments at 97% on the contracted accounts. Today the forecast accuracy lives in a Supply Planner's monthly bias report, the open-order backlog lives in a Category Manager's daily SQL extract, and the customer-tier service-level number is a quarterly slide built by the CFO's office. Three artifacts, one order book — and when a key OEM account calls at 9 AM asking why their bearings order is 12 days late, the answer takes an hour to assemble and lands without a recovery plan attached. This space ends that. One governed surface that turns yesterday's forecast-vs-actual into the *expedite-these-5, backorder-those-3, lock-the-tier-1-service-level* decision before the customer call queue fills up.

---

## Key KPIs in scope

- Forecast accuracy / MAPE (%) — best-in-class industrial distributors run 10-20% MAPE
- Fill rate (%) — line/case-fill target ≥97% for MRO distribution
- Order backlog units and open-order value ($) — working-capital and revenue-at-risk signal
- Backorder rate (%) — lost-sales and customer-churn leading indicator
- Lead time (days) — commitment vs. actual time-to-ship
- Forecast bias (units) — systematic over/under-forecasting by category
- Customer satisfaction score (1-5) — service-level outcome
- Days-to-ship — fulfillment cycle metric

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MAPE** | Mean Absolute Percentage Error |
| **MRO** | Maintenance, Repair & Overhaul |
| **SKU** | Stock Keeping Unit |

---

## Act 1 — The signal — finding the forecast misses and the at-risk revenue *(≈4 min)*

**Persona:** Category Manager • **Job to be done:** Locate the categories where the forecast is structurally off and the open-order revenue at risk — before the customer escalations land.

*This is the first 20 minutes of a real category review. Two questions in, the Category Manager has the bias map and the revenue exposure that used to take a half-day of cross-system pulls.*

### Question (Act 1.1)

> **Show monthly total order revenue by product category for the trailing 12 months.**

**What to say while it runs:** Monthly total order revenue by product category for the trailing 12 months. This is the topline read on what's actually flowing — and whether the forecasted mix is the mix the customers are buying. Categories where the revenue line bent down without a price drop are categories where we're losing share, not just demand.

**What to look for:** Monthly bars on `total_order_revenue` by `product_category` — `DATE_TRUNC('month', order_date)`. Look for the category where the line bent — that's the forecast model's blind spot.

**Land the point:** That picture used to take the Category Manager an hour in Excel every Monday. Now it's the first chart of the day — and the category review starts on the right SKUs instead of last month's leftovers.

### Question (Act 1.2)

> **Which product categories have the worst forecast accuracy (highest avg forecast error) over the last 6 months?**

**What to say while it runs:** Categories with the worst forecast accuracy over the last 6 months. Best-in-class industrial distribution runs 10-20% MAPE; anything above 25% is a category where the planning system is essentially guessing. The dollars-at-risk follow the accuracy gap directly.

**What to look for:** Ranked categories by `avg_forecast_error`. The categories with the worst MAPE are where the model retraining or the demand-sensing investment lands first.

**Land the point:** That's the model-investment prioritization conversation. The Supply Planner walks into the next IT prioritization with the specific categories where forecast accuracy is structurally bad — not a heat map, a ranked list with dollars.

---

## Act 2 — The decision — expedite, backorder, or lose the line *(≈4 min)*

**Persona:** Supply Planner • **Job to be done:** Decide which SKUs get expedited air freight this week, which accept the backorder, and which OEM accounts get a recovery call before they escalate.

*Three questions that turn the forecast-miss inventory into a defensible expedite-vs-backorder commitment. The middle question is the anchor — the backorder-revenue to expedite-cost conversion that decides where the freight dollars go.*

### Question (Act 2.1)

> **Top 10 SKUs by open order value USD this week — and what is their fill rate?**

**What to say while it runs:** Top 10 SKUs by open order value with their current fill rate. Open-order value is the at-risk revenue if we miss the ship window; fill rate is whether we're actually shipping what we promised. SKUs with high open-order value and a sub-90% fill rate are the SKUs that drive the expedite-vs-backorder call.

**What to look for:** Ranked top-10 on `open_order_value_usd` with `fill_rate_pct` beside. The top 2-3 SKUs with low fill rates are this week's expedite shortlist.

**Land the point:** That table is the actual expedite shortlist for Monday's logistics call. The Supply Planner makes the air-vs-truck decision on dollars-at-stake, not on whoever called the sales rep last.

### Question (Act 2.2)

> **How has the monthly backordered order count trended across customer segments?**

**What to say while it runs:** Monthly backordered order count trended across customer segments. The segment with rising backorders is the segment where the next renewal conversation gets ugly. MRO can usually absorb a 2-day slip; OEM cannot — a missed bearings ship costs them line-down time at $5-50K per hour.

**What to look for:** Monthly trend on `backordered_count` split by `customer_segment`. Watch the OEM line — that's the segment with the worst chargeback economics if it climbs.

**Land the point:** Customer-tier risk used to be discovered when the account manager called from a customer site. Now the segment-level backorder trend is the same artifact the Supply Planner uses Monday morning — and the OEM recovery plan goes out *before* the escalation call comes in.

> **Anchor moment.** Stop on the top-10 open-order-value list and the OEM backorder trend on screen. Pick the worst case — say a tier-1 OEM with $400K open-order value on 5 bearing SKUs running at 85% fill rate.

> *Industrial SKU stockouts on a tier-1 OEM cost 5-10% in margin loss plus a customer-tier penalty in the $5-50K range per chargeback event — call it $40K of direct exposure on that account this week. Air-expedite freight on the at-risk lines runs $500-2K per order vs. $50-200 standard — call it $5K of incremental freight to recover $40K of margin and the OEM line-down avoidance. Across the 20-SKU portfolio, recurring tier-1 fill-rate slippage exposure is $1.5-2.5M annually; recovering even 60% of that with disciplined expedite calls is a million-dollar margin defense.*

> That's the decision this space automates. Not the customer-service ticket. The expedite call. Air freight gets booked on 4 SKUs by lunch, the tier-1 OEM gets the recovery commitment by 2 PM, and the chargeback line on the next month's P&L stays empty.

### Question (Act 2.3)

> **Which SKUs have the largest forecast bias (forecasted vs actual units) in the latest model version?**

**What to say while it runs:** SKUs with the largest forecast bias in the latest model version. Bias is the systematic over- or under-forecasting; a -200-unit bias means the model is consistently under-forecasting and we are stocking out. Bias is fixable; random noise is not — that's where the planner's intervention is highest-leverage.

**What to look for:** Top SKUs by absolute `forecasted_units - actual_units` from `demand_forecasts`. Look for SKUs where the bias is unidirectional — that's a model retraining or a parameter override candidate.

**Land the point:** That's the demand-sensing intervention list. The planner overrides the model on the SKUs where the bias is structural, the model retrains on the rest, and forecast accuracy lifts 3-5 points by the next cycle — without buying a new system.

---

## Act 3 — The commitment — locking the service-level tiers and the forecast investment *(≈4 min)*

**Persona:** VP of Supply Chain (with CFO) • **Job to be done:** Defend the customer-tier service-level commitments to the executive team and lock next year's contract-tier guarantees plus the demand-sensing investment.

*The VP doesn't need another supply-chain dashboard; they need the same lead-time and customer-satisfaction numbers the planning team is acting on, in the same language, so the renewal pricing and the tier-1 SLA guarantee both anchor on one source.*

### Question (Act 3.1)

> **What is the average lead time and days-to-ship by customer segment for shipped orders?**

**What to say while it runs:** Average lead time and days-to-ship by customer segment for shipped orders. Lead time is the commitment; days-to-ship is the actual. The gap between them is the trust gap — and customer segments with widening gaps are the segments where we're losing renewals on service before we lose them on price.

**What to look for:** Aggregate by `customer_segment` on `avg_lead_time` and `avg_days_to_ship`. The segment with the widest gap is the segment where the SLA needs to be renegotiated or backed by safety stock.

**Land the point:** That comparison is the actual contract-tier evidence. The VP walks into the renewal pricing committee with the segment-level service-level reality — not the marketing version — and the tier-1 OEM contracts get priced on real fulfillment data.

### Question (Act 3.2)

> **Which product categories have customer satisfaction below 3.5, and what is their backorder volume?**

**What to say while it runs:** Categories with customer satisfaction below 3.5 and their backorder volume. Satisfaction below 3.5 on a 5-point scale is the leading indicator of churn; backorder volume tells you whether it's a service problem or a product problem. Together they tell you where to put the next safety-stock investment.

**What to look for:** Filter on `customer_satisfaction_score < 3.5` with `backorder_units` beside. The categories with both low CSAT and high backorders are the safety-stock investment priority.

**Land the point:** That's the working-capital ask the CFO has been pushing back on for three quarters. Now it's not 'we'd like to carry more inventory' — it's 'these 4 categories have CSAT below renewal-risk threshold and these are the backorder volumes driving it.' The safety-stock budget gets approved on evidence, not on advocacy.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — DistroForecast Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total order revenue by product category for the trailing 12 months.
2. Which product categories have the worst forecast accuracy (highest avg forecast error) over the last 6 months?
3. Top 10 SKUs by open order value USD this week — and what is their fill rate?
4. How has the monthly backordered order count trended across customer segments?
5. Which SKUs have the largest forecast bias (forecasted vs actual units) in the latest model version?
6. What is the average lead time and days-to-ship by customer segment for shipped orders?
7. Which product categories have customer satisfaction below 3.5, and what is their backorder volume?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
