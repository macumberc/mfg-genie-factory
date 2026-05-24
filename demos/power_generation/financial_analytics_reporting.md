# PowerLedger Corp — Demo Script

**Space:** Power Generation — PowerLedger Corp - Financial Analytics & Reporting 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + FP&A leads, Treasury / Capex governance, Department Heads
**KPIs touched:** Total revenue, Actual vs. budget variance, Operating margin, YTD spend pacing vs. annual budget, CapEx committed, Budget status distribution
**Big decision automated:** Which generation portfolio segment — thermal, hydro, wind, or solar — earns next cycle's capex dollars, and which cost centers get put on a forced reforecast before the board reviews the budget.

---

## Pre-demo checklist

- Open the Genie space `PowerLedger Corp - Financial Analytics & Reporting 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PowerLedger Corp runs 20 cost centers across four operating regions and four corporate departments — generation ops, maintenance, fuel procurement, and capital projects. Today the revenue number lives in the FP&A close pack, the YTD spend pacing in a Treasury workbook tracking the $1-3M capex commitments line-by-line, and the operating-margin defense in the CFO's board deck. Three artifacts, three teams, three different ways to roll up the same 20 cost centers — and the reforecast call that decides whether Renewable Expansion or Plant Upgrades earns next year's capital gets made on whichever workbook was last refreshed. This space ends that. One governed surface where revenue, variance, CapEx committed, and budget-status flag all reconcile so the recapitalization conversation happens on the same numbers the audit committee will see.

---

## Key KPIs in scope

- Total revenue (USD) — top-line by department and quarter
- Actual vs. budget variance ($, %) — favorable/unfavorable flag
- Operating margin (%) — utility-sector benchmark ~12-18%
- YTD spend pacing vs. annual budget — burn-rate indicator
- CapEx committed (USD) — capital governance metric
- Budget status distribution — On Track / At Risk / Over Budget
- Cost per MWh (derived) — fleet-wide efficiency view
- Approval status backlog — Pending vs Approved transaction count

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — finding the revenue lines and the over-budget cost centers before the close *(≈4 min)*

**Persona:** FP&A Lead • **Job to be done:** Surface the revenue trajectory and the cost centers eating into operating margin so the reforecast call has a starting line — not just a feeling.

*This is where the close conversation stops being a stitching exercise and starts being a triage. Two questions in, the FP&A lead has the revenue trend and the names of the cost centers that are dragging the variance line.*

### Question (Act 1.1)

> **Show monthly total revenue USD by department for the trailing 12 months.**

**What to say while it runs:** Trailing-12 revenue by department is the chart every monthly close opens with — Generation Ops carries the top line, Capital Projects carries nothing yet but commits the most capex. Notice whether the Operations bars are flat or climbing — that's the leading indicator on operating margin, and utility benchmark is 12-18%.

**What to look for:** Monthly bars of total_revenue broken out by department over 12 months — `DATE_TRUNC('month', record_date)` shape. Watch the Operations regions; if Northeast or Midwest is flat while Southeast climbs, the fleet mix story writes itself.

**Land the point:** Now the FP&A lead can rank departments on revenue trajectory in seconds instead of rebuilding the pivot every Friday — that's the *which segments are funding the operating margin* conversation that used to require the controllers to align on the close pack first.

### Question (Act 1.2)

> **Top 10 cost centers by total variance USD year-to-date — which are most over budget?**

**What to say while it runs:** Top 10 cost centers by total_variance USD year-to-date is the over-budget watchlist. Anything past 10% adverse variance trips the FP&A reforecast rule — those are the cost centers that get a forced rebudget before quarter-end, not after.

**What to look for:** A ranked table — cost center, department, total_variance_usd, variance_pct. The point isn't the top of the list; it's the cluster of Capital Projects names that signals a capex slippage problem vs. a fuel-cost problem.

**Land the point:** Right there is the reforecast list. Before this space, that artifact was the output of three Treasury analysts pulling cost-center extracts by department. Now it's the input to the CFO's pre-board call — and that call happens on numbers everyone in the meeting already saw.

---

## Act 2 — The decision — defending the operating margin and locking the reforecast *(≈4 min)*

**Persona:** Department Head • **Job to be done:** Defend their own department's variance to the CFO and commit to which cost centers get a forced reforecast vs. which get a budget reallocation from a sibling line.

*Three questions that turn the variance watchlist into a defensible capital-recovery recommendation. The middle question is the anchor — the operating-margin trajectory that decides whether the fleet defends the 15% guide or revises it.*

### Question (Act 2.1)

> **Which departments are flagged Over Budget or At Risk this quarter, and by how much?**

**What to say while it runs:** Over Budget and At Risk are the two budget-status flags that trigger a Department Head briefing. Anything sitting in those buckets this quarter is a defended-line conversation — either the department has a recovery plan, or the line gets moved to a reforecast.

**What to look for:** A short table — department, budget_status, total_variance_usd. The story is in which departments cluster in Over Budget: if Fuel is there, it's a hedge-book call; if Capital Projects is there, it's a slippage call; the two get very different treatments.

**Land the point:** That distribution used to be a slide the CFO assembled at 11 PM the night before the budget meeting. Now it's the first question the Department Head answers in real time — and the recovery commitment moves from defensive narrative to specific cost-center action.

### Question (Act 2.2)

> **How has fleet average operating margin trended month-over-month?**

**What to say while it runs:** Average operating margin month over month — utility-sector benchmark sits at 12-18%, and falling below the floor is the single number that prompts an analyst downgrade. The slope matters more than the level; a flat line above 12 is fine, a declining line *anywhere* needs an explanation before the earnings call.

**What to look for:** Monthly trend of avg_operating_margin against the 12% floor. The inflection points — particularly Q3 if Fuel is squeezing — are the ones the Treasury team will get asked about by the rating agencies.

**Land the point:** When the margin slope is in the Department Head's hand at the start of the month instead of the analyst's hand at the end of the quarter, the recovery action gets taken in time to matter — and the *operating margin defense* conversation moves out of the boardroom and into the cost-center owner's calendar.

> **Anchor moment.** Stop on the operating-margin trend and the over-budget cost-center list on screen. Pick the worst department — call it Capital Projects, total_variance_usd of $2-3M unfavorable across Renewable Expansion and Battery Storage Projects, two of the top-3 capex-committed lines.

> *Renewable Expansion and Battery Storage hold roughly $25-30M of committed CapEx between them, with $2-3M of YTD variance against the annual budget. At a 15% operating-margin guide, a $3M variance compounds to roughly $20M of revenue exposure to recover next year — or roughly 100 basis points of fleet operating margin if it goes unhedged. Across the four Capital Projects cost centers at PowerLedger's scale, that's the difference between defending the 15% guide to the analysts and revising it down to 13% on the next earnings call.*

> That's the decision this space automates. Not the slide. The decision. The CapEx reforecast gets written from a defended margin position, not a defensive one — and the Battery Storage commitment either earns a deeper allocation or moves to next cycle with a documented variance trail.

### Question (Act 2.3)

> **Which fiscal quarter had the largest budget variance, and what drove it by department?**

**What to say while it runs:** The fiscal_quarter rollup with department breakdown is the variance attribution view. Q3 typically owns the fleet's worst variance — summer gas burn, peak-load maintenance. Knowing whether Q3's gap was Fuel-driven or Maintenance-driven is the difference between a hedge conversation and a capex conversation.

**What to look for:** Quarter-over-quarter total_variance_usd broken out by department. Look for the quarter where Fuel and Maintenance variance both spike together — that's the operating-stress quarter the next budget cycle has to plan for.

**Land the point:** That attribution used to take the FP&A team three days of reconciling cost-center extracts. Now it's the answer the Department Head walks into the budget defense already holding — and the *which quarter shaped the reforecast* call is no longer a postmortem; it's a planning input.

---

## Act 3 — The commitment — shaping next year's CapEx mix and the hedge-book defense *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the operating-margin guide upstream to the board and lock in which segments — thermal, renewable expansion, grid modernization, storage — earn the next dollar of capital.

*The CFO doesn't need more dashboards; the CFO needs the same numbers the Department Heads just committed to, in the same language, so the board narrative writes itself from the FP&A workpapers.*

### Question (Act 3.1)

> **Top 10 cost centers by CapEx committed USD this year — and how much remaining budget do they hold?**

**What to say while it runs:** Top 10 cost centers by CapEx committed USD year-to-date, with remaining-budget alongside, is the capital-deployment map. The pairing matters — high commit + thin remaining means the project is nearly fully funded; high commit + fat remaining means a slippage flag the audit committee will ask about.

**What to look for:** Ranked table of total_capex_committed paired with total_remaining_budget by cost center. Renewable Expansion, Grid Modernization, Plant Upgrades, Battery Storage Projects are the four to watch — that's where the next $20-40M of fleet capex decisions cluster.

**Land the point:** When this artifact ships from the same space the FP&A lead used yesterday, the CFO walks into the board CapEx conversation defending one number, not three — and the *which segments earn capital next* call becomes a programmatic recommendation instead of a competitive scramble between department heads.

### Question (Act 3.2)

> **What is the monthly trend in YTD spend versus annual budget pacing across all departments?**

**What to say while it runs:** YTD spend versus annual budget pacing by department is the burn-rate story. Departments tracking flat to budget at the H1 mark have headroom; departments at 60%+ utilization by July are either over-running or pulling forward — both are conversations the CFO needs to lead before the analysts start asking.

**What to look for:** Monthly trend of total_ytd_spend rising against total_annual_budget by department. The inflection points show which departments will hit 100% before December — that's the reallocation list, and the recapitalization narrative builds from it.

**Land the point:** Triage in the close meeting at the start of the month, capital allocation in the board pack at the end. Same space, same numbers. The Department Head's variance defense and the CFO's CapEx commitment are now the *same artifact* — and the rating agencies, the audit committee, and the analyst desk all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PowerLedger Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total revenue USD by department for the trailing 12 months.
2. Top 10 cost centers by total variance USD year-to-date — which are most over budget?
3. Which departments are flagged Over Budget or At Risk this quarter, and by how much?
4. How has fleet average operating margin trended month-over-month?
5. Which fiscal quarter had the largest budget variance, and what drove it by department?
6. Top 10 cost centers by CapEx committed USD this year — and how much remaining budget do they hold?
7. What is the monthly trend in YTD spend versus annual budget pacing across all departments?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
