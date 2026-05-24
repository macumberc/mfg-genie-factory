# PureChem Analytics — Demo Script

**Space:** Chemicals & Materials — PureChem Analytics - Quality Event Root Cause Analysis 🔍
**Runtime:** ~15 minutes • 7 questions
**Audience:** Quality Director + Plant Manager, Quality Director, CFO partner
**KPIs touched:** Critical event count, Total cost of quality, CAPA closure rate, Average resolution time, Batch pass rate / first-pass yield, Root-cause mix
**Big decision automated:** Which production line earns the next equipment-or-process capex, which root-cause category drives the next CAPA program, and which 3-5 products get a batch-release process change vs. accept the current pass-rate floor.

---

## Pre-demo checklist

- Open the Genie space `PureChem Analytics - Quality Event Root Cause Analysis 🔍`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PureChem Analytics runs 6 production lines making 20 chemicals — acids, bases, solvents, polymers, specialty — and is under standing pressure to drive cost-of-quality below the industry 5-10% of revenue band. Today the deviation-aging report lives in the Quality Director's CAPA spreadsheet, the root-cause Pareto lives in the Plant Manager's monthly review, and the COQ-as-percent-of-revenue lives in the CFO's margin deck. Three artifacts, same incidents — and the next $2-5M of quality-system capex (sensors, MES, CAPA tooling, line redesign) gets allocated by whichever director made the most persuasive case in the quarterly governance call. This space ends that. One governed surface where critical-event counts, COQ dollars, CAPA closure rates, and batch pass rates land in the same conversation as the capex calendar.

---

## Key KPIs in scope

- Critical event count — escalation and regulatory reporting trigger
- Total cost of quality ($) — direct margin impact; benchmark 5-10% of revenue
- CAPA closure rate (%) — target ≥ 90% closed-effective within 90 days
- Average resolution time (days) — target ≤ 30 days for major deviations
- Batch pass rate / first-pass yield (%) — target ≥ 95% on-spec
- Root-cause mix (Equipment / Process / Material / Human Error / Environmental) — capex vs. training priority signal
- Open / In-Progress event backlog — quality system health indicator
- Temperature deviation magnitude — process-stability leading indicator

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — separating chronic margin leakage from one-off bad batches *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Find the products and lines where cost of quality is structurally embedded — not just last month's incident.

*This is where the monthly quality review becomes a capex prioritization. Two questions in, the plant manager has the COQ-by-category picture the CFO normally sees only at quarter-end.*

### Question (Act 1.1)

> **Show monthly total cost of quality by product category for the trailing 12 months.**

**What to say while it runs:** Monthly total cost of quality by product category over 12 months — acids, bases, solvents, polymers, specialty. Industry COQ runs 5-10% of revenue in basic chemicals; if a category is climbing past that band, it's not noise, it's structural margin leakage and it needs a CAPA program, not a CAPA ticket.

**What to look for:** Monthly total_cost_of_quality_usd by product_category. Watch for the category whose trend is climbing while volume is flat — that's the one whose unit-cost-of-quality is silently eating the P&L.

**Land the point:** Right there is the conversation the CFO usually has alone with finance and now has with operations. The categories at the top of this trend are the ones earning a CAPA program, not just incident-by-incident response.

### Question (Act 1.2)

> **Top 10 products by cost of quality this year — and what is the dominant root cause?**

**What to say while it runs:** Top 10 products by cost of quality year-to-date, with the dominant root-cause category alongside — Equipment, Process, Material, Human Error, Environmental. The root-cause column is what decides whether the fix is capex (Equipment), continuous improvement (Process), supplier (Material), or training (Human Error). Each routes to a different budget.

**What to look for:** Ranked list with total_cost_of_quality_usd and the root_cause_category that dominates. The Equipment-driven rows are line-upgrade candidates; the Material-driven rows are supplier-de-qualification candidates.

**Land the point:** Before this space, that table got assembled by hand for every quarterly review. Now it's the plant manager's first question — and the capex-vs-training conversation starts with a defensible product list instead of the loudest incident.

---

## Act 2 — The decision — which root cause drives the next CAPA program and which line earns capex *(≈4 min)*

**Persona:** Quality Director • **Job to be done:** Commit the next quarter's CAPA program direction and the production-line capex shortlist — equipment fix, process redesign, or supplier change.

*Three questions that convert the COQ Pareto into a defensible budget recommendation. The middle question is the anchor — the line-by-line quality-event math that turns the capex debate into a payback calculation.*

### Question (Act 2.1)

> **How has critical event count trended month-over-month across production lines?**

**What to say while it runs:** Critical event count month over month across production lines. Critical-severity events are escalation triggers — for specialty chemicals, more than two criticals on the same line in a quarter is a regulatory-disclosure conversation and a near-certain insurance premium impact. A line drifting up here isn't an ops problem, it's an executive-attention problem.

**What to look for:** Monthly trend of critical_event_count by production_line. The lines whose critical count is climbing despite stable volume are the ones whose equipment or process control has structurally degraded.

**Land the point:** That chart is the difference between a quality-review status update and an executive-committee escalation. The lines at the top earn an immediate intervention, not a CAPA queue spot.

### Question (Act 2.2)

> **Which root cause categories have the highest open / in-progress event backlog?**

**What to say while it runs:** Root-cause categories ranked by open / in-progress event backlog. Equipment-heavy backlog means we're behind on PdM and there's a capex case; process-heavy means continuous-improvement is overloaded; material-heavy means the supplier panel needs to move. This single ranking decides which budget the next $1-3M goes against.

**What to look for:** Ranked table of root_cause_category by open_event_count. The top row is the budget category that gets the next governance vote.

**Land the point:** When the director, the plant manager, and the CFO all see the same root-cause ranking and the same backlog, the budget conversation stops being three meetings and starts being one prioritization. That's a structural change in how quality programs get funded.

> **Anchor moment.** Hold on the COQ-by-category chart and the production-line backlog ranking. Pick the worst line — call it $4M of trailing-12-month COQ, dominantly Equipment-driven, with a critical-event count climbing for two consecutive quarters.

> *Four million in COQ on one line, with equipment-driven root cause running 60% of incidents, means roughly $2.4M of annually-recurring margin leakage is addressable with an equipment intervention. A line-level capex retrofit on specialty chemical equipment runs $2-5M; payback under 24 months on the worst line alone. Across 6 production lines, the COQ Pareto identifies $5-8M of annually-recurring margin recovery — funded by a single-cycle capex envelope.*

> That's the decision this space automates. Not the deck — the decision. The next capex dollar moves from 'whoever sent the most-recent escalation email' to a quantified COQ-versus-payback ranking. The CAPA program direction stops being the director's hunch and becomes the root-cause backlog Pareto.

### Question (Act 2.3)

> **What is the average CAPA closure rate by product category over the last 6 months?**

**What to say while it runs:** Average CAPA closure rate by product category over 6 months. Target is 90%+ closed-effective within 90 days. A category whose closure rate is sliding below 70% has CAPA execution risk, not detection risk — the system is finding problems but the org isn't closing them. That's a process-redesign signal, not a tooling signal.

**What to look for:** Monthly trend of avg_capa_closure_rate_pct by product_category. The categories whose closure rates are diverging from target are the ones whose quality team is structurally under-resourced.

**Land the point:** That gap is what differentiates a quality-tooling investment from a quality-headcount investment. Both are capex; they go to different lines on the plan.

---

## Act 3 — The commitment — locking the quality capex envelope and the next-cycle COQ target *(≈4 min)*

**Persona:** CFO partner • **Job to be done:** Defend the quality budget to the executive committee and shape next year's quality-system investment envelope against the COQ-as-percent-of-revenue trajectory.

*The CFO doesn't need another COQ slide; they need the same line-level and category-level numbers the quality director is using, so the budget defense writes itself.*

### Question (Act 3.1)

> **Top 10 production lines by total quality events — and how do their batch pass rates compare?**

**What to say while it runs:** Top 10 production lines by total quality events with batch pass rate alongside. The lines with the most events and the lowest pass rate are the ones whose downstream working-capital impact is largest — held inventory, rework, scrap, customer concessions. This is the chart that ties operational quality to financial outcomes.

**What to look for:** Ranked table by total_quality_events with avg_batch_pass_rate side-by-side. The high-events, low-pass-rate quadrant is where the next capex memo gets defended.

**Land the point:** That's the conversation that converts the quality budget from a cost center into a margin-recovery story. Same numbers as the plant manager, same definitions — and the executive committee gets one story instead of three.

### Question (Act 3.2)

> **Which products have a batch pass rate below 90%, and what is the COQ dollar exposure?**

**What to say while it runs:** Products with batch pass rate below 90%, with the COQ dollar exposure attached. Target first-pass yield for specialty chemicals is 95%+; anything below 90% on a high-revenue product is a recurring write-down whose budget case writes itself.

**What to look for:** Filtered list of products with avg_batch_pass_rate below 90% and the trailing-12-month COQ. The biggest exposure is the product whose batch-release process change earns the next process-engineering hour.

**Land the point:** Triage at 8 AM, root-cause Pareto at 10, capex defense at noon. Same space. Same numbers. The plant manager's daily review and the CFO's quality-investment pitch are now the same artifact — and the executive committee stops getting two different numbers from two different decks.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PureChem Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total cost of quality by product category for the trailing 12 months.
2. Top 10 products by cost of quality this year — and what is the dominant root cause?
3. How has critical event count trended month-over-month across production lines?
4. Which root cause categories have the highest open / in-progress event backlog?
5. What is the average CAPA closure rate by product category over the last 6 months?
6. Top 10 production lines by total quality events — and how do their batch pass rates compare?
7. Which products have a batch pass rate below 90%, and what is the COQ dollar exposure?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
