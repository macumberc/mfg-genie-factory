# RefineLedger Corp — Demo Script

**Space:** Oil & Gas Refining — RefineLedger Corp - Financial Analytics & Reporting 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Finance VP, Controller, Division Presidents (Gulf Coast / Midwest / National)
**KPIs touched:** Operating margin, Return on Invested Capital, EBITDA by division and cost center, Revenue and OPEX vs. plan variance, Cost per unit of output, CAPEX deployment vs. plan
**Big decision automated:** Which 2-3 cost centers get a structural OPEX intervention this quarter, which divisions defend their capex envelope, and which regions earn the next $50M tranche of growth capital — all defended live in the CFO's monthly business review.

---

## Pre-demo checklist

- Open the Genie space `RefineLedger Corp - Financial Analytics & Reporting 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RefineLedger Corp runs financial analytics across 20 cost centers spanning Processing, Supply Chain, Support, and Corporate divisions across Gulf Coast, Midwest, and National operations. Today the OPEX-vs-plan variance lives in the Controller's monthly close workbook, the ROIC-by-region cut sits in the FP&A team's quarterly board pack, and the cost-per-barrel benchmark gets pulled from a separate division-level rollup nobody reconciles to the GL. Three artifacts, three close cycles — so the margin-defense narrative at the quarterly review gets written in tabs that don't tie, and the Division Presidents argue about which numbers are real before they argue about what to do. This space ends that. One governed surface where the actual-vs-plan delta, the ROIC ranking, and the cost-per-bbl ratio all draw from the same GL — and the CFO walks into the executive review with one set of numbers, not three.

---

## Key KPIs in scope

- Operating margin (%) — refining peers typically run 5-15% through-cycle
- Return on Invested Capital (ROIC %) — top-quartile refiners exceed 12%
- EBITDA ($) by division and cost center
- Revenue and OPEX vs. plan variance (% and $)
- Cost per unit of output ($/bbl equivalent)
- CAPEX deployment vs. plan
- Headcount efficiency (revenue per FTE)
- G&A as a percentage of revenue

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CAPEX** | Capital Expenditure |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |
| **OPEX** | Operating Expense |

---

## Act 1 — The signal — surfacing the cost centers driving the margin miss before the close package goes out *(≈4 min)*

**Persona:** Controller • **Job to be done:** Land the variance commentary for the monthly close package without spending three days reconciling between the GL extract, the FP&A model, and the divisional rollup.

*This is the moment the monthly close narrative starts forming. Two questions in, the Controller already has the cost-center ranking that used to take a full day of Excel.*

### Question (Act 1.1)

> **Top 10 cost centers by total actual revenue over the last 12 months.**

**What to say while it runs:** Top cost centers by `total_actual_revenue` is where the CFO starts every monthly review — but the value is in the *gap* between top and bottom. The bottom of the list is usually where the structural margin leak is hiding, and it's the one nobody touches because the absolute numbers are smaller.

**What to look for:** A ranked table of the top 10 cost centers by 12-month actual revenue. Click *Show generated code* once — the room sees governed columns from the metric view, not analyst-built math.

**Land the point:** Right there is the conversation the CFO will run in the executive review next week — and for the first time, every Division President is looking at the exact same number.

### Question (Act 1.2)

> **Show monthly trend of total EBITDA across the company for the trailing 12 months.**

**What to say while it runs:** Now the EBITDA trend — this is the chart that determines whether the year's margin guidance holds. Refining peers run 5-15% operating margin through-cycle, and a single quarter of slippage is the difference between an in-line print and a downgrade.

**What to look for:** Monthly bars of `total_ebitda` across the company over 12 months — `DATE_TRUNC('month', ...)` shape. Watch for the months the variance opened up against plan.

**Land the point:** Before this space, that chart was rebuilt by hand for the close package every month. Now it's the Controller's first question of the day — and the variance commentary writes itself before the GL is even closed.

---

## Act 2 — The decision — locking the OPEX-cut list and the capex defense before the board pack ships *(≈4 min)*

**Persona:** Finance VP • **Job to be done:** Commit to the cost centers and divisions that get a structural intervention this quarter and the ones that defend their plan untouched.

*Three questions that turn the monthly variance into a defensible quarterly intervention plan. The middle question is the anchor — adverse-revenue-variance dollars converted into a margin-defense decision.*

### Question (Act 2.1)

> **Which divisions are running OPEX over plan year-to-date, and by how much?**

**What to say while it runs:** OPEX over plan by division is the structural-vs-noise filter — anything more than 3% over plan YTD is structural and needs an intervention plan. Refining-peer through-cycle OPEX discipline is what separates the 5% margin operators from the 12% margin operators.

**What to look for:** A table by division of `total_actual_opex` vs `total_planned_opex`, with the dollar gap. The shape — one division 8% over plan, two near plan — is what the intervention is sized against.

**Land the point:** That table used to take a half-day of cross-system stitching against the FP&A model. Now it's the input to the quarterly business review the CFO runs on Monday.

### Question (Act 2.2)

> **Top 10 cost centers by adverse revenue variance vs. plan this quarter.**

**What to say while it runs:** Adverse revenue variance vs plan this quarter is where the margin defense gets real. On a refinery our size, a $5M adverse variance against a 200 KBD plan is basically a quarter where the crack spread moved against us by a buck — recoverable through slate optimization, not structural. A $20M variance is a different conversation.

**What to look for:** Top 10 cost centers by adverse `total_actual_revenue` vs `total_planned_revenue` this quarter. The cluster pattern matters — if three are in the same division, that's an integrated planning question, not three independent ones.

**Land the point:** When the Finance VP, the Controller, and the Division President all see the same adverse-variance ranking, the conversation stops being about whose model is right and starts being about *which cost centers get a corrective action plan*.

> **Anchor moment.** Stop on the adverse-revenue-variance table. Pick the top three cost centers — call them collectively about $15M of adverse variance against a $200M planned-revenue base for the quarter.

> *$15M of adverse revenue variance against plan, at a roughly 10% operating margin pass-through, is $1.5M of operating-income drag this quarter — $6M annualized. Now stack a structural OPEX intervention on the two cost centers running 8% over plan — that's typically a 200-400 bps OPEX-to-revenue compression, worth another $5-10M/year on these divisions. Total margin recovery in the room: $10-15M/year. On a CFO's bonus card, that's two ROIC points. Even if the program lands at half — five points of ROIC compounded into next year's capex envelope.*

> That's the decision this space automates. Not the variance slide. The decision. The intervention list moves from a quarterly debate about whose number is right to a signed corrective-action plan the Controller can hold each Division President against.

### Question (Act 2.3)

> **How has operating margin trended month-over-month by division?**

**What to say while it runs:** Operating margin by division month-over-month is the *direction* number. Through-cycle refining peers manage 5-15% — and inside that band, the inflection points are what matter. A division that drifts from 11% to 7% over two quarters is the candidate for a structural review *before* it shows up in the year-end print.

**What to look for:** Monthly `total_ebitda`-over-revenue by division. Watch for the divisions where the curve is bending the wrong way.

**Land the point:** That direction view is the difference between a clean board pack and a board pack that gets re-cut at midnight the day before the meeting.

---

## Act 3 — The commitment — sizing the next $50M capital tranche and defending the ROIC story to the board *(≈4 min)*

**Persona:** CFO • **Job to be done:** Lock the capital-allocation narrative for the year — which region earns growth capital, which holds plan, which gets harvested.

*The CFO doesn't need a new pack; they need the same numbers the Controller and the Division Presidents are acting on, in the same language, so the board ROIC narrative writes itself.*

### Question (Act 3.1)

> **Which regions have the highest ROIC, ranked best to worst?**

**What to say while it runs:** ROIC ranking by region is the capital-allocation conversation in one chart. Top-quartile refiners exceed 12% ROIC through-cycle. Anything below 8% is a candidate for harvest-mode operating, not growth capital.

**What to look for:** Regions ranked best-to-worst on ROIC. The shape — one region above 12%, one in the 8-12% band, one below — is the capital-allocation skeleton.

**Land the point:** When that ranking is the same one the Finance VP and Controller already validated this quarter, the board capital-allocation conversation moves from a debate to a decision.

### Question (Act 3.2)

> **What is the OPEX-to-revenue ratio by division this quarter?**

**What to say while it runs:** OPEX-to-revenue ratio by division is the cost-leadership lens. Combine it with the ROIC ranking and you have the four-quadrant map every CFO wants — growth investment, OPEX intervention, harvest-mode, and divest.

**What to look for:** Divisions on `total_actual_opex` over `total_actual_revenue` this quarter. Match each one against the ROIC ranking from the prior question. The four-quadrant overlay is the capital-allocation slide.

**Land the point:** Close at 8 AM, capital allocation at 10 — same space, same numbers. The Controller's variance commentary, the Finance VP's intervention list, and the CFO's board pack are now the *same artifact* — and the executive team stops getting surprised at year-end.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RefineLedger Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 cost centers by total actual revenue over the last 12 months.
2. Show monthly trend of total EBITDA across the company for the trailing 12 months.
3. Which divisions are running OPEX over plan year-to-date, and by how much?
4. Top 10 cost centers by adverse revenue variance vs. plan this quarter.
5. How has operating margin trended month-over-month by division?
6. Which regions have the highest ROIC, ranked best to worst?
7. What is the OPEX-to-revenue ratio by division this quarter?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
