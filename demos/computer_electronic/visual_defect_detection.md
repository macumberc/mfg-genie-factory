# VisionTech Electronics — Demo Script

**Space:** Computer & Electronic — VisionTech Electronics - Visual Defect Detection 🔬
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Manufacturing + Plant Quality Engineer, VP Quality, VP Manufacturing
**KPIs touched:** Defect rate, Actual pass rate, Classification accuracy, False positive / false negative counts, Scrap cost, Rework cost
**Big decision automated:** Which 2-3 inspection stations get the next 3D AOI upgrade, which defect signatures earn engineering escalation, and which product lines get a vision-model retraining run before the next ramp.

---

## Pre-demo checklist

- Open the Genie space `VisionTech Electronics - Visual Defect Detection 🔬`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> VisionTech Electronics runs AOI/SPI inspection across multiple PCBA product lines feeding both flagship consumer and high-mix industrial customers. Today the defect Pareto lives on the Plant Quality Engineer's whiteboard, the model-accuracy and false-call drag live in a vision-team JIRA dashboard, and the scrap-plus-rework cost lives in the VP Manufacturing's monthly variance report. Three artifacts, same boards — and the decision to upgrade an inspection station to 3D AOI ($300-800K per station) or escalate a defect signature to design engineering gets made by whoever's spreadsheet was most recent. This space ends that. One governed surface where defect PPM, pass rate, classification accuracy, false-positive drag, and scrap/rework dollars land in the same conversation as the capex plan and the model retraining calendar.

---

## Key KPIs in scope

- Defect rate (PPM) — world-class AOI targets <100 PPM escape, <2000 PPM false-fail
- Actual pass rate (%) — first-pass yield; gap-to-target drives capacity loss
- Classification accuracy (%) — vision model precision, retraining trigger
- False positive / false negative counts — operator drag and escape risk
- Scrap cost ($) — non-recoverable cost of quality
- Rework cost ($) — recoverable cost of quality, labour-intensive
- Average inspection confidence — model certainty, retraining signal
- Forecast defect rate (PPM) — forward-looking quality risk

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **PPM** | Parts Per Million (defect rate) |
| **VP** | Vice President |

---

## Act 1 — The signal — separating real escapes from false-call drag *(≈4 min)*

**Persona:** Plant Quality Engineer • **Job to be done:** Pull tomorrow's escalation list — which product lines are missing pass-rate targets, and which are losing throughput to false fails.

*This is where the morning quality huddle becomes a quantified upgrade-and-retrain conversation. Two questions in, the engineer has the line-level picture that used to require a half-hour of merging dashboards.*

### Question (Act 1.1)

> **Show monthly defect PPM and actual pass rate by product line for the trailing 12 months.**

**What to say while it runs:** Monthly defect PPM and actual pass rate by product line over 12 months. World-class AOI targets are below 100 PPM escape and below 2,000 PPM false-fail. A line whose defect PPM is climbing while pass rate is flat means the line is catching more but yielding the same — that's a process-drift signal, not an inspection improvement.

**What to look for:** Two-line chart per product_line: avg_defect_rate_ppm and avg_actual_pass_rate. Watch for lines where PPM is rising — those are the ones whose root cause sits upstream of the inspection station, not at it.

**Land the point:** Right there is the first escalation conversation. Lines whose PPM is climbing get a process-engineering deep dive; lines whose pass rate is degrading get the vision-model retraining slot. Two different actions, both decided in 8 seconds.

### Question (Act 1.2)

> **Which 10 product lines have the highest combined scrap and rework cost this year?**

**What to say while it runs:** Top 10 product lines by combined scrap and rework cost year-to-date. Scrap is non-recoverable cost of quality; rework is recoverable but labor-intensive. Lines at the top of both columns are the ones whose unit economics are quietly bleeding — and they're the obvious shortlist for the next inspection-station capex.

**What to look for:** Ranked table of product_line by total_scrap_cost plus total_rework_cost. The repeat names across both columns are the lines whose station-upgrade case writes itself.

**Land the point:** Before this space, that table got assembled by hand for the variance review. Now it's the engineer's first question — and the capex shortlist starts on cost-of-quality dollars, not on which product line shipped a recall last quarter.

---

## Act 2 — The decision — which stations get the 3D AOI upgrade and which defects escalate to engineering *(≈4 min)*

**Persona:** VP Quality • **Job to be done:** Commit the next capex round — which inspection stations get upgraded — and decide which defect signatures need to escalate to design engineering for an upstream fix.

*Three questions that turn the line-level pain into a defensible capex and engineering-escalation recommendation. The middle question is the anchor — the scrap-plus-rework math that converts the inspection-station upgrade from an ops ask into a margin-recovery case.*

### Question (Act 2.1)

> **How has classification accuracy trended month-over-month across vision model versions?**

**What to say while it runs:** Classification accuracy month over month across vision model versions. A new model rollout should show a step-up in accuracy; a drift downward without a deployment means the underlying defect mix is shifting and the model is stale. Either way, the trajectory of this line is the trigger for the next retraining run.

**What to look for:** Monthly trend of avg_classification_accuracy_pct broken out by model_version. The version whose accuracy is sliding fastest is the one that needs retraining before the next product ramp.

**Land the point:** That chart is the difference between a model that's earning automation rights and one that's quietly accumulating false-call cost. The lines using the worst-performing model are the immediate retraining priorities.

### Question (Act 2.2)

> **Top 10 product lines by false positive count this quarter — what's the operator-hour drag?**

**What to say while it runs:** Top 10 product lines by false positive count this quarter, with operator-hour drag attached. False positives don't damage product — they damage throughput. Each false fail is roughly 2-5 minutes of operator review time, and on a high-volume line that's a meaningful capacity hit that nobody books to a line item.

**What to look for:** Ranked table of product_line by false_positive_count with an operator-hour estimate alongside. The high-false-positive lines are the ones where vision-model precision is hurting yield even when defect detection looks fine.

**Land the point:** When the engineer, the VP, and the CFO all see the same false-call drag in the same units, the model-retraining conversation stops being a data-team ask and starts being a throughput recovery case. That's a different prioritization meeting.

> **Anchor moment.** Hold on the scrap-plus-rework ranking and the false-positive drag column. Pick the worst product line — call it $1.2M of scrap, $800K of rework, and 40,000 false-positive inspections costing roughly 3 minutes of operator time each.

> *Two million in cost of quality on one product line is the visible bleeding. Layer the false-positive drag: 40,000 false fails times 3 minutes is 2,000 operator-hours of lost throughput annually — at fully-loaded $80/hour that's another $160K of capacity recovery. And on a flagship product, every yield point recovered is worth $10-50M of annual revenue against high-margin contracts. A 3D AOI station upgrade runs $300-800K with proven yield gains of 1-3 percentage points; payback inside 12 months on the worst line alone. Across 2-3 stations, the upgrade case justifies $5-15M of recovered revenue plus $3-5M of avoided scrap and rework.*

> That's the decision this space automates. Not the slide — the decision. Station upgrades run on yield-recovery math, not on whose plant manager attended last week's escalation call. Model retraining gets prioritized on false-call drag dollars. Defect signatures earn engineering escalation on forecast PPM, not on the most-recent customer complaint.

### Question (Act 2.3)

> **Which product lines are forecast to miss their target pass rate in the next two months, and what's the projected PPM gap?**

**What to say while it runs:** Product lines forecast to miss target pass rate in the next two months, with projected PPM gap. This is the forward-looking view — the lines whose current trajectory says they'll be below committed yield two months from now, while there's still time to retrain the model or escalate the defect upstream.

**What to look for:** Filtered list of product_line where forecast_defect_rate_ppm exceeds target_pass_rate_pct threshold, with the projected gap. The biggest gap with the highest revenue volume is the line whose next ramp is at risk.

**Land the point:** That forward view is the difference between reactive quality and proactive yield management. The first triggers a recall response; the second triggers a model retraining and a station upgrade before the customer notices.

---

## Act 3 — The commitment — locking the inspection capex envelope and the vision-model roadmap *(≈4 min)*

**Persona:** VP Manufacturing • **Job to be done:** Defend the inspection capex envelope to the executive committee and shape the next 12 months of vision-model investment and product-line escalation priorities.

*The VP Manufacturing doesn't need another defect Pareto; they need the same scrap, rework, false-call, and forecast-PPM numbers the quality engineer and VP Quality are using, in the same definitions, so the capex case is one artifact.*

### Question (Act 3.1)

> **What is the total cost of quality (scrap + rework) by product line, and how does it split between recoverable and non-recoverable?**

**What to say while it runs:** Total cost of quality by product line split into recoverable rework and non-recoverable scrap. The recoverable-vs-non-recoverable split is the conversation finance cares about — recoverable cost is a process-improvement target; non-recoverable scrap is the one that justifies inspection-station capex.

**What to look for:** Stacked bar chart by product_line: total_rework_cost on top of total_scrap_cost. The lines with the largest non-recoverable stack are the inspection-capex priorities; lines with mostly recoverable cost are process-engineering targets.

**Land the point:** That's the chart that defends a multi-million-dollar inspection investment to the board. Same numbers as the engineer sees, same definitions — and the executive committee gets one cost-of-quality story instead of three.

### Question (Act 3.2)

> **Which defect types account for the most critical-severity escapes over the last 90 days?**

**What to say while it runs:** Defect types accounting for the most critical-severity escapes over the last 90 days. Critical escapes are the ones that reach customers — every one is a warranty exposure and a brand-reputation event. The defect types on this list are the ones earning the next design-engineering escalation and the next 3D AOI capability requirement.

**What to look for:** Ranked table of defect_type by count of critical-severity escapes. The top of the list is the design-engineering escalation queue, not just an inspection-station problem.

**Land the point:** Daily quality triage at 8 AM, capex shortlist at 10, board defense at noon. Same space. Same numbers. The engineer's escalation list and the VP's capex pitch are now the same artifact — and the executive committee gets one inspection story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — VisionTech Electronics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly defect PPM and actual pass rate by product line for the trailing 12 months.
2. Which 10 product lines have the highest combined scrap and rework cost this year?
3. How has classification accuracy trended month-over-month across vision model versions?
4. Top 10 product lines by false positive count this quarter — what's the operator-hour drag?
5. Which product lines are forecast to miss their target pass rate in the next two months, and what's the projected PPM gap?
6. What is the total cost of quality (scrap + rework) by product line, and how does it split between recoverable and non-recoverable?
7. Which defect types account for the most critical-severity escapes over the last 90 days?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
