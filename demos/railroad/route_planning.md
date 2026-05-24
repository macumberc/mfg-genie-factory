# RailRoute Logistics — Demo Script

**Space:** Railroad — RailRoute Logistics - Route Planning & Optimization 🗺️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Operations + Network Operations Director, Service Design VP, COO
**KPIs touched:** Train velocity, Terminal dwell, Gross ton-miles, On-time performance, Capacity utilization, Fuel gallons per ton-mile
**Big decision automated:** Where to put the next $200-300M of corridor capex — which 3-5 sidings get built, which dispatcher policy gets changed, and which corridor is recapitalized to pull a mile-per-hour of network velocity out of the system.

---

## Pre-demo checklist

- Open the Genie space `RailRoute Logistics - Route Planning & Optimization 🗺️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RailRoute Logistics is the Class I network-design surface covering 20 corridors. Today the velocity-and-dwell view lives in the Network Operations Director's daily ops report, the capacity utilization view sits in a Service Design spreadsheet refreshed each cycle, and the capex prioritization deck is rebuilt every quarter by the planning team out of CSX/UP/NS-style corridor plans. Three artifacts, same network — and the meet/pass siding investment, the dispatcher policy change, and the train-handling recapitalization get debated in three different rooms with three different versions of the capacity story. This space ends that. Network velocity is the lever — every 1 mph of sustained velocity unlocks 5-10% more capacity on the existing fleet, and at a $14B Class I that's the kind of number that moves the operating ratio by half a point.

---

## Key KPIs in scope

- Train velocity (mph) — primary driver of cycle time and asset turns
- Terminal dwell (hours) — congestion and yard-throughput indicator
- Gross ton-miles (GTM) — top-line freight throughput
- On-time performance (%) — customer-facing reliability metric
- Capacity utilization (%) — service design and pricing input
- Fuel gallons per ton-mile — operating-ratio and ESG metric
- Projected capex ($) and capacity risk band — capital planning inputs
- Maintenance window days — service-design tradeoff vs. capex

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **ESG** | Environmental, Social, Governance |

---

## Act 1 — The signal — finding the corridors choking the network *(≈4 min)*

**Persona:** Network Operations Director • **Job to be done:** Surface the corridors where velocity and dwell are dragging on the network — before the service-design team sets the next cycle's plan.

*This is where the capacity-investment conversation starts. Two questions in, the Network Ops Director has the bottom-velocity corridor list and the regional GTM picture in the same surface.*

### Question (Act 1.1)

> **Which 10 corridors had the lowest average velocity over the last 90 days?**

**What to say while it runs:** Bottom 10 corridors by avg_velocity_mph over the last 90 days. Class I network velocity benchmark is 22-25 mph system-wide; anything sustaining under 18 mph is a structural bottleneck, not an operational hiccup. Each mph below the network average is a measurable capacity tax.

**What to look for:** Ranked table — corridor_name, region, avg_velocity_mph. The bottom of that list is the bottleneck inventory; the regions concentrated there are next year's capex story.

**Land the point:** Before this space, that list was assembled from a Sunday-night corridor-by-corridor PowerBI export. Now it's the Network Ops Director's open — and the capacity conversation with Service Design starts an hour before the planning meeting, not in it.

### Question (Act 1.2)

> **Show monthly gross ton-miles by region for the trailing 12 months.**

**What to say while it runs:** Monthly gross_ton_miles by region for the trailing 12 months. GTM is the top-line throughput number — the lever that moves the operating ratio. Regions where GTM is climbing while velocity is dropping are the *we're filling the pipe* regions; those are also the regions where the next bottleneck shows up first.

**What to look for:** Stacked monthly GTM by region. Watch for the regions where GTM growth is outrunning capacity additions — that's the capex case.

**Land the point:** That picture used to live in the COO's quarterly book. Now it's the daily ops surface — and the corridor-capex conversation no longer waits for the quarterly review to start.

---

## Act 2 — The decision — siding investment, recapitalization, or dispatcher policy *(≈4 min)*

**Persona:** Service Design VP • **Job to be done:** Commit the corridor-capex prioritization list, the dispatcher-policy changes, and the maintenance-window plan for the next service-design cycle.

*Three questions that convert corridor data into capital allocation. The middle question — projected capex needed across the network — is the anchor. That's the dollars conversation the COO is waiting for.*

### Question (Act 2.1)

> **Which corridors are flagged as High or Critical capacity risk in the most recent plans, and what capex do they require?**

**What to say while it runs:** Corridors flagged High or Critical capacity_risk in the most recent plans, with their capex_needed_usd. Capacity risk classification is the planning team's standing taxonomy — High and Critical are the ones that either get capex or get a dispatcher-policy workaround. There is no third option; the question is which lever, on which corridor.

**What to look for:** Filtered table — corridor_id, region, capacity_risk in ('High','Critical'), capex_needed_usd. The dollar column is what differentiates the *expensive but necessary* from the *cheap and overdue*.

**Land the point:** That table is the capex prioritization slide Service Design used to spend a month rebuilding. Now it's a question — and the conversation about *which corridor goes first* turns into a one-meeting decision.

### Question (Act 2.2)

> **What is the total projected capex needed across the network in the trailing 12 months of plans, by region?**

**What to say while it runs:** Total projected capex_needed across the network in the last 12 months of plans, by region. This is the envelope conversation — the dollar number the COO and CFO need to know before next year's capital plan goes to the board. Regions concentrating high-risk corridors are the ones with the biggest capex asks.

**What to look for:** Bar by region summing capex_needed_usd. The tallest bars are next year's capital-plan story; the shape of the distribution is the regional concentration risk.

**Land the point:** When capex and capacity risk both sit on the same governed surface, the *how much do we need to invest* conversation becomes a one-question answer instead of a three-week planning cycle. That number — typically $200-300M of priority corridor capex on a Class I — is the conversation that locks in the operating-ratio commitment to the board.

> **Anchor moment.** Stop on the velocity-bottom list, the capex-by-region rollup, and the dwell-trending chart together. Pick the top 3-5 High-risk corridors carrying the biggest GTM — these are the corridors where capex converts directly into network velocity.

> *Call the top 3 capex-priority corridors a combined $180M of siding and yard investment that buys 1.5 mph of sustained velocity on the affected lanes. A 1 mph network velocity improvement unlocks roughly 5-10% more capacity on the existing fleet, and on a $14B Class I a half-point of operating-ratio improvement is roughly $70M of annual EBIT. The $180M capex against $70M+/year of EBIT is a sub-3-year payback — and that's before the avoided locomotive purchases of $3-5M each that would otherwise be required to hold the GTM curve. The 5 lowest-priority Low-risk corridors in the same view are the ones that get a maintenance-window optimization instead of capex — that's where the operating budget gets freed up to fund the priority list.*

> That is the capex-prioritization decision this space automates. Not the slide. The decision. The next $200-300M of corridor capital — sidings, yards, dispatching technology — gets ranked on velocity dollars and OR points, not on whichever region-VP made the loudest case at the planning offsite.

### Question (Act 2.3)

> **Top 10 corridors by terminal dwell hours this month — and how does that compare to last month?**

**What to say while it runs:** Top 10 corridors by terminal_dwell_hours this month vs last month. Terminal dwell is the second velocity lever — every hour of dwell is an hour of locked equipment. Industry benchmark is 22-28 hours; anything climbing above 30 is a yard-throughput investment or a dispatcher-policy fix.

**What to look for:** Side-by-side bar — avg_dwell_hours this month vs last. The bars that grew are the operational-fix queue; the bars that have been chronically high are the capex queue.

**Land the point:** Dwell is the conversation that separates the operational fix from the capital ask. Corridors climbing month over month get a dispatcher-policy review; corridors chronically high get a yard expansion. Same chart, two completely different actions.

---

## Act 3 — The commitment — locking in the capital plan and the velocity story *(≈4 min)*

**Persona:** COO • **Job to be done:** Defend the capital envelope to the board and confirm the velocity improvement will land in next year's operating ratio.

*The COO needs the velocity story, the fuel story, and the maintenance-window story in one surface — that's the case for the corridor program at the board level.*

### Question (Act 3.1)

> **How has fuel efficiency (gallons per ton-mile) trended month-over-month across the network?**

**What to say while it runs:** Monthly fuel_gallons_per_ton_mile across the network. Fuel is roughly 15-20% of operating cost — and fuel efficiency is the cleanest ESG number we report. Improving velocity reduces fuel-per-ton-mile because trains stop and restart less. The two metrics move together; this is where the velocity story becomes a sustainability story.

**What to look for:** Monthly trend of avg fuel_gallons_per_ton_mile. The slope is the dual operating-cost and ESG signal — and the inflection is where the velocity investment is showing up in the fuel line.

**Land the point:** When velocity, fuel efficiency, and capex all live in the same surface, the operating-ratio improvement and the ESG commitment become the same story to the board. That's the corridor-program case — and it doesn't need three separate decks to make it.

### Question (Act 3.2)

> **Which regions show the most maintenance window days in the trailing 12 months of plans, and what is the projected GTM impact?**

**What to say while it runs:** Regions with the most maintenance_window_days in the trailing 12 months of plans and their projected GTM impact. Maintenance windows are the service-design tradeoff — too few and the asset condition slips, too many and the velocity story collapses. The optimum is corridor-specific.

**What to look for:** Bar — region by avg maintenance_days alongside total projected_gtm_millions. The corridors with high maintenance windows AND high projected GTM are the windows-to-renegotiate conversation.

**Land the point:** Same space the Network Ops Director opened with. Same numbers. The capex prioritization, the maintenance-window plan, and the velocity commitment are now the *same artifact* — and the board gets one story about how next year's operating ratio gets earned, not three reconciled decks.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RailRoute Logistics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 corridors had the lowest average velocity over the last 90 days?
2. Show monthly gross ton-miles by region for the trailing 12 months.
3. Which corridors are flagged as High or Critical capacity risk in the most recent plans, and what capex do they require?
4. What is the total projected capex needed across the network in the trailing 12 months of plans, by region?
5. Top 10 corridors by terminal dwell hours this month — and how does that compare to last month?
6. How has fuel efficiency (gallons per ton-mile) trended month-over-month across the network?
7. Which regions show the most maintenance window days in the trailing 12 months of plans, and what is the projected GTM impact?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
