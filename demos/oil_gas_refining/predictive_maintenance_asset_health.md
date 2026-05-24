# RefineGuard Systems — Demo Script

**Space:** Oil & Gas Refining — RefineGuard Systems - Predictive Maintenance & Asset Health 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Reliability + Maintenance & Reliability Planner, Refinery Manager, Reliability VP
**KPIs touched:** Equipment availability, Mean Time Between Failures, Mean Time To Repair, Predicted Remaining Useful Life for critical rotating equipment, Predictive catch rate, Throughput loss from unplanned events
**Big decision automated:** Which 2-3 critical assets get swapped before the next turnaround vs. ridden into the cycle, which process units pull capex protection, and whether the turnaround window slips by two weeks or holds — defended against a $1-5M/day unplanned-shutdown exposure.

---

## Pre-demo checklist

- Open the Genie space `RefineGuard Systems - Predictive Maintenance & Asset Health 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RefineGuard Systems monitors 20 critical refinery assets — pumps, compressors, heat exchangers, reactors, furnaces, columns — across Crude Distillation, FCC, Hydrotreating, Catalytic Reforming, and Alkylation. Today the predicted remaining-useful-life number lives in the vibration team's data historian export, the work-order backlog and repair spend live in the CMMS, and the availability rollup gets reconstructed each month by a Reliability Engineer pulling MTBF tables into Excel. Three systems, three teams — so the turnaround scope gets locked using whoever's data is freshest, the predictive program's catch rate gets argued about every quarter, and the executive team finds out about a $3M/day unplanned shutdown after it has already started. This space ends that. RUL, work-order history, and availability all answer the same question: *which assets get swapped before the next turnaround, and which earn the ride into the cycle.*

---

## Key KPIs in scope

- Equipment availability (%) — top-quartile refiners run >96%
- Mean Time Between Failures (MTBF days)
- Mean Time To Repair (MTTR hours)
- Predicted Remaining Useful Life (RUL days) for critical rotating equipment
- Predictive catch rate (was_predicted = TRUE share)
- Throughput loss (bbl) from unplanned events
- Repair spend ($) by failure mode
- Alarm/Trip frequency by process unit

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **MTBF** | Mean Time Between Failures |
| **MTTR** | Mean Time To Repair |
| **RUL** | Remaining Useful Life |

---

## Act 1 — The signal — separating the throughput-loss assets from the noise before the turnaround scope freezes *(≈4 min)*

**Persona:** Maintenance & Reliability Planner • **Job to be done:** Pull the next-cycle swap list from telemetry and event history before the turnaround scope-lock meeting — not after.

*This is where the turnaround AFE list takes shape. Two questions in, the Planner already has the ranking that used to take a full day of CMMS reports stitched together with the vibration team's export.*

### Question (Act 1.1)

> **Top 10 equipment assets by total throughput loss (barrels) over the last 12 months.**

**What to say while it runs:** Throughput loss in barrels is where the conversation starts because it converts directly to margin. Top-quartile refiners run >96% mechanical availability — every 1% of availability lost on a 200 KBD refinery is roughly 730,000 barrels a year of lost throughput, and at $10/bbl gross margin that's $7M.

**What to look for:** Top 10 assets by `total_throughput_loss_bbl` over 12 months. Look at the top three — those are the assets that will dominate the turnaround scope-lock conversation.

**Land the point:** Now the Reliability Planner can size the turnaround AFE on dollars at risk, not on the loudest engineer in the room — that's the swap-vs-ride decision in minutes instead of a quarter.

### Question (Act 1.2)

> **Show monthly trend of unplanned downtime hours by process unit for the trailing 12 months.**

**What to say while it runs:** Unplanned downtime hours by process unit is the leading indicator that tells you whether the predictive program is winning. The FCC and Hydrocracker are the high-margin units — any month they spike on downtime, every barrel that didn't move through is $1-5M of margin walking out the door.

**What to look for:** Monthly trend of `total_downtime_hours` by process unit over 12 months — `DATE_TRUNC('month', ...)`. The inflection months tell you when a failure mode broke containment and started costing money.

**Land the point:** Before this space, that chart was rebuilt for the reliability steering committee once a month. Now it's the Planner's first question of the day — and the executive team gets the same view, in real time.

---

## Act 2 — The decision — turnaround swap list, predictive catch defense, failure-mode capex *(≈4 min)*

**Persona:** Refinery Manager • **Job to be done:** Lock the turnaround swap list and decide which failure modes get a capital-protection program vs. accepted into the next cycle.

*Three questions that turn the daily telemetry into a defensible turnaround AFE. The middle question is the anchor — predicted-RUL-under-30-days converted into avoided shutdown dollars.*

### Question (Act 2.1)

> **Which equipment has predicted remaining useful life under 30 days right now?**

**What to say while it runs:** Predicted RUL under 30 days is the actionable end of the model — and it's the list every Reliability VP wants on their desk before the turnaround scope freezes. RUL under 30 days on a critical FCC or Hydrocracker asset is not a watch-list item, it's a swap-or-pull decision.

**What to look for:** A short table of assets where `min_rul_days < 30`, with process unit. The shape matters — if two are on the same FCC train, that's a sequenced shutdown, not two independent jobs.

**Land the point:** That list used to be the output of a half-day comparing vibration trends against work-order history. Now it's the input to the turnaround scope-lock meeting that happens at 8 AM Monday.

### Question (Act 2.2)

> **What share of maintenance events were predicted by the ML model, by failure mode?**

**What to say while it runs:** Predictive catch rate by failure mode is the program-defense number. The Reliability VP has to defend the predictive investment every quarter — and the answer is *was_predicted = TRUE* divided by total events, by failure mode. Above 70% catch on rotating equipment is industry-leading; below 40% on a class of asset is the funding-pressure cliff.

**What to look for:** Catch-rate by failure mode. Pareto shape — a few failure modes will dominate, and the catch-rate gap is where the next ML investment gets sized.

**Land the point:** When the Planner, the Refinery Manager, and the Reliability VP all see the same catch-rate breakdown, the predictive-program funding conversation stops being about whose anecdote is more recent and starts being about *which failure modes get the next ML investment*.

> **Anchor moment.** Stop on the RUL-under-30-days list. Pick the worst — call it a critical FCC compressor or hydrocracker charge pump with RUL flagged at 21 days.

> *An unplanned shutdown of the FCC or Hydrocracker is $1-5M/day of lost margin on a refinery our size. Call it $3M/day. A typical predictive-driven controlled swap is $1-3M of work, scheduled into a planned 5-7 day window — versus a forced unplanned shutdown that often runs 14-21 days because nothing is staged. Avoiding a single two-week unplanned shutdown is $40-60M of preserved margin against a $2M swap cost. Payback is 1-2 days. Stack across the 4-6 critical-RUL assets the model surfaces in a typical year and the conversation isn't *can we justify the predictive program*, it's *which assets get the next replacement slot and which earn the ride*.*

> That's the decision this space automates. Not the reliability dashboard. The turnaround swap list, the predictive-program defense, and the next-cycle capex ranking — all on the same data the Refinery Manager defends to the executive team.

### Question (Act 2.3)

> **Top 10 process units by total repair spend year-to-date.**

**What to say while it runs:** Repair spend by process unit is the dollar overlay on the operational story. The FCC and Hydrocracker will usually be at the top — but if a smaller treating unit shows up in the top 3, that's a fleet-wide-design-flaw conversation, not a one-asset replacement.

**What to look for:** Top 10 process units by `total_repair_cost_usd` YTD. Match against the throughput-loss ranking from Act 1 — when a unit is in both top-10 lists, it earns capex protection in the next cycle.

**Land the point:** That cross-cut used to take a full day in Excel against the CMMS extract. Now it's a 15-second question — and it is the conversation that ranks the next $20M of reliability capex.

---

## Act 3 — The commitment — locking the availability story for the executive committee and shaping the predictive roadmap *(≈4 min)*

**Persona:** Reliability VP • **Job to be done:** Defend the reliability program's quarter-over-quarter availability trend to the executive team and lock the next cycle's predictive-program investment.

*The Reliability VP doesn't need another KPI dashboard; they need the same numbers the Planner and the Refinery Manager are already acting on, in the same language, so the executive availability narrative writes itself.*

### Question (Act 3.1)

> **How has average equipment availability trended month-over-month across the refinery?**

**What to say while it runs:** Equipment availability trend month-over-month across the refinery is the executive-committee headline. Top-quartile is >96%. If we're trending at 94% and the predictive program is supposed to be lifting us, the executive team wants to see the curve bend — not hear about catch-rate anecdotes.

**What to look for:** Monthly trend of `avg_health_score` and availability across the refinery. The inflection point is the conversation — what changed in the program when the curve started bending.

**Land the point:** When that curve is in the Reliability VP's hand the day before the executive review, the availability conversation moves from defensive to programmatic — and the executive team stops finding out about reliability problems from the daily ops report.

### Question (Act 3.2)

> **Which failure modes drove the most throughput loss this quarter, and at what total repair cost?**

**What to say while it runs:** Failure modes ranked by throughput loss and repair cost is the *which failure modes earn the next predictive investment* view. The Pareto tells you where to spend the next ML dollar — and the dollar overlay tells you whether it's a capex protection or a tuning campaign.

**What to look for:** Failure modes ranked by `total_throughput_loss_bbl` with `total_repair_cost_usd` attached. The shape determines whether the next investment is a vibration-monitoring expansion, an acoustic-monitoring pilot, or a corrosion-prediction model.

**Land the point:** Turnaround swap list at 8 AM, predictive-program roadmap at 10 — same space, same numbers. The Planner's scope list, the Refinery Manager's capex ranking, and the Reliability VP's program defense are now the *same artifact* — and the executive team gets one reliability story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RefineGuard Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 equipment assets by total throughput loss (barrels) over the last 12 months.
2. Show monthly trend of unplanned downtime hours by process unit for the trailing 12 months.
3. Which equipment has predicted remaining useful life under 30 days right now?
4. What share of maintenance events were predicted by the ML model, by failure mode?
5. Top 10 process units by total repair spend year-to-date.
6. How has average equipment availability trended month-over-month across the refinery?
7. Which failure modes drove the most throughput loss this quarter, and at what total repair cost?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
