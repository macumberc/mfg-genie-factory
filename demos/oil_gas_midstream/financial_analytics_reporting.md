# MidLedger Analytics — Demo Script

**Space:** Oil & Gas Midstream — MidLedger Analytics - Financial Analytics & Reporting 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + FP&A Director, Division Presidents, Treasurer
**KPIs touched:** EBITDA, Operating margin, ROIC, Revenue actual vs. plan, OpEx actual vs. plan, Cost per unit
**Big decision automated:** Which midstream segment — gathering, processing, or transmission — earns the next $50M of capex, and which divisions get a budget cut to fund it.

---

## Pre-demo checklist

- Open the Genie space `MidLedger Analytics - Financial Analytics & Reporting 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> MidLedger Analytics runs an integrated gathering, processing, and transmission portfolio across multiple operating regions. Today the EBITDA-by-division number lives in FP&A's monthly close model, the actual-vs-plan opex variance lives in the controller's GL extract, and the ROIC view lives in the Treasurer's quarterly capital-stack deck. Three models, same dollars — and the next-year capex allocation, the budget-variance escalation, and the unit-economics conversation all run on three different period-cuts of the same ledger. This space ends that. One governed surface where ebitda_usd, actual vs. planned, operating_margin_pct, and roic_pct line up by division and region — so capex allocation gets made on returns, not on whose budget owner pushed back hardest in the planning meeting.

---

## Key KPIs in scope

- EBITDA ($) — primary profitability metric
- Operating margin (%) — current portfolio ranges -10% to 35%; healthy divisions trend above 20%
- ROIC (%) — return on invested capital (target >WACC, typically 8-10%)
- Revenue actual vs. plan ($) — top-line variance
- OpEx actual vs. plan ($) — cost-side variance
- Cost per unit ($) — unit economics across cost centers
- Headcount — labor capacity by division
- Budget variance (%) — actual vs. budget at GL-category level

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |

---

## Act 1 — The signal — which divisions are carrying the portfolio and which are bleeding margin *(≈4 min)*

**Persona:** FP&A Director • **Job to be done:** Pull the monthly EBITDA-by-division trend and the worst opex-variance cost centers before the executive review.

*This is the moment the next quarterly business review starts to take shape. Two questions in, FP&A has the EBITDA shape and the variance list that used to take three days of cross-system stitching.*

### Question (Act 1.1)

> **Show monthly total EBITDA by division for the trailing 12 months.**

**What to say while it runs:** Monthly EBITDA by division over the trailing 12 is the portfolio-health view. Midstream divisions should run above 20% operating margin in steady state — anything dipping into single digits month after month is a structural conversation, not a one-time variance.

**What to look for:** Monthly bars of total_ebitda by division — DATE_TRUNC('month', snapshot_month) shape. The room should notice which divisions hold steady and which are sawtoothing on tariff-cycle resets.

**Land the point:** Now the FP&A director walks into the QBR with the divisional ranking already framed — and the conversation that used to start 'let me explain my chart' starts 'here's where the portfolio is winning and where it's not.'

### Question (Act 1.2)

> **Top 10 cost centers by actual-vs-planned opex variance this year.**

**What to say while it runs:** Top 10 cost centers by actual-vs-planned opex variance YTD is the controllable-cost story. We don't care about timing variances; we care about the ones running 15%+ over plan three months in a row — those are the ones the cost-center owner needs to defend.

**What to look for:** Ranked table of cost_center_name with actual and budget_amount side by side. Sort by the dollar variance, not the percent — a 5% miss on a big cost center beats a 50% miss on a small one.

**Land the point:** That list used to be the result of GL extracts and pivot tables on the 12th business day. Now it's a question — and the cost-center owner gets the conversation at month +5, not at quarter-end.

---

## Act 2 — The decision — which segment earns the next capex dollar *(≈4 min)*

**Persona:** Division President • **Job to be done:** Defend the gathering vs. processing vs. transmission capex split and lock the budget-variance plan for the back half of the year.

*Three questions that turn the variance view into a capex-allocation recommendation. The middle question is the anchor — the EBITDA-to-capital-return math that converts a monthly close into a board-level investment decision.*

### Question (Act 2.1)

> **Which divisions have operating margins below 20%, and how has that trended monthly?**

**What to say while it runs:** Divisions with operating_margin_pct below 20%, trended monthly, separates one-quarter weather from a structural problem. A division below 20% for a single month is a variance; below 20% for six months is either a tariff-renewal conversation, an opex restructuring, or a divestiture study.

**What to look for:** Divisions filtered to operating_margin_pct < 20%, with the monthly shape over 12 months. Slope matters more than level — a 25%-margin division trending down is a worse story than a 15% division trending up.

**Land the point:** When the President can pull that filter in a question, the divestiture-or-fix conversation moves from a once-a-year strategic offsite to a quarterly working decision.

### Question (Act 2.2)

> **What is the total actual revenue by region this quarter compared to plan?**

**What to say while it runs:** Actual revenue by region this quarter compared to plan is the top-line variance view. Gathering revenue is volume-driven, transmission revenue is tariff- and demand-charge-driven — the same dollar miss has very different implications by segment. Region matters because Permian gathering doesn't behave like Marcellus transmission.

**What to look for:** Region with total_actual_revenue vs. total_planned_revenue. The biggest signed gap is where the next capex argument either gets reinforced or undercut.

**Land the point:** Same revenue number, same region cuts, same period — for FP&A, the division president, and the board. That's the moment the capex defense stops being three competing decks and becomes one ranked list.

> **Anchor moment.** Hold on the EBITDA-by-division chart and the regional revenue-vs-plan view. Pick the underperforming division — call it transmission running $40M EBITDA on $200M revenue against a $50M plan.

> *A $10M EBITDA miss on $200M revenue is a 5-point margin gap, and at an 8% WACC that's $125M of foregone enterprise value at the segment level. A targeted $30M capex into either the gathering footprint or the transmission compressor upgrade typically yields 15-20% incremental ROIC — call it $5M of annual EBITDA uplift, payback under 6 years, well inside dropdown horizons. Across three segments competing for $50M, the segment with the documented 15%+ ROIC opportunity wins — and that decision used to take a 90-day capital-allocation cycle.*

> That's the decision this space automates. Not the close pack. The capex allocation. Gathering vs. processing vs. transmission ranked on ROIC and variance, not on whose President had the strongest narrative in the Q4 offsite.

### Question (Act 2.3)

> **Top 10 GL categories by total transaction amount year-to-date.**

**What to say while it runs:** Top 10 GL categories by total_amount YTD is where the dollars are actually living. We say 'control opex,' but unless we can rank GL categories by dollars, we're guessing at which line item the savings come from. Power, chemicals, maintenance contracts — those usually top the list.

**What to look for:** Ranked table of gl_category with total_amount_usd. The biggest categories are where targeted savings programs have to land — small-category cost-cuts are noise.

**Land the point:** When the division president can identify the top three GL categories driving the variance in a question, the next sourcing or operational program gets pointed at the right line item — not at whichever cost center was the loudest in budget season.

---

## Act 3 — The commitment — locking ROIC and unit economics for the board *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the capital plan to the board and the rating agencies on consistent ROIC and unit-economics evidence.

*The CFO doesn't need another close-pack; they need the same EBITDA, ROIC, and cost-per-unit numbers the divisions are running on, so the rating-agency narrative writes itself when the next debt-issuance window opens.*

### Question (Act 3.1)

> **How has ROIC trended month-over-month across the company?**

**What to say while it runs:** ROIC trended month-over-month across the company is the capital-discipline view. WACC sits 8-10%; ROIC consistently above WACC means the capital plan is creating value, below means we're destroying it. The slope is the story the board cares about more than any single month.

**What to look for:** Monthly trend of roic_pct. A flat-to-rising line above WACC is what the rating agency expects to see going into the next refinancing window.

**Land the point:** When the CFO can show ROIC trending up by quarter — and pair it with the capex queue the division presidents have signed off on — the rating-agency conversation moves from 'show us the plan' to 'we like the plan.' And that's a real basis-point conversation on the next bond.

### Question (Act 3.2)

> **Which cost centers have the highest cost per unit, and what is the headcount in each?**

**What to say while it runs:** Cost centers with the highest cost_per_unit and the headcount in each is the productivity view. Cost-per-unit cuts through size — a high-headcount cost center with strong cost_per_unit is well-leveraged; a low-headcount one with weak cost_per_unit is a process problem, not a staffing problem.

**What to look for:** Ranked table of cost_center_name with cost_per_unit and headcount. The combination tells you whether the right answer is process re-engineering or staffing change.

**Land the point:** Triage in the controller's office in the morning, board-level productivity narrative in the afternoon. Same space. Same numbers. The FP&A variance list and the CFO's investor-day chart are now the same artifact — and the rating-agency review gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — MidLedger Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total EBITDA by division for the trailing 12 months.
2. Top 10 cost centers by actual-vs-planned opex variance this year.
3. Which divisions have operating margins below 20%, and how has that trended monthly?
4. What is the total actual revenue by region this quarter compared to plan?
5. Top 10 GL categories by total transaction amount year-to-date.
6. How has ROIC trended month-over-month across the company?
7. Which cost centers have the highest cost per unit, and what is the headcount in each?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
