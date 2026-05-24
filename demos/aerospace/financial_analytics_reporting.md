# AeroLedger Corp — Demo Script

**Space:** Aerospace — AeroLedger Corp - Financial Analytics & Cost Reporting 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO + Segment Controller, FP&A Lead
**KPIs touched:** Gross margin %, Operating margin %, EBITDA and EBITDA margin %, Revenue variance vs. budget %, Revenue per employee, Backlog book-to-bill ratio
**Big decision automated:** Which business segments earn the next $50M of program capex and which cost centers get a budget reset before next quarter's earnings call.

---

## Pre-demo checklist

- Open the Genie space `AeroLedger Corp - Financial Analytics & Cost Reporting 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroLedger Corp runs 20 cost centers across 5 business segments — Commercial Aviation, Defense, Space, Business Jets, and Services. Today the segment revenue rollup lives in the Controller's HFM-extracted Excel, the variance-vs-budget analysis lives in the FP&A binder for the monthly review, and the EBITDA-by-segment story lives in the slide deck the CFO rebuilds for the audit committee. Three artifacts, same GL — and the capex defense at the quarterly program review gets reduced to whoever has the freshest numbers, not the right numbers. This space ends that. One governed surface where revenue, COGS, margin, R&D spend, and variance sit together, so the capex-allocation decision becomes a 30-minute conversation in front of the board, not a three-day reconciliation drill before it.

---

## Key KPIs in scope

- Gross margin % — A&D commercial benchmark 18-22%, defense 10-15%, services 25-35%
- Operating margin % — top-tier A&D ~10-12%
- EBITDA (USD) and EBITDA margin %
- Revenue variance vs. budget % (flag >5% adverse)
- Revenue per employee (USD) — productivity benchmark $300K-$500K in A&D
- Backlog book-to-bill ratio (target >1.0 for growth)
- Total R&D spend (USD) — innovation indicator, typical 4-7% of revenue in A&D
- Cost efficiency ratio (actual cost / budgeted cost; target <1.0)

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, and Amortization |

---

## Act 1 — The signal — finding the cost centers carrying margin and the ones quietly bleeding it *(≈4 min)*

**Persona:** Segment Controller • **Job to be done:** Identify which cost centers are driving revenue and gross margin growth and which are dragging the segment number before close.

*This is the moment the segment scorecard starts forming for the operating review. Two queries in, the controller already knows which cost centers carry the story and which need a deeper diagnostic.*

### Question (Act 1.1)

> **Top 10 cost centers by total revenue over the last 12 months — and what are their gross margins?**

**What to say while it runs:** Top 10 cost centers by total revenue YTD with their gross margin. A&D commercial benchmark on GM% is 18-22%, defense 10-15%, services 25-35%. Anything where revenue is high but GM% is below benchmark for the segment is where margin is being given away — that's a pricing or COGS conversation, not a volume conversation.

**What to look for:** A ranked table of 10 cost centers with revenue rank alongside gross_margin_pct. The room should see which cost centers earn their seat (high revenue, in-band margin) vs. which are subsidized (high revenue, low margin).

**Land the point:** Right there is the segment review opener. The controller can name three cost centers worth defending and two worth scoping for a margin reset — without rebuilding the deck.

### Question (Act 1.2)

> **Show monthly trend in total revenue by business segment for the trailing 12 months.**

**What to say while it runs:** Now the monthly revenue trend by business segment over 12 months. The mix shift between Commercial, Defense, and Services is the story the CFO carries to the earnings call. Defense steady, Commercial cyclical, Services growing is the right shape; anything else needs an explanation.

**What to look for:** Monthly revenue by business_segment using `DATE_TRUNC('month', ...)`. Watch for segments where the trend is breaking against the operating-plan narrative.

**Land the point:** Before this space, that chart was a monthly artifact for the operating review. Now it's the controller's first question of the day — and the conversation about which segments need a forecast revision starts a month earlier.

---

## Act 2 — The decision — naming the capex winners, naming the cost-center resets *(≈4 min)*

**Persona:** FP&A Lead • **Job to be done:** Commit to a segment-level capex recommendation and the list of cost centers that miss next quarter's budget allocation.

*Three questions that turn variance and R&D-spend data into a defensible capital-allocation recommendation. The middle question is the anchor — converting cost-efficiency drift into the recoverable-cost dollars the CFO can defend at the board.*

### Question (Act 2.1)

> **Which business segments have the largest unfavorable revenue variance vs. budget this quarter?**

**What to say while it runs:** Revenue variance vs. budget by segment this quarter. We flag anything over 5% adverse. Adverse variance on Commercial Aviation right now is volume; on Defense it's typically contract-timing; on Services it's pricing. The category determines whether it's a forecast fix or a cost-center conversation.

**What to look for:** Segments ranked by unfavorable revenue_variance_pct. Watch for asymmetry — a segment with big adverse revenue variance AND climbing COGS is the segment whose capex defense just got harder.

**Land the point:** That ranking is the variance-narrative outline the FP&A lead builds the review around. No more 'why was Commercial soft' as a board surprise — it's already in the controller's morning view.

### Question (Act 2.2)

> **Top 10 projects by R&D spend in the last 12 months.**

**What to say while it runs:** Top 10 projects by R&D spend over the last 12 months. A&D typically runs R&D at 4-7% of revenue. Anything where a single project consumes a disproportionate slice of the R&D envelope is a conversation: is this on the TRL maturity curve, or is it a runaway? That's a capex conversation.

**What to look for:** Projects ranked by total_rd_spend. The shape — concentrated in one or two programs vs. distributed — tells the room whether R&D is portfolio'd or under-diversified.

**Land the point:** That table is the R&D capex defense. Two queries in, the FP&A lead has a defensible recommendation to walk into the board — and the conversation moves from 'R&D is too high' to 'these 3 programs are 70% of the spend, here's the gate decision on each.'

> **Anchor moment.** Land on the cost-efficiency ratio table from earlier. Pick the worst-offending cost center — call it $80M annual budget running at a 1.15 cost-efficiency ratio.

> *1.15 ratio means $12M of cost overrun against that $80M budget — recurring. If 4 cost centers across AeroLedger's 20 are running at 1.10+, the segment-level structural overrun is roughly 4 × $80M × 0.10 = $32M per year. Reset to budget on three of them captures $20-25M of operating margin — that's 1-2 points of consolidated operating margin against A&D's 10-12% benchmark. At the multiple AeroLedger trades at, that's $200-400M of enterprise value the cost-center reset defends.*

> That's the decision this space automates. The capex slate and the cost-center reset list get written from the same view. The CFO walks into the board with a defended margin number, not a 'we'll get back to you.'

### Question (Act 2.3)

> **How has operating margin trended month-over-month by business segment?**

**What to say while it runs:** Cost centers exceeding their cost budget. Cost-efficiency ratio benchmark is below 1.0 — anything above 1.1 is structural. We're not interested in noise here, we're interested in the cost centers that consistently overrun. Those are the next-cycle budget-reset candidates.

**What to look for:** Cost centers ranked by cost_efficiency_ratio above 1.0. The point isn't the list, it's that the list is the reset target.

**Land the point:** That comparison is the difference between knowing a cost center is over and knowing it's structurally over. The first gets a memo; the second gets a budget cut. The CFO needs the second.

---

## Act 3 — The commitment — defending the capex slate to the board and shaping the earnings narrative *(≈4 min)*

**Persona:** CFO • **Job to be done:** Defend program capex against the operating plan and lock in next quarter's segment-level investment story for the earnings call.

*The CFO doesn't need a new dashboard — they need the same revenue, margin, and variance numbers the controller is acting on, packaged for the board and consistent with the guidance already given to the Street.*

### Question (Act 3.1)

> **Which cost centers exceed their cost budget, and by how much?**

**What to say while it runs:** Operating margin by segment month over month. Top-tier A&D operating margin is 10-12%; anything that slips below 8% for two consecutive months is a Street-facing problem, not an internal one. This is the chart the audit committee asks for.

**What to look for:** Monthly trend of operating_margin_pct by business_segment. Watch for two-month declines — that's the threshold for a guidance conversation.

**Land the point:** When the CFO can pull this view live in front of the board, the conversation about which segments earn capex and which earn a cost-out plan is grounded in the same numbers the segment teams are managing to. No more 'we'll need to take that offline.'

### Question (Act 3.2)

> **Show monthly trend in EBITDA by business segment for the trailing 12 months.**

**What to say while it runs:** EBITDA trend by segment over 12 months. This is the line the Street tracks. Services growing EBITDA faster than Commercial is the right shape for a services-led narrative; the inverse is a problem. The book-to-bill above 1.0 is what defends the multiple.

**What to look for:** Monthly ebitda_usd by business_segment. The slope of each line — and where Services sits — is the earnings-narrative story.

**Land the point:** Segment controllers, FP&A, and the CFO now share one view. The earnings call story matches the operating-review story matches the cost-center reset story. One space. One number. One narrative.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroLedger Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 cost centers by total revenue over the last 12 months — and what are their gross margins?
2. Show monthly trend in total revenue by business segment for the trailing 12 months.
3. Which business segments have the largest unfavorable revenue variance vs. budget this quarter?
4. Top 10 projects by R&D spend in the last 12 months.
5. How has operating margin trended month-over-month by business segment?
6. Which cost centers exceed their cost budget, and by how much?
7. Show monthly trend in EBITDA by business segment for the trailing 12 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
