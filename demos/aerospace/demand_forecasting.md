# AeroParts Supply — Demo Script

**Space:** Aerospace — AeroParts Supply - Demand Forecasting & Backlog 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Supply Chain + Demand Planner, Aftermarket Program Manager
**KPIs touched:** Forecast accuracy / MAPE, Forecast bias, Fill rate %, On-time delivery %, Backlog value and aging buckets, Average lead time by part category
**Big decision automated:** Which 5 aftermarket SKUs to pre-build with safety stock vs. which 5 to accept stockouts on — and where to defend lead-time commitments to airline customers next quarter.

---

## Pre-demo checklist

- Open the Genie space `AeroParts Supply - Demand Forecasting & Backlog 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroParts Supply distributes 20 aftermarket SKUs — rotables (HPT disks, fan blades), repairables (fuel nozzles, hydraulic actuators), and consumables (gasket kits, O-rings) — to 5 customer segments: Airline, MRO, Military, OEM, and Leasing. Today the forecast accuracy number lives in the Demand Planner's MAPE spreadsheet, the backlog aging report lives in the Program Manager's Excel pivot, and the fill-rate-vs-AOG-penalty number lives in a quarterly slide the VP of Supply Chain rebuilds for the operating review. Three workbooks, same 20 SKUs — and which parts get pre-built into safety stock vs. which get fulfilled reactively is decided in a meeting that always runs over because nobody has the same numbers. This space ends that. One governed surface where forecast bias, backlog aging, and fill rate sit next to each other, so the safety-stock investment becomes a 15-minute conversation instead of a quarterly debate.

---

## Key KPIs in scope

- Forecast accuracy / MAPE — aero aftermarket benchmark 20-30% (intermittent demand), <15% on rotables
- Forecast bias (over- vs. under-forecast count)
- Fill rate % (target >95% on AOG critical parts)
- On-time delivery % (industry benchmark 90-95%)
- Backlog value (USD) and aging buckets
- Average lead time (days) by part category
- Inventory turns (target 4-6x for aftermarket)
- Total aftermarket revenue (USD)

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **AOG** | Aircraft on Ground |
| **MAPE** | Mean Absolute Percentage Error |
| **MRO** | Maintenance, Repair & Overhaul |
| **OEM** | Original Equipment Manufacturer |
| **VP** | Vice President |

---

## Act 1 — The signal — finding where the forecast is leaking dollars before the customer calls *(≈4 min)*

**Persona:** Demand Planner • **Job to be done:** Identify which SKUs have backlog stacking up faster than the forecast says they should, and which customer segments are driving it.

*This is the moment the safety-stock pre-build list starts forming. The planner is looking for the mismatch between what the model said and what the orders actually did — because that's where the AOG fines are hiding.*

### Question (Act 1.1)

> **Top 10 parts by total backlog units — and which customer segments do they ship to?**

**What to say while it runs:** Backlog units by SKU is the leading indicator the planner watches. On rotables — HPT disks, fan blades — the target fill rate is 95% because every backlog day on an AOG-critical SKU is a $10-15K-per-hour penalty conversation with an airline customer. Notice which SKUs are also concentrated in the Airline segment — those are the contractual exposures.

**What to look for:** A ranked table of the top 10 SKUs by total backlog units with their customer segment mix. The room should see that rotables tend to cluster at the top and that one or two SKUs carry disproportionate Airline exposure.

**Land the point:** That list IS the safety-stock candidate list. Now the planner can walk into the program review with a defensible pre-build proposal instead of a gut call — and the AOG-penalty conversation moves from 'we missed' to 'we hedged'.

### Question (Act 1.2)

> **Show monthly trend in average forecast error % by part category over the trailing 12 months.**

**What to say while it runs:** Now forecast error by part category over 12 months. Aero aftermarket MAPE benchmark is 20-30% on intermittent demand and under 15% on rotables. Anything above 30% on a Rotable line is the forecast model losing money — that's where bias is structural, not noise.

**What to look for:** Monthly trend bars by part category using `DATE_TRUNC('month', ...)`. Watch for categories where the line is climbing or stuck above benchmark — those are the SKUs the model can't see.

**Land the point:** Before this space, that chart was a quarterly artifact in the model-review deck. Now it's the planner's first question of the day — and the conversation about which SKUs need a new forecast model starts a quarter earlier.

---

## Act 2 — The decision — which 5 SKUs earn safety stock and which 5 accept the stockout *(≈4 min)*

**Persona:** Aftermarket Program Manager • **Job to be done:** Commit to a pre-build list — naming exactly which SKUs get inventory dollars allocated and which get a managed-stockout posture with the customer.

*Three questions that turn the watchlist into a defensible safety-stock recommendation. The middle question is the anchor — converting backlog and fill-rate gaps into the AOG-penalty math the CFO will sign off on.*

### Question (Act 2.1)

> **Which customer segments drive the most aftermarket revenue this year?**

**What to say while it runs:** Aftermarket revenue by customer segment tells us where the dollars are concentrated. Airlines and MRO together typically run 60-70% of the book — they're also the segments with the AOG SLAs. The Leasing segment is steadier but lower margin.

**What to look for:** Revenue by customer segment YTD. The point isn't the ranking — it's that Airline + MRO exposure is the segment that needs fill-rate protection because that's where the penalty clauses live.

**Land the point:** When the planner, program manager, and VP all see the same revenue-by-segment cut, the safety-stock conversation stops being 'whose customer is loudest' and becomes 'where the contractual penalties are biggest.'

### Question (Act 2.2)

> **Top 10 parts by total order revenue — what is their average lead time?**

**What to say while it runs:** Top 10 SKUs by revenue with their average lead time. Rotables benchmark at 21-45 days, expendables 14-30, AOG-critical under 24 hours. Anything where the revenue is high AND the lead time is creeping past benchmark is a candidate for the pre-build list — that's the SKU where inventory carrying cost is cheaper than the AOG fine.

**What to look for:** A table joining revenue rank to avg_lead_time_days. Sort visually — the upper-left quadrant (high revenue, long lead time) is the safety-stock list.

**Land the point:** That quadrant IS the pre-build recommendation. Two queries in, the program manager has a defensible list to walk into the CFO review — and the conversation moves from 'we need more inventory budget' to 'here are the 5 SKUs and the AOG hours they protect.'

> **Anchor moment.** Park on the top 10 SKUs by revenue + lead time view. Pick one rotable — say HPT disks — with high revenue, lead time creeping past benchmark, and Airline-segment exposure.

> *Average AOG hour penalty is $10-15K. If we're missing fill rate on 5 AOG-critical rotables and each generates 3 stockout events per quarter at an average 12 AOG hours per event, that's 5 SKUs × 3 events × 12 hours × $12K = $2.2M per quarter in penalty exposure. Pre-building safety stock on those 5 SKUs costs ~$400K in carry — maybe 6 SKUs × $14K-$42K unit cost × 5-unit buffer. Payback is one quarter. Across the full 20-SKU portfolio at AeroParts' scale, that's $6-9M of annual recoverable AOG penalty.*

> That's the decision this space automates. The pre-build list gets written from AOG-dollar exposure, not from whose customer escalated last. Safety-stock budget gets defended on penalty math, not on instinct.

### Question (Act 2.3)

> **How has on-time delivery % trended month-over-month by part category?**

**What to say while it runs:** On-time delivery trend by part category — industry benchmark is 90-95%. Anything below 90% on a Rotable line means we're either eating AOG penalties or the airline customer is shopping the contract. That's the metric the VP carries into the customer QBR.

**What to look for:** Monthly OTD trend by part_category. Watch for categories where OTD is sliding below 90% — those need either supplier-side escalation or a higher safety stock target.

**Land the point:** That's the slide the VP shows the airline customer in next month's QBR. Same numbers the planner just acted on. No reconciliation meeting, no version mismatch.

---

## Act 3 — The commitment — defending the safety-stock posture and the lead-time guarantee to airline customers *(≈4 min)*

**Persona:** VP of Supply Chain • **Job to be done:** Defend the pre-build investment to the CFO and lock the lead-time commitments AeroParts will make in next year's airline supply contracts.

*The VP doesn't need a new report — they need the same numbers the planner is acting on, packaged for the operating review and the customer contract negotiation.*

### Question (Act 3.1)

> **Which part categories show forecast over-forecast bias, and by how much?**

**What to say while it runs:** Forecast bias by category — over-forecast vs. under-forecast. Persistent over-forecasting on Rotables means we're tying up cash in inventory we don't move. Persistent under-forecasting on Consumables means we're paying expedite freight. Bias direction tells the CFO whether to invest in better models or in carry capacity.

**What to look for:** Categories ranked by over_forecast_count and the dollar gap. Look for asymmetry — over-bias on slow movers, under-bias on critical fast-movers is the worst combination.

**Land the point:** When the VP walks into the operating review with this view, the safety-stock ask isn't 'more inventory budget' — it's 'fix bias on these 3 categories OR fund safety stock on these 5 SKUs.' That's a CFO-grade tradeoff, not a wish list.

### Question (Act 3.2)

> **Show the monthly trend in total shipped order count across the network.**

**What to say while it runs:** Shipped-order count trend across the network. This is the volume-and-mix story that determines whether next year's airline contracts get a 24-hour AOG commitment or a 48-hour one — and what we charge for it.

**What to look for:** Monthly shipped_order_count trend. The shape — flat, climbing, or seasonal — is what shapes the contract pricing model the VP signs next quarter.

**Land the point:** Triage at the desk, safety-stock list at the program review, contract terms at the customer QBR. One space. Same numbers. The airline gets one story from AeroParts, not three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroParts Supply — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 parts by total backlog units — and which customer segments do they ship to?
2. Show monthly trend in average forecast error % by part category over the trailing 12 months.
3. Which customer segments drive the most aftermarket revenue this year?
4. Top 10 parts by total order revenue — what is their average lead time?
5. How has on-time delivery % trended month-over-month by part category?
6. Which part categories show forecast over-forecast bias, and by how much?
7. Show the monthly trend in total shipped order count across the network.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
