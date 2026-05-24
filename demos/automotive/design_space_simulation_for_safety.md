# SafeDesign Automotive — Demo Script

**Space:** Automotive — SafeDesign - Safety Simulation Analytics 🧪
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director, Vehicle Program + Chief Safety Engineer, CAE Manager, Vehicle Program leadership
**KPIs touched:** Total simulation runs, Pass/fail rate, Five-star rating count, Average injury risk score, Peak deceleration, Cabin intrusion
**Big decision automated:** Lock the body-structure + material combination (model, structural thickness, airbag count, safety package) that wins NCAP 5-star at target weight — and kill the variants HPC throughput cannot finish before SOP.

---

## Pre-demo checklist

- Open the Genie space `SafeDesign - Safety Simulation Analytics 🧪`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> Apex Motor Group is running design-space exploration on 8 body programs (Guardian Sedan, Fortress SUV, Ironclad Truck, Shield EV, Rampart Crossover, Aegis Wagon, Sentinel Coupe, Bulwark Van) across 5 crash modes — Full Frontal, Frontal Offset, Side Impact, Rear Impact, Rollover. Today the injury-risk numbers come out of the CAE Manager's HPC job-log workbook, the 5-star yield count sits in the Chief Safety Engineer's NCAP tracker, and the weight-vs-safety tradeoff is whichever PowerPoint the Vehicle Program lead built last Friday. A single 56-km/h frontal sim is 10–12 hours on HPC, and the program needs thousands of runs across configurations — which means the *which body/material combo do we lock for SOP* call gets made on whoever's spreadsheet was loudest on Thursday. This space ends that. One governed surface where simulation throughput, injury risk, 5-star yield, and the weight-vs-safety tradeoff live next to each other — and the body-lock decision happens in the room, not 3 reviews later.

---

## Key KPIs in scope

- Total simulation runs — HPC throughput per period
- Pass/fail rate — share of runs meeting injury-risk targets
- Five-star rating count — runs achieving NCAP 5-star outcome
- Average injury risk score — primary safety-performance metric per run
- Peak deceleration (g) — occupant-load indicator
- Cabin intrusion (mm) — structural-performance indicator
- Composite safety score — multi-parameter rollup on configurations
- Forecast error vs regulatory compliance — actual vs forecasted safety score on monthly cohort

---

## Act 1 — The signal — where the HPC budget is actually buying 5-star runs *(≈4 min)*

**Persona:** CAE Manager • **Job to be done:** Find which configurations are converting HPC hours into 5-star results vs. burning the queue on configurations that will never pass.

*Every CAE hour spent on a configuration that fails injury-risk targets is an hour the lead-program body lock doesn't get. Two questions in and the CAE Manager has the queue prioritization the team has been arguing about for a month.*

### Question (Act 1.1)

> **Show the monthly trend in total simulation runs and average injury risk score for the trailing 12 months.**

**What to say while it runs:** Monthly trend on total simulation runs and average injury risk score. The simulation count tells me throughput, the injury risk line tells me whether the design space is converging or thrashing. If runs are up but injury risk isn't dropping, we're burning HPC on dead branches.

**What to look for:** Twin lines over the trailing 12 months — `total_simulation_runs` and `avg_injury_risk_score` from the metric view. The room should watch for the inflection where runs spike but average injury risk plateaus — that's the moment we lost convergence and started throwing compute at the wrong configurations.

**Land the point:** Now the CAE Manager can tell the program lead *which months we burned the HPC budget vs. which months we earned 5-star credit* — that's the simulation-throughput conversation that used to take a quarterly review.

### Question (Act 1.2)

> **Top 10 model/body-type combinations by five-star safety rating count this year.**

**What to say while it runs:** Top 10 model and body-type combinations by `five_star_count` this year. This is the *which configurations are actually winning NCAP* list — and it's the only list that matters when we're locking the body for SOP.

**What to look for:** Ranked list — Guardian Sedan / Fortress SUV / Shield EV variants at the top, weaker body/safety-package combos at the bottom. The gap from #1 to #10 is the size of the convergence problem we still have left.

**Land the point:** That ranking used to be the output of a Friday-afternoon CAE Manager + program lead meeting. Now it's the first artifact in the room — and the body-program lock conversation starts where it should: with the configurations actually clearing the bar.

---

## Act 2 — The decision — locking the body-structure and material combo for SOP *(≈4 min)*

**Persona:** Chief Safety Engineer • **Job to be done:** Commit to the material + structural-thickness + airbag-count combination that hits 5-star at weight target — and defend the variants we're killing.

*Three questions that turn the simulation backlog into a defensible body-lock recommendation. The middle question is the anchor — the weight-vs-safety conversion that decides which configurations make SOP.*

### Question (Act 2.1)

> **Which crash test types have the highest fail count, and how does that break down by body type?**

**What to say while it runs:** Which crash test types have the highest `fail_count`, broken down by body type? Frontal Offset and Rollover are the two modes where most programs lose 5-star — if our fail count concentrates there for one body type, that's the structural problem we have to solve before SOP.

**What to look for:** A pivot — body_type × crash_test_type with `fail_count` from `simulation_runs_metrics`. Watch for a single body type lighting up red across two crash modes — that's the configuration getting cut.

**Land the point:** That heatmap is the kill-list. Now the Chief Safety Engineer can walk into the program review and say *these three configurations fail two crash modes and we're stopping the runs* — instead of letting the HPC queue decide that for us in week 11.

### Question (Act 2.2)

> **What is the average composite safety score by material type, and how does it correlate with average vehicle weight?**

**What to say while it runs:** Average `composite_safety_score` by `material_type` versus average `weight_kg`. This is the trade-curve the team has been arguing about — High-Strength Steel vs. Aluminum Alloy vs. Carbon Fiber Composite. Every kilogram of body weight is a kilogram off range or fuel economy; every safety point lost is a star lost.

**What to look for:** A scatter or paired-bar — material on one axis, `avg_composite_safety_score` and `avg_vehicle_weight` on the other. The room is looking for the material that sits highest on safety AND lowest on weight — that's the body-lock candidate.

**Land the point:** When the Chief Safety Engineer, the CAE Manager, and the program lead all query weight-vs-safety the same way and see the same trade-curve, the meeting stops being about whose material assumption is right and starts being about *which combo we're locking*.

> **Anchor moment.** Stop on the material/weight trade-curve and the deceleration ranking. Take the Guardian Sedan Advanced configuration — it's hitting 5-star on Frontal Offset but sitting 50 kg over target on High-Strength Steel. The question is whether swapping to Aluminum Alloy holds 5-star.

> *A 5-star NCAP outcome is worth ~$300–$800/unit in residual value and ~$500/unit in average OEM transaction price on a typical sedan program (industry resale data). At 50,000 Guardian Sedans/year, that's $15M–$40M/year of program economics riding on one body-lock decision. Lose 5-star on one trim and that's $20M of margin vaporized. Win 5-star at 50 kg lighter and we pick up ~3% fuel-economy / range — another $200/unit of CAFE/regulatory headroom. That's why the Chief Safety Engineer cares which row of the material table wins the simulation — it's not an engineering taste call, it's $20–40M of program margin.*

> That's the decision this space automates. Not the NCAP slide. The body-lock. Material + thickness + airbag-count gets committed on the trade-curve the simulations actually produced — and the variants that lose get killed in the program review, not in week 11 when the HPC queue runs out.

### Question (Act 2.3)

> **Top 10 configurations by average peak deceleration in frontal crash runs — where are we closest to occupant-load limits?**

**What to say while it runs:** Top 10 configurations by average `peak_deceleration_g` in frontal crash runs — where are we closest to occupant-load limits? FMVSS occupant chest-g and HIC thresholds aren't bright lines you cross safely. If a configuration is sitting within a few g of the limit, one supplier-material substitution and we're a recall waiting to happen.

**What to look for:** Ranked list of configs by `avg_peak_deceleration` in Frontal Offset + Full Frontal. The point isn't the absolute number — it's how much margin each configuration has against the limit.

**Land the point:** Now we know which configurations earn the airbag-count upgrade and which earn a re-design. That's a sourcing/BOM conversation, not a CAE conversation — and it's the right room to have it in.

---

## Act 3 — The commitment — defending the body-lock to the program executive review *(≈4 min)*

**Persona:** Vehicle Program lead • **Job to be done:** Take the locked body-structure recommendation to the executive program review, defend the kill-list, and protect the SOP launch window.

*The program lead doesn't need more simulations; they need the same numbers the CAE Manager and Chief Safety Engineer are committing to, framed against the regulatory and schedule risks the executive team actually asks about.*

### Question (Act 3.1)

> **How has the converged-design count trended month-over-month, and which body types are stalling?**

**What to say while it runs:** How has `converged_count` trended month-over-month, and which body types are stalling? Convergence is the schedule signal — if a body type isn't converging by month -6 to SOP, the launch window is moving. Period.

**What to look for:** Monthly trend of `converged_count` from `parameter_snapshots_metrics`, sliced by body_type. Watch for a body type whose convergence has flatlined for 2+ months — that's the program-risk flag.

**Land the point:** When the program lead walks into the executive review with this curve, the conversation is *here's the body that's on schedule, here's the one that needs an extra HPC allocation* — not *we'll know in 4 weeks*. That's how the launch window gets defended, not negotiated.

### Question (Act 3.2)

> **How accurate were our monthly forecasted vs actual safety scores, and which model programs missed regulatory compliance?**

**What to say while it runs:** Monthly forecasted vs actual safety scores, and which model programs missed `regulatory_compliance`. The CAE model is only as good as its track record — if a program's forecasts have been low by 5+ composite points all year, we don't trust this month's number on the body-lock call.

**What to look for:** Paired bars by `model_name` — `forecasted_safety_score` vs `actual_safety_score` from `simulation_summary_monthly`, with `regulatory_compliance` as a status flag. Programs in the 'Non-Compliant' or 'Under Review' state are the ones the executive team will ask about.

**Land the point:** Three artifacts — kill-list, body-lock, schedule risk — all from the same governed surface. Now the program executive review is a decision meeting, not a status meeting. That's the conversation that used to need a steering committee.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — SafeDesign Automotive — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in total simulation runs and average injury risk score for the trailing 12 months.
2. Top 10 model/body-type combinations by five-star safety rating count this year.
3. Which crash test types have the highest fail count, and how does that break down by body type?
4. What is the average composite safety score by material type, and how does it correlate with average vehicle weight?
5. Top 10 configurations by average peak deceleration in frontal crash runs — where are we closest to occupant-load limits?
6. How has the converged-design count trended month-over-month, and which body types are stalling?
7. How accurate were our monthly forecasted vs actual safety scores, and which model programs missed regulatory compliance?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
