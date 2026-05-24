# StratOil Dynamics — Demo Script

**Space:** Oil & Gas Integrated — StratOil Dynamics - Scenario Planning & Business Simulation 🎯
**Runtime:** ~15 minutes • 7 questions
**Audience:** CEO, CFO and Board + Strategy & Planning Director, Corporate Finance Lead, Head of Energy Transition
**KPIs touched:** NPV, IRR, Probability-weighted NPV, Breakeven oil price, Projected production, CO2 intensity
**Big decision automated:** Which 2-3 strategic scenarios — out of the 20 in the simulation portfolio — get adopted as the base case for next-cycle capital allocation, which Transition scenarios earn pilot capex, and how the dividend coverage holds under the Board's downside oil-price band.

---

## Pre-demo checklist

- Open the Genie space `StratOil Dynamics - Scenario Planning & Business Simulation 🎯`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> StratOil Dynamics runs 20 strategic scenarios spanning oil-price stress decks ($40-$100 WTI), production-upside cases, capital-reallocation pathways, and Transition/net-zero scenarios. Today the probability-weighted NPV by scenario lives in the Strategy team's Crystal Ball model, the breakeven-price analysis is owned by Corporate Finance in a separate workbook, and the CO2-intensity-by-scenario view is built by the Energy Transition team in a third deck for the Board sustainability committee. Three artifacts, three teams — and the Board walks into the annual capital-allocation review with three views of the same scenario portfolio and no single source of truth on dividend coverage in a downside. This space ends that. NPV, IRR, breakeven, projected EBITDA, CO2 intensity, variance to baseline — answered out of the same conversation, with the same probability weights, against the same Board hurdle.

---

## Key KPIs in scope

- NPV ($MM) — primary value metric per scenario
- IRR (%) — return threshold; majors typically use 10-15% hurdle
- Probability-weighted NPV ($MM) — risk-adjusted portfolio value
- Breakeven oil price ($/bbl) — downside resilience indicator
- Projected production (MBOED) — top-line operational driver
- CO2 intensity (kg/BOE) — transition / Scope 1+2 benchmark, IOGP median ~17
- EBITDA margin (%) — projected profitability under scenario
- Variance to baseline (%) — scenario delta vs. current trajectory

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **BOE** | Barrels of Oil Equivalent |
| **CEO** | Chief Executive Officer |
| **CFO** | Chief Financial Officer |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |

---

## Act 1 — The shape — which scenarios are actually carrying the value story *(≈4 min)*

**Persona:** Strategy & Planning Director • **Job to be done:** Anchor the scenario-portfolio view before the next strategy retreat — which cases dominate the NPV distribution and where the probability-weighted value is concentrated.

*This is the Strategy Director's prep window before the corporate strategy retreat. Two questions in, the NPV ranking across scenarios and the probability-weighted value curve are on screen — not refreshed, governed.*

### Question (Act 1.1)

> **Top 10 scenarios by average NPV across all simulation runs.**

**What to say while it runs:** Top 10 scenarios by average NPV across all simulation runs. The point isn't the top — it's how *flat* or how *steep* the curve is. A steep top-to-bottom NPV spread means a few scenarios dominate the portfolio value; a flat one means the company's strategic optionality is broadly distributed, and that's a much different capital-allocation conversation.

**What to look for:** Ranked table of 10 scenarios by avg_npv_mm. Watch the spread between #1 and #10 — a 5x gap says the strategy choice is concentrated; a 2x gap says the strategy is robust across paths.

**Land the point:** Now the Strategy Director can hand the retreat the NPV-ranked scenario set the room actually came to discuss — not the version that was current at last quarter's offsite.

### Question (Act 1.2)

> **Show monthly probability-weighted NPV by scenario category for the trailing 12 months.**

**What to say while it runs:** Monthly probability-weighted NPV by scenario category over 12 months. Probability-weighted NPV is the metric that the Board sees — raw NPV without a probability weight overweights low-likelihood high-value paths. The category cut tells you whether Baseline, Price Stress, Production Upside, or Transition is carrying the current expected portfolio value.

**What to look for:** Monthly weighted_npv_mm by scenario_category — DATE_TRUNC('month', kpi_month). Watch for shifts in which category is dominant; that shift is the macro signal that the corporate strategy is implicitly re-balancing.

**Land the point:** When the Board sees the same probability-weighted NPV curve the Strategy team is working from, the strategy retreat stops being a methodology debate and starts being a capital-allocation conversation.

---

## Act 2 — Stress, transition, or hold — locking the base case *(≈4 min)*

**Persona:** Corporate Finance Lead (acting on behalf of the CFO) • **Job to be done:** Defend the next-cycle base case against the Board's downside band and surface which Transition scenarios actually clear the corporate hurdle.

*Three questions that turn 20 scenarios into a defensible base-case + 2 sensitivity recommendation. The middle question — breakeven price across categories — is the anchor that quantifies the dividend coverage under the Board's downside oil-price band.*

### Question (Act 2.1)

> **Which Transition scenarios deliver positive IRR above 10%, and what is their projected CO2 intensity?**

**What to say while it runs:** Transition scenarios with IRR above 10%, with their projected CO2 intensity. The transition portfolio is the most-watched part of the strategy now — Board sustainability committees require a credible economic case alongside the emissions case. IOGP median CO2 intensity is around 17 kg/BOE; transition scenarios that come in materially below that *and* clear the 10% hurdle are the ones that earn pilot capex.

**What to look for:** Table of scenarios with scenario_category = Transition where irr_pct > 10, showing co2_intensity_kg_boe. Look for rows that pair sub-15 kg/BOE intensity with double-digit IRR — those are the pilots that defend the transition strategy to the Board.

**Land the point:** That short list used to come out of three different working sessions between Strategy and the Transition team. Now it's the input to the pilot-capex conversation the CFO can actually commit against.

### Question (Act 2.2)

> **Compare average breakeven oil price across Baseline, Price Stress, and Production Upside scenarios.**

**What to say while it runs:** Breakeven oil price across Baseline, Price Stress, and Production Upside. Breakeven is the downside-resilience metric — at what oil price does this scenario still cover its cost of capital. For an IOC, a portfolio breakeven of $35-45/BBL is investor-grade; over $55 is exposed. The Board's standard sensitivity is the $50/BBL downside — if the breakeven is at or above that, the dividend is at risk.

**What to look for:** Grouped table of avg_breakeven_price by scenario_category. Look at Baseline versus Price Stress — if the gap is wide, the portfolio has resilience optionality; if it's narrow, the dividend coverage is more fragile than the headline implies.

**Land the point:** Breakeven across categories, by the same probability weights, in one view. That's the conversation that turns dividend-coverage stress testing from an annual exercise into a quarterly discipline.

> **Anchor moment.** Hold on the breakeven-price-by-category view. Pick the Price Stress scenario at $50/BBL WTI — call it a portfolio with $20B in projected revenue and an avg breakeven that has moved from $42 to $48.

> *At StratOil's portfolio scale, a $1/BBL move in WTI is roughly $250-400M of annual EBITDA on a 700,000 BOE/d production base. So a $50 WTI downside versus a $70 base case is a $5-8B annual EBITDA hit — well in excess of the current dividend run-rate. A breakeven that has crept from $42 to $48 means the dividend has $2-3 of head-room left before coverage breaks. Sanction a $1.5B greenfield with a $55/BBL economic threshold and you've burned what little cushion there was; defer that project, pace the LNG train, and you preserve $3-4B of dividend optionality across the next two stress cycles. Compound this across the 4-5 Price Stress scenarios currently in the portfolio and you're looking at a $10-15B difference in cumulative dividend-funding capacity over a 5-year stress window.*

> That's the dividend-defense conversation this space converts from a once-a-year stress test into a quarterly portfolio discipline. The capital pacing decision becomes a number — not a posture.

### Question (Act 2.3)

> **Top 10 scenarios by projected EBITDA — and how do they rank on CO2 intensity?**

**What to say while it runs:** Top 10 scenarios by projected EBITDA, with CO2 intensity alongside. This is the dual-objective scoring the Board actually uses — economic return against transition posture. A scenario that scores top decile on EBITDA but top decile on CO2 intensity is no longer a clean approve; it requires a re-balancing argument.

**What to look for:** Top 10 by avg_projected_ebitda_mm with co2_intensity_kg_boe as a side column. Watch where the EBITDA leaders sit on CO2 — that's the dual-objective tension the strategy retreat exists to resolve.

**Land the point:** EBITDA and CO2 in the same answer is the question the Board asks every cycle. Having it one query away changes how the strategy team prepares the deck — and how the CEO defends it.

---

## Act 3 — The Board commitment — adopting the base case *(≈4 min)*

**Persona:** Head of Energy Transition (defending the Transition pathway) • **Job to be done:** Defend the transition-strategy story alongside the financial story so the Board adopts a coherent base case rather than two disconnected narratives.

*The Head of Transition takes the recommendation up the chain. The EBITDA trajectory and the variance-to-baseline screen are the two views that align the financial story with the transition story before the Board lands on a base case.*

### Question (Act 3.1)

> **How has average projected EBITDA trended month-over-month across the portfolio?**

**What to say while it runs:** Average projected EBITDA month-over-month across the portfolio. The EBITDA trajectory across the simulation portfolio is the corporate-strategy heartbeat. If projected EBITDA is widening over time across the portfolio, the strategy is in growth mode; if it's flat or compressing, the strategy has to defend that to the Board in the same conversation as the dividend.

**What to look for:** Monthly avg_projected_ebitda_mm portfolio-wide. Inflection points are what tells the room whether the current strategy is gaining or losing economic ground.

**Land the point:** Having this trajectory in the same view as the transition portfolio is what lets the Board adopt a coherent base case — not pick between economics and transition as two separate votes.

### Question (Act 3.2)

> **Which Price Stress scenarios have negative variance to baseline greater than 15%?**

**What to say while it runs:** Price Stress scenarios with negative variance to baseline greater than 15%. The 15% downside threshold is the Board's standard stress trigger — anything beyond it is the scenario that has to be modeled in detail for the next dividend coverage review. The point is to surface the scenarios that drive the worst-case capital pacing decisions before the Board has to ask.

**What to look for:** Table of scenarios with scenario_category = Price Stress and variance_to_baseline_pct < -15. Watch for clusters in similar oil-price decks — that's where the dividend-coverage stress is concentrated.

**Land the point:** Knowing the worst-case scenarios before the Board asks is the difference between the CEO walking into the annual capital review with a defense and walking in with a recommendation. This space makes it the second one.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — StratOil Dynamics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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
2. Show monthly probability-weighted NPV by scenario category for the trailing 12 months.
3. Which Transition scenarios deliver positive IRR above 10%, and what is their projected CO2 intensity?
4. Compare average breakeven oil price across Baseline, Price Stress, and Production Upside scenarios.
5. Top 10 scenarios by projected EBITDA — and how do they rank on CO2 intensity?
6. How has average projected EBITDA trended month-over-month across the portfolio?
7. Which Price Stress scenarios have negative variance to baseline greater than 15%?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
