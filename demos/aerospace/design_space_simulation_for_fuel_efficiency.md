# AeroSim Dynamics — Demo Script

**Space:** Aerospace — AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Engineering + Chief Engineer, Optimization Lead
**KPIs touched:** Specific fuel consumption, Lift-to-drag ratio, Drag coefficient, Fuel efficiency improvement % vs. baseline configuration, Pareto-optimal design count, Technology Readiness Level
**Big decision automated:** Which 2-3 wing-and-engine configurations to freeze and carry into preliminary design review — locking the design that hits the airline customer's fuel-burn target without slipping the cert window.

---

## Pre-demo checklist

- Open the Genie space `AeroSim Dynamics - Fuel Efficiency Design Optimization 🧪`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroSim Dynamics is exploring 20 candidate aircraft configurations for a next-gen narrowbody — four wing types (Conventional, Folding Wingtip, Truss-Braced, Blended Wing Body) crossed with four engine architectures (Turbofan, Geared Turbofan, Open Rotor, Hybrid Electric). Today the L/D and SFC numbers live in the Chief Engineer's CFD-results spreadsheet, the Pareto-front analysis lives in the Optimization Lead's Python notebook, and the TRL maturity rollup lives in the program-review deck the VP of Engineering rebuilds every quarter. Three artifacts, same 20 configs — and the design freeze gets pushed another quarter because nobody can defend which config carries forward without re-running the math live in the room. This space ends that. One governed surface where fuel burn, L/D, Pareto status, TRL, and compute spend sit on the same axis, so the design freeze becomes a defensible decision instead of a recurring debate.

---

## Key KPIs in scope

- Specific fuel consumption (SFC, kg/nm) — top design objective
- Lift-to-drag ratio (industry benchmark: 18-20 narrowbody, 19-22 widebody)
- Drag coefficient (Cd) — Cd reduction of 1% ≈ 0.7% fuel savings
- Fuel efficiency improvement % vs. baseline configuration
- Pareto-optimal design count
- Technology Readiness Level (TRL 1-9; production-ready ≥ TRL 7)
- Compute hours per design iteration
- Convergence residual — CFD solution quality indicator

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the configurations that beat fuel-burn target without breaking the cert calendar *(≈4 min)*

**Persona:** Chief Engineer • **Job to be done:** Identify which configurations are simultaneously hitting the SFC target AND mature enough on the TRL curve to make the certification timeline.

*This is the moment the design-freeze shortlist starts forming. Two questions in, the engineer already has the candidates that earn another round of CFD spend versus the ones that get retired.*

### Question (Act 1.1)

> **Top 10 configurations by lowest fuel burn — and which are Pareto-optimal?**

**What to say while it runs:** Fuel burn ranking is where the engineering team anchors — but it's the intersection with Pareto status that funds the next iteration. Configurations that aren't on the Pareto front are dominated by something else; they're not coming with us. The cutoff is the bottom row of the top 10 that's still flagged Pareto-optimal.

**What to look for:** A ranked table of 10 configurations by lowest fuel_burn_kg_nm with their is_pareto_optimal flag. The room should see that some low-fuel-burn configs are NOT Pareto-optimal — those are technically interesting but commercially dead.

**Land the point:** Right there is the shortlist the chief engineer carries into the design-freeze review. Pareto-dominated configurations get retired today, not after another $500K of CFD compute.

### Question (Act 1.2)

> **Show monthly trend in average lift-to-drag ratio by wing type for the trailing 12 months.**

**What to say while it runs:** Now L/D trend by wing type over 12 months. Narrowbody benchmark is 18-20, widebody 19-22, BWB candidates need 25+ to justify the airframe risk. A 1% drag improvement is roughly 0.7% fuel savings — that translates to about $200K per year per aircraft in operating cost. Watch for wing types where the curve has flattened — that's diminishing returns.

**What to look for:** Monthly L/D bars by wing_type using `DATE_TRUNC('month', ...)`. Plateaus mean the design space is exhausted; rising lines mean the optimizer is still finding gains worth funding.

**Land the point:** Before this space, that chart was rebuilt for the quarterly tech review. Now it's the engineer's first question of the morning — and the 'kill this wing type vs. fund another round' conversation starts a quarter earlier.

---

## Act 2 — The decision — freezing the design, retiring the dominated configs, defending the cert window *(≈4 min)*

**Persona:** Optimization Lead • **Job to be done:** Commit to a 2-3 configuration shortlist for design freeze and recommend which engine architectures get killed before they consume more HPC budget.

*Three questions that turn the candidate list into a defensible portfolio recommendation. The middle question is the anchor — converting fuel-burn improvement into airline lifetime-savings the program board will sign off on.*

### Question (Act 2.1)

> **Which engine types have the highest fuel efficiency improvement vs. baseline this year?**

**What to say while it runs:** Fuel efficiency improvement by engine architecture — production gate is 15% vs. baseline. Anything under 15% doesn't justify the cert risk; anything above 20% is where the airline customer starts writing letters of intent. Geared Turbofan and Open Rotor usually fight it out here.

**What to look for:** Engine architectures ranked by avg_fuel_efficiency_improvement_pct. Watch the gap between #1 and #3 — if it's tight, the choice is risk-driven; if it's wide, the lead candidate is obvious.

**Land the point:** That ranking is the engine-architecture down-select. Two queries in, the optimization lead has the defensible kill list — and the conversation with the engine OEMs moves from 'we're still evaluating' to 'we're freezing on these two architectures.'

### Question (Act 2.2)

> **How many Pareto-optimal designs do we have by wing type, and what is their average drag coefficient?**

**What to say while it runs:** Pareto-optimal count by wing type with average drag coefficient. A wing type with many Pareto designs at low Cd is a fertile design space — fund more iterations. A wing type with one Pareto winner at high Cd is a one-trick pony — freeze the winner and move on.

**What to look for:** Wing types ranked by pareto_run_count alongside min_drag_coefficient. The combination tells you where compute budget keeps paying off vs. where it's exhausted.

**Land the point:** That table is the next round's HPC budget allocation. Truss-Braced gets another $2M of compute, BWB-Hybrid gets frozen at its current best, Folding Wingtip gets retired. Defensible, on dollars and L/D, not on whose pet design is loudest.

> **Anchor moment.** Stay on the engine-architecture and wing-type rankings. Pick the lead config — say Geared Turbofan + Truss-Braced — sitting at 18% fuel efficiency improvement vs. baseline.

> *Jet fuel runs ~$3/gallon and a narrowbody burns about 800 gallons per hour at cruise. 18% fuel improvement on a 3,000-hour-per-year utilization is ~430,000 gallons saved per aircraft per year — call it $1.3M per aircraft annually at $3/gal. An airline customer ordering 100 aircraft over a 25-year program lifetime sees $3.3B of lifetime fuel savings. The 1% Cd improvement the Truss-Braced wing is delivering compounds on top of that. That's the number the airline writes the LOI against.*

> That's the decision this space defends. The design freeze isn't 'whose simulation looked prettiest' — it's the configuration that backs $3B of airline lifetime-savings math. HPC budget moves accordingly; the cert window holds because the dominated configs got retired last quarter, not next quarter.

### Question (Act 2.3)

> **Top 10 configurations by compute hours consumed — are they delivering Pareto results?**

**What to say while it runs:** Top 10 configurations by compute hours consumed — and whether they're delivering Pareto results. This is the diagnostic the optimization lead uses to decide which configs are burning HPC budget without paying it back. Anything in the top 10 of compute with zero Pareto runs is a kill candidate.

**What to look for:** Configurations ranked by compute_hours with their pareto_run_count alongside. Big number, small Pareto count = retire.

**Land the point:** That's the difference between an optimization program that converges and one that consumes budget forever. Compute dollars move to the configs paying them back; the rest get frozen or retired.

---

## Act 3 — The commitment — defending the design freeze to the program board and the launch airline *(≈4 min)*

**Persona:** VP of Engineering • **Job to be done:** Lock the design-freeze decision in front of the program board, defend the cert calendar, and shape next year's R&D investment between the surviving configurations.

*The VP doesn't need new charts — they need the same fuel-burn and Pareto numbers the engineering team is acting on, in the language the program board and the launch airline both speak.*

### Question (Act 3.1)

> **Show monthly trend in Pareto-optimal run count over the last 12 months.**

**What to say while it runs:** Pareto-optimal run count by month over the last year. This is the program-health line — if it's climbing, the optimization program is converging on better designs; if it's flat, we're at the efficient frontier and design freeze is the right call.

**What to look for:** Monthly pareto_run_count trend. A plateauing line is the signal that the design space is exhausted and the freeze decision is ripe.

**Land the point:** When that line goes flat, the VP can walk into the program board and say 'we've found the efficient frontier, here are the 3 configurations on it, here's the freeze recommendation.' Defensible. On data. Not on calendar pressure.

### Question (Act 3.2)

> **Which configurations have reached TRL 7 or higher, and what is their fuel efficiency improvement?**

**What to say while it runs:** TRL maturity vs. fuel efficiency improvement on the surviving configs. Production gate is TRL 7. Anything in the design freeze candidate set still sitting at TRL 5 means we're betting cert on two more years of tech maturation — that's a CFO conversation, not a freeze conversation.

**What to look for:** Surviving configs with their avg_trl and avg_fuel_efficiency_improvement_pct. The quadrant matters — high improvement + low TRL = risk; high improvement + TRL 7+ = freeze candidate.

**Land the point:** Engineering, optimization, and program management now share one view. The launch airline gets one fuel-burn commitment number. The cert calendar gets defended on the same configs the optimization team is funding. One space. One story.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroSim Dynamics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 configurations by lowest fuel burn — and which are Pareto-optimal?
2. Show monthly trend in average lift-to-drag ratio by wing type for the trailing 12 months.
3. Which engine types have the highest fuel efficiency improvement vs. baseline this year?
4. How many Pareto-optimal designs do we have by wing type, and what is their average drag coefficient?
5. Top 10 configurations by compute hours consumed — are they delivering Pareto results?
6. Show monthly trend in Pareto-optimal run count over the last 12 months.
7. Which configurations have reached TRL 7 or higher, and what is their fuel efficiency improvement?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
