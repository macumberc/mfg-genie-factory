# NanoVista Semiconductor — Demo Script

**Space:** Semiconductor — NanoVista - Quality Event RCA 🔍
**Runtime:** ~15 minutes • 7 questions
**Audience:** Chief Quality Officer + Customer Quality leaders, alongside Yield Engineering and Fab Operations
**KPIs touched:** Die yield %, DPPM, First-pass yield %, Defect density per cm², Containment effectiveness %, Critical event count
**Big decision automated:** Which lots to scrap vs. salvage this week, which fab tool to pull down for re-qualification, and which raw-material supplier to disqualify before the next DPPM excursion hits the automotive customer.

---

## Pre-demo checklist

- Open the Genie space `NanoVista - Quality Event RCA 🔍`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> NanoVista Semiconductor runs 20 products across 4 fabs (Taiwan, Arizona, Dresden, Singapore) shipping into automotive-grade (DPPM <10 target) and consumer-grade (DPPM <500) markets. Today the quality_events feed lives in the fab MES + 8D event tracker, the lot yield numbers live in Yield Engineering's nightly wafer-bin Excel, and DPPM and customer complaint trends sit in the Chief Quality Officer's monthly customer-scorecard PPT. Three systems, one excursion — and the last automotive PMIC escape took 11 days from event open to root cause and cost $8M in customer recovery plus a 6-month sourcing review. A 1pp yield uplift on the flagship is worth $10-100M/year and a single fab-tool unplanned downtime is $50-200K/hour. This space ends the lag. One governed surface where Yield, Fab Ops, and the CQO see DPPM, defect density, and affected-wafer count in the same conversation that authorizes scrap, re-qual, or supplier disqualification.

---

## Key KPIs in scope

- Die yield % — average wafer-level good-die rate; leading-edge fabs target 90%+, mature nodes 95%+
- DPPM — defective parts per million shipped; automotive-grade target <10, consumer <500
- First-pass yield % — share of lots passing electrical test without rework; target 90%+
- Defect density per cm² — wafer defectivity; mature processes <0.10, ramping nodes <0.30
- Containment effectiveness % — defects caught before shipment; target 95%+
- Critical event count — Critical-severity excursions per month; trend should be flat or declining
- Mean time to resolution (days) — avg cycle from event open to closure; target <7 days
- Affected wafer count — at-risk WIP per excursion; sizes containment scope

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **WIP** | Work In Process |

---

## Act 1 — The signal — which products and root causes are eating wafers before customer escape *(≈4 min)*

**Persona:** Yield Engineering lead • **Job to be done:** Pull the at-risk product list and the dominant root-cause categories out of last night's quality-event feed and yield snapshots, before the 8 AM containment call.

*This is where the 8D containment scope gets set. Two questions in, the Yield lead has the products bleeding the most yield and the dominant failure modes — ready for the cross-fab containment call.*

### Question (Act 1.1)

> **Which 10 products have the lowest average lot yield over the trailing 12 months?**

**What to say while it runs:** Bottom 10 products by avg_yield_pct over 12 months — leading-edge target is 90%+ and mature 95%+. Anything chronically below 85% on a leading-edge product is not a fab-of-the-week issue, that's a process-of-record problem and the 8D has to be at the methodology level.

**What to look for:** Ranked table from lot_yield_metrics with avg_yield_pct and unique_product_count. The chronic offenders are where Yield Engineering reallocates this quarter's improvement program.

**Land the point:** Right there is the yield-improvement scope. Now the Yield lead can name the 5 products that earn the next FMEA in minutes — that's the engineering-prioritization conversation that used to be a 90-minute Monday workshop.

### Question (Act 1.2)

> **Show monthly critical event count by fab location for the trailing 12 months.**

**What to say while it runs:** Monthly critical_event_count by fab_location — Taiwan, Arizona, Dresden, Singapore. A fab whose critical event line is climbing while the others are flat is either bringing on new capacity badly or running a tool past its qualification envelope. Both are escalations.

**What to look for:** Monthly trend, DATE_TRUNC('month', event_date) shape, broken out by fab_location from quality_events_metrics. Watch for fab lines diverging upward against the others.

**Land the point:** Before this space, that chart was assembled by hand for the monthly Customer Quality scorecard. Now Yield Engineering opens with it — and the cross-fab containment conversation starts an hour earlier.

---

## Act 2 — The decision — scrap, salvage, or re-qual the tool *(≈4 min)*

**Persona:** Fab Operations Manager • **Job to be done:** Decide which lots to scrap, which to salvage with rework, and which tool gets pulled down for re-qualification before the next shift starts.

*Three questions that turn the yield watchlist into a defensible scrap/salvage/re-qual decision. The middle question is the anchor — the wafers-affected to dollars conversion that converts root-cause signals into 8D authorization.*

### Question (Act 2.1)

> **Which root cause categories account for the most wafers affected this quarter?**

**What to say while it runs:** Root cause categories ranked by total_wafers_affected this quarter from quality_events. Equipment-related root causes mean a re-qualification (1-4 weeks of lost production); material-related root causes mean a supplier disqualification (90+ day requalification). The wafers-affected dollars are how we triage which gets attention first.

**What to look for:** Ranked table of root_cause_category with total_wafers_affected from quality_events_metrics. The top 2-3 categories are where the 8D corrective-action capacity goes this quarter.

**Land the point:** That ranking used to be a manual 8D-system query that took the Yield team a full morning. Now it's the input to the corrective-action authorization the Fab Ops manager signs at the standup.

### Question (Act 2.2)

> **Rank product families by average defect density per cm² — which need yield-improvement focus?**

**What to say while it runs:** Average defect_density_per_cm2 by product_family — mature processes run <0.10, ramping nodes <0.30. Any family chronically above 0.30 is a yield-improvement target, and the wafers in those lots are scrap or salvage candidates depending on the bin distribution.

**What to look for:** Per-family ranking from lot_yield_metrics. The families above 0.30 are where the FMEA capacity goes; the ones spiking above 0.50 are where lots are getting scrapped this week.

**Land the point:** When Yield Engineering, Fab Ops, and Customer Quality all query defect density the same way and see the same number, the meeting stops being whose binmap is current and starts being which lots ship to the automotive customer this week.

> **Anchor moment.** Stop on the root-cause table and the defect-density-by-family chart on screen. Pick the worst combination — call it equipment-root-cause excursions hitting 25,000 affected wafers this quarter on the automotive PMIC family with first_pass_yield_pct dropping 3 points.

> *A 5nm wafer is $5-30K depending on product; call it $15K average for an automotive PMIC. 25,000 affected wafers × $15K = $375M of inventory exposure if we scrap everything blind. Of that, salvage on 70% via bin-class rework recovers $260M and confines the scrap loss to $115M. On the upside, pulling down the responsible tool for a 2-week re-qualification costs us about $50-100M of forgone production at $50-200K/hour, but it stops a $10-100M/year yield gap on the flagship from going chronic. Net call: scrap the 5,000 wafers in the worst bins, salvage 20,000 with rework, pull the etch tool down for 14 days of re-qual, and disqualify the photoresist supplier that the root-cause category points at — preserving the automotive customer's DPPM scorecard and protecting a 1pp yield uplift worth $30-50M annually.*

> That's the decision this space automates. Not the slide. The decision. 5,000 wafers scrapped, 20,000 salvaged, one tool down for re-qual, one supplier disqualified — in one conversation, with one set of numbers, before the automotive customer asks.

### Question (Act 2.3)

> **How has average DPPM trended monthly across all fabs, and which fab is above the 100 DPPM threshold?**

**What to say while it runs:** Now DPPM trended monthly across fabs from quality_kpi_monthly. Automotive-grade target is <10 DPPM; any fab above 100 DPPM is in customer-containment territory. The fab whose DPPM line is climbing first is the one we have to either gate-and-contain or pull tools down on.

**What to look for:** Monthly DPPM trend by fab_location with the 100 DPPM threshold marked. The fab above the line is the one where the next customer audit is going to land.

**Land the point:** That comparison is the difference between knowing yield is slipping and knowing the customer is about to see it. The first is a status report; the second is a tool-down authorization and a customer notification.

---

## Act 3 — The commitment — shaping the customer-quality scorecard and the supplier portfolio *(≈4 min)*

**Persona:** Chief Quality Officer • **Job to be done:** Defend the DPPM trajectory to the automotive customer, lock in the supplier disqualification, and shape next year's quality-investment plan.

*The CQO doesn't need more dashboards; they need the same DPPM, first-pass yield, and customer-complaint numbers Yield Engineering is acting on, in the same language the customer scorecard speaks — so the customer audit and the next sourcing review become the same artifact.*

### Question (Act 3.1)

> **Which products have the highest customer complaint volume in the trailing 6 months, and what is their first-pass yield?**

**What to say while it runs:** Products with the highest customer_complaints over 6 months and their first_pass_yield_pct alongside. The pattern we want to see is high complaints driven by low first-pass yield; the pattern we don't is high complaints despite clean first-pass yield — that's a packaging or field-stress issue we are missing.

**What to look for:** Ranked table from quality_kpi_monthly with both columns. The products with high complaints AND high first-pass yield are the ones the next customer-quality investigation has to land on.

**Land the point:** When this view is in the CQO's hand before the customer audit, the customer conversation moves from defensive to programmatic — and the executive team stops being told about customer escapes after they happen.

### Question (Act 3.2)

> **What is the monthly trend in grade C lot count by product family — where is yield slipping below 75%?**

**What to say while it runs:** Monthly grade_c_lot_count by product_family — grade C means yield below 75%. A family with rising grade C count is the one the next yield-improvement budget has to defend; flat or declining grade C is where we can pull engineering attention to the next family.

**What to look for:** Monthly trend from lot_yield_metrics. Families with grade_c climbing 3+ months in a row are next quarter's yield-improvement targets.

**Land the point:** Triage at the 8 AM containment, scrap/salvage decision at the 10 AM ops call, customer narrative at 2. Same space. Same numbers. The Yield Engineering watchlist and the CQO's customer scorecard are now the same artifact — and the executive team gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — NanoVista Semiconductor — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 products have the lowest average lot yield over the trailing 12 months?
2. Show monthly critical event count by fab location for the trailing 12 months.
3. Which root cause categories account for the most wafers affected this quarter?
4. Rank product families by average defect density per cm² — which need yield-improvement focus?
5. How has average DPPM trended monthly across all fabs, and which fab is above the 100 DPPM threshold?
6. Which products have the highest customer complaint volume in the trailing 6 months, and what is their first-pass yield?
7. What is the monthly trend in grade C lot count by product family — where is yield slipping below 75%?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
