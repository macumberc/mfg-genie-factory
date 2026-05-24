# WellGuard Upstream — Demo Script

**Space:** Oil & Gas Upstream — WellGuard Upstream - Predictive Maintenance & Asset Health 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Reliability + Reliability Engineer, Asset Manager, Drilling Manager
**KPIs touched:** Avg health score, MTBF days, Availability %, Predicted RUL days, Unplanned downtime hours, Repair cost and cost per downtime hour
**Big decision automated:** Which 3-5 ESPs and rod pumps to pull and replace this month, which artificial-lift system to install on the next completion cycle, and whether the predictive-maintenance program earns next year's reliability capex or gets cut back to break-fix.

---

## Pre-demo checklist

- Open the Genie space `WellGuard Upstream - Predictive Maintenance & Asset Health 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> WellGuard Upstream runs 20 critical pieces of rotating equipment — top drives, mud pumps, ESPs, rod pumps, BOPs, and compressors — across the Permian, Eagle Ford, Bakken, Haynesville, and Marcellus. Today the health-score watchlist lives in the Reliability Engineer's OSIsoft PI export, the deferred-production number sits in the Drilling Manager's daily report, and the repair-cost-vs-budget view is rebuilt every Friday by the Asset Manager in a CMMS pivot. Three artifacts, same fleet — and the workover-rig schedule plus next year's predictive-maintenance budget get decided by whichever number wins the meeting. The space ends that. It converts the 30-day-RUL alert into a defensible pull-and-replace recommendation in the same conversation the AFE narrative is written.

---

## Key KPIs in scope

- Avg health score (0-100) — composite condition indicator from sensor telemetry
- MTBF days — mean time between failures; ESP industry benchmark is ~400-600 days
- Availability % — target ≥95% on rotating equipment, ≥98% on BOPs
- Predicted RUL days — remaining useful life from ML model; <30d = act now
- Unplanned downtime hours — emergency + corrective events
- Repair cost (USD) and cost per downtime hour — maintenance spend efficiency
- Production loss (BBL) — deferred barrels from equipment downtime
- Prediction rate — % of events flagged in advance by the ML model

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **BBL** | Barrels |
| **ESP** | Electric Submersible Pump |
| **MTBF** | Mean Time Between Failures |
| **ROI** | Return on Investment |
| **RUL** | Remaining Useful Life |
| **VP** | Vice President |

---

## Act 1 — The signal — surfacing the units that are about to fail this quarter *(≈4 min)*

**Persona:** Reliability Engineer • **Job to be done:** Pull the at-risk equipment list out of yesterday's telemetry — ranked by downtime impact, not by alert noise.

*This is where the intervention queue starts to form. Two questions in, the engineer already has the unit list that used to take a half-day of CMMS-to-PI stitching.*

### Question (Act 1.1)

> **Top 10 equipment assets by total unplanned downtime hours over the last 90 days.**

**What to say while it runs:** Top 10 by total unplanned downtime hours over the last 90 days. The point isn't which assets are noisy — it's which ones have already cost us availability. Rotating-equipment availability target is 95%, BOPs 98%. Anything that consumed real downtime this quarter is a candidate for either a teardown or a replacement decision.

**What to look for:** Ranked table — equipment ID, type, field, total_unplanned_downtime_hours. Click Show generated code once so the room sees the metric view is doing the SUM, not free-form math.

**Land the point:** Right there is the pull-list the Reliability Engineer used to spend a morning assembling. Now it's the input to the workover-rig conversation that happens before the 8 AM standup — not after.

### Question (Act 1.2)

> **Show monthly trend of total repair cost and production loss BBL across the fleet for the trailing 12 months.**

**What to say while it runs:** Now monthly trend of total_repair_cost_usd and total_production_loss_bbl across the fleet for the trailing 12 months. This is the chart that determines whether reliability is winning or losing this year. Cost going up is fine if production-loss is going down — that's the program working.

**What to look for:** Dual-axis monthly trend over 12 months. Watch for the inflection — the month the production-loss line bends down is the month the predictive program earned its keep.

**Land the point:** Before this space, that chart was rebuilt by hand for the quarterly reliability review. Now it's the engineer's morning open — and the conversation with the Asset Manager about whether to add or cut PM headcount starts from the same picture.

---

## Act 2 — The decision — pull-and-replace, workover, or run-to-failure *(≈4 min)*

**Persona:** Asset Manager • **Job to be done:** Commit this month's intervention list — which 3-5 ESPs come out, which rod pumps get a workover, and which units are managed run-to-failure.

*Three questions that turn the watchlist into a dollar-ranked intervention queue. The middle question is the anchor — RUL plus deferred production is the conversation the room came to see.*

### Question (Act 2.1)

> **Which assets currently have a predicted RUL under 30 days, and what is their equipment type and field?**

**What to say while it runs:** min_rul_days under 30 by equipment type and field. ESP industry MTBF benchmark is 400-600 days, so a 30-day RUL is a real intervention call — not a hypothetical. The question isn't *will* this unit fail, it's *do we pull it on schedule or wait for the failure event*.

**What to look for:** Short table — equipment, type, field, predicted_rul_days. The list is the next 30 days of rig and crew assignments.

**Land the point:** Now the workover queue is the same artifact the reliability engineer sees, the asset manager sees, and the drilling manager schedules against. One list, three decisions — pull, workover, or accept the risk.

### Question (Act 2.2)

> **What is the prediction rate (share of events flagged by ML) by equipment type this year?**

**What to say while it runs:** Prediction rate by equipment type year to date — share of events the ML model flagged in advance. If we're at 70%+ on ESPs and 40% on rod pumps, that tells us where the model investment goes next. This is the slide the VP of Reliability uses to defend the program.

**What to look for:** Bar by equipment_type. The gap between predicted and total events is the program's measurable lift — and the gap is also where the deferred-barrel dollars are still leaking.

**Land the point:** When predicted rate, downtime hours, and production loss are all in the same governed surface, the conversation about *should we expand the PM program* turns into *which equipment types earn more sensors next year*.

> **Anchor moment.** Stop on the RUL-under-30 list and the fleet-level deferred-production trend together. Pick the worst three ESPs on the list — typical Permian ESP pull-and-replace runs $250-500K including deferred production, and the deferred-barrels measure on those units is already material.

> *Call the three worst ESPs a combined 800 deferred barrels per day at $70 oil — that's $56,000 a day of recoverable revenue, $1.7M a month if they sit. An unplanned ESP failure costs $250-1M between the pull, the replacement string, and the deferred production while the rig moves. Three planned pulls at $400K beats three unplanned failures at $750K by over $1M — and that's before the deferred-production delta. Scale that across 20 critical assets and the predictive-maintenance program is paying $3-5M a year against a CMMS license and a few extra sensors.*

> That is the conversation that locks in next year's reliability capex. The pull list gets built on dollars — not on which engineer made the loudest case in the morning standup. ESP intervention calendar is a one-page output of this space, not a four-week budget exercise.

### Question (Act 2.3)

> **Top 10 fields by alarm and trip count this month — how does that compare to last month?**

**What to say while it runs:** Top 10 fields by alarm-trip count this month vs last month. This is the field-level pressure gauge. A field where the alarm count is climbing month over month is a field where the on-site crew is being trained to ignore the system — and that's the failure that costs you $1M.

**What to look for:** Side-by-side bar — alarm_trip_count, this month vs last. Look for the fields that are accelerating, not just the ones with the biggest absolute number.

**Land the point:** The alarm-fatigue conversation is one of the hardest to win without data. Now it's a chart — and the call to retune thresholds on the worst three fields gets made on Tuesday, not in next quarter's reliability review.

---

## Act 3 — The commitment — sizing the reliability budget and the artificial-lift mix *(≈4 min)*

**Persona:** VP of Reliability • **Job to be done:** Defend the predictive-maintenance program upstream and shape next cycle's reliability capex — which fields get more instrumentation, which equipment types get standardized, which get harvested.

*The VP doesn't need another dashboard; they need the engineer's numbers and the asset manager's numbers reconciled, in the language of OR impact and deferred barrels, so the AFE conversation writes itself.*

### Question (Act 3.1)

> **Which equipment types have the lowest availability and shortest MTBF over the last 6 months?**

**What to say while it runs:** Availability and MTBF by equipment type over the last 6 months. ESP industry MTBF benchmark is 400-600 days. If our number is 280, that's the gap. Equipment types under the benchmark are either getting replaced or getting more sensors — those are the only two answers.

**What to look for:** Table by equipment_type with avg availability_pct and mtbf_days side by side. The equipment types in the bottom-right of that view are the artificial-lift-mix conversation for next year's completions.

**Land the point:** That's how the artificial-lift standardization decision gets made — not on the vendor's pitch deck, on our own MTBF data. The next 10 completions go on the lift system that's actually delivering 500+ MTBF days in our basins.

### Question (Act 3.2)

> **What is the total deferred production (BBL) and repair spend from Emergency events by field, year to date?**

**What to say while it runs:** Total deferred production and Emergency-event repair spend by field year to date. This is the field-level prioritization view — the fields that earn an Asset Integrity capex line item versus the ones being run as harvest assets.

**What to look for:** Ranked by field — total_production_loss_bbl and total_repair_cost_usd from event_type = 'Emergency'. The dollars are what break the tie when two fields look equally bad operationally.

**Land the point:** Triage at 8 AM, capex allocation at 10. Same space, same numbers. The Reliability Engineer's pull list and the VP's AFE pitch are now the *same artifact* — and the executive team gets one story about reliability ROI, not three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — WellGuard Upstream — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 equipment assets by total unplanned downtime hours over the last 90 days.
2. Show monthly trend of total repair cost and production loss BBL across the fleet for the trailing 12 months.
3. Which assets currently have a predicted RUL under 30 days, and what is their equipment type and field?
4. What is the prediction rate (share of events flagged by ML) by equipment type this year?
5. Top 10 fields by alarm and trip count this month — how does that compare to last month?
6. Which equipment types have the lowest availability and shortest MTBF over the last 6 months?
7. What is the total deferred production (BBL) and repair spend from Emergency events by field, year to date?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
