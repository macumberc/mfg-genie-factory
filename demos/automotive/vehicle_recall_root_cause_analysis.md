# Apex Motor Group — Demo Script

**Space:** Automotive — Apex Motor Group - Recall & Defect Analytics 🚨
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director, Quality + Quality VP, Supplier-Quality Engineer, Warranty/CFO finance team
**KPIs touched:** Recall completion rate, Average days to remedy, Critical recall count, Units affected per campaign, Total estimated recall cost, Warranty claim cost per claim
**Big decision automated:** Which 2-3 tier-1 suppliers to consolidate to (or exit), which open recall campaign to launch first against the NHTSA 60-day clock, and which warranty-claim pattern is the next NHTSA recall waiting to be filed.

---

## Pre-demo checklist

- Open the Genie space `Apex Motor Group - Recall & Defect Analytics 🚨`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> Apex Motor Group's recall and warranty exposure spans 20 vehicle models — Ford F-150 to Toyota Camry, Tesla Model Y to Jeep Wrangler — and 15 tier-1 suppliers including Bosch, Denso, Magna, Continental, ZF, Aisin, Lear, Aptiv, Valeo, and Hella. Today the NHTSA campaign tracker sits in the Field Quality engineer's SharePoint, the supplier-defect concentration lives in the Quality VP's spreadsheet rebuilt monthly from the NHTSA portal export, and the warranty-claim cost ledger is a Tableau extract the Warranty/CFO team pulls on Mondays. Three artifacts, same defect-to-supplier-to-dollars story — and the *which supplier do we exit, which campaign do we launch first, which claim pattern is the next 25V- filing* decision gets made on whichever number was loudest at the Tuesday quality call. NHTSA's 60-day owner-notification clock is unforgiving — miss it on one campaign and the daily penalty is $26K/violation per vehicle, and the industry completion-rate benchmark is only 75–87%. This space replaces those three workbooks with one governed surface where component, supplier, severity, days-to-remedy, and warranty leading-indicators live next to each other — and the supplier-consolidation and recall-prioritization decisions happen in the same conversation.

---

## Key KPIs in scope

- Recall completion rate (%) — share of affected units repaired (NHTSA industry range 75–87%)
- Average days to remedy — must beat NHTSA's 60-day final-notice rule
- Critical recall count — campaigns with injury/fatality exposure
- Units affected per campaign — fleet exposure and parts-supply impact
- Total estimated recall cost ($) — financial impact (parts + labor + logistics)
- Warranty claim cost per claim ($) — leading indicator of an emerging recall
- Supplier defect concentration — share of recalls traced to a single tier-1
- Open vs closed recall count — campaign-management workload

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |

---

## Act 1 — The signal — finding the supplier and component patterns before NHTSA finds them for us *(≈4 min)*

**Persona:** Supplier-Quality Engineer • **Job to be done:** Pull this month's recall financial exposure out of the campaign log and the supplier ledger — and find the warranty pattern that's about to become next month's NHTSA filing.

*Every recall campaign filed late is a $26K/vehicle/day exposure to NHTSA penalties. Every warranty claim that should have triggered a recall investigation is a class-action waiting. The Supplier-Quality Engineer has to find both, in the same 20 minutes.*

### Question (Act 1.1)

> **Show monthly recall event volume and total estimated cost for the trailing 12 months.**

**What to say while it runs:** Monthly recall event volume and `total_estimated_cost` for the trailing 12 months. The volume line is the workload; the cost line is the boardroom conversation. When they diverge — fewer recalls but more cost — we're filing bigger, deeper-exposure campaigns.

**What to look for:** Twin lines from `recall_analysis_metrics` — `total_recall_events` and `total_estimated_cost` by `recall_month`. Watch for the inflection where cost climbs while volume stays flat — that's the signal that one campaign is dragging the whole quarter.

**Land the point:** Now the Supplier-Quality Engineer can walk into the Tuesday quality call with *here are the 2 campaigns blowing the quarterly cost line* — instead of letting the loudest field-quality email decide the agenda.

### Question (Act 1.2)

> **Top 10 suppliers by total estimated recall cost — which tier-1s are driving the most financial exposure?**

**What to say while it runs:** Top 10 suppliers by `total_estimated_cost` — which tier-1s are driving the most financial exposure? When one supplier shows up against 5 different component groups across 4 vehicle models, that's not bad luck — that's a supplier-consolidation conversation.

**What to look for:** Ranked list of `supplier_id` from `recall_events` aggregated by `total_estimated_cost`, with `unique_vehicle_model_count` as a side column. Watch for a Bosch or Denso showing up with 3+ models and $50M+ exposure — that's the consolidation candidate or the exit decision.

**Land the point:** Right there is the supplier-strategy conversation. Before this space, that ranking required three days of NHTSA-portal CSV scraping. Now it's a 30-second query — and the *consolidate or hold supplier diversity* decision starts where it should: with the financial exposure picture.

---

## Act 2 — The decision — supplier consolidation, campaign-launch order, and the next recall waiting to happen *(≈4 min)*

**Persona:** Quality VP • **Job to be done:** Commit to the supplier-consolidation decision, the campaign-launch priority order against the NHTSA 60-day clock, and the warranty pattern that earns a preemptive recall investigation.

*Three questions that turn the recall backlog into a defensible quality-policy recommendation. The middle question is the anchor — the supplier-spend math that decides whether we exit a tier-1 or double down on consolidation.*

### Question (Act 2.1)

> **Which component groups have the highest critical recall count and average days to remedy?**

**What to say while it runs:** Which `component_group` has the highest `critical_recall_count` and `avg_days_to_remedy`? The critical count is the boardroom risk; days-to-remedy is the NHTSA 60-day-clock risk. When both light up on the same component, that's a campaign that needs the rig and the parts logistics today.

**What to look for:** Pivot — `component_group` × `critical_recall_count` × `avg_days_to_remedy` from `recall_analysis_metrics`. Watch for Air Bags or Brakes sitting above 60 days on remedy — that's a penalty exposure measured in millions per day if it slips further.

**Land the point:** That heatmap is the launch-order. Now the Quality VP can walk into the field-quality review and say *Air Bags goes first because we're already at 58 days, ADAS Software goes second* — instead of letting the loudest engineering team set the rig schedule.

### Question (Act 2.2)

> **What is the total estimated cost of all open recall campaigns by component group?**

**What to say while it runs:** Total `total_estimated_cost` of all open recall campaigns by `component_group`. This is the *what's still on the books* picture — the open-campaign exposure is the line item the CFO partner is going to ask about, and the component breakdown is where the supplier consolidation argument lives.

**What to look for:** Bar chart from `recall_analysis_metrics` filtered to open status, by `component_group` with `total_estimated_cost`. The top 3 components are the supplier-consolidation candidates; the long tail is where the diversification story might still survive.

**Land the point:** When the Quality VP, the Supplier-Quality Engineer, and the CFO partner all see the same open-exposure picture, the *exit Supplier X or consolidate to Supplier Y* meeting stops being about whose preferred vendor wins and starts being about *which combination cuts $40M of forward exposure*.

> **Anchor moment.** Stop on the supplier ranking and the open-campaign exposure list. Take the top-2 suppliers — say Bosch and Denso together account for $80M of estimated cost across 4 vehicle models, with 5 of the top-10 open recalls between them.

> *A typical recall remedy runs $200–500 per vehicle (parts + labor + dealer logistics). Apex's tier-1 supplier spend across the recall-touched component categories is roughly $400–600M/year; industry data on supplier consolidation says 5–12% of category spend is recoverable when an OEM consolidates from 4–5 tier-1s to 2 dominant ones — that's $20–70M/year of supplier-consolidation savings. On top of that, every campaign filed late is exposed to NHTSA's $26K/violation/day penalty — on a 50,000-unit Bosch campaign, slipping 10 days past the 60-day final notice is $13M of pure penalty exposure. And the warranty side: at $400–1,500/claim average, an unfiled recall masquerading as warranty work bleeds $2–5M/quarter before anybody files. Put it together and the consolidation-plus-prioritization decision in front of us is $30–60M/year of recoverable margin and $10–20M of avoided NHTSA penalty.*

> That's the decision this space automates. Not the recall dashboard. The supplier-consolidation commitment and the campaign-launch order. Bosch + Denso consolidation enters Letter-of-Intent stage this quarter, the Air Bags campaign moves to top of the rig schedule, and the Quality VP walks into the executive review with the dollar number — not the campaign-count number.

### Question (Act 2.3)

> **How has average days to remedy trended month-over-month vs the NHTSA 60-day benchmark?**

**What to say while it runs:** Which `region` has the highest warranty `avg_claim_cost`, and what `component_code` is driving it? A region running 25%+ above network average on claim cost for one component is either a population defect or the leading edge of an unfiled recall. Either way, that's the next NHTSA filing if we wait.

**What to look for:** Pivot — region × component_code from `warranty_claim_metrics`. Watch for the SU-BLJ (ball joint), BR-PAD (brake pads), or AB-INF (airbag inflator) lighting up in one region — that's the warranty pattern that's about to become a recall.

**Land the point:** That's the difference between filing a recall on our schedule and filing it on NHTSA's. The first is a $50–100M campaign you control; the second is a class-action with a $26K/day clock running against you.

---

## Act 3 — The commitment — defending the recall P&L and the supplier strategy to the executive team *(≈4 min)*

**Persona:** Warranty/CFO finance partner • **Job to be done:** Defend the recall-cost forecast and supplier-spend plan to executive leadership — supplier consolidation, recall-cost reserves, and warranty-claim leading-indicator triggers for the next year.

*The CFO partner doesn't need a new database; they need the same exposure numbers the Quality VP and the Supplier-Quality Engineer are acting on, framed against the recall-cost reserve and the NHTSA-clock risk the executive team and the auditors actually ask about.*

### Question (Act 3.1)

> **Top 10 vehicle models by units affected in recall campaigns over the trailing 12 months.**

**What to say while it runs:** How has `avg_days_to_remedy` trended month-over-month vs the NHTSA 60-day benchmark? This is the regulatory-risk picture in one chart — if our trailing-quarter average is sitting above 60, every new campaign starts in the penalty window.

**What to look for:** Monthly trend of `avg_days_to_remedy` from `recall_analysis_metrics` with a 60-day reference line. Watch for the trend line crossing 60 — that's the moment the NHTSA exposure becomes systemic, not campaign-specific.

**Land the point:** When the CFO partner walks into the audit and risk-committee review with this curve, the conversation moves from *are we compliant* to *here's how much faster our remedy timeline is than the regulatory floor*. That's the recall-reserve conversation that used to need a steering committee and a law-firm memo.

### Question (Act 3.2)

> **Which regions have the highest warranty claim cost per claim, and what components are driving it?**

**What to say while it runs:** Top 10 vehicle models by `units_affected` in recall campaigns over the trailing 12 months. The units-affected ranking is the long-term reliability-program scorecard — the models that keep showing up are the ones with structural quality issues that no individual campaign fixes.

**What to look for:** Ranked list of models by total units affected. Watch for models that show up across multiple component groups — that's the reliability-redesign candidate, not just a campaign target.

**Land the point:** Three artifacts — supplier-consolidation case, campaign-launch order, recall-reserve forecast — all from one governed surface. The Quality VP, the Supplier-Quality Engineer, and the CFO partner are now committing to the same numbers. The supplier strategy and the recall reserve become one decision instead of three meetings and a quarterly steering committee.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — Apex Motor Group — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly recall event volume and total estimated cost for the trailing 12 months.
2. Top 10 suppliers by total estimated recall cost — which tier-1s are driving the most financial exposure?
3. Which component groups have the highest critical recall count and average days to remedy?
4. What is the total estimated cost of all open recall campaigns by component group?
5. How has average days to remedy trended month-over-month vs the NHTSA 60-day benchmark?
6. Top 10 vehicle models by units affected in recall campaigns over the trailing 12 months.
7. Which regions have the highest warranty claim cost per claim, and what components are driving it?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
