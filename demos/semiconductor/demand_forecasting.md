# ChipFlow Supply — Demo Script

**Space:** Semiconductor — ChipFlow - Demand Forecasting 📈
**Runtime:** ~15 minutes • 7 questions
**Audience:** Supply Chain VP + CFO partner, alongside Demand Planning and Sales Ops
**KPIs touched:** Forecast accuracy %, Backlogged order count, Book-to-bill ratio, Lead time, Weeks of supply, Total order revenue
**Big decision automated:** Which 5 SKUs to pre-build wafer starts against this quarter, which 5 customer commitments to renegotiate before backlog forces allocation, and which product lines to flag for write-down.

---

## Pre-demo checklist

- Open the Genie space `ChipFlow - Demand Forecasting 📈`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> ChipFlow Supply ships 20 SKUs across Microcontroller, Memory, Analog, Power, and Connectivity to OEM Tier 1, OEM Tier 2, Distributor, Contract Manufacturer, and Direct Enterprise channels. Today the backlog aging lives in a Sales Ops Salesforce export, the forecast-accuracy and bias numbers live in Demand Planning's weekly Excel from the ARIMA / Prophet / ML Ensemble runs, and weeks-of-supply sits in the Supply Chain VP's monthly S&OP slide. Three workbooks, one cycle — and during the last book-to-bill inflection the team allocated wafer starts to the wrong four SKUs and ate a write-down on the other six. This space ends that. One governed surface where the VP and the CFO can see backlog exposure in dollars, forecast bias by category, and weeks-of-supply by SKU in the same conversation that sets the wafer-start commit.

---

## Key KPIs in scope

- Forecast accuracy % — 1-MAPE on units forecast; world-class semis target 70%+, with leading-edge SKUs often 50-60%
- Backlogged order count — orders past quoted lead time; leading indicator of capacity or yield issues
- Book-to-bill ratio — bookings vs shipments; >1.0 indicates growing demand, <1.0 contraction
- Lead time (days) — quoted vs achieved; semi industry median 12–26 weeks during shortage cycles
- Weeks of supply — committed vs available inventory; healthy 8–16 weeks
- Total order revenue (USD) — top-line demand signal
- Forecast bias — chronic over/under bias by SKU category
- Customer segment concentration — share of revenue at-risk by segment

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MAPE** | Mean Absolute Percentage Error |
| **OEM** | Original Equipment Manufacturer |
| **SKU** | Stock Keeping Unit |
| **VP** | Vice President |

---

## Act 1 — The signal — where the order book is leaking dollars before allocation *(≈4 min)*

**Persona:** Sales Ops / Demand Planning lead • **Job to be done:** Identify which SKUs are sitting in backlog with real revenue exposure and which customer segments are absorbing it, before the next book-to-bill cycle call.

*This is where the wafer-start allocation conversation actually starts — not in the S&OP deck, but in the backlogged_order_count line. Two questions in, the room has the at-risk dollars by SKU and the trailing demand shape by segment.*

### Question (Act 1.1)

> **Which 10 SKUs have the highest backlogged order count, and what is our exposed revenue?**

**What to say while it runs:** Backlog above quoted lead time is the first place the order book starts hemorrhaging revenue. We're looking at the top 10 SKUs by backlogged_order_count with their exposed total_order_revenue_usd next to them — and in semis the Tier-1 automotive SKUs are the ones you cannot let slip.

**What to look for:** A ranked table of 10 SKUs with backlog count and revenue exposure. Click Show generated code once — governed measures from customer_order_metrics, not free-form math.

**Land the point:** Right there is the allocation conversation. Now Demand Planning can name the 5 SKUs that need pre-build wafer starts in minutes — that's the wafer-start commit conversation that used to require a 90-minute S&OP debate.

### Question (Act 1.2)

> **Show monthly total order revenue by customer segment for the trailing 12 months.**

**What to say while it runs:** Now the 12-month total_order_revenue_usd shape by customer_segment — OEM Tier 1 vs OEM Tier 2 vs Distributor vs Contract Manufacturer vs Direct Enterprise. The segment whose trend turns first IS the cycle inflection, six weeks before the SIA prints it.

**What to look for:** Monthly bars by segment with DATE_TRUNC('month', order_date). Watch for the segment whose line flattens or rolls — that's the early-warning indicator the CFO wants.

**Land the point:** Before this space, that chart was a Tuesday-night Excel rebuild for the Wednesday S&OP. Now Sales Ops opens with it — and the question of which segments to defend on price vs. release on lead-time is on the table before coffee.

---

## Act 2 — The decision — which SKUs get the wafer starts, which customers get renegotiated *(≈4 min)*

**Persona:** Supply Chain VP • **Job to be done:** Commit the quarter's scarce wafer-start capacity to the SKUs that pay back and de-commit on the ones whose forecast bias and lead-time inflation say the cycle has turned.

*Three questions that convert the watchlist into a defensible wafer-start commit. The middle question is the anchor — the deferred-revenue conversation that converts forecast bias into allocation policy.*

### Question (Act 2.1)

> **Which product categories have the worst forecast accuracy this quarter — where do we need model retraining?**

**What to say while it runs:** Forecast accuracy < 70% by category is where we are flying blind on the next quarter's wafer commit. Anything below 60% on a leading-edge category means the model itself needs retraining — that's the Demand Planning ask we surface here.

**What to look for:** A short table of product_category with avg_forecast_accuracy_pct from forecast_accuracy_metrics. Below 60% is a red flag; below 50% means the ARIMA or Prophet baseline is fighting the cycle.

**Land the point:** That list used to be the output of a half-day spreadsheet pull. Now it's the input to the model-retraining decision the VP signs off on at the standup.

### Question (Act 2.2)

> **Rank the 5 customer regions by average lead time — where is lead-time inflation worst?**

**What to say while it runs:** Lead time by region — Asia Pacific vs. Greater China vs. North America vs. Europe. Semi shortage cycles push avg_lead_time_days from 56-84 to 168-365. Whichever region's number is climbing fastest is where customer renegotiation has to start first.

**What to look for:** Top 5 regions ranked by avg_lead_time_days from customer_order_metrics. The deltas vs last quarter are the real signal — that's the part the spreadsheet usually skips.

**Land the point:** When the VP, Demand Planning, and the CFO see the same lead-time number governed the same way, the conversation stops being whose Excel is right and starts being which customers we call this week.

> **Anchor moment.** Stop on the backlog ranking from Act 1 and the lead-time-by-region table on screen. Pick the worst SKU pair — call it 2 automotive MCU SKUs sitting at 800 backlogged orders combined with an average order_revenue_usd of $45,000 per order.

> *800 backlogged orders × $45K average revenue = $36M of exposed revenue on two SKUs alone. At a leading-edge gross margin of 50%, that's $18M of gross profit on the wrong side of the wafer-start commit. If we pre-build 5 of these SKUs at $10-15M of inventory carrying cost per cycle, the payback is 6-8 weeks of unblocked Tier-1 shipments. On the other side, the 6 SKUs with forecast accuracy below 60% and weeks_of_supply above 16 are write-down candidates at the next quarter close — call that a $5-10M E&O reserve we are choosing to take instead of doubling down.*

> That's the decision this space automates. Not the slide. The decision. The wafer-start commit is built on backlog dollars and forecast bias, not on the loudest sales VP. Five SKUs get pre-built, five customer commitments get renegotiated, six SKUs get flagged for write-down — in one conversation, with one set of numbers.

### Question (Act 2.3)

> **How has total units ordered trended monthly by product category — is book-to-bill turning?**

**What to say while it runs:** Now weeks_of_supply below 4 by SKU — these are the stockout-risk SKUs where we'll lose the order if we don't allocate wafer starts this week. Healthy WOS is 8-16; under 4 is a hard escalation.

**What to look for:** A list of SKUs from inventory_positions with weeks_of_supply < 4 and committed_units exposure. The committed_units column is the dollars-at-risk multiplier.

**Land the point:** That comparison is the difference between knowing supply is tight and knowing which Tier-1 customer is going to call angry on Friday. The first is a status report; the second is a wafer-start commit.

---

## Act 3 — The commitment — shaping next cycle's wafer-start mix and the customer-segment portfolio *(≈4 min)*

**Persona:** CFO partner • **Job to be done:** Defend the wafer-start commit and the write-down exposure to the audit committee and the board, and lock in the customer-segment mix for next year's revenue plan.

*The CFO doesn't need more dashboards; they need backlog exposure, forecast bias, and weeks-of-supply in the same governed language as the engineer's morning watchlist — so the quarterly close narrative writes itself.*

### Question (Act 3.1)

> **Which SKUs have less than 4 weeks of supply this month and are at stockout risk?**

**What to say while it runs:** Monthly total_units_ordered by product_category over 12 months is the book-to-bill picture. When Microcontroller and Memory turn opposite directions, that IS the cycle — and the CFO needs that chart in the earnings prep deck six weeks before the call.

**What to look for:** Monthly trend across the 5 categories, DATE_TRUNC('month', order_date) shape. Inflection points by category are what shape next year's wafer-start mix.

**Land the point:** When this curve is in the CFO's hand a quarter before the print, the audit committee conversation moves from defensive to programmatic — and the board stops getting surprised at year-end.

### Question (Act 3.2)

> **What is the total forecasted vs actual units in the trailing 6 months, and which categories are chronically Over or Under?**

**What to say while it runs:** Trailing 6-month total_forecasted_units vs total_actual_units by category with the forecast_bias label — Over, Under, or On Target. Chronic Over-forecast is where E&O reserve goes up; chronic Under-forecast is where revenue is left on the table.

**What to look for:** Side-by-side bars from forecast_accuracy_metrics. Categories tagged 'Over-forecast' for 3+ months in a row are the write-down candidates; 'Under-forecast' for 3+ months are the wafer-start opportunity.

**Land the point:** Triage at 8 AM, allocation at 10, audit-committee narrative at 2. Same space. Same numbers. The Sales Ops backlog list and the CFO's forecast-bias story are now the same artifact — and the executive team gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — ChipFlow Supply — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 SKUs have the highest backlogged order count, and what is our exposed revenue?
2. Show monthly total order revenue by customer segment for the trailing 12 months.
3. Which product categories have the worst forecast accuracy this quarter — where do we need model retraining?
4. Rank the 5 customer regions by average lead time — where is lead-time inflation worst?
5. How has total units ordered trended monthly by product category — is book-to-bill turning?
6. Which SKUs have less than 4 weeks of supply this month and are at stockout risk?
7. What is the total forecasted vs actual units in the trailing 6 months, and which categories are chronically Over or Under?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
