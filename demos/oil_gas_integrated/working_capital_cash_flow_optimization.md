# CashFlow Energy — Demo Script

**Space:** Oil & Gas Integrated — CashFlow Energy - Working Capital & Cash Flow Optimization 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO and Treasurer + Treasury Director, Corporate Controller, Divisional Finance Lead (Upstream)
**KPIs touched:** Free cash flow, DSO, DPO, Cash conversion cycle, Current ratio, Net debt
**Big decision automated:** Which business units carry a JIB / receivables collection sprint, which get a payables-stretch directive, and which get OPEX-timing protection — and how the freed working capital funds the next dividend installment vs. the buyback authorization.

---

## Pre-demo checklist

- Open the Genie space `CashFlow Energy - Working Capital & Cash Flow Optimization 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CashFlow Energy runs 20 business units across Upstream, Downstream, Midstream, and Corporate — a $40B revenue, $25B OPEX integrated. Today daily inflows and outflows are reconciled by Treasury out of the cash management system every morning, DSO and AR aging live in the Controller's monthly close pack, and the free-cash-flow forecast that supports the dividend recommendation is owned by Corporate Finance in a separate workbook. Three artifacts, same liquidity — and when oil prices move $10 in a month the CFO walks into the dividend-and-buyback review with three slightly different views of the cash-conversion cycle and how much head-room the balance sheet really has. This space ends that. Inflows, outflows, AR, AP, inventory, DSO, DPO, cash conversion cycle, free cash flow, net debt — answered out of one governed surface, against the same definition of segment.

---

## Key KPIs in scope

- Free cash flow ($MM) — primary shareholder-return funding source
- DSO (days sales outstanding) — IOC benchmark 30-45 days
- DPO (days payable outstanding) — typically 30-50 days for majors
- Cash conversion cycle (days) — DSO + DIO - DPO; lower = better
- Current ratio — liquidity health, target >1.0
- Net debt ($MM) — leverage indicator
- Accounts receivable / payable / inventory ($MM) — working-capital component balances
- Cash balance ($MM) — on-hand liquidity by business unit

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **DIO** | Days Inventory Outstanding |

---

## Act 1 — The pulse — where cash is actually moving across the portfolio *(≈4 min)*

**Persona:** Treasury Director • **Job to be done:** Anchor the daily cash position and the segment-level free-cash-flow trajectory before the weekly Treasury committee.

*This is the Treasury Director's window before the weekly cash call. Two questions in, the cash-inflow ranking and the segment FCF curve are on screen — the same numbers that used to require reconciling three reports.*

### Question (Act 1.1)

> **Top 10 business units by total cash inflows over the last 90 days.**

**What to say while it runs:** Top 10 business units by total cash inflows over the last 90 days. The point isn't the rank — Upstream is always near the top. The point is the concentration. In integrated portfolios, 60-70% of cash inflow concentrates in 5-6 business units; that's the working-capital exposure if any one of them has a JIB or counterparty timing issue.

**What to look for:** Ranked table of 10 business units by total_inflows_usd over 90 days. Watch the spread — and watch where Midstream and Downstream units sit relative to Upstream. That mix is the structural cash-inflow story.

**Land the point:** Now Treasury can walk into the cash call with the same inflow concentration view the Controller uses — no more pre-meeting reconciliation between the cash management system and the GL close.

### Question (Act 1.2)

> **Show monthly free cash flow by segment for the trailing 12 months.**

**What to say while it runs:** Monthly free cash flow by segment over 12 months. Free cash flow is the metric that funds the dividend and the buyback. The segment cut tells you whether Upstream is carrying the FCF profile alone or whether Downstream and Midstream are contributing — and that mix matters because Upstream FCF is the most price-exposed.

**What to look for:** Monthly total free_cash_flow_usd by segment — DATE_TRUNC('month', kpi_month). Watch for segments going opposite directions; divergence is the leading signal of which segment carries dividend defense in the next downcycle.

**Land the point:** When the same segment FCF curve sits with Treasury, Corporate Finance, and the CFO, the dividend-coverage conversation stops being a reconciliation and starts being a capital-return conversation.

---

## Act 2 — Collect, stretch, or hold — locking the working-capital levers *(≈4 min)*

**Persona:** Corporate Controller • **Job to be done:** Commit to the specific working-capital actions for the quarter — which BUs get JIB/AR pressure, which get payables-stretch room, and which get inventory protection.

*Three questions that turn the working-capital picture into a defensible action list. The middle question — cash-conversion cycle in Downstream — is the anchor that quantifies how many days of working capital are actually on the table.*

### Question (Act 2.1)

> **Which business units have DSO above 45 days, and what is their accounts receivable balance?**

**What to say while it runs:** Business units with DSO above 45 days, with their AR balance. IOC benchmark DSO is 30-45 days; anything materially above 45 is a JIB or counterparty timing problem, not a credit policy issue. The AR balance alongside is what tells Treasury whether it's a $5M conversation or a $50M conversation.

**What to look for:** Table of business units with dso_days > 45 showing accounts_receivable_usd. Sort descending. The top 3 or 4 rows are the BUs the Corporate Controller has to assign a collection lead to this quarter.

**Land the point:** That list used to be the output of a week of close-pack rollup. Now it's the input to the JIB collection sprint that actually moves dividend headroom.

### Question (Act 2.2)

> **What is the trend in cash conversion cycle month-over-month across the Downstream segment?**

**What to say while it runs:** Cash conversion cycle month-over-month across Downstream. Cash conversion cycle is DSO plus DIO minus DPO — the number of days working capital is locked up before it converts to cash. For Downstream specifically, inventory is the largest lever because refined-product inventory turns over weekly. A CCC that's drifting up in Downstream means inventory is building or AR is stretching, both of which compress liquidity.

**What to look for:** Monthly cash_conversion_cycle_days trend filtered to Downstream segment. Watch for sustained upward drift — that's the leading indicator the Treasurer cares about before it shows up in net debt.

**Land the point:** When the Downstream CCC trend is on the Controller's screen quarterly — not annually — the working-capital conversation moves from reactive to programmatic. That's the difference between a one-off year-end sweep and a quarterly discipline.

> **Anchor moment.** Stop on the DSO list and the Downstream CCC curve together. Pick the worst-offender BU — call it an Upstream unit running 55 days DSO with $400M in AR, against a 35-day target.

> *55 versus 35 days of DSO on $400M of AR is roughly $145M of working capital trapped that doesn't need to be — at CashFlow's scale of $40B revenue, that's about 0.4% of revenue stuck in receivables timing. Bringing that BU back to a 40-day DSO frees roughly $110M of cash. Run the same lens across the 4-5 BUs currently above 45 days and you're looking at $300-500M of one-time working capital release. Pair that with a 5-day payables stretch on the Downstream OPEX base ($8B) — another $110M of DPO benefit — and the integrated portfolio has roughly $400-600M of cash freed up. That's a dividend installment, or one buyback tranche, in working-capital optimization alone.*

> That's the dividend-funding conversation this space converts from an annual sweep into a quarterly action plan. The lever isn't a financing decision — it's a working-capital discipline, executed BU by BU, against the same governed view.

### Question (Act 2.3)

> **Top 10 business units by net debt — and how does that compare to their cash balance?**

**What to say while it runs:** Top 10 business units by net debt with their cash balance alongside. Net debt is the leverage metric the rating agencies watch; the cash balance is what tells you how much head-room each BU has against intercompany funding. A BU running high net debt with low cash is the next funding ask — and a BU with high cash relative to net debt is a candidate for intercompany sweep.

**What to look for:** Top 10 by net_debt_usd with cash_balance_usd as a comparison column. Watch for asymmetry — BUs whose net debt is high but cash balance is high are intercompany-funding targets, not external-borrowing candidates.

**Land the point:** Net debt and cash side-by-side, across 20 BUs, in one query. That's the conversation that turns intercompany funding from an ad-hoc Treasury exercise into a quarterly portfolio sweep.

---

## Act 3 — The dividend defense — taking the recommendation to the CFO *(≈4 min)*

**Persona:** Divisional Finance Lead (Upstream) • **Job to be done:** Defend the segment's FCF contribution and surface the BUs whose FCF is structurally negative so capital allocation can be re-balanced.

*The Divisional Finance Lead's job is to defend Upstream's FCF story before it goes to the CFO and on to the Board. The negative-FCF screen and the AP trend are the two views that frame the structural conversation.*

### Question (Act 3.1)

> **Which business units have negative free cash flow this year, and by how much?**

**What to say while it runs:** Business units with negative free cash flow this year, and by how much. Negative FCF in any segment is the Board's first question on the capital-return slide. The 'by how much' matters because a BU $50M negative may be a one-time investment-cycle issue; a BU $250M negative is a structural problem and a capital-allocation re-balance.

**What to look for:** Table of business units with free_cash_flow_usd < 0 showing the magnitude. Sort ascending (most negative first). Watch which segment carries the worst — that's the segment that has to defend its capital allocation in the next planning cycle.

**Land the point:** Negative-FCF BUs by name and magnitude, in one query. That's the difference between the CFO walking into the Board with a recommendation and walking in with a list of things to investigate.

### Question (Act 3.2)

> **How has total accounts payable trended month-over-month by segment?**

**What to say while it runs:** Total accounts payable month-over-month by segment. AP trend is the cleanest read on payables-stretch discipline. If AP is climbing faster than activity-driven growth, you're stretching suppliers; if AP is compressing, you're paying faster than you need to. For IOCs in a dividend-defense posture, sustained AP growth at the segment level is a deliberate working-capital lever — but only if it's measured.

**What to look for:** Monthly total_payables_usd by segment. Watch which segment is leaning hardest on payables stretch — that's the segment that has the most working-capital optionality (and the most supplier risk if it stretches further).

**Land the point:** Segment-level AP trend, governed, every cycle. That's how Treasury defends the payables-stretch policy to the CFO without losing the conversation to a supplier-risk objection.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CashFlow Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 business units by total cash inflows over the last 90 days.
2. Show monthly free cash flow by segment for the trailing 12 months.
3. Which business units have DSO above 45 days, and what is their accounts receivable balance?
4. What is the trend in cash conversion cycle month-over-month across the Downstream segment?
5. Top 10 business units by net debt — and how does that compare to their cash balance?
6. Which business units have negative free cash flow this year, and by how much?
7. How has total accounts payable trended month-over-month by segment?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
