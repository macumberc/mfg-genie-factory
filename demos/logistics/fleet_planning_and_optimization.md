# FleetEdge Solutions — Demo Script

**Space:** Logistics — FleetEdge Solutions - Fleet Planning & Optimization 🚚
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Logistics + Fleet Manager, S&OP Lead, CFO partner
**KPIs touched:** Asset utilization %, On-time delivery %, Revenue per vehicle, Cost per km, Maintenance cost as % of revenue, Idle hours
**Big decision automated:** Which vehicle classes and individual assets to retire in the next 20-truck refresh, which depots to rebalance into, and whether to lease or buy the replacements.

---

## Pre-demo checklist

- Open the Genie space `FleetEdge Solutions - Fleet Planning & Optimization 🚚`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FleetEdge Solutions runs 20 mixed-class vehicles — Heavy Duty, Medium Duty, Light Duty, and Sprinters — dispatched out of 8 regional depots. Today the utilization picture lives in the Fleet Manager's weekly dispatch board, the OTD and failure rates in the VP Logistics' Friday QBR slide, and the per-vehicle revenue/maintenance P&L in the CFO partner's quarterly fleet review. Three artifacts, three cadences, same trucks — and the lease-vs-buy decision on the next 20-asset refresh gets made on whichever number the loudest executive remembered. This space ends that. One governed surface that turns daily dispatch records into the *which class, which units, which depots, which financing* conversation in the same room.

---

## Key KPIs in scope

- Asset utilization % — dispatched / available hours; industry target 70%+ for heavy duty
- On-time delivery % — SLA performance; target 95%+
- Revenue per vehicle (USD/month) — asset productivity metric
- Cost per km (fuel + maintenance) — primary unit-cost lever
- Maintenance cost as % of revenue — fleet health and aging signal
- Idle hours — under-utilization indicator
- Operation count — throughput per asset class
- Delivery failure / partial rate — service quality red flag

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **SLA** | Service Level Agreement |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the under-earning trucks before the next allocation cycle *(≈4 min)*

**Persona:** Fleet Manager • **Job to be done:** Pull the under-performing vehicles out of last month's dispatch data — not by gut, by revenue per asset and utilization.

*This is where the refresh shortlist starts forming. Two questions in, the Fleet Manager already has the class-level revenue vs. fuel-cost picture that used to take half a day in Excel.*

### Question (Act 1.1)

> **Show monthly total revenue and monthly fuel cost by vehicle class for the trailing 12 months.**

**What to say while it runs:** Monthly revenue and fuel cost by vehicle class — this is the unit-economics chart for the whole fleet. Heavy Duty should be carrying the revenue; Sprinters should be cheap to run. If the gap narrows on either side, the class mix is wrong.

**What to look for:** Twelve months of revenue and fuel cost side-by-side across HD / MD / LD / Sprinter. Look for the class where fuel cost as a share of revenue is climbing — that's the class to interrogate first.

**Land the point:** Now the Fleet Manager can spot a structurally underperforming vehicle class in seconds — that's the conversation that starts the lease-vs-buy debate for the next 20-truck order.

### Question (Act 1.2)

> **How has average utilization trended month-over-month across each vehicle class?**

**What to say while it runs:** Average utilization trend by class. The industry target on Heavy Duty is 70% or better. Sprinters and Light Duty drift to the low 60s in a soft demand quarter — that's normal. A sustained downtrend on HD is the red flag.

**What to look for:** Month-over-month avg_utilization_pct lines by vehicle class. Watch for the class whose trend has flattened or fallen below target for two-plus quarters.

**Land the point:** Before this space that trend lived in a PowerPoint that was refreshed once a quarter. Now it's a five-second query — and the depot rebalancing conversation happens monthly, not annually.

---

## Act 2 — Refurbish, retire, or rebalance — locking the asset list *(≈4 min)*

**Persona:** S&OP Lead • **Job to be done:** Decide which specific vehicles get retired in the next refresh, which depots receive the redeployed capacity, and what failure rate is structural vs. asset-specific.

*Three questions that move from the asset-level shortlist to a defensible recommendation. The middle question is the anchor — converting maintenance-cost share into a per-asset retire-or-keep call.*

### Question (Act 2.1)

> **Top 10 vehicles by monthly revenue last month, and what was each vehicle's maintenance cost?**

**What to say while it runs:** Top 10 vehicles by monthly revenue last month plus their maintenance cost. We want to see whether the revenue leaders are also money pits — high revenue with a 30%+ maintenance share is an asset on the edge of retirement, not a champion.

**What to look for:** A ranked list of 10 trucks with total_monthly_revenue alongside total_monthly_maintenance_cost. Watch for revenue leaders whose maintenance cost is climbing into double-digit percent of revenue.

**Land the point:** That used to be a manual join across the dispatch system and the maintenance ledger. Now it's the input to the retire-or-overhaul decision the Fleet Manager and CFO partner argue about every refresh cycle.

### Question (Act 2.2)

> **Which depots had the highest share of delivery_status = 'Failed' or 'Partial' operations this quarter?**

**What to say while it runs:** Failed and Partial delivery share by depot this quarter. Anything above 5% is an SLA chargeback risk — most freight contracts have a 1-2% OTIF penalty per missed window. A depot pushing 8-10% failure rate is a structural problem, not a bad week.

**What to look for:** Depots ranked by share of delivery_status in ('Failed','Partial'). The top of the list is where capacity is mis-matched to demand — either too few trucks, too few drivers, or the wrong class mix.

**Land the point:** Before this space the depot conversation was anecdotal — 'Atlanta feels rough this quarter'. Now it's a ranked list with chargeback exposure attached, and the depot rebalancing recommendation has a number on it.

> **Anchor moment.** Stop on the retirement candidates list. Take the worst Sprinter — running 60% utilization on a class target of 80%, $0.90/km maintenance + fuel against a fleet of 20 vehicles.

> *A Sprinter sitting at 60% utilization vs. a 80% target is leaking roughly $20K/year of revenue per vehicle at FleetEdge's freight rates. We see 4 Sprinters in that band — call it $80K/year of recoverable revenue from rebalancing alone. Now layer the maintenance side: the top 3 retirement candidates are running ~35% maintenance-to-revenue against a healthy fleet baseline of 15%. Retiring those three and replacing with leased Mediums recovers another $150-200K/year in maintenance + lost-revenue cost. Across the 20-vehicle fleet, that's a $300K+ annual recurring decision — bigger than the lease-vs-buy delta on the entire 20-truck refresh.*

> That's the decision this space automates. Not the slide. The decision. Refresh list rebuilt on per-asset dollars, not whichever truck broke down most recently in front of the executive team.

### Question (Act 2.3)

> **Top 10 vehicles by maintenance cost as a percent of revenue — which assets should we consider retiring?**

**What to say while it runs:** Top 10 vehicles by maintenance cost as a percent of revenue — these are the retirement candidates. Industry rule of thumb: anything north of 25% on an asset older than 5 years is run-to-failure territory; anything north of 40% is already costing more than it earns.

**What to look for:** Vehicles ranked by total_monthly_maintenance_cost / total_monthly_revenue. The top 5-10 are the names that go into the refresh recommendation.

**Land the point:** That ranked list IS the next refresh shortlist. The Fleet Manager and CFO partner walk out of this question with the asset names — not 'we should retire some Sprinters' but 'we are retiring these seven units and rebalancing the slots to Atlanta and Dallas'.

---

## Act 3 — The commitment — locking the 20-truck refresh and the financing call *(≈4 min)*

**Persona:** VP Logistics • **Job to be done:** Defend the refresh recommendation to the CFO and the board — which class mix, which depots get the slots, lease or buy, and what the operating-margin lift looks like on paper.

*The VP doesn't need another dashboard; they need the same per-asset numbers the Fleet Manager and S&OP Lead are acting on, framed so the board paper writes itself.*

### Question (Act 3.1)

> **What is the total operation count and on-time operation count by depot for the last 90 days?**

**What to say while it runs:** Operation count and on-time operation count by depot for the last 90 days. This is the throughput-vs-quality picture by location — a depot can be high-volume and still be the source of the SLA chargebacks if the OTD ratio is off.

**What to look for:** Depots ranked by operation_count alongside on_time_operation_count. The on-time ratio per depot is the number the VP will quote to the customer's procurement team.

**Land the point:** When the VP can show the board both the volume AND the service-quality picture by depot, the lease-vs-buy debate moves from 'how many trucks' to 'which class, which depot, which contract structure' — and the financing call lands in one meeting.

### Question (Act 3.2)

> **Which vehicle class generated the highest revenue per kilometer in the most recent reporting month?**

**What to say while it runs:** Which class generated the highest revenue per kilometer last month. This is the gravity number for the refresh mix — the class with the best $/km earned the right to most of the new capacity.

**What to look for:** A class-level ranking of total_revenue_usd / total_distance_km. Heavy Duty typically wins on long-haul; Sprinter wins on short urban — the surprise is when the ranking flips and a class no one expected is the margin leader.

**Land the point:** That single ranking turns into the class-mix decision on the 20-truck order. Fleet refresh sign-off used to be a quarter-long exercise across three spreadsheets and two committees. Now the recommendation, the depot allocation, and the lease-vs-buy framing are one conversation — and the board paper writes itself.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FleetEdge Solutions — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total revenue and monthly fuel cost by vehicle class for the trailing 12 months.
2. How has average utilization trended month-over-month across each vehicle class?
3. Top 10 vehicles by monthly revenue last month, and what was each vehicle's maintenance cost?
4. Which depots had the highest share of delivery_status = 'Failed' or 'Partial' operations this quarter?
5. Top 10 vehicles by maintenance cost as a percent of revenue — which assets should we consider retiring?
6. What is the total operation count and on-time operation count by depot for the last 90 days?
7. Which vehicle class generated the highest revenue per kilometer in the most recent reporting month?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
