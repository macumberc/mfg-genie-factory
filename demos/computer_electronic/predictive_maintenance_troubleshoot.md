# AssemblyGuard Systems — Demo Script

**Space:** Computer & Electronic — AssemblyGuard Systems - Predictive Maintenance 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** EMS Plant Manager + Maintenance Director, Maintenance Director, CFO partner
**KPIs touched:** MTBF, MTTR, Availability, Total downtime hours, Maintenance cost, Prediction accuracy
**Big decision automated:** Which 3-5 machines to replace vs. refurbish in the next capex cycle, which assembly line gets dedicated to which product family, and where to expand PdM coverage next.

---

## Pre-demo checklist

- Open the Genie space `AssemblyGuard Systems - Predictive Maintenance 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AssemblyGuard Systems runs SMT and electronics assembly lines for a contract-manufacturing book where unplanned downtime costs $50-200K an hour against committed customer SLAs. Today the bad-actor machine list lives on the Maintenance Director's whiteboard, the prediction-accuracy trend lives on a data-science PowerPoint nobody outside the team has seen, and the PdM program ROI lives in the CFO's investment-defense slide once a quarter. Three artifacts, same fleet — and the machine-replace-vs-refurbish call (a $200K-1M per-machine decision) and the line-to-product-family assignment get made in a Friday meeting where everyone is bringing different spreadsheets. This space ends that. One governed surface where MTBF, MTTR, availability, prediction accuracy, and maintenance cost land in the same conversation as the capex calendar and the production schedule.

---

## Key KPIs in scope

- MTBF (hours) — reliability KPI; PdM typically lifts MTBF 20-40%
- MTTR (hours) — repair speed; planned PdM repairs run 40-60% faster than emergency
- Availability (%) — uptime; world-class OEE availability 90%+
- Total downtime hours — direct capacity loss; 60% of SMT downtime is feeder/nozzle
- Maintenance cost ($) — PdM programs cut total maintenance cost 10-25%
- Prediction accuracy (%) — model quality; drives PdM coverage expansion
- Critical alert count — leading indicator for unplanned events
- Average anomaly score — fleet health pulse

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **EMS** | Electronic Manufacturing Services |
| **KPI** | Key Performance Indicator |
| **MTBF** | Mean Time Between Failures |
| **MTTR** | Mean Time To Repair |
| **OEE** | Overall Equipment Effectiveness |
| **ROI** | Return on Investment |

---

## Act 1 — The signal — finding the bad-actor machines and the lines that are dragging availability *(≈4 min)*

**Persona:** EMS Plant Manager • **Job to be done:** Pull tomorrow's intervention candidates and the lines that are quietly bleeding capacity — before customer SLAs do the talking.

*This is where the Friday capex meeting becomes a quantified replace-or-refurbish call. Two questions in, the plant manager has the bad-actor list that used to live in a maintenance technician's head.*

### Question (Act 1.1)

> **Show monthly MTBF and availability trend by machine type for the trailing 12 months.**

**What to say while it runs:** Monthly MTBF and availability trend by machine type over 12 months. World-class OEE availability is 90%+; MTBF on SMT placement equipment typically runs 200-400 hours between failures. A machine type whose MTBF is sliding while availability is flat means we're catching failures faster but they're happening more often — that's an aging-fleet signal, not a maintenance-process win.

**What to look for:** Two-line chart by machine_type: avg_mtbf_hours and avg_availability_pct over 12 months. Watch for the machine type where MTBF is falling but availability is held up — that's the fleet being kept alive by heroic maintenance and rising parts spend.

**Land the point:** Right there is the first replacement-vs-refurbish conversation. Aging machine types are the ones earning the next capex slot — and the plant manager just identified them in 8 seconds, not by which technician's email was loudest.

### Question (Act 1.2)

> **Which 10 machines have the highest total downtime hours and maintenance cost this year?**

**What to say while it runs:** Top 10 machines by total downtime hours and maintenance cost year-to-date. Sixty percent of SMT downtime is feeder and nozzle related — but the machines that show up on both rankings together (high downtime AND high cost) are the ones whose unit economics no longer work, regardless of root cause.

**What to look for:** Ranked table of machine_id by total_total_downtime_hours and total_maintenance_cost. Repeat names across both columns are the bad-actor short list — those are replace-or-refurbish decisions, not maintenance-process decisions.

**Land the point:** Before this space, that ranking was assembled by hand for every quarterly maintenance review. Now it's the plant manager's first question — and the capex shortlist starts on dollars, not on which machine the technicians complain about most.

---

## Act 2 — The decision — replace, refurbish, or accept; which line earns which product family *(≈4 min)*

**Persona:** Maintenance Director • **Job to be done:** Commit the capex shortlist — which machines move to replacement, which to overhaul, which to accept — and align line assignments to product-family criticality.

*Three questions that turn the bad-actor list into a defensible capex recommendation. The middle question is the anchor — the downtime-dollar math that converts the replacement decision from a maintenance ask into a finance-defensible payback.*

### Question (Act 2.1)

> **What share of corrective maintenance events were correctly predicted, by assembly line?**

**What to say while it runs:** Share of corrective maintenance events that were correctly predicted, by assembly line. PdM coverage is the leading indicator of program maturity — a line with prediction accuracy above 80% is one where we can plan against downtime; a line below 50% is one where we're still in reactive mode and SLA risk is real. This ranking is what decides where the next PdM model investment goes.

**What to look for:** Bar chart by assembly_line with the share of predicted vs corrective maintenance events. The lines on the right are PdM mature; the lines on the left are SLA exposure waiting to happen.

**Land the point:** That ranking is the conversation that moves PdM expansion from 'data science wishlist' to a line-by-line investment plan. Lines that aren't covered are the lines whose customer concessions and air-freight bills are eating their margin.

### Question (Act 2.2)

> **Top 10 failure modes by repair cost over the last quarter — and how many of them were predicted?**

**What to say while it runs:** Top 10 failure modes by repair cost over the last quarter — and how many of them were predicted. A failure mode that's expensive AND unpredicted is the one to chase next, in both the maintenance program and the PdM model retraining. Failure modes that are expensive AND predicted are already paying back the PdM investment.

**What to look for:** Ranked table of failure_mode by total_repair_cost with the share that was predicted alongside. The high-cost, low-predicted quadrant is where engineering time goes next.

**Land the point:** When the engineer, the director, and the CFO all see the same failure-mode ranking with the same prediction share, the PdM-expansion debate stops being a data-team pitch and starts being a maintenance-program decision. That's a different governance call.

> **Anchor moment.** Hold on the bad-actor machine list and the total downtime hours column. Pick the worst machine — call it 80 hours of unplanned downtime year-to-date and $180K in repair spend.

> *Eighty hours of unplanned downtime on an EMS line costs the business $50-200K per hour against committed customer SLAs — call it $100K/hour conservatively. That's $8M of contract-impact exposure on one machine before you add the $180K in repair spend. Replacement on a modern placement machine runs $400-800K; payback inside a single fiscal year on one machine alone. Across 5 bad-actor machines, the math says $25-40M of annual SLA exposure that the current fleet can't reliably serve — and that's the capex envelope the CFO can defend without breaking a sweat.*

> That's the decision this space automates. Not the deck — the decision. The replace-vs-refurbish call runs on downtime-dollar math against SLA exposure, not the loudest technician. The line-assignment call routes high-margin customers to the most-predicted lines, not the most-recently-serviced ones. The PdM-coverage roadmap is funded out of avoided downtime, not out of corporate IT slack.

### Question (Act 2.3)

> **How has prediction accuracy trended month-over-month across the fleet?**

**What to say while it runs:** Prediction accuracy month over month across the fleet. A rising trend means PdM is earning more autonomous decision-making rights; a stalled trend means the model is drifting and needs retraining before it gets blamed for the next missed call. This is the one chart that decides whether we lean into PdM coverage or hold the line.

**What to look for:** Monthly trend of total_prediction_accuracy_percent. Inflection points downward are retraining triggers; flat-high trends are signals to expand coverage to new machine types.

**Land the point:** That trend is the difference between a PdM program that's earning trust and one that's losing it. The first justifies the next expansion budget; the second triggers a model refresh before the next quarterly review.

---

## Act 3 — The commitment — locking the capex envelope and the PdM coverage roadmap *(≈4 min)*

**Persona:** CFO partner • **Job to be done:** Defend the capex and PdM-program investment to the executive committee and shape next year's fleet renewal budget.

*The CFO doesn't need another availability slide; they need the same MTBF, downtime, and prediction-accuracy numbers the maintenance director is using, in the same definitions, so the investment case writes itself.*

### Question (Act 3.1)

> **Which assembly lines have availability below 90%, and what is the projected maintenance cost to close the gap?**

**What to say while it runs:** Assembly lines with availability below 90% with projected maintenance cost to close the gap. This is the capex-prioritization view — which lines have a quantified renewal case, what it costs to fix them, and what the alternative is in terms of continued contract risk.

**What to look for:** Ranked table of assembly_line with availability below 90% and the projected maintenance_cost_usd to close the gap. The biggest gap with the lowest current availability is the line whose renewal case writes itself.

**Land the point:** That's the chart that defends the fleet-renewal envelope to the board. Same numbers as the maintenance director sees, same definitions — and the executive committee stops getting two different stories from operations and finance.

### Question (Act 3.2)

> **How many critical sensor alerts were raised by machine type over the last 30 days, and which machines are repeat offenders?**

**What to say while it runs:** Critical sensor alerts by machine type over the last 30 days with repeat-offender machines flagged. Repeat-offender machines are the ones whose next failure is no longer a surprise; the question isn't whether to act, it's whether to act before or after the next SLA miss.

**What to look for:** Ranked list of machine_type by critical_alert_count with the highest-frequency machine_id called out. The repeat offenders are the immediate-action list, not the quarterly review list.

**Land the point:** Daily triage at 8 AM, capex prioritization at 10, board defense at noon. Same space. Same numbers. The plant manager's bad-actor list and the CFO's fleet-renewal pitch are now the same artifact — and the executive committee gets one fleet story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AssemblyGuard Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly MTBF and availability trend by machine type for the trailing 12 months.
2. Which 10 machines have the highest total downtime hours and maintenance cost this year?
3. What share of corrective maintenance events were correctly predicted, by assembly line?
4. Top 10 failure modes by repair cost over the last quarter — and how many of them were predicted?
5. How has prediction accuracy trended month-over-month across the fleet?
6. Which assembly lines have availability below 90%, and what is the projected maintenance cost to close the gap?
7. How many critical sensor alerts were raised by machine type over the last 30 days, and which machines are repeat offenders?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
