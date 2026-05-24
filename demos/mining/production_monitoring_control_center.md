# MineOps Central — Demo Script

**Space:** Mining — MineOps Central - Production Monitoring Control Center 📊
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Reliability + Processing Plant Lead, Mine Manager, CFO partner
**KPIs touched:** Mill throughput, Plant recovery, Concentrate grade, Equipment utilization, Bottleneck count, Energy intensity
**Big decision automated:** Which crusher and which mill to feed next quarter, which 2-3 bottleneck units get the debottleneck capex, and what ore-blend ratio gets locked into the mine plan to lift mill recovery.

---

## Pre-demo checklist

- Open the Genie space `MineOps Central - Production Monitoring Control Center 📊`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> MineOps Central runs concentrator plant analytics across 20 processing units — primary and secondary crushing, SAG and Ball mills, flotation cells, thickeners, and material handling. Today the throughput-by-stage picture lives in the Processing Plant Lead's shift handover sheet, the unplanned-downtime detail in the Mine Manager's weekly reliability report, and the cost-per-ton and energy-intensity view in the CFO partner's monthly opex review. Three artifacts, three cadences, same flowsheet — and the question of which bottleneck unit gets the next $10M of debottlenecking capex gets answered on whichever spreadsheet was most recently shared. This space ends that. One governed surface where stage throughput, recovery, energy intensity, and plan adherence sit in the same conversation that sets the capex slate and the ore-blend recommendation.

---

## Key KPIs in scope

- Mill throughput (tph and tpd) — primary driver of concentrate output; data spans ~100-1000 tph across the plant
- Plant recovery (%) — target 85-92% for sulfide flotation circuits
- Concentrate grade (%) — saleable product quality vs. smelter penalty thresholds
- Equipment utilization (%) — target 85%+ on critical-path mills and crushers
- Bottleneck count — number of constrained units in the flowsheet
- Energy intensity (kWh/ton) — opex and ESG-relevant; SAG benchmark 7-10 kWh/t
- Unplanned downtime hours — direct lost-production impact at $/ton concentrate
- Plan adherence (%) — actual vs. planned daily throughput

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **ESG** | Environmental, Social, Governance |
| **SAG** | Semi-Autogenous Grinding (mill) |
| **TPD** | Tons Per Day |

---

## Act 1 — The signal — finding the stage that's actually limiting the plant *(≈4 min)*

**Persona:** Processing Plant Lead • **Job to be done:** Pull the structural bottleneck out of last quarter's data — not by gut, by stage-level throughput and recovery.

*This is where the debottleneck shortlist starts forming. Two questions in, the Plant Lead already has the stage-level picture that used to take a day of stitching against the historian export.*

### Question (Act 1.1)

> **Show monthly average mill throughput (tph) by processing stage for the trailing 12 months.**

**What to say while it runs:** Monthly average throughput in tons-per-hour by processing stage for the last 12 months. The whole plant only runs as fast as its slowest stage — and the question is whether that slowest stage is the same one quarter after quarter, or whether the bottleneck moves.

**What to look for:** Twelve months of avg_throughput_tph by stage — primary crushing through flotation. Watch for the stage whose curve has flattened while feed is rising — that's the constraint.

**Land the point:** Before this space that picture was rebuilt by hand against the PI historian every month. Now it's the Plant Lead's first question of the day — and the debottleneck conversation starts on a quarter-over-quarter trend, not a yesterday's-shift anecdote.

### Question (Act 1.2)

> **Top 10 processing units by total unplanned downtime hours this quarter — which stage is driving it?**

**What to say while it runs:** Top 10 processing units by total unplanned downtime hours this quarter, with the stage each unit sits in. Concentrator unplanned downtime runs $50-150 per ton of ore lost at the mill. A unit with 200+ hours of downtime is a $1M-plus structural opex hit, not a maintenance write-off.

**What to look for:** Units ranked by total_downtime with their processing stage attached. The pattern to watch is whether the downtime is concentrated in one stage — that's the stage whose reliability investment has the biggest production lift.

**Land the point:** Now the Plant Lead can rank where the dollars are leaking in seconds — that's the input to the debottleneck conversation that used to require a reliability engineer to build a custom report.

---

## Act 2 — Feed, debottleneck, or re-blend — locking the capex and the ore plan *(≈4 min)*

**Persona:** Mine Manager • **Job to be done:** Decide which crusher and mill to feed next quarter, which 2-3 bottleneck units get the debottleneck capex, and what ore-blend ratio gets locked into the mine plan.

*Three questions that take the bottleneck shortlist into a defensible capex and ore-plan recommendation. The middle question is the anchor — energy intensity converted to opex dollars and the recovery gap converted to revenue dollars.*

### Question (Act 2.1)

> **Which units are most frequently flagged as bottlenecks, and what is their average utilization?**

**What to say while it runs:** Units most frequently flagged as bottlenecks with their average utilization. Critical-path mills and crushers should run >85% utilization. A unit running >85% AND flagged as a bottleneck is the obvious debottleneck investment; a unit flagged as a bottleneck at <70% utilization is a process-flow problem, not a capacity problem.

**What to look for:** Units ranked by bottleneck_count alongside avg_utilization. The split between the two patterns drives whether the answer is capex or process redesign.

**Land the point:** That used to be a quarterly reliability investigation. Now it's a Tuesday morning question — and the capex shortlist comes out of the same query.

### Question (Act 2.2)

> **How has plant recovery trended month-over-month by unit type across grinding and concentration?**

**What to say while it runs:** Plant recovery trended monthly by unit type across grinding and concentration. Sulfide flotation recovery target is 85-92%. A SAG-Ball-Flotation circuit whose recovery is sliding from 88% to 85% over two quarters is losing 3 percentage points of saleable concentrate — at our scale that's mid-seven figures a year.

**What to look for:** Monthly avg_recovery_pct by unit type. Watch for the inflection point — is the recovery slip in the grinding circuit (ore-blend issue) or in flotation (reagent or float-cell tuning)? The answer changes whose budget pays for the fix.

**Land the point:** Before this space the recovery conversation was a metallurgist's monthly memo. Now it's the input to the ore-blend recommendation that the Mine Manager sends back to the pit plan.

> **Anchor moment.** Stop on the recovery trend. The plant has slid from 88% to 85.5% recovery over the last two quarters. With the plant feeding ~25,000 tpd and a concentrate price equivalent to ~$80 per ton of ore at headline grades, every percentage point of recovery is real revenue.

> *2.5 percentage points of recovery loss across ~25,000 tpd of ore = 625 tons/day of saleable concentrate-equivalent lost. At ~$80/ton of ore equivalent revenue, that's $50K/day, or roughly $18M/year of recoverable revenue from closing the recovery gap. Now layer the energy line: the worst SAG mill is running 11.5 kWh/ton against a 9 kWh/ton benchmark — at $25/MWh and ~25,000 tpd of feed, that's ~$570K/year of avoidable power cost per mill, and we have two in that band. Across the 20-unit flowsheet, the recovery and energy conversation is a $15-20M/year decision that comes out of one screen.*

> That's the decision this space automates. Not the slide. The decision. The capex slate and the ore-plan recommendation get built on recovery dollars and energy dollars — not on whichever metallurgist sent the latest memo.

### Question (Act 2.3)

> **Top 10 units by energy intensity (kWh/ton) — and how do they rank by processing stage?**

**What to say while it runs:** Top 10 units by energy intensity in kWh per ton, ranked by stage. SAG mills benchmark at 7-10 kWh/ton; ball mills 8-12; crushers 1-2. A unit running 30%+ above its stage benchmark is either undersized for the feed or running on the wrong ore-blend.

**What to look for:** Units ranked by avg_energy_per_ton with stage breakout. The high-intensity units against the SAG benchmark of 7-10 kWh/ton are the candidates for either control-loop tuning or feed re-blending.

**Land the point:** That ranked list turns into the ore-blend recommendation. Not 'we're using too much power' — 'we are shifting the harder ore-blend feed from SAG-3 to SAG-1 next quarter, and that buys us 8% on the energy line'.

---

## Act 3 — The commitment — locking the debottleneck capex and the mill-feed plan *(≈4 min)*

**Persona:** VP Reliability • **Job to be done:** Defend the debottleneck capex slate and the mill-feed plan to the CFO and the executive team, and lock the quarter's production guidance.

*The VP needs the same numbers the operators are acting on, framed so the capex case, the production guidance, and the ESG energy intensity story tell the same story.*

### Question (Act 3.1)

> **What is the plan adherence (actual vs. planned TPD) by processing stage for the last 90 days?**

**What to say while it runs:** Plan adherence — actual vs. planned TPD by stage for the last 90 days. Plan adherence below 95% on a critical-path stage is a production guidance risk for the quarter. This is the number the executive team wants to see before signing the production forecast.

**What to look for:** Per-stage actual TPD / planned TPD ratio. Stages running below 95% adherence are the candidates for the capex shortlist OR the production-guidance haircut conversation.

**Land the point:** When the VP can put plan adherence, bottleneck count, and recovery on one screen, the production-guidance call moves from a backroom negotiation to a defensible number with a unit-by-unit explanation behind it.

### Question (Act 3.2)

> **Which units had the most Off Spec quality readings in the last quarter, and what was their average concentrate grade?**

**What to say while it runs:** Units with the most Off Spec quality readings in the last quarter and their average concentrate grade. Off-Spec readings are the smelter-penalty leading indicator — sustained Off Spec is what triggers grade-discount clauses in concentrate offtake contracts.

**What to look for:** Units ranked by Off Spec reading count with avg concentrate grade alongside. The intersection of Off Spec frequency AND below-target grade is the unit that needs an upstream process intervention.

**Land the point:** Daily ops at 7 AM, debottleneck shortlist at 9, executive production guidance at 11. Same space. The Plant Lead's shift sheet and the VP Reliability's capex pitch are now the same artifact — and the production guidance, the capex slate, and the ore-blend recommendation all come out of one conversation instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — MineOps Central — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly average mill throughput (tph) by processing stage for the trailing 12 months.
2. Top 10 processing units by total unplanned downtime hours this quarter — which stage is driving it?
3. Which units are most frequently flagged as bottlenecks, and what is their average utilization?
4. How has plant recovery trended month-over-month by unit type across grinding and concentration?
5. Top 10 units by energy intensity (kWh/ton) — and how do they rank by processing stage?
6. What is the plan adherence (actual vs. planned TPD) by processing stage for the last 90 days?
7. Which units had the most Off Spec quality readings in the last quarter, and what was their average concentrate grade?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
