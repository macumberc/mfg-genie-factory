# PlanWorks Manufacturing — Demo Script

**Space:** Machinery — PlanWorks Manufacturing - Resource Planning 🏭
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Operations + Production Planner, Scheduler, CFO
**KPIs touched:** Schedule adherence, Capacity utilization, On-time work order completion, Throughput, Efficiency, Overtime hours
**Big decision automated:** Which 5-10 work orders get expedited this week vs. deferred, which work centers absorb a capacity shift across departments, and which tier-2 components move from make to buy on the next quarter's MRP run.

---

## Pre-demo checklist

- Open the Genie space `PlanWorks Manufacturing - Resource Planning 🏭`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PlanWorks runs 20 work centers across six work-center types — CNC Machining, Lathe Operations, Welding, Assembly, Painting, Testing — distributed across four departments (Dept-A through Dept-D). Today the Production Planner releases work orders out of the SAP MRP run, the Scheduler resequences them in a separate APS/Preactor tool, and the VP Operations tracks schedule adherence and overtime in a weekly Excel rolled up from work-center supervisors. Three systems, the same work-order backlog, and the expedite-vs-defer call gets made every Monday on whichever spreadsheet was freshest at the meeting. This space ends that: one governed surface where schedule adherence, capacity utilization, queue hours, and overtime all resolve to the same work center and the same week — so the expedite list, the capacity rebalance, and the make-or-buy call can be made on the same dollars.

---

## Key KPIs in scope

- Schedule adherence (%) — target ≥90%
- Capacity utilization (%) — sweet spot 80–90%, >95% triggers expedite/overtime
- On-time work order completion (%) — target ≥95%
- Throughput (units) — capacity output indicator
- Efficiency (%) — actual vs standard hours, target ≥90%
- Overtime hours — cost and worker-burnout signal
- Changeover hours — SMED/lean improvement opportunity
- Queue hours — bottleneck and lead-time driver

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the work centers about to break overtime cover *(≈4 min)*

**Persona:** Production Planner • **Job to be done:** Build the expedite list and the at-risk-work-order list before the Monday production meeting, without rebuilding the APS extract.

*This is the conversation that determines who works overtime this week and which customer ships late. Two questions in, the Planner already has both lists.*

### Question (Act 1.1)

> **Top 10 work centers by capacity utilization this month — which are above 95% and risk overtime?**

**What to say while it runs:** Top 10 work centers by capacity utilization this month — anything above 95% is in expedite/overtime territory whether we like it or not. The sweet spot is 80-90%; above that and we're paying premium labor and burning equipment life to ship on time.

**What to look for:** Ranked work_center_id with utilization_pct. Watch for CNC Machining or Welding work centers showing up — those tend to be the bottlenecks because they're routing-shared across multiple product lines.

**Land the point:** When the Planner can see the over-95% work centers in 10 seconds, the load-balancing call happens before overtime is committed, not after the timecards come in on Friday. That's a five-figure weekly savings on labor cost alone.

### Question (Act 1.2)

> **What is the monthly trend in schedule adherence by work center type over the trailing 12 months?**

**What to say while it runs:** Monthly trend in avg_schedule_adherence by work_center_type. Target is 90%; world-class manufacturers run 95%+. Below 80% sustained means the MRP plan and shop reality have diverged — either the routings are wrong, the capacity model is wrong, or the priorities are getting overridden ad-hoc.

**What to look for:** Six lines on one chart — CNC Machining, Lathe Operations, Welding, Assembly, Painting, Testing. Watch for a department whose adherence has been declining for three months; that's where the MRP-vs-shop-reality fight is losing.

**Land the point:** Before this space, adherence-by-department was a slide the VP Ops rebuilt for the QBR. Now the Planner sees it on Monday and the corrective routing changes get queued for the next MRP run — not three months later in a Six Sigma project.

---

## Act 2 — The decision — capacity rebalance and the make-or-buy call *(≈4 min)*

**Persona:** Scheduler • **Job to be done:** Lock the recommendation on which work orders get expedited, which work centers shift load to other departments, and which tier-2 components move to outside-purchased.

*These three questions are where the operational decisions get committed for the week. Overtime correlation tells you whether utilization is real demand or just bad scheduling; on-time completion ranks who's missing customer commitments; changeover hours is the SMED ROI conversation.*

### Question (Act 2.1)

> **Which work centers have the highest overtime hours, and how does that correlate with utilization?**

**What to say while it runs:** Work centers with the highest overtime_hours, correlated with utilization_pct. The relationship matters: high utilization + high overtime is a real capacity gap. High overtime + medium utilization is a scheduling problem — we're paying for labor we didn't need to. Different fix for each.

**What to look for:** Ranked work_center_id with overtime_hours and utilization_pct side by side. Watch for the high-OT/medium-utilization rows; those are the schedulers' fastest wins.

**Land the point:** When the Scheduler can resolve overtime vs utilization in one query, the load-balancing decision moves from politics to pattern recognition. Overtime spend drops without missing a single shipment date.

### Question (Act 2.2)

> **Rank work center types by on-time work order completion — which are below the 95% target?**

**What to say while it runs:** Work_center_type ranked by avg_on_time_completion against the 95% target. Below 90% on a sustained basis means we're losing customer credibility — and at this scale, the LD (late delivery) penalties on heavy-equipment contracts run 2-5% of revenue per missed milestone. That's the dollar cost of the planning miss.

**What to look for:** Bar chart by work_center_type with avg_on_time_completion. The families below 90% are either expediting candidates or make-or-buy reconsideration candidates for the components routed through them.

**Land the point:** Same numbers the planner uses to release work, now framed as customer commitment. When CNC Machining sits at 87% on-time and Welding at 93%, the expedite list, the capacity shift, and the make-or-buy conversation all start from the same fact. That's the operating leverage.

> **Anchor moment.** Stop on the on-time-completion ranking and the overtime correlation chart. Pick CNC Machining as the work-center type — say it runs 88% on-time-completion against the 95% target, with two of the four CNC work centers at 98%+ utilization and meaningful overtime each week.

> *On a $200M annual production base, a 7-point on-time-completion gap on CNC Machining work translates into roughly 2-3% of revenue exposed to late-delivery penalties — call it $4-6M/year of LD penalty risk and customer credibility erosion. Capacity rebalancing across the four CNC work centers — shifting volume from Dept-A to under-utilized Dept-B — typically recovers 3-5 points of on-time-completion at zero capex, and that's $2-3M/year of avoided penalty. Layer the make-or-buy decision on tier-2 machined components — outsourcing 15% of the most-bottlenecked routings at a 10-15% buy-vs-make cost premium still nets $1-2M/year of avoided expedite and overtime. Combined: $5-8M/year of recoverable margin on a $200M base, and the capacity-expansion capex defer story writes itself.*

> That's the make-or-buy and capacity-rebalance commitment in one set of numbers. The Scheduler builds the week's expedite list from the same view the VP Ops uses to defend the FY plan to the CFO. Three teams, one shop floor, one set of numbers — and the capex deferral story is the leave-behind.

### Question (Act 2.3)

> **Show monthly trend in total throughput vs planned hours across all work centers.**

**What to say while it runs:** Top 10 work centers by total_changeover_hours. Changeover is non-value-added time; SMED programs typically target 50% reduction over two years. The biggest changeover-hour work centers are the biggest lean ROI opportunities — and on shared-routing work centers, every hour of changeover saved is an hour of capacity recovered.

**What to look for:** Ranked work_center_id with changeover_hours, ideally with the work-center type for context. Watch for Painting or CNC Machining work centers near the top; those are the high-leverage SMED targets.

**Land the point:** Changeover hours goes from an industrial-engineering KPI to a planner's daily input. When 200 hours of changeover get cut on the top three work centers, that's 200 hours of capacity that doesn't need to be added with capex — and the make-or-buy decision on the marginal tier-2 components shifts toward make.

---

## Act 3 — The commitment — locking the capacity plan and the FY MRP strategy *(≈4 min)*

**Persona:** VP Operations • **Job to be done:** Defend the capacity plan and the capex deferral story to the CFO, with the same numbers the Planner releases work against every Monday.

*The VP Operations walks into the FY plan defense with the planner's daily working numbers as the source of truth — not a reconstructed slide deck. That's the change.*

### Question (Act 3.1)

> **Top 10 work centers by changeover hours — where is the biggest SMED opportunity?**

**What to say while it runs:** Monthly trend in total_throughput overlaid with total_planned_hours across all work centers. We want throughput growing faster than planned-hours grow — that's productivity improvement. If they move together, we're just running harder, not smarter. If throughput is flat while hours grow, the operating leverage is gone.

**What to look for:** Two lines on one chart, 12 months. The shape of the gap between them is the productivity story the CFO wants to see at the FY review.

**Land the point:** When the VP Ops can show throughput-per-hour climbing in the same view the Planner uses to release work, the FY plan defense lands. The capacity-expansion capex conversation moves from 'we need another line' to 'we recovered 15% capacity from changeover reduction — defer capex one cycle.' That's the boardroom narrative.

### Question (Act 3.2)

> **Which work centers have the longest queue hours, and how is throughput trending there?**

**What to say while it runs:** Work centers with the longest queue_hours, with throughput trended alongside. Long queues at a work center mean either the MRP is over-loading it or the work center can't keep up — and both have different fixes. Queue at a CNC center suggests outsourcing; queue at Assembly suggests headcount.

**What to look for:** Ranked work_center_id with queue_hours and a trended view of throughput. Watch for a work center where queue is rising while throughput is flat — that's the bottleneck that's about to break customer commitments.

**Land the point:** Queue hours becomes the daily proxy for lead-time risk. When the Planner, the Scheduler, and the VP Ops all see the same queue data with the same routings, the expedite call, the capacity shift, and the make-or-buy decision all happen against the same numbers — and the CFO defers the capacity capex one more year because the operating leverage is real.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PlanWorks Manufacturing — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 work centers by capacity utilization this month — which are above 95% and risk overtime?
2. What is the monthly trend in schedule adherence by work center type over the trailing 12 months?
3. Which work centers have the highest overtime hours, and how does that correlate with utilization?
4. Rank work center types by on-time work order completion — which are below the 95% target?
5. Show monthly trend in total throughput vs planned hours across all work centers.
6. Top 10 work centers by changeover hours — where is the biggest SMED opportunity?
7. Which work centers have the longest queue hours, and how is throughput trending there?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
