# QualityRefine Analytics — Demo Script

**Space:** Oil & Gas Refining — QualityRefine Analytics - Quality Event Root Cause Analysis 🔍
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP of Quality + Process Engineer, Refinery Manager, VP of Quality
**KPIs touched:** First-pass yield, Off-spec rate of total production, Off-spec volume and financial impact, Sulfur compliance, Octane on-spec for premium / regular gasoline grades, Mean time to resolution by severity
**Big decision automated:** Which off-spec batches get quarantined and reprocessed vs. blended off this week, which root causes earn a structural process fix in the next AFE, and whether the ULSD sulfur-management program holds the 10 ppm spec or needs a hydrotreater severity push.

---

## Pre-demo checklist

- Open the Genie space `QualityRefine Analytics - Quality Event Root Cause Analysis 🔍`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> QualityRefine Analytics runs quality event and batch analytics across 20 process units spanning Crude Distillation, FCC, Hydrotreating, Reforming, Alkylation, and Blending. Today the off-spec barrel count lives in the Process Engineer's deviation log, the financial-impact rollup gets reconstructed in the Quality VP's monthly scorecard, and the sulfur-PPM-by-batch detail sits in the lab-LIMS export nobody reconciles to either. Three artifacts, three update cadences — so the off-spec quarantine call, the root-cause Pareto, and the ULSD compliance defense never happen on the same data. The result is product giveaway barrels that should have been reprocessed and structural process problems that get rediscovered every quarter. This space ends that. Deviations, batches, and KPIs all answer the same question: *which off-spec gets reprocessed, which root causes earn capital protection, and which units are at risk of breaching the 10 ppm sulfur spec next quarter.*

---

## Key KPIs in scope

- First-pass yield (%) — industry target >95% for refined products
- Off-spec rate (%) of total production
- Off-spec volume (bbl) and financial impact ($)
- Sulfur compliance (ULSD ≤10 ppm, jet ≤3000 ppm)
- Octane on-spec for premium / regular gasoline grades
- Mean time to resolution (hours) by severity
- Critical event count and root-cause Pareto
- Quality cost ($) per barrel produced

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **PPM** | Parts Per Million (defect rate) |

---

## Act 1 — The signal — surfacing the off-spec barrels and unit-level deviation patterns before the giveaway hits the P&L *(≈4 min)*

**Persona:** Process Engineer • **Job to be done:** Pull the week's quarantine-vs-blend-off list from deviation events and batch records — not from the lab-LIMS extract three days late.

*This is the moment the off-spec disposition decision starts forming. Two questions in, the Process Engineer already has the ranked unit list that used to take a full day of LIMS reports stitched against the deviation log.*

### Question (Act 1.1)

> **Top 10 process units by total off-spec volume (barrels) over the last 12 months.**

**What to say while it runs:** Off-spec volume by unit is the headline cost number. Industry first-pass yield is >95% — every percentage point below that on a 200 KBD refinery is 2,000 BPD of barrels we made twice or gave away in product blends.

**What to look for:** Top 10 units ranked by `total_off_spec_bbl` over 12 months. The room should notice the long tail — and that two or three units typically drive 60% of the off-spec.

**Land the point:** Now the Process Engineer can isolate the 3-5 units driving the off-spec giveaway in minutes — that's the quarantine-vs-reprocess conversation that used to wait for the weekly quality review.

### Question (Act 1.2)

> **Show monthly trend of total financial impact from quality events for the trailing 12 months.**

**What to say while it runs:** Financial impact from quality events month-over-month is the chart the Quality VP defends to the executive team. Industry off-spec disposition costs run $20-60/bbl of giveaway depending on whether you reprocess or downgrade — so a $2M month is roughly 40-100 KBBL of off-spec product moving through the wrong disposition path.

**What to look for:** Monthly bars of `total_financial_impact_usd` over 12 months. The spike months are the ones where a root cause broke containment and started compounding.

**Land the point:** Before this space, that chart was rebuilt for the monthly quality scorecard. Now it's the Process Engineer's first question of the day — and the Quality VP gets the same view, in real time, before the close period locks.

---

## Act 2 — The decision — root-cause-Pareto-driven AFE list and the ULSD compliance defense *(≈4 min)*

**Persona:** Refinery Manager • **Job to be done:** Lock the root-cause intervention list for the next two quarters and decide which off-spec product grades earn an immediate hydrotreater severity push vs. an accepted-and-blended disposition.

*Three questions that turn the deviation log into a defensible quality-program AFE. The middle question is the anchor — failed-batch rate translated into reprocessing dollars.*

### Question (Act 2.1)

> **Which root causes drove the most Major or Critical quality events this year?**

**What to say while it runs:** Major and Critical root causes by event count is the Pareto every Process Engineer wants but few have time to build. The top three root causes usually drive 70%+ of the financial impact — and the question is whether they're operational (procedure fix) or structural (capex fix).

**What to look for:** Root causes ranked by Major+Critical event count. Watch for the cluster pattern — three root causes on the same unit means a structural process issue, three on different units means a procedural one.

**Land the point:** That Pareto used to take a half-day in Excel from the deviation log. Now it's the input to the quality steering meeting that happens at 8 AM Monday.

### Question (Act 2.2)

> **What is the batch fail rate by product grade, ranked worst to best?**

**What to say while it runs:** Batch fail rate by product grade is the *where do we run reprocessing economics* question. A 5% fail rate on premium gasoline is a $/octane question. A 5% fail rate on ULSD is a $/sulfur question. The disposition economics are different — and the slate plan has to know.

**What to look for:** Product grades on `total_batches` fail rate, ranked worst to best. Premium and ULSD usually sit at the top; the middle of the list is where the surprises live.

**Land the point:** When the Process Engineer, the Refinery Manager, and the Quality VP all see the same fail-rate-by-grade ranking, the conversation stops being about whose batch summary is most current and starts being about *which product grade earns a hydrotreater severity push*.

> **Anchor moment.** Stop on the fail-rate-by-grade ranking. Pick the worst — call it premium gasoline at a 4% batch fail rate.

> *On a 200 KBD refinery with roughly 30 KBD of premium output, a 4% batch fail rate is about 1,200 BPD of off-spec premium — 440 KBBL/year. Industry off-spec disposition cost runs $20-60/bbl depending on whether the batch gets reprocessed or downgraded to regular. Call it $40/bbl. That's $17M/year of giveaway and reprocessing on one grade. Drive the fail rate from 4% to the industry-target 1% and you recover three points of yield — roughly $13M/year of preserved margin. A typical root-cause-driven process fix is $0.5-3M of work. Payback under three months. Stack the ULSD compliance defense on top and the conversation isn't *can we justify a quality program*, it's *which root cause gets the next AFE slot*.*

> That's the decision this space automates. Not the quality scorecard. The off-spec quarantine list, the root-cause AFE ranking, and the ULSD compliance defense — all on the same data the Quality VP defends to the executive committee.

### Question (Act 2.3)

> **Top 10 units by average sulfur PPM — which are at risk of breaching the 10 ppm ULSD spec?**

**What to say while it runs:** Average sulfur PPM by unit is the ULSD compliance leading indicator. The 10 ppm spec is bright-line — anything trending in the 7-9 ppm range on a Hydrotreater is at risk of breaching the spec on a feed-quality swing. That's a regulatory conversation, not a quality one.

**What to look for:** Top 10 units by `avg_sulfur_ppm`, with the 10 ppm bright line drawn. Watch for the units in the 7-9 ppm yellow zone — those are the candidates for severity push or feed re-route.

**Land the point:** That ranking is the difference between getting ahead of a ULSD breach with a severity-push decision and finding out about it from the next quarter's regulatory filing.

---

## Act 3 — The commitment — locking the first-pass-yield narrative and the next-cycle quality capex *(≈4 min)*

**Persona:** VP of Quality • **Job to be done:** Defend the quality program's first-pass yield trend to the executive team and lock the next $5-10M of quality-program capex.

*The Quality VP doesn't need another scorecard; they need the same numbers the Process Engineer and the Refinery Manager are already acting on, in the same language, so the executive quality narrative writes itself.*

### Question (Act 3.1)

> **How has first-pass yield trended month-over-month by product grade?**

**What to say while it runs:** First-pass yield by product grade month-over-month is the executive-committee headline. Industry benchmark is >95%. A grade trending down quarter-over-quarter is the early warning that either feed quality, catalyst, or operating envelope has slipped — and the executive team wants to see the curve bend, not hear about anecdotes.

**What to look for:** Monthly trend of `avg_yield_pct` by product grade. The inflection point tells you the quarter the root cause broke containment.

**Land the point:** When that curve is in the VP of Quality's hand the day before the executive review, the quality conversation moves from defensive to programmatic — and the executive team stops finding out about quality issues from the regulator.

### Question (Act 3.2)

> **Which units have the longest average resolution time for Critical events?**

**What to say while it runs:** Average resolution hours for Critical events is the *is the quality response system working* number. Industry-leading is under 24 hours on Critical. Anything above 72 hours is a structural process problem — not enough engineers, not the right escalation path, or not the right authority at the unit level.

**What to look for:** Units ranked by `avg_resolution_hours` on Critical-severity events. The shape determines whether the next investment is in tooling, headcount, or escalation policy.

**Land the point:** Off-spec triage at 8 AM, quality capex at 10 — same space, same numbers. The Process Engineer's quarantine list, the Refinery Manager's AFE rankings, and the VP of Quality's executive defense are now the *same artifact* — and the executive team gets one quality story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — QualityRefine Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 process units by total off-spec volume (barrels) over the last 12 months.
2. Show monthly trend of total financial impact from quality events for the trailing 12 months.
3. Which root causes drove the most Major or Critical quality events this year?
4. What is the batch fail rate by product grade, ranked worst to best?
5. Top 10 units by average sulfur PPM — which are at risk of breaching the 10 ppm ULSD spec?
6. How has first-pass yield trended month-over-month by product grade?
7. Which units have the longest average resolution time for Critical events?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
