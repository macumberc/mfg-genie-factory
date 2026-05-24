# SiteTrack Construction — Demo Script

**Space:** Construction & Engineering — SiteTrack Construction - Project Completion Monitoring 🏗️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Construction + CFO, Project Controls Lead, Project Director
**KPIs touched:** Schedule Performance Index, Cost Performance Index, Schedule variance, Percent complete, Crew productivity, Total Recordable Incident Rate proxy
**Big decision automated:** Which 3-5 projects in the portfolio get escalated for recovery action this month, which PMs and crews get redeployed, and which budgets get re-baselined to the CFO before EAC blows past board-approved limits.

---

## Pre-demo checklist

- Open the Genie space `SiteTrack Construction - Project Completion Monitoring 🏗️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> SiteTrack Construction is delivering 20 active projects — bridges, highways, hospitals, data centers, marine, renewables — with combined budget-at-completion north of $300M. Today SPI and CPI live in the Project Controls Lead's Primavera-fed Excel, the daily crew/cost/safety roll-up sits in each Project Director's WIP report, and the risk-tier and EAC slide gets rebuilt every Friday for the VP's red-yellow-green dashboard. Three artifacts, three update cadences, and a recovery decision that gets made when the project is already 8 weeks past the point where intervention was cheap. This space pulls SPI, CPI, schedule variance, earned value, actual cost, risk tier, and safety incidents into one governed surface — so the recovery conversation happens on the daily data, not the monthly slide.

---

## Key KPIs in scope

- Schedule Performance Index (SPI) — industry threshold: <0.9 = behind, >1.0 = ahead
- Cost Performance Index (CPI) — <0.95 = over budget, target ≥1.00
- Schedule variance (days) — negative = behind plan
- Percent complete (%) — earned-value based progress
- Crew productivity (work hours per day, crew_count)
- Total Recordable Incident Rate proxy — safety_incidents per project-month
- Budget at Completion vs. Actual Cost to Date — EAC/ETC driver
- High/Critical risk project count — escalation queue size

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **VP** | Vice President |

---

## Act 1 — The signal — catching the schedule slip before the EAC catches the board *(≈4 min)*

**Persona:** Project Controls Lead • **Job to be done:** Find the projects whose SPI trajectory says they're going to miss their delivery date, before the as-built does.

*This is the conversation that turns a weekly Primavera roll-up into a same-day recovery action. Two questions surface the slip while there's still budget left to fix it.*

### Question (Act 1.1)

> **Top 10 projects with the worst schedule performance index over the last 90 days — what's their risk level?**

**What to say while it runs:** Top 10 projects with the worst schedule_performance_index over the last 90 days, with their risk_level alongside. SPI under 0.9 means we're earning 90 cents of planned value for every dollar of schedule — that's behind-the-curve territory. Anything Critical or High risk in that table is a same-week conversation, not a monthly one.

**What to look for:** Ranked table: project_name, avg SPI, risk_level. The room should notice the projects that are *both* low SPI *and* Critical risk — those are the headline-risk items.

**Land the point:** Right there is the recovery short-list. The Project Controls Lead used to need a half-day stitching Primavera and the EVM workbook to get that list. Now it's the first 30 seconds of the Monday call — and the recovery PM is on a plane Tuesday.

### Question (Act 1.2)

> **Show monthly total earned value and actual cost to date by project type for the trailing 12 months.**

**What to say while it runs:** Monthly total_earned_value and total_actual_cost by project type over 12 months. The gap is the cost variance — when actual cost runs ahead of earned value, CPI drops and EAC bloats. Watch for project types where the two lines have been diverging for two or three months running; that's a structural CPI problem, not a one-month blip.

**What to look for:** Two-line monthly trend per project type, EV vs AC. Healthcare and Commercial Construction are typically the divergence flags in this portfolio — long durations, sticky labor cost.

**Land the point:** Before this space, that chart got rebuilt by hand for the Friday VP review. Now it's the *first* question of the controls cycle — and the project-mix re-baselining conversation starts a week earlier.

---

## Act 2 — The decision — escalate, accept, or rebaseline *(≈4 min)*

**Persona:** Project Director • **Job to be done:** Decide which projects get a recovery PM and a crew redeployment this month, which get a controlled re-baseline to the CFO, and which get accepted at the new EAC.

*Three questions turn the watch-list into a recovery action plan with dollars attached. The middle question is the anchor — schedule variance days converted into the dollars-of-overrun conversation the board is going to ask about.*

### Question (Act 2.1)

> **Which projects are flagged High or Critical risk this month, and what is their total budget at completion?**

**What to say while it runs:** Projects flagged High or Critical risk this month with their total budget_at_completion. Total BAC across the High/Critical bucket is the recovery program's funding ask. Anything Critical at >$15M BAC is a steering-committee item regardless of SPI — the optics alone justify the attention.

**What to look for:** Filtered list: risk_level IN ('High','Critical'), sorted by budget_at_completion DESC. The room should notice how concentrated the dollar exposure is — typically 3-4 projects own 60-70% of the high-risk BAC.

**Land the point:** That list is the difference between *managing a portfolio* and *managing the projects that actually move the year*. The Project Director now walks into the VP's office with the names, the dollars, and the next 30-day action.

### Question (Act 2.2)

> **How has average schedule variance days trended monthly across the portfolio by region?**

**What to say while it runs:** Average schedule_variance_days trended monthly by region. Negative variance is days behind plan; on a $20M project, every day of slip translates to roughly 1-2% of BAC in extended GCs and indirect cost. The region with worsening avg_schedule_variance is the region that needs a senior PM on a recovery rotation — not next quarter, this quarter.

**What to look for:** Monthly trend, avg_schedule_variance_days by region. Watch for regions where the variance line has been deteriorating four months running — that's a leading indicator the regional PM bench is overstretched.

**Land the point:** When the schedule-variance trend is on the same screen as the CPI deterioration, the recovery decision is no longer 'which project is loudest' — it's 'which region's PM bench gets the next senior hire, and which two projects get co-supervised this quarter'.

> **Anchor moment.** Hold the schedule-variance trend and the high-cost project leaderboard on screen. Pick the worst project — call it 45 days behind plan, $25M original budget, currently tracking $4M over.

> *Original BAC $25M, current cost variance signals a 16% overrun — right at the upper end of the 5-20% industry overrun band before formal re-baseline triggers. Extended GCs and indirect labor on a project this size run $40-60K per week of slip; 45 days is 6-7 weeks, so $250-400K of pure schedule-driven burn before any scope rework. A recovery PM rotation is roughly $200K/quarter; a controlled re-baseline tells the CFO the new number once instead of in three monthly surprises. Across the 4-5 projects in the High/Critical tier at this scale, the difference between *catch and recover* and *let it run* is $5-15M of contribution margin a year — which is the difference between a tolerable contractor and one the board calls a turnaround story.*

> That's the decision this space automates. Recovery PM redeployment and re-baseline timing get set on the same screen as the SPI and safety trend — not in next month's red-yellow-green slide. The PM and labor rotation gets built on dollars-of-overrun, not loudest email.

### Question (Act 2.3)

> **Top 10 projects by total daily cost spent this quarter, with crew count and safety incidents.**

**What to say while it runs:** Top 10 projects by total_daily_cost this quarter with crew_count and safety_incidents alongside. High daily cost AND high crew_count is the burn-rate signal — we're spending fast. High daily cost AND safety_incidents trending up is the *quality-of-execution* signal — the crew is overworked and the safety leading indicator is already moving.

**What to look for:** Ranked table: project_name, total_daily_cost, avg crew_count, total_safety_incidents. The room should notice the project that is *both* in the top 10 spend AND in the top 5 safety incidents — that's a near-miss away from a Recordable.

**Land the point:** That correlation is the difference between knowing a project is over-budget and knowing it's heading toward a stop-work order. The first is an EAC problem. The second is a CEO-call problem.

---

## Act 3 — The commitment — portfolio policy and next-cycle PM allocation *(≈4 min)*

**Persona:** VP Construction • **Job to be done:** Defend the portfolio performance and the recovery plan to the CFO and the board, and shape which project types the firm pursues next year.

*The VP doesn't need new charts; they need the same SPI, CPI, schedule-variance, and EAC numbers the controls team is acting on, in board-ready form, so the portfolio narrative writes itself.*

### Question (Act 3.1)

> **What is the monthly trend in high/critical risk project count for the trailing 12 months?**

**What to say while it runs:** Monthly trend in high_risk_count over 12 months. The shape of that line *is* the portfolio's health story. If the count is climbing despite added controls, the issue is intake (we're taking on work we can't deliver). If it's declining, the recovery program is working and the CFO sees it.

**What to look for:** Monthly trend of high/critical risk_level project count. Watch for inflection points that line up with intake decisions — e.g. a spike six months after a quarter of aggressive pursuits.

**Land the point:** When that single chart is in the VP's hand before the board meeting, the conversation about *intake discipline* writes itself — and next year's pursuit-mix policy stops being a hallway debate.

### Question (Act 3.2)

> **Which project types have the lowest average cost performance index, and what is their total actual cost to date?**

**What to say while it runs:** Project types with the lowest average cost_performance_index and their total_actual_cost. CPI under 0.95 is over-budget territory; under 0.85 is structurally over-budget — the unit rates we estimated with are simply wrong for that work type. That's not a recovery problem; that's an estimating-input problem the next bid cycle has to fix.

**What to look for:** Ranked project types by avg CPI ascending, total_actual_cost alongside. The room should notice the project types where we're losing the most money in absolute dollars, not just percentage.

**Land the point:** Triage at 9, recovery decisions at noon, portfolio strategy at 4. Same space, same numbers. The Project Controls Lead's recovery list and the VP's board narrative are now the same artifact — and the CFO gets one story instead of three reconciliations.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — SiteTrack Construction — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 projects with the worst schedule performance index over the last 90 days — what's their risk level?
2. Show monthly total earned value and actual cost to date by project type for the trailing 12 months.
3. Which projects are flagged High or Critical risk this month, and what is their total budget at completion?
4. How has average schedule variance days trended monthly across the portfolio by region?
5. Top 10 projects by total daily cost spent this quarter, with crew count and safety incidents.
6. What is the monthly trend in high/critical risk project count for the trailing 12 months?
7. Which project types have the lowest average cost performance index, and what is their total actual cost to date?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
