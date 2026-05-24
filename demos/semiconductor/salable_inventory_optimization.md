# WaferVault Systems — Demo Script

**Space:** Semiconductor — WaferVault - Salable Inventory Optimization 📦
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Supply Chain VP, alongside Inventory Planning and Operations
**KPIs touched:** Inventory turns, Days of supply, Excess exposure, Obsolete exposure, Fill rate %, Inventory value
**Big decision automated:** Which 5 die-bank SKUs to push to distribution this quarter vs. hold for premium customers, which products to write down before quarter close, and where to size the next E&O reserve disclosure.

---

## Pre-demo checklist

- Open the Genie space `WaferVault - Salable Inventory Optimization 📦`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> WaferVault Systems holds inventory across wafer bank, die bank, WIP, and finished-goods stages for 20 products and multiple warehouse locations. Today the daily transaction feed lives in SAP, the weekly aging snapshots live in Inventory Planning's Power BI export, and the monthly turns, E&O exposure, and fill-rate KPIs land on the CFO's working-capital review. Three systems, one quarter — and the last cycle turn caught $80M of die-bank inventory aging past 180 days that should have been pushed to distribution at $0.80 on the dollar three months earlier. Semi industry median turns are 3-4x; die-bank holding cost is 20-40% per year in obsolescence risk. This space ends the lag. One governed surface where the Supply Chain VP, CFO, and Inventory Planning see excess exposure, obsolete exposure, and aging in the same conversation that authorizes push-to-distribution, write-down, or strategic hold.

---

## Key KPIs in scope

- Inventory turns — annualized COGS / avg inventory; semi median 3–4x, top-quartile 5x+
- Days of supply — days to deplete at current demand; healthy 90–120, alarms above 180
- Excess exposure (USD) — value of inventory above demand cover; reserve trigger
- Obsolete exposure (USD) — value of E&O write-down candidates; CFO disclosure item
- Fill rate % — share of demand shipped on time; target 95%+
- Inventory value (USD) — working-capital tied up across stages
- Available-to-sell units — uncommitted salable inventory by SKU
- Scrap transaction count — yield loss and obsolescence signal

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **SKU** | Stock Keeping Unit |
| **VP** | Vice President |
| **WIP** | Work In Process |

---

## Act 1 — The signal — where working capital is trapped and how fast it's aging *(≈4 min)*

**Persona:** Inventory Planning lead • **Job to be done:** Surface the products with the most excess exposure and the warehouse locations where inventory value is concentrating, before the weekly working-capital call.

*This is where the push-to-distribution conversation actually starts — not in the CFO's review, but in the excess_exposure_usd line. Two questions in, the planner has the at-risk dollars by product and the warehouse-level inventory shape ready for the VP.*

### Question (Act 1.1)

> **Which 10 products have the highest excess exposure in USD this month?**

**What to say while it runs:** Top 10 products by excess_exposure_usd this month — that's the value of inventory sitting above demand cover that triggers the E&O reserve question. In semis, die-bank holding cost compounds at 20-40% a year, so excess that ages past 90 days starts becoming write-down material.

**What to look for:** Ranked table from inventory_kpi_monthly with excess_exposure_usd. The top 5 names are the candidates for the push-to-distribution decision the VP is sizing.

**Land the point:** Right there is the working-capital conversation. Now the planner can name the 5 products that need a distribution push in minutes — that's the inventory-action authorization that used to require a Friday MRP committee.

### Question (Act 1.2)

> **Show monthly total inventory value by warehouse location for the trailing 12 months.**

**What to say while it runs:** Monthly total_inventory_value_usd by warehouse_location over 12 months. If a single hub keeps growing while shipments are flat, that's a position imbalance — the inventory is in the wrong warehouse, and rebalancing has to come before any push or write-down.

**What to look for:** Monthly trend, DATE_TRUNC('month', snapshot_date) shape, broken out by warehouse_location from inventory_snapshot_metrics. Watch for hubs where the line is climbing while consumption stays flat.

**Land the point:** Before this space, that chart was rebuilt for every quarterly review out of SAP and Power BI. Now Inventory Planning opens with it — and the rebalancing conversation starts hours before the Supply Chain VP standup.

---

## Act 2 — The decision — push to distribution, hold for premium, or write down *(≈4 min)*

**Persona:** Supply Chain VP • **Job to be done:** Commit the inventory actions this week — which die-bank SKUs go to distribution at discount, which stay held for premium customers, and which products move to E&O write-down.

*Three questions that turn the working-capital watchlist into a defensible inventory-action plan. The middle question is the anchor — the obsolete-exposure to E&O-reserve conversation that converts aging signals into CFO disclosure.*

### Question (Act 2.1)

> **Which product lines have the worst inventory turns this quarter — where is working capital trapped?**

**What to say while it runs:** Product lines with the worst inventory_turns this quarter — semi median is 3-4x and top-quartile is 5x+. Any product line stuck below 2x for two quarters in a row is working capital we are choosing to trap; that's a portfolio question, not a planning question.

**What to look for:** Ranked table from inventory_kpi_monthly with inventory_turns. The bottom 3 product lines are the ones the VP has to either accept a lower turn target on or actively decompose.

**Land the point:** That list used to be a quarterly working-capital memo authored by FP&A. Now it's the input to the next portfolio decision the VP is signing off on this week.

### Question (Act 2.2)

> **Top 10 products by obsolete exposure — what is the E&O reserve we should be carrying?**

**What to say while it runs:** Top 10 products by obsolete_exposure_usd — these are the names that drive the E&O reserve disclosure the CFO has to defend at quarter close. Anything inflecting upward 2 quarters in a row is a write-down committee item, not a sales-discount question.

**What to look for:** Ranked table from inventory_kpi_monthly with obsolete_exposure_usd. The dollars sum to the reserve number the audit committee will see.

**Land the point:** When Inventory Planning, the VP, and the CFO all query obsolete exposure the same way and see the same number, the meeting stops being whose aging report is current and starts being how much E&O hits the income statement next quarter.

> **Anchor moment.** Stop on the obsolete-exposure table and the scrap-by-stage chart on screen. Pick the worst case — call it 5 die-bank SKUs sitting on $60M of obsolete_exposure_usd with aging_bucket past 180 days and inventory_turns below 1.5x.

> *Die-bank obsolescence cost compounds at 20-40% annually; call it 30% on $60M, that's $18M of write-down risk we are absorbing if we sit still. Pushing 3 of those SKUs to distribution at $0.80 on the dollar recovers $48M of cash against a $12M margin haircut — net $36M of working capital freed, vs. a near-certain $18M write-down. The remaining 2 SKUs, both flagship parts, get held for premium customers at full margin because forecast actuals support the hold. Across the broader portfolio, the products with days_of_supply above 180 and obsolete_exposure flagged are a $30-50M E&O reserve we now disclose proactively at the quarter close, ahead of the audit — sized once, defended once.*

> That's the decision this space automates. Not the slide. The decision. Three SKUs pushed to distribution Monday, two held for the flagship customer, $40M of E&O reserve sized and disclosed — in one conversation, with one set of numbers, before the audit committee walks in.

### Question (Act 2.3)

> **How has scrap transaction count trended monthly by stock stage — where are we losing yield to scrap?**

**What to say while it runs:** Now monthly scrap_transaction_count by stock_stage — wafer bank vs. die bank vs. WIP vs. finished goods. Scrap concentrating in die bank is yield-loss bleeding into salable inventory; scrap concentrating in finished goods is a forecast-and-position issue. Different problem, different action.

**What to look for:** Monthly trend of scrap_transaction_count from inventory_transaction_metrics, by stock_stage. The stage with the rising line is where the operational root cause has to land.

**Land the point:** That comparison is the difference between knowing scrap is up and knowing where the dollars are going. The first is a status report; the second is a corrective-action authorization.

---

## Act 3 — The commitment — shaping next quarter's E&O reserve and the position policy *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the E&O reserve and the working-capital trajectory to the audit committee and lock in the inventory-policy floor for next fiscal year.

*The CFO doesn't need more BI; they need the excess, obsolete, and fill-rate numbers in the same governed language Inventory Planning is acting on — so the working-capital narrative and the position policy are the same artifact.*

### Question (Act 3.1)

> **Which products have more than 180 days of supply and aging-bucket >90 days — write-down candidates?**

**What to say while it runs:** Trailing 12-month fill_rate_pct by product line against the 95% target. Below 95% is revenue we are leaving on the table; above 98% is service-level over-investment that costs us in inventory turns. The product lines on either tail are where the position policy has to change.

**What to look for:** Ranked table from inventory_kpi_monthly with fill_rate_pct by product_line. Lines below 90% are the ones losing premium customers; lines above 98% are where we can pull working capital out.

**Land the point:** When this view is in the CFO's hand at the working-capital review, the audit committee conversation moves from defensive to programmatic — and the executive team stops being surprised at the quarterly E&O reserve.

### Question (Act 3.2)

> **What is the trailing 12-month fill rate by product line, and which lines are below the 95% target?**

**What to say while it runs:** Products with days_of_supply above 180 and aging_bucket past 90 days — the write-down candidate list. This is the disclosure the CFO has to be ready to defend at the quarter call, and surfacing it 6 weeks early changes the conversation from reactive to managed.

**What to look for:** Products from inventory_snapshots filtered on days_of_supply > 180 AND aging > 90 days. The dollar sum is the reserve floor.

**Land the point:** Triage at the planner's standup, push-or-hold decisions at the VP's review, audit-committee narrative at the quarter close. Same space. Same numbers. The Inventory Planning watchlist and the CFO's reserve disclosure are now the same artifact — and the audit committee gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — WaferVault Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 products have the highest excess exposure in USD this month?
2. Show monthly total inventory value by warehouse location for the trailing 12 months.
3. Which product lines have the worst inventory turns this quarter — where is working capital trapped?
4. Top 10 products by obsolete exposure — what is the E&O reserve we should be carrying?
5. How has scrap transaction count trended monthly by stock stage — where are we losing yield to scrap?
6. Which products have more than 180 days of supply and aging-bucket >90 days — write-down candidates?
7. What is the trailing 12-month fill rate by product line, and which lines are below the 95% target?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
