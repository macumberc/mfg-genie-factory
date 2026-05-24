# MidCapital Systems — Demo Script

**Space:** Oil & Gas Midstream — MidCapital Systems - Working Capital & Cash Flow Optimization 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Treasurer, Controller, AR / AP Leadership
**KPIs touched:** Free cash flow, DSO, DPO, Cash conversion cycle, Current ratio, Net debt
**Big decision automated:** Which business units pull their DSO inside 45 days this quarter, which JIB / payables-cycle terms we re-negotiate with the top 5 shippers, and how much trapped working capital we free to fund the next dropdown.

---

## Pre-demo checklist

- Open the Genie space `MidCapital Systems - Working Capital & Cash Flow Optimization 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> MidCapital Systems manages cash and working capital across gathering, processing, and transmission business units serving multiple operating regions. Today the DSO and JIB-aging numbers live in the AR team's collections workbook, the DPO and payables schedule live in the AP team's vendor-cycle tracker, and the free-cash-flow view lives in the Treasurer's monthly capital-stack model. Three workbooks, same balance sheet — and the collections-prioritization decision, the payables-timing strategy, and the next-dropdown funding case all get built from snapshots that don't reconcile. This space ends that. One governed surface where accounts_receivable_usd, dso_days, dpo_days, free_cash_flow_usd, and cash_conversion_cycle_days line up by business unit and segment — so the working-capital release becomes a quarterly cash-target, not an annual aspiration.

---

## Key KPIs in scope

- Free cash flow ($) — primary cash-generation metric
- DSO (days) — days sales outstanding (midstream median ~45-55)
- DPO (days) — days payables outstanding (target 45-60)
- Cash conversion cycle (days) — DSO + DIO − DPO; target <30 days
- Current ratio — short-term liquidity (healthy >1.5)
- Net debt ($) — debt minus cash, leverage proxy
- AR / AP / Inventory balances ($) — working-capital components
- Net cash flow ($) — inflows minus outflows by period

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **DIO** | Days Inventory Outstanding |

---

## Act 1 — The signal — where the cash is trapped and where it's flowing *(≈4 min)*

**Persona:** Controller • **Job to be done:** Identify the business units and segments where free cash flow is eroding and AR balances are concentrating, before the treasury-team's weekly cash forecast.

*This is the moment the quarter's cash-target conversation starts to form. Two questions in, the controller has the FCF trend and the AR-balance ranking that used to take a week of GL extracts and AR-aging joins.*

### Question (Act 1.1)

> **Show monthly free cash flow by segment for the trailing 12 months.**

**What to say while it runs:** Monthly free_cash_flow_usd by segment over the trailing 12 is the cash-generation view. Gathering, processing, and transmission have very different cash profiles — gathering is volume-led, transmission is contracted demand charges — and we want to see which segment is reliably generating cash and which is sawtoothing.

**What to look for:** Monthly bars of free_cash_flow_usd by segment — DATE_TRUNC('month', kpi_month) shape. The room should notice which segment is the steady cash generator and which is the volatile one creating treasury-forecasting headaches.

**Land the point:** Now the controller walks into the treasury meeting with the cash-generation picture already framed — and the conversation that used to start 'where are we on cash' starts 'gathering is the volatility, here's why, here's the plan.'

### Question (Act 1.2)

> **Top 10 business units by total accounts receivable as of the latest snapshot.**

**What to say while it runs:** Top 10 business units by total accounts_receivable_usd is the trapped-cash view. AR is real cash sitting on the balance sheet — every dollar there is a dollar we could have used to fund capex, repay revolver, or distribute. The top 10 BUs typically carry 60-70% of total AR, and that's where the collections campaign has to land.

**What to look for:** Ranked table of business_unit_name with total accounts_receivable_usd. The top 5 are the BUs where collections leadership gets a name-by-name action plan, not a general 'reduce DSO' target.

**Land the point:** That list used to be the output of monthly AR aging plus business-unit reconciliation. Now it's a question — and the collections-prioritization conversation happens at week +1, not month +1.

---

## Act 2 — The decision — releasing trapped working capital this quarter *(≈4 min)*

**Persona:** Treasurer • **Job to be done:** Lock the working-capital-release target by segment and decide which shipper / JIB terms get re-negotiated this cycle.

*Three questions that turn the AR view into a cash-release commitment. The middle question is the anchor — the DSO-to-dollars math that converts a controller dashboard into a CFO-level cash target.*

### Question (Act 2.1)

> **Which segments have DSO above 45 days, and how has that trended monthly?**

**What to say while it runs:** Segments with dso_days above 45 days and how that's trended monthly is the structural-vs-cyclical view. Midstream median DSO runs 45-55; anything above 45 sustained for two months running is either a JIB-billing problem with the operators or a shipper invoice-dispute backlog — and the fix is different in each case.

**What to look for:** Segments filtered to dso_days > 60 with the monthly shape. A rising DSO line is the trigger for a collections SWAT team; a flat line above 60 is a contract-term renegotiation candidate.

**Land the point:** When the Treasurer can see DSO above 60 by segment with the trend in one view, the collections decision moves from a generic AR campaign to a named-segment plan that the controller and the shipper-relationship lead both own.

### Question (Act 2.2)

> **How has the cash conversion cycle trended month-over-month across the company?**

**What to say while it runs:** Cash conversion cycle month-over-month is the working-capital-machine view. Target is under 30 days; we live in the 35-50 range. The shape — flattening, rising, declining — tells us whether the levers we're pulling (collections, payables timing, inventory drawdown) are actually working as a system.

**What to look for:** Monthly trend of cash_conversion_cycle_days. A flat-to-declining line below 35 is healthy; a rising line means we're either funding receivables growth or losing payables leverage.

**Land the point:** That trend reframes the working-capital conversation from a monthly close ritual to a quarterly target the CFO and Treasurer commit to in front of the board. Same numbers, different conversation.

> **Anchor moment.** Hold on the cash-conversion-cycle trend and the DSO-above-60 table. Take the gathering segment — call it $400M annual revenue, current DSO of 65 days against a target of 45.

> *Pulling DSO from 65 to 45 days on $400M of annual revenue is $400M × (20/365) = $22M of working capital released — one-time, permanent, free. Layer in payables-timing optimization (DPO from 40 to 55 on a $250M annual payables base) and that's another $250M × (15/365) = $10M released. Combined, $32M of one-time cash freed on a single segment. Across two underperforming segments at roughly the same scale, $50-60M of trapped cash comes back to the balance sheet — enough to fund a dropdown without revolver draw, or to add 6 cents of distribution coverage on the MLP unit.*

> That's the decision this space automates. Not the monthly close memo. The capital release. Working-capital targets become quarterly commitments with named owners, and the next dropdown gets funded from operations instead of debt.

### Question (Act 2.3)

> **Top 10 business units by net cash flow year-to-date.**

**What to say while it runs:** Top 10 business units by net_cash_flow_usd YTD is the where-cash-is-coming-from view. Inflows minus outflows by BU shows us which units are net contributors and which are net consumers of cash — and that's the input to the dropdown-coverage and the inter-company funding decisions.

**What to look for:** Ranked table of business_unit_name with net_cash_flow_usd. The top contributors are the BUs whose cash funds the bottom-of-the-list growth investments.

**Land the point:** When the Treasurer can rank BUs by net cash contribution, the inter-segment funding conversation stops being political and becomes mechanical — and that's how the next dropdown gets sized.

---

## Act 3 — The commitment — defending the capital plan and the distribution policy *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the cash-generation plan to the board and lock the distribution-coverage commitment for the next four quarters.

*The CFO doesn't need a second cash dashboard; they need the same FCF, DSO, and current-ratio numbers the Treasurer and Controller are running on — so the board cash narrative and the distribution-coverage commitment are built off one source.*

### Question (Act 3.1)

> **What is the total inventory balance by region this quarter compared to last quarter?**

**What to say while it runs:** Total inventory_usd by region this quarter compared to last quarter is the slow-moving-cash view. Midstream inventory is mostly linefill, chemicals, and integrity spares — but it still ties up cash, and if it's growing region-over-region without a project justification, that's a working-capital target we can attack.

**What to look for:** Region with current quarter total_inventory_usd vs. prior quarter. The biggest signed increase is the region where the operations team owes a story.

**Land the point:** When the CFO can see inventory growth by region paired with what's driving it, the inventory-discipline conversation moves from once-a-year audit finding to a quarterly working-capital review that the operations leads have to defend.

### Question (Act 3.2)

> **Which business units have a current ratio below 1.5, and what is their net debt?**

**What to say while it runs:** Business units with a current_ratio below 1.5 and their net_debt_usd is the liquidity-risk view. Healthy operators sit above 1.5; below 1.0 is a board-level conversation. Pair that with net_debt to see whether the issue is short-term illiquidity or structural leverage.

**What to look for:** Business_unit_name with current_ratio < 1.5 and net_debt_usd. Low-ratio, high-debt is the segment that needs either a capital injection or an operating restructuring.

**Land the point:** Triage in the AR meeting at 8 AM, working-capital target locked by afternoon, distribution-coverage commitment defended to the board by Friday. Same space. Same numbers. The Controller's collections plan, the Treasurer's cash forecast, and the CFO's distribution-policy commitment are now the same artifact.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — MidCapital Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly free cash flow by segment for the trailing 12 months.
2. Top 10 business units by total accounts receivable as of the latest snapshot.
3. Which segments have DSO above 45 days, and how has that trended monthly?
4. How has the cash conversion cycle trended month-over-month across the company?
5. Top 10 business units by net cash flow year-to-date.
6. What is the total inventory balance by region this quarter compared to last quarter?
7. Which business units have a current ratio below 1.5, and what is their net debt?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
