# TransRoute Logistics — Demo Script

**Space:** Logistics — TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Logistics + Fleet Manager, S&OP Lead, CFO partner
**KPIs touched:** Fuel cost per km, Load utilization %, On-time delivery %, Fuel efficiency, Cost per delivery, Traffic delay minutes
**Big decision automated:** Which 5-8 lanes get redesigned from point-to-point to multi-stop, which depots get demoted, and where the next cross-dock investment lands.

---

## Pre-demo checklist

- Open the Genie space `TransRoute Logistics - Route Planning & Delivery Efficiency 🗺️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> TransRoute Logistics runs 28 mixed-fleet vehicles — Semis, Trucks, and Vans — across a 10-metro depot network. Today the fuel-cost-by-lane number lives in the Fleet Manager's weekly fuel-spend tracker, the OTIF and traffic delay picture in the VP Logistics' Monday operations review, and the CO2 and scope-1 reporting in the CFO partner's quarterly ESG workbook. Three artifacts, three cadences, same trucks — and every year the lane-design and cross-dock conversation gets postponed because no one can reconcile the three numbers in the same week. This space ends that. One governed surface where lane fuel cost, load utilization, traffic exposure, and CO2 sit in the same conversation that sets the redesign and capex slate.

---

## Key KPIs in scope

- Fuel cost per km (USD) — primary driver of variable cost; benchmark $0.18–$0.30/km for diesel semis
- Load utilization % — capacity fill rate; <70% signals deadhead / under-loading exposure
- On-time delivery % — customer SLA metric; 95%+ is industry target
- Fuel efficiency (km / liter) — operating ratio and ESG metric
- Cost per delivery (USD) — unit economics for pricing and margin analysis
- Traffic delay minutes — congestion / route-quality indicator
- CO2 emissions (kg) — scope-1 reporting and customer ESG asks
- Total distance km — exposure base for all per-km ratios

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **ESG** | Environmental, Social, Governance |
| **OTIF** | On-Time In-Full |
| **SLA** | Service Level Agreement |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the lanes that are quietly bleeding fuel *(≈4 min)*

**Persona:** Fleet Manager • **Job to be done:** Pull the structurally expensive lanes out of the segment data — not by gut, by total fuel cost and per-km efficiency.

*This is where the redesign shortlist starts forming. Two questions in, the Fleet Manager already has the network-level fuel picture that used to take a half-day of stitching against the fuel-card export.*

### Question (Act 1.1)

> **Show the monthly trend in total fuel cost across the network for the trailing 12 months.**

**What to say while it runs:** Network fuel cost monthly for the last 12 months. Anyone in this industry knows diesel is the biggest variable line — but the question we actually care about is the trend, and whether the trend is fuel price or fuel volume. If the trend moves while price is flat, that's a routing or load-utilization issue.

**What to look for:** Twelve months of total_fuel_cost_usd at the network level. Watch for the slope — a rising line during a flat diesel quarter is the redesign trigger.

**Land the point:** Before this space that chart was rebuilt from the fuel-card pivot every month. Now it's the Fleet Manager's first question of the day — and the redesign conversation starts on a trend, not on a one-bad-week anecdote.

### Question (Act 1.2)

> **How has on-time delivery percentage trended month-over-month by vehicle type?**

**What to say while it runs:** On-time delivery percentage trended by vehicle type. Industry target is 95%+. If Vans are sliding below 90% while Semis hold steady, the question is whether it's traffic, depot mis-sequencing, or under-staffed last-mile.

**What to look for:** Monthly avg_on_time_delivery_pct lines by Semi / Truck / Van. The fleet that's sliding is the one whose lane design is wrong.

**Land the point:** Now the Fleet Manager can pinpoint which vehicle type is dragging service performance in seconds — that's the input to the lane-redesign discussion that used to live three layers deep in a QBR deck.

---

## Act 2 — Redesign, retire, or consolidate — locking the lane slate *(≈4 min)*

**Persona:** S&OP Lead • **Job to be done:** Decide which lanes get redesigned into multi-stop, which vehicles get reassigned, and which deserve a cross-dock investment vs. a depot retirement.

*Three questions that take the lane and asset shortlist to a defensible redesign recommendation. The middle question is the anchor — cost-per-delivery against load utilization is the unit-economics tie-breaker.*

### Question (Act 2.1)

> **Top 10 origin-destination lanes by total fuel cost over the last 90 days — which are dragging margin?**

**What to say while it runs:** Top 10 origin-destination lanes by total fuel cost over the last 90 days. The expensive lanes deserve scrutiny, but the real signal is when an expensive lane is *also* showing low load utilization — that's a deadhead problem masquerading as a fuel problem.

**What to look for:** A ranked table of OD lanes with total_fuel_cost_usd. Cross-reference with avg_load_utilization_pct from the same view — the bad lanes are expensive AND under 70% loaded.

**Land the point:** That ranked list used to be a manual VLOOKUP between the fuel-card system and the dispatch board. Now it's a single query — and the redesign conversation begins from the same lane list everyone in the room can see.

### Question (Act 2.2)

> **Top 10 vehicles by cost per delivery last month, and what was their average load utilization?**

**What to say while it runs:** Top 10 vehicles by cost per delivery last month and their load utilization. Industry benchmark on cost-per-delivery is $80-150 for urban Vans, $250-400 for regional Trucks, $500-800 for long-haul Semis. Anything 20%+ above the band on a sub-70% load utilization is a lane-redesign candidate, not a driver-coaching candidate.

**What to look for:** Vehicles ranked by avg_cost_per_delivery_usd with avg_load_utilization_pct sitting next to them. The pattern to watch is high cost paired with low load — that's the multi-stop opportunity.

**Land the point:** Before this space the cost-per-delivery conversation was a finance presentation 30 days after the month closed. Now it's a Tuesday morning question — and the answer drives the route-design rework cycle.

> **Anchor moment.** Stop on the cost-per-delivery list. Take the top 5 routes — running ~$1.10/km cost vs. a network baseline of $0.75/km, on lanes averaging 55% load utilization against a fleet target of 80%.

> *Five lanes running $0.35/km above the network baseline, each at roughly 200,000 km/year of distance — that's $70K/year/lane of excess unit cost, or $350K/year across the five. Now layer the load utilization gap: converting two of those routes from point-to-point to multi-stop closes the utilization gap from 55% to ~75% and avoids $80-100K/year per lane in deadhead miles. Total annual recovery from the redesign: $500-600K/year. Across the 28-vehicle fleet that comfortably funds the next cross-dock investment in the bid book.*

> That's the decision this space automates. Not the slide. The decision. The redesign slate gets built on per-lane dollars, not on the loudest depot manager's complaint in the Monday meeting.

### Question (Act 2.3)

> **Which weather conditions correlate with the highest average traffic delay minutes?**

**What to say while it runs:** Traffic delay minutes by weather condition. This is the answer to 'is our schedule realistic'. Snow and Heavy Rain conditions correlated with 2x normal delay minutes mean we're systematically under-buffering the schedule and turning it into chargebacks.

**What to look for:** avg_traffic_delay_minutes grouped by weather. Watch for conditions where delay is 50%+ above the baseline — those are the schedule windows that need a routing buffer or a different vehicle class.

**Land the point:** That ranked picture turns into the seasonal-schedule recommendation. Not 'our routes are slow in winter' — 'these 4 lanes get a +25-minute buffer December through March, and these 2 lanes shift from Van to Semi for the same period'.

---

## Act 3 — The commitment — locking the redesign slate and the cross-dock capex *(≈4 min)*

**Persona:** VP Logistics • **Job to be done:** Defend the redesign recommendation, the cross-dock investment, and the scope-1 reporting to the CFO and the customer ESG team.

*The VP needs the same numbers the planners are acting on, framed so the redesign capex case and the customer ESG conversation hold up the same story.*

### Question (Act 3.1)

> **What is the total CO2 emissions trend monthly by vehicle type for scope-1 reporting?**

**What to say while it runs:** Monthly CO2 emissions by vehicle type for scope-1 reporting. Customers' procurement teams now ask for emissions per shipment in the RFP. If our Semi CO2 trend isn't flat or declining, we're inviting a contractual lever the buyer will pull.

**What to look for:** Monthly total_co2_emissions_kg by Semi / Truck / Van. The trend by vehicle type is what gets quoted in the customer ESG response — and it ties directly to the lane-redesign and fleet-mix decisions Act 2 just framed.

**Land the point:** When the VP can put the emissions trend, the lane-design recommendation, and the cost-per-delivery in the same conversation, the scope-1 disclosure stops being a separate spreadsheet exercise and becomes a byproduct of the operating plan.

### Question (Act 3.2)

> **How does average load utilization compare across Semi, Truck, and Van fleets for the last 90 days?**

**What to say while it runs:** Average load utilization across Semi, Truck, and Van for the last 90 days. This is the capacity-mix gravity number — it tells us whether the fleet is the right composition, or whether the next 5 trucks should be a different class than the ones we have today.

**What to look for:** avg_load_utilization_pct across the three vehicle types. The class running below 70% in steady demand is the class with structural overcapacity — and the lane-redesign or fleet-mix recommendation has to address it.

**Land the point:** Redesign slate at 9 AM, cross-dock capex at 11, ESG response at 1. Same space. The VP walks into the CFO conversation with one set of numbers covering operations, capex, and reporting — and the network redesign stops being a five-month working group and becomes a one-month decision.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — TransRoute Logistics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in total fuel cost across the network for the trailing 12 months.
2. How has on-time delivery percentage trended month-over-month by vehicle type?
3. Top 10 origin-destination lanes by total fuel cost over the last 90 days — which are dragging margin?
4. Top 10 vehicles by cost per delivery last month, and what was their average load utilization?
5. Which weather conditions correlate with the highest average traffic delay minutes?
6. What is the total CO2 emissions trend monthly by vehicle type for scope-1 reporting?
7. How does average load utilization compare across Semi, Truck, and Van fleets for the last 90 days?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
