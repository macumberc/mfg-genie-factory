# LedgerView Industrial — Demo Script

**Space:** Machinery — LedgerView Industrial - Financial Analytics 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Controller, FP&A Director, Business-unit leaders
**KPIs touched:** Gross margin, Operating margin, Budget utilization, Variance vs budget, Revenue, Total expense
**Big decision automated:** Which 2-3 cost centers absorb the cost cut, which product lines lose program capex next FY, and where the FP&A budget defends its credibility with the lender on the covenant call.

---

## Pre-demo checklist

- Open the Genie space `LedgerView Industrial - Financial Analytics 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> LedgerView Industrial closes its books against 20 cost centers across four divisions — Industrial Manufacturing, Technology (R&D + IT), Commercial (Sales & Marketing), and Corporate G&A — funded by an FY26 operating plan with covenant-driven margin targets to its senior lender. Today the Controller works variance out of Hyperion exports, FP&A reconciles budget-vs-actual in a 30-tab Excel rolled up by division, and the CFO's lender package gets stitched together from three different sources of truth a week before each quarterly call. Three workbooks, one chart of accounts, and the program-capex-defense conversation gets reopened every cycle because the numbers don't reconcile. This space ends that: one governed surface where gross margin, operating margin, budget utilization, and variance all resolve to the same cost center and the same fiscal period — so the cost-cut allocation and the covenant defense come out of the same artifact.

---

## Key KPIs in scope

- Gross margin (%) — industrial machinery typical 25–35%, leaders 35%+
- Operating margin (%) — industrial OEMs typical 8–15%
- Budget utilization (%) — target 95–105% (within plan)
- Variance vs budget ($ and %) — early warning trigger
- Revenue ($) — top-line growth
- Total expense ($) — cost containment KPI
- Cost per headcount ($) — productivity benchmark
- Pending / reversed transactions — close-cycle hygiene

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **KPI** | Key Performance Indicator |
| **OEM** | Original Equipment Manufacturer |

---

## Act 1 — The signal — finding the cost centers bending the operating plan *(≈4 min)*

**Persona:** FP&A Director • **Job to be done:** Build this week's variance-review hot-list before the close meeting, with the margin drift identified by cost center type instead of by who emailed the Controller first.

*This is the conversation that gates which cost centers get a budget challenge ahead of the next reforecast. Two questions in, FP&A already has the candidate list.*

### Question (Act 1.1)

> **What is the monthly trend in gross margin by cost center type over the trailing 12 months?**

**What to say while it runs:** Monthly trend in avg_gross_margin by cost_center_type over the trailing 12 months. Industrial machinery typical is 25-35%; leaders run 35%+. The shape of the line by division tells you whether the margin pressure is in Manufacturing, R&D burn, Sales discounting, or G&A bloat — and each of those has a different owner.

**What to look for:** Five lines on one chart — Manufacturing, R&D, Sales & Marketing, G&A, IT. Watch for the type whose line has bent below 25%; that's a structural margin problem, not a single-period miss.

**Land the point:** When FP&A can see margin drift by cost center type without rebuilding the close pack, the budget-challenge conversation moves from anecdotal to evidentiary. The reforecast cycle compresses, and the CFO walks into the lender call already knowing which division owes a story.

### Question (Act 1.2)

> **Top 10 cost centers by budget variance — which are most over budget this quarter?**

**What to say while it runs:** Top 10 cost centers by total budget variance this quarter — variance_usd negative means over budget. The CFO doesn't want the entire 20; the CFO wants the top 10 worst-offenders, ranked by dollar magnitude, so the conversation prioritizes itself.

**What to look for:** Ranked cost_center_id with variance_usd. The largest negative variances are the cost-cut candidates; the largest positive variances might be plan-quality issues or capacity not yet deployed.

**Land the point:** That ranked list used to be a Friday-night FP&A exercise. Now it's the input to Monday's variance review — three cost centers get a 'show us the plan' email and the rest stay on autopilot. Time to insight collapses from a week to an afternoon.

---

## Act 2 — The decision — which 2-3 cost centers fund the cost cut and which programs lose capex *(≈4 min)*

**Persona:** CFO • **Job to be done:** Lock the recommendation on where the $X million cost reduction comes from, which programs survive the reforecast, and how the operating-margin story gets defended to the lender.

*These three questions are where the cost-cut allocation gets committed. Operating-margin coverage tells you where the structural problem is; revenue-vs-expense tells you the trajectory; cost-per-headcount ranks productivity for the layoff-vs-reinvest decision.*

### Question (Act 2.1)

> **Which cost center types have operating margin below the 8% industrial OEM benchmark?**

**What to say while it runs:** Cost_center_types whose avg_operating_margin sits below the 8% industrial OEM benchmark. Below 8% on a sustained basis is either a structural cost issue or a pricing-power issue — and at this scale it's the leading indicator for the lender's covenant test.

**What to look for:** Bar chart by cost_center_type with avg_operating_margin filtered to below 8%. The cost centers in this list are either getting restructured, sold, or have to write a credible margin-recovery plan into the FY27 operating plan.

**Land the point:** When the CFO can see operating-margin coverage by cost center type in one query, the lender-covenant defense stops being a Saturday spreadsheet exercise. The conversation with the bank moves from 'we're working on it' to 'here's the three cost centers we're acting on, and here's the savings curve.'

### Question (Act 2.2)

> **Show monthly trend in total revenue vs total expenses across the company.**

**What to say while it runs:** Monthly total_revenue overlaid with total_expenses across the company. We want revenue trending up while expenses hold flat — anything else is a margin compression story we need to tell preemptively. The gap between the lines is what funds capex and dividends.

**What to look for:** Two lines on one chart, 12 months. The convergence or divergence is the FY26 operating-plan-vs-actuals story the board will see at the next meeting.

**Land the point:** Same chart the Controller is using to close the month, now the CFO's headline slide for the board. The argument about 'whose number is right' goes away — there's one revenue number, one expense number, one operating-margin shape. That's the credibility win with the lender.

> **Anchor moment.** Stop on the operating-margin coverage chart and the cost-per-headcount ranking. Pick a single cost center — say a Sales & Marketing cost center running 4% operating margin against a 10% target, with about $4M annual spend, on a $200M revenue base for the division.

> *A 6-percentage-point operating-margin gap on $4M of cost center spend is $240K per year of margin shortfall — but the larger story is that this cost center is a stand-in for the same pattern across three other Commercial centers. If the four Sales & Marketing cost centers each have a similar 4-6pp gap, the combined operating-margin lift from fixing them is $1-2M annually. On a $200M revenue base where the lender covenant test is operating margin > 10%, that 50-100bps swing is the difference between passing and tripping the covenant — which is hundreds of basis points of refinancing cost, not just an internal target miss.*

> That's the program-capex defense in one calculation. Sales & Marketing absorbs the FY27 cost cut, R&D defends its budget because cost-per-headcount is benchmark-appropriate, G&A gets a productivity stretch. The covenant call gets a real plan instead of a deferral. Decision made on dollars, in one conversation, with the same numbers the Controller closes the month on.

### Question (Act 2.3)

> **Rank cost center types by cost per headcount — where is productivity strongest?**

**What to say while it runs:** Cost_center_types ranked by total_cost_per_headcount. Manufacturing should be the lowest fully-loaded cost; R&D and Sales the highest. If G&A is anywhere near R&D, that's the cost-cut conversation. If Manufacturing is rising faster than revenue, that's an automation case.

**What to look for:** Ranked cost_center_type with total_cost_per_headcount. The order should match industry expectations; any inversion is a flag.

**Land the point:** Cost per headcount lands the productivity argument in one number. When the FP&A Director, the CFO, and the business-unit leaders all see the same ranking, the layoff-vs-reinvest decision becomes a defensible action plan — not a political fight.

---

## Act 3 — The commitment — locking the FY operating plan and the lender narrative *(≈4 min)*

**Persona:** Controller • **Job to be done:** Defend the close to the auditor and lock the FY operating plan against the same numbers FP&A and the CFO use in the lender pack.

*The Controller doesn't need a new dashboard; they need posting-status hygiene and the cost-per-headcount ranking in the same artifact the CFO defended to the lender — so close quality and operating-plan defensibility are the same problem.*

### Question (Act 3.1)

> **Top 10 cost centers by total expense this year, and how does that compare to budget?**

**What to say while it runs:** Account_category breakdown of pending and reversed postings with dollar value. Pending + Reversed above 5% of total transactions is a close-quality flag — auditors will find it, the lender will ask about it, and FP&A's variance commentary becomes unreliable until it's cleaned up.

**What to look for:** Account_category with counts and dollar value where posting_status IN ('Pending','Reversed'). Watch for a category — Revenue or COGS especially — with a disproportionate share. That's an audit-trail problem before it's an FP&A problem.

**Land the point:** When the Controller can see close-cycle hygiene by account category in one query, the audit prep cycle compresses by a week. More importantly, the FP&A variance commentary the CFO uses with the lender is defensible — every number traces back to a posted transaction, not a pending one.

### Question (Act 3.2)

> **Which account categories have the most pending or reversed postings, and what is the dollar value?**

**What to say while it runs:** Top 10 cost centers by total expense this year, with implicit comparison to budget. The top spenders are the ones the lender will ask about line by line — and the gap between actual and budget is the credibility test for the FY operating plan.

**What to look for:** Ranked cost_center_id with SUM(total_expense_usd) and the implicit budget overlay from budget_snapshots. Watch for the cost center that's 110%+ of budget without a corresponding revenue overshoot — that's the explanation owed to the lender.

**Land the point:** Same numbers FP&A is acting on, same numbers the CFO is defending. The lender call stops being a stitch-together exercise and starts being a one-artifact conversation. Three teams, one chart of accounts, one set of numbers — that's the close-cycle credibility upgrade.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — LedgerView Industrial — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. What is the monthly trend in gross margin by cost center type over the trailing 12 months?
2. Top 10 cost centers by budget variance — which are most over budget this quarter?
3. Which cost center types have operating margin below the 8% industrial OEM benchmark?
4. Show monthly trend in total revenue vs total expenses across the company.
5. Rank cost center types by cost per headcount — where is productivity strongest?
6. Top 10 cost centers by total expense this year, and how does that compare to budget?
7. Which account categories have the most pending or reversed postings, and what is the dollar value?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
