# SiliconPath Design — Demo Script

**Space:** Semiconductor — SiliconPath - Design Space Simulation 🧪
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Engineering + CTO, alongside Design Engineering leads and IP Architecture
**KPIs touched:** Timing slack, Dynamic power, Leakage power, Die area, DRC violations, Pareto front size
**Big decision automated:** Tape-out go / no-go on the 3nm and 5nm blocks this quarter — which 2 designs commit the $5-30M mask set, which 1 gets a re-spin, and which design family gets the next $50M of engineering headcount.

---

## Pre-demo checklist

- Open the Genie space `SiliconPath - Design Space Simulation 🧪`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> SiliconPath Design carries 20 chip designs across Application Processor, AI Accelerator, RF Modem, IoT Controller, and Power Management families on 3nm, 5nm, 7nm, and 14nm nodes. Today the DRC violation log lives in the Design Engineering Cadence/Synopsys reports, the PPA Pareto front lives in IP Architecture's weekly EDA Excel, and design_closure_status sits on the VP of Engineering's quarterly tapeout review slide. Three artifacts, one decision — and the last tape-out slipped because the Blocked-design count wasn't visible until the milestone review. A 5nm mask set is $5-30M and a tape-out slip is $20-50M of NPV plus a competitive socket lost. This space ends the surprise. One governed surface that converts the nightly simulation run into the *tape-out commit vs. re-spin vs. headcount-add* decision in the same conversation.

---

## Key KPIs in scope

- Timing slack (ns) — worst negative slack; ≥0 means timing closure achieved
- Dynamic power (mW) — switching power; critical for mobile/edge SoCs (<500 mW typical)
- Leakage power (mW) — static power; gating factor for thermals at 5nm/3nm
- Die area (mm²) — silicon cost driver; advanced nodes target <100 mm² for high-volume
- DRC violations — design rule check failures; must reach zero before tapeout
- Pareto front size — number of optimal PPA tradeoff points discovered
- Convergence % — share of optimization runs that closed all constraints; target 80%+
- Design closure status — share of designs Blocked vs Complete; tapeout-readiness signal

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **PPA** | Power Purchase Agreement |
| **VP** | Vice President |

---

## Act 1 — The signal — which designs are bleeding DRC violations before tape-out lockdown *(≈4 min)*

**Persona:** Design Engineering lead • **Job to be done:** Get yesterday's simulation run results into a ranked list of designs that are not converging — by avg_drc_violations and completed_runs ratio — before the tape-out window closes.

*This is the moment the tape-out short-list starts forming. Two questions in, the lead has the designs that need re-spin attention versus the ones that are clean enough to commit a mask set against.*

### Question (Act 1.1)

> **Which 10 designs have the highest average DRC violations in the trailing 12 months?**

**What to say while it runs:** DRC violations have to reach zero before tapeout — there is no negotiation on this. Top 10 designs by avg_drc_violations over 12 months is the list of who has been chronically dirty, and chronic dirty in a 3nm flow means we are not closing in time for the next mask-set committee.

**What to look for:** A ranked table from simulation_run_metrics with avg_drc_violations and unique_design_count. The bottom 3 are the ones the lead has to either swap engineering capacity onto or schedule for re-spin.

**Land the point:** Right there is the tape-out commit conversation. Now the Design Engineering lead can name the at-risk designs in minutes — that's the mask-set commitment conversation that used to wait for the Friday block-leads sync.

### Question (Act 1.2)

> **Show monthly trend of completed simulation runs by design family.**

**What to say while it runs:** Now the monthly trend of completed_runs by design_family — Application Processor vs AI Accelerator vs RF Modem vs IoT Controller vs Power Management. If completed_runs is flat while DRC violations climb, the toolchain or the floorplan is the bottleneck, not engineering hours.

**What to look for:** Monthly trend, DATE_TRUNC('month', run_date) shape, broken out by design_family. Watch the AI Accelerator and RF Modem lines — those are the families where mask-set economics are most punishing.

**Land the point:** Before this space, that chart was assembled by the EDA admin from Cadence run logs. Now the design lead opens with it — and the conversation about whether we need more compute or more engineers happens an hour earlier.

---

## Act 2 — The decision — tape-out commit, re-spin, or kill *(≈4 min)*

**Persona:** VP of Engineering • **Job to be done:** Commit the next mask set on the designs that are converging and pull the trigger on re-spin or kill for the ones that aren't.

*Three questions that turn the Design Engineering watchlist into a tape-out commit memo. The middle question is the anchor — the convergence-and-Pareto conversation that converts engineering signals into mask-set dollars.*

### Question (Act 2.1)

> **Which design families have the most Blocked designs this quarter — what is blocking tapeout?**

**What to say while it runs:** Blocked-design count by family this quarter is the no-tapeout signal. A design with design_closure_status = 'Blocked' isn't a budget conversation, it's a calendar slip — and at 3nm a one-quarter slip costs the socket.

**What to look for:** blocked_design_count from optimization_result_metrics by design_family. Anything above 2 in a family is a structural issue in the methodology, not a single-design issue.

**Land the point:** That list used to be a Cadence and Synopsys spreadsheet roll-up that took two days. Now it's the input to the mask-set commit memo the VP signs Friday.

### Question (Act 2.2)

> **Top 10 designs by best performance score this month, with their power and area tradeoffs.**

**What to say while it runs:** Top 10 designs by best_performance_score with their best_power_mw and best_area_mm2 alongside is the PPA Pareto in one view. The flagship has to clear performance AND fit thermal AND fit die-cost — all three, in one row.

**What to look for:** A ranked table from optimization_results with the three PPA columns side-by-side. The designs at the top of performance but with leakage above target are the thermal-fail risks. The ones with strong PPA AND clean DRC are the tape-out short-list.

**Land the point:** When Design Engineering, IP Architecture, and the VP all query the Pareto the same way and see the same number, the meeting stops being whose simulation run is current and starts being which 2 blocks get the mask set.

> **Anchor moment.** Stop on the blocked_design_count chart from Q1 and the PPA Pareto on screen. Pick the worst case — say AI Accelerator has 3 Blocked designs at 3nm with avg_convergence_pct hovering at 55%, and the flagship has best_performance_score in the top 3 but leakage_power_mw is 30% over budget.

> *A 3nm mask set runs $5-30M; call it $15M for the flagship. A tape-out slip on this design is $20-50M of NPV plus the socket. If we commit on the dirty flagship at 55% convergence, the expected outcome is a re-spin — and a re-spin at 3nm is $10-15M of mask costs plus one quarter of slip, call it another $25M of NPV. The right call is: re-spin the AI Accelerator now at $5M of engineering cost rather than tape-out and discover the leakage fail at first silicon. Across the 5nm and 3nm portfolio, that's $30-60M of mask-set risk we are choosing to retire this quarter. Conversely, the Power Management family at 90% convergence and clean DRC commits its mask set Friday and clears the path for $100-200M of annual revenue at production ramp.*

> That's the decision this space automates. Not the slide. The decision. Two tape-outs committed, one re-spin authorized, $50M of headcount reallocated from the Blocked methodology to the family that's ramping — in one conversation, with one set of numbers.

### Question (Act 2.3)

> **How has average convergence percentage trended month-over-month by design family?**

**What to say while it runs:** Now avg_convergence_pct trended monthly by family — the methodology health number. Industry target for a healthy advanced-node flow is 80%+. Below 70% and we're throwing engineering hours at a methodology problem.

**What to look for:** Trend lines per family, monthly. A family stuck below 70% for 3+ months is where the next engineering-headcount investment has to go, or where we accept the family won't make next year's roadmap.

**Land the point:** That comparison is the difference between knowing a design is hard and knowing the methodology itself is the bottleneck. The first is a status report; the second is a re-org and a capex line.

---

## Act 3 — The commitment — shaping next year's tape-out roadmap and the engineering capex *(≈4 min)*

**Persona:** CTO • **Job to be done:** Defend the tape-out roadmap to the board and lock in the design-family investment mix and the EDA capex for next fiscal year.

*The CTO doesn't need more PPT decks; they need the same numbers Design Engineering is acting on, in the same language, so the roadmap defense and the EDA capex conversation become the same artifact.*

### Question (Act 3.1)

> **Which target process nodes have the worst average timing slack — where are we missing closure?**

**What to say while it runs:** Worst average timing_slack by target_node_nm — 3nm, 5nm, 7nm, 14nm. Slack <0 means we're missing closure; the node where total_timing_slack_ns is dragging hardest is where the methodology has to evolve or the roadmap has to slip.

**What to look for:** Per-node ranking from simulation_run_metrics. If 3nm is dragging while 5nm is clean, that's the EDA-tools or library-IP conversation. If both advanced nodes are dragging, that's a hiring conversation.

**Land the point:** When this curve is in the CTO's hand a quarter before the roadmap commit, the board conversation moves from reactive to programmatic — and the executive team stops being told about tape-out slips after they happen.

### Question (Act 3.2)

> **What is the total leakage power across all 5nm and 3nm designs, and how does that trend monthly?**

**What to say while it runs:** Total_leakage_power_mw across all 5nm and 3nm designs, trended monthly. Leakage is the thermal-budget gate for mobile and edge SoCs — once a node-family aggregate leakage starts climbing, the customer-facing SKU mix has to change.

**What to look for:** Monthly trend of total_leakage_power_mw from simulation_run_metrics, filtered to 3nm and 5nm. An inflecting line is the cue to either invest in low-leakage IP or pivot the roadmap.

**Land the point:** Triage at the standup, tape-out commit at the block-leads sync, roadmap defense at the board. Same space. Same numbers. The Design Engineering watchlist and the CTO's roadmap pitch are now the same artifact — and the executive team gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — SiliconPath Design — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 designs have the highest average DRC violations in the trailing 12 months?
2. Show monthly trend of completed simulation runs by design family.
3. Which design families have the most Blocked designs this quarter — what is blocking tapeout?
4. Top 10 designs by best performance score this month, with their power and area tradeoffs.
5. How has average convergence percentage trended month-over-month by design family?
6. Which target process nodes have the worst average timing slack — where are we missing closure?
7. What is the total leakage power across all 5nm and 3nm designs, and how does that trend monthly?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
