# ReservoirSight Analytics — Demo Script

**Space:** Oil & Gas Upstream — ReservoirSight Analytics - Reservoir Management 🛢️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Reserves + Reservoir Engineer, Asset Manager, VP of Reserves
**KPIs touched:** Oil rate and gas rate, Water cut %, GOR, Recovery factor %, Annual decline rate %, Cumulative oil and estimated ultimate recovery
**Big decision automated:** Whether to sign the EOR / waterflood AFE on the two worst-watered reservoirs, where to land the next 3-5 infill wells, and which formations get a type-curve revision that reshapes next year's PV-10.

---

## Pre-demo checklist

- Open the Genie space `ReservoirSight Analytics - Reservoir Management 🛢️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> ReservoirSight Analytics covers 20 reservoirs across the Permian (Wolfcamp, Bone Spring, Spraberry), Eagle Ford, Williston, Marcellus / Utica, Haynesville, DJ Basin, and Anadarko. Today the decline-curve plots live in the Reservoir Engineer's IHS Harmony / ARIES exports, the OPEX-per-BOE benchmark lives in the Asset Manager's monthly financial pack, and the EUR / recovery-factor numbers go into a separate reserves committee deck once a quarter. Three artifacts, same subsurface — and the EOR sign-off, the infill program, and the next type-curve revision get decided in three different meetings, sometimes with three different numbers. This space ends that. The water-cut surveillance the engineer does on Monday is the same view the VP of Reserves takes to the reserves committee on Friday — and the capital decision behind it is a $50-300M call.

---

## Key KPIs in scope

- Oil rate (BOPD) and gas rate (MCF/day) — primary production volumes
- Water cut % — sweep efficiency; >50% signals watered-out wells, >75% near-economic-limit
- GOR (gas-oil ratio, SCF/BBL) — reservoir energy/phase indicator
- Recovery factor % — shale typically 5-12%, conventional 25-50%
- Annual decline rate % — shale wells often 30-50% Y1, 12-20% in later years
- Cumulative oil (BBL) and estimated ultimate recovery (EUR)
- OPEX per BOE — onshore US benchmark ~$8-15/BOE
- Breakeven price (USD/BBL) — Permian Tier-1 ~$35-45, marginal acreage $55+

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **BBL** | Barrels |
| **BOE** | Barrels of Oil Equivalent |
| **BOPD** | Barrels of Oil Per Day |
| **EUR** | Estimated Ultimate Recovery |
| **GOR** | Gas-Oil Ratio (SCF/BBL) |
| **MCF** | Thousand Cubic Feet (gas volume) |
| **OPEX** | Operating Expense |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the reservoirs the type curve no longer fits *(≈4 min)*

**Persona:** Reservoir Engineer • **Job to be done:** Surface the reservoirs where actual production is diverging from the planned decline curve — before the reserves committee asks why.

*This is where the type-curve revision conversation starts. The engineer needs the divergence list ranked by material impact, not alphabetical by reservoir name.*

### Question (Act 1.1)

> **Top 10 reservoirs by average oil rate (BOPD) over the last 90 days.**

**What to say while it runs:** Top 10 reservoirs by average oil rate BOPD over the last 90 days — that's the top of the production stack. Pay attention to the *spread*. Tier-1 Permian wells produce 800-1500 BOPD initially; the gap between top and bottom is where the type-curve story is hiding.

**What to look for:** Ranked table — reservoir_name, formation, basin, avg_oil_bpd. Click Show generated code once — the room sees that avg_oil_bpd comes from the governed metric view, not a one-off SQL.

**Land the point:** That's the reservoir engineer's starting watchlist. The reservoirs at the top right now are the ones funding next year's drilling program; the reservoirs at the bottom are either harvest candidates or EOR candidates — and we'll separate those two in act 2.

### Question (Act 1.2)

> **Show the monthly trend in average water cut and decline rate by basin for the trailing 12 months.**

**What to say while it runs:** Now monthly trend in avg water_cut_pct and avg decline_rate_pct by basin over the trailing 12 months. Water cut above 50% means sweep is faltering, above 75% the reservoir is near its economic limit. Shale decline is usually 30-50% in Year 1, 12-20% later. Basins outside those bands need an explanation.

**What to look for:** Dual-axis monthly trend, faceted by basin. Watch for basins where both lines are climbing — that's the classic mature-asset signature and the EOR conversation gets opened there.

**Land the point:** Before this space, the Reservoir Engineer rebuilt that chart for every reserves review. Now it's the Monday-morning surveillance view, and the type-curve revision proposal walks into the committee with the basin trend already attached.

---

## Act 2 — The decision — EOR sign-off, infill drilling, or harvest *(≈4 min)*

**Persona:** Asset Manager • **Job to be done:** Decide which 2-3 reservoirs get an EOR AFE this cycle, which 3-5 infill locations earn the next drilling slot, and which assets move to harvest mode.

*Three questions that convert subsurface data into capital allocation. The middle question — OPEX and breakeven by basin and formation — is the anchor; that's where the economics decide which reservoirs earn capital vs. produce to economic limit.*

### Question (Act 2.1)

> **Which reservoirs have water cut above 60% and what is their cumulative oil and recovery factor?**

**What to say while it runs:** Reservoirs with water_cut_pct above 60% plus their cumulative_oil_bbl and recovery_factor_pct. The combination is what matters. High water cut with low recovery factor — say 8% — is a waterflood candidate. High water cut with already-high recovery — say 25% — is at economic limit. Same number, totally different decision.

**What to look for:** Filtered table — reservoir_name, water_cut_pct, cumulative_oil_bbl, recovery_factor_pct. The bottom rows are the EOR target list; the top rows are the abandonment study.

**Land the point:** That table is the EOR / abandonment short list the asset team used to spend three weeks generating from IHS + the AFE system + the well files. Now it's a question — and the conversation with the VP of Reserves moves from *do we have time to evaluate* to *which two reservoirs do we pull AFEs for*.

### Question (Act 2.2)

> **What is the average OPEX per BOE and breakeven price by basin and formation this year?**

**What to say while it runs:** Average opex_per_boe and breakeven_price_usd by basin and formation this year. Permian Tier-1 breakeven is $35-45; marginal acreage is $55+. OPEX benchmark onshore is $8-15/BOE. Anything in the upper-right of those ranges is a structural ask — either lower OPEX through automation or harvest the position.

**What to look for:** Matrix by basin and formation. The formations above $15/BOE OPEX *or* above $55/BBL breakeven are the structural conversations — these aren't quarter-by-quarter issues, they're portfolio composition decisions.

**Land the point:** When OPEX/BOE and breakeven sit in the same governed surface, the assertion *this reservoir is uneconomic at strip* is no longer an opinion — it's a chart. That changes the abandonment conversation from a quarterly debate into a one-meeting decision.

> **Anchor moment.** Stop on the breakeven + OPEX matrix and the EUR-vs-cumulative chart together. Pick the two highest-EUR reservoirs sitting at 60%+ recovery with water cut above 60% — typical EOR / waterflood AFE on a target like that is $50-150M of capital and 5-15% lift on PV-10.

> *Take a reservoir at 40 million bbl EUR currently producing 70% water. A waterflood study sized to add even 8% recovery factor adds roughly 3.2 million incremental barrels. At $70 oil, that's $224M of gross revenue, $80-120M of PV-10 against a $75M AFE — payback inside 4 years. Across the two top EOR candidates, the program is a $400-500M PV uplift against a $150M capital ask. Now invert the screen — the four reservoirs in the upper-right of the OPEX / breakeven matrix at 25%+ recovery with no infill upside are harvest assets, and the OPEX dollars get re-allocated to the EOR.*

> That is the AFE conversation this space automates. Not the slide. The decision. The EOR sign-off and the abandonment list come out of the same question set — and the reserves committee gets one number, not three.

### Question (Act 2.3)

> **Top 10 reservoirs by estimated ultimate recovery (EUR) — and how does that compare to cumulative oil produced?**

**What to say while it runs:** Top 10 reservoirs by estimated_eur_bbl with their cumulative oil produced. The ratio — produced over EUR — is recovery progress. Reservoirs at 60%+ of EUR are mature; reservoirs at 15% are early. The early ones with high EUR are the infill targets; the mature ones are the EOR targets.

**What to look for:** Side-by-side bar — estimated_eur_bbl and cumulative_oil_bbl. The gap between the two bars is the remaining-recoverable; the ratio is the maturity flag.

**Land the point:** That single view answers two AFE questions at once — where to drill the next infill, and where to bring forward an EOR study. Two capital decisions out of one question is the shape of this space.

---

## Act 3 — The commitment — defending reserves and shaping the type-curve revision *(≈4 min)*

**Persona:** VP of Reserves • **Job to be done:** Walk into the reserves committee with the type-curve revision, defend the breakeven, and lock in next year's drilling and EOR capital.

*The reserves committee doesn't want another dashboard; they want the engineer's surveillance numbers and the asset manager's economics in the same view, in the language of EUR, recovery factor, and breakeven.*

### Question (Act 3.1)

> **How has reservoir pressure trended month over month for Permian Basin wells?**

**What to say while it runs:** Reservoir pressure trend month over month for Permian Basin wells. Pressure decline is the leading indicator the reserves committee uses to age the asset — and to decide whether the EUR number we've been carrying is still defensible. If pressure is falling faster than the type curve predicts, the type curve needs a revision.

**What to look for:** Monthly trend of avg_reservoir_pressure for Permian. Inflection points are what shape the type-curve revision proposal — and the type curve sets next year's AFE assumptions.

**Land the point:** When the pressure curve, the decline curve, and the water-cut curve all live in the same space, the type-curve revision is a one-meeting decision, not a quarter-long study. And a 5-15% revision on PV-10 across a $2-3B asset base is the kind of number that moves the company's whole capital plan.

### Question (Act 3.2)

> **Which formations have the steepest annual decline rates, and what is their monthly oil volume?**

**What to say while it runs:** Formations with the steepest annual decline rates and their monthly oil volume. Steep decline plus high volume means we're harvesting; steep decline plus low volume is a candidate for either restimulation or shut-in. The formation-level cut is how the drilling program gets reshaped year over year.

**What to look for:** Table — formation, avg_decline_rate, monthly_oil_bbl. The top-right corner of that table is the next program's drilling target list; the bottom-right is the restimulation candidates.

**Land the point:** Same space the reservoir engineer used Monday morning. Same numbers. The infill program, the EOR list, and the type-curve revision are the *same artifact* — and the reserves committee gets one defensible story instead of three competing decks.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — ReservoirSight Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 reservoirs by average oil rate (BOPD) over the last 90 days.
2. Show the monthly trend in average water cut and decline rate by basin for the trailing 12 months.
3. Which reservoirs have water cut above 60% and what is their cumulative oil and recovery factor?
4. What is the average OPEX per BOE and breakeven price by basin and formation this year?
5. Top 10 reservoirs by estimated ultimate recovery (EUR) — and how does that compare to cumulative oil produced?
6. How has reservoir pressure trended month over month for Permian Basin wells?
7. Which formations have the steepest annual decline rates, and what is their monthly oil volume?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
