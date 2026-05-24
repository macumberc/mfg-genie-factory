# AeroChain Logistics — Demo Script

**Space:** Aerospace — AeroChain Logistics - Supply & Materials Planning 🔗
**Runtime:** ~15 minutes • 7 questions
**Audience:** COO + Procurement Manager, VP of Supply Chain
**KPIs touched:** Supplier on-time delivery %, Late delivery count vs. total PO count, Days of supply, Supplier quality %, Average lead time, Monthly spend by material class and supplier region
**Big decision automated:** Which long-lead materials to dual-source this quarter and which supplier regions to escalate before titanium or forging shortages stop the production line.

---

## Pre-demo checklist

- Open the Genie space `AeroChain Logistics - Supply & Materials Planning 🔗`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroChain Logistics sources 20 long-lead aerospace materials — titanium plate, nickel superalloys, carbon composites, structural forgings — from 6 supplier regions across North America, Europe, and Asia. Today the PO performance data lives in the Procurement Manager's SAP extract, the on-hand vs. days-of-supply lives in a planning spreadsheet refreshed weekly, and the single-source exposure map lives in the VP of Supply Chain's risk slide that gets rebuilt before every operating review. Three artifacts, same 20 materials — and the dual-source-or-stay-single decision gets made in the moment when a delivery slips, not as a planned risk-management cycle. This space ends that. One governed surface where lead time, on-hand inventory, supplier OTD, single-source exposure, and spend sit together, so the qualification-and-escalation decisions become a defensible quarterly cycle, not a reactive scramble after the next late delivery.

---

## Key KPIs in scope

- Supplier on-time delivery % (target >95%, industry benchmark 90-95%)
- Late delivery count vs. total PO count
- Days of supply (target 30-60 days for production materials, 90+ for long-lead forgings)
- Supplier quality % (acceptance rate, target >99% on flight-critical)
- Average lead time (weeks) — titanium 30-40 wks, composites 16-24 wks, forgings 40-60 wks
- Monthly spend (USD) by material class and supplier region
- Single-source material count — risk concentration metric
- Critical / at-risk material count blocking production

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **COO** | Chief Operating Officer |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the materials about to stop the line before procurement does *(≈4 min)*

**Persona:** Procurement Manager • **Job to be done:** Identify which materials are tracking late and which supplier regions are slipping against benchmark — before the production planner escalates.

*This is the moment the at-risk material list starts forming. Two queries in, the procurement manager already has the materials that need an expedite call this week and the suppliers that need a quarterly business review.*

### Question (Act 1.1)

> **Top 10 materials by total order value over the last 12 months, and which supplier regions ship them?**

**What to say while it runs:** Top 10 materials by order value over 12 months with their supplier regions. The high-value, region-concentrated materials are where single-source risk lives. Titanium plate concentrated in two regions, forgings concentrated in one — that's the exposure map procurement needs to defend.

**What to look for:** A ranked table of 10 materials by total_order_value with supplier_region. The room should see which materials are both expensive AND regionally concentrated — that's the dual-source candidate list.

**Land the point:** Right there is the qualification-program shortlist. The procurement manager can name the 3 materials that earn a dual-source qualification this year — and the conversation with sourcing moves from 'we should diversify' to 'here are the materials, here's the qualification budget.'

### Question (Act 1.2)

> **Show monthly trend in late delivery count by supplier region.**

**What to say while it runs:** Now late delivery count by supplier region over 12 months. Aerospace OTD benchmark is 90-95%; anything below 85% in a region is a structural reliability issue, not a one-off. Asia-Pacific forgings and European composite suppliers tend to be the leading-indicator regions.

**What to look for:** Monthly late_delivery_count by supplier_region using `DATE_TRUNC('month', ...)`. Watch for regions where the line is climbing — those are the supplier-business-review priorities.

**Land the point:** Before this space, that chart was a quarterly supplier-review artifact. Now it's the procurement manager's first question of the morning — and the conversation about which suppliers earn a CAPA or get put on probation starts a quarter earlier.

---

## Act 2 — The decision — dual-source these, escalate those, accept the risk on the rest *(≈4 min)*

**Persona:** VP of Supply Chain • **Job to be done:** Commit to a dual-source qualification list, a supplier-escalation list, and an at-risk material list — naming exactly where capital and contracting hours go.

*Three questions that turn the late-delivery and on-hand data into a defensible supply-risk action plan. The middle question is the anchor — converting at-risk material exposure into the production-line-down cost math the COO will sign off on.*

### Question (Act 2.1)

> **Which material classes have the lowest days of supply right now, and what is at risk?**

**What to say while it runs:** Material classes with the lowest days of supply right now. Production materials target is 30-60 days; long-lead forgings need 90+. Anything below 30 days on a titanium or forging line means production is one late shipment from a line-down event.

**What to look for:** Material classes ranked by avg_days_of_supply with critical_material_count alongside. The combination tells you what's already in the red and what's drifting toward it.

**Land the point:** That table is the line-down risk register. Two queries in, the VP of Supply Chain has a defensible escalation plan — and the conversation with the COO moves from 'supply is tight' to 'these 4 materials need a board-approved safety-stock bump this month.'

### Question (Act 2.2)

> **Top 10 supplier regions by average lead time in weeks — flag any above industry benchmark.**

**What to say while it runs:** Supplier regions ranked by average lead time in weeks. Titanium benchmark is 30-40 weeks, composites 16-24, forgings 40-60. Anything above benchmark on a high-value material is a dual-source case — single sourcing on a 50-week lead time is one geopolitical event away from a program slip.

**What to look for:** Supplier_region ranked by avg_lead_time_weeks with benchmark overlay. Watch for regions where lead times are creeping past benchmark — those are the dual-source priorities.

**Land the point:** That ranking is the dual-source qualification budget request. The VP of Supply Chain can defend $5-10M of qualification investment with the specific lead-time-vs-benchmark gap, not with a generic 'diversification' argument.

> **Anchor moment.** Park on the days-of-supply and lead-time views. Pick the worst-exposed material — say structural forgings at 22 days of supply with a 52-week lead time from a single supplier region.

> *An aerospace final-assembly line going down for material shortage costs $50-100K per aircraft-day in deferred revenue plus penalty exposure. If structural forgings cause a 4-day line stoppage across 5 aircraft on the line, that's 5 × 4 × $75K = $1.5M per event. With a 52-week lead time on the recovery, you can't expedite your way out — the only defense is safety stock or a qualified alternate source. Qualifying a second source runs $2-4M and 12-18 months; carrying an extra 60 days of safety stock runs maybe $3-5M in working capital. Versus one or two line-down events per year at $1.5M each plus program-slip penalties, both pencil. The dual-source pays back over 24 months and ends the single-source-risk slide forever.*

> That's the decision this space defends. The dual-source budget, the safety-stock bump, and the at-risk material register are written from one view. The COO approves the qualification capex on line-down math, not on a generic risk argument.

### Question (Act 2.3)

> **How has total monthly spend trended over the trailing 12 months by material class?**

**What to say while it runs:** Monthly total spend trend by material class over 12 months. Spend trajectory tells you which categories are inflating fastest — usually titanium and nickel superalloys lead — and which to lock under long-term agreements before the next price cycle.

**What to look for:** Monthly monthly_spend_usd by material_class. Categories where spend is climbing without volume climbing are the price-escalation conversations.

**Land the point:** That's the difference between knowing spend is up and knowing which categories to lock now vs. later. The first is a budget memo; the second is a multi-year supply-agreement decision worth tens of millions.

---

## Act 3 — The commitment — defending supply continuity to the COO and shaping next year's sourcing strategy *(≈4 min)*

**Persona:** COO • **Job to be done:** Approve the dual-source qualification capex, lock the multi-year supply agreements, and set the safety-stock policy for the next operating cycle.

*The COO doesn't need a new report — they need the same OTD, lead-time, and at-risk numbers the procurement team is acting on, packaged for the operating review and consistent across every supplier negotiation.*

### Question (Act 3.1)

> **Which materials are flagged as critical or at-risk this month, and what is on hand?**

**What to say while it runs:** Average lead-time weeks trend over 12 months. This is the structural-tightness story — if average lead times across the portfolio are climbing, the supply market is constrained and safety-stock policy needs to tighten. If they're falling, dual-source qualifications can be staged.

**What to look for:** Monthly avg_lead_time_weeks across material classes. The slope tells the COO whether next year's safety-stock budget needs to expand or hold.

**Land the point:** When that view is in the COO's hand at the operating review, the sourcing-strategy conversation becomes a leading-indicator story, not a reactive line-down apology. Multi-year supply agreements get signed on the right side of the price cycle.

### Question (Act 3.2)

> **Show monthly trend in average lead time weeks for the trailing 12 months.**

**What to say while it runs:** Materials flagged Critical or At-Risk this month with their on-hand position. This is the immediate-action list — the materials where production is one shipment from a line-down event. On-hand kg vs. days-of-supply tells you whether the answer is expedite, alternate source, or safety stock bump.

**What to look for:** Materials filtered to at_risk_flag IN ('Critical','At-Risk') with on_hand_kg. The shortest days of supply goes to the top of the escalation list.

**Land the point:** Procurement, the VP of Supply Chain, and the COO now share one view. The escalation list, the dual-source budget, and the supply-agreement strategy are written from the same numbers. One space. One supply story. Production stays on schedule.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroChain Logistics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 materials by total order value over the last 12 months, and which supplier regions ship them?
2. Show monthly trend in late delivery count by supplier region.
3. Which material classes have the lowest days of supply right now, and what is at risk?
4. Top 10 supplier regions by average lead time in weeks — flag any above industry benchmark.
5. How has total monthly spend trended over the trailing 12 months by material class?
6. Which materials are flagged as critical or at-risk this month, and what is on hand?
7. Show monthly trend in average lead time weeks for the trailing 12 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
