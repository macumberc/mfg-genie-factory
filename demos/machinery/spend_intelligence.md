# SpendLens Manufacturing — Demo Script

**Space:** Machinery — SpendLens Manufacturing - Spend Intelligence 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** Chief Procurement Officer + Category Manager, Sourcing Lead, CFO partner
**KPIs touched:** Realized savings, Maverick spend, On-time delivery, Quality acceptance, Contract compliance, PO cycle time
**Big decision automated:** Which 30% of the supplier base to rationalize off the AVL, which 5-7 contracts to renegotiate first this cycle, and where to set the maverick-spend escalation tripwire.

---

## Pre-demo checklist

- Open the Genie space `SpendLens Manufacturing - Spend Intelligence 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> SpendLens Manufacturing manages direct and indirect spend across hundreds of suppliers and dozens of spend categories. Today the Category Manager runs supplier scorecards in a quarterly Excel built from ERP exports, the Sourcing Lead keeps a 'renegotiation hit list' in a personal OneNote, and the CPO sees only roll-up savings numbers in finance's monthly KPI deck. Meanwhile, the long tail — the bottom 20% of suppliers — accounts for 80% of the supplier-master complexity and zero of the strategic value, but nobody can prove that without a week of pivot work. The result: contracts roll over because nobody had time to renegotiate, savings targets get set by extrapolation, and maverick spend leaks unmonitored. This space replaces that with one governed view where supplier scorecards, category spend, savings, and maverick-spend percentages all reconcile — and the tail-supplier consolidation decision becomes a 20-minute conversation, not a 6-month consulting project.

---

## Key KPIs in scope

- Realized savings ($) — typical 3–5% of addressable spend, leaders 5–8%
- Maverick spend (%) — leaders <5%, average 20–30%
- On-time delivery (%) — supplier target ≥95%
- Quality acceptance (%) — supplier target ≥98%
- Contract compliance (%) — target ≥85%
- PO cycle time (days) — efficiency lever, target <7 days
- Supplier diversity spend (%) — ESG and corporate-goal metric
- Cost avoidance ($) — value beyond hard savings

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **ESG** | Environmental, Social, Governance |

---

## Act 1 — The signal — where is procurement's leverage actually concentrated? *(≈4 min)*

**Persona:** Category Manager • **Job to be done:** Identify before the quarterly category review which categories deserve a structured sourcing event and which are already getting best-in-class savings.

*This is the moment the quarterly category-review prep starts. Two questions in, the manager has the spend concentration and the savings trend that used to require a week of ERP wrangling.*

### Question (Act 1.1)

> **Top 10 spend categories by total spend this year — where is procurement leverage concentrated?**

**What to say while it runs:** Categories ranked by total spend this year. The Pareto matters — typically 20% of categories account for 80% of spend, and those are the only categories where a sourcing event pays back inside a quarter. Categories outside the top 20% rarely justify a structured RFP unless there's a compliance lever.

**What to look for:** Ranked table from `spend_kpi_metrics` with `total_spend` by `spend_category`. Eye lands on the top 5 — that's the sourcing calendar for the next two quarters. Click *Show generated code* once so the room sees the metric view doing the work.

**Land the point:** That ranking is the sourcing-calendar conversation. Before this space, prioritization was an annual exercise that nobody fully trusted; now the Category Manager has the dollar-weighted priority in one query, and the disagreement about which RFP goes first ends before the meeting starts.

### Question (Act 1.2)

> **What is the monthly trend in realized savings vs maverick spend percentage over the trailing 12 months?**

**What to say while it runs:** Monthly trend in realized savings vs maverick spend percentage. Leaders run 5-8% realized savings against under 5% maverick; the average enterprise sits around 3% savings against 20-30% maverick. Both curves moving in the right direction means the sourcing strategy is working — diverging curves means a category is leaking somewhere.

**What to look for:** Two trend lines from `spend_kpi_metrics`: `total_savings` and `avg_maverick_pct`, monthly. Watch for the months where maverick climbs while savings flatten — that's the leak.

**Land the point:** Before this space, savings was a number finance produced once a quarter, and maverick spend was a number nobody owned. Now both are on the same chart, and the conversation about who is accountable for the leak happens in the room, not in the all-hands.

---

## Act 2 — The decision — tail-supplier rationalization and the renegotiation hit list *(≈4 min)*

**Persona:** Sourcing Lead • **Job to be done:** Commit on which 30% of the supplier base to consolidate off, which 5-7 contracts to renegotiate first, and where to escalate maverick-spend offenders.

*Three questions that turn the supplier base into a defensible consolidation and contract-prioritization recommendation. The middle question is the anchor — the maverick-spend-to-dollar conversion that funds the next sourcing year.*

### Question (Act 2.1)

> **Which suppliers have on-time delivery below the 95% target this quarter?**

**What to say while it runs:** Suppliers with on-time delivery below the 95% target this quarter. OTD under 95% on a strategic supplier is a contract-conversation; under 90% is a supplier-replacement conversation; under 80% is an SCAR-and-exit conversation. Industry data says one point of OTD improvement on direct materials is worth roughly 0.5% of category spend.

**What to look for:** Ranked table from `supplier_snapshots` filtered to `on_time_delivery_pct < 95`, with `spend_category` next to it. Watch for strategic-category suppliers in the under-80% tier — those are the immediate action items.

**Land the point:** Before this space, OTD was a quarterly conversation that ended in 'we'll talk to them.' Now the Sourcing Lead has the OTD-vs-spend matrix, and the supplier-exit decision is a budget item, not a footnote.

### Question (Act 2.2)

> **Rank spend categories by realized savings — which exceed the 5% best-in-class benchmark?**

**What to say while it runs:** Categories ranked by realized savings — which exceed the 5% best-in-class benchmark. Categories above 5% don't need more sourcing investment; they need protection. Categories under 3% are the ones where the next RFP will pay back. The middle is where you make the renegotiation tradeoffs.

**What to look for:** Ranked categories by `total_savings / total_spend` from `spend_kpi_metrics`. The eye should land on the categories below 3% — those are the renegotiation candidates for the next cycle.

**Land the point:** That ranking is the renegotiation calendar. The Sourcing Lead walks into the next sourcing council with a dollar-weighted contract slate, not a 'who screamed loudest' list.

> **Anchor moment.** Hold on the maverick-spend trend and the bottom-quartile categories view. Pick the worst category — call it $40M of total spend with 25% maverick, on a supplier base of 200 vendors where the bottom 60 vendors account for 4% of spend.

> *25% maverick on $40M is $10M of off-contract spend leaking annually on one category. Industry data says rationalizing the tail — dropping 30% of suppliers in a category — typically saves 12-18% on the addressable category spend. Take the middle: 15% × $10M = $1.5M of recoverable spend on this one category. Across the broader spend portfolio at SpendLens' scale, the tail-spend rationalization play is a $20-35M/year addressable opportunity. Layer the MRO contract renegotiation prioritization on top — another 8-15% on the categories below the 3% savings line — and the program is $50M+ of recoverable spend per year.*

> That's the decision this space automates. Not the supplier scorecard pdf. The decision. The tail-supplier exit list gets locked in with the dollar impact attached, the renegotiation calendar is signed off in one meeting, and the maverick-spend escalation tripwire moves from policy text to a measured threshold.

### Question (Act 2.3)

> **Show monthly trend in cost avoidance vs total spend across the supplier base.**

**What to say while it runs:** Monthly trend in cost avoidance vs total spend across the supplier base. Cost avoidance is the soft-savings number — should-cost wins, price-hold concessions, value-engineering benefits. Leaders run cost avoidance at 2-4% of spend on top of hard savings; without it, the supplier base is essentially passive.

**What to look for:** Two trend lines from `spend_kpi_metrics`: `total_cost_avoidance` and `total_spend`, monthly. Watch for the months where avoidance is flat — those are the months the sourcing team was processing POs instead of negotiating.

**Land the point:** Cost avoidance has historically been the number nobody trusts. When it's on the same governed surface as realized savings, the CPO can defend the soft-savings target to the CFO without a four-page methodology footnote.

---

## Act 3 — The commitment — the supplier portfolio and CPO board narrative *(≈4 min)*

**Persona:** Chief Procurement Officer • **Job to be done:** Defend the savings trajectory upstream and commit on the supplier portfolio reshape and category-priority list for the next year.

*The CPO has to tell the executive team a coherent story about realized savings, supplier risk, and category economics — and the supplier rationalization slate has to land in the same conversation as the savings forecast.*

### Question (Act 3.1)

> **Top 10 suppliers by supplier score — and how does that correlate with total spend?**

**What to say while it runs:** Top 10 suppliers by supplier score, and how that correlates with total spend. The healthy pattern is *high score paired with high spend* — that means we are concentrating volume with our best suppliers. The dangerous pattern is *high spend with mediocre score* — that's the concentration risk the CFO should ask about.

**What to look for:** From `supplier_snapshots`, top 10 suppliers ranked by `supplier_score` with `total_spend` next to it. The eye should pick out the *mismatches* — strategic suppliers with weak scores, or strong suppliers we're under-utilizing.

**Land the point:** When the CPO can show that the supplier portfolio is actively rebalancing toward the high-score vendors, the board conversation moves from 'are we saving enough' to 'are we taking the right risk' — and the supplier-strategy narrative finally has a numerical spine.

### Question (Act 3.2)

> **Which categories have the highest maverick spend percentage, and what is the off-contract dollar value?**

**What to say while it runs:** Categories with the highest maverick-spend percentage, alongside the off-contract dollar value. The combination matters — high maverick percentage on a low-spend category is a policy fix; high maverick on a high-spend category is a board-level governance issue.

**What to look for:** Ranked categories from `spend_kpi_metrics` by `avg_maverick_pct`, with `total_spend` and the implied off-contract dollars. The view to land on: the top-3 categories where the maverick dollars are over $1M each.

**Land the point:** Same space, same numbers — the Category Manager's leak chart and the CPO's board narrative are now the same artifact. The compliance team gets one number, the CFO gets one number, and the supplier rationalization decision goes from a wishlist to next month's signed contract amendments.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — SpendLens Manufacturing — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 spend categories by total spend this year — where is procurement leverage concentrated?
2. What is the monthly trend in realized savings vs maverick spend percentage over the trailing 12 months?
3. Which suppliers have on-time delivery below the 95% target this quarter?
4. Rank spend categories by realized savings — which exceed the 5% best-in-class benchmark?
5. Show monthly trend in cost avoidance vs total spend across the supplier base.
6. Top 10 suppliers by supplier score — and how does that correlate with total spend?
7. Which categories have the highest maverick spend percentage, and what is the off-contract dollar value?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
