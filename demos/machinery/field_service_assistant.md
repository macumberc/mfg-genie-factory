# FieldForce Machinery — Demo Script

**Space:** Machinery — FieldForce Machinery - Field Service Assistant 🛠️
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Service + Service Manager, Dispatcher, CFO
**KPIs touched:** First-time fix rate, SLA compliance, Mean time to resolution, Mean time to dispatch, Technician utilization, Cost per ticket
**Big decision automated:** Which 5-10 install-base accounts get up-sold to a subscription service contract, which equipment families lose the warranty-extension fight, and how technician routing gets rebuilt around first-time-fix dollars instead of geographic convenience.

---

## Pre-demo checklist

- Open the Genie space `FieldForce Machinery - Field Service Assistant 🛠️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FieldForce supports an install base of 20 equipment SKUs — Excavators, Cranes, Generators, Compressors, Pump Systems — across Northeast, Southeast, Midwest, and West regions, serviced through a roughly 50-technician field force. Today the Service Manager works ticket queues out of the ServiceMax dashboard, the Dispatcher routes techs from a separate scheduling tool, and the VP Service tracks first-time fix rate and SLA compliance from a Friday-night PowerBI rollup. Three systems, the same install base, and the warranty-vs-out-of-warranty accountability conversation gets settled by whoever has the freshest spreadsheet. This space ends that: one governed surface where ticket cost, FTF rate, SLA compliance, and repeat-visit rate resolve to the same equipment family and the same region — so the subscription-contract up-sell list and the routing rebuild can both be made on the same dollars.

---

## Key KPIs in scope

- First-time fix rate (%) — industry leader benchmark ≥80%, average 70–75%
- SLA compliance (%) — target ≥95%
- Mean time to resolution (hrs) — customer-experience driver
- Mean time to dispatch (hrs) — early operational lever
- Technician utilization (%) — target 75–85% (productive hours)
- Cost per ticket ($) — service margin input
- Repeat visit rate (%) — leaders <10%
- Customer satisfaction (1–5) — NPS proxy for service relationship

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **SLA** | Service Level Agreement |
| **VP** | Vice President |

---

## Act 1 — The signal — which equipment families are draining service margin this quarter *(≈4 min)*

**Persona:** Service Manager • **Job to be done:** Find this week's accountability hot-list before the regional QBR — which equipment types are dragging FTF and which issue categories are bleeding cost.

*This is the conversation that shapes whose performance review gets a hard discussion and whose product gets escalated to engineering. Two questions in, the Service Manager already has the list.*

### Question (Act 1.1)

> **What is the monthly trend in first-time fix rate by equipment type over the trailing 12 months?**

**What to say while it runs:** Monthly trend in avg_ftf_rate by equipment_type. Industry leaders run 80%+; the average shop sits at 70-75%. Anything below 65% sustained for three months is a training gap, a parts-availability gap, or a product-reliability gap — and each one has a different owner.

**What to look for:** Five lines on one chart — Excavator, Crane, Generator, Compressor, Pump System. Watch for the family that's been flat or declining; that's the candidate for either a tech-training sprint or an engineering escalation.

**Land the point:** When the Service Manager can see which families are losing the FTF battle without rebuilding the BI extract, the Friday escalation conversation moves from gut-feel to numbers. That's the difference between blaming the techs and fixing the parts kit.

### Question (Act 1.2)

> **Top 10 equipment models by average resolution hours — which need the most dispatch time?**

**What to say while it runs:** Top 10 equipment_models by avg_resolution_hours. Resolution hours is the customer-experience proxy and the technician-cost driver in one number. The longer the resolution, the more travel time, the more parts-trip rework, the worse the CSAT.

**What to look for:** Ranked models with avg_resolution_hours. Look for the outliers — a model with double the family average is either an under-trained tech population or a known engineering issue burning service hours.

**Land the point:** That ranked list used to come out of a ServiceMax extract on Friday. Now it's the input to the dispatch decision on Monday — which models get senior techs assigned, which get junior techs paired with a remote-assist call. Routing-by-skill becomes routine, not a project.

---

## Act 2 — The decision — subscription contract up-sell list and warranty-vs-out-of-warranty accountability *(≈4 min)*

**Persona:** VP Service • **Job to be done:** Lock the install-base accounts that get the subscription-contract pitch this quarter, and decide which equipment families take the warranty cost vs. the customer.

*These three questions are where the aftermarket revenue story gets defended. Issue categories tell you where engineering owes you a fix; SLA compliance tells you where the contract terms are bleeding; the cost-vs-FTF chart is the up-sell conversation.*

### Question (Act 2.1)

> **Which issue categories drive the highest total service cost this quarter?**

**What to say while it runs:** Total_service_cost by issue_category this quarter. Mechanical, Hydraulic, and Software each have very different P&L profiles — Mechanical we can train against, Hydraulic is a parts-pipeline problem, Software is an engineering escalation. The dollar split is who owes us a fix.

**What to look for:** Bar chart by issue_category with total_service_cost. Watch for Software or Hydraulic taking a disproportionate share — that's the cost we're absorbing on behalf of product engineering.

**Land the point:** When the VP Service walks into the engineering QBR with 'Hydraulic issues are $X of last quarter's service cost,' the conversation stops being qualitative. Warranty cost recovery gets a sharper number, and the install-base accountability conversation has actual ammunition.

### Question (Act 2.2)

> **Rank equipment types by SLA compliance — which are below the 95% target?**

**What to say while it runs:** Equipment_type ranked by avg_sla_compliance against the 95% target. Below 95% means the contract terms are being missed — either the dispatch model isn't sized for the install base or the parts depot isn't placed right. Both are operational fixes the dispatcher can act on this week.

**What to look for:** Ranked equipment_type with avg_sla_compliance. The families below 90% are the immediate escalation; the ones at 90-95 are the tuning candidates.

**Land the point:** Same numbers the Service Manager is looking at, now framed as contract risk. Each percentage point below 95 has a credit-back dollar value — and now that lives in the same conversation as the routing decision. That's customer-economic, not operational-trivia.

> **Anchor moment.** Stop on the SLA-compliance ranking and the cost-vs-FTF chart. Pick an equipment family running 88% SLA at $2,400 average cost per ticket — call it Generators, our largest install base with about 200 units in the field.

> *Each Generator service ticket runs $2,400 fully-loaded and we average 7 tickets per generator per year on out-of-warranty assets — that's $17K of service spend per asset, much of which the customer is paying piecemeal. A subscription contract at $20-30K/year converts that into predictable recurring revenue while pulling FTF rate up to 85%+ because preventive visits replace emergency ones. Across 100 of the 200 generators converting at $25K/year uplift, that's $2.5M of recurring aftermarket revenue annually — and the warranty cost recovery on Hydraulic and Software issues is a separate $300-500K of cost reduction. Combined: a $3M annual margin story on the Generator install base alone.*

> Subscription service contracts on heavy equipment carry $5-25K/asset/year of recurring revenue versus break-fix at maybe $3-5K/year. The math is the up-sell list and the routing rebuild become one conversation, owned by the VP Service, defended on the same numbers the dispatcher is acting on.

### Question (Act 2.3)

> **Show monthly trend in average cost per ticket vs first-time fix rate across the install base.**

**What to say while it runs:** Monthly trend in avg_cost_per_ticket overlaid with avg_ftf_rate. The relationship between these two is the heart of service margin — when FTF goes up, cost per ticket goes down because the second visit doesn't happen. This chart tells you whether the service line is winning or losing on margin.

**What to look for:** Two lines on one chart, 12 months. We want cost per ticket trending down while FTF trends up. The cross-over points are where the operational changes actually paid off.

**Land the point:** When the CFO sees that cost per ticket dropped $200 while FTF moved from 71% to 79%, the service line stops being a cost center and starts being an aftermarket profit story. That's the subscription-contract pitch.

---

## Act 3 — The commitment — locking next year's service-line P&L and the install-base playbook *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend service-line margin expansion to the board and commit to the subscription-contract growth target.

*The CFO doesn't need another monthly service deck; they need top-N high-resolution-hour tickets and the worst repeat-visit families in the same conversation, because the cost story and the up-sell story are the same story.*

### Question (Act 3.1)

> **Top 10 highest-priority tickets by resolution hours in the last 30 days.**

**What to say while it runs:** Top 10 highest-priority tickets in the last 30 days ranked by resolution_hours. These are the tickets that ate the most technician time on the most important jobs — and they're the tickets the customer remembers when contract renewal comes up. The customers behind these tickets are either churn risks or up-sell candidates; rarely neutral.

**What to look for:** Ranked tickets with ticket_id, equipment_model, priority, resolution_hours. Watch for the same equipment_model showing up multiple times — that's a single account with a structural issue.

**Land the point:** When the CFO can see by name which 10 customer-tickets ate the quarter's service margin, the account-management conversation becomes specific. Renewal risk gets surfaced before it's a churn email; up-sell candidates get pitched while the pain is fresh.

### Question (Act 3.2)

> **Which equipment types have the worst repeat visit rate, and what is the cost impact?**

**What to say while it runs:** Equipment_type ranked by total_repeat_visit_percent. Leaders run under 10%; above 15% is a structural quality or training problem. Each repeat visit is a free service call we ate — and the dollar value times the install base is the cost we're carrying invisibly.

**What to look for:** Ranked equipment_type with total_repeat_visit_percent. The worst family is either the next training investment, the next engineering escalation, or the next family we don't take new service contracts on.

**Land the point:** Same install base, same techs, same dispatch tool — but now the routing decision, the contract decision, and the engineering escalation all happen against the same numbers. Service stops being three teams stitching three systems and becomes one P&L story the VP Service defends in one slide.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FieldForce Machinery — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. What is the monthly trend in first-time fix rate by equipment type over the trailing 12 months?
2. Top 10 equipment models by average resolution hours — which need the most dispatch time?
3. Which issue categories drive the highest total service cost this quarter?
4. Rank equipment types by SLA compliance — which are below the 95% target?
5. Show monthly trend in average cost per ticket vs first-time fix rate across the install base.
6. Top 10 highest-priority tickets by resolution hours in the last 30 days.
7. Which equipment types have the worst repeat visit rate, and what is the cost impact?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
