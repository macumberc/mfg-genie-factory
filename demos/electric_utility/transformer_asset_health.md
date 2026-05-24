# GridGuard Utilities — Demo Script

**Space:** Electric Utility — GridGuard Utilities - Transformer Asset Health ⚡
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP T&D + CFO, Asset Manager, Substation Engineer
**KPIs touched:** Transformer health index, Dissolved gas, Top oil temperature, Load factor, Critical alert count, Forecasted maintenance cost
**Big decision automated:** Which 3-5 transformers in the fleet get replaced this cycle, which get refurbished, and which get run-to-failure — given $200K-$2M unit cost, 18-month lead times, and the customer-minute exposure if a 345kV bank fails in July.

---

## Pre-demo checklist

- Open the Genie space `GridGuard Utilities - Transformer Asset Health ⚡`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> GridGuard Utilities operates 20 power transformers across 12 substations spanning 69kV through 345kV — from Oakdale's 32-year-old 345kV main banks to Grandview's 5-year-old tie bank. Today the DGA results live in the Substation Engineer's IEEE C57.104 spreadsheet, the load-and-thermal trend lives in the SCADA historian, and the remaining-useful-life and forecasted-maintenance-cost slide gets rebuilt every quarter for the Asset Manager's capital review. Three artifacts, three update cadences, and a replacement decision that gets made on the oldest-equipment-first rule — which is how an 8-year-old 345kV Hitachi unit at Hillcrest can have a critical DGA trend nobody triages while we order a replacement for a 35-year-old 69kV Pinewood feeder that's running at 40% load with a 70 health index. This space puts DGA, oil temperature, load percentage, health index, critical alerts, failure events, repair costs, remaining useful life, and forecasted maintenance in one governed surface — so the replace/refurbish/run-to-fail decision tracks asset condition, not asset age.

---

## Key KPIs in scope

- Transformer health index (0-100) — composite score; <50 triggers inspection, <30 replacement review
- Dissolved gas (ppm) — IEEE C57.104 thresholds: >500 ppm Watch, >1000 ppm Warning, >2500 ppm Critical
- Top oil temperature (°C) — sustained >95°C accelerates insulation aging (Arrhenius)
- Load factor (% of rated capacity) — >100% triggers loss-of-life concerns
- Critical alert count — operational backlog for asset engineering
- Forecasted maintenance cost ($) — 12-month capex/opex planning input
- Remaining useful life (years) — drives replacement prioritization
- Total repair cost & customer-minutes — reliability $ exposure per event

---

## Act 1 — The signal — finding the next failure before it's a 4 AM phone call *(≈4 min)*

**Persona:** Substation Engineer • **Job to be done:** Pull tomorrow's inspection priorities out of yesterday's sensor data — health index, DGA, oil temperature — not from a quarterly inspection calendar.

*This is the conversation that turns a routine SCADA scan into a same-week field-inspection order. Two questions surface the transformer condition that the age-based PM schedule misses.*

### Question (Act 1.1)

> **Which 10 transformers have the lowest average health index over the last 90 days?**

**What to say while it runs:** The 10 transformers with the lowest avg health_index over the last 90 days. Health index under 50 is inspection territory; under 30 is replace-or-refurbish review. The interesting tell is *young* transformers near the bottom — those aren't end-of-life, those are early failures the original PM cadence wasn't designed to catch.

**What to look for:** Ranked table: transformer_name, substation, avg health_index, voltage_class. The room should notice that the lowest-health transformer might be a Hillcrest 345kV unit that's only 12 years old — not the 35-year-old Pinewood feeder everyone expected.

**Land the point:** Right there is the gap between condition-based and age-based maintenance. The Substation Engineer can defend a same-week inspection on a relatively young 345kV unit — because the data says so, not because the calendar said so.

### Question (Act 1.2)

> **Show monthly trend of critical alert count by substation for the trailing 12 months.**

**What to say while it runs:** Top 10 transformers by max_dissolved_gas_ppm — which are above the 1000 ppm IEEE C57.104 Warning threshold. DGA is the gold-standard internal-condition indicator: <500 ppm is Normal, 500-1000 Watch, 1000-2500 Warning, >2500 is Critical — an *active fault* is occurring inside the tank. A 345kV transformer in the Warning band is a 4-week decision window before it becomes a forced outage.

**What to look for:** Ranked table: transformer_name, max_dissolved_gas_ppm, voltage_class. The room should notice the units crossing 1000 ppm and the ones already at 2500+ — those are decisions, not data points.

**Land the point:** Before this space, that list got rebuilt by hand from quarterly DGA lab returns. Now it's the *first* question of the asset-engineering day — and the inspection queue gets built on parts-per-million, not on a 90-day calendar.

---

## Act 2 — The decision — replace, refurbish, or run-to-fail *(≈4 min)*

**Persona:** Asset Manager • **Job to be done:** Commit to the next 12-month replacement and refurbishment list — the AFE that has to clear before the long-lead transformer orders go to procurement.

*Three questions convert the daily condition signal into a defensible capital recommendation. The middle question is the anchor — forecasted maintenance cost, remaining useful life, and customer-minute exposure converted into the dollar-of-deferred-failure number the CFO is going to ask about.*

### Question (Act 2.1)

> **Top 10 transformers by maximum dissolved gas reading — which are above the 1000 ppm Warning threshold?**

**What to say while it runs:** Monthly trend of critical_alert_count by substation over 12 months. A single critical alert is a data point; a substation with sustained critical alerts month-over-month is a *system*-level issue — could be cooling, could be loading, could be a manufacturing-cohort defect across a vintage of units. That's a substation-wide refurbishment conversation, not a single-unit one.

**What to look for:** Monthly trend, critical_alert_count by substation. The room should notice substations with persistent critical alerts vs. one-time spikes — those are different problems.

**Land the point:** When the critical-alert trend is on the same screen as the health-index ranking, the conversation about whole-substation refurbishment vs. single-unit replacement starts being data-driven — not 'whichever capex is shovel-ready'.

### Question (Act 2.2)

> **What is total repair cost and customers affected by root cause for the trailing 12 months?**

**What to say while it runs:** Total_repair_cost_usd and total_customers_affected by root_cause for the trailing 12 months. Insulation Degradation and Oil Contamination together usually drive most of the repair spend; Bushing Failure typically drives the worst customer impact per event. That breakdown tells us whether the dollars and the customer-minutes are coming from the same failure modes — they often aren't.

**What to look for:** Root-cause table: total_repair_cost_usd, total_customers_affected. The room should notice the gap between *spend driver* and *customer-impact driver* — a $30K bushing failure that took out 8,000 customers is a worse event than a $200K insulation refurbishment we scheduled.

**Land the point:** That comparison is the difference between *managing repair spend* and *managing reliability exposure*. The first is an opex line; the second is the rate-case headline. They are not the same problem and they don't get the same capital.

> **Anchor moment.** Hold the DGA leaderboard and the remaining-life table on screen. Pick the worst 345kV unit — Oakdale Main Bank A, 32 years old, DGA above 2500 ppm, remaining life under 3 years, criticality 'Critical'.

> *A new 345kV power transformer runs $1.5-2M for the unit itself, $300-500K for installation, plus 12-18 months of lead time. Refurbishment (oil filtration, bushing replacement, gasket overhaul) runs $200-400K and buys 5-7 years — *if* the insulation hasn't degraded structurally. Uninsured failure of a 345kV bank in July: $500K-3M for the asset plus emergency replacement plus 8-24 hours of outage. At $5-50/MWh for unserved energy and a substation serving 50,000+ customers, an 8-hour outage in summer peak is 100+ MWh of unserved energy — $500K-$5M depending on how the PUC calculates it. Across the 4-5 transformers in the bottom-remaining-life tier, the difference between *plan and replace* and *run-to-fail* is $10-20M of reliability-and-replacement exposure that the rate case absolutely sees. And the 18-month lead time means the AFE clears *now* or we own the exposure for the next two summers.*

> That's the decision this space automates. Replace/refurbish/run-to-fail get set on the same screen as the live DGA, the forecasted maintenance, and the remaining-life curve — not in next quarter's capital review deck. The procurement lead times mean the data has to drive the decision *this* month.

### Question (Act 2.3)

> **Which transformers have the lowest remaining useful life, and what is the forecasted maintenance cost for each?**

**What to say while it runs:** The transformers with the lowest remaining_useful_life_years with their forecasted_maintenance_cost_usd. Remaining life under 5 years means the asset is on the replacement clock — but if forecasted maintenance is climbing, the *economic* end-of-life is already here. The two numbers together tell us refurbish, replace, or harvest.

**What to look for:** Ranked table: transformer_name, remaining_useful_life_years, forecasted_maintenance_cost_usd, voltage_class. The room should notice that some 345kV units have low remaining life *and* high forecasted maintenance — those are the headline replacement candidates.

**Land the point:** Right there is the AFE list. The Asset Manager walks into the capital review with the transformers named, the dollars attached, and the customer-minute exposure quantified.

---

## Act 3 — The commitment — multi-year transformer replacement program and reliability defense *(≈4 min)*

**Persona:** VP T&D • **Job to be done:** Defend the transformer-fleet replacement program to the CFO and the rate-case team — lock in next year's replacement AFE, refurbishment opex, and the customer-minute-exposure narrative for the PUC.

*The VP doesn't need a new dashboard. They need the same health, DGA, repair, and remaining-life numbers the asset team is acting on, in capital-plan and rate-case form, so the program narrative writes itself.*

### Question (Act 3.1)

> **How has average oil temperature trended month-over-month for 345kV assets during summer months?**

**What to say while it runs:** Avg oil_temperature trended month-over-month for 345kV assets during summer months. Sustained oil temp above 95°C accelerates insulation aging by Arrhenius — every 7-8°C above design roughly doubles the rate. A 345kV bank running 100°C all summer is shortening its life by years vs. one running 80°C. That tells us whether the cooling system upgrades on the AFE list are *thermal-stress-justified* or just nice-to-haves.

**What to look for:** Monthly trend, avg oil_temp_celsius for voltage_class = '345kV' in June-September. The room should notice the units that ran hot last summer — those are the cooling-upgrade candidates, regardless of DGA.

**Land the point:** When the thermal trend is on the same screen as the DGA and the remaining-life, the cooling-system capex ask becomes a *life-extension* program — not just maintenance. That's the framing the CFO funds.

### Question (Act 3.2)

> **Which substations have the highest failure event count and total customer-minutes interrupted this year?**

**What to say while it runs:** Substations with the highest failure event count and total customers_affected this year. Substation-level concentration is the rate-case headline. If two substations own 60% of the reliability exposure, the AFE next year concentrates there — and the PUC sees a targeted plan, not a peanut-butter spread.

**What to look for:** Substation-level ranked table: total_failure_events, total_customers_affected. The room should notice Oakdale (aged 345kV banks) and Lakewood (aged 138kV) typically dominating — those are the program's anchor substations.

**Land the point:** Triage at 8, AFE list at 10, rate-case prep at 2. Same space, same numbers. The Substation Engineer's inspection queue, the Asset Manager's replacement list, and the VP T&D's PUC narrative are now the same artifact — and the regulator gets one transformer-program story instead of three reconciliations.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — GridGuard Utilities — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 transformers have the lowest average health index over the last 90 days?
2. Show monthly trend of critical alert count by substation for the trailing 12 months.
3. Top 10 transformers by maximum dissolved gas reading — which are above the 1000 ppm Warning threshold?
4. What is total repair cost and customers affected by root cause for the trailing 12 months?
5. Which transformers have the lowest remaining useful life, and what is the forecasted maintenance cost for each?
6. How has average oil temperature trended month-over-month for 345kV assets during summer months?
7. Which substations have the highest failure event count and total customer-minutes interrupted this year?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
