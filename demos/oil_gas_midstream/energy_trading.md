# TradeFlow Energy — Demo Script

**Space:** Oil & Gas Midstream — TradeFlow Energy - Energy Trading Analytics ⚡
**Runtime:** ~15 minutes • 7 questions
**Audience:** Head of Trading + Trading Lead, Chief Risk Officer, CFO
**KPIs touched:** Realized P&L, Volume traded, MTM value, VaR 95%, Net position, Delta
**Big decision automated:** How to rebalance the book — which commodity to run net long vs. net short, which counterparty exposure to cap, and which spread book to expand vs. unwind before the next VaR breach.

---

## Pre-demo checklist

- Open the Genie space `TradeFlow Energy - Energy Trading Analytics ⚡`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> TradeFlow Energy runs a multi-commodity book across crude, natural gas, NGLs, and refined products. Today the realized P&L lives in the Trading Lead's settlement workbook, the MTM and VaR live in the risk team's mark-to-market sheet that lands at 7 AM the next day, and the counterparty exposure lives in the CFO's credit committee tracker. Three workbooks, same book — and the position-sizing decision, the counterparty-limit-renewal decision, and the morning VaR walk all get made on different snapshots of reality. This space ends that. One governed surface where pnl_usd, net_position_bbl, mtm_value_usd, and var_95_usd line up against the same contract list — so the rebalance conversation happens before the breach, not the morning after.

---

## Key KPIs in scope

- Realized P&L ($) — settled trading gains/losses
- Volume traded (bbl) — book activity by commodity
- MTM value ($) — current mark-to-market exposure
- VaR 95% ($) — 1-day 95% value at risk
- Net position (bbl) — directional commodity exposure
- Delta — first-order price sensitivity
- Sharpe ratio — risk-adjusted return (target >1.0)
- Win rate (%) — share of profitable trades (benchmark >55%)

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — which commodity is making money and which is bleeding into VaR *(≈4 min)*

**Persona:** Trading Lead • **Job to be done:** Identify the books, commodities, and contracts driving P&L vs. consuming VaR before the pre-open call.

*This is the moment the day's position-sizing decision starts to form. Two questions in, the desk has the commodity-level P&L and the volume-by-contract ranking the risk team will reconcile against by 9 AM.*

### Question (Act 1.1)

> **Show monthly total P&L by commodity for the trailing 12 months.**

**What to say while it runs:** Monthly P&L by commodity is the desk-health view. Crude vs. gas vs. NGL vs. refined — the four books shouldn't all be making money or losing money in the same month. If they are, we're not trading the spreads, we're long the market.

**What to look for:** Monthly bars of total_pnl_usd by commodity over 12 months — DATE_TRUNC('month', trade_date) shape. The room should notice which commodity is the steady contributor and which is the volatile one driving VaR consumption.

**Land the point:** Now the Trading Lead walks into the morning call with the question already framed — 'we're earning on gas spreads and bleeding on crude, do we cut crude size or rotate desks' — and that's the conversation the Head of Trading wants to have in 30 seconds, not 30 minutes.

### Question (Act 1.2)

> **Top 10 contracts by total volume traded year-to-date.**

**What to say while it runs:** Top 10 contracts by total_volume_bbl YTD is the activity map — and the Sharpe-ratio target is >1.0, so we're looking for the contracts where volume is high AND it's actually paying for the risk. High-volume, low-Sharpe contracts are the ones we're either re-pricing or unwinding.

**What to look for:** Ranked table of contract_name with total_volume_bbl. The story is in the contracts at the top — these are where the book's risk lives, and where the next pricing or limit conversation has to land.

**Land the point:** That ranking used to require an end-of-month settlement run plus risk reconciliation. Now it's a question — and that's the difference between waiting on a settlement file and acting on it inside the trading day.

---

## Act 2 — The decision — rebalancing the book and locking the counterparty limits *(≈4 min)*

**Persona:** Head of Trading • **Job to be done:** Decide which commodity to net long or short, which counterparty type's exposure to cap, and which spread book to grow vs. unwind for the week.

*Three questions that turn the activity view into a defensible book-rebalance recommendation. The middle question is the anchor — the VaR-trend and P&L-impact math that turns a dashboard into a position decision.*

### Question (Act 2.1)

> **Which counterparty types have the largest net position exposure right now?**

**What to say while it runs:** Counterparty-type net position is the credit conversation. We have producer-side, refiner-side, marketer-side, and bank-side counterparties, and our net exposure on each has to fit inside the credit committee's tier limits. If marketers are running too long on us, that's a margin-call risk in a price-spike.

**What to look for:** Counterparty_type with avg_net_position_bbl. The biggest absolute exposure is where the credit memo gets re-pulled this week.

**Land the point:** When the Head of Trading and the CFO see the same counterparty exposure in the same view, the limit-renewal conversation moves from 'CFO asks for the report' to 'desk and credit agree the cap and post it by close.'

### Question (Act 2.2)

> **How has total VaR trended month-over-month across the trading book?**

**What to say while it runs:** Total VaR trend month-over-month is the firm-level risk story. Our 1-day 95% VaR has hard board limits, and if total_var_usd has been climbing four months in a row without P&L climbing with it, we're paying for risk we're not capturing — that's a sizing problem, not a market problem.

**What to look for:** Monthly trend of total_var_usd. Flat or declining VaR with rising P&L is the desired shape; rising VaR with flat P&L is the rebalance trigger.

**Land the point:** That trend is the input to next week's position-sizing memo. The desk cuts contract size on the books bleeding VaR, and the freed risk capacity rotates to the spread book that's earning.

> **Anchor moment.** Hold on the VaR-trend chart and the top-MTM contract list. Imagine total_var_usd has drifted from $2M to $4M over the last two months, while monthly_pnl_usd has been roughly flat.

> *$4M of 1-day 95% VaR on a flat P&L book is signal that we're paying for risk we're not capturing. Annualized P&L on a healthy book runs 1-3% of notional traded — so a $500M notional book should be earning $5-15M/year, not flat. A 25% size reduction on the two highest-VaR contracts cuts $4M VaR to roughly $3M and frees the risk capacity for two new spread positions; at 2% expected return on $100M reallocated, that's $2M of incremental P&L in 12 months, on the same firm-level risk budget.*

> That's the decision this space automates. Not the daily risk slide. The rebalance. Net long/short by commodity and counterparty caps get set on VaR-to-P&L efficiency, not on the loudest voice on the morning call.

### Question (Act 2.3)

> **Top 10 contracts by total MTM value as of the latest snapshot.**

**What to say while it runs:** Top 10 contracts by total_mtm_usd as of latest snapshot is the unrealized-exposure view. A big positive MTM is good news only if we have a clear unwind path; a big negative MTM is where the next surprise loss comes from — that's the unwind-vs-hold call we'll make in the next anchor.

**What to look for:** Ranked table by total_mtm_usd. The signed value matters — sort by absolute value to find the contracts whose marks are moving the firm's book.

**Land the point:** When the desk can pull the top MTM contracts in a question, the daily risk-committee walk stops being a slide pack and becomes a working session — and the unwind decisions get made the same day the marks move.

---

## Act 3 — The commitment — defending the book to the risk committee and CFO *(≈4 min)*

**Persona:** Chief Risk Officer • **Job to be done:** Sign off on the desk's rebalance plan and present the residual exposure to the CFO and audit committee.

*The CRO doesn't need a second risk dashboard; they need the same P&L, position, and VaR numbers the desk is trading on — so the limit framework and the audit-committee narrative are built off one source.*

### Question (Act 3.1)

> **What is the average trade price by commodity in the last quarter, and how does that compare to the prior quarter?**

**What to say while it runs:** Average trade price by commodity last quarter vs. prior quarter is the execution-quality view. If our average price is materially off mid-market, we're either chasing fills or being picked off by counterparties — both are conversations the CRO has to have with the desk.

**What to look for:** Avg_price_usd by commodity for two quarters side by side. The delta is the story — a 1-2% drift on a billion-dollar notional is real money.

**Land the point:** When the CRO can run that comparison in a question instead of waiting on the quarterly TCA report, the execution-quality conversation happens four weeks earlier — and that's the difference between a behavior change and a quarterly slap on the wrist.

### Question (Act 3.2)

> **Which commodities have the highest share of unsettled trades, and what is the volume at risk?**

**What to say while it runs:** Commodities with the highest share of unsettled trades + volume at risk is the operational-risk view. Settlement_status of unsettled past T+2 is where margin calls and fails-to-deliver live, and that's reputational risk we don't want surfacing at the audit committee.

**What to look for:** Commodity with unsettled share and volume_bbl. Anything above industry-norm unsettled rate is a back-office conversation, not a trading one.

**Land the point:** Same numbers the desk trades on, the back office settles on, and the CRO defends to the audit committee. That's the one-version-of-truth the regulator asks about — and now we can answer in real time.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — TradeFlow Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total P&L by commodity for the trailing 12 months.
2. Top 10 contracts by total volume traded year-to-date.
3. Which counterparty types have the largest net position exposure right now?
4. How has total VaR trended month-over-month across the trading book?
5. Top 10 contracts by total MTM value as of the latest snapshot.
6. What is the average trade price by commodity in the last quarter, and how does that compare to the prior quarter?
7. Which commodities have the highest share of unsettled trades, and what is the volume at risk?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
