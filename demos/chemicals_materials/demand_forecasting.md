# ChemFlow Industries — Demo Script

**Space:** Chemicals & Materials — ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** Supply Chain VP + Plant Manager, Supply Chain VP, CFO
**KPIs touched:** Forecast accuracy / MAPE, Fill rate / fulfilled order count, Backorder count, Days of supply, Safety stock vs. on-hand position, Order value and average unit price
**Big decision automated:** Which 4-5 grades to expand catalog capacity on, which 3-4 grades to retire, and which plant gets the next turnaround window — and at what safety-stock level we run the rest.

---

## Pre-demo checklist

- Open the Genie space `ChemFlow Industries - Demand Forecasting & Inventory Optimization 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> ChemFlow Industries runs 20 grades across 6 manufacturing plants serving 5 customer segments — coatings, specialties, base chemicals, polymers, additives. Today the forecast accuracy number lives in the demand planner's S&OP workbook, the days-of-supply number lives in each plant manager's safety-stock spreadsheet, and the gap-to-budget number lives in the CFO's revenue-bridge slide. Three workbooks, same SKUs — and next quarter's grade-by-grade capacity allocation (and which plant earns the next turnaround slot) gets decided in a 90-minute S&OP meeting nobody believes the numbers in. This space ends that. One governed surface where MAPE, DOS, backorder dollars, and the forecast-to-actual revenue gap land in the same conversation as the turnaround calendar.

---

## Key KPIs in scope

- Forecast accuracy / MAPE (%) — industry benchmark ~25-30% MAPE at SKU-plant-month grain
- Fill rate / fulfilled order count — target ≥ 98% for industrial chemicals
- Backorder count — leading indicator of customer churn risk
- Days of supply (DOS) — target 30-60 days finished goods, 15-30 for high-volume
- Safety stock vs. on-hand position — working capital governor
- Order value ($) and average unit price ($/kg) — revenue and price-realization signal
- Forecast vs. actual revenue gap — ties demand plan to P&L
- Reorder status mix (Critical / Low / Reorder Placed / Adequate) — stockout risk

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MAPE** | Mean Absolute Percentage Error |
| **OTIF** | On-Time In-Full |
| **SKU** | Stock Keeping Unit |
| **VP** | Vice President |

---

## Act 1 — The signal — separating the grades the plan is winning on from the ones it's bleeding *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Find tomorrow's stockout candidates and the grades where the forecast is consistently wrong — before the order book makes the decision for you.

*This is where the S&OP debate gets pre-empted. Two questions in, the plant manager already has the grades-to-watch list that the demand planner spent yesterday afternoon building in Excel.*

### Question (Act 1.1)

> **Show monthly total order value by product category for the trailing 12 months.**

**What to say while it runs:** Monthly total order value by product category over 12 months — coatings, specialties, base chemicals, polymers, additives. The trend tells you which categories are growing organically vs. which are running hot on price. Raw-material swings of 20-40% YoY are normal in basic chemicals, so the slope matters more than any single month.

**What to look for:** Monthly total_order_value_usd by product_category. Watch for the category where volume is flat but order value is climbing — that's price-driven and not real demand growth.

**Land the point:** Right there is the first capacity-planning conversation. The categories with real demand growth are the ones that earn next year's plant time; the ones that are growing on price alone are the ones we hedge instead of expand.

### Question (Act 1.2)

> **How has forecast accuracy (actual vs forecasted kg) trended month-over-month by product category?**

**What to say while it runs:** Now forecast accuracy by category — actual quantity kg against forecasted quantity kg, month over month. Industry MAPE at SKU-plant-month grain is 25-30%. Anything north of 40% means the demand model has structural blind spots in that category, and safety stock is doing the work the plan can't.

**What to look for:** Monthly gap between total_actual_qty_kg and total_forecasted_qty_kg by category. The categories with the widest divergence are the ones where working capital is being burned to compensate.

**Land the point:** Before this space, that chart got rebuilt by hand for the monthly S&OP. Now it's the planner's first question of the day — and the grade-expansion conversation starts an hour earlier with a different shortlist than gut would have produced.

---

## Act 2 — The decision — which grades to expand, which to retire, which plant earns the next turnaround *(≈4 min)*

**Persona:** Supply Chain VP • **Job to be done:** Commit to a 12-month grade portfolio decision — what stays, what goes, where capacity gets added, and which plant gets the next turnaround window.

*Three questions that turn the demand signal into a defensible capacity-allocation recommendation. The middle question is the anchor — the backorder-dollar exposure that converts the stockout-risk list into a working-capital decision.*

### Question (Act 2.1)

> **Top 10 products by backorder count in the last 90 days — which plants are they shipping from?**

**What to say while it runs:** Top 10 products by backorder count over the last 90 days, with the plants they're shipping from. Backorder count is the leading indicator of customer churn — for industrial chemicals, target fill rate is 98%+. A grade that's chronically backordered is either underforecast or undercapacitied; either way it's a capacity-allocation flag.

**What to look for:** Ranked list with backorder_count and plant_id. The repeat offenders shipping from the same plant are the candidates for the next debottleneck investment.

**Land the point:** That list used to be the back of the supply chain VP's monthly deck. Now it's the input to the turnaround-prioritization conversation — and the plant manager isn't defending their book, they're agreeing on the numbers.

### Question (Act 2.2)

> **Which products currently have a Critical or Low reorder status, and how many days of supply are remaining?**

**What to say while it runs:** Products in Critical or Low reorder status, with days of supply remaining. Days-of-supply targets are 30-60 days finished goods, 15-30 for high-volume. Anything in single digits is a confirmed stockout exposure — and every day on that list is a customer-segment churn risk we can put a dollar on.

**What to look for:** Filtered list of inventory positions where reorder_status is Critical or Low, sorted ascending by days_of_supply. The Critical rows are the ones earning emergency air-freight today.

**Land the point:** When the planner, the plant manager, and the supply chain VP all see the same DOS column, the safety-stock debate stops being political and starts being arithmetic. The grades on this list are the ones either expanding capacity or retiring — there's no third option.

> **Anchor moment.** Pause on the backorder ranking and the forecast-vs-actual revenue gap. Pick the worst plant — call it $4M of unfilled backorder over the trailing 90 days on a handful of grades, and a $6M forecast-to-actual revenue shortfall.

> *Four million in backorder over 90 days annualizes to $16M of at-risk revenue, and industrial-chemical fill-rate gaps below 95% routinely cost 8-12% of the affected book in churn within 18 months. That's $1.3-1.9M of margin a year on the table — on one plant, on a handful of grades. Across 6 plants, $5-8M of annual churn-risk margin that the forecast is mispricing today. A typical plant turnaround runs $5-15M; the math on a backorder-dollar-prioritized turnaround pays back inside one cycle.*

> That's the decision this space automates. Not the S&OP slide — the decision. Capacity expansion and turnaround scheduling get built off backorder dollars and forecast-gap dollars, not the loudest customer-segment story. The grade-retirement list and the capacity-add list become two sides of the same conversation.

### Question (Act 2.3)

> **What is the total forecasted revenue vs actual revenue gap by plant for the last 6 months?**

**What to say while it runs:** Forecasted revenue vs. actual revenue gap by plant over 6 months. This is the CFO's leading-indicator number — if the plan is consistently low at a plant, we're under-buying feedstock; consistently high, we're tying up working capital that funds nothing. Either direction is a portfolio decision, not a planning tweak.

**What to look for:** Plant-level table of total_forecasted_revenue vs total_actual_revenue with the dollar gap. Look for plants where the gap is large and one-directional — that's a structural forecast-model problem, not noise.

**Land the point:** That gap is the conversation that converts the S&OP meeting from a status update into a capacity-investment decision. The plant with the worst structural gap is either the turnaround candidate or the retirement candidate, depending on where the demand is going.

---

## Act 3 — The commitment — locking the capacity plan and the 12-month grade portfolio *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the working-capital and capacity plan to the executive committee and shape next year's plant capex envelope.

*The CFO doesn't need another forecast; they need the same DOS, backorder, and forecast-gap numbers the supply chain VP is using, in the same definitions, so the capital case writes itself.*

### Question (Act 3.1)

> **Top 10 customer segments by total order value this year — and how has average unit price moved?**

**What to say while it runs:** Top 10 customer segments by total order value this year, with average unit price movement alongside. Price realization is the easiest signal to lose in raw-material noise — if a high-volume segment is showing price compression, that's the one whose forecast needs to be reconciled against contract terms, not just demand.

**What to look for:** Ranked table of customer segments by total_order_value_usd with the YoY movement in avg_unit_price_usd. Segments where price is sliding faster than feedstock costs are negotiating from a position we didn't notice.

**Land the point:** That's the chart the commercial team and finance need to align on before the next contract cycle. Same numbers as the planner sees, same definitions — and the executive committee gets one revenue story, not two.

### Question (Act 3.2)

> **Which product categories have the highest backorder rate, and what is the dollar exposure?**

**What to say while it runs:** Product categories with the highest backorder rate, with the dollar exposure attached. This is the capex-prioritization view — which categories have demand the current footprint can't serve, and what the cost of *not* fixing it is over a 12-month window.

**What to look for:** Bar chart of categories with backorder rate and a stacked column for dollar exposure. The biggest bars are the ones whose plant lines earn next year's capacity capex — not the loudest customer, the most expensive structural gap.

**Land the point:** Triage at 8 AM, capacity allocation at 10, capex at noon. Same space. Same numbers. The plant manager's backorder list and the CFO's capex pitch are now the same artifact — and the board hears one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — ChemFlow Industries — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total order value by product category for the trailing 12 months.
2. How has forecast accuracy (actual vs forecasted kg) trended month-over-month by product category?
3. Top 10 products by backorder count in the last 90 days — which plants are they shipping from?
4. Which products currently have a Critical or Low reorder status, and how many days of supply are remaining?
5. What is the total forecasted revenue vs actual revenue gap by plant for the last 6 months?
6. Top 10 customer segments by total order value this year — and how has average unit price moved?
7. Which product categories have the highest backorder rate, and what is the dollar exposure?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
