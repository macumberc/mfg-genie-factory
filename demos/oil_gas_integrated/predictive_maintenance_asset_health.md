# DeepHorizon Energy — Demo Script

**Space:** Oil & Gas Integrated — DeepHorizon Energy - Predictive Maintenance & Asset Health 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** Upstream VP and CFO + Asset Manager, Reliability Engineering Lead, Platform Production Engineer
**KPIs touched:** Average asset health score, MTBF, MTTR, Availability, Predicted RUL, Alarm + trip event count
**Big decision automated:** Which 3-5 critical rotating assets across the 6 platforms get refurbished now, which get replaced in the next turnaround, and which earn an emergency intervention — and how the avoided deferred-production saves the Upstream EBITDA print.

---

## Pre-demo checklist

- Open the Genie space `DeepHorizon Energy - Predictive Maintenance & Asset Health 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> DeepHorizon Energy operates 20 critical rotating assets — compressors, pumps, separators, gas-handling skids — across 6 offshore and onshore production facilities. Today the asset-health score lives in a Reliability Engineering team's OSIsoft PI dashboards, the MTBF/availability benchmarks sit in the platform reliability lead's monthly reliability deck, and the dollarized production-loss number is back-calculated by Asset Management from monthly accounting close. Three artifacts, same fleet — and the refurb-vs-replace call on a $5-10M compressor gets made in a turnaround planning meeting where each team brings a different version of the same asset. This space ends that. Health score, predicted RUL, MTBF, deferred production, repair cost — answered in the same conversation, against the same dollar impact, with the same definition of critical.

---

## Key KPIs in scope

- Average asset health score (0-100) — composite reliability index
- MTBF (days) — rotating equipment industry benchmark ~60-180 days
- MTTR (hours) — target <24h for repairable failures
- Availability (%) — IOGP target >97% for critical production equipment
- Predicted RUL (days) — early-warning lead time for planning
- Alarm + trip event count — high-severity sensor exceedances
- Production loss (bbl) — financial impact of unplanned downtime
- Repair cost ($) — direct maintenance spend by asset / failure mode

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MTBF** | Mean Time Between Failures |
| **MTTR** | Mean Time To Repair |
| **ROI** | Return on Investment |
| **RUL** | Remaining Useful Life |
| **VP** | Vice President |

---

## Act 1 — The signal — which assets are bleeding production today *(≈4 min)*

**Persona:** Platform Production Engineer • **Job to be done:** Identify the assets driving production loss right now and the platforms where the reliability slope is bending the wrong way.

*This is the production engineer's morning — used to be an hour stitching PI data against the maintenance log. Two questions in, the top-loss assets and the platform health curve are on screen.*

### Question (Act 1.1)

> **Top 10 assets by total production loss in barrels over the last 90 days.**

**What to say while it runs:** Top 10 assets by total production loss in barrels over the last 90 days. The point isn't the headline number — it's the *concentration*. In most IOC fleets, 60-70% of unplanned deferred production comes from 4 or 5 assets. If your top-10 list isn't heavily skewed, your data is averaged wrong.

**What to look for:** Ranked table of 10 assets by total_production_loss_bbl over 90 days. Watch the spread between the #1 asset and the #10 asset — a 5x gap is the signal that says the refurb conversation is a short list, not a fleet-wide program.

**Land the point:** That short list used to be the output of a week of cross-team reconciliation between Reliability and Asset Management. Now it's the input to the turnaround prioritization conversation that happens before the platform team's standup.

### Question (Act 1.2)

> **Show monthly average asset health score by platform for the trailing 12 months.**

**What to say while it runs:** Monthly average asset health score by platform over 12 months. IOGP target for critical equipment availability is over 97%; health scores correlate to that — anything trending below 70-75 is structurally weak fleet. The platform-level view is what tells you whether reliability is a fleet issue or a localized one.

**What to look for:** Monthly avg_health_score by platform_name — DATE_TRUNC('month', reading_timestamp). Look for platforms whose health curve is sloping down faster than the others; that's where the next critical-asset failure will originate.

**Land the point:** When the same health curve is on the production engineer's screen and the Asset Manager's screen and the Upstream VP's monthly review, the offshore-platform reliability conversation stops being about which dashboard is current.

---

## Act 2 — Refurb, replace, or run-to-fail — locking the turnaround AFE *(≈4 min)*

**Persona:** Reliability Engineering Lead • **Job to be done:** Convert the predicted-RUL and MTBF picture into a defensible refurb-vs-replace recommendation for the next turnaround AFE.

*Three questions that move the reliability conversation from individual work orders to fleet-level capital allocation. The middle question — MTBF trend — is the anchor that turns asset-health into a dollar conversation.*

### Question (Act 2.1)

> **Which assets have predicted remaining useful life under 30 days, and what platforms are they on?**

**What to say while it runs:** Assets with predicted remaining useful life under 30 days, and what platforms they're on. RUL under 30 days is the threshold that should trigger pre-emptive intervention scheduling — running a critical compressor or sea-water lift pump to failure on an offshore platform is the single most expensive thing that can happen on an asset.

**What to look for:** Table of assets with predicted_rul_days < 30 grouped by platform_name. Look for platforms with multiple assets in the under-30 bucket — that's a cluster, and a cluster is a turnaround-planning event, not a one-off work order.

**Land the point:** That list used to live in three different reliability engineers' notebooks. Now it's the work-order queue the Operations team commits against in the next planning meeting.

### Question (Act 2.2)

> **What is the trend in MTBF days month-over-month across all rotating equipment?**

**What to say while it runs:** MTBF days month-over-month across rotating equipment. The industry benchmark for rotating equipment MTBF is 60-180 days depending on duty. If the trend is flat or rising, your reliability program is working. If it's compressing — particularly in the under-90-day range — that's a structural reliability problem, and that's a capex story.

**What to look for:** Monthly mtbf_days trend across rotating equipment. Inflection points or sustained downtrends are what convert the conversation from O&M spend to capital allocation.

**Land the point:** When MTBF compression shows up in this view a quarter before it shows up in the availability print, the Reliability Lead has a real shot at converting the turnaround scope from like-for-like replacement to a targeted reliability upgrade.

> **Anchor moment.** Hold on the under-30-day RUL list and the MTBF compression curve together. Pick the worst-case asset — call it an offshore platform gas compressor with 20 days RUL on a platform producing 60,000 BOE/d.

> *If that compressor trips and takes the platform partially offline for 5 days while a spares plan executes, you're looking at roughly 200,000 BBL of deferred production at platform-level oil cut. At $70/BBL realized that's $14M of lost revenue. On top of that, an emergency intervention on an offshore platform is $250-500K/day in vessel and contractor cost — call it another $2M. Versus a planned refurb at the next turnaround at $3-5M, all-in. So the planned intervention saves $10-13M against the unplanned scenario on one asset. Across the 4-5 assets currently inside the 30-day RUL window, that's $40-60M of avoided unplanned downtime — and that's before counting the safety-and-environmental risk premium the Board now requires on offshore incidents.*

> That's the refurb-vs-run-to-fail call this space converts from a reliability-engineering opinion into a CFO-backed turnaround AFE. The dollar number is the headline; the predicted RUL is the trigger.

### Question (Act 2.3)

> **Which failure modes drove the highest repair cost this year?**

**What to say while it runs:** Failure modes ranked by repair cost this year. The Pareto on failure modes is usually the cleanest story in the deck — bearing failures, seal leaks, control-system trips. The cost-weighted ranking is what tells you where the reliability-engineering budget should actually go.

**What to look for:** Failure_mode by sum(repair_cost_usd) descending. Watch the top 2 or 3 failure modes — those are the ones a reliability-engineering capex case can target with measurable MTBF gain.

**Land the point:** Failure-mode-weighted spend is the conversation that turns reliability from a cost center into an EBITDA lever. The CFO will fund a $10M reliability program against the right Pareto chart — not against a generic uplift case.

---

## Act 3 — The program — defending the predictive maintenance ROI to the Upstream VP *(≈4 min)*

**Persona:** Asset Manager • **Job to be done:** Quantify the ROI of the predictive maintenance program and shape next year's reliability capex against the Upstream EBITDA target.

*The Asset Manager's job is to make the predictive-maintenance program defensible upstream. The ML-predicted-share and the alarm-trip trend are the two views that quantify the value of the program — not just its activity.*

### Question (Act 3.1)

> **Top 10 assets by alarm and trip event count this quarter — and how does that compare to last quarter?**

**What to say while it runs:** Top 10 assets by alarm and trip event count this quarter versus last quarter. The level matters less than the direction — assets where alarm activity is climbing are the assets where the next high-severity event originates. This is the leading indicator the program is designed to surface.

**What to look for:** Top 10 assets ranked by alarm_trip_count with a side-by-side comparison to last quarter. The deltas tell you which assets are aging vs. which were always alarm-noisy.

**Land the point:** Alarm trend by asset, quarter on quarter, in one query. That's the leading indicator the Upstream VP needs to know whether the reliability program is buying genuine MTBF gain or just shifting the spend distribution.

### Question (Act 3.2)

> **What share of maintenance events were predicted by the ML model, by asset type?**

**What to say while it runs:** Share of maintenance events that were predicted by the ML model, by asset type. This is the ROI question for the predictive-maintenance program. If the predicted-share is under 30%, the program isn't earning its keep. Over 60%, and it's funding itself many times over. The asset-type cut is where you find out which kinds of equipment the model serves well — and which need a different reliability strategy.

**What to look for:** Grouped table of count(was_predicted=true) over total event count by asset_type. Look for the asset types where predicted-share is highest — those are the segments where the program is defensible; the rest is the next investment case.

**Land the point:** Predicted-share by asset type is the metric that turns the predictive-maintenance program from a science project into a capital line item. With that number in hand, the Upstream VP can defend or expand the program against the Board on actual avoided-cost dollars.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — DeepHorizon Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 assets by total production loss in barrels over the last 90 days.
2. Show monthly average asset health score by platform for the trailing 12 months.
3. Which assets have predicted remaining useful life under 30 days, and what platforms are they on?
4. What is the trend in MTBF days month-over-month across all rotating equipment?
5. Which failure modes drove the highest repair cost this year?
6. Top 10 assets by alarm and trip event count this quarter — and how does that compare to last quarter?
7. What share of maintenance events were predicted by the ML model, by asset type?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
