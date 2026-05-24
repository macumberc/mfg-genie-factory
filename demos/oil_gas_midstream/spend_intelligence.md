# MidSpend Analytics — Demo Script

**Space:** Oil & Gas Midstream — MidSpend Analytics - Spend Intelligence 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Procurement + Chief Procurement Officer, Category Managers, Operations Director
**KPIs touched:** Total spend, Savings, Maverick spend, Contract compliance, Supplier quality score, On-time delivery
**Big decision automated:** Which suppliers to consolidate to in the top 3 spend categories, which High-risk-tier suppliers we exit, and which MRO category gets the next sourcing campaign.

---

## Pre-demo checklist

- Open the Genie space `MidSpend Analytics - Spend Intelligence 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> MidSpend Analytics manages procurement across compressor parts, valves and actuators, line pipe, integrity services, chemicals, and contract labor for a midstream operator. Today the supplier-spend ranking lives in the Procurement VP's annual category review, the quality and on-time-delivery scorecard lives in the category manager's supplier dashboard, and the maverick-spend report lives in the finance team's monthly accruals workbook. Three workbooks, same suppliers — and the consolidation decisions, the contract-compliance campaigns, and the High-risk-tier exits all get made on snapshots that don't agree on who the top supplier even is. This space ends that. One governed surface where total_spend_usd, quality_score, on_time_delivery_pct, and maverick_spend_pct line up by supplier and spend category — so the consolidation conversation moves from a savings target to a signed letter of intent.

---

## Key KPIs in scope

- Total spend ($) — addressable procurement spend
- Savings ($) — realized cost reductions vs. baseline
- Maverick spend (%) — off-contract spend (target <5%)
- Contract compliance (%) — % of spend on contracted terms
- Supplier quality score (0-100) — composite supplier scorecard
- On-time delivery (%) — supplier OTD (target >95%)
- Defect rate (%) — supplier quality issues (target <2%)
- Avg lead time (days) — supplier responsiveness

---

## Act 1 — The signal — where the spend is concentrated and where the maverick leakage lives *(≈4 min)*

**Persona:** Category Manager • **Job to be done:** Identify the spend categories driving the bulk of addressable spend and the supplier rankings before the quarterly category review.

*This is the moment the consolidation pitch starts to form. Two questions in, the category team has the spend-category trend and the supplier ranking that used to take a quarter of ERP extracts and pivot work.*

### Question (Act 1.1)

> **Show monthly total spend by spend category for the trailing 12 months.**

**What to say while it runs:** Monthly total_spend by spend_category over the trailing 12 is the addressable-spend view. We typically see 70% of spend living in 4-5 categories — line pipe, valves and actuators, compressor parts, integrity services, chemicals. Those are the categories where consolidation moves the financial result; everything else is noise.

**What to look for:** Monthly bars of total_spend_usd by spend_category — DATE_TRUNC('month', transaction_date) shape. The room should notice which categories dominate and which are seasonal or project-driven.

**Land the point:** Now the category manager walks into the QBR with the spend-category picture already framed — and the consolidation pitch starts from data the CFO trusts, not a deck the VP Procurement has to defend.

### Question (Act 1.2)

> **Top 10 suppliers by total spend year-to-date.**

**What to say while it runs:** Top 10 suppliers by total_spend YTD is the consolidation-candidate view. The Pareto rule shows up here too — usually the top 10 carry 50-60% of addressable spend. The question for each one is: are we paying market, or are we paying tail-spend prices because we never consolidated?

**What to look for:** Ranked table of supplier_name with total_spend_usd. The top 10 are exactly the suppliers whose next master-agreement renewal is the leverage point for category-wide rate reductions.

**Land the point:** That list used to be the output of a once-a-year category review. Now it's a question — and the renewal-leverage conversation happens four times a year, not once.

---

## Act 2 — The decision — consolidating to fewer suppliers and exiting the High-risk tier *(≈4 min)*

**Persona:** VP Procurement • **Job to be done:** Lock the supplier-consolidation list for the next sourcing cycle and decide which High-risk-tier suppliers we exit.

*Three questions that turn the supplier ranking into a consolidation and risk-mitigation decision. The middle question is the anchor — the spend-times-savings-rate math that converts a procurement view into a CFO-grade savings commitment.*

### Question (Act 2.1)

> **Which suppliers have a quality score below 70, and what is their on-time delivery percentage?**

**What to say while it runs:** Suppliers with quality_score below 70 and their on_time_delivery_pct is the supplier-exit view. Below 70 quality combined with below-95% OTD is the profile of a supplier we either restructure with a corrective-action plan or replace. We don't want to be the operator that keeps a bad supplier because exiting is awkward.

**What to look for:** Table of supplier_name with quality_score < 70 and on_time_delivery_pct. The combination of low quality and low OTD is the queue topper for category-team intervention.

**Land the point:** When the VP Procurement can pull both quality and OTD in one view, the supplier-exit conversation moves from a year-end scorecard slap-on-wrist to a Q+30 decision the category team commits to with the supplier in writing.

### Question (Act 2.2)

> **How has maverick spend percentage trended month-over-month across the company?**

**What to say while it runs:** Maverick_spend_pct trended month-over-month is the contract-leakage view. Best-in-class operators run below 5% maverick spend; anything above 10% means we're either under-contracted, the requesters are bypassing the catalogs, or the master agreements aren't getting used. Each of those has a different fix.

**What to look for:** Monthly trend of avg maverick_spend_pct. A flat-to-declining curve under 5% is healthy; a climbing curve is a process problem we need to attack at the requisition layer.

**Land the point:** That trend turns 'reduce maverick spend' from a perennial procurement initiative into a measurable program with a number, a slope, and an owner. The CFO can see whether the campaign is working in real time.

> **Anchor moment.** Hold on the top-10 supplier ranking from Act 1 and the maverick-spend trend on screen. Take the top spend category — valves and actuators, call it $180M annual spend across 11 suppliers, 14% maverick spend.

> *$180M annual spend with 11 suppliers and a typical midstream consolidation target of 3-4 strategic suppliers historically yields 4-7% category savings — call it 5% conservative on $180M, that's $9M/year of recurring savings. Closing maverick spend from 14% to under 5% on the same base ($16M of off-contract spend pulled onto contracted terms at typical 8% spread) is another $1.3M/year. Combined, $10M+/year of repeatable savings on a single category — and that's just one of the top 4. Across the top 4 categories the total realistic recurring savings is $25-40M/year on a $700M addressable spend.*

> That's the decision this space automates. Not the QBR slide. The signed letter of intent. The supplier-consolidation move goes from a savings target the CFO is asked to believe to a list of suppliers, signed agreements, and a measurable run-rate.

### Question (Act 2.3)

> **Top 10 suppliers by total realized savings this year.**

**What to say while it runs:** Spend categories with the most High risk-tier exposure and their total_spend is the risk-concentration view. Risk-tier exposure isn't just about quality; it's about geopolitical, financial, and single-source risk that turns into integrity-event exposure on the pipe. High-risk-tier dollars are where the dual-source program has to land.

**What to look for:** Spend_category with risk_tier = High count and total_spend_usd. High-spend, High-risk-tier is the category where the next dual-source campaign earns the most risk reduction per sourcing dollar.

**Land the point:** When the Procurement VP can pair risk-tier with spend dollars, the dual-source decision stops being a generic mandate and becomes a ranked program — and the category that earns the next dual-source RFP is no longer up for debate.

---

## Act 3 — The commitment — locking the strategic supplier book and the operational scorecard *(≈4 min)*

**Persona:** Chief Procurement Officer • **Job to be done:** Defend the consolidated supplier book to the executive team and lock the operational supplier scorecard with operations leadership.

*The CPO doesn't need a third procurement dashboard; they need the same spend, quality, and OTD numbers the category managers and operations directors are running on — so the executive savings pitch and the operations scorecard are built off one source.*

### Question (Act 3.1)

> **Which spend categories carry the most High risk-tier exposure, and what is the total spend?**

**What to say while it runs:** Top 10 suppliers by total realized savings this year is the where-the-program-is-working view. We celebrate the suppliers who delivered against the consolidation thesis — and we use the laggards as evidence in the next negotiation cycle.

**What to look for:** Ranked table of supplier_name with savings_usd. The top 5 are the testimonials for the next sourcing campaign; the bottom of the top-10 is where the next contract-renewal renegotiation pressure goes.

**Land the point:** When the CPO can show the executive team realized savings by supplier name, the procurement program stops being a target on a slide and becomes a track record — and that's how the next year's stretch savings target gets believed.

### Question (Act 3.2)

> **What is the average lead time by spend category, and how has it trended monthly?**

**What to say while it runs:** Average lead_time by spend_category trended monthly is the operations-impact view. Procurement isn't just about cost — extended lead times directly delay integrity work and unplanned-event response, and operations leadership feels every day of lead-time slip. We want a flat or declining trend, especially in compressor parts and integrity services.

**What to look for:** Monthly trend of avg_lead_time by spend_category. A rising lead-time curve in a critical category is what we need to catch before it shows up as an extended pipeline outage.

**Land the point:** Triage in the category meeting in the morning, ops impact reviewed by afternoon, executive savings pitch built off the same numbers Friday. Same space. Same numbers. The category manager's supplier list, the VP Procurement's consolidation pitch, and the CPO's executive narrative are now the same artifact.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — MidSpend Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total spend by spend category for the trailing 12 months.
2. Top 10 suppliers by total spend year-to-date.
3. Which suppliers have a quality score below 70, and what is their on-time delivery percentage?
4. How has maverick spend percentage trended month-over-month across the company?
5. Top 10 suppliers by total realized savings this year.
6. Which spend categories carry the most High risk-tier exposure, and what is the total spend?
7. What is the average lead time by spend category, and how has it trended monthly?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
