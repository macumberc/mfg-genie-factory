# FoodPlan Analytics — Demo Script

**Space:** Food & Beverage — FoodPlan Analytics - Scenario Planning & Simulation 🎯
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Strategy + CFO, Revenue Growth Management Lead, S&OP Lead
**KPIs touched:** Total simulated revenue, Average simulated margin, Revenue at risk, Optimal price change, Confidence level, Invest count
**Big decision automated:** Which 2-3 categories get the next-cycle new-SKU launch budget vs. which plants get the line-refurb capex, and what optimal price moves go into next year's annual operating plan.

---

## Pre-demo checklist

- Open the Genie space `FoodPlan Analytics - Scenario Planning & Simulation 🎯`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FoodPlan Analytics models 20 product categories across consumer segments and retail / foodservice / e-commerce channels heading into next year's annual operating plan. Today the COGS-inflation scenarios live in a Finance analyst's Excel workbook, the elasticity coefficients live in a Revenue Growth Management spreadsheet, and the competitive-pressure read lives in a strategy team PowerPoint built off Nielsen extracts. Three artifacts, one P&L — and when the CFO asks 'what's the optimal price move on dairy if input costs jump 8%', the answer takes a week and arrives in a deck that nobody can rebuild. This space ends that. One governed surface where the CFO, RGM, and S&OP run the same scenarios on the same data and walk out with the new-SKU vs. refurbish-capex allocation already signed.

---

## Key KPIs in scope

- Total simulated revenue ($) — top-line under each scenario set
- Average simulated margin (%) — contribution margin after COGS shocks
- Revenue at risk ($) — downside exposure across disruption scenarios
- Optimal price change (%) — RGM recommendation; CPG elasticity typically -0.3 to -0.6
- Confidence level (%) — statistical confidence on outcome bands
- Invest count — categories flagged Invest investment priority
- Disruption scenario count — adverse runs in the trailing period
- Market share (%) — competitive position by segment / channel

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **VP** | Vice President |

---

## Act 1 — The signal — sizing the downside and ranking the upside *(≈4 min)*

**Persona:** Revenue Growth Management Lead • **Job to be done:** Locate the categories with the most revenue-at-risk and the highest expected upside under base scenarios — before the AOP draft hits the CFO.

*This is the first stop in AOP-prep. Two questions in, the RGM lead has the downside map and the optimal-price ranking that used to take three analysts a week to assemble.*

### Question (Act 1.1)

> **Show the monthly trend in total revenue at risk across all segments for the trailing 12 months.**

**What to say while it runs:** Monthly trend in total revenue at risk across all segments. Revenue-at-risk is the downside dollar number — what we lose if the pessimistic and disruption scenarios actually fire. A rising line is structural exposure building; a flat line is a portfolio holding its own through the volatility.

**What to look for:** Monthly trend on `total_revenue_at_risk` measure. Look for the months where the line spiked — that's the consumer-sentiment or input-cost event that the portfolio absorbed (or didn't).

**Land the point:** Now Strategy and the CFO are looking at the same downside number with the same scenario definitions. The 'what if commodities run hot' conversation stops being a slide-build exercise and becomes a continuous read.

### Question (Act 1.2)

> **Top 10 categories by expected revenue under base scenarios — what is the optimal price change for each?**

**What to say while it runs:** Top categories by expected revenue under base scenarios with optimal price change beside. Optimal price change is the RGM recommendation engine output. CPG elasticity typically runs -0.3 to -0.6 — so a category recommending +4% with elasticity -0.4 is forecasting roughly 1.6% volume drop and a 2.4% margin lift.

**What to look for:** Ranked top-10 on `total_expected_revenue` with `avg_optimal_price_change`. The categories with the highest expected revenue *and* a positive optimal price change are the AOP-priority categories.

**Land the point:** That ranking is the price-action plan ready to walk into the next RGM steering meeting. The argument moves from 'we should think about pricing' to 'here are the 5 categories, here are the moves, here's the elasticity backing each one'.

---

## Act 2 — The decision — new-SKU launch vs. line-refurb capex *(≈4 min)*

**Persona:** S&OP Lead • **Job to be done:** Allocate the next-cycle capex between new-SKU launches in the high-elasticity / high-confidence categories and line-refurbishment in the categories with the most disruption exposure.

*Three questions that turn the scenario library into a defensible capex allocation. The middle question is the anchor — the revenue-at-risk to capex-recovery conversion that decides where the dollars go.*

### Question (Act 2.1)

> **Which channels show the highest disruption count, and how does that affect average simulated margin?**

**What to say while it runs:** Channels with the highest disruption count and their average simulated margin. Disruption scenarios are the adverse runs — supply break, demand collapse, competitive entry. A channel taking heavy disruption scenarios with margin compression is a channel where we need either pricing power, supply-chain investment, or an exit.

**What to look for:** Ranked `channel` by `disruption_count` with `avg_simulated_margin`. The channel where both numbers are bad is the channel that drives the capex argument for line-refurb.

**Land the point:** Channel exit and channel reinforcement are usually the slide-build exercise from hell. Now the S&OP lead and the CFO have the channel-by-channel disruption count and the margin compression in one view — the channel-strategy call gets made on evidence.

### Question (Act 2.2)

> **How has total simulated revenue trended month-over-month across consumer segments?**

**What to say while it runs:** Monthly trend in total simulated revenue across consumer segments. This is the topline confidence chart. A segment running flat under base scenarios with a wide downside band is a segment that needs portfolio defense; a segment running up with tight bands is the segment that earns the new-SKU launch budget.

**What to look for:** Monthly `total_simulated_revenue` split by `segment`. Look for the segment with rising base revenue and tight scenario dispersion — that's where investment lands; segments with flat revenue and wide bands are where we maintain, not expand.

**Land the point:** Segment-level investment used to be argued on intuition and last year's growth rate. Now the AOP segment allocation is anchored on simulated revenue with confidence bands — and Strategy walks into the board's portfolio review with the same numbers Finance is using to roll up the P&L.

> **Anchor moment.** Stop on the revenue-at-risk trend from Act 1 and the Invest-flagged top-10 on screen. Pick the worst-case downside — call it $25M of annual revenue-at-risk concentrated in 3 categories.

> *A typical CPG line refurbishment runs $3-5M and unlocks 15-20% throughput plus the OEE and shrink improvements that flow with it. If even 30% of that $25M downside is structural and refurb-addressable, that's $7-8M of recoverable revenue against a $3-5M investment — payback under 12 months on the worst-exposed plants. Meanwhile a new-SKU launch in an Invest category at FoodPlan's scale carries a $4-6M budget and the model projects $15-25M of incremental revenue at the 80% confidence band — a 3-4x return at half the execution risk of the refurb.*

> That's the capex-allocation call this space automates. Not the AOP slide. The dollars. New-SKU launch budget on dairy and protein, line-refurb capex on the bakery plant carrying the disruption exposure — both decisions signed in the same conversation, both backed by the same simulation library.

### Question (Act 2.3)

> **Top 10 categories flagged Invest investment priority — what is the projected revenue uplift?**

**What to say while it runs:** Top 10 categories flagged Invest investment priority with the projected revenue uplift. Invest categories are the ones the model is telling us to lean into — strong elasticity, strong sentiment, weak competitive pressure. The uplift number is the case-build for either the new-SKU launch or the marketing reinvestment.

**What to look for:** Filter `investment_priority='Invest'`, rank by `expected_revenue_usd`. The top 2-3 are the next-cycle launch candidates.

**Land the point:** That ranking *is* the new-SKU launch allocation. The S&OP lead, the brand team, and the CFO are looking at the same Invest-flagged categories with the same projected uplift — and the launch-portfolio decision gets made in one meeting instead of one quarter.

---

## Act 3 — The commitment — locking the AOP and the portfolio strategy *(≈4 min)*

**Persona:** VP of Strategy (with CFO) • **Job to be done:** Defend the portfolio-strategy recommendation to the executive team and lock the AOP price moves, the launch allocation, and the line-refurb capex.

*The VP doesn't need another scenario deck; they need the same expected-revenue and revenue-at-risk numbers the operating team is acting on, in the same language, so the board's portfolio review and the CFO's AOP commitment are anchored on one source.*

### Question (Act 3.1)

> **Which segments have the highest demand elasticity (most price-sensitive), and what are the recommended price moves?**

**What to say while it runs:** Segments by demand elasticity ranked most-to-least price-sensitive with recommended price moves. Elasticity is the price-pricing-power read — segments under -0.5 are the price-takers, segments closer to -0.2 are the categories with brand strength. The recommendation column tells you where the AOP price-move dollars land.

**What to look for:** Ranked by `demand_elasticity` from `scenario_runs` with `avg_optimal_price_change`. Watch for the segments where high elasticity meets a positive price recommendation — those are the gain-share moves.

**Land the point:** That's the AOP price card. Not a strategy slide — the actual recommended move per segment with the elasticity backing each one. The CFO signs the price plan and the brand team writes the trade-promo plan off the same artifact.

### Question (Act 3.2)

> **What is the monthly trend in average simulated margin, and which scenario types are pulling it down?**

**What to say while it runs:** Monthly trend in average simulated margin with the scenario types pulling it down. This is the portfolio-margin health view. When the disruption and pessimistic scenarios are pulling the trailing average down, that's the cue for capex on the most-exposed plants; when base and optimistic are pulling it up, that's the cue for launch-budget expansion.

**What to look for:** Monthly `avg_simulated_margin` with a `scenario_type` breakdown. The contribution of disruption scenarios to the margin compression is the leading indicator for capex prioritization.

**Land the point:** The board's portfolio review now has one chart: this one. The VP defends the AOP with the same simulation library the S&OP team uses to plan the production schedule — and next year's portfolio strategy stops being a committee decision and becomes a continuous one.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FoodPlan Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in total revenue at risk across all segments for the trailing 12 months.
2. Top 10 categories by expected revenue under base scenarios — what is the optimal price change for each?
3. Which channels show the highest disruption count, and how does that affect average simulated margin?
4. How has total simulated revenue trended month-over-month across consumer segments?
5. Top 10 categories flagged Invest investment priority — what is the projected revenue uplift?
6. Which segments have the highest demand elasticity (most price-sensitive), and what are the recommended price moves?
7. What is the monthly trend in average simulated margin, and which scenario types are pulling it down?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
