# PartsVault Industrial — Demo Script

**Space:** Machinery — PartsVault Industrial - Spare Parts Optimization 📦
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Supply Chain + Inventory Planner, MRO Buyer, CFO partner
**KPIs touched:** Inventory turnover ratio, Fill rate / service level, Stockout events, Carrying cost, Days of supply, Emergency orders
**Big decision automated:** Which critical spares to stock locally vs. expedite on demand, which MRO suppliers to consolidate down to, and how to rebalance the parts fleet across the four warehouses.

---

## Pre-demo checklist

- Open the Genie space `PartsVault Industrial - Spare Parts Optimization 📦`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PartsVault Industrial holds spare-parts inventory across multiple categories and four regional warehouses serving the field-service fleet. Today the Inventory Planner runs ABC analysis in a quarterly Excel pivot, the MRO Buyer keeps a 'usual suspects' supplier list in Outlook contacts, and the VP Supply Chain only sees the working-capital number once a month in finance's cash deck. Meanwhile, a stockout on a critical bearing locks up a $2M customer asset for 24 hours and triggers an air-freight invoice nobody anticipated. The decision about which parts to stock vs. expedite, and which MRO suppliers deserve a long-term contract, gets made on whoever was burned most recently. This space replaces that with one governed view that ties turnover, fill rate, stockout events, and emergency-order premiums to the same parts and warehouses — so the carry-vs-expedite call becomes math, not memory.

---

## Key KPIs in scope

- Inventory turnover ratio — MRO benchmark 2–4x, leaders 6x+
- Fill rate / service level (%) — target ≥95% for critical spares
- Stockout events — direct downtime risk
- Carrying cost ($) — typical 20–30% of inventory value annually
- Days of supply — target 30–90 days for MRO
- Emergency orders — premium-cost indicator
- Inventory value ($) — working-capital tied up in spares
- Lead time (days) — supplier responsiveness benchmark

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MRO** | Maintenance, Repair & Overhaul |
| **VP** | Vice President |

---

## Act 1 — The signal — where is working capital trapped, and which parts are about to bite us? *(≈4 min)*

**Persona:** Inventory Planner • **Job to be done:** Identify before week-end which parts are over-stocked relative to turnover and which are flashing high stockout risk against critical-asset coverage.

*This is the moment the planner decides which reorder triggers to override and which to honor. Two questions in, the planner has the carrying-cost ranking and the turnover trend that used to require a Tuesday-morning pivot rebuild.*

### Question (Act 1.1)

> **Top 10 part categories by carrying cost — where is working capital tied up?**

**What to say while it runs:** Part categories ranked by carrying cost. Industry rule of thumb is 20-30% of inventory value per year — so a million-dollar bucket of slow-movers is costing us $200-300K just to sit on the shelf. The categories at the top of this list are the ones where every extra week of supply is a measurable cash drag.

**What to look for:** Ranked table from `inventory_kpi_metrics` with `total_carrying_cost` by `part_category`. The eye should land on the top 3 — usually one critical-spare bucket and two long-tail commodity buckets. Click *Show generated code* once so the room sees the metric view in action.

**Land the point:** That ranking is the working-capital release conversation. Before this space it was a quarterly finance exercise; now the planner can pull it before lunch and the next reorder-policy override is grounded in dollars, not hunches.

### Question (Act 1.2)

> **What is the monthly trend in inventory turnover ratio by category over the trailing 12 months?**

**What to say while it runs:** Now the trend in inventory turnover by category over 12 months. MRO benchmark is 2-4 turns per year; leaders hit 6 turns or more. The categories where the turnover line is *flat or declining* are the categories accumulating slow-movers — and slow-movers eventually become a write-down conversation.

**What to look for:** Monthly `avg_turnover` trend by category, `DATE_TRUNC('month', kpi_month)` shape. Watch for categories where the line has flattened below 2 turns — those are the candidates for either price-down/clearance or a write-down reserve.

**Land the point:** Before this space, the slow-mover write-down was an annual surprise in Q4. Now the planner can flag it a quarter ahead — and the CFO doesn't get blindsided in the close.

---

## Act 2 — The decision — stock locally, expedite on demand, or consolidate suppliers *(≈4 min)*

**Persona:** MRO Buyer • **Job to be done:** Commit on which critical spares move to local stock, which stay on expedite-from-central, and which MRO suppliers get consolidated into the next master agreement.

*Three questions that turn the daily reorder list into a defensible inventory and sourcing strategy. The middle question is the anchor — the stockout-to-downtime-dollar conversion that justifies the local-stock investment.*

### Question (Act 2.1)

> **Which parts are currently at High stockout risk with days of supply under 30?**

**What to say while it runs:** Parts currently at High stockout risk with under 30 days of supply. 30 days is the MRO floor most asset-heavy operators run — anything below that on a Critical-class part is one supplier hiccup away from an AOG-equivalent event in the field.

**What to look for:** A filtered view of `inventory_snapshots` where `stockout_risk = 'High'` and `days_of_supply < 30`. Look at `inventory_value_usd` next to it — the high-risk *and* high-value parts are the ones to expedite first.

**Land the point:** That list used to be the planner's mental backlog. Now it's the agenda for the Monday MRO call — and the conversation about whether to pre-position a $50K bearing at the West warehouse is grounded in days-of-supply, not narrative.

### Question (Act 2.2)

> **Rank part categories by total stockout events this quarter — which are hurting MRO service?**

**What to say while it runs:** Part categories ranked by total stockout events this quarter. Each stockout on a critical spare typically means 4-24 hours of customer asset downtime depending on the part — and the field-service contract usually has a $X/hour SLA penalty attached.

**What to look for:** Ranked categories by `total_stockouts` from `inventory_kpi_metrics`. The eye lands on categories with both high stockout count AND high carrying cost — those are the ones where the policy is wrong, not the volume.

**Land the point:** The stockout-event ranking is the difference between *feeling* we have an MRO service problem and *knowing* which categories are responsible for it. The MRO buyer walks into the next supplier review with the receipts.

> **Anchor moment.** Hold on the stockout-by-category ranking and the carrying-cost view. Pick the worst combination — say, 40 stockout events this quarter on a critical-bearing category, with each event causing 8 hours of customer-asset downtime.

> *40 stockouts × 8 hours per event = 320 hours of downtime. At $5,000/hour of customer-asset value at risk on industrial equipment (towards the conservative end — heavy-equipment customers pay $10-50K/hour for line shutdowns), that's $1.6M of customer impact per quarter, or roughly $6M/year. The local-stock investment to eliminate 80% of these stockouts is in the $400-700K working-capital range — payback inside one quarter. And the MRO-supplier consolidation play on top of that is 10-20% savings on the addressable category spend — another $2-4M/year on a $20M MRO base.*

> That's the decision this space automates. Not the inventory report. The decision. Local-stock policy gets rewritten on dollars, the MRO supplier consolidation moves from a project on the wishlist to a signed master agreement, and the field-service team stops paying air-freight ransoms.

### Question (Act 2.3)

> **Show monthly trend in emergency orders vs total parts transactions.**

**What to say while it runs:** Monthly trend in emergency orders vs. total parts transactions. Emergency orders carry a 30-100% premium over standard freight. If the emergency-order ratio is climbing, two things are true: the planning system is reacting instead of anticipating, AND the freight P&L is bleeding.

**What to look for:** Two trend lines from `parts_transactions_metrics`: `emergency_issues` and `total_transactions`, monthly. The ratio matters more than the absolute count — a rising ratio is the early warning that policy is broken.

**Land the point:** When the emergency-order ratio is on the same screen as the stockout count, the parts buyer can finally argue *which* of the two to fix first — and the consolidate-to-fewer-suppliers conversation gets data, not relationships, behind it.

---

## Act 3 — The commitment — the parts-fleet rebalance and supplier consolidation slate *(≈4 min)*

**Persona:** VP Supply Chain • **Job to be done:** Defend the working-capital plan upstream and commit on the parts-fleet rebalance and MRO supplier consolidation for the next fiscal cycle.

*The VP needs the same parts, the same warehouses, and the same fill-rate numbers the planner is using — expressed in the language of working capital, service level, and supplier portfolio.*

### Question (Act 3.1)

> **Top 10 parts by emergency-order frequency, and what is the lead-time gap versus standard orders?**

**What to say while it runs:** Top 10 parts by emergency-order frequency, with the lead-time gap versus standard orders. Emergency lead time on a critical bearing might be 2 days versus a 4-week standard order — that gap is the cost of a broken planning policy on those specific parts.

**What to look for:** Top-10 parts from `parts_transactions` filtered to `urgency = 'Emergency'`, joined to `avg_lead_time_days` for the standard lead time on the same part. The bigger the gap, the worse the policy on that part.

**Land the point:** The VP can now point to specific part numbers — not categories, not narratives — and say *these* are the parts moving to local stock next quarter. The MRO consolidation conversation has names, not categories.

### Question (Act 3.2)

> **Which categories have fill rate below the 95% target, and what is the underlying inventory value?**

**What to say while it runs:** Categories with fill rate below the 95% target, alongside their inventory value. The categories with low fill rate AND low inventory value are under-invested — easy fix. The categories with low fill rate AND high inventory value have the wrong parts in stock — the harder conversation.

**What to look for:** Ranked categories from `inventory_kpi_metrics` filtered to `avg_fill_rate < 95`, with the matching `inventory_value_usd` from snapshots. The eye should pick out categories where high investment is producing low service — those are the wrong-mix candidates.

**Land the point:** Same space, same numbers — the planner's reorder watchlist and the VP's working-capital plan are now the same artifact. The board sees one story about where the $5M of trapped MRO cash gets released, and which suppliers carry the next contract cycle.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PartsVault Industrial — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 part categories by carrying cost — where is working capital tied up?
2. What is the monthly trend in inventory turnover ratio by category over the trailing 12 months?
3. Which parts are currently at High stockout risk with days of supply under 30?
4. Rank part categories by total stockout events this quarter — which are hurting MRO service?
5. Show monthly trend in emergency orders vs total parts transactions.
6. Top 10 parts by emergency-order frequency, and what is the lead-time gap versus standard orders?
7. Which categories have fill rate below the 95% target, and what is the underlying inventory value?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
