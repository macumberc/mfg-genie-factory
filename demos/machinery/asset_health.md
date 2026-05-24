# IronPulse Manufacturing — Demo Script

**Space:** Machinery — IronPulse Manufacturing - Asset Health Monitor 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Operations + Reliability Engineer, Plant Manager, CFO
**KPIs touched:** Health index, Vibration velocity, Remaining useful life, Asset availability, Mean time between failures, Unplanned downtime hours
**Big decision automated:** Which 3-5 of the 20 industrial assets get refurbished vs. retired next budget cycle, and how much of the predictive maintenance program survives the CFO review.

---

## Pre-demo checklist

- Open the Genie space `IronPulse Manufacturing - Asset Health Monitor 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> IronPulse runs 20 heavy rotating assets — Atlas Copco and Ingersoll Rand compressors, Sulzer and Flowserve pumps, Siemens Energy and GE Vernova turbines, Flender and SEW-Eurodrive gearboxes, ABB motors — across five plant areas: Utilities, Process, Power Gen, Milling, Conveyor. Today the Reliability Engineer lives in the SCADA historian and a vibration analyst's spreadsheet, the Plant Manager tracks availability in a monthly Excel rolled up from CMMS work orders, and the CFO's view of the predictive maintenance program is one slide in a quarterly deck. Three views, twenty assets, and the refurbish-vs-retire decision still gets made on which superintendent argues loudest. This space replaces that with a single governed surface where ISO 10816 vibration zones, health index, availability, and maintenance spend all resolve to the same number — and the PdM program's ROI defends itself.

---

## Key KPIs in scope

- Health index (0–100) — composite condition score; <50 triggers planned intervention
- Vibration velocity (mm/s) — ISO 10816 zones: Good <4.5, Alert 4.5–11.2, Danger ≥11.2
- Remaining useful life (days) — predictive horizon to plan parts and labor
- Asset availability (%) — world-class target ≥90%, leaders 95%+
- Mean time between failures (MTBF) — heavy rotating equipment benchmark 4,000–8,000 hrs
- Unplanned downtime hours — direct production-loss driver
- Prediction catch rate — % of failures detected before breakdown (target ≥60%)
- Maintenance cost ($) per asset — capex deferral and opex budget input

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **MTBF** | Mean Time Between Failures |
| **ROI** | Return on Investment |
| **RUL** | Remaining Useful Life |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the assets bleeding hours before the morning safety meeting *(≈4 min)*

**Persona:** Reliability Engineer • **Job to be done:** Identify which assets are silently dragging availability so today's intervention list isn't shaped by yesterday's loudest breakdown.

*This is the conversation where the workorder backlog gets re-prioritized for the week. Two questions in, the engineer already has the list that used to take a half-day of cross-referencing.*

### Question (Act 1.1)

> **Top 10 assets by unplanned downtime hours in the last 90 days, and what was their average health index?**

**What to say while it runs:** Most reliability teams sort by failure count — but the dollar-driver is downtime hours, weighted by what health index those same assets were sitting at. A Turbine at health index 45 with 30 unplanned downtime hours is a very different conversation than a Motor at 70 with 30 hours. We want the first one.

**What to look for:** A ranked table of 10 assets — unplanned_downtime_hours alongside their avg_health_index. Watch for the assets where both numbers are bad; those are the ones the program has been losing on.

**Land the point:** Right there is the refurbish-or-retire shortlist. The Reliability Engineer can build it in two minutes instead of waiting on the next monthly health report — and the workorder schedule gets reshaped today, not next week.

### Question (Act 1.2)

> **Show monthly trend in average health index by asset type across the trailing 12 months.**

**What to say while it runs:** Now the trend on average health index by asset class. This is the chart that tells the PdM program whether it's bending the curve or just measuring failure. A health index above 80 is healthy, 50-79 is watch, below 50 is critical.

**What to look for:** Monthly lines across Compressors, Pumps, Turbines, Gearboxes, Motors. Watch for an asset class drifting from Watch into Critical territory — that's a structural reliability problem, not a one-off failure.

**Land the point:** When that curve is in the engineer's hand a quarter before availability slips, the Plant Manager stops getting blindsided in the operations review. That's the difference between a reliability program and a firefighting program.

---

## Act 2 — Refurbish or retire — locking the AFE list *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Decide which 3-5 assets get $800K refurbishments, which get retired and replaced, and which get harvested to end-of-life on the next capex cycle.

*The middle three questions are where the refurbish-vs-retire shortlist gets defended. The vibration danger-zone question and the prediction-catch question both feed the same conclusion — the assets we are catching are the ones we keep; the ones we miss are the ones we replace.*

### Question (Act 2.1)

> **Which assets currently have vibration velocity in the ISO 10816 Danger zone (≥11.2 mm/s)?**

**What to say while it runs:** ISO 10816 — vibration above 11.2 mm/s is the Danger zone. Operating an asset in Danger isn't a maintenance question, it's a safety and economic-life question. Anything in this list is either coming out of service or going on a hard intervention plan.

**What to look for:** A short table — asset_id, asset_type, manufacturer, vibration_velocity_mm_s — filtered to the Danger threshold. The list should be small. If it's not small, that's the program failing.

**Land the point:** That list used to come out of a vibration analyst's quarterly report. Now it's a real-time view the Plant Manager can act on without waiting for the next walk-around. Workorder release moves from monthly to same-shift.

### Question (Act 2.2)

> **What share of failures in the last 6 months were caught by the prediction model, broken out by asset type?**

**What to say while it runs:** Prediction catch rate — what share of failures in the last six months the ML model saw coming versus what showed up as a Breakdown detection_method. Target is 60% caught. Below that, the PdM program is decoration. Above 75%, it's defending its own budget.

**What to look for:** A bar by asset_type with sensor-detected vs breakdown-detected counts. The gap between sensor and breakdown is the program's value contribution — and Turbines almost always look different from Pumps.

**Land the point:** When the CFO sees that Turbines are running at a 78% catch rate and Gearboxes at 35%, the conversation stops being 'is PdM worth it' and starts being 'why aren't we instrumenting the Gearboxes the way we instrumented the Turbines.' That's a program-expansion conversation.

> **Anchor moment.** Stop on the catch-rate chart and the danger-zone list. Pick a single Gearbox in the Danger vibration zone with a 45 health index — call it 80 hours of unplanned downtime over the last 12 months, with the ML model only catching 30% of failures on that asset class.

> *Gearbox unplanned downtime in heavy industrial settings runs $15K-25K per hour just in production loss, never mind secondary damage. 80 hours times $20K is $1.6M per year of avoided production loss if we catch even half of those failures pre-emptively. A full gearbox refurbish runs $800K — payback under 12 months on one asset. Across the four Gearboxes in the fleet, lifting catch rate from 35% to 65% is $3-5M per year of recoverable production. That number is bigger than the entire annual PdM software and analyst budget.*

> That's the AFE conversation that used to require a steering committee. The Plant Manager walks into the capex review with the refurb-vs-retire list already justified — and the PdM program survives the CFO review because it pays for itself out of the Gearbox numbers alone.

### Question (Act 2.3)

> **Rank manufacturers by average asset availability — which are below the 90% world-class threshold?**

**What to say while it runs:** Manufacturer ranking by availability against the world-class 90% threshold. The point isn't to embarrass Atlas Copco or Sulzer — it's to find the spec issue, the install issue, or the operating-pattern issue. Below 90% on a fleet is structural.

**What to look for:** Ranked manufacturers with avg_availability. Note which fall below 90 — those are the candidates for either supplier-engagement escalation or fleet rationalization on the next capex cycle.

**Land the point:** When the engineer, the plant manager, and procurement all see the same availability number, the next supplier QBR has actual ammunition. That's how supplier-managed-inventory and extended-warranty terms get renegotiated.

---

## Act 3 — The commitment — defending the PdM program at the budget review *(≈4 min)*

**Persona:** CFO • **Job to be done:** Lock in next year's PdM budget and decide which asset classes earn instrumentation expansion versus which get capex-replaced.

*The CFO doesn't need more dashboards; they need maintenance cost trended against unplanned downtime in the same conversation, so the program's ROI defends itself.*

### Question (Act 3.1)

> **Monthly trend in total maintenance cost vs unplanned downtime hours across the network.**

**What to say while it runs:** Monthly trend in total_maintenance_cost overlaid with total_unplanned_downtime hours. This is the chart that proves the program is working — or isn't. We want maintenance cost flat-or-down while downtime is trending down. Anything else is a flag.

**What to look for:** Two lines on one chart over 12 months: maintenance spend and unplanned downtime hours. The story is the relationship between them, not either line on its own.

**Land the point:** When the CFO can see — in one chart — that we spent $400K more on planned maintenance but saved 200 hours of unplanned downtime, the budget conversation moves from 'cut PdM' to 'fund the second wave of instrumentation.' That's a totally different boardroom narrative.

### Question (Act 3.2)

> **Top 10 assets by repair cost from breakdown-detected failures — what is the cost gap versus sensor-detected ones?**

**What to say while it runs:** Top 10 assets by repair cost from Breakdown-detected failures, with the implicit comparison to Sensor-detected ones. Breakdown repairs cost 3-5x more than sensor-detected ones because they include secondary damage and emergency labor. This is the dollar gap that funds the program.

**What to look for:** Ranked assets with total repair_cost_usd filtered to detection_method = 'Breakdown'. The gap to the same assets' sensor-detected average is the per-asset ROI of the instrumentation program.

**Land the point:** Same data the Reliability Engineer is using, same data the Plant Manager is using, now in the CFO's language: dollars avoided. The PdM program stops being an opex line item to defend and starts being a capex deferral story to fund. One space, three personas, one number — that's the leave-behind.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — IronPulse Manufacturing — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 assets by unplanned downtime hours in the last 90 days, and what was their average health index?
2. Show monthly trend in average health index by asset type across the trailing 12 months.
3. Which assets currently have vibration velocity in the ISO 10816 Danger zone (≥11.2 mm/s)?
4. What share of failures in the last 6 months were caught by the prediction model, broken out by asset type?
5. Rank manufacturers by average asset availability — which are below the 90% world-class threshold?
6. Monthly trend in total maintenance cost vs unplanned downtime hours across the network.
7. Top 10 assets by repair cost from breakdown-detected failures — what is the cost gap versus sensor-detected ones?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
