# ChipArchitect Labs — Demo Script

**Space:** Computer & Electronic — ChipArchitect Labs - SoC Design Space Simulation 🧪
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Engineering + SoC Design Lead, VP Engineering, Program Management Office
**KPIs touched:** Convergence rate, PPA improvement, Best frequency, Best power, Pareto-optimal points found, Timing slack
**Big decision automated:** Which design family + process node combination gets the next tape-out slot, which design family gets another spin in simulation, and where to redirect the next 100K compute-hours of DSE budget.

---

## Pre-demo checklist

- Open the Genie space `ChipArchitect Labs - SoC Design Space Simulation 🧪`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> ChipArchitect Labs runs pre-silicon design-space exploration across a portfolio of SoC design families targeting multiple process nodes — each tape-out is a $5-15M mask-set commitment on advanced nodes and a 9-12 month schedule lock once committed. Today the PPA tradeoff lives in the design lead's spreadsheet, the compute-burn-rate lives in the PMO's quarterly slide, and the convergence-rate trend lives in the VP Engineering's roadmap deck. Three artifacts, same simulations — and the next tape-out commitment (the single most expensive decision the org makes in a year) gets argued in a 2-hour committee meeting nobody trusts the underlying numbers in. This space ends that. One governed surface where convergence rate, best frequency, best power, Pareto points, timing slack, and total sim hours land in the same conversation as the tape-out gate.

---

## Key KPIs in scope

- Convergence rate (%) — share of runs that meet timing/power/area constraints
- PPA improvement (%) — generation-on-generation power-performance-area lift
- Best frequency (GHz) — peak achievable clock under target voltage/power
- Best power (mW) — minimum power at target frequency, drives leakage budget
- Pareto-optimal points found — DSE coverage; richer Pareto = more design optionality
- Timing slack (ns) — closure margin; negative slack = violation
- Total simulation hours — compute spend; modern DSE frameworks cut iterations 75-90%
- Target met rate — share of optimization runs that meet PPA spec

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **PPA** | Power Purchase Agreement |
| **VP** | Vice President |

---

## Act 1 — The signal — separating designs that are converging from designs burning compute *(≈4 min)*

**Persona:** SoC Design Lead • **Job to be done:** Find the design families whose simulation runs are actually closing on PPA targets vs. the ones consuming compute on flat surfaces.

*This is where the tape-out shortlist starts forming. Two questions in, the design lead has the convergence picture that used to require a half-day of spreadsheet stitching across multiple project leads.*

### Question (Act 1.1)

> **Show monthly convergence rate and PPA improvement by design family for the trailing 12 months.**

**What to say while it runs:** Monthly convergence rate and PPA improvement by design family over 12 months. Convergence rate is the share of runs meeting timing/power/area constraints; a healthy DSE program tracks 60-80% and rising. Anything below 40% means the design family isn't ready for tape-out commitment — it's still in exploration, not optimization.

**What to look for:** Two-line chart per design family: avg_convergence_rate and avg_ppa_improvement, month over month. The families whose convergence is rising while PPA improvement holds steady are the obvious tape-out candidates; the ones with flat or falling convergence are still in the exploration regime.

**Land the point:** Right there is the first cut. Families that are converging on PPA are the ones to bring to the tape-out gate; families that aren't are the ones to either pull compute or kill before they consume another quarter of headcount.

### Question (Act 1.2)

> **Which 10 SoC designs have the highest total simulation hours this quarter, and what's the convergence rate?**

**What to say while it runs:** Top 10 SoC designs by total simulation hours this quarter with convergence rate alongside. Compute hours are the proxy for design-team time; modern DSE frameworks cut iteration count 75-90% over manual sweeps, so a design that's still burning hours without converging is one whose constraints need to be re-stated, not whose compute budget needs to be raised.

**What to look for:** Ranked table of soc_design by total_sim_hours with avg_convergence_rate side-by-side. The high-hours, low-convergence quadrant is where the budget is being burned on a problem that isn't well-formed.

**Land the point:** That table used to be a back-channel email thread between the design leads and the PMO. Now it's the design lead's first question — and the kill-or-continue conversation starts on numbers, not on whose project has the longest history.

---

## Act 2 — The decision — which design family + node combination earns the tape-out slot *(≈4 min)*

**Persona:** VP Engineering • **Job to be done:** Commit the next tape-out — pick the design family, lock the process node, and re-allocate compute budget away from designs that aren't earning their spend.

*Three questions that turn the convergence ranking into a defensible tape-out recommendation. The middle question is the anchor — the compute-spend math that converts the kill list into a dollar-denominated decision.*

### Question (Act 2.1)

> **How has the count of Pareto-optimal points trended month-over-month by design family?**

**What to say while it runs:** Pareto-optimal point count month over month by design family. Richer Pareto = more design optionality at the tape-out gate. A family with a growing Pareto front is one where the silicon team will still have room to negotiate against late-binding constraints; a family with a stalled Pareto is one whose design space has been fully explored — for better or worse.

**What to look for:** Monthly total_pareto_points by design_family. The families with climbing Pareto counts are the ones with active optimization headroom; the flat ones are the ones whose PPA story is essentially locked.

**Land the point:** That trend is the difference between a tape-out you commit because you've explored the space and a tape-out you commit because you ran out of time. Both ship; only one is defensible to the executive committee.

### Question (Act 2.2)

> **Top 10 design families by best achievable frequency at lowest power — what's the energy efficiency picture?**

**What to say while it runs:** Top 10 design families by best achievable frequency at lowest power. This is the energy-efficiency ranking — best frequency / best power, simultaneously. Modern flagship SoCs need to win both axes or they lose the workload they were designed for, and this ranking is where the tape-out shortlist actually gets ordered.

**What to look for:** Ranked table of design_family with best_frequency_ghz and best_power_mw. The Pareto winners on this view are the literal tape-out candidates.

**Land the point:** When the design lead, the VP, and the PMO all query best-frequency-at-best-power the same way, the tape-out debate stops being whose architecture is most loved and starts being whose PPA story is most defensible. That's a different gate meeting.

> **Anchor moment.** Hold on the timing-violation share and the total sim hours columns. Pick the worst design family — call it 12,000 sim hours per month on a family running 70% timing-violation rate.

> *Twelve thousand sim hours a month at roughly $2-3 per EDA cloud-compute hour for advanced-node simulation is $25-35K/month — call it $400K/year — burning on a family whose timing can't close. That's headcount, not just compute. Now scale: if the same compute pool funds a converging family instead, the team gains a full tape-out cycle of optimization headroom. And the alternative on the other side of the gate — a mask-set respin on an advanced node — is $5-15M and 9-12 months of schedule. One avoided respin pays for the entire DSE program five times over. The decision being made on this screen is multi-million-dollar capital allocation, not a slide layout.*

> That's the decision this space automates. Not the slide — the decision. Tape-out gate runs on PPA-and-convergence dollars, not on which design lead is loudest. The kill list runs on compute-burned-on-failed-sweeps math. The CFO finally has a one-page view that ties EDA spend to silicon outcomes.

### Question (Act 2.3)

> **Which design families have the highest share of timing-violation runs, and how much simulation compute is being burned on failed sweeps?**

**What to say while it runs:** Design families with the highest share of timing-violation runs and the compute being burned on failed sweeps. Negative timing slack is non-negotiable — a design that can't close timing in simulation won't close timing in silicon either, and the compute being spent chasing it is a sunk cost. This is the prioritization view for *killing* programs, not for tape-out.

**What to look for:** Ranked table of design_family by share-of-runs with negative timing_slack_ns, with total_sim_hours alongside. The high-violation, high-compute quadrant is the kill list.

**Land the point:** That ranking is the conversation the VP usually has alone with the design leads and now has with the PMO and finance in the same room. The compute being burned on failed sweeps gets a dollar value — and the kill decision moves from program politics to portfolio math.

---

## Act 3 — The commitment — shaping the SoC roadmap and the next compute envelope *(≈4 min)*

**Persona:** Program Management Office • **Job to be done:** Defend the tape-out and roadmap commitments to the executive committee and lock in next cycle's compute and headcount envelope.

*The PMO doesn't need more design data; they need the same convergence, PPA, and compute-burn numbers the VP is acting on, in the same definitions, so the roadmap defense writes itself.*

### Question (Act 3.1)

> **What is the total simulation compute spend by process node, and how does target-met rate compare across nodes?**

**What to say while it runs:** Total simulation compute spend by process node with target-met rate alongside. Newer nodes cost more per sim hour and demand higher convergence to justify the per-wafer premium. This is the chart that decides where the next $1-2M of EDA budget goes — by node, not by design family.

**What to look for:** Bar chart of total_sim_hours per process_node with target_met share side-by-side. The high-spend, low-target-met node is the one whose investment case needs the hardest justification at the next board update.

**Land the point:** That's the chart that defends the node strategy. Which nodes we're committing to, which we're cooling on, and what the compute envelope needs to look like for next year. The roadmap conversation moves from architecture lore to defensible portfolio math.

### Question (Act 3.2)

> **How has average best frequency and best power trended month-over-month across the SoC roadmap?**

**What to say while it runs:** Average best frequency and best power month over month across the SoC roadmap. This is the trajectory view — are we improving generation-on-generation, or are we plateauing? An R&D org that's plateaued on PPA is one whose next tape-out is the wrong tape-out, and that's a strategic conversation that needs evidence.

**What to look for:** Two-line monthly chart of avg(best_frequency_ghz) and avg(best_power_mw) across all design families. Inflection points up are tape-out windows; flat trends are signals to either re-architect or pivot nodes.

**Land the point:** Daily DSE triage at 8 AM, tape-out gate at 10, board roadmap defense at noon. Same space. Same numbers. The design lead's convergence picture and the PMO's roadmap pitch are now the same artifact — and the executive committee gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — ChipArchitect Labs — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly convergence rate and PPA improvement by design family for the trailing 12 months.
2. Which 10 SoC designs have the highest total simulation hours this quarter, and what's the convergence rate?
3. How has the count of Pareto-optimal points trended month-over-month by design family?
4. Top 10 design families by best achievable frequency at lowest power — what's the energy efficiency picture?
5. Which design families have the highest share of timing-violation runs, and how much simulation compute is being burned on failed sweeps?
6. What is the total simulation compute spend by process node, and how does target-met rate compare across nodes?
7. How has average best frequency and best power trended month-over-month across the SoC roadmap?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
