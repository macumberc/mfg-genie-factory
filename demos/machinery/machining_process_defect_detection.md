# PrecisionEdge Corp — Demo Script

**Space:** Machinery — PrecisionEdge Corp - Machining Defect Detection ⚙️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Manufacturing + Production Supervisor, Quality Engineer, CFO
**KPIs touched:** Defect rate, First-pass yield, Surface finish Ra, Tool flank wear, Scrap cost, Cost of Quality
**Big decision automated:** Which CNC machines get pulled off-line for ballscrew/spindle rebuild vs. kept running with tighter tool-change cadence, which raw-material supplier gets re-qualified, and how Cost-of-Quality stops eroding the plant's annual bonus.

---

## Pre-demo checklist

- Open the Genie space `PrecisionEdge Corp - Machining Defect Detection ⚙️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PrecisionEdge runs 20 CNC machines — 5-Axis CNCs, Lathes, Mills, Surface Grinders, Drills — split across five production cells (A through E) machining precision parts to a 1.6 micrometer Ra target. Today the Production Supervisor watches defect flags in the MES on the shop floor, the Quality Engineer reconciles tool-flank-wear measurements in a CMM log Excel, and the VP Manufacturing tracks scrap and rework cost out of a SAP cost-of-quality report a week after month-end. Three views, the same machines, and the line-shut-vs-release decision keeps getting made on the supervisor's gut because the wear data and the defect data live in different systems. This space ends that: one governed surface where defect rate, first-pass yield, flank wear, and Cost-of-Quality all resolve to the same machine and the same operation type — so the line shut/release call and the supplier qualification can be made in the same conversation.

---

## Key KPIs in scope

- Defect rate (%) — world-class machining target <1%, typical CNC shops 2–5%
- First-pass yield (%) — world-class ≥99%, leaders 95%+
- Surface finish Ra (μm) — target ≤1.6 μm for precision parts
- Tool flank wear (mm) — replace at 0.3 mm per ISO 3685
- Scrap cost ($) — typical 1–3% of cost of goods sold
- Cost of Quality (scrap + rework) — leaders <2% of revenue
- Cycle time per part (sec) — productivity and capacity indicator
- Tool changes per month — wear-program health and unplanned-stop driver

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **FPY** | First Pass Yield |
| **VP** | Vice President |

---

## Act 1 — The signal — which machines are leaking yield this month *(≈4 min)*

**Persona:** Production Supervisor • **Job to be done:** Identify which CNCs need to come down for inspection vs. stay running, before the shift-change handover.

*This is the call that decides which machine the night shift inherits with a problem and which one is clean. Two questions in, the Supervisor already knows where to send the maintenance tech.*

### Question (Act 1.1)

> **Top 10 machines by defect rate this month — which CNC models are underperforming?**

**What to say while it runs:** Top 10 machines by avg_defect_rate this month. World-class machining is below 1%; average CNC shops live in the 2-5% range. Anything above 5% is either tool wear running out of spec, a fixture issue, or — sometimes — a raw-material batch problem. The list tells the supervisor where to look first.

**What to look for:** Ranked machine_id with avg_defect_rate and machine_model. Watch for one or two 5-Axis CNCs or Surface Grinders showing up — those are the high-value parts where a defect rate spike is real margin lost.

**Land the point:** When the Supervisor can resolve this in 10 seconds instead of pulling the MES extract during morning standup, the line-shut decision happens at 7am, not at lunch. That's a half-shift of scrap avoided every time it's right.

### Question (Act 1.2)

> **Show monthly trend in Cost of Quality (scrap + rework) across the trailing 12 months.**

**What to say while it runs:** Monthly trend in total_scrap_cost + total_rework_cost — Cost of Quality. Leaders run COQ under 2% of revenue. The trend matters more than the level: a rising COQ line means the program is losing ground regardless of the absolute number.

**What to look for:** One line, 12 months. Watch for the inflection points; those are usually the months a new operator was added, a tool spec was changed, or a raw-material lot was swapped. Each inflection has a story.

**Land the point:** Before this space, COQ trend was a slide the VP Manufacturing rebuilt for the monthly ops review. Now it's the Supervisor's first chart of the shift — and the corrective-action conversation starts before the dollars get to the P&L.

---

## Act 2 — The decision — line shut/release call and the supplier qualification *(≈4 min)*

**Persona:** Quality Engineer • **Job to be done:** Lock the recommendation on which machines get pulled for rebuild, which tools get an immediate change-out, and which raw-material supplier earns the corrective-action notice.

*These three questions are where the operational call gets defended. Flank-wear vs the 0.3 mm ISO threshold tells you which tools come out now; FPY ranking tells you which machines have a structural issue; defect-type-by-machine ties it back to root cause.*

### Question (Act 2.1)

> **Which tools are at or past 0.3 mm flank wear and need immediate replacement?**

**What to say while it runs:** Tools at or past 0.3 mm flank_wear_mm — the ISO 3685 replacement threshold. Above 0.3 mm, surface finish degrades and dimensional accuracy collapses; the next part off that machine has a real chance of being scrap. This is the change-out list for the next maintenance window.

**What to look for:** A table of tool_id, machine_id, flank_wear_mm sorted DESC, filtered above 0.3 mm. The list should be small. If it's not, the wear-monitoring program is losing.

**Land the point:** That list used to be a Quality Engineer's CMM-log spreadsheet exercise. Now it's the input to the next tool-room run — which tools come off which machines, in what order. Tool-change cadence stops being a calendar event and becomes a wear-driven decision.

### Question (Act 2.2)

> **Rank machine models by average first-pass yield — which are below the 99% world-class target?**

**What to say while it runs:** Machine_models ranked by avg_first_pass_yield against the 99% world-class target. Below 95% is a structural problem — either the machine needs a spindle rebuild, the ballscrews are losing accuracy, or the operator population needs retraining. None of those are quick fixes.

**What to look for:** Ranked machine_model with avg_first_pass_yield. Watch for one family — say Surface Grinders — sitting 3-5 points below the others. That's the family that's about to drop a contract because the customer-acceptance rate is sliding.

**Land the point:** When the Quality Engineer can defend a $200-400K machine rebuild against the FPY gap times the contract value, the capex case writes itself. The 'do we shut the line' conversation becomes a one-page recommendation, not a steering committee.

> **Anchor moment.** Stop on the FPY ranking and the COQ trend. Pick a Surface Grinder running 94% FPY against the 99% target, with monthly scrap+rework cost averaging $18K — typical at this scale and machine class.

> *A 5-point FPY gap on a Surface Grinder running ~3,000 parts/month at an average part value of $150 is $22,500/month of avoided scrap — call it $250K annually on one machine. A spindle/ballscrew rebuild runs $200-400K — payback under 18 months on a single machine. Across the four Surface Grinders, lifting FPY from 94% to 98% is roughly $800K-1M of annual recoverable margin — and that's before the customer-credit costs of late shipments to spec. The supplier raw-material qualification work is the complement: if 30% of the dimensional OOT defects trace to a single material batch, re-qualifying or dropping that supplier eliminates another $100-200K of annual scrap.*

> That's the line shut/release decision and the supplier-corrective-action conversation in one number. The VP Manufacturing walks into the capex review with the Surface Grinder rebuild already justified, and procurement walks into the supplier QBR with the material-batch defect attribution already documented. Two decisions, one space, same dollars.

### Question (Act 2.3)

> **What is the monthly trend in average surface finish Ra by operation type?**

**What to say while it runs:** Defect_type cost impact across machines — which defect categories drive the most cost, and which machines produce them most. Surface Scratch and Tool Mark usually point to tool wear; Dimensional OOT usually points to thermal drift or ballscrew wear; Burr usually points to operator setup. Each diagnosis has a different fix and a different owner.

**What to look for:** Cross-tab of defect_type by machine_model with implicit cost. Watch for Dimensional OOT concentrating on one machine — that's the spindle-rebuild candidate. Watch for Tool Mark or Surface Scratch concentrating in one operation_type — that's a tool-grade or supplier-material issue.

**Land the point:** Defect categorization stops being a quality-engineering archaeology project and becomes a same-day root-cause diagnosis. Same machines, same tools, same techs — but now the corrective-action conversation has actual evidence.

---

## Act 3 — The commitment — locking next year's machine-rebuild capex and the COQ target *(≈4 min)*

**Persona:** VP Manufacturing • **Job to be done:** Defend the machine-rebuild capex and the COQ-reduction commitment to the CFO and the executive team.

*The VP Manufacturing walks into the FY plan defense with the same numbers the Quality Engineer is acting on, in the same conversation. That's the leave-behind.*

### Question (Act 3.1)

> **Top 10 machines by total scrap cost over the last quarter, and what was their defect rate?**

**What to say while it runs:** Top 10 machines by total_scrap_cost over the last quarter, with their avg_defect_rate alongside. The high-scrap-cost machines should be the high-defect-rate machines. If they're not, we have a high-value-part exposure on a machine that doesn't look bad on the surface — and that's the most dangerous quality gap.

**What to look for:** Ranked machine_id with total_scrap_cost and avg_defect_rate in the same row. Watch for a machine in the top 5 scrap-cost list that has a defect rate below 3% — that's a high-value-parts contamination story, and it needs immediate audit.

**Land the point:** When the VP Manufacturing can see scrap cost and defect rate together, the rebuild-vs-replace conversation becomes specific. The CFO sees the dollars, the supervisor sees the machines, and the rebuild capex case lands on facts instead of intuition.

### Question (Act 3.2)

> **Which defect types account for the most cost impact, and which machines produce them most often?**

**What to say while it runs:** Monthly trend in avg_surface_finish by operation_type. The 1.6 micrometer Ra target is the precision-machining contract spec for most aerospace and medical work. Anything trending up — surface getting rougher — is either a tool-wear or a coolant-program issue, and those have very different fixes.

**What to look for:** Five lines on one chart — Milling, Turning, Drilling, Grinding, Boring — over 12 months. Watch for Grinding or Turning trending past 1.6 — those are the operations where customer rejection rates spike fastest.

**Land the point:** Surface finish goes from a CMM-log artifact to a board-level KPI. When the VP Manufacturing can defend FPY recovery with the operation-level Ra trend as the leading indicator, the COQ-reduction commitment for FY27 stops being a goal and becomes a program with a measurable signal. One space, three personas, one number.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PrecisionEdge Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 machines by defect rate this month — which CNC models are underperforming?
2. Show monthly trend in Cost of Quality (scrap + rework) across the trailing 12 months.
3. Which tools are at or past 0.3 mm flank wear and need immediate replacement?
4. Rank machine models by average first-pass yield — which are below the 99% world-class target?
5. What is the monthly trend in average surface finish Ra by operation type?
6. Top 10 machines by total scrap cost over the last quarter, and what was their defect rate?
7. Which defect types account for the most cost impact, and which machines produce them most often?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
