# AeroCapital Finance — Demo Script

**Space:** Aerospace — AeroCapital Finance - Working Capital & Cash Flow 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Program Finance Lead, Treasury Lead
**KPIs touched:** Days Sales Outstanding, Days Payable Outstanding, Cash Conversion Cycle, Free Cash Flow by program, Operating Cash Flow, WIP inventory
**Big decision automated:** Which programs to escalate for cash recovery this quarter and which to renegotiate payment terms on — to defend free cash flow guidance at the next earnings call.

---

## Pre-demo checklist

- Open the Genie space `AeroCapital Finance - Working Capital & Cash Flow 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroCapital Finance manages working capital across 20 aerospace programs spanning 5 program types — Production, Military, Aftermarket, Development, and Space. Today the program-level receivables aging lives in the Program Finance Lead's Oracle extract, the DSO/DPO/CCC snapshot lives in Treasury's weekly liquidity workbook, and the free-cash-flow guidance defense lives in the CFO's Street-facing model that gets rebuilt before every earnings call. Three artifacts, same 20 programs — and the cash-recovery escalation list gets driven by whichever finance partner spoke up last, not by where the cash is actually trapped. This space ends that. One governed surface where AR, AP, WIP, DSO, DPO, CCC, and overdue receivables sit together, so the cash-recovery and payment-terms decisions become a defensible quarterly cycle, not a reactive scramble before the close.

---

## Key KPIs in scope

- Days Sales Outstanding (DSO) — A&D benchmark 60-90 days (long contract cycles)
- Days Payable Outstanding (DPO) — typical 45-60 days
- Cash Conversion Cycle (CCC) — best-in-class A&D <90 days, average 120-150 days
- Free Cash Flow (USD) by program
- Operating Cash Flow (USD) — top CFO scorecard metric
- WIP inventory (USD) — major working-capital lever in long-cycle programs
- Overdue receivables % (target <5%)
- Working capital ratio (current assets / current liabilities; target 1.5-2.0)

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **WIP** | Work In Process |

---

## Act 1 — The signal — finding the cash trapped in receivables before the close window *(≈4 min)*

**Persona:** Program Finance Lead • **Job to be done:** Identify which programs are carrying the most receivables exposure and which counterparties are slipping payment terms — before quarter-end.

*This is the moment the cash-recovery escalation list starts forming. Two queries in, the program finance lead already has the receivables that need a collections call this week and the programs whose DSO is structurally drifting.*

### Question (Act 1.1)

> **Top 10 programs by accounts receivable balance — and what is their DSO?**

**What to say while it runs:** Top 10 programs by accounts receivable balance with their DSO. A&D benchmark on DSO is 60-90 days because of long contract cycles — but anything over 120 days is a structural collections problem, not a contract-cycle artifact. The ranking IS the cash-recovery priority list.

**What to look for:** A ranked table of 10 programs by total_receivables with avg_dso alongside. The room should see that one or two programs usually carry disproportionate AR — those are the dollars worth a finance partner's afternoon.

**Land the point:** Right there is the cash-recovery shortlist. The program finance lead can name three programs that earn an escalation call this week — and the conversation with the customer moves from 'we're behind' to 'here are the invoices, here are the dates, here's the recovery plan.'

### Question (Act 1.2)

> **Show monthly trend in net cash flow by program type over the trailing 12 months.**

**What to say while it runs:** Now monthly net cash flow by program type over 12 months. The shape of each program-type line is the cash-conversion story — Production should be steady, Military lumpy by contract milestone, Development typically negative, Aftermarket the most cash-positive. Anything breaking that pattern is the diagnostic anchor.

**What to look for:** Monthly net_cash_flow by program_type using `DATE_TRUNC('month', ...)`. Watch for program types where the line is breaking against the expected shape — those are the programs needing a cash-flow forecast revision.

**Land the point:** Before this space, that chart was a monthly artifact for the treasury review. Now it's the program finance lead's first question of the morning — and the conversation about which programs need payment-term renegotiation starts a quarter earlier.

---

## Act 2 — The decision — escalating these programs, renegotiating those terms, freeing the trapped WIP *(≈4 min)*

**Persona:** Treasury Lead • **Job to be done:** Commit to a cash-recovery escalation list, a payment-terms renegotiation list, and a WIP-burndown plan — naming exactly where Treasury and the program teams put their hours.

*Three questions that turn the receivables watchlist into a defensible cash-recovery action plan. The middle question is the anchor — converting WIP and CCC exposure into the free-cash-flow dollars the CFO can defend on the earnings call.*

### Question (Act 2.1)

> **Which program types have the worst cash conversion cycle, and what is the WIP exposure?**

**What to say while it runs:** Program types with the worst cash conversion cycle and their WIP exposure. Best-in-class A&D CCC is below 90 days; industry average is 120-150. Anything above 180 means the program is funding the customer's inventory. WIP alongside CCC tells you whether the lever is collections (high AR) or production (high WIP).

**What to look for:** Program types ranked by avg_ccc with total_wip_inventory alongside. The combination tells you whether the recovery is a collections call or a production-acceleration conversation.

**Land the point:** That ranking is the working-capital action plan. Two queries in, Treasury has a defensible recommendation — and the conversation moves from 'CCC is too high' to 'here's the WIP we can ship this quarter, here's the receivables we can pull in.'

### Question (Act 2.2)

> **Top 10 counterparties by total inflows in the last 12 months.**

**What to say while it runs:** Top 10 counterparties by total inflows over 12 months. This is the counterparty-concentration view — if one or two counterparties carry 50%+ of inflows, that's both a relationship-management priority and a counterparty-risk conversation for Treasury.

**What to look for:** Counterparties ranked by total_inflows. Watch for concentration — that's the relationship that earns a CFO-level QBR before any payment-terms conversation.

**Land the point:** That table is the counterparty-strategy view. The CFO and Treasury now know which 3 counterparties to invest the relationship hours in, and which can absorb tighter payment terms without strategic damage.

> **Anchor moment.** Park on the CCC-and-WIP view. Pick the worst program type — say Development programs running at 195-day CCC with $180M of trapped WIP across the portfolio.

> *Pulling CCC from 195 days to the A&D best-in-class 90 days frees roughly 105 days of working capital. On $180M of WIP that's roughly $180M × (105/195) ≈ $97M of cash released from that program type alone. At AeroCapital's cost of capital — call it 6% — that's $5.8M per year of avoided carry. More importantly, that's $97M of cash the CFO can deploy into program capex, share buyback, or debt paydown without going to the credit markets. Across all 5 program types, even a partial CCC compression of 30-40 days unlocks $50-100M of one-time cash plus $3-6M of annual recurring carry savings.*

> That's the decision this space defends. The cash-recovery list, the payment-terms renegotiation list, and the WIP-burndown target get written from the same view. The CFO walks into the earnings call defending the FCF guidance with program-level math, not with a 'we're working on it.'

### Question (Act 2.3)

> **How has free cash flow trended month-over-month by program type?**

**What to say while it runs:** Programs with the highest overdue receivables percentage right now. Target is below 5%; anything above 10% is structural. The point isn't the list — it's that the list is the escalation queue for the next two weeks.

**What to look for:** Programs ranked by overdue_receivables_pct above 5%. The point is which programs are blocking cash from converting — those are the escalation priorities.

**Land the point:** That comparison is the difference between knowing receivables are old and knowing exactly which programs to escalate. The first is a metric; the second is a Friday-afternoon collections call.

---

## Act 3 — The commitment — defending free cash flow guidance to the Street and locking next-year payment policy *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the free-cash-flow guidance to the Street and lock in next-year payment-terms policy with the top counterparties.

*The CFO doesn't need a new model — they need the same DSO, CCC, and FCF numbers Treasury and the program teams are acting on, packaged for the earnings call and the audit committee.*

### Question (Act 3.1)

> **Which programs have the highest overdue receivables percentage right now?**

**What to say while it runs:** Free cash flow trend by program type over 12 months. This is the line the Street tracks. Production and Aftermarket FCF growing, Development burning to plan, Military lumpy — that's the right shape for an A&D narrative. The inverse is a guidance problem.

**What to look for:** Monthly free_cash_flow_usd by program_type. Watch the Aftermarket and Production lines — those are the lines that defend the FCF guidance the Street modeled in.

**Land the point:** When the CFO can pull this view live in front of the audit committee, the FCF defense becomes a program-by-program story instead of a single consolidated number. That's how guidance gets defended, not just delivered.

### Question (Act 3.2)

> **Show monthly trend in total WIP inventory across all programs for the trailing 12 months.**

**What to say while it runs:** Monthly WIP inventory trend across all programs. WIP is the single biggest working-capital lever in long-cycle aerospace. Declining WIP with stable revenue means the production system is converting faster; rising WIP with stable revenue means cash is getting trapped. The slope is the policy signal.

**What to look for:** Monthly total_wip_inventory across all programs. Rising slope = a working-capital problem in formation; declining slope = the CCC improvements are landing.

**Land the point:** Program finance, Treasury, and the CFO now share one view. The cash-recovery plan, the payment-terms policy, and the FCF guidance are written from the same numbers. One space. One cash story. Same answers from the program room to the earnings call.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroCapital Finance — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 programs by accounts receivable balance — and what is their DSO?
2. Show monthly trend in net cash flow by program type over the trailing 12 months.
3. Which program types have the worst cash conversion cycle, and what is the WIP exposure?
4. Top 10 counterparties by total inflows in the last 12 months.
5. How has free cash flow trended month-over-month by program type?
6. Which programs have the highest overdue receivables percentage right now?
7. Show monthly trend in total WIP inventory across all programs for the trailing 12 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
