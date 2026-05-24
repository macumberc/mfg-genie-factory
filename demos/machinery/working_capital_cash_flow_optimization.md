# CapitalFlow Machinery — Demo Script

**Space:** Machinery — CapitalFlow Machinery - Working Capital Optimization 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Treasurer, AR/AP Lead, CEO partner
**KPIs touched:** Cash Conversion Cycle, DSO, DPO, Net Working Capital, Operating cash flow, Free cash flow
**Big decision automated:** Which 2-3 business units get tighter DSO targets next quarter, which suppliers to renegotiate payment terms with, and how much aged inventory to take a write-down on before year-end.

---

## Pre-demo checklist

- Open the Genie space `CapitalFlow Machinery - Working Capital Optimization 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CapitalFlow Machinery manages working capital across multiple business units in a capital-intensive industrial portfolio. Today the AR team chases collections from a daily aged-trial-balance spreadsheet, the AP team manages payment timing in a SAP screen nobody else can see, and the Treasurer rolls up DSO, DPO, and CCC into a monthly cash deck for the CFO. The result: by the time the CFO sees that Business Unit X's DSO has slipped from 42 to 58 days, $30M of cash is already trapped — and the call on whether to tighten credit, push out a payment, or write down obsolete inventory gets made on whichever number leadership saw most recently. This space ends that. One governed view where transaction-level days outstanding, monthly DSO/DPO, and forecast variance all reconcile against the same BUs — so the trapped-cash conversation happens before the quarter closes, not after.

---

## Key KPIs in scope

- Cash Conversion Cycle (days) — industrial machinery benchmark 60–120 days, leaders <60
- DSO (Days Sales Outstanding) — target <45 days B2B industrials
- DPO (Days Payable Outstanding) — leverage 45–75 days without supplier strain
- Net Working Capital ($) — capital efficiency lever
- Operating cash flow ($) — core business health
- Free cash flow ($) — capex/dividend coverage
- AR collection rate (%) — target ≥98%
- Cash flow forecast variance (%) — accuracy target <5%

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CEO** | Chief Executive Officer |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — where is cash trapped, and how much is it costing us? *(≈4 min)*

**Persona:** Treasurer • **Job to be done:** Identify before the weekly cash meeting which business units are dragging the Cash Conversion Cycle and how that maps to operating cash flow.

*This is the moment the weekly cash-position call gets prepared. Two questions in, the Treasurer has the BU-level CCC ranking and the operating-cash-flow trend that used to require a Monday pivot from SAP exports.*

### Question (Act 1.1)

> **Top 10 business units by Cash Conversion Cycle days — where is cash trapped longest?**

**What to say while it runs:** Business units ranked by Cash Conversion Cycle days. Industrial machinery benchmark is 60-120 days; leaders run under 60. Any BU above 120 days is sitting on trapped cash measured in tens of millions — that's not an AR problem, that's a structural working-capital problem.

**What to look for:** Ranked table from `working_capital_snapshots` with `cash_conversion_cycle_days` by `business_unit_type`. Eye lands on the BUs above 120 — those are the ones whose finance lead needs to be in next week's meeting. Click *Show generated code* once so the room sees the governed measure firing.

**Land the point:** That ranking is the trapped-cash conversation. Before this space, it took 4 days after month-end to even know the number; now the Treasurer can pull it on a Monday morning and the call on tightening BU credit is grounded in current data, not last month's.

### Question (Act 1.2)

> **What is the monthly trend in operating cash flow vs free cash flow over the trailing 12 months?**

**What to say while it runs:** Monthly trend in operating cash flow vs free cash flow. The gap between them is capex — when that gap widens, the business is reinvesting; when it narrows, the business is harvesting. Either is fine, *if it's intentional*. Unintentional narrowing is the warning sign.

**What to look for:** Two trend lines from `cash_flow_kpi_metrics`: `total_operating_cf` and `total_free_cash_flow`, monthly over 12 months. Watch for the months where the free-cash-flow line dips below operating — that's where capex spiked or working capital got worse.

**Land the point:** Before this space, that two-curve view was a chart the FP&A team built once a quarter. Now the CFO walks into the board meeting having already pre-empted the question about why FCF dropped — because they've been watching the leading indicators all along.

---

## Act 2 — The decision — DSO levers, payment-terms negotiation, and the write-down call *(≈4 min)*

**Persona:** AR/AP Lead • **Job to be done:** Commit on which BUs get tighter DSO targets, which suppliers to push for extended payment terms, and how much aged inventory to take a write-down on this cycle.

*Three questions that turn the daily AR/AP grind into a defensible working-capital strategy. The middle question is the anchor — the DSO-improvement-to-cash conversion that funds the next year's growth without new debt.*

### Question (Act 2.1)

> **Which business units have DSO above the 45-day target, and what is the outstanding AR balance?**

**What to say while it runs:** Business units with DSO above the 45-day target, and the outstanding AR balance on each. B2B industrial best-practice is 35-45 days; anything above 60 days on a non-distressed customer base is a credit-policy or collections-process failure, not a customer problem.

**What to look for:** From `working_capital_snapshots`, BUs filtered to `dso_days > 45` with `accounts_receivable_usd` next to them. The combination matters — high DSO and high AR balance is the cash-trap concentration; you fix that BU first.

**Land the point:** That table used to be the output of a half-day of cross-referencing aged trial balances. Now it's the first item on the weekly cash call — and the call on which BU gets a tighter credit policy is grounded in dollars, not anecdote.

### Question (Act 2.2)

> **Rank business unit types by AR collection rate — which are below the 98% target?**

**What to say while it runs:** Business-unit types ranked by AR collection rate against the 98% target. Collection rate under 98% means cash is leaking somewhere — either bad debt, dispute write-offs, or a customer base trending sideways. Each of those is a different fix.

**What to look for:** Ranked BU types by `avg_collection_rate` from `cash_flow_kpi_metrics`. Watch for BU types below 95% — those are the ones where the gap between revenue and collected cash is structurally widening.

**Land the point:** Same space, same numbers — when the AR team can show *which* BU type is bleeding collections, the conversation with the BU GM stops being 'try harder' and starts being 'here's the customer cohort that needs a payment plan or a write-off.'

> **Anchor moment.** Hold on the BU-level DSO view and the NWC trend. Pick the worst BU — say, $120M annual revenue, current DSO of 62 days, target 45 days.

> *Daily revenue on $120M is $329K. A 5-day DSO improvement at this BU is 5 × $329K = $1.6M of cash released. The 17-day gap to target is roughly $5.6M of trapped cash on one BU. Now scale: across the portfolio at CapitalFlow's revenue base, a 5-day DSO improvement across all BUs is typically $15-25M of one-time cash released. Layer the DPO negotiation play — extending payment terms by 10 days on $200M of payables is another $5.5M of working capital — and the write-down call on aged inventory: even a 50% write-down on a $20M slow-mover bucket reclassifies $10M of carrying value out of working capital. The combined play is a $25-40M cash release without taking on new debt.*

> That's the decision this space automates. Not the monthly cash deck. The decision. The DSO target gets tightened on the BU where the math says it has to be, the supplier-payment-terms negotiation calendar is set on the AP side, and the year-end write-down conversation lands in October instead of December.

### Question (Act 2.3)

> **Show monthly trend in net working capital across all business units.**

**What to say while it runs:** Monthly trend in net working capital across the business units. NWC is the headline cash-trap number. When it climbs, cash is going into AR, inventory, or pre-paid expenses; when it drops, cash is being released. The shape of this curve is what determines whether we need a new credit line this year — or whether we have $30M to fund a tuck-in acquisition without raising any.

**What to look for:** From `cash_flow_kpi_metrics`, `total_working_capital` trend monthly, 12 months. Watch for the inflection — a sustained climb in NWC over 2-3 months is the early warning that something on the operations side is degrading.

**Land the point:** When NWC is on a governed surface the CFO and Treasurer both query, the conversation about the next debt facility moves from a panicked Q3 ask to a structured Q1 decision.

---

## Act 3 — The commitment — the CFO's working-capital plan and the cash forecast *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the working-capital trajectory to the CEO and board, lock in next year's cash plan, and commit on the BU-level DSO and write-down targets.

*The CFO has to tell the board a credible story about cash generation, working-capital efficiency, and the trapped-cash recovery program. The forecast variance and the operational levers have to land in the same conversation.*

### Question (Act 3.1)

> **Top 10 transactions by days outstanding — where should the collections team focus?**

**What to say while it runs:** Top 10 transactions by days outstanding. This is the collections-team focus list — the longest-aged invoices that haven't moved. Industry rule: invoices over 90 days outstanding have a 25% chance of becoming bad debt; over 180 days it's closer to 70%.

**What to look for:** From `cash_flow_transactions`, top 10 by `days_outstanding`, filtered to `direction = 'Inflow'`. Look at `amount_usd` next to it — the largest aged invoices are the ones to chase first, regardless of which BU they're under.

**Land the point:** That list used to be a heroic spreadsheet a senior collector built each Monday. Now it's the first slide of the weekly working-capital review — and the conversation about which customers move to legal collections is grounded in transaction-level evidence.

### Question (Act 3.2)

> **Which business units have the worst cash flow forecast variance, and what is the dollar impact?**

**What to say while it runs:** Business units with the worst cash flow forecast variance, and the dollar impact. Industry best-practice forecast variance is under 5%; anything above 10% means the forecast model is broken for that BU and the CFO's commitment to the board is wishful thinking.

**What to look for:** From `cash_flow_kpi_metrics`, BUs ranked by `total_forecast_variance_percent` with `total_net_cash_flow` next to it. The eye should land on BUs where the dollar impact of the variance is largest — those are the ones to rebuild the forecast for first.

**Land the point:** Same space, same numbers — the Treasurer's weekly cash position and the CFO's quarterly board narrative are now the same artifact. The cash forecast moves from a number people debate to a number people trust, and the next debt facility — or the next dividend increase — gets decided on evidence, not on instinct.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CapitalFlow Machinery — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 business units by Cash Conversion Cycle days — where is cash trapped longest?
2. What is the monthly trend in operating cash flow vs free cash flow over the trailing 12 months?
3. Which business units have DSO above the 45-day target, and what is the outstanding AR balance?
4. Rank business unit types by AR collection rate — which are below the 98% target?
5. Show monthly trend in net working capital across all business units.
6. Top 10 transactions by days outstanding — where should the collections team focus?
7. Which business units have the worst cash flow forecast variance, and what is the dollar impact?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
