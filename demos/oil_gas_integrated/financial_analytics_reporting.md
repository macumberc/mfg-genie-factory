# PetroLedger Corp — Demo Script

**Space:** Oil & Gas Integrated — PetroLedger Corp - Financial Analytics & Reporting 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO and Divisional VPs + FP&A Director, Controllership Lead, Upstream / Downstream Divisional Controller
**KPIs touched:** Revenue, EBITDA, Operating margin, ROIC, OPEX per BOE, Budget variance
**Big decision automated:** Which divisions (Upstream / Downstream / Midstream / Corporate) get over- vs. under-invested in the next planning cycle, and which cost centers carry budget cuts vs. budget protection ahead of the Q-close board read.

---

## Pre-demo checklist

- Open the Genie space `PetroLedger Corp - Financial Analytics & Reporting 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PetroLedger Corp runs 20 cost centers across Upstream, Downstream, Midstream, and Corporate — roughly $40B of annual revenue, $25B of OPEX, and a $6B capex program. Today the revenue-vs-plan pull comes out of the FP&A consolidation deck refreshed every Friday in Excel, OPEX variance is reconciled in SAP cost-center hierarchies by Controllership, and OPEX-per-BOE benchmarks live in the Upstream divisional VP's monthly book. Three artifacts, three teams, and the CFO walks into the quarterly close with three slightly different reads on which division is actually carrying earnings. This space converts the consolidation into a single governed question — revenue, EBITDA, operating margin, ROIC, OPEX/BOE, budget variance — answered the same way every time, by every team, with the same definition of division.

---

## Key KPIs in scope

- Revenue ($MM) — top-line, actual vs. planned
- EBITDA ($MM) — earnings before interest, taxes, depreciation, amortization
- Operating margin (%) — IOC top-quartile >20% in mid-cycle environments
- ROIC (%) — capital efficiency; IOC target 8-12%
- OPEX per BOE ($/BOE) — lifting cost benchmark; majors target <12 $/BOE upstream
- Budget variance (%) — actual vs. plan at cost center / GL category
- Total CAPEX ($MM) — capital deployed by division
- G&A spend ($MM) — overhead trend

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **BOE** | Barrels of Oil Equivalent |
| **CAPEX** | Capital Expenditure |
| **CFO** | Chief Financial Officer |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |
| **OPEX** | Operating Expense |

---

## Act 1 — The pulse — where revenue and EBITDA are actually landing this cycle *(≈4 min)*

**Persona:** FP&A Director • **Job to be done:** Get a clean picture of which cost centers are carrying the revenue print and how divisional EBITDA is trending before the close meeting starts.

*This is the FP&A Director's pre-close working session — the one that used to be spent refreshing the consolidation. Two questions in, the cost-center ranking and the divisional EBITDA curve are on screen.*

### Question (Act 1.1)

> **Top 10 cost centers by total actual revenue this year.**

**What to say while it runs:** Cost centers ranked by total actual revenue this year. The point isn't who's on top — Upstream production cost centers will always lead. The point is the bottom of the list, where Corporate and shared-services cost centers sit. If a cost center is consuming budget but not generating attributable revenue, the divisional VP needs to defend it in the close.

**What to look for:** A ranked table of 10 cost centers with total amount_usd where account_type = Revenue. Look at the spread — the top one or two cost centers carry an outsized share, which is the concentration risk story FP&A has to tell upstream.

**Land the point:** Now the FP&A Director can walk into the close with the same numbers the divisional controllers will quote — no more pre-meeting reconciliation calls just to align on what the revenue print actually is.

### Question (Act 1.2)

> **Show monthly EBITDA by division for the trailing 12 months.**

**What to say while it runs:** Monthly EBITDA by division for the trailing 12. This is the chart the CFO opens every quarterly investor call with. If Upstream is widening EBITDA while Downstream is compressing, the capital-allocation conversation is already different — refining margin is the swing factor most analysts under-weight.

**What to look for:** Monthly total_ebitda by division — DATE_TRUNC('month', snapshot_month). Watch the Downstream line against the Upstream line; divergence is the leading signal of where capex needs to re-shift.

**Land the point:** When the same EBITDA curve is in the FP&A Director's hand and the CFO's hand and the Investor Relations deck by Monday morning, the close meeting stops being a number-reconciliation and starts being a capital-mix conversation.

---

## Act 2 — Where the budget breaks — cost centers that earn protection vs. cuts *(≈4 min)*

**Persona:** Controllership Lead • **Job to be done:** Lock the budget-variance call: which cost centers get a corrective action, which get re-baselined, and which carry the next round of cuts.

*Three questions that turn 20 cost centers into a defensible variance-response plan. The middle question — operating margin by division — is the anchor that frames the cut conversation in dollars, not percentages.*

### Question (Act 2.1)

> **Which cost centers are over budget on OPEX, and by what percentage?**

**What to say while it runs:** Cost centers over budget on OPEX, with the percentage. For majors, the standing tolerance on OPEX variance is plus-or-minus 5%. Anything over 10% is a corrective-action trigger, and over 20% is a re-baseline event. The point is not the average overrun — it's the long tail.

**What to look for:** A table of cost centers with total_actual_opex > total_planned_opex showing the percentage delta. Sort descending. The top three or four rows are the ones the CFO will name in the close.

**Land the point:** That list used to be assembled by Controllership over three days of cost-center deep-dives. Now it's the input to the corrective-action conversation the divisional VPs need to have *before* the close, not after.

### Question (Act 2.2)

> **What is operating margin by division for the most recent quarter?**

**What to say while it runs:** Operating margin by division for the most recent quarter. IOC top-quartile is over 20% in a mid-cycle environment. Anything materially below that is either a one-time charge story or a structural cost issue — and those two get treated very differently in the next planning cycle.

**What to look for:** A table or bar of avg operating_margin_pct grouped by division for the most recent quarter. Look for divisions sitting below the 20% benchmark; those are the ones where the budget conversation gets harder.

**Land the point:** Operating margin by division is the number the Board sees. When the FP&A Director and the divisional controllers are looking at the *same* margin, by the *same* definition, the budget defense conversation stops being about whose number is right.

> **Anchor moment.** Hold on the OPEX-over-budget list and the operating-margin-by-division chart together. Pick the worst cost center — call it an Upstream production cost center running 15% over OPEX plan on a $300M annual OPEX base.

> *15% over plan on $300M of OPEX is $45M of unplanned cost in the current year. On Upstream OPEX/BOE economics, with majors targeting under $12/BOE lifting cost, every dollar of overrun on a 100,000 BOE/d cost center is $36M/year — so $45M of variance is roughly $1.20/BOE of margin compression. At PetroLedger's revenue scale of ~$40B, that single cost center alone is 10-15 basis points of total operating margin. Compound that across the 5-6 cost centers currently above 10% variance and you're looking at $200-300M of avoidable OPEX dragging operating margin by 50-80 basis points — the difference between top-quartile and median peer performance.*

> That's the cut-list conversation, in dollars, against the operating-margin number the Board reads. Not a reconciliation exercise. The actual list of cost centers that protect vs. trim the next planning cycle.

### Question (Act 2.3)

> **Top 10 cost centers by ROIC — and how does Upstream compare to Downstream?**

**What to say while it runs:** ROIC ranking — top 10 cost centers, with Upstream and Downstream side-by-side. IOC ROIC target is 8-12%. Cost centers above that are the segments earning their cost of capital; cost centers below it are net consumers. The Upstream-vs-Downstream comparison is the structural mix question for next-year capital allocation.

**What to look for:** Top 10 by roic_pct with division as a comparison column. Watch where Upstream cost centers sit versus Downstream cost centers — if the gap is widening, the capital-mix recommendation writes itself.

**Land the point:** Now the divisional ROIC story is one query away. The capital-allocation conversation the CFO has with the Board next quarter is grounded in the same numbers the divisional VPs are already working from.

---

## Act 3 — Defending the segment story to the Board *(≈4 min)*

**Persona:** Divisional Controller (Upstream) • **Job to be done:** Pre-wire the Board read on segment economics — where lifting cost is trending, where revenue plan is at risk, and what next-cycle capital allocation should reflect.

*The Divisional Controller's job is to make sure the Upstream story holds together before the CFO carries it to the Board. The OPEX/BOE trend and the revenue variance map are the two slides that matter.*

### Question (Act 3.1)

> **How has OPEX per BOE trended month-over-month across the Upstream division?**

**What to say while it runs:** OPEX per BOE month-over-month across Upstream. Majors target under $12/BOE; anything in the $8-10 range is top quartile. The trend matters more than the level — a rising OPEX/BOE in a flat-price environment is what compresses margin, and that's the leading indicator FP&A wants two quarters early.

**What to look for:** Monthly opex_per_boe trend across Upstream cost centers. Inflection points are what frame the capital-allocation pitch — if OPEX/BOE is climbing, the case for capex-funded efficiency projects strengthens.

**Land the point:** When this curve is on the Divisional Controller's desk a quarter before it shows up in the divisional EBITDA print, the Upstream capex defense is no longer reactive — it's a programmatic ask against a known trend.

### Question (Act 3.2)

> **What is total revenue variance percent (actual vs. planned) by region for the trailing 12 months?**

**What to say while it runs:** Total revenue variance percent by region for the trailing 12. Regional revenue variance is where geo-political and commodity-price exposure shows up first. A double-digit negative variance in one region with positive variance in another is the segment-mix story the Board needs to hear before it shows up in next quarter's earnings.

**What to look for:** Grouped table of revenue variance (actual minus planned over planned) by region, trailing 12. Watch for regions with negative variance > 5-10% — those are the regions where the divisional VP needs a defensible response on price, volume, or both.

**Land the point:** Regional revenue variance, by the same definition, every cycle. That's the difference between FP&A getting surprised at year-end and FP&A walking the Board through a known trajectory two quarters early.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PetroLedger Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 cost centers by total actual revenue this year.
2. Show monthly EBITDA by division for the trailing 12 months.
3. Which cost centers are over budget on OPEX, and by what percentage?
4. What is operating margin by division for the most recent quarter?
5. Top 10 cost centers by ROIC — and how does Upstream compare to Downstream?
6. How has OPEX per BOE trended month-over-month across the Upstream division?
7. What is total revenue variance percent (actual vs. planned) by region for the trailing 12 months?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
