# MidStream Dynamics — Demo Script

**Space:** Oil & Gas Midstream — MidStream Dynamics - Scenario Planning & Simulation 🎯
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Strategy + CFO, COO, Network Planning Lead
**KPIs touched:** Weighted NPV, Projected EBITDA, Projected throughput, CapEx required, Regulatory risk score, Throughput change vs. baseline
**Big decision automated:** Which two scenarios anchor next year's strategic plan — and the resulting capex sequence, dropdown coverage ratio, and MLP-distribution policy we commit to in front of the board.

---

## Pre-demo checklist

- Open the Genie space `MidStream Dynamics - Scenario Planning & Simulation 🎯`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> MidStream Dynamics models tariff-escalation, volume-defense, M&A, and regulatory-shock scenarios across an integrated gathering, processing, and transmission footprint. Today the weighted-NPV scenario rankings live in the strategy team's planning model, the projected EBITDA scenarios live in FP&A's long-range plan, and the regulatory-risk overlay lives in Legal's policy-exposure tracker. Three models, same enterprise — and the capex sequencing, the dropdown coverage decision, and the distribution-policy commitment all get made on different scenario sets that don't reconcile. This space ends that. One governed surface where weighted_npv_mm, projected_ebitda_mm, capex_required_mm, and regulatory_risk_score line up by scenario — so the strategic plan gets locked on probability-weighted dollars, not on whichever scenario the loudest exec advocated for.

---

## Key KPIs in scope

- Weighted NPV ($MM) — probability-weighted scenario value
- Projected EBITDA ($MM) — bottom-line scenario outcome
- Projected throughput (mbpd) — operational scenario output
- CapEx required ($MM) — capital commitment to execute scenario
- Regulatory risk score (0-100) — policy / permitting exposure
- Throughput change (%) vs. baseline — operational delta
- Variance to baseline (%) — financial delta vs. base case
- Confidence level — High / Medium / Low statistical confidence

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **COO** | Chief Operating Officer |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |
| **VP** | Vice President |

---

## Act 1 — The signal — which scenarios are carrying value and which are eating capex *(≈4 min)*

**Persona:** Network Planning Lead • **Job to be done:** Surface the top-NPV scenarios and the EBITDA trajectory across the planning portfolio before the strategy-team review.

*This is the moment the long-range plan starts to form. Two questions in, the planning team has the NPV ranking and the EBITDA trend that used to take a quarter of modeling and reconciliation.*

### Question (Act 1.1)

> **Top 10 scenarios by average NPV across all simulation runs.**

**What to say while it runs:** Top 10 scenarios by avg_npv_mm is the value-ranking view. We model a hundred-plus scenarios across tariff escalation, volume defense, M&A, and regulatory shocks — the top 10 typically capture 60-70% of the probability-weighted upside. Those are the ones the board actually has to commit capital to.

**What to look for:** Ranked table of scenario_name with avg_npv_mm. The top 10 list is the scenario portfolio leadership needs to defend; everything below is informational.

**Land the point:** Now the Planning Lead walks into the strategy review with the scenarios already ranked by dollars — and the conversation that used to start 'walk me through the model' starts 'here are the 10 scenarios we're funding, here are the others we're parking.'

### Question (Act 1.2)

> **Show monthly trend of average projected EBITDA by scenario type for the trailing 12 months.**

**What to say while it runs:** Monthly trend of avg projected_ebitda_mm by scenario_type over the trailing 12 is the realization-vs-model view. We don't just want NPV; we want to see which scenario types — infrastructure, M&A, regulatory — are trending toward or away from their modeled EBITDA outcomes as new data lands.

**What to look for:** Monthly bars of avg_ebitda_mm by scenario_type — DATE_TRUNC('month', snapshot_date) shape. Scenarios converging toward their forecast are credible; ones drifting away signal a model assumption that's no longer holding.

**Land the point:** That trend used to be the output of a quarterly assumptions review. Now it's a continuous question — and when an assumption breaks, the strategy team catches it in days, not in the next planning cycle.

---

## Act 2 — The decision — which scenarios earn capital and which we shelve *(≈4 min)*

**Persona:** VP Strategy • **Job to be done:** Lock the scenario set the executive team commits to and translate it into the capex sequence and dropdown framework for the next 18 months.

*Three questions that turn the scenario portfolio into a strategic commitment. The middle question is the anchor — the NPV-to-capex math that converts a planning exercise into a board decision.*

### Question (Act 2.1)

> **Which scenarios have the highest regulatory risk score, and what is their projected throughput?**

**What to say while it runs:** Scenarios with the highest regulatory_risk_score and their projected_throughput_mbpd is the policy-exposure view. A high-NPV scenario with a regulatory risk score of 80 is a very different commitment than one with a score of 30 — the throughput overlay tells us how much volume is at risk if the policy environment turns.

**What to look for:** Scenarios with regulatory_risk_score and projected_throughput_mbpd. The top of this list is where the M&A or expansion case has to clear a higher bar before the board signs off.

**Land the point:** When the VP Strategy can see regulatory exposure paired with throughput, the M&A vs. organic-expansion conversation moves from 'which has higher NPV' to 'which has the right risk profile' — and that's the board-level reframe that changes the answer.

### Question (Act 2.2)

> **What is the total capex required across all Infrastructure scenarios, by scenario type?**

**What to say while it runs:** Total capex_required across all Infrastructure scenarios, by scenario_type, is the affordability check. We can have a beautiful scenario portfolio that aggregates to $4B of required capex against an $800M annual budget — and if we don't see that early, the strategic plan promises more than the balance sheet delivers.

**What to look for:** Scenario_type with total_capex_mm. The aggregate vs. the budget envelope is the binary 'does this strategy actually fit' check.

**Land the point:** That total used to take FP&A weeks to roll up across the planning model. Now it's a question — and the scenario-vs-budget reconciliation happens before the board sees the plan, not after.

> **Anchor moment.** Hold on the top-NPV scenarios table and the capex-by-scenario-type aggregate. Take the top two infrastructure scenarios — together $300M weighted NPV, requiring $600M of capex against a $1B annual capex envelope.

> *$300M of weighted NPV on $600M of capex is a 50% NPV-to-capex ratio — strong. But two scenarios consuming 60% of annual capex means we've effectively locked the next 18 months. Compare that to a third scenario at $150M NPV / $200M capex (75% NPV-to-capex ratio) — better unit economics, leaves room for the M&A optionality. Probability-weight the three, layer in regulatory_risk, and the right portfolio is two of the three, not all three. That's a $200M reallocation decision that used to take a 90-day capital-allocation cycle.*

> That's the decision this space automates. Not the strategy slide. The capex sequence. The scenario portfolio gets locked on weighted NPV against budget envelope, not on which scenario sponsor had the strongest narrative at the offsite.

### Question (Act 2.3)

> **How has average regulatory risk trended month-over-month across the scenario portfolio?**

**What to say while it runs:** Average regulatory_risk trended month-over-month is the policy-environment temperature check. As FERC orders, EPA rules, and state PUC decisions land, our portfolio's effective risk score moves with them — and a rising line means we're getting more exposed to scenarios we already committed to.

**What to look for:** Monthly trend of avg_regulatory_risk. A rising line is the trigger for a mid-cycle scenario revisit, even if individual project NPVs still look attractive.

**Land the point:** When that curve is in front of the Strategy VP and the CFO together, the discipline of revisiting commitments on a quarterly cadence becomes mechanical, not political — and that's a real shift in how the company manages strategic risk.

---

## Act 3 — The commitment — defending the plan to the board and the MLP investors *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend the strategic plan to the board and translate it into the dropdown / distribution-coverage framework MLP investors price into the unit.

*The CFO doesn't need a second strategy deck; they need the same NPV, capex, and risk numbers the Planning Lead and the VP Strategy are running on — so the dropdown sequence and the distribution-coverage commitment are built off one source.*

### Question (Act 3.1)

> **Top 10 scenarios by total throughput change percent.**

**What to say while it runs:** Top 10 scenarios by total throughput_change_percent is the operational-realism view. A scenario can have a beautiful NPV and still imply a throughput change the network can't actually deliver — capacity, contracts, and integrity windows constrain reality. We want the high-NPV scenarios that imply realistic throughput moves, not 30%-volume miracles.

**What to look for:** Ranked table of scenario_name with throughput_change_pct. Anything above ±20% deserves a second look at the operating assumptions before committing capital.

**Land the point:** When the CFO can pair NPV with throughput realism, the board pitch lands with both confidence and credibility. The 'how confident are you' question gets a number, not a hedge.

### Question (Act 3.2)

> **Which low-confidence scenarios have NPV above the portfolio average — and what is the risk score for each?**

**What to say while it runs:** Low-confidence scenarios with NPV above the portfolio average and their risk_score is the optionality view. Low-confidence-high-NPV is exactly where we want optionality — not main-case capex, but staged investment, JV structures, or right-of-first-refusal commitments that we exercise as the confidence improves.

**What to look for:** Filter to confidence_level = Low with npv_mm above portfolio avg and risk_score attached. These are the candidates for optionality structures, not full capex commitments.

**Land the point:** Triage in the strategy team in the morning, dropdown sequence locked by afternoon, MLP distribution-coverage commitment defended to the board by Friday. Same space. Same numbers. The Planning Lead's portfolio, the VP Strategy's commitments, and the CFO's investor-day narrative are now the same artifact.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — MidStream Dynamics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 scenarios by average NPV across all simulation runs.
2. Show monthly trend of average projected EBITDA by scenario type for the trailing 12 months.
3. Which scenarios have the highest regulatory risk score, and what is their projected throughput?
4. What is the total capex required across all Infrastructure scenarios, by scenario type?
5. How has average regulatory risk trended month-over-month across the scenario portfolio?
6. Top 10 scenarios by total throughput change percent.
7. Which low-confidence scenarios have NPV above the portfolio average — and what is the risk score for each?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
