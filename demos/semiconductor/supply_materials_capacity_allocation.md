# CapAlloc Semi — Demo Script

**Space:** Semiconductor — CapAlloc - Supply & Capacity Allocation 🔗
**Runtime:** ~15 minutes • 7 questions
**Audience:** COO + CFO, alongside Procurement and Supply Chain leads
**KPIs touched:** Fab utilization %, Wafer starts, Material lead time, Delayed order count, Reject rate %, Plan adherence %
**Big decision automated:** Which fab line dedicates to which product family next quarter, which single-source EUV materials trigger an emergency second-source qualification, and which SKU moves foundry-vs-IDM in the next sourcing review.

---

## Pre-demo checklist

- Open the Genie space `CapAlloc - Supply & Capacity Allocation 🔗`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CapAlloc Semi sources 20 materials (silicon wafers, photoresists, gases, sputtering targets, EUV consumables) into multiple fab lines, with capacity allocation reshuffles worth $50-500M of quarterly revenue at supply-constrained leaders. Today the supplier PO and quality reject data live in Ariba and the QMS, the weekly fab-line utilization and bottleneck classification live in the MES + a Procurement Excel, and the monthly allocation plan and procurement spend sit in the Supply Chain VP's S&OP deck. Three systems, one allocation cycle — and last quarter the team over-committed Fab Line 2 to a consumer product while the flagship automotive SKU sat on critical bottleneck because the EUV consumable lead time inflated from 60 to 120 days and nobody saw the inflection until the monthly review. EUV-gas single-source risk plus fab-line plan adherence below 95% is the combination that loses sockets. This space ends that. One governed surface where the COO, Procurement, and the CFO see lead times, utilization, and bottlenecks in the same conversation that sets fab-line dedication and make-buy.

---

## Key KPIs in scope

- Fab utilization % — consumed vs available wafer starts; world-class 85–90%, >95% signals risk of breakage
- Wafer starts (weekly) — capacity throughput baseline
- Material lead time (days) — supplier responsiveness; EUV-related gases often 90+ days
- Delayed order count — supplier-on-time exposure
- Reject rate % — incoming quality issues, target <1%
- Plan adherence % — allocation discipline vs commit; target 95%+
- Procurement spend (USD) — direct materials COGS line
- Critical bottleneck count — fab lines flagged as capacity-constrained

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **COO** | Chief Operating Officer |

---

## Act 1 — The signal — which suppliers are slipping and which fab lines are above the breakage line *(≈4 min)*

**Persona:** Procurement lead • **Job to be done:** Identify the suppliers with rising delayed_order_count and the fab lines pushing utilization above 95% before the weekly S&OP review.

*This is where the allocation conversation actually starts — not in the S&OP deck, but in the delayed_order_count and utilization_pct lines. Two questions in, the Procurement lead has the supplier risk list and the over-utilized fab lines ready for the COO.*

### Question (Act 1.1)

> **Rank suppliers by delayed order count in the trailing 12 months — which carry the most on-time risk?**

**What to say while it runs:** Top 10 suppliers by delayed_order_count over 12 months — these are the names carrying the most on-time risk into the next quarter. EUV-related gases and photoresists typically run 90+ days lead time even healthy; any slippage compounds across the wafer-start schedule.

**What to look for:** Ranked table from material_order_metrics with delayed_order_count and total_order_value_usd. The dollar column is the criticality multiplier — a small supplier with 50 delays matters less than a strategic supplier with 10 delays.

**Land the point:** Right there is the supplier-risk conversation. Now Procurement can name the 3 suppliers that need an emergency review in minutes — that's the second-source qualification authorization that used to require a 90-minute steering committee.

### Question (Act 1.2)

> **Show monthly fab utilization by fab line for the trailing 12 months — where are we above 95%?**

**What to say while it runs:** Monthly avg_utilization_pct by fab_line over 12 months — target is 85-90% world-class; above 95% signals risk of breakage and tool-stress yield loss. A fab line above 95% for 3+ months in a row is a capex conversation, not an allocation conversation.

**What to look for:** Monthly trend by fab_line from capacity_utilization_metrics. Watch for the lines sitting above the 95% threshold — those are next quarter's capex committee agenda.

**Land the point:** Before this space, that chart was assembled out of the MES and a Procurement Excel on Sunday night for the Monday S&OP. Now the Procurement lead opens with it — and the fab-line capex conversation starts in the standup, not in the steering committee.

---

## Act 2 — The decision — fab-line dedication, second-source qualification, and make-buy *(≈4 min)*

**Persona:** COO • **Job to be done:** Commit the next-quarter fab-line dedication, authorize emergency second-source qualification on critical EUV materials, and tee up the make-buy decision for the next sourcing review.

*Three questions that turn the supplier-and-utilization watchlist into a defensible allocation plan. The middle question is the anchor — the lead-time and procurement-spend conversation that converts category risk into a quarterly capacity commit.*

### Question (Act 2.1)

> **Which material categories have the longest average lead times — which are single-source risks?**

**What to say while it runs:** Material categories with the longest avg_lead_time_days — EUV consumables and advanced photoresists are typically single-source and lead times above 90 days are the norm. Any category creeping past 120 days while we have flagship product on it is an emergency second-source qualification.

**What to look for:** Ranked material_category list from material_order_metrics with avg_lead_time_days. The single-source categories at the top are the ones the COO's risk committee has to retire.

**Land the point:** That list used to be a quarterly sourcing review printout. Now it's the input to the emergency-qualification authorization the COO signs Friday.

### Question (Act 2.2)

> **Top 10 materials by total procurement spend this quarter, and how does that compare to last quarter?**

**What to say while it runs:** Top 10 materials by total_order_value_usd this quarter alongside last quarter — the procurement spend trajectory tells us where category management has to focus and where the make-buy conversation belongs. Materials inflecting upward in spend while quality_result rejects are climbing is the worst combination.

**What to look for:** Side-by-side bars from material_order_metrics with this quarter vs. last quarter. The deltas show where supplier negotiation capacity goes this cycle.

**Land the point:** When Procurement, the COO, and the CFO all query procurement spend the same way and see the same number, the meeting stops being whose Ariba report is current and starts being which SKUs go foundry-vs-IDM in the next sourcing review.

> **Anchor moment.** Stop on the lead-time-by-category table and the procurement-spend ranking on screen. Pick the worst combination — call it EUV consumables at 130-day avg lead time with $200M of trailing spend, while Fab Line 2 sits at 97% utilization carrying the flagship automotive SKU.

> *A capacity reshuffle on the flagship line moves $50-500M of quarterly revenue depending on how the wafer starts redistribute; call it $150M of revenue exposure on the worst-case allocation miss. Emergency-qualifying a second EUV gas supplier costs $5-10M and takes 6-9 months — but it retires the single-source risk that's currently gating $600M of annual flagship revenue. Foundry-vs-IDM on one constrained SKU shifts about $80M of capex into variable cost — the right call if utilization can be maintained at 90%+ on the freed-up internal capacity by reallocating a consumer family in. Across the portfolio, the right move is: dedicate Fab Line 2 to the automotive flagship, qualify a second EUV supplier on 9-month aggressive timeline, move one consumer SKU to TSMC at $40-60M annualized premium, and reauthorize $30M of capex on the line that's been critical-bottleneck for 4 consecutive months.*

> That's the decision this space automates. Not the slide. The decision. One fab line dedicated, one second-source qualified, one SKU moved to foundry, $30M of capex committed — in one conversation, with one set of numbers, before the COO walks into the board meeting.

### Question (Act 2.3)

> **How has critical bottleneck count trended monthly by fab line — which lines need capex?**

**What to say while it runs:** Now monthly critical_bottleneck_count by fab_line — a bottleneck_status = 'Critical' classification means the line is gating a product family. A fab line trending critical for 2+ months is where the next $50-200M of capex has to be authorized or the product family has to be reallocated to a different line.

**What to look for:** Monthly trend of critical_bottleneck_count from capacity_utilization_metrics, by fab_line. The lines that stay critical month over month are next year's capex priority.

**Land the point:** That comparison is the difference between knowing a fab line is busy and knowing it's structurally constrained. The first is an ops metric; the second is a capex authorization.

---

## Act 3 — The commitment — shaping next year's supply chain and the fab capex plan *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the supply-chain risk posture and the fab capex to the board, and lock in the supplier and capacity policy for the next fiscal year.

*The CFO doesn't need more dashboards; they need lead-time, utilization, and supplier-quality numbers in the same governed language Procurement is acting on — so the board narrative and the next sourcing review become the same artifact.*

### Question (Act 3.1)

> **Which suppliers have the highest reject rate — where do we have quality exposure?**

**What to say while it runs:** Suppliers with the highest rejected_order_count — these are the quality-exposure names that drive incoming material reject rates above 1%. A supplier with rising rejects is one bad lot away from a fab excursion; defending that risk to the board requires the second-source plan and the qualification dollars committed.

**What to look for:** Ranked table from material_order_metrics with rejected_order_count and total_order_value_usd. The highest-spend, highest-reject combinations are the most urgent disqualification conversations.

**Land the point:** When this view is in the CFO's hand before the board meeting, the supply-chain risk discussion moves from reactive to programmatic — and the executive team stops being told about supplier excursions after they happen.

### Question (Act 3.2)

> **What is the trailing 6-month plan adherence percentage by material category, and which categories are below the 95% target?**

**What to say while it runs:** Trailing 6-month plan_adherence_pct by material category against the 95% target. Below 95% means the allocation plan we committed at the start of the quarter didn't hold — that's either a forecast issue, a supplier issue, or a fab-line issue, and the data tells us which one.

**What to look for:** Ranked table from allocation_monthly with plan_adherence_pct by material_category. Categories chronically below 90% are next quarter's allocation-discipline focus.

**Land the point:** Triage at the standup, allocation decisions at the S&OP, board narrative at the capex committee. Same space. Same numbers. The Procurement watchlist and the CFO's capex pitch are now the same artifact — and the board gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CapAlloc Semi — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Rank suppliers by delayed order count in the trailing 12 months — which carry the most on-time risk?
2. Show monthly fab utilization by fab line for the trailing 12 months — where are we above 95%?
3. Which material categories have the longest average lead times — which are single-source risks?
4. Top 10 materials by total procurement spend this quarter, and how does that compare to last quarter?
5. How has critical bottleneck count trended monthly by fab line — which lines need capex?
6. Which suppliers have the highest reject rate — where do we have quality exposure?
7. What is the trailing 6-month plan adherence percentage by material category, and which categories are below the 95% target?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
