# CargoSight Analytics — Demo Script

**Space:** Logistics — CargoSight Analytics - Load Demand & Shipment Forecasting 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Logistics + Demand Planner, S&OP Lead, CFO partner
**KPIs touched:** Forecast volume accuracy, Capacity utilization %, Backlog orders, Delivered freight revenue, On-time delivery rate, Average transit days
**Big decision automated:** Which lanes to bid aggressively on at the next contract cycle, which to hold flat, and which 3-5 to drop entirely from the network book.

---

## Pre-demo checklist

- Open the Genie space `CargoSight Analytics - Load Demand & Shipment Forecasting 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CargoSight Analytics manages a 20-lane book across Domestic FTL, Domestic LTL, Cross-Border, and Intermodal, fed by 8 distribution hubs. Today the forecast-accuracy picture lives in the Demand Planner's monthly model-review workbook, the backlog and capacity tightness in the S&OP Lead's weekly capacity tracker, and the delivered freight revenue in the CFO partner's revenue-assurance pivot table. Three artifacts, three cadences, same lanes — and at every contract renewal the bid team flies half-blind on which lanes are actually earning money vs. which are subsidizing the others. This space ends that. One governed surface where the forecast accuracy, the capacity utilization, and the freight revenue per lane sit in the same conversation that sets the bid-or-drop call.

---

## Key KPIs in scope

- Forecast volume accuracy (actual / forecasted shipments) — target 95–105%; MAPE goal <10% for established lanes
- Capacity utilization % — lane fill rate; >85% on cross-border lanes signals capacity tightness
- Backlog orders — orders awaiting capacity; leading indicator of customer escalations
- Delivered freight revenue (USD) — top-line per lane / hub
- On-time delivery rate — delivered / total orders
- Average transit days — service-level metric for delivered shipments
- Average wait hours for capacity — dock / hub throughput pressure
- Delayed order count — service-quality signal by lane category

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **FTL** | Full Truckload |
| **LTL** | Less than Truckload |
| **MAPE** | Mean Absolute Percentage Error |
| **VP** | Vice President |

---

## Act 1 — The signal — forecast vs actual, lane by lane *(≈4 min)*

**Persona:** Demand Planner • **Job to be done:** Pull the lanes where the forecast is systematically wrong out of last quarter's data — these are the lanes that will hurt the next bid.

*This is where the bid prep starts. Two questions in, the Demand Planner already has the lane-category picture that used to require stitching the forecast file against the actuals export.*

### Question (Act 1.1)

> **Show monthly forecasted vs actual shipments by lane category for the trailing 12 months.**

**What to say while it runs:** Monthly forecasted vs. actual shipments by lane category for the last 12 months. A healthy book sits in the 95-105% band. Outside of that, we're either turning down profitable freight because we sized capacity too low, or carrying empty trucks because we sized too high.

**What to look for:** Twelve months of total_forecasted_shipments vs. total_actual_shipments split by Domestic FTL / LTL / Cross-Border / Intermodal. Look for the category whose actual line is consistently above or below the forecast — that's the structurally mis-priced book.

**Land the point:** Before this space the forecast-vs-actual chart was rebuilt every month on top of two CSV exports. Now the Demand Planner opens with it — and the conversation about which lane categories are systemically mis-forecast starts on the first slide.

### Question (Act 1.2)

> **How has delivered freight revenue trended month-over-month by origin hub?**

**What to say while it runs:** Delivered freight revenue trended monthly by origin hub. This is the top-line lens by hub — and it surfaces hubs where the lane mix is shifting under us without the QBR catching it.

**What to look for:** Monthly total_freight_revenue by origin hub. Hubs whose revenue is sliding while the network total holds flat are the hubs that have lost share to a competing carrier on at least one lane.

**Land the point:** When the Planner can see hub-level revenue trend without waiting for the CFO's monthly close, the early-warning conversation moves from 'we missed Q3' to 'we caught it in Month 2 and re-tendered the lane'.

---

## Act 2 — Bid, hold, or drop — locking the lane list *(≈4 min)*

**Persona:** S&OP Lead • **Job to be done:** Decide which lanes get aggressive pricing at the next renewal, which hold flat, and which 3-5 lanes come out of the book entirely.

*Three questions that take the lane shortlist to a defensible bid recommendation. The middle question is the anchor — backlog plus utilization is the lane-tightness picture that tells us where we can raise rates.*

### Question (Act 2.1)

> **Top 10 lanes by total actual shipments last quarter and what was their forecast accuracy?**

**What to say while it runs:** Top 10 lanes by total actual shipments last quarter, alongside their forecast accuracy. We want the volume leaders — but more importantly, which of those volume leaders are also the lanes we forecast worst on. Those are the lanes that hurt the network when they swing.

**What to look for:** A ranked list of 10 lanes with total_actual_shipments and the actual/forecasted ratio. Lanes with high volume AND accuracy outside the 95-105% band are the priority for forecast-model retraining and a renegotiated rate floor.

**Land the point:** That used to be a manual VLOOKUP across the forecast file and the dispatch system. Now it's a single query — and the bid-prep conversation starts from the same lane list everyone in the room can see.

### Question (Act 2.2)

> **Which lane categories have the highest delayed order count this quarter — where is service quality slipping?**

**What to say while it runs:** Lane categories with the highest delayed order count this quarter — service quality by lane type. If Cross-Border delayed_order_count is climbing while Domestic FTL holds flat, the issue isn't the network, it's the customs lane mix — and that changes how we bid the category at renewal.

**What to look for:** delayed_order_count grouped by lane category. Watch for one category breaking away from the rest — that's the category whose unit economics are quietly slipping below acceptable.

**Land the point:** Before this space the answer to 'where is service quality slipping' was a roundtable opinion poll. Now it's a ranked list with order counts attached — and the bid team knows exactly which lane category needs a chargeback-protected rate.

> **Anchor moment.** Stop on the capacity-tight lanes list. Take the top three lanes — running >90% utilization, double-digit backlog, sitting at average freight charges in the $2.20/lane-mile range across an FTL book.

> *Three capacity-constrained lanes at $2.20/lane-mile, with an addressable rate-card raise of $0.30/lane-mile when utilization is north of 85%. Each lane runs ~80 loads/month at an average 1,200 miles — that's $30K/month per lane in incremental revenue, or roughly $1M/year across the three. Now layer the drop side: the bottom 4 lanes are running at 55% utilization and 1.5% OTIF chargebacks against revenue. Dropping them frees ~6% of network capacity that gets redeployed into the bid-up lanes — call it another $400-600K/year of margin recovery. Across CargoSight's 20-lane book, that's a $1.5M+ annual decision that comes out of one screen.*

> That's the decision this space automates. Not the QBR slide. The decision. The bid book gets rebuilt on per-lane utilization, accuracy, and backlog dollars — not on the carrier rep's last conversation with the shipper.

### Question (Act 2.3)

> **Top 10 lanes by average capacity utilization with backlog orders greater than 10 — where are we capacity-constrained?**

**What to say while it runs:** Top 10 lanes by capacity utilization with more than 10 backlog orders. >85% utilization with backlog means we're turning down freight — that's pricing power on the next renewal. Below 70% with backlog means the lane is broken, and we need to drop it or restructure.

**What to look for:** Lanes ranked by avg_capacity_utilization with backlog_orders > 10. The top of the list is bid-up territory; the lanes with low utilization but high backlog are the candidates for elimination.

**Land the point:** That ranked list IS the next bid book. The S&OP Lead and CFO partner walk out with the lane names — not 'we should raise prices on cross-border' but 'these four lanes get a 12% bid, those three come out of the book entirely'.

---

## Act 3 — The commitment — locking the network book and the model-portfolio call *(≈4 min)*

**Persona:** VP Logistics • **Job to be done:** Defend the network book to the CFO and the customer-facing sales leadership — which lanes are growth, which are run-off, and which forecast model gets the ongoing investment.

*The VP needs the same numbers the planners are acting on, framed so the customer conversation and the budget conversation hold up the same story.*

### Question (Act 3.1)

> **How does average transit days for delivered orders compare across Domestic FTL, LTL, Cross-Border, and Intermodal?**

**What to say while it runs:** Average transit days for delivered orders by lane category — this is the service-level picture customers will quote back at us in the contract negotiation. Cross-Border carrying 6+ days vs. an industry expectation of 4 is a renegotiation lever the customer will use first.

**What to look for:** avg_transit_days grouped across Domestic FTL, LTL, Cross-Border, Intermodal. The category that runs above industry norms is the category most exposed to a service-credit clause at renewal.

**Land the point:** When the VP can show transit-days by category and rate it against the customer's own contracted SLA, the contract conversation moves from defensive ('we missed') to programmatic ('here's the lane-mix we're proposing to fix it').

### Question (Act 3.2)

> **What is the monthly forecast accuracy ratio (actual / forecasted shipments) by model version?**

**What to say while it runs:** Monthly forecast accuracy ratio by model version. We rotate forecast models roughly every 18 months — this is the answer to 'is the new model actually better than the one it replaced?'. If model v3 is delivering 96% on accuracy where v2 delivered 91%, that's an investment thesis for the data-science budget.

**What to look for:** Monthly accuracy ratio (total_actual_shipments / total_forecasted_shipments) by model version. Watch for the version inflection — that's the model we keep funding.

**Land the point:** Bid prep at 8 AM, model-portfolio review at 10. Same space. The VP walks into the CFO conversation with one set of numbers covering the lane book, the service quality, AND the forecasting investment — and the contract cycle stops being three separate fights.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CargoSight Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly forecasted vs actual shipments by lane category for the trailing 12 months.
2. How has delivered freight revenue trended month-over-month by origin hub?
3. Top 10 lanes by total actual shipments last quarter and what was their forecast accuracy?
4. Which lane categories have the highest delayed order count this quarter — where is service quality slipping?
5. Top 10 lanes by average capacity utilization with backlog orders greater than 10 — where are we capacity-constrained?
6. How does average transit days for delivered orders compare across Domestic FTL, LTL, Cross-Border, and Intermodal?
7. What is the monthly forecast accuracy ratio (actual / forecasted shipments) by model version?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
