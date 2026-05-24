# DriveWell Automotive — Demo Script

**Space:** Automotive — DriveWell - Vehicle Health & Maintenance Analytics 🚗
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director, Aftersales + Aftersales VP, Connected Services lead, Reliability/CFO partner
**KPIs touched:** Vehicle health score, DTC count per reading, Critical alert count, Predicted failure rate, Average repair cost, Warranty-covered service count
**Big decision automated:** Which 3-4 model/region cohorts get the next OTA-driven preventive service campaign, where warranty leakage demands a recall-vs-warranty escalation, and which dealer regions earn a CSAT-recovery intervention.

---

## Pre-demo checklist

- Open the Genie space `DriveWell - Vehicle Health & Maintenance Analytics 🚗`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> DriveWell — the connected-services arm of Apex Motor Group — runs telemetry across the in-warranty fleet (20 model variants spanning Apex Sedan, Horizon SUV, Titan Truck, Pulse EV, Venture Crossover, Sierra Wagon, Bolt Sport, Atlas Van, Ranger Pickup, and their hybrids) sold through 7 dealer regions (Northeast, Southeast, Midwest, Southwest, West Coast, Mountain, Pacific NW). Today the critical-alert count from the Connected Services lead's Splunk dashboard, the warranty-vs-cash repair cost from the Aftersales VP's monthly P&L file, and the predicted-failure-rate cohort report from the Reliability team's model-output CSV all describe the same vehicles — but they're never on the same table. The result: campaign prioritization gets made on whichever number landed loudest at the Monday call, and warranty leakage on a model nobody escalates becomes a recall 6 months later. Industry data shows predictive DTC monitoring cuts breakdowns by up to 75% and unplanned downtime by 50%, and emergency repairs cost 3–9x planned service — every campaign-prioritization mistake is paid for in the warranty line. This space puts telemetry, repair cost, CSAT, and forecast accuracy on one governed surface so the OTA-campaign and warranty-escalation decisions happen in the same room.

---

## Key KPIs in scope

- Vehicle health score — composite 0–100 telemetry rollup (engine, battery, tire, DTC)
- DTC count per reading — diagnostic trouble codes from OBD-II / J1939 streams
- Critical alert count — high-severity telemetry alerts requiring intervention
- Predicted failure rate (%) — forward-looking ML model output
- Average repair cost ($) — service event cost, planned vs emergency (3–9x gap)
- Warranty-covered service count — share of repairs under OEM warranty
- Customer satisfaction (CSAT) — post-service score on 1.0–5.0 scale
- Forecast accuracy — actual vs forecasted health score on monthly cohort

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **OEM** | Original Equipment Manufacturer |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the model/region cohorts before they become a Tuesday-morning emergency *(≈4 min)*

**Persona:** Connected Services lead • **Job to be done:** Pull tomorrow's preventive-service campaign list out of yesterday's telemetry — by model, by region, by alert pattern, before the first emergency repair lands.

*Every critical alert that becomes an unplanned breakdown is a 3–9x cost event vs. a planned service. The Connected Services lead has 24 hours to turn the telemetry signal into a dealer-network instruction.*

### Question (Act 1.1)

> **Show the monthly trend in average vehicle health score by connectivity tier for the trailing 12 months.**

**What to say while it runs:** Monthly trend in `avg_health_score` by `connectivity_tier`. The Elite/Premium tiers should run higher than Standard because we're seeing more telemetry on them — if Premium's health score is dropping while Standard is flat, we have a model-quality problem the telemetry caught and our reporting didn't.

**What to look for:** Three lines from `vehicle_telemetry_metrics` — Elite, Premium, Standard — over the trailing 12 months. Watch for a tier dropping below 75; that's the line where the dealer network starts seeing complaints.

**Land the point:** Now the Connected Services lead can flag a quality drift in week 2, not week 10. That's the difference between an OTA campaign and a multi-region warranty surge.

### Question (Act 1.2)

> **Top 10 vehicle models with the highest critical alert count over the last 90 days.**

**What to say while it runs:** Top 10 vehicle models with the highest `critical_alert_count` over the last 90 days. Critical alerts are the part the dealer network feels — battery, engine temp, ABS DTCs that throw a check-engine light. The model ranking is the campaign-prioritization list, full stop.

**What to look for:** Ranked table — `model` × `critical_alert_count` from `vehicle_telemetry_metrics` filtered to the last 90 days. The top of the list is the next OTA campaign or service-bulletin; the bottom is where the fleet is healthy.

**Land the point:** Right there is the campaign queue. Before this space, that ranking was a Splunk export plus a half-day of Excel correlation. Now it's a 30-second query — and the dealer-bulletin conversation starts at 9 AM instead of after lunch.

---

## Act 2 — The decision — recall, warranty, or service-bulletin — and which region earns the campaign first *(≈4 min)*

**Persona:** Aftersales VP • **Job to be done:** Decide which model/region cohort gets a preventive-service campaign, where warranty leakage justifies a recall escalation, and which dealer regions need a CSAT intervention.

*Three questions that turn the alert backlog into a defensible aftersales action plan. The middle question is the anchor — the warranty-vs-emergency cost math that decides which campaigns get funded.*

### Question (Act 2.1)

> **Which service regions have the highest average repair cost, and what service types are driving it?**

**What to say while it runs:** Which `service_region` has the highest `avg_labor_hours` and `total_repair_cost`, and what `service_type` is driving it? A region that's running 30% above network average on emergency repairs has either a dealer-training problem or a model-deployment problem — and either way it's a campaign target.

**What to look for:** Pivot — region × service_type with `total_repair_cost` and `avg_labor_hours` from `maintenance_records_metrics`. Watch for Emergency Repair lighting up red in one region — that's the cohort where the OTA campaign actually pays for itself.

**Land the point:** That table is the campaign-targeting brief. Before this space, the Aftersales VP heard about regional cost spikes from a P&L variance report 6 weeks late. Now it's a row on screen — and the dealer-network campaign goes out before the next billing cycle.

### Question (Act 2.2)

> **How does warranty-covered service count compare to total service records by model this year?**

**What to say while it runs:** `warranty_covered_count` vs `total_service_records` by model this year. The ratio is the warranty-leakage signal. Industry benchmarks say healthy programs run 60–70% of in-warranty work covered; below 50% and the warranty terms or the diagnostic process is failing — and the customer is paying for what we should be covering.

**What to look for:** Paired bars by model — covered count vs total service. Watch for the Pulse EV or Ranger Pickup where the ratio is low — that's either a dispute pattern or a campaign-vs-recall escalation candidate.

**Land the point:** When the Aftersales VP, the Reliability team, and Legal all see the same warranty-leakage number, the *do we recall or do we warranty-bulletin* conversation moves from a quarterly review to a same-week decision. That's a recall-clock that doesn't get triggered, or a recall-clock that gets triggered before NHTSA does it for us.

> **Anchor moment.** Stop on the warranty-leakage ratio and the regional repair-cost table. Take the Ranger Pickup in the Southwest region — say it's showing `warranty_covered_count` at 40% of total service records with `avg_repair_cost` 25% above network average.

> *Industry warranty-claim cost averages $400–$1,500 per claim depending on component (parts + labor + diagnostic time). If the Ranger Pickup in Southwest is running 1,500 service events per quarter at $900 average and we're under-covering by 20 points, that's 300 events × $900 = $270K/quarter the customer is paying out-of-pocket that arguably should be warranty — and every one of those is a CSAT event and a recall-petition risk. Multiply across 4 model/region cohorts with similar leakage and we're looking at $1.0–1.5M/quarter, $4–6M/year of customer-experience exposure that's currently invisible in the warranty P&L. On the other side, an emergency repair averages 3–9x the planned-service cost; if predictive DTC monitoring catches even 30% of that volume before it becomes emergency work, that's another $2–3M/year of avoided cost on the warranty line.*

> That's the decision this space automates. Not the dashboard. The campaign-launch and warranty-escalation call. The OTA-driven preventive campaign on the Ranger Pickup Southwest cohort gets funded this week, the warranty-coverage policy gets a same-week review for the leaking models, and the Aftersales VP walks into the executive review with the dollar number — not a CSAT anecdote.

### Question (Act 2.3)

> **What is the trend in average DTC count per reading month-over-month, and which models are above the fleet average?**

**What to say while it runs:** Trend in `avg_dtc_count` per reading month-over-month, sliced by model — and which models are above the fleet average. A rising DTC trend on one model is the leading indicator of a campaign or, worse, a quality escape we haven't filed yet.

**What to look for:** Monthly trend lines by model. Spotting a model where DTC count climbs 2 months in a row while the rest of the fleet is flat — that's the model that needs an engineering-team root-cause review *now*.

**Land the point:** That's the difference between knowing a model has problems and knowing it's *getting worse*. The first is a status report; the second is a campaign-launch decision.

---

## Act 3 — The commitment — locking next quarter's campaign budget and the recall-vs-warranty policy *(≈4 min)*

**Persona:** Reliability/CFO partner • **Job to be done:** Defend the aftersales investment plan to executive leadership — campaign budget, warranty-coverage policy, and predicted-failure-driven OTA priorities for the next quarter.

*The Reliability/CFO partner doesn't need a deeper data dive; they need the same numbers the Aftersales VP and the Connected Services lead are acting on, framed against predicted-failure forecasts that the executive team will challenge.*

### Question (Act 3.1)

> **Top 10 models by total repair cost — and what share of those repairs were warranty-covered?**

**What to say while it runs:** Top 10 models by `total_repair_cost` — and what share of those repairs were warranty-covered? This is the warranty-P&L picture on one screen. The high-cost / low-coverage models are the ones the CFO is going to ask about.

**What to look for:** Ranked list by `total_repair_cost` with `warranty_covered_count` as a side column. Watch for models where coverage is low and repair cost is high — those are the recall-escalation candidates.

**Land the point:** When the CFO partner walks into the executive review with this list, the conversation is *here's the $X of leakage and here's the campaign that recovers $Y of it* — not *we'll know next quarter*. That's the warranty-P&L conversation that used to need a steering committee.

### Question (Act 3.2)

> **How accurate were our monthly predicted vs actual health scores by model over the trailing 12 months?**

**What to say while it runs:** Monthly `forecasted_health_score` vs `actual_health_score` by model over the trailing 12 months. The forecast accuracy is the credibility check on our predictive-failure model — if we're missing by 5+ points consistently on one model, we don't trust its `predicted_failure_rate` for next quarter's campaign-prioritization decision.

**What to look for:** Paired lines from `vehicle_health_monthly`. Look for the gap between forecasted and actual on specific models — that's where the predictive model needs retraining before next planning cycle.

**Land the point:** Three artifacts — campaign queue, warranty-leakage list, forecast-accuracy check — all from one governed surface. The Connected Services lead, the Aftersales VP, and the CFO partner are now committing to the same numbers. The OTA-campaign budget and the warranty-coverage policy become one decision instead of three meetings.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — DriveWell Automotive — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in average vehicle health score by connectivity tier for the trailing 12 months.
2. Top 10 vehicle models with the highest critical alert count over the last 90 days.
3. Which service regions have the highest average repair cost, and what service types are driving it?
4. How does warranty-covered service count compare to total service records by model this year?
5. What is the trend in average DTC count per reading month-over-month, and which models are above the fleet average?
6. Top 10 models by total repair cost — and what share of those repairs were warranty-covered?
7. How accurate were our monthly predicted vs actual health scores by model over the trailing 12 months?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
