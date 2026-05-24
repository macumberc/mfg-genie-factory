# DistroCapital Finance — Demo Script

**Space:** Industrial Distribution — DistroCapital Finance - Working Capital & Cash Flow 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Treasurer, Branch Manager, Segment GM
**KPIs touched:** Cash conversion cycle days, DSO, DPO, Net cash flow, Current ratio, AR balance and inventory investment
**Big decision automated:** Which customer accounts get their credit terms tightened this quarter, which vendor terms get renegotiated, and how many DSO days the next cash-conversion-cycle target commits to releasing.

---

## Pre-demo checklist

- Open the Genie space `DistroCapital Finance - Working Capital & Cash Flow 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> DistroCapital Finance runs treasury and working capital across 20 business units spanning pipe & valve, industrial supply, electrical, welding, safety, and corporate — across multiple regions with B2B credit terms ranging from net-15 to net-90. Today the AR aging lives in the controller's daily aged-trial-balance, the DSO/DPO trend is a treasury team's weekly Excel, and the cash-conversion-cycle commitment is a quarterly slide built for the board's audit committee. Three artifacts, same dollars — and when the CFO is asked at the earnings call whether DSO can come down 5 days next year, the answer is 'we're working on it' because nobody has the customer-level evidence to commit. This space ends that. One governed surface where the CFO, Treasurer, and Segment GMs run the same DSO / DPO / DIO levers on the same data, and the credit-tightening call gets made customer-by-customer instead of policy-wide.

---

## Key KPIs in scope

- Cash conversion cycle (CCC) days — industrial distribution typical 60-90 days, best-in-class <45
- DSO (Days Sales Outstanding) — target 30-45 days for B2B industrial
- DPO (Days Payable Outstanding) — target 30-45 days; widen carefully to preserve vendor terms
- Net cash flow ($) — inflow minus outflow over period
- Current ratio — healthy 1.5-2.5x; <1.0 is a liquidity warning
- AR balance and inventory investment ($) — capital tied up in operations
- Liquidity status mix (Strong/Adequate/Tight/Critical) — risk concentration
- Forecast variance (actual vs forecasted cash flow) — treasury planning accuracy

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — finding the cash drag and the AR concentration *(≈4 min)*

**Persona:** Branch Manager • **Job to be done:** Locate the business units bleeding cash and the customer accounts where AR is concentrated — before the monthly cash review surfaces them.

*This is the first stop in a real treasury review. Two questions in, the Branch Manager has the cash-position map and the AR ranking that used to take Treasury two days to assemble.*

### Question (Act 1.1)

> **Show monthly net cash flow by business segment for the trailing 12 months.**

**What to say while it runs:** Monthly net cash flow by business segment for the trailing 12 months. Net cash flow is the topline treasury signal — segments running negative for consecutive months are segments where the working-capital model isn't holding. The segment-level pattern tells you whether it's a topline problem or a cash-conversion problem.

**What to look for:** Monthly trend on `net_cash_flow` measure by `business_segment`. Look for segments where the line went negative without a corresponding revenue drop — that's pure cash-conversion drag.

**Land the point:** Cash position by segment used to surface in the monthly close — three weeks late. Now the Branch Manager and the Treasurer see the same number on Monday morning, and the cash-conversion intervention happens before the bank covenant conversation.

### Question (Act 1.2)

> **Top 10 business units by AR balance USD this week — and what is their DSO?**

**What to say while it runs:** Top 10 business units by AR balance with their DSO. AR balance is the absolute capital tied up; DSO tells you whether it's normal terms-extended or aging-and-uncollected. Units with high AR balance *and* DSO above 45 days are the customer-credit-terms tightening candidates.

**What to look for:** Ranked top-10 on `ar_balance_usd` from `cash_transactions` with `dso_days` beside. Top units with DSO > 45 are the credit-policy intervention list.

**Land the point:** That table is the actual credit-tightening shortlist. The Branch Manager and the CFO make the customer-credit call on AR-concentration evidence, not on whoever's been pushing back on Collections.

---

## Act 2 — The decision — DSO, DPO, and DIO levers; tightening credit terms *(≈4 min)*

**Persona:** Segment GM • **Job to be done:** Decide which customer accounts get terms tightened, which vendor terms get renegotiated, and how many days of DSO/DIO improvement the segment commits to.

*Three questions that turn the cash-conversion-cycle picture into a defensible customer-by-customer and vendor-by-vendor terms decision. The middle question is the anchor — the DIO-days to working-capital conversion that anchors the CFO's commitment.*

### Question (Act 2.1)

> **Which business segments have average cash conversion cycle above 75 days over the last quarter?**

**What to say while it runs:** Business segments with average CCC above 75 days over the last quarter. Industrial distribution typically runs 60-90 days CCC; best-in-class is under 45. Segments above 75 are segments where 30 days of working capital could be released with disciplined DSO and DIO action — and that's a number the Treasurer can take to the bank.

**What to look for:** Aggregate by `business_segment` on `avg_ccc_days`. Segments above 75 are the structural-improvement targets; segments above 90 are the urgent-intervention list.

**Land the point:** That ranking *is* the CCC improvement plan. The Segment GM commits to a CCC-days target for their segment, the CFO signs the working-capital release commitment, and the bank-relationship conversation becomes a presentation of evidence instead of a hope.

### Question (Act 2.2)

> **How has the count of business units in Critical or Tight liquidity status trended month-over-month?**

**What to say while it runs:** Monthly count of business units in Critical or Tight liquidity status. Critical and Tight are the buckets where current ratio drops below 1.5 — anything in Critical needs immediate intervention, and anything Tight is the leading indicator of the next Critical. Trending count tells you whether the portfolio is consolidating around liquidity strength or splintering.

**What to look for:** Monthly count on `critical_count` and a similar count for Tight from `working_capital_snapshots`. A rising line is structural; a flat-low line is portfolio discipline.

**Land the point:** Liquidity-status trending used to be discovered when a BU missed payroll. Now the CFO sees the count of Tight-or-worse units before it becomes a covenant conversation — and the credit-line draw decision gets made with two weeks of runway instead of two days.

> **Anchor moment.** Stop on the CCC-above-75 segments and the AR-by-DSO ranking on screen. Pick the worst case — say two segments running at 85 days CCC on a $400M annual revenue base across DistroCapital's portfolio.

> *Each day of CCC released on a $400M revenue base is roughly $1.1M of working capital freed — straight math, daily revenue × CCC days. Trimming 5 days off the cash conversion cycle is $5.5M of working capital released; trimming 10 days — credible if you tighten the worst tier-3 customer credit terms and stretch vendor payments on the two largest spend categories — is $11M. At a 6% cost of capital, that's $660K of annual interest savings on the freed working capital alone. And the bank covenant headroom from a current-ratio improvement is the real prize — it's the difference between needing a refinancing conversation and not.*

> That's the decision this space automates. Not the treasury report. The terms. Customer credit gets tightened on the 8 tier-3 accounts with DSO > 60, vendor terms get extended on the 3 largest spend categories, and the CFO commits to a 10-day CCC improvement at the next earnings call with evidence to back it.

### Question (Act 2.3)

> **What is the cash flow variance (actual minus forecast) by region for the latest month?**

**What to say while it runs:** Cash flow variance — actual minus forecast — by region for the latest month. Variance is the treasury-forecast accuracy read. Regions with consistent negative variance are regions where the cash forecast is structurally optimistic — and that's the planning discipline the Treasurer needs to fix before the next quarter's cash-needs ask.

**What to look for:** Aggregate variance by `region` for latest `forecast_month` from `working_capital_snapshots`. Regions with absolute variance > 10% of forecasted are the planning-discipline interventions.

**Land the point:** Forecast-vs-actual cash variance used to be a Treasury internal metric. Now it's a regional-leadership accountability — and the cash-planning accuracy lifts because the GM is being measured on it in the same surface as their P&L.

---

## Act 3 — The commitment — locking the working-capital target and the credit policy *(≈4 min)*

**Persona:** CFO (with Treasurer) • **Job to be done:** Defend the working-capital target to the board's audit committee and lock next year's credit policy, vendor-terms framework, and CCC commitment.

*The CFO doesn't need another treasury slide; they need the same DSO, DPO, and CCC numbers the segment GMs are acting on, in the same language, so the board-level commitment and the segment-by-segment accountability both anchor on one source.*

### Question (Act 3.1)

> **Top 10 business units by net working capital (AR + inventory − AP) this quarter.**

**What to say while it runs:** Top 10 business units by net working capital — AR plus inventory minus AP — this quarter. Net working capital is the capital-tied-up number that matters to the board. The units at the top with weak turnover are the segments that need either credit-policy tightening or inventory-rationalization — and that's where next year's working-capital ask lands first.

**What to look for:** Rank by `ar_balance_usd + inventory_investment_usd - ap_balance_usd` from `cash_transactions`. The top of the list is where the working-capital intervention has the most leverage.

**Land the point:** That's the actual working-capital portfolio view. The CFO walks into the board's audit committee with the BU-by-BU evidence, the segment GMs see the same ranking, and the working-capital target stops being a top-down ask and starts being a segment-by-segment commitment.

### Question (Act 3.2)

> **Which regions have DSO above 45 days, and how does their current ratio compare?**

**What to say while it runs:** Regions with DSO above 45 days with their current ratio. DSO above 45 days on B2B industrial is the credit-policy warning; current ratio below 1.5 is the liquidity warning. Regions where both are flashing are the regions where Sales gets new credit-policy guardrails and Treasury gets a credit-line headroom review.

**What to look for:** Filter regions with `dso_days > 45` from `cash_transactions` and `avg_current_ratio` from `working_capital_monthly`. The intersection is the credit-policy intervention list.

**Land the point:** Credit policy used to be argued between Sales and Treasury with each side citing different numbers. Now there's one number — and the policy gets set on regional evidence with the CFO holding the pen. That's the difference between treasury management as a back-office function and as a strategic lever.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — DistroCapital Finance — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly net cash flow by business segment for the trailing 12 months.
2. Top 10 business units by AR balance USD this week — and what is their DSO?
3. Which business segments have average cash conversion cycle above 75 days over the last quarter?
4. How has the count of business units in Critical or Tight liquidity status trended month-over-month?
5. What is the cash flow variance (actual minus forecast) by region for the latest month?
6. Top 10 business units by net working capital (AR + inventory − AP) this quarter.
7. Which regions have DSO above 45 days, and how does their current ratio compare?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
