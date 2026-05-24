# RefineOps Central — Demo Script

**Space:** Oil & Gas Refining — RefineOps Central - Production Monitoring 📊
**Runtime:** ~15 minutes • 7 questions
**Audience:** COO + Refinery Manager, Operations Planner, COO
**KPIs touched:** Unit utilization, Throughput by unit and refinery section, Product yield, Mechanical availability, Energy intensity, Gross margin and OPEX per barrel
**Big decision automated:** Which 2-3 conversion units get the FCC catalyst change call this cycle, which units get severity-pushed to capture crack-spread upside, and which units below the $8/bbl gross-margin threshold lose the slate-allocation fight.

---

## Pre-demo checklist

- Open the Genie space `RefineOps Central - Production Monitoring 📊`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RefineOps Central runs 20 process units spanning Primary (Crude/Vacuum), Conversion (FCC, Hydrocracker, Reformer, Alkylation, Coker), Treating, Blending, Gas Processing, and Utilities. Today the daily throughput-by-unit number lives in the operations historian, the conversion yield numbers live in the Process Engineer's LP-model output, and the gross-margin-per-barrel cut sits in a separate Planning workbook that gets reconciled monthly. Three artifacts on three cadences — so the catalyst-change call, the severity-push decision, and the slate-allocation conversation never happen on the same data. This space ends that. Daily throughput, yield, and margin all answer the same question: *which units run hard this cycle, which get a catalyst change, and which lose the slate fight when crack spreads compress.*

---

## Key KPIs in scope

- Unit utilization (%) — top-quartile refiners run 92%+ mechanical utilization
- Throughput (BPD) by unit and refinery section
- Product yield (%) — FCC gasoline 50%+, hydrocracker distillate 60%+
- Mechanical availability (%) — target >96%
- Energy intensity (BTU/bbl)
- Gross margin and OPEX per barrel
- Unplanned downtime hours by section
- Feed quality (API gravity) impact on conversion yield

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **API** | Application Programming Interface |
| **BPD** | Barrels Per Day |
| **OPEX** | Operating Expense |

---

## Act 1 — The signal — finding the throughput leaks and utilization gaps before the morning ops call ends *(≈4 min)*

**Persona:** Refinery Manager • **Job to be done:** Pull the daily watchlist of units running soft against nameplate — not from the LP rerun, from yesterday's actual throughput.

*This is the moment the daily slate decision starts forming. Two questions in, the Refinery Manager has the unit ranking that used to take a half-hour of Excel against the historian extract.*

### Question (Act 1.1)

> **Top 10 process units by total product output (barrels) over the last 12 months.**

**What to say while it runs:** Total product output by unit is the headline number — but the value is in the spread between the top of the list and the bottom. Top-quartile refiners run 92%+ mechanical utilization. Anything materially under that on a high-margin conversion unit is barrels of margin we left on the table.

**What to look for:** A ranked table of top 10 units by `total_product_bbl` over 12 months. The room should notice the long tail — and that the bottom of the list is where the margin recovery hides.

**Land the point:** Now the Refinery Manager can isolate the units running soft against nameplate in minutes — that's the daily slate conversation that used to wait for the weekly ops review.

### Question (Act 1.2)

> **Show monthly trend of average unit utilization for the trailing 12 months.**

**What to say while it runs:** Unit utilization trend month-over-month is the chart that tells you whether the operating envelope is holding. Top-quartile is 92%+. A unit drifting from 94% to 86% over two quarters is the signal that either feed quality, catalyst, or mechanical availability is slipping — and we want to catch it before it shows up in the gross margin print.

**What to look for:** Monthly line of `avg_utilization_pct` over 12 months — `DATE_TRUNC('month', ...)`. The inflection months are where the next conversation starts.

**Land the point:** Before this space, that chart was rebuilt for the monthly business review. Now it's the Refinery Manager's first question of the day — and the COO sees the same view, same numbers, same time.

---

## Act 2 — The decision — catalyst change, severity push, or harvest-mode operating *(≈4 min)*

**Persona:** Operations Planner • **Job to be done:** Commit the slate plan and the catalyst-change call for the cycle — which units run hard, which run soft, which earn a catalyst order.

*Three questions that turn the daily throughput stream into a defensible slate plan. The middle question is the anchor — unplanned downtime hours converted into recoverable margin.*

### Question (Act 2.1)

> **Which units are running below 70% utilization, and what is the throughput gap to nameplate?**

**What to say while it runs:** Units running below 70% utilization with a measurable throughput gap to nameplate are the candidates for either a catalyst change, a severity push, or a structural review. On a conversion unit, 70% utilization isn't a soft-market signal — it's a constraint somewhere we can fix.

**What to look for:** A table of units below 70% `avg_utilization_pct` with the BPD gap to nameplate. The shape — one unit at 55%, two units at 65% — is what the catalyst-order conversation gets sized against.

**Land the point:** That list used to take a half-day comparing the historian against the LP-model run. Now it's the input to the catalyst-and-severity meeting that happens at 8 AM Monday.

### Question (Act 2.2)

> **Top 10 units by total unplanned downtime hours year-to-date.**

**What to say while it runs:** Top units by unplanned downtime hours YTD is the *which units are bleeding margin* view. The FCC and Hydrocracker are the high-margin units — every unplanned hour on those is $40-200K of margin gone. Below them the tradeoff is different; smaller units cost less per hour but can stack up.

**What to look for:** Top 10 units ranked by `total_downtime_hours` YTD. Watch for whether the top of the list is conversion units (margin-driven conversation) or treating/blending units (slate-flexibility conversation).

**Land the point:** When the Refinery Manager, the Operations Planner, and the COO all see the same downtime-ranked list, the conversation stops being about whose log was right and starts being about *which units earn the next mechanical-availability project*.

> **Anchor moment.** Stop on the downtime-hours ranking. Pick the worst conversion unit — call it the FCC at 200 unplanned downtime hours YTD on a 50 KBD design.

> *200 unplanned hours on a 50 KBD FCC is roughly 415,000 barrels of throughput not converted. At $10/bbl gross margin for FCC products, that's $4M of margin walked out the door this year on one unit. A catalyst change at the right moment is $1-5M of material plus $5-10M/day during the 3-5 day swap window. Even on the worst-case swap economics, recovering 200 bps of yield on the FCC for the next 18 months is roughly $15-25M of margin. Net upside: easily $10M+/year. Stack against the two other conversion units in the top-5 downtime ranking, and the conversation isn't *can we justify a catalyst order this cycle*, it's *which unit gets the slot first*.*

> That's the decision this space automates. Not the slate slide. The catalyst-change call, the severity-push commitment, and the harvest-mode list — all on the same data the COO sees in the executive review.

### Question (Act 2.3)

> **How has average yield trended month-over-month for conversion units (FCC, Hydrocracker, Reformer)?**

**What to say while it runs:** Conversion-unit yield trend month-over-month is the catalyst-life conversation. FCC gasoline yield 50%+, hydrocracker distillate 60%+ — those are the design targets. A 200 bps decline over three months on the FCC is the textbook catalyst-aging signal, and the catalyst-change call gets made on this chart.

**What to look for:** Monthly `avg_yield_pct` for FCC, Hydrocracker, and Reformer. The decline rate matters more than the snapshot — a slow drift is normal, a step change is a process upset that needs investigation.

**Land the point:** That trend is the difference between a calendar-driven catalyst change and a margin-driven one. The first is a maintenance schedule; the second is a $5-10M decision the Operations Planner gets to defend with data.

---

## Act 3 — The commitment — locking the slate, the catalyst plan, and the next-cycle margin defense *(≈4 min)*

**Persona:** COO • **Job to be done:** Defend the production plan to the executive committee and rank the units that earn the next mechanical-availability and yield-improvement capex.

*The COO doesn't need a new pack; they need the same numbers the Refinery Manager and the Operations Planner are acting on, in the same language, so the executive margin-defense narrative writes itself.*

### Question (Act 3.1)

> **Which refinery sections have the highest energy intensity per barrel?**

**What to say while it runs:** Energy intensity per barrel by refinery section is the *which unit is structurally bleeding margin* view. Energy is typically 50-60% of refinery OPEX — and a 10% energy-intensity gap on a major section is a million-dollar conversation, not a tuning conversation.

**What to look for:** Refinery sections ranked by `avg_energy_intensity`. Match against the gross-margin-per-barrel ranking from the next question — sections that are high-energy AND low-margin are harvest-mode candidates, not investment candidates.

**Land the point:** When that ranking is in the COO's hand a quarter before the capex review, the structural-vs-tuning conversation moves from a debate to a slot in the AFE list.

### Question (Act 3.2)

> **What is the gross margin per barrel by unit, and which units are below the $8/bbl threshold?**

**What to say while it runs:** Gross margin per barrel by unit is the harvest-vs-invest decision in one chart. The $8/bbl threshold is the bright line — any unit below $8/bbl is a structural conversation, not an ops conversation. Above $15/bbl is where the next severity push lives.

**What to look for:** Units on `avg_margin_per_bbl`. Look for the units below $8/bbl — and ask whether they're below because of feed slate (recoverable), energy intensity (capex), or yield (catalyst).

**Land the point:** Daily slate at 8 AM, capital allocation at 10 — same space, same numbers. The Refinery Manager's watchlist, the Operations Planner's catalyst plan, and the COO's executive-review pack are now the *same artifact* — and the executive team gets one production story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RefineOps Central — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 process units by total product output (barrels) over the last 12 months.
2. Show monthly trend of average unit utilization for the trailing 12 months.
3. Which units are running below 70% utilization, and what is the throughput gap to nameplate?
4. Top 10 units by total unplanned downtime hours year-to-date.
5. How has average yield trended month-over-month for conversion units (FCC, Hydrocracker, Reformer)?
6. Which refinery sections have the highest energy intensity per barrel?
7. What is the gross margin per barrel by unit, and which units are below the $8/bbl threshold?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
