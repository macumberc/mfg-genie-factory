# TrackGuard Systems — Demo Script

**Space:** Railroad — TrackGuard Systems - Predictive Maintenance & Asset Health 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Mechanical + Reliability Lead, Mechanical VP, CFO
**KPIs touched:** Fleet health score, 30-day failure probability, Remaining useful life, Emergency event count, Total downtime hours, Parts + labor spend vs maintenance budget
**Big decision automated:** Which 5-8 locomotives go into the next overhaul slot, which fleet earns next year's reliability capex, and whether we can hold maintenance spend flat without giving back the operating-ratio improvement.

---

## Pre-demo checklist

- Open the Genie space `TrackGuard Systems - Predictive Maintenance & Asset Health 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> TrackGuard Systems is the Class I mechanical-reliability surface covering 20 locomotives and railcars across Line Haul, Yard, Bulk, Intermodal, Hazmat, and General fleets. Today the sensor-anomaly watchlist lives in the Reliability Lead's Wabtec / GE health-monitoring portal, the work-order spend sits in the Mechanical VP's SAP PM dashboard, and the budget-vs-actual view comes out of the CFO's monthly close pack — different definitions of an emergency event in each. Three artifacts, same fleet — and the overhaul prioritization, the FRA-risk posture, and the maintenance-budget signoff get made by whichever number reaches the meeting first. This space ends that. The vibration spike the Reliability Lead caught on Tuesday and the budget overrun the CFO is staring at on Friday are now the same conversation — and a single FRA-reportable failure event runs $5-50M, so getting it right matters.

---

## Key KPIs in scope

- Fleet health score (0-100) — ML composite of vibration, bearing temp, oil pressure
- 30-day failure probability (%) — leading indicator for unplanned removals
- Remaining useful life (days) — capital and overhaul planning input
- Emergency event count — reliability and FRA reportable risk signal
- Total downtime hours — service availability and revenue exposure
- Parts + labor spend ($) vs maintenance budget — cost discipline
- Failure component mix — Engine / Brakes / Wheels / Bearings / Couplers / Electronics root-cause concentration
- Preventive-to-corrective ratio — reliability maturity benchmark

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **FRA** | Federal Railroad Administration |
| **RUL** | Remaining Useful Life |

---

## Act 1 — The signal — catching the failure curve before the operating ratio does *(≈4 min)*

**Persona:** Reliability Lead • **Job to be done:** Find the units whose health is decaying faster than the fleet — and rank them by the dollars on the line, not the alert count.

*This is where the overhaul-slot list begins to form. Two questions in, the Reliability Lead has the at-risk units and the fleet-trend picture together — that's the conversation Mechanical and Finance want to have *before* the budget signoff.*

### Question (Act 1.1)

> **Show the monthly trend in fleet average health score over the trailing 12 months by asset type.**

**What to say while it runs:** Monthly trend of fleet avg_health_score by asset_type over the trailing 12 months. Fleet health below 70 is a yellow flag; below 60 is reliability-policy territory. The shape of those curves — which asset types are decaying, which are stable, which were rebuilt and bounced back — is the input to the overhaul-slot conversation.

**What to look for:** Multi-line monthly trend by asset_type. The asset types whose lines are sloping down month over month are the overhaul targets; flat lines are the keepers.

**Land the point:** Before this space, that chart was rebuilt for every monthly mechanical review. Now it's the Reliability Lead's first question of the day — and the conversation with the Mechanical VP about *which locomotives go in the next overhaul slot* starts from one picture.

### Question (Act 1.2)

> **Top 10 assets by total downtime hours over the last 90 days.**

**What to say while it runs:** Top 10 assets by total_downtime_hours over the last 90 days. Class I locomotive availability target is 92-94%; anything chewing real downtime this quarter is either an overhaul candidate or a sell-back candidate. Same question, two different dispositions depending on age.

**What to look for:** Ranked table — asset_name, asset_type, fleet, total_downtime_hours. The list is the next overhaul-slot queue *or* the leasing-decision list — Act 2 separates the two.

**Land the point:** That ranking used to be the output of two days of cross-system stitching between the health portal and SAP PM. Now it's a question — and the queue gets assembled before the morning standup, not after.

---

## Act 2 — The decision — overhaul, defer, or retire *(≈4 min)*

**Persona:** Mechanical VP • **Job to be done:** Commit the overhaul slot list and the deferred-overhaul roster — and decide which component categories earn extra parts inventory next quarter.

*Three questions that turn the watchlist into a dollar-ranked work plan. The middle question — parts plus labor by failure component vs. budget — is the anchor. That's where the maintenance budget gets re-cut.*

### Question (Act 2.1)

> **Which assets have a 30-day failure probability above 25% and less than 90 days of remaining useful life?**

**What to say while it runs:** Assets with failure_probability_pct above 25% and remaining_useful_life_days under 90. That's the failure-imminent quadrant. A locomotive overhaul deferral is $3-5M per unit of preserved capital, but the cost of an unplanned removal — between deferred service and emergency work — typically runs 15-25% more failures and the FRA risk that comes with each. Deferral is real money; so is failure.

**What to look for:** Filtered table — asset_id, asset_type, fleet, failure_probability_pct, remaining_useful_life_days. That short list is the next overhaul-slot queue with dollars attached.

**Land the point:** Now the overhaul slot list is the same artifact the Reliability Lead sees, the Mechanical VP signs, and the CFO funds. The decision moves from *which units are worst* to *which units we can defer without giving back the OR improvement*.

### Question (Act 2.2)

> **How has the share of emergency events versus preventive events trended month-over-month across the fleet?**

**What to say while it runs:** Total parts_cost_usd plus labor_cost_usd by failure_component for the last quarter, against maintenance_budget_usd. Engine and Wheels usually dominate, but Bearings overrunning is the leading signal that vibration thresholds are mis-set. Component-level overrun tells you where the capex goes — extra parts inventory, more sensors, or a vendor renegotiation.

**What to look for:** Bar by failure_component with budget line overlay. The components above the budget line are the inventory and sourcing conversation for next quarter.

**Land the point:** When parts spend, labor spend, and budget all sit on the same governed surface, the conversation about *can we hold maintenance flat next year* stops being a hope and becomes a component-by-component decision. That conversation used to take a quarter; now it's an answer.

> **Anchor moment.** Stop on the failure-imminent list and the parts-plus-labor by component chart together. Pick the worst 5 locomotives — units with failure_probability above 35% and RUL under 60 days, already showing $200K+ of unplanned repair this quarter.

> *A planned overhaul on those 5 units runs $3-4M apiece — $15-20M total. The unplanned failure path on the same 5 is 15-25% more failure events, each with $80K-150K of parts plus labor, plus 4-8 days of unplanned downtime at $30-50K per day of lost revenue per unit, plus the FRA exposure. Net, the unplanned path is roughly $4-6M worse over 12 months on those 5 units — and that's before a single derailment. Across the 20-unit critical fleet, the predictive-maintenance program is buying $8-12M a year and 0.3-0.5 points of operating ratio against $14B of revenue.*

> That is the overhaul-slot decision this space automates. Not the slide. The decision. The overhaul queue, the parts inventory plan, and the FRA-risk posture for next year are a one-page output of this space — and the conversation with the CFO is about which 5 units, not whether the program is worth funding.

### Question (Act 2.3)

> **What is the total parts plus labor spend by failure component for the last quarter, and how does it compare to budget?**

**What to say while it runs:** Share of emergency_count vs total events month over month. Preventive-to-corrective ratio is the reliability-maturity score. Best-in-class Class I is roughly 70% preventive; if we're at 50/50, that's where the reliability investment goes. Emergency events are also where the FRA risk lives — fines run $5-25K per violation, derailments $5-50M per event.

**What to look for:** Monthly trend of emergency_count vs other event types. The ratio trending the wrong direction is the FRA-risk conversation — same chart, same data, no separate audit.

**Land the point:** The preventive-to-corrective mix is one of the hardest reliability conversations to win without data. Now it's a chart — and the call to expand the predictive program gets made at the operating committee, not at the next FRA hearing.

---

## Act 3 — The commitment — sizing the maintenance budget and the FRA-risk posture *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the maintenance-budget cap to the board and confirm the FRA-risk exposure is shrinking.

*The CFO needs the reliability story, the cost story, and the FRA-risk story in the same view. That's the operating-ratio narrative — and it's a board-meeting conversation.*

### Question (Act 3.1)

> **Rank the 6 asset types by average bearing temperature in the latest month of data — flag any above 85 Celsius.**

**What to say while it runs:** Asset types ranked by avg_bearing_temp in the latest month — flag anything above 85 Celsius. Bearing temp is the cleanest leading indicator of a hot-box detector hit on the network — and a hot-box hit is a service disruption and a regulator phone call. This is the sensor cut that connects mechanical to FRA risk.

**What to look for:** Ranked asset_type by avg_bearing_temp_celsius — flagged rows above 85. The flagged asset types are the hot-box-risk concentration.

**Land the point:** When bearing temperature, failure probability, and emergency-event rate are in the same surface, the FRA exposure is no longer an instinct — it's a queue. The board conversation about regulatory risk gets quantified, not narrated.

### Question (Act 3.2)

> **Show monthly maintenance budget versus actual spend by fleet over the trailing 6 months.**

**What to say while it runs:** Monthly maintenance_budget_usd vs actual_maintenance_usd by fleet over the trailing 6 months. Where actual is consistently over budget, the budget needs to move — or the fleet needs to be re-mixed. Where it's under, that's where the operating-ratio dividend is hiding.

**What to look for:** Dual-line monthly trend per fleet — budget vs actual. The fleets persistently over-budget are the capex-or-retirement conversation; the under-budget fleets are the OR dividend.

**Land the point:** Same space the Reliability Lead opened with. Same numbers. The overhaul plan, the FRA-risk posture, and the maintenance-budget envelope are now the *same artifact* — and the board gets one mechanical story, not three reconciled versions.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — TrackGuard Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in fleet average health score over the trailing 12 months by asset type.
2. Top 10 assets by total downtime hours over the last 90 days.
3. Which assets have a 30-day failure probability above 25% and less than 90 days of remaining useful life?
4. How has the share of emergency events versus preventive events trended month-over-month across the fleet?
5. What is the total parts plus labor spend by failure component for the last quarter, and how does it compare to budget?
6. Rank the 6 asset types by average bearing temperature in the latest month of data — flag any above 85 Celsius.
7. Show monthly maintenance budget versus actual spend by fleet over the trailing 6 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
