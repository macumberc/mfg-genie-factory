# ForecastPro Machinery — Demo Script

**Space:** Machinery — ForecastPro Machinery - Demand Forecasting 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Sales + S&OP Planner, Demand Manager, CFO
**KPIs touched:** Forecast accuracy, MAPE, Fill rate, Backlog units, Forecast bias, Cancellation rate
**Big decision automated:** Which 2 product families get capacity expansion next fiscal year, which get plant consolidation, and which regions get dealer-channel investment versus harvest.

---

## Pre-demo checklist

- Open the Genie space `ForecastPro Machinery - Demand Forecasting 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> ForecastPro runs 20 equipment SKUs across five families — Heavy Excavators for Mining, Mobile Cranes for Construction, Industrial Generators for Energy, Centrifugal Pumps for Water/Waste, Control Valves for Oil & Gas — sold into Americas, EMEA, APAC, and LATAM through a dealer channel. Today the S&OP planner reconciles SKU-level MAPE in a stat-tool workbook, the Demand Manager tracks backlog and cancellations in the order-management extract, and the VP Sales tunes regional mix in a quarterly Salesforce dashboard. Three workbooks, same orders, three different versions of fill rate — and the capacity-expansion call for next year keeps getting deferred because the numbers don't reconcile. This space ends that: one governed surface where MAPE, fill rate, backlog, and revenue all resolve to the same product family and the same region, so the capacity bet and the channel investment can be made on dollars instead of opinions.

---

## Key KPIs in scope

- Forecast accuracy (%) — best-in-class 75–85% at SKU level (100% − MAPE)
- MAPE (%) — mean absolute percentage error; <15% world-class, 15–25% average
- Fill rate (%) — order fulfillment target ≥95%
- Backlog units — capacity and lead-time stress indicator
- Forecast bias — chronic over/under-forecast detector
- Cancellation rate (%) — demand-quality signal
- Total revenue ($) — financial impact of demand performance
- Lead time (days) — competitive promise tracking

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MAPE** | Mean Absolute Percentage Error |
| **SKU** | Stock Keeping Unit |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the families the forecast is quietly failing *(≈4 min)*

**Persona:** Demand Manager • **Job to be done:** Pull this week's forecast-correction list and the backlog-risk shortlist out of the same conversation, instead of two separate workbooks.

*This is the week the next S&OP cycle gets seeded. Two questions in, the Demand Manager already knows which families need a forecast override and which SKUs are at lead-time risk.*

### Question (Act 1.1)

> **What is the monthly trend in forecast accuracy by product family over the trailing 12 months?**

**What to say while it runs:** Monthly trend in avg_forecast_accuracy by product family. World-class at SKU level is 75-85%; under 75% means the model is systematically wrong. The trend line tells you whether v4.2 is actually beating v4.0 or just rebadged.

**What to look for:** Five lines on one chart — Heavy Excavators, Mobile Cranes, Industrial Generators, Centrifugal Pumps, Control Valves — over 12 months. Watch for the family that's been below 75% for three or more months: that's a structural model problem, not a one-off miss.

**Land the point:** When the Demand Manager can see the family trajectories in one view, the weekly override conversation moves from 'whose gut do we trust' to 'where is the model losing.' That's the input to next quarter's planning bake-off.

### Question (Act 1.2)

> **Top 10 equipment models by backlog units — which are at greatest risk of missed lead time?**

**What to say while it runs:** Top 10 equipment_models by backlog_units. Backlog is capacity stress — units the customer wants that we haven't shipped. Anything above promised lead_time_days is a credibility risk. This is the list dealers call us about.

**What to look for:** Ranked models with backlog_units and avg_lead_time. Watch for the Heavy Excavator and Mobile Crane SKUs — those have the longest natural lead times and the least slack to absorb a forecast miss.

**Land the point:** That ranked list used to come out of an order-management report on Friday. Now it's the input to Monday's expedite call — which SKUs we paid overtime to clear and which dealers get the apology email. Lead-time credibility, one conversation.

---

## Act 2 — Capacity expand or plant consolidate — the families that earn next year's capex *(≈4 min)*

**Persona:** S&OP Planner • **Job to be done:** Lock the recommendation on which 2 product families get capacity expansion, which 2 hold flat, and which 1 consolidates plants.

*These three questions are where the capacity bet gets sized. Cancellations tell you where demand is soft; fill rate tells you where capacity is short; revenue mix tells you where the dollars actually are.*

### Question (Act 2.1)

> **Which customer regions have the highest order cancellation rate this quarter?**

**What to say while it runs:** Cancellation rate by customer_region this quarter. Industry leaders run under 3%. Above 5% is a demand-quality flag — either the dealer is over-promising or the regional economics turned. Either way, capacity for that region doesn't grow next year.

**What to look for:** Four bars — Americas, EMEA, APAC, LATAM — with cancelled_orders against new_orders ratio. Watch for a region above 5%: that's the consolidation-candidate region.

**Land the point:** When the VP Sales can see cancellations resolved by region in seconds instead of a Salesforce extract on Friday, the dealer-channel investment debate becomes a numbers conversation. LATAM stays or LATAM exits — and we know which on a Tuesday.

### Question (Act 2.2)

> **Rank product families by fill rate — which are below the 95% target?**

**What to say while it runs:** Ranking product families by avg_fill_rate. Target is 95%. Below that is missed revenue, capacity shortfall, or both. The families above 95% are paying their own way; the ones below need capacity or need to drop.

**What to look for:** Bar chart by product_family with avg_fill_rate. Note which fall below 95 — those are the capacity-expansion candidates if demand is real, the consolidation candidates if demand is hollow.

**Land the point:** That fill-rate ranking used to be a slide the VP Sales rebuilt monthly. Now it's the same artifact the planner uses on Tuesday and the VP defends to the board in three weeks — same definition, same number.

> **Anchor moment.** Stop on the fill-rate ranking and the revenue trend. Pick a single family — call it Mobile Cranes at 87% fill rate against the 95% target, with 600 units of backlog and quarterly revenue around $15M.

> *An 8-point fill rate gap on $60M annual family revenue is roughly $5M in missed shipments per year — assuming the demand was real and didn't roll to a competitor. If half of that recovers with one additional Mobile Crane line at $4-6M capex, the payback is under 12 months and the run-rate revenue picks up $3-4M every year after. Across the five families, every 1pp of fill rate recovered is $1-1.5M of annual revenue at this scale — and our two below-target families are leaving $8-12M on the table.*

> That's the FY plan in one number. Capacity expansion goes to Mobile Cranes and Heavy Excavators, Centrifugal Pumps holds flat, Control Valves consolidates to one plant. Decision made on dollars, not on which product manager argued the loudest in the steering committee.

### Question (Act 2.3)

> **Show monthly trend in total revenue vs new orders received.**

**What to say while it runs:** Monthly total_revenue overlaid with total_new_orders. Revenue trending up while new orders trend flat means we're shipping out of backlog — a temporary win. Revenue trending up with new orders up is real demand. Revenue down with cancellations up is a structural problem.

**What to look for:** Two lines on one chart, 12 months. The shape of the gap between them is the leading indicator the CFO actually cares about.

**Land the point:** When the planner, the demand manager, and the CFO all see the revenue-vs-orders chart with the same governed definition, the FY plan stops being an argument and starts being a sizing exercise. Three families fund growth, two harvest — that conversation now takes one meeting, not three.

---

## Act 3 — The commitment — locking the capex board package and the dealer-channel mix *(≈4 min)*

**Persona:** VP Sales • **Job to be done:** Defend the capacity bet and the regional dealer investment to the board, with the same numbers the planner is acting on.

*The VP Sales walks into the FY board package with the planner's working numbers, not a reconstructed slide deck. That's the change.*

### Question (Act 3.1)

> **Top 10 equipment models by total order revenue this year, and what was the forecast accuracy for each?**

**What to say while it runs:** Top 10 equipment_model by total_order_revenue this year, with their forecast accuracy alongside. The top revenue SKUs better be the ones with the best forecast — if they're not, we're guessing on our most important products and that's a board conversation in itself.

**What to look for:** Ranked SKUs with total_order_revenue and avg_forecast_accuracy in the same row. Watch for a high-revenue SKU with sub-70% accuracy — that's the SKU getting an immediate model-tuning sprint.

**Land the point:** When the highest-revenue SKUs and their forecast quality sit in the same view, the board package writes itself: top-line growth, by family, with the forecast confidence to back it. No reconciliation step, no two-day prep cycle.

### Question (Act 3.2)

> **Which forecast model versions have the worst MAPE, and what is the cost of the bias?**

**What to say while it runs:** Worst MAPE by model_version. v4.2 was supposed to beat v4.0 — has it? The bias times the unit volume times the average unit price is the dollar cost of the wrong forecast. That's the number that justifies the data science budget or kills it.

**What to look for:** Bar chart by model_version with avg(mape_pct), filtered to the SKUs in the v4.2 cohort. Watch for v4.2 having worse MAPE than v4.1 — that means the upgrade was a regression and we need to know.

**Land the point:** Forecast quality goes from a back-office metric to a P&L line. When the VP can defend the demand plan with both revenue growth and the MAPE-times-ASP cost of the residual error, the board approval cycle compresses from two months to one. One space, three personas, one set of numbers.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — ForecastPro Machinery — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. What is the monthly trend in forecast accuracy by product family over the trailing 12 months?
2. Top 10 equipment models by backlog units — which are at greatest risk of missed lead time?
3. Which customer regions have the highest order cancellation rate this quarter?
4. Rank product families by fill rate — which are below the 95% target?
5. Show monthly trend in total revenue vs new orders received.
6. Top 10 equipment models by total order revenue this year, and what was the forecast accuracy for each?
7. Which forecast model versions have the worst MAPE, and what is the cost of the bias?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
