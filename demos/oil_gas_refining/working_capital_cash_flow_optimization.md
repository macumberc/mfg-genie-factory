# RefineCapital Systems — Demo Script

**Space:** Oil & Gas Refining — RefineCapital Systems - Working Capital & Cash Flow Optimization 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Treasurer, Controller, CFO
**KPIs touched:** Cash conversion cycle, Days Sales Outstanding, Days Payable Outstanding, Free cash flow by segment, Current ratio, Net debt and net debt / EBITDA leverage
**Big decision automated:** Which 2-3 segments get an immediate AR collections push, how much crude-inventory length to carry through the next crack-spread cycle, and which payables terms get renegotiated this quarter to fund the year's growth capex without touching the revolver.

---

## Pre-demo checklist

- Open the Genie space `RefineCapital Systems - Working Capital & Cash Flow Optimization 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RefineCapital Systems runs working capital and cash flow analytics across 20 business units spanning Processing, Supply Chain, Support, and Corporate segments. Today the daily cash position lives in Treasury's bank-balance workbook, the DSO and AR aging live in the Controller's collections file, and the inventory-tied-up number gets pulled monthly from a separate Supply Chain rollup that nobody reconciles to the GL. Three artifacts, three update cadences — so the cash conversion cycle, the crude-inventory positioning call, and the AR collections priority all live in different rooms. The result is working capital trapped in receivables that should have been collected, and inventory length carried into compressing crack spreads that should have been worked down. This space ends that. Cash flows, working-capital snapshots, and KPI trends all answer the same question: *how much cash do we free this quarter, and where do we deploy it.*

---

## Key KPIs in scope

- Cash conversion cycle (days) — refining peers typically run 15-40 days NWC
- Days Sales Outstanding (DSO) — integrated refiners target 25-35 days
- Days Payable Outstanding (DPO) — typically 30-50 days
- Free cash flow ($) by segment
- Current ratio — healthy refiners run 1.2-1.8
- Net debt ($) and net debt / EBITDA leverage
- Inventory tied up in feedstock and product (bbl converted to $)
- Net cash flow (inflows − outflows) by business unit

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |

---

## Act 1 — The signal — surfacing the cash leaks and the segment-level cash gap before Treasury's morning position *(≈4 min)*

**Persona:** Treasurer • **Job to be done:** Land the daily cash position and the week-ahead funding view without rebuilding the bank-balance workbook against four different source extracts.

*This is the moment the daily cash position takes shape. Two questions in, the Treasurer already has the segment ranking that used to take an hour of Excel against the bank-balance file and the Supply Chain rollup.*

### Question (Act 1.1)

> **Top 10 business units by net cash flow over the last 12 months.**

**What to say while it runs:** Net cash flow by business unit is where the conversation starts. Refining peers run 15-40 days of net working capital through-cycle — anything materially outside that band is either trapped cash or unsustainable extension on a supplier.

**What to look for:** Top 10 business units by `net_cash_flow_usd` over 12 months. The shape — most positive, a few notably negative — is the cash-deployment skeleton.

**Land the point:** Now the Treasurer can isolate the segments dragging the company's free cash flow in minutes — that's the AR-push and inventory-action conversation that used to wait for the monthly Treasury review.

### Question (Act 1.2)

> **Show monthly trend of total free cash flow across the company for the trailing 12 months.**

**What to say while it runs:** Free cash flow trend month-over-month is the chart the CFO defends to the board. A 200 KBD refiner generates a wide free-cash-flow range across the cycle — and the curve direction matters more than the snapshot. If FCF is bending down two months in a row, the question is whether it's crack-spread compression (recoverable) or working-capital trapped in inventory (operational).

**What to look for:** Monthly bars of free cash flow over 12 months — `DATE_TRUNC('month', ...)`. Watch for the months where the trend slipped against where crack spreads were going.

**Land the point:** Before this space, that chart was rebuilt for the monthly board pack. Now it's the Treasurer's first question of the day — and the CFO sees the same FCF view, in real time, before the close period locks.

---

## Act 2 — The decision — AR collections push, crude inventory positioning, and the payables renegotiation list *(≈4 min)*

**Persona:** Controller • **Job to be done:** Commit the collections plan for the quarter, lock the crude-inventory positioning against the crack-spread forecast, and rank the suppliers for terms renegotiation.

*Three questions that turn the working-capital snapshot into a defensible cash-release plan. The middle question is the anchor — AR balance translated into freed working capital.*

### Question (Act 2.1)

> **Which business units have DSO greater than 45 days — driving working capital trapped in receivables?**

**What to say while it runs:** DSO above 45 days is the bright-line working-capital flag. Integrated refiners target 25-35 days DSO. Anything materially above 45 is working capital trapped in receivables — and the *which counterparties* answer is where the collections push gets aimed.

**What to look for:** A table of business units where `avg_dso_days > 45`. The shape — typically one or two segments well above the target — is what the collections-push effort gets sized against.

**Land the point:** That list used to be reconstructed monthly from the Controller's collections workbook. Now it's the input to the credit and collections meeting that happens at 8 AM Monday.

### Question (Act 2.2)

> **Top 10 business units by total accounts receivable balance right now.**

**What to say while it runs:** Top business units by accounts receivable balance right now is the *where is the cash sitting* view. On a refiner our size, a $50M AR balance trapped at 50 DSO instead of 30 DSO is $20M of cash sitting outside the company. That's growth capex without touching the revolver — if we can move the DSO needle.

**What to look for:** Top 10 business units by `total_receivables_usd`. Stack against the DSO list — the units that show up in both are the ones where the collections push has both the dollars and the days to compress.

**Land the point:** When the Treasurer, the Controller, and the CFO all see the same AR-balance ranking, the conversation stops being about whose collections file is most current and starts being about *which counterparties get the collections push this quarter*.

> **Anchor moment.** Stop on the AR-balance ranking. Pick the top three business units — call them collectively $200M of accounts receivable balance against a 50-day DSO baseline, on a 30-day target.

> *$200M of AR at 50 DSO compressed to the 30-day target frees roughly $80M of cash — directly, immediately, no revolver draw. Now layer the crude-inventory positioning call: $1/BBL on a 1M BBL crude position is $1M of working capital, and most refiners can flex 1-3M BBL of length across a crack-spread cycle. Work down 2M BBL of crude length at $70/BBL when crack spreads are compressing and that's $140M of working capital reclaimed. Combined cash release in the room: $200M+ — at a 6% cost of capital that's $12M/year of interest savings, plus the avoided revolver draw, plus the ability to fund this year's growth capex without touching the credit line.*

> That's the decision this space automates. Not the working capital slide. The collections-push list, the crude-inventory positioning call, and the supplier-terms renegotiation queue — all on the same data the CFO defends to the board.

### Question (Act 2.3)

> **How has the cash conversion cycle trended month-over-month by segment?**

**What to say while it runs:** Cash conversion cycle by segment month-over-month is the direction number — and the leading indicator for whether next quarter's free cash flow holds. Through-cycle refining peers manage 15-40 days NWC. A segment drifting from 20 days to 35 days over two quarters is the candidate for a structural review *before* it shows up in the year-end print.

**What to look for:** Monthly trend of cash conversion cycle by segment. The inflection months tell you when DSO, DPO, or inventory broke the working-capital envelope.

**Land the point:** That direction view is the difference between a clean Treasury board pack and a board pack that gets re-cut at midnight.

---

## Act 3 — The commitment — locking the liquidity narrative and the leverage defense for the executive committee *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the company's liquidity and leverage story to the board and lock the working-capital plan for the next two quarters.

*The CFO doesn't need a new Treasury dashboard; they need the same numbers the Treasurer and the Controller are already acting on, in the same language, so the board liquidity narrative writes itself.*

### Question (Act 3.1)

> **Which segments have a current ratio below 1.0 — signaling liquidity risk?**

**What to say while it runs:** Current ratio below 1.0 is a hard liquidity flag. Healthy refiners run 1.2-1.8 — anything sliding toward 1.0 is the conversation rating agencies want to have *before* the next bond cycle. The segment-level view tells you whether it's structural or a working-capital timing issue.

**What to look for:** Segments ranked on current ratio. Anything below 1.2 is yellow zone, below 1.0 is red. The shape determines whether this is a covenant-management problem or a one-segment operating problem.

**Land the point:** When that ranking is in the CFO's hand a quarter before the next rating-agency review, the liquidity conversation moves from reactive to programmatic — and the executive team stops getting surprised by the credit committee.

### Question (Act 3.2)

> **What is total inventory tied up by segment, and how has it changed quarter-over-quarter?**

**What to say while it runs:** Inventory tied up by segment quarter-over-quarter is the crude-positioning conversation. On a 200 KBD refiner, every million barrels of crude length is roughly $70M of working capital at $70/BBL. The QoQ delta tells you whether we're building length into compressing crack spreads — exactly the wrong moment.

**What to look for:** Segments on `total_inventory` with the QoQ change drawn. Watch for the segments building length when crack spreads are forecast to compress — those are the candidates for an immediate inventory work-down.

**Land the point:** Daily cash position at 8 AM, working-capital plan at 10 — same space, same numbers. The Treasurer's daily position, the Controller's collections plan, and the CFO's board liquidity narrative are now the *same artifact* — and the executive team gets one cash story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RefineCapital Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 business units by net cash flow over the last 12 months.
2. Show monthly trend of total free cash flow across the company for the trailing 12 months.
3. Which business units have DSO greater than 45 days — driving working capital trapped in receivables?
4. Top 10 business units by total accounts receivable balance right now.
5. How has the cash conversion cycle trended month-over-month by segment?
6. Which segments have a current ratio below 1.0 — signaling liquidity risk?
7. What is total inventory tied up by segment, and how has it changed quarter-over-quarter?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
