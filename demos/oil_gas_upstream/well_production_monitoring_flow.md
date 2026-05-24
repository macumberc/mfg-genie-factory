# WellFlow Monitoring — Demo Script

**Space:** Oil & Gas Upstream — WellFlow Monitoring — Well Production Monitoring 📊
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Production + ops team (Asset Manager, Field Superintendent, Production Engineer)
**KPIs touched:** Uptime, Artificial Lift Efficiency, Water Cut, GOR, Deferred Oil (BBL), LOE/BOE, Oil Rate (BOPD)

---

## Pre-demo checklist

- Open the Genie space `WellFlow Monitoring - Well Production Monitoring 📊`.
- Confirm the SQL warehouse is **warm** — first query latency is the only thing that can flatten the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain — the morning Excel ritual, the disputed deferred-barrel number, the LOE benchmarking gap]. Watch what happens when that's a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> WellFlow Monitoring runs 20 horizontal and vertical wells across 11 multi-well pads — Wolfcamp, Bone Spring, Eagle Ford, Bakken, Marcellus, the usual suspects. Today their production data lives in SCADA, the JIB, the AFE system, and a stack of well files. Every morning, a Production Engineer spends the first hour stitching it together in Excel to figure out which wells need attention. The Field Superintendent has a different spreadsheet to rank pads. The Asset Manager has a third one for the monthly review. Three teams, three workbooks, same underlying data. We built one governed space on top of it. Let me show you what their day looks like with it.

---

## Act 1 — The Production Engineer's morning triage *(~4 min)*

**Persona:** Production Engineer • **Job to be done:** Find the wells that need attention today.

### Question 1

> **Which wells have uptime below 90% or lift efficiency below 70%, and what pad are they on?**

**What to say while it runs:** "Two thresholds — 90% uptime, 70% lift efficiency — these aren't my numbers, those are the engineer's standing rules. Anything below either one gets a root-cause review."

**What to look for:** A short table of wells with their pad name, uptime %, and lift efficiency %. Click *Show generated code* once — show the room the SQL is auditable.

**Land the point:** "That's the first 30 minutes of every morning, answered in 8 seconds. And nobody had to build a dashboard for it."

### Question 2 (follow-up — show conversational memory)

> **For those wells, how has GOR trended month over month?**

**What to say:** "Notice I didn't restate which wells. Genie carries the context. Rising GOR can mean gas breakthrough or reservoir-energy decline — that's the engineer's next diagnostic step, and they got there without leaving the conversation."

**Land the point:** "This is what 'AI as a teammate' actually looks like. Not a search box — a back-and-forth that mirrors how your engineers already think."

---

## Act 2 — The Field Superintendent's pad ranking *(~5 min)*

**Persona:** Field Superintendent • **Job to be done:** Decide where the workover rig goes this week and where capex gets prioritized next quarter.

### Question 3

> **Top 10 wells by water cut % — and how does that compare to last quarter?**

**What to say:** "Water cut above 60% means you start prioritizing water-handling capacity. Above 75%, you're near the economic limit. The 'vs last quarter' is the part the spreadsheet workflow usually skips because it's too much work."

**Land the point:** "That comparison is the difference between knowing a well is bad and knowing it's getting worse. That changes the capex conversation."

### Question 4 — the anchor moment

> **Show the monthly trend in total deferred oil BBL by pad for the trailing 12 months.**

**What to say while it renders:** "Deferred oil is barrels you didn't produce because of downtime, chokes, or shut-ins. Every one of those is recoverable revenue if you find the root cause."

**Land the point — do the math out loud:** "Look at [pick the worst pad on the chart]. Call it 500 deferred barrels a month. At $70 oil, that's $420,000 of recoverable revenue per year — on one pad. Multiply across 11 pads and this conversation pays for the platform several times over."

> If the room engages with the number, stay here. This is the beat that converts.

### Question 5

> **Which pads have the most shut-in or workover wells right now, and what is the deferred oil impact?**

**What to say:** "Now the superintendent has a workover prioritization list, ranked by dollars at stake, not by who emailed loudest."

**Land the point:** "Same data your team already has. The difference is they can act on it before the morning standup, not after."

---

## Act 3 — The Asset Manager's monthly review *(~4 min)*

**Persona:** Asset Manager • **Job to be done:** Defend the portfolio's performance to the executive team and shape next year's AFE.

### Question 6

> **What is the average LOE per BOE by pad and well type year to date?**

**What to say:** "Onshore US benchmark for lease operating expense is $6 to $12 per BOE. Anything above $12 is a cost-leadership flag for that pad. This is the slide the Asset Manager rebuilds every month."

**Land the point:** "And right now, this is governed. Every team querying this is using the same definition of LOE/BOE, the same definition of uptime, the same definition of water cut. No more two VPs walking into the same meeting with two different numbers."

### Question 7 (close on a high note)

> **Top 10 wells by average oil rate (BOPD) over the last 90 days.**

**What to say:** "And on the upside — these are the wells shaping next year's AFE. The completion designs, the spacing, the artificial lift choices that worked. That's the conversation that drives the investment story."

**Land the point:** "Triage, prioritization, and portfolio strategy. One space. Three teams. Zero new dashboards."

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the Asset Manager and the engineer both ask about uptime, they get the same number.
2. **Conversational, not dashboard sprawl.** You didn't see a single pre-built dashboard. Every chart in this demo was generated by a question. That means the next question — the one you haven't thought of yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of your engineers' day, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is 20 wells with three tables. Now imagine 200 wells, plus your AFE data, plus your facility data, plus your completion data — all in the same space, governed the same way, asked the same way. That's the shape of the conversation we should have next."

---

## Anticipated questions

**"How do we know it isn't making the SQL up?"**
Every answer ships with the generated SQL one click away. It runs against your governed tables in Unity Catalog. If it's wrong, it's auditable wrong — and you can correct the metric definition once and have every future answer benefit. Unlike an LLM answering from training data, Genie can only return what the SQL actually returns.

**"What about row-level and column-level security?"**
Unity Catalog's row filters and column masks apply automatically. If a Field Superintendent only has access to their own pads, that's exactly what Genie can answer about — same governance you already have.

**"Can we add our own KPIs?"**
Yes. The KPI definitions you saw (uptime, water cut, LOE/BOE, deferred oil) live in metric views as YAML. They're version-controlled, peer-reviewed, and authored once. New KPI = a pull request, not a new dashboard.

**"How fresh is the data?"**
Whatever your ingestion cadence is. Daily SCADA loads feed `production_readings`, weekly engineering reviews feed `well_status_snapshots`, monthly accounting close feeds `production_kpi_monthly`. Genie always queries the current state.

**"Who else in upstream uses this?"**
Happy to share specific references after this call. The pattern — daily triage + pad ranking + monthly review against one governed space — is the standard upstream production-monitoring shape.

---

## Quick-reference card (read off-screen)

1. Which wells have uptime below 90% or lift efficiency below 70%, and what pad are they on?
2. For those wells, how has GOR trended month over month?
3. Top 10 wells by water cut % — and how does that compare to last quarter?
4. Show the monthly trend in total deferred oil BBL by pad for the trailing 12 months.
5. Which pads have the most shut-in or workover wells right now, and what is the deferred oil impact?
6. What is the average LOE per BOE by pad and well type year to date?
7. Top 10 wells by average oil rate (BOPD) over the last 90 days.

**Three "land the point" beats not to miss:** Q1 (30-min Excel ritual → 8 seconds), Q4 (deferred barrels × oil price = real money), Q6 (one governed definition across teams).
