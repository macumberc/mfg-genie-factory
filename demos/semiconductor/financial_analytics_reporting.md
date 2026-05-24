# SemiLedger Analytics — Demo Script

**Space:** Semiconductor — SemiLedger - Financial Analytics & Reporting 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Controller, alongside Finance Business Partners and Department Heads
**KPIs touched:** Gross margin %, Operating margin %, R&D intensity %, Capex intensity, Cost per wafer, Revenue per employee
**Big decision automated:** Which product family to double down R&D investment on vs. flag for EOL, which 3 cost centers absorb the next round of cost-takeout, and how to defend gross-margin trajectory in the next earnings call.

---

## Pre-demo checklist

- Open the Genie space `SemiLedger - Financial Analytics & Reporting 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> SemiLedger Analytics closes the books across 20 cost centers spanning Fab Operations, R&D Engineering, Sales & Marketing, Quality & Test, and Supply Chain. Today the GL transactions and CapEx lines live in Oracle EBS, the budget-vs-actual workbook lives in the FP&A weekly close folder, and the gross-margin and R&D-intensity KPIs sit in the CFO's monthly board deck. Three systems, one earnings cycle — and the last variance review missed a $40M CapEx overrun in Fab Operations until the quarterly forecast was already with the audit committee. Semi peer benchmarks (50-60% leading-edge GM, 15-25% R&D intensity, 25-35% capex intensity) drive every product-family investment decision, but today those numbers arrive after the decisions are made. This space ends that. One governed surface where the CFO, Controller, and Finance Business Partners see margin, variance, and intensity in the same conversation that sets the next-year operating plan.

---

## Key KPIs in scope

- Gross margin % — semiconductor industry leading-edge 50–60%, mature analog 40–50%
- Operating margin % — sustainable target 25–35% at scale
- R&D intensity % — R&D / revenue; semi industry 15–25%, advanced-logic leaders 20%+
- Capex intensity — direct-materials and equipment as % of revenue; foundries run 30–35%
- Cost per wafer (USD) — fully loaded; varies $3k (mature 200mm) to $20k+ (5nm 300mm)
- Revenue per employee (USD) — productivity benchmark; industry median ~$500k–$1M
- Budget variance % — absolute variance; >10% = Critical overrun
- Headcount by department — capacity planning input

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — where margin and variance are bleeding before the quarter closes *(≈4 min)*

**Persona:** Finance Business Partner • **Job to be done:** Surface the gross-margin trajectory and the critical budget overruns by cost center before the FP&A close lock, so the variance commentary writes itself instead of being reverse-engineered.

*This is where the close-meeting agenda actually starts. Two questions in, the FBP has the gross-margin story and the cost-center critical-overrun list ready for the CFO before the Friday close meeting.*

### Question (Act 1.1)

> **Show monthly total revenue, COGS, and OpEx for the trailing 12 months — what is the trajectory of gross margin?**

**What to say while it runs:** Trailing 12-month total_revenue_usd, total_cogs_usd, and total_opex_usd — the gross-margin shape in one chart. Semi leading-edge GM target is 50-60%; if the line is rolling under 45% the earnings narrative needs to change three weeks before the print.

**What to look for:** Monthly bars or lines, DATE_TRUNC('month', transaction_date) shape, with revenue, COGS, and OpEx side-by-side. The gross-margin trajectory comes out of the slope between revenue and COGS.

**Land the point:** Right there is the gross-margin story. Now the FBP can hand the CFO the earnings-prep skeleton in minutes — that's the board-narrative conversation that used to require a week of slide rebuilds.

### Question (Act 1.2)

> **Which 10 cost centers have the largest critical budget overruns this quarter?**

**What to say while it runs:** Top 10 cost_centers by critical_overrun_count this quarter. 'Critical Overrun' means absolute variance above 10% — that's not a forecasting noise band, that's a control issue. Fab Operations critical overruns are the ones that move the consolidated number.

**What to look for:** Ranked table from budget_variance_metrics with critical_overrun_count and total_variance_usd side-by-side. The dollar column is what separates noise from material exposure.

**Land the point:** Before this space, that list was the output of a manual Oracle EBS pull plus a budget workbook reconciliation. Now it's the first question of the FBP's day — and the cost-takeout conversation starts before the variance review, not after.

---

## Act 2 — The decision — which product families earn the next R&D dollar and which cost centers absorb the take-out *(≈4 min)*

**Persona:** Controller • **Job to be done:** Commit the next round of R&D investment and the cost-takeout actions in defensible language for the CFO and the audit committee.

*Three questions that turn the variance watchlist into a portfolio-investment recommendation. The middle question is the anchor — the R&D-intensity vs. semi benchmark conversation that converts spend signals into family-level investment policy.*

### Question (Act 2.1)

> **Rank departments by total CapEx spend in the trailing 12 months — where is investment concentrated?**

**What to say while it runs:** Total_capex_usd by department over 12 months — Fab Operations always leads in semis (foundry capex intensity 30-35%) but R&D Engineering capex is the leading indicator of next-cycle competitiveness. Where investment is concentrating tells us where the bet is being placed.

**What to look for:** Ranked department list from financial_transaction_metrics with total_capex_usd. Compare Fab Operations spend trajectory vs. R&D Engineering — the ratio is the strategic posture in one number.

**Land the point:** That list used to be a quarterly capex committee printout. Now it's the input to the next R&D investment commit the Controller is signing off on tomorrow.

### Question (Act 2.2)

> **How has the critical overrun count trended month-over-month by department?**

**What to say while it runs:** Average rd_intensity_pct by department against the 15-25% semi-industry benchmark. Advanced-logic leaders run 20%+; if a family is dropping below 15% while its competitive node is moving, that's not a savings, that's a slow EOL. If R&D intensity is above 25% and gross margin isn't responding, that's a capital-discipline problem.

**What to look for:** Per-department table from financial_kpi_monthly with rd_intensity_pct vs. the benchmark band shaded on the chart. Look for the families on either tail.

**Land the point:** When the CFO, the Controller, and the department head all query R&D intensity the same way and see the same number, the meeting stops being about whose ratio definition is correct and starts being which family gets the next $50M.

> **Anchor moment.** Stop on the R&D-intensity chart and the cost-center critical-overrun list on screen. Pick a Fab Operations cost center with total_variance_usd of $40M on the year and operating_margin_pct compressing 3 points below plan.

> *Sustainable semi operating margin at scale is 25-35%. A 3-point compression on a $2B revenue line is $60M of operating profit — and that $40M variance in Fab Operations is two-thirds of the gap right there. If we reauthorize $15M of cost-takeout (vendor consolidation, idle-tool retirement, OT reduction) at a 70% recovery rate, that's $10M back into operating margin. On the R&D side, the Application Processor family at 22% R&D intensity and 55% gross margin is where the next $30M goes — that's a 1.5-point GM accretion at production ramp, worth $30M annualized. The cost center at 28% R&D intensity but flat revenue is the EOL conversation — call that $20M of R&D reallocation.*

> That's the decision this space automates. Not the slide. The decision. R&D dollars reallocate to one family, EOL flag goes on another, three cost centers absorb the take-out — in one conversation, with the same numbers the audit committee will see.

### Question (Act 2.3)

> **Which departments have the highest R&D intensity, and how does that compare to the 15–25% semi-industry benchmark?**

**What to say while it runs:** Now critical_overrun_count trended monthly by department. A flat line is healthy; a climbing line is a control-environment issue the audit committee will ask about. Quality & Test trending up while Sales & Marketing stays flat tells a very specific operational story.

**What to look for:** Monthly trend of critical_overrun_count from budget_variance_metrics, by department. The departments inflecting upward are the ones that need a focused variance review, not a blanket cost-takeout.

**Land the point:** That comparison is the difference between knowing a department is over budget and knowing whether it's a one-time exception or a structural overrun. The first is a status report; the second is a cost-takeout authorization.

---

## Act 3 — The commitment — shaping next year's operating plan and the earnings narrative *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the operating plan to the board, lock in the family-level investment mix, and align the earnings-call narrative with the actual cost-takeout actions.

*The CFO doesn't need more close packs; they need the variance, margin, and intensity numbers in the same governed language as the FBP's morning view — so the board narrative and the line-of-business conversation are the same artifact.*

### Question (Act 3.1)

> **What is the trailing 12-month total OpEx by GL category, and which categories are growing fastest?**

**What to say while it runs:** Trailing 12-month total_opex_usd by gl_category, ranked by growth rate. Semi OpEx growth above revenue growth is the gross-margin compression we are about to print — categories like Sales & Marketing growing faster than revenue is a comp-design conversation, not a finance one.

**What to look for:** Ranked table of GL categories with growth rates side-by-side. The fastest-growing OpEx category against flat or declining revenue is the next earnings-call question we want to have an answer for.

**Land the point:** When this view is in the CFO's hand four weeks before the print, the earnings prep moves from defensive to programmatic — and the audit committee stops being told about variances after they happen.

### Question (Act 3.2)

> **Which cost centers have the largest negative budget variance percentage — where should the CFO focus on cost actions?**

**What to say while it runs:** Cost centers with the largest negative variance_pct year-to-date. Negative variance in semis is the early indicator of either pricing pressure or yield slip — and the cost centers that show it first are where the cost-action playbook needs to land.

**What to look for:** Bottom-ranked cost_centers from budget_variance_metrics by avg_variance_pct. The 3-5 worst names anchor the cost-action authorization the CFO is taking to the board.

**Land the point:** Triage at the FBP's standup, takeout decisions at the Controller's review, board narrative in the earnings prep. Same space. Same numbers. The variance watchlist and the CFO's board pitch are now the same artifact — and the audit committee gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — SemiLedger Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total revenue, COGS, and OpEx for the trailing 12 months — what is the trajectory of gross margin?
2. Which 10 cost centers have the largest critical budget overruns this quarter?
3. Rank departments by total CapEx spend in the trailing 12 months — where is investment concentrated?
4. How has the critical overrun count trended month-over-month by department?
5. Which departments have the highest R&D intensity, and how does that compare to the 15–25% semi-industry benchmark?
6. What is the trailing 12-month total OpEx by GL category, and which categories are growing fastest?
7. Which cost centers have the largest negative budget variance percentage — where should the CFO focus on cost actions?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
