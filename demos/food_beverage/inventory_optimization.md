# FreshStock Solutions — Demo Script

**Space:** Food & Beverage — FreshStock Solutions - Perishable Inventory Optimization 📦
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Supply Chain + CFO, Plant Manager, S&OP Lead
**KPIs touched:** Spoilage rate, Fill rate, Freshness score, Total spoilage cost, Average shelf remaining, Inventory turnover ratio
**Big decision automated:** Which perishable SKUs get marked down vs. donated vs. held this week, and which production lines get re-mixed to defend the 97% OTIF score on the Walmart/Kroger scorecards.

---

## Pre-demo checklist

- Open the Genie space `FreshStock Solutions - Perishable Inventory Optimization 📦`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FreshStock Solutions runs 20 perishable SKUs across 12 production lines — bakery, dairy, produce, protein, seafood, frozen — into national grocery accounts with 97% OTIF chargeback thresholds. Today the days-to-expiry number lives in a Plant Manager's morning WMS export, the fill-rate-by-line view sits in a Supply Planner's Excel pivot, and the monthly spoilage P&L is rebuilt by Finance from the SAP shrink report. Three workbooks, same SKUs — and the markdown / donate / hold decision gets made by whichever buyer screams loudest at 7 AM. This space ends that. One governed surface that turns yesterday's WMS feed into the line-by-line production-mix and shrink-disposition call before the trucks leave the dock.

---

## Key KPIs in scope

- Spoilage rate (%) — fresh produce ~5-8%, refrigerated ~5%, dry goods <2% benchmark
- Fill rate (%) — retailer scorecard threshold 95-98% OTIF
- Freshness score — blended quality / days-remaining index 0-100
- Total spoilage cost ($) — shrink dollars; perishables drive ~2/3 of grocery shrink
- Average shelf remaining (days) — pipeline health for downstream channels
- Inventory turnover ratio — target 12-20x annually for fresh items
- Near-expiry units — at-risk inventory needing markdown or diversion
- On-hand units — stocking-position balance vs. expected demand

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **OTIF** | On-Time In-Full |

---

## Act 1 — The signal — finding the categories burning shrink dollars before the morning huddle ends *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Pull today's shrink-risk categories and lines out of yesterday's snapshot — by dollars, not by gut.

*This is the moment the day's production-mix and markdown queue gets set. Two questions in, the plant manager has the disposition list that used to take a morning of Excel pivots.*

### Question (Act 1.1)

> **Show the monthly trend in total spoilage cost across all product categories for the trailing 12 months.**

**What to say while it runs:** Total spoilage cost by month is the chart Finance rebuilds every quarter for the shrink review. Perishables drive about two-thirds of grocery shrink — so when this line moves, the CFO notices. Watch the produce and seafood bars in the summer months — that's where the structural exposure sits.

**What to look for:** Monthly trend bars across all categories — `DATE_TRUNC('month', perf_month)` shape on `total_spoilage_cost`. Look for the seasonal lift in produce/seafood and the categories that climbed without a seasonal excuse.

**Land the point:** Now the plant manager sees the same shrink number Finance sees, in the same definition, before the close. That's the conversation that used to happen six weeks late in the monthly business review.

### Question (Act 1.2)

> **Top 10 product categories by spoilage cost this year — what optimization actions are most common for each?**

**What to say while it runs:** Now flip to the top categories by spoilage cost YTD with the optimization-action mix — Markdown, Donate, Reorder, or No Action. The action mix tells you whether the team is actually intervening or just watching the shrink accrue.

**What to look for:** Ranked table — top 10 categories on `total_spoilage_cost` with `optimization_action` distribution. Categories with a lot of 'No Action' beside high cost are the ones being managed by status report, not by decision.

**Land the point:** That's the start of the markdown-vs-donate-vs-hold conversation. Now the plant manager picks the categories for this week's intervention list off the same dollars-at-stake ranking the CFO will see at month-end.

---

## Act 2 — The decision — markdown, donate, or hold; and which lines absorb the production-mix shift *(≈4 min)*

**Persona:** S&OP Lead • **Job to be done:** Set the production-mix change for next week, lock the markdown disposition by line, and protect the 97% retailer fill rate.

*Three questions that turn the daily shrink list into a defensible week-over-week production-mix and disposition plan. The middle question is the anchor — the near-expiry-units to shrink-dollars conversion that pays for the line shift.*

### Question (Act 2.1)

> **Which production lines have the lowest fill rate, and how much near-expiry inventory are they carrying?**

**What to say while it runs:** Now drill into the production lines with the worst fill rate and the most near-expiry inventory in flight. These two metrics together — `avg_fill_rate` below the 95% OTIF floor and `total_near_expiry` climbing — are the structural mismatch between what we're producing and what the retailers can actually sell through.

**What to look for:** A table of lines ranked by lowest `avg_fill_rate` with `total_near_expiry` side by side. Lines below 95% with a stack of near-expiry units are the production-mix candidates.

**Land the point:** That list used to be the output of two days of cross-checking the WMS export against the Excel order book. Now it's the input to Monday's S&OP meeting — and the line-by-line production-mix call gets made on data, not on whoever's loudest about chargebacks.

### Question (Act 2.2)

> **How has average freshness score trended month-over-month by product category?**

**What to say while it runs:** Average freshness score by category over the last 12 months — the leading indicator. Fresh produce should hold above 70, dairy above 75. When the curve bends down before the spoilage cost spikes, that's the window to redirect production. Miss it and you're just managing the shrink, not preventing it.

**What to look for:** Monthly trend of `avg_freshness` by category. Inflection points are what matter — categories where freshness dropped 2 months ago are the ones with rising shrink this month.

**Land the point:** Catching the freshness slide before the cost shows up turns this from a shrink-recovery exercise into a production-planning exercise. That's the difference between Finance writing off $500K and S&OP redirecting it.

> **Anchor moment.** Stop on the near-expiry top-10 with the dollar exposure. Pick the worst category — call it 1,200 near-expiry units in produce and dairy in any given week.

> *At a blended $1.50 spoiled SKU-day cost across perishables, 1,200 near-expiry units sitting unsold is roughly $1,800 of shrink that week — call it $90K a year if it's a recurring pattern. Across all 8 perishable categories at FreshStock's scale, recurring near-expiry exposure is $700K-1M of annual shrink that's recoverable with disposition timing alone. Add the OTIF chargeback math — a single 2% retailer chargeback on a $50K order is another $1K per missed pick — and the case clears $1.5M before we touch the production-mix lever.*

> That's the decision this space automates. Not the dashboard. The disposition. Markdown queue built on dollars, donate-credit captured at month-end, production mix shifted next Monday — and Walmart's scorecard stays green.

### Question (Act 2.3)

> **Top 10 product categories by near-expiry units — what is the projected shrink dollar exposure?**

**What to say while it runs:** Top 10 categories by near-expiry units with the projected shrink-dollar exposure. The dollar exposure is the number that turns 'we have inventory at risk' into 'we have $X at risk' — and tells you whether to mark down 30%, donate to food banks for the tax credit, or push aggressive promo through the retailer.

**What to look for:** Ranked table on `total_near_expiry` with a calculated dollar exposure (units × est value). The top 2-3 rows are the disposition decisions for this week.

**Land the point:** That ranking is the actual disposition queue. The plant manager has the action; the S&OP lead has the dollars; the CFO sees both. Same artifact, three roles — and the markdown call gets signed off before lunch instead of next quarter.

---

## Act 3 — The commitment — shaping the shrink budget and the OTIF scorecard guarantee *(≈4 min)*

**Persona:** VP of Supply Chain (with CFO) • **Job to be done:** Defend the perishable-inventory P&L to the executive team and lock the next-year shrink target and retailer-service commitments.

*The VP doesn't need another shrink report; they need the same numbers the plant is acting on, in the same language, so the operating-plan negotiation with Finance and the retailer-scorecard conversation with Sales both write themselves.*

### Question (Act 3.1)

> **Which temperature zones in the perishable_products table show the highest spoilage and shortest days-to-expiry?**

**What to say while it runs:** Temperature-zone view — which zones in the perishable_products table show the highest spoilage and shortest days-to-expiry. Frozen running hot, refrigerated running long — those are the cold-chain decisions: refurbish the dock seals, add a third reefer truck on the produce lane, or shrink the days-to-expiry buffer at receiving.

**What to look for:** Aggregate over `temperature_zone` with avg `days_to_expiry` and spoiled-unit counts. The room should see which zone is structurally underperforming — usually one specific zone × category combination.

**Land the point:** That's the capex conversation. Cold-chain investment used to be argued on anecdote — 'the produce truck was warm once.' Now it's argued on shrink dollars by zone, and the VP walks into the operating-plan meeting with the asset case already built.

### Question (Act 3.2)

> **What is the monthly trend in inventory turnover ratio, and which categories fall below the 12x benchmark?**

**What to say while it runs:** Inventory turnover by month with the 12x benchmark line. Fresh categories below 12 turns are structurally over-stocked — that's both shrink risk and working capital. The categories sitting at 6-8 turns are the SKUs we should be considering for SKU-rationalization heading into next year's plan.

**What to look for:** Monthly `avg_turnover` by category. The categories chronically below 12 are the SKU-rationalization candidates; the ones north of 20 are where we should be expanding production capacity.

**Land the point:** Now the SKU-portfolio conversation has the same shape as the shrink conversation has the same shape as the OTIF conversation. The VP, the CFO, and the retailer-facing sales lead are working from one number — and next year's shrink target stops being a Finance guess and starts being a signed-up commitment.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FreshStock Solutions — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in total spoilage cost across all product categories for the trailing 12 months.
2. Top 10 product categories by spoilage cost this year — what optimization actions are most common for each?
3. Which production lines have the lowest fill rate, and how much near-expiry inventory are they carrying?
4. How has average freshness score trended month-over-month by product category?
5. Top 10 product categories by near-expiry units — what is the projected shrink dollar exposure?
6. Which temperature zones in the perishable_products table show the highest spoilage and shortest days-to-expiry?
7. What is the monthly trend in inventory turnover ratio, and which categories fall below the 12x benchmark?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
