# FactoryPulse Systems — Demo Script

**Space:** Machinery — FactoryPulse Systems - Production Monitoring 📊
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Operations + Plant Manager, Shift Supervisor, CFO partner
**KPIs touched:** OEE, Availability, Performance, Quality, Unplanned downtime, Reject rate
**Big decision automated:** Which 2-3 production lines earn the next capex upgrade, which shift gets the staffing reinforcement next quarter, and which lines get pulled into a structured OEE turnaround.

---

## Pre-demo checklist

- Open the Genie space `FactoryPulse Systems - Production Monitoring 📊`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FactoryPulse Systems runs 20 lines (assembly, welding, painting, machining, packaging) across 4 plants. Today the Shift Supervisor watches a SCADA HMI screen for live line states, the Plant Manager keeps a weekly downtime tracker in Excel, and the VP Operations sees OEE only once a month in a finance-built PowerPoint. Three views of the same lines, three different numbers, and the call on whether to stop a line, swap a shift, or sign the next CNC upgrade gets made on whichever number reached the executive first. This space ends that — one governed surface where availability, performance, quality, and energy-per-unit all reconcile, and the throughput-vs-quality tradeoff becomes an explicit conversation instead of a hallway argument.

---

## Key KPIs in scope

- OEE (%) — world-class ≥85%, typical discrete mfg 60% (Availability × Performance × Quality)
- Availability (%) — world-class ≥90%
- Performance (%) — speed vs rated, world-class ≥95%
- Quality (%) — world-class ≥99.9%
- Unplanned downtime (min) — primary OEE drag
- Reject rate (%) — leaders <1%, target zero scrap
- Throughput (units/shift) — capacity utilization indicator
- Energy (kWh) per unit — cost and ESG metric

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **ESG** | Environmental, Social, Governance |
| **OEE** | Overall Equipment Effectiveness |
| **VP** | Vice President |

---

## Act 1 — The signal — is the line earning the floor space it occupies? *(≈4 min)*

**Persona:** Shift Supervisor • **Job to be done:** Decide before the end of shift which lines to keep running flat-out and which to pull for a forced changeover or maintenance window.

*This is the moment the line-release call gets made. Two questions in, the supervisor already has the OEE ranking that used to require waiting for the month-end deck.*

### Question (Act 1.1)

> **Top 10 production lines by OEE this month — which are above the 85% world-class threshold?**

**What to say while it runs:** World-class OEE is 85%; typical discrete manufacturing sits around 60%. The gap between our best and worst line is the real story — that's where shift staffing and capex both have to flow. Anything below 60% on this list is structurally underperforming, not just having a bad week.

**What to look for:** A ranked table of 10 lines with their average OEE this month, line type, and plant. The eye should go to the spread — top quartile vs. bottom quartile. Click *Show generated code* once so the room sees `MEASURE(avg_oee)` against the governed metric view.

**Land the point:** Right there is the line-release conversation that used to require a steering committee. The supervisor now knows in 30 seconds which lines deserve the operators we have, and which ones need to come down for an honest look.

### Question (Act 1.2)

> **Show monthly trend in average OEE by line type across the trailing 12 months.**

**What to say while it runs:** Now the trend by line type over twelve months — assembly, welding, painting, machining, packaging. The shape of these curves tells you whether a recent OEE dip is seasonal, a one-off, or a structural decline that needs intervention before next quarter.

**What to look for:** Monthly trend lines, one per line type, on a 12-month window with the `DATE_TRUNC('month', ...)` shape. Watch for line types where the curve is *bending downward* — those are the ones that just lost the right to argue for status-quo staffing.

**Land the point:** Before this space, that chart was rebuilt from finance's exports every month. Now the supervisor can flag a structural OEE decline two weeks before it hits the CFO's deck — and the conversation about reinforcing that shift starts with the room agreeing the trend is real.

---

## Act 2 — The decision — takt vs. quality, and which line earns the next capex dollar *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Commit on which lines come down for a structured OEE turnaround, which shift gets staffing reinforcement, and which lines earn next quarter's automation upgrade.

*Three questions that turn line-level OEE into a defensible capex and staffing recommendation. The middle question is the anchor — the unplanned-downtime-to-dollars conversion the executive team came to see.*

### Question (Act 2.1)

> **Top 10 lines by total unplanned downtime minutes over the last 90 days — and how does that break down by shift?**

**What to say while it runs:** Lines ranked by total unplanned downtime, broken out by shift. The leadership benchmark is roughly 5% of available time. Anything past 10% is a structural problem — that line isn't *having* a bad week, it's *operating* a bad system.

**What to look for:** A table by line with `total_downtime_min` from `production_runs_metrics`, broken out by shift. The bars that jump out are the lines where night shift downtime is structurally higher — that's the staffing call.

**Land the point:** That used to be a footnote on a CFO slide. Now it's the first item on the plant-manager review — and the decision about reinforcing the Plant-West night shift moves from anecdote to dollars.

### Question (Act 2.2)

> **Rank line types by average reject rate — where is scrap concentrated?**

**What to say while it runs:** Now reject rate by line type. Best-in-class is under 1%; world-class is essentially zero scrap. The line types above 3% aren't just throwing away material — they're throwing away takt time on rework. That's the takt-vs-quality tradeoff in one number.

**What to look for:** Line types ranked by `reject_rate_pct`, with `total_actual_qty` next to it for scale. The eye should land on the line types that are *high volume AND high reject rate* — those are the lines where automation pays back fastest.

**Land the point:** That ranking is the difference between a plant manager guessing which line is the priority and a plant manager who can walk into the capex committee with the actual dollar bleed.

> **Anchor moment.** Hold on the unplanned-downtime ranking and the reject-rate-by-line-type view. Pick the worst combination — say, 1,200 unplanned downtime minutes per month on a high-volume welding line.

> *Industrial machinery throughput is typically $15-30K per hour of contribution margin on a fully-loaded line. 1,200 unplanned minutes a month is 20 hours; at $20K/hour that's $400K/month, or roughly $5M/year of lost throughput on a single welding line. Layer on a 3% reject rate at $200 per scrapped weldment across 50,000 units of monthly output — another $3.6M/year. One line. Across 20 lines at FactoryPulse's scale, this is a $15-25M/year recoverable-throughput conversation.*

> That's the decision this space automates. Not the dashboard refresh. The decision. The next capex dollar goes to the line where the throughput and scrap math actually pays back inside 18 months — not to the loudest plant manager.

### Question (Act 2.3)

> **What is the monthly trend in total energy consumption per good unit produced?**

**What to say while it runs:** Energy consumption per good unit produced — the ESG and unit-economics chart in one. Painting and welding will dominate; that's expected. The story is the monthly *direction* — is energy intensity creeping up because of aging equipment, or trending down because of the variable-speed retrofit?

**What to look for:** Monthly trend of `SUM(energy_kwh) / SUM(actual_qty)` from snapshots joined to runs. Inflection points matter more than absolute level — that's where capex paid off or stopped paying off.

**Land the point:** This chart turns the ESG report from a compliance artifact into a capex-prioritization tool. The plant where energy-per-unit is climbing is the plant whose CNC line gets the variable-frequency-drive retrofit, not the one that yelled loudest.

---

## Act 3 — The commitment — staffing the next quarter and locking in the capex slate *(≈4 min)*

**Persona:** VP Operations • **Job to be done:** Defend the production plan upstream, lock in the capex slate for next quarter, and shape the workforce plan against the OEE trajectory.

*The VP doesn't need another KPI book; they need the *same* OEE numbers the shift supervisor is acting on, expressed in the language of capacity, capital, and cost-per-unit.*

### Question (Act 3.1)

> **Top 10 lines by lost throughput hours (downtime + changeover) over the last 90 days.**

**What to say while it runs:** Night vs day shift productivity by line type — throughput, reject rate, and downtime side-by-side. Industry data says the night-shift productivity gap is usually 5-15%; if it's wider here, that's a staffing or supervision call, not a line problem.

**What to look for:** A comparison table grouped by shift and line type, pulling `total_actual_qty`, `reject_rate_pct`, and `total_downtime_min`. The eye lands on line types where the night shift gap is more than 15% — those are the candidates for either staffing reinforcement or running fewer lines at night.

**Land the point:** This is the workforce plan in one query. Whether we reinforce night-shift supervision on the welding lines or consolidate to a longer day-shift run is now a decision backed by twelve months of evidence — and the labor argument gets settled before the budget cycle, not during it.

### Question (Act 3.2)

> **Compare night vs day shift throughput, reject rate, and downtime by line type — is there a shift-driven productivity gap?**

**What to say while it runs:** Top 10 lines by lost throughput hours — downtime plus changeover. This is the prioritization view that turns shop-floor noise into a capex order-of-magnitude. The lines at the top are the ones that earn either a single-minute-exchange-of-die program or an automation retrofit.

**What to look for:** Lines ranked by combined `total_downtime_min` and changeover time over 90 days, with `unique_line_count` for context. The room should see the top 5 lines accounting for most of the recoverable hours — the Pareto is the whole point.

**Land the point:** Same space, same numbers, same data model — the shift supervisor's downtime watchlist and the VP's capex slate are now the same artifact. The board gets one story about where the next $5M of investment goes, instead of three competing versions from three plants.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FactoryPulse Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 production lines by OEE this month — which are above the 85% world-class threshold?
2. Show monthly trend in average OEE by line type across the trailing 12 months.
3. Top 10 lines by total unplanned downtime minutes over the last 90 days — and how does that break down by shift?
4. Rank line types by average reject rate — where is scrap concentrated?
5. What is the monthly trend in total energy consumption per good unit produced?
6. Top 10 lines by lost throughput hours (downtime + changeover) over the last 90 days.
7. Compare night vs day shift throughput, reject rate, and downtime by line type — is there a shift-driven productivity gap?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
