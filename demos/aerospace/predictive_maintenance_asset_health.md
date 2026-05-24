# AeroGuard Systems — Demo Script

**Space:** Aerospace — AeroGuard Systems - Predictive Maintenance & Asset Health 🔧
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Operations + Fleet Engineer, MRO Program Manager
**KPIs touched:** Dispatch reliability %, Aircraft-on-Ground downtime hours per event, Unscheduled engine removal rate, Average engine health score, EGT margin remaining, Remaining useful life per engine
**Big decision automated:** Which engines to keep on-wing vs. pull for shop visit this quarter — and which MRO slots to book now to protect dispatch reliability through the summer schedule.

---

## Pre-demo checklist

- Open the Genie space `AeroGuard Systems - Predictive Maintenance & Asset Health 🔧`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroGuard Systems monitors 20 in-service aircraft engines across 5 airline operators — a mix of narrowbody and widebody fleets. Today the EGT-margin trend lives in the Fleet Engineer's CMMS export, the AOG-hours-by-event log lives in the MRO Program Manager's spreadsheet, and the dispatch-reliability rollup lives in the operating review deck the VP rebuilds every month. Three artifacts, same 20 engines — and the on-wing vs. shop-visit call gets made in the moment by whichever engineer escalated first, with no shared view of which engines are actually closest to the cliff. This space ends that. One governed surface where EGT margin, health score, anomaly counts, and unscheduled-removal history sit together, so the shop-visit booking decision becomes a defensible scheduling call, not a reactive scramble after the next IFSD event.

---

## Key KPIs in scope

- Dispatch reliability % (industry benchmark: 99.0%+ narrowbody, 99.5%+ widebody)
- Aircraft-on-Ground (AOG) downtime hours per event
- Unscheduled engine removal rate (target: <0.10 per 1,000 EFH)
- Average engine health score (0–100; flag <60)
- EGT margin remaining (°C) — shop-visit predictor
- Remaining useful life (flight hours) per engine
- Total MRO spend (USD) by event type
- Critical anomaly count by airline / engine model

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **AOG** | Aircraft on Ground |
| **EFH** | Engine Flight Hours |
| **EGT** | Exhaust Gas Temperature |
| **MRO** | Maintenance, Repair & Overhaul |
| **RUL** | Remaining Useful Life |
| **VP** | Vice President |

---

## Act 1 — The signal — catching the engines about to come off-wing before the next anomaly does it for us *(≈4 min)*

**Persona:** Fleet Engineer • **Job to be done:** Identify which engines are showing degradation patterns severe enough to warrant a planned shop visit instead of an in-service surprise.

*This is the moment the shop-visit candidate list starts forming. Two questions in, the engineer already has the engines that need a planned removal slot before they cause an AOG event.*

### Question (Act 1.1)

> **Top 10 engines by total maintenance cost over the last 12 months — which airlines do they belong to?**

**What to say while it runs:** Engines ranked by 12-month maintenance cost with their airline. The pattern matters — one airline carrying disproportionate cost usually means a fleet-wide operational issue (over-temp ops, harsh duty cycle); one engine model carrying it means a design or supplier issue. The cost rank is the diagnostic anchor.

**What to look for:** A ranked table of 10 engines by total_maintenance_cost with their airline. The room should see whether the top of the list clusters by operator or by engine model — that's where the root-cause conversation goes.

**Land the point:** Right there is the shop-visit shortlist. The engineer can name the engines that earn a planned removal slot — and the conversation with the airline goes from 'why is your cost up' to 'here are the three engines, here's the booking.'

### Question (Act 1.2)

> **Show the monthly trend in critical anomaly count by airline.**

**What to say while it runs:** Now critical anomaly count by airline over 12 months. Critical-flag anomalies — EGT margin near zero, vibration above threshold — are the leading indicator. A rising trend by airline usually means a duty-cycle issue; rising by engine model means a fleet-wide design exposure. Dispatch reliability target is 99.0%+ narrowbody, 99.5%+ widebody.

**What to look for:** Monthly trend of critical_alert_count by airline using `DATE_TRUNC('month', ...)`. Watch for airlines where the line is climbing — those need a conversation before dispatch reliability slips.

**Land the point:** Before this space, that chart was rebuilt for the monthly fleet review. Now it's the engineer's first question of the morning — and the conversation about MRO slot booking starts weeks earlier.

---

## Act 2 — The decision — keep on-wing, pull for shop visit, or accept the AOG risk *(≈4 min)*

**Persona:** MRO Program Manager • **Job to be done:** Commit a shop-visit schedule — naming which engines book MRO slots this quarter and which stay on-wing under enhanced monitoring.

*Three questions that turn the anomaly watchlist into a defensible MRO booking plan. The middle question is the anchor — converting unscheduled-removal exposure into the cost-of-removal-event math the VP of Ops will sign off on.*

### Question (Act 2.1)

> **Which engine models have the worst average health score this quarter?**

**What to say while it runs:** Engine models with the worst average health score this quarter. Below 60 is the standing flag — that's the threshold the engineers set, not me. A model averaging below 60 across the fleet means the next IFSD event is a 'when', not an 'if', and the MRO slots get booked accordingly.

**What to look for:** Engine models ranked by avg_health_score with their critical_alert_count. The room should see that one or two models are running well below 60 — those are the slot-booking priorities.

**Land the point:** That ranking IS the MRO slot allocation. Two queries in, the program manager has a defensible booking plan — and the conversation with the MRO vendor moves from 'when can you fit us in' to 'here are the 6 engines, here are the dates.'

### Question (Act 2.2)

> **How many unscheduled removals occurred by engine model in the last 6 months, and what was the total downtime?**

**What to say while it runs:** Unscheduled removals by engine model over 6 months with total downtime. Industry benchmark target is below 0.10 unscheduled removals per 1,000 EFH — that's the dispatch-reliability commitment to the airline. Anything above 0.15 is a contract-exposure conversation.

**What to look for:** Engine models ranked by unscheduled_removal_count and total downtime_hours. The point is which models are blowing the dispatch-reliability commitment — those are the AOG-cost-of-doing-nothing list.

**Land the point:** That table is the case for shop-visit acceleration. The cost of pulling early is real; the cost of an unscheduled removal during the summer schedule is bigger. This view lets the program manager make that call on dollars.

> **Anchor moment.** Park on the unscheduled-removal-by-engine-model view. Pick the worst model — say it's averaging 0.18 removals per 1,000 EFH, well above the 0.10 target.

> *A typical engine shop visit costs $300-500K just in materials and labor. An unscheduled removal — bag-and-tag, AOG ferry, expedite logistics, no advance MRO slot — runs $500K-1M plus 3-7 AOG days at $10-15K per AOG hour. Call it $1.5M per unscheduled event vs. $400K planned. Across 5 airlines and 20 engines, dropping unscheduled removals from 0.18 to 0.10 per 1,000 EFH on the problem fleet saves roughly 6-8 events per year × $1.1M delta = $6-9M annually in recovered cost — before counting the dispatch-reliability protection that defends the airline contracts.*

> That's the decision this space automates. Shop-visit slots get booked from health-score and EGT-margin trends, not from the last failure. AOG exposure moves from 'something we eat' to 'something we hedge.' The fleet engineer, the program manager, and the airline all see the same prediction the same morning.

### Question (Act 2.3)

> **Top 10 most expensive maintenance findings by total cost — and what is the average AOG hours per occurrence?**

**What to say while it runs:** Top 10 most expensive maintenance findings by total cost with average AOG hours per occurrence. Hot-section findings — burner cans, HPT blades — run $300-500K per removal event in shop cost alone, plus the aircraft-on-ground penalty. This is the root-cause-to-dollars view.

**What to look for:** Findings ranked by total cost with avg_downtime_hours alongside. Watch for findings where the AOG hours are climbing — that's the airline-relationship risk.

**Land the point:** That's the difference between knowing a finding is expensive and knowing it's structurally expensive. The first gets logged; the second gets a CAPA, a supplier-quality escalation, and a shop-visit acceleration.

---

## Act 3 — The commitment — defending dispatch reliability to the airline customer and shaping next year's MRO contract *(≈4 min)*

**Persona:** VP of Operations • **Job to be done:** Defend dispatch reliability against the airline SLA, lock in next year's MRO capacity commitments, and decide which engine models earn fleet expansion vs. retirement.

*The VP doesn't need a new report — they need the same health-score and AOG-hours numbers the engineering team is acting on, packaged for the airline QBR and the MRO vendor negotiation.*

### Question (Act 3.1)

> **Show monthly average EGT for widebody engines over the trailing 12 months.**

**What to say while it runs:** Monthly EGT trend for widebody engines over 12 months. EGT margin is the standing shop-visit predictor. A flat margin is healthy; a declining margin is the leading indicator of an imminent removal. This is the metric the VP shows the airline's chief operating officer at the QBR.

**What to look for:** Monthly avg_egt_celsius for widebody engines. Watch for engines where EGT is climbing month over month — that's the next quarter's shop-visit roster.

**Land the point:** When that view is in the VP's hand a quarter before the next unscheduled removal, the airline conversation becomes proactive instead of reactive — and the MRO capacity ask is sized on data, not on last year's surprise.

### Question (Act 3.2)

> **Which engines are in the Critical risk category right now, and what is their remaining useful life?**

**What to say while it runs:** Engines currently in the Critical risk category with their remaining useful life in flight hours. This is the immediate-action list — the engines that need a slot in the next 30-60 days, not the next quarter. RUL is the prioritization knob; risk category is the threshold.

**What to look for:** Engines filtered to risk_category = 'Critical' with their remaining_useful_life_hours. The shortest RUL goes first.

**Land the point:** Triage at the engineering desk, MRO booking at the program review, dispatch-reliability defense at the airline QBR. One space. Same numbers. The airline gets one story from AeroGuard, the MRO vendor gets one schedule, the fleet stays in the air.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroGuard Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 engines by total maintenance cost over the last 12 months — which airlines do they belong to?
2. Show the monthly trend in critical anomaly count by airline.
3. Which engine models have the worst average health score this quarter?
4. How many unscheduled removals occurred by engine model in the last 6 months, and what was the total downtime?
5. Top 10 most expensive maintenance findings by total cost — and what is the average AOG hours per occurrence?
6. Show monthly average EGT for widebody engines over the trailing 12 months.
7. Which engines are in the Critical risk category right now, and what is their remaining useful life?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
