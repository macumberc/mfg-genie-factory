# StockSmart Distribution — Demo Script

**Space:** Industrial Distribution — StockSmart Distribution - Inventory Optimization 📦
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Operations + CFO, Branch Manager, Supply Planner
**KPIs touched:** Inventory turnover ratio, Fill rate, Days of supply, Stockout rate / days, Carrying cost, Inventory value at risk
**Big decision automated:** Which warehouse-product combos get depleted vs. restocked this cycle, which slow-moving SKUs come off the catalog as write-offs, and how much working capital gets released from the next inventory budget.

---

## Pre-demo checklist

- Open the Genie space `StockSmart Distribution - Inventory Optimization 📦`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> StockSmart Distribution carries 20 warehouse-product combinations across pipe fittings, power tools, abrasives, cutting tools, and welding consumables in 3 distribution centers. Today the days-of-supply by SKU lives in a Branch Manager's WMS export, the slow-mover write-off candidate list is a Supply Planner's quarterly Excel, and the carrying-cost vs. turnover P&L is rebuilt by the CFO's office every quarter. Three artifacts, same warehouses — and the SKU-rationalization decision drags from quarter to quarter because nobody can agree on which SKUs are truly slow-moving vs. which are slow because we keep stocking them in the wrong DC. This space ends that. One governed surface that turns yesterday's WMS feed into the *deplete-or-restock, delist-or-keep, rebalance-or-reduce* call before the working-capital review hits the CFO's desk.

---

## Key KPIs in scope

- Inventory turnover ratio — industrial distribution benchmark 4-6 turns/year (best-in-class 6-8)
- Fill rate (%) — MRO target ≥97%
- Days of supply (DOH) — typically 30-60 days for fast movers, flag >120 as slow-moving
- Stockout rate / days — direct lost-sales indicator
- Carrying cost ($) — typically 20-30% of average inventory value annually
- Inventory value at risk — overstock and obsolete SKU exposure
- Below-reorder-point SKU count — replenishment urgency signal
- GMROI proxy — turnover-driven gross-margin return on inventory investment

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **DOH** | Days On Hand |
| **MRO** | Maintenance, Repair & Overhaul |
| **SKU** | Stock Keeping Unit |

---

## Act 1 — The signal — finding the turnover problems and the stockout bleed *(≈4 min)*

**Persona:** Branch Manager • **Job to be done:** Locate the categories where turnover is structurally low and the warehouse-product combos taking the most stockout days — before the next branch review starts on the wrong issues.

*This is the start of a real branch review. Two questions in, the Branch Manager has the turnover-by-category and stockout-by-combo lists that used to take a half-day of WMS reconciliation.*

### Question (Act 1.1)

> **Show monthly inventory turnover ratio by product category for the trailing 12 months.**

**What to say while it runs:** Monthly inventory turnover by category for the trailing 12 months. Industrial distribution benchmark is 4-6 turns per year; best-in-class is 6-8. Categories chronically running below 4 turns are either over-stocked structurally or slow-moving SKUs we should be questioning at the catalog level.

**What to look for:** Monthly trend on `avg_turnover_ratio` by `product_category`. Categories with a flat-low line are structural; categories that recently dropped are the new problem.

**Land the point:** Now turnover is the same number Operations and Finance both see, with the same definition. The 'we should improve turnover' conversation stops being a goal and starts being a category-by-category action list.

### Question (Act 1.2)

> **Top 10 warehouse-product combos with the most stockout days over the last 90 days.**

**What to say while it runs:** Top 10 warehouse-product combos with the most stockout days over the last 90 days. Stockout days are direct lost-sales. A combo with 15 stockout days in 90 is a combo where we're losing roughly one in six order requests — and the customer is finding it somewhere else.

**What to look for:** Ranked top-10 on `total_stockout_days` per `wp_id`. The DC × SKU pairs at the top are the safety-stock or rebalance candidates.

**Land the point:** That ranking is the actual stockout-fix list. The Branch Manager and the Supply Planner make the safety-stock-up vs. rebalance-between-DCs call on dollars-at-stake, not on whoever called the regional VP last.

---

## Act 2 — The decision — delist, deplete, or restock *(≈4 min)*

**Persona:** Supply Planner • **Job to be done:** Decide which SKUs get the next stocking reorder, which warehouse-product combos get depleted and rebalanced, and which slow-movers get delisted with a write-off.

*Three questions that turn the inventory position into a defensible SKU-rationalization commitment. The middle question is the anchor — the days-of-supply to carrying-cost conversion that decides how much working capital is locked vs. released.*

### Question (Act 2.1)

> **Which warehouses have average days-of-supply above 120, and what is their total carrying cost?**

**What to say while it runs:** Warehouses with average days-of-supply above 120 and their total carrying cost. Days-of-supply above 120 on industrial SKUs is the overstock signal — typically 30-60 days is healthy for fast-movers. Carrying cost runs 20-30% of inventory value annually, so DOH above 120 on a $1M SKU position is $200-300K of carrying cost on inventory that isn't moving.

**What to look for:** Aggregate by `warehouse` on `avg_days_of_supply` with `total_carrying_cost`. Warehouses with DOH > 120 and high carrying cost are the depletion candidates.

**Land the point:** That list is the actual depletion-and-rebalance plan for next cycle. The Supply Planner picks which DC carries which categories on real carrying-cost math — and working capital gets released without breaking the fill-rate commitment.

### Question (Act 2.2)

> **How has fill rate trended month-over-month by warehouse across the network?**

**What to say while it runs:** Fill rate trended month-over-month by warehouse across the network. Industrial MRO target is 97%. A warehouse that drifted from 97% to 92% lost roughly 5% of fulfillment to stockout — and that's the warehouse where safety stock needs to come up, not down, even while we're depleting elsewhere.

**What to look for:** Monthly `avg_fill_rate` by `warehouse`. Watch for the warehouse where the line dropped — that's the safety-stock increase candidate, the inverse of the depletion list.

**Land the point:** The deplete-this-warehouse and restock-that-one call usually arrives in two separate meetings. Now it's one chart — and the rebalance plan is the joint output instead of the compromise.

> **Anchor moment.** Stop on the DOH-above-120 list and the Reduce-flagged categories on screen. Pick the worst case — say $4M of inventory sitting at 140 DOH across 4 categories carrying $1M of annual carrying cost.

> *Releasing 30 days of inventory from a $4M overstocked position is $1M of working capital recovered with no top-line impact. Carrying cost on that $1M at the industry standard 25% is $250K per year of P&L savings. Pair that with the slow-mover write-off — even taking a $200K one-time charge to delist 18 SKUs unlocks the $500K of carrying cost on those SKUs going forward. Net: about $1.5M of working capital released *and* $750K of annual P&L improvement from one cycle of disciplined SKU action.*

> That's the decision this space automates. Not the working-capital review. The action. The slow-mover delist list gets approved Tuesday, the DC rebalance runs Friday, and the CFO's working-capital target moves down by $1.5M without anyone touching the topline.

### Question (Act 2.3)

> **Which product categories were flagged for the 'Reduce' optimization action most often last quarter?**

**What to say while it runs:** Product categories flagged for the Reduce optimization action most often last quarter. Reduce is the model's recommendation that we're carrying too much and turnover doesn't justify it. The categories where Reduce shows up consistently are the SKU-rationalization candidates — the ones where the slow-mover write-off conversation finally has the data behind it.

**What to look for:** Aggregate by `product_category` filtered on `optimization_action='Reduce'`. The top 2-3 categories are this quarter's delist-and-write-off candidates.

**Land the point:** That table *is* the SKU-rationalization committee agenda. The 'we should kill some SKUs' goal becomes 'here are 18 SKUs across 3 categories with the carrying-cost math attached, here's the proposed write-off.' The decision lands instead of cycling for another year.

---

## Act 3 — The commitment — locking the SKU portfolio and the GMROI target *(≈4 min)*

**Persona:** VP of Operations (with CFO) • **Job to be done:** Defend the inventory investment to the executive team and lock the next-cycle SKU portfolio, the safety-stock policy, and the GMROI commitment.

*The VP doesn't need another carrying-cost slide; they need the same inventory-value and turnover numbers the planning team is acting on, in the same language, so the working-capital target and the catalog-rationalization decision both anchor on one source.*

### Question (Act 3.1)

> **Top 10 SKUs by inventory value (on_hand_qty * unit_cost_usd) — and what is their turnover ratio?**

**What to say while it runs:** Top 10 SKUs by inventory value with their turnover ratio. Inventory value × turnover is the GMROI proxy — high value at high turnover is the working-capital ROI; high value at low turnover is the working-capital trap. The bottom of this list is where the next write-off conversation goes.

**What to look for:** Rank by `on_hand_qty * unit_cost_usd` with `turnover_ratio` beside. SKUs with high value and turnover under 3 are the structural write-off candidates; SKUs with high value and turnover above 8 are where we lean in.

**Land the point:** That's the actual GMROI ranking. The VP walks into the working-capital committee with the SKU-by-SKU evidence, the CFO sees the same numbers, and the inventory-investment target stops being a top-down ask and starts being a SKU-portfolio commitment.

### Question (Act 3.2)

> **Which warehouse-product combos are currently below reorder point, and how many units of supply remain?**

**What to say while it runs:** Warehouse-product combos currently below reorder point with units of supply remaining. This is the replenishment urgency list — combos where the next stockout is hours or days away. The combos here are the ones the VP needs to know about before the regional sales call.

**What to look for:** Filter on `on_hand_qty < reorder_point` from `inventory_transactions` ordered by `days_of_supply`. The top of the list is the urgent-action queue.

**Land the point:** Replenishment-urgency used to arrive in the form of a regional manager calling the VP. Now the VP sees it before the regional manager — and the conversation goes from reactive ('what happened?') to proactive ('here's what's already done'). That's the operating discipline that earns the next budget cycle.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — StockSmart Distribution — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly inventory turnover ratio by product category for the trailing 12 months.
2. Top 10 warehouse-product combos with the most stockout days over the last 90 days.
3. Which warehouses have average days-of-supply above 120, and what is their total carrying cost?
4. How has fill rate trended month-over-month by warehouse across the network?
5. Which product categories were flagged for the 'Reduce' optimization action most often last quarter?
6. Top 10 SKUs by inventory value (on_hand_qty * unit_cost_usd) — and what is their turnover ratio?
7. Which warehouse-product combos are currently below reorder point, and how many units of supply remain?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
