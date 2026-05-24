# NucleoSafe Systems — Demo Script

**Space:** Power Generation — NucleoSafe Systems - Nuclear Safety & Compliance ☢️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Nuclear Operations + Reactor Engineer, Operations Manager, NRC Compliance Lead
**KPIs touched:** NRC compliance score, Safety margin, Total alarm count, Open corrective actions, Deficiency count per inspection, Forced outage rate
**Big decision automated:** Which safety systems get retrofitted ahead of the next NRC inspection, whether the upcoming outage is refueling-only or a refurb-scope, and whether each reactor unit earns a 20-year license-extension capex commitment.

---

## Pre-demo checklist

- Open the Genie space `NucleoSafe Systems - Nuclear Safety & Compliance ☢️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> NucleoSafe Systems operates 20 instrumented components across multi-unit reactor sites — fuel assemblies, control rods, primary and auxiliary coolant pumps, steam generators, and containment systems. Today the neutron-flux and coolant-flow readings live in the reactor control room's hourly logs, the compliance-score and deficiency trend lives in the NRC Compliance team's INPO performance binder, and the corrective-action backlog sits in a separate CAP system that nobody reconciles to the safety logs in real time. Three systems, same 20 components, three different versions of *which components are trending toward a Warning band* — and the outage-scope and license-extension capex decisions get shaped by whichever artifact the Operations Manager saw last week. This space ends that. One governed surface where compliance score, safety margin, alarm count, and corrective-action backlog reconcile so the inspection-prep conversation and the multi-billion-dollar license-extension AFE both come from the same numbers.

---

## Key KPIs in scope

- NRC compliance score — INPO benchmark; Index 1 plants score >95
- Safety margin (%) — distance to operating limit; >20% acceptable
- Total alarm count — safety-system event frequency
- Open corrective actions — backlog vs. NRC commitments
- Deficiency count per inspection — quality trend indicator
- Forced outage rate (nuclear) — target <2% (vs ~5% fleet thermal)
- Days since last inspection — surveillance interval compliance
- Component health distribution — Normal / Watch / Warning / Critical

---

## Act 1 — The signal — finding the components trending out of Normal before NRC walks the floor *(≈4 min)*

**Persona:** Reactor Engineer • **Job to be done:** Pull next week's targeted-walkdown list out of last week's safety-system data and name the components that are sliding toward a Warning band before the next surveillance window.

*This is the moment the pre-inspection prep stops being a months-long binder exercise and becomes a daily discipline. Two questions in, the Reactor Engineer has the compliance trajectory and the deficiency-leaders ranking — that's the spine of the inspection-readiness brief.*

### Question (Act 1.1)

> **Show monthly average NRC compliance score by reactor unit for the trailing 12 months.**

**What to say while it runs:** Monthly avg_compliance_score by reactor unit for the trailing 12 months is the INPO-style trajectory chart. Index 1 plants — the top quartile of the U.S. fleet — sit above 95. Anything sliding below 90 for sustained months is the slope that ends with an NRC inspection finding, not the score itself.

**What to look for:** Monthly trend of avg_compliance_score by reactor_unit with `DATE_TRUNC('month', inspection_date)`. The flat-or-rising units are clear; any unit showing a 3-6 month declining slope is the one the inspection-prep team has to brief at the next operating review.

**Land the point:** Now the Reactor Engineer can rank reactor units on compliance trajectory in seconds instead of cross-referencing INPO indicators and CAP-system exports — that's the *which unit is the inspection risk* conversation that used to require the NRC Compliance Lead to compile two binders first.

### Question (Act 1.2)

> **Top 10 components by total deficiencies found this year.**

**What to say while it runs:** Top 10 components by total_deficiencies this year is the recurring-finding list. Components — particularly steam generators, control rod drives, primary coolant pumps — accumulating deficiencies year over year are the candidates for either a corrective-action program escalation or a refurb-scope decision at the next outage.

**What to look for:** Ranked table — component_name, component_type, total_deficiencies. The recurrence pattern matters; a steam generator with five deficiencies across two quarters is a different conversation than one with five in a single inspection cycle.

**Land the point:** Right there is the refurb-scope shortlist. Before this space, that list was the output of three Compliance analysts cross-referencing the CAP system against the surveillance log. Now it's the input to the *which components earn outage capex* conversation — and that conversation happens on numbers that reconcile to the NRC filing.

---

## Act 2 — The decision — refueling-only, refurb-scope, or safety-system retrofit *(≈4 min)*

**Persona:** Operations Manager • **Job to be done:** Decide whether next year's outage is refueling-only or carries a multi-system refurb scope, and commit to which safety systems get retrofitted ahead of the NRC inspection cycle.

*Three questions that turn the deficiency picture into the outage-scope commitment. The middle question is the anchor — the safety-margin-to-outage-days conversion that decides whether the operations team accepts $20M of additional outage cost to avoid $200M of regulatory exposure.*

### Question (Act 2.1)

> **Which component types had the most failed inspections this year, and how many corrective actions remain open?**

**What to say while it runs:** Component types with the most failed inspections paired with corrective_actions_open count is the *root-cause-versus-recurrence* view. A component type with high failures *and* a long open-action tail is a systemic issue — that's a refurb-scope decision, not a maintenance ticket. A component type with high failures and a clean backlog is being well-managed, and the next inspection won't escalate.

**What to look for:** A short table — component_type, fail_count, total_open_corrective_actions. The combination is the story; steam generators with 10 failures and 30 open actions is the conversation the NRC will want, and the one Operations needs an answer to before the inspection-prep meeting.

**Land the point:** That artifact used to take a Compliance analyst three days of reconciling the surveillance log against the CAP backlog. Now it's the *what scope goes into next outage's AFE* answer — and the call between a $50M refueling outage and a $300M refurb outage gets made on data, not on the Senior Reactor Engineer's recollection.

### Question (Act 2.2)

> **How has total safety alarm count trended month-over-month by component type?**

**What to say while it runs:** Components in Warning or Critical health_status with their avg_safety_margin alongside is the proximity-to-limit view. Safety margin above 20% is comfortable; under 10% is the threshold where the NRC starts asking about operating limits in the next inspection. The combination of bad health and thin margin is the system that has to come out of service for retrofit before the inspection window.

**What to look for:** Components filtered to Warning + Critical health_status with avg_safety_margin per component. Components clustered under 15% margin are the must-do retrofit list; components in Warning but with 25%+ margin are watch-and-wait.

**Land the point:** When this list is in the Operations Manager's hand a quarter before the outage window, the retrofit decisions get made with engineering and procurement lead time — and the *which systems earn the limited outage clock* conversation stops being a war room and starts being a planned commitment.

> **Anchor moment.** Stop on the Warning-and-Critical component list and the safety-margin column on screen. Pick the worst cluster — call it three steam generators across two reactor units with safety margin under 12% and a combined corrective-action backlog of 40+ items.

> *A refueling-only outage runs roughly 25-30 days at $1-2M of lost margin per day — call it $40M of lost generation revenue. Adding a steam-generator retrofit scope extends that outage another 15-25 days at the same daily rate — another $20-40M of lost margin. Net additional cost: $20-40M. The downside scenario is an NRC inspection finding on those three steam generators triggering an emergency derate or a forced unplanned outage — call it $50-100M of lost margin plus regulatory exposure that compounds into the next license-renewal review. Across NucleoSafe's three reactor units, the math is clear: pre-emptive scope adds $20-40M of planned outage; deferred scope risks $200M+ of unplanned outage plus a Yellow finding in the next inspection cycle.*

> That's the decision this space automates. Not the slide. The decision. The outage AFE gets sized from real safety-margin and deficiency-trend data, not from the senior engineer's recollection of the last refurb cycle — and the inspection-prep package and the AFE narrative land in the same artifact.

### Question (Act 2.3)

> **Which components currently sit in Warning or Critical health status, and what is their average safety margin?**

**What to say while it runs:** Monthly trend in total_alarm_count by component_type is the leading indicator on equipment health. Alarm counts climbing month over month, particularly on coolant pumps or steam generators, point to a degradation that hasn't surfaced as a deficiency yet — that's the *find it before the inspector does* signal.

**What to look for:** Monthly bars of total_alarm_count broken out by component_type with `DATE_TRUNC('month', reading_date)`. The slope, not the level, is what matters; a steam generator trending up across two quarters is a refurb conversation, even if every individual alarm closed clean.

**Land the point:** That alarm trajectory used to surface in the quarterly engineering review. Now the Reactor Engineer and the Operations Manager see it the same morning — and the *do we pre-inspect this component before NRC arrives* call has time to actually happen.

---

## Act 3 — The commitment — license-extension AFE and the long-cycle compliance defense *(≈4 min)*

**Persona:** NRC Compliance Lead • **Job to be done:** Defend the fleet's compliance trajectory upstream to the NRC and the board, and recommend which reactor units earn a 20-year license-extension capex commitment versus an early-retirement study.

*The NRC Compliance Lead doesn't need more dashboards; the lead needs the same numbers the Operations team is acting on so the NRC submittal and the board's license-extension recommendation both reconcile to the operating record.*

### Question (Act 3.1)

> **Top 10 components by days since last inspection — are any past the 90-day surveillance window?**

**What to say while it runs:** Top 10 components by days_since_last_inspection with a 90-day surveillance threshold is the *are we current* view. The surveillance window is a hard NRC commitment; missing a window is an automatic finding, not a discussion. The cluster of components approaching the window is the inspection-schedule binding constraint for next quarter.

**What to look for:** Ranked table of days_since_last_inspection by component_name with the 90-day mark flagged. Any component past 90 is a current finding; the cluster sitting at 70-85 is the *what gets walked next week* list that has to be locked in.

**Land the point:** When this list is on the NRC Compliance Lead's screen in the same space the Reactor Engineer uses, the surveillance schedule gets defended to the inspector with one artifact — and the *did we meet our commitments* conversation becomes a one-line confirmation instead of a multi-day binder pull.

### Question (Act 3.2)

> **What is the monthly trend in average safety margin percentage across the reactor fleet?**

**What to say while it runs:** Monthly trend in avg_safety_margin across the reactor fleet is the long-cycle license-extension story. A flat-or-rising fleet margin is the technical foundation for the 20-year extension submittal; a declining slope across multiple years is the conversation about whether one of these units is an early-retirement candidate instead. That's an $8-15B capex call.

**What to look for:** Monthly fleet-wide avg_safety_margin across 24+ months. The slope across years is the regulatory and capital story; the variance across units is the *which reactor earns the next license* call.

**Land the point:** Triage in the morning surveillance walk, license-extension submittal at the next NRC submittal cycle. Same space, same numbers. The Reactor Engineer's component watchlist and the Compliance Lead's license-renewal defense are now the *same artifact* — and the NRC, the board, and the rating agencies all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — NucleoSafe Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly average NRC compliance score by reactor unit for the trailing 12 months.
2. Top 10 components by total deficiencies found this year.
3. Which component types had the most failed inspections this year, and how many corrective actions remain open?
4. How has total safety alarm count trended month-over-month by component type?
5. Which components currently sit in Warning or Critical health status, and what is their average safety margin?
6. Top 10 components by days since last inspection — are any past the 90-day surveillance window?
7. What is the monthly trend in average safety margin percentage across the reactor fleet?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
