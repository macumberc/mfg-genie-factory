# SolarEdge Power — Demo Script

**Space:** Power Generation — SolarEdge Power - Solar & Storage Optimization ☀️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Asset Management + Site Operator, Asset Manager, CFO / Customer Programs Lead
**KPIs touched:** Performance Ratio, Panel efficiency, Solar generation, Inverter availability, Battery state of charge, Battery health / SOH
**Big decision automated:** Which sites earn the next fleet inverter-replacement tranche, which battery sites get a re-financing or ITC-recap, and which underperforming sites move into asset-performance-management remediation before the next investor report.

---

## Pre-demo checklist

- Open the Genie space `SolarEdge Power - Solar & Storage Optimization ☀️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> SolarEdge Power operates a 20-site behind-the-meter fleet — a mix of commercial rooftops, industrial ground-mount, and a small residential community-solar program — typically representing 80-120 MW of PV and 30-40 MWh of co-located battery storage. Today the daily yield and inverter-uptime number lives in a Site Operator's monitoring dashboard, the demand-charge-avoidance receipts sit in the Customer Programs spreadsheet billing each host customer, and the battery cycle-count and SOH trend sits in a separate vendor portal that nobody reconciles to financial performance. Three artifacts, same 20 sites, three different versions of *which sites are still hitting their ITC-financing performance ratio* — and the inverter-replacement program and the ITC-recap decision get shaped by whichever sheet the Asset Manager updated last quarter. This space ends that. One governed surface where PR, inverter uptime, battery SOH, and demand-charge dollars reconcile so the fleet-level capex program and the customer-by-customer economics finally close on the same numbers.

---

## Key KPIs in scope

- Performance Ratio (PR) — industry benchmark 75-85% for well-maintained PV
- Panel efficiency (%) — modern Si PV ~19-22%
- Solar generation (kWh) — top-line yield
- Inverter availability (%) — fleet target >98%
- Battery state of charge (%) — dispatch headroom
- Battery health / SOH (%) — >80% considered serviceable
- Self-consumption ratio — on-site value vs. export
- Demand-charge ($) avoided — primary BTM economic driver

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — finding the underperforming sites and the panel-degradation outliers *(≈4 min)*

**Persona:** Site Operator • **Job to be done:** Pull tomorrow's site-visit list out of yesterday's PV and inverter data, and name which sites are sliding below their performance-ratio commitment.

*This is the moment the morning O&M sweep stops being a portal-by-portal scroll and becomes a one-screen triage. Two questions in, the Site Operator has the fleet-yield picture and the panel-efficiency outlier list.*

### Question (Act 1.1)

> **Show monthly total solar generation kWh by site type for the trailing 12 months.**

**What to say while it runs:** Monthly total_solar_generation_kwh by site_type for the trailing 12 months is the seasonality and fleet-yield read. Commercial rooftop fleets carry the bulk of the kWh; ground-mount industrial sites carry the highest yield per kW; residential typically the most variable. Watch the slope — if industrial yield is climbing while commercial is flat, the residential and commercial fleets are the ones leaking the performance ratio.

**What to look for:** Monthly bars of total_solar_generation_kwh stacked by site_type with `DATE_TRUNC('month', record_date)`. The story is the year-over-year trajectory at this point in the season — if last March was a higher peak than this March on the same site_type, soiling or degradation is in front of us.

**Land the point:** Now the Site Operator can size fleet yield by site_type in seconds instead of cross-referencing 20 site-level portals — that's the *which segment is dragging the performance ratio* conversation that used to require a Saturday spent in monitoring portals.

### Question (Act 1.2)

> **Top 10 sites by average panel efficiency over the last 90 days.**

**What to say while it runs:** Top 10 sites by avg_panel_efficiency over 90 days is the degradation watchlist. Modern silicon PV runs 19-22% at install — anything sliding below 17% for sustained periods is soiling, hot-spot damage, or a string-level fault. The bottom of this list is the field-visit ranking, and the top is the *what does a healthy site look like* benchmark the rest of the fleet is being judged against.

**What to look for:** Ranked table — site_name, site_type, avg_panel_efficiency. Watch for clusters; multiple sites in the same region sliding together is a soiling-and-cleaning conversation, while individual outliers are usually equipment-level failures.

**Land the point:** Right there is the field-truck routing for the next two weeks. Before this space, that list was the output of a Site Operator scrolling through 20 site portals. Now it's the first question of the morning — and the *which sites get a truck-roll this week* call moves from random sampling to data-driven priority.

---

## Act 2 — The decision — inverter recap, battery refinance, or asset-performance-management remediation *(≈4 min)*

**Persona:** Asset Manager • **Job to be done:** Decide which sites earn the next inverter-replacement capex, which battery sites need an ITC-recap or financing renegotiation, and which sites enter an Asset Performance Management program ahead of the investor report.

*Three questions that turn the morning watchlist into the defensible capital-program recommendation. The middle question is the anchor — the demand-charge-and-inverter-failure conversion that decides whether the next $5-8M of fleet capex goes to inverter replacement or to battery augmentation.*

### Question (Act 2.1)

> **Which sites have battery health below 80% and elevated cycle counts — what is the financial exposure?**

**What to say while it runs:** Sites with battery health below 80% with elevated cycle counts is the storage-asset-management watchlist. SOH under 80% is the operational floor where the vendor warranty curve typically ends and the customer-facing capacity guarantee starts to slip. Pair that with cycle count above the manufacturer-stated bound and you have the financing-renegotiation candidate set.

**What to look for:** A short table — site_name, avg_battery_health, total_cycle_count, discharge/charge ratio. The pattern that matters is high cycle count + dropping health on the same site; those are the sites where the ITC-tied performance guarantee is at risk and the customer billing is leaking.

**Land the point:** That asset-health list used to live in the vendor portal and surface in the quarterly Asset Performance Management review. Now it's the *which batteries need an augmentation cell or a refinance* conversation happening live — and the customer-facing economics defense moves from reactive billing-credit to programmatic remediation.

### Question (Act 2.2)

> **How has total demand charge USD trended month-over-month, and which sites contribute most savings?**

**What to say while it runs:** Total demand_charge_usd month over month is the primary BTM economic driver — that's the dollars the host customer would otherwise be paying their utility, and the value SolarEdge is actually selling. Sites where demand-charge avoidance is climbing are the relationship anchors; sites where it's flat or sliding are the sites where battery dispatch logic is off, or the host customer's load profile has shifted.

**What to look for:** Monthly trend of total demand_charge_usd by site_name. The slope tells the customer-economics story; rising avoidance is good news, flat lines on industrial sites are an investigation, and declining lines are the *do we revisit the contract* conversation.

**Land the point:** When this trajectory is in the Asset Manager's hand at the start of the quarter, the customer-renewal conversation gets framed on actual avoidance dollars, not vendor projections — and the *do we re-sign or harvest* call on each customer moves from a sales conversation to a data-driven recommendation.

> **Anchor moment.** Stop on the inverter-uptime watchlist and the demand-charge trend on screen. Pick the worst cluster — call it five commercial sites with inverter availability around 92-94% and demand-charge avoidance that's flat or declining year over year despite a growing host-customer load.

> *A 1 percentage point lift in inverter availability across the fleet of 20 sites — call it 100 kW per site on average, 1,500 sun-hours a year — is roughly 30,000 kWh per site annually, or 600,000 kWh across the fleet. At a blended on-site/export value of $0.12-0.18/kWh, that's $70-100K of annual yield recovery on a 1 pp lift. A full inverter replacement program across the worst five sites runs $1.5-2.5M of capex with a 4-6 percentage point availability lift expected — call it $300-500K of annual recovery, plus the demand-charge avoidance protection that prevents customer credits. Payback inside five years on equipment that lives 10-15. Across SolarEdge's full 20-site portfolio, the inverter-replacement program isn't *do we do it*; it's *which five sites earn the first tranche of capex this year*.*

> That's the decision this space automates. Not the slide. The decision. The inverter-replacement program gets ranked on actual yield and demand-charge dollars, not on vendor warranty schedules — and the Site Operator's truck-roll list and the Asset Manager's capex AFE land in the same artifact.

### Question (Act 2.3)

> **Which sites had inverter status outside of 'Operating' more than 5% of days this year?**

**What to say while it runs:** Sites where inverter_status sat outside 'Operating' more than 5% of days this year is the inverter-uptime watchlist. Fleet target is >98% inverter availability; sites running below that materially are either approaching end-of-life on the original inverter set or have a thermal/firmware issue that's eating yield. Five percent of days offline at a typical commercial site is a $10-30K annual yield hit before you count demand-charge slippage.

**What to look for:** Sites with inverter availability < 95% of days, with inverter_status counts broken out. The bottom of this list is the inverter-replacement program candidates — and that's a capex decision sized in the millions across the fleet.

**Land the point:** That uptime watchlist used to require pulling alarm logs from 20 site portals once a month. Now it's a one-line query — and the *which sites earn the next $200-500K of inverter replacement* conversation runs on operating data, not on vendor recommendations.

---

## Act 3 — The commitment — fleet capex program and the customer-economics defense *(≈4 min)*

**Persona:** CFO / Customer Programs Lead • **Job to be done:** Defend the fleet's PR commitment to the investor base, lock in the multi-year inverter-replacement capex program, and decide which host customers earn financing renewals.

*The CFO doesn't need more dashboards; the CFO needs the same numbers the Asset Manager is acting on so the investor PR-commitment defense and the per-customer financing case both reconcile to operating data.*

### Question (Act 3.1)

> **Top 10 sites by total net meter credit kWh year-to-date — and how does that compare to last year?**

**What to say while it runs:** Top 10 sites by total net_meter_credit_kwh year-to-date with year-over-year comparison is the export-economics view. Sites where net-meter credit is climbing year over year are the strongest performers; sites where it's declining are either local-policy headwinds — utility-rate changes — or actual yield slippage that needs the field-truck list from Act 2 attached.

**What to look for:** Ranked table of total net_meter_credit_kwh by site_name with YoY delta. The story is the bifurcation; the strongest sites carry the investor narrative, the weakest sites are the ITC-recap candidates.

**Land the point:** When this list ships from the same space the Site Operator and Asset Manager used today, the customer-economics defense lands on one number — and the *which customers earn renewal financing* conversation becomes a programmatic ranking instead of a series of bilateral negotiations.

### Question (Act 3.2)

> **What is the monthly trend in average battery state of charge across all storage sites?**

**What to say while it runs:** Monthly trend in avg_state_of_charge across all storage sites is the fleet-storage health and utilization view. A flat-or-rising SOC on the morning of high-rate hours is good news — those batteries are charged when the customer needs them. A declining SOC trend on the same time-of-day window is either control-logic drift or genuine capacity loss, and the difference matters for the warranty and recap conversation.

**What to look for:** Monthly avg_state_of_charge by site_name, ideally with the time-of-charge pattern visible. The pattern matters more than the level; storage that consistently has charge when demand-charge events fire is delivering its value, storage that doesn't is an asset-performance-management escalation.

**Land the point:** Field triage at 8 AM, investor narrative at the next earnings cycle. Same space, same numbers. The Site Operator's morning sweep, the Asset Manager's capex AFE, and the CFO's investor defense are now the *same artifact* — and the host customers, the tax-equity investors, and the analyst desk all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — SolarEdge Power — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total solar generation kWh by site type for the trailing 12 months.
2. Top 10 sites by average panel efficiency over the last 90 days.
3. Which sites have battery health below 80% and elevated cycle counts — what is the financial exposure?
4. How has total demand charge USD trended month-over-month, and which sites contribute most savings?
5. Which sites had inverter status outside of 'Operating' more than 5% of days this year?
6. Top 10 sites by total net meter credit kWh year-to-date — and how does that compare to last year?
7. What is the monthly trend in average battery state of charge across all storage sites?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
