# LabAuto Sciences — Demo Script

**Space:** Chemicals & Materials — LabAuto Sciences - Autonomous Lab Experiments & Optimization 🧪
**Runtime:** ~15 minutes • 7 questions
**Audience:** R&D VP + Bench Scientist, R&D VP, CFO partner
**KPIs touched:** Average product yield, Experiment pass rate, Average product purity, Cost per experiment, Model prediction accuracy, Yield headroom
**Big decision automated:** Which 2-3 formulations get the next 6 months of pilot-line time, which 4-5 get archived, and which 8-10 stay in the autonomous queue for another optimization pass.

---

## Pre-demo checklist

- Open the Genie space `LabAuto Sciences - Autonomous Lab Experiments & Optimization 🧪`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> LabAuto Sciences runs 20 active formulation programs — catalysts, coatings, polymers, pharmaceuticals, nanomaterials — across four labs in Boston, San Diego, Basel, and Shanghai. Today the program ROI lives in the CFO's quarterly deck, the formulation rankings live in the R&D VP's portfolio review slides, and the parameter-confidence numbers live on each bench scientist's local notebook. Three artifacts, same experiments — and the pilot-line allocation for next quarter (a $500K-1M commitment per program) gets decided by whichever PI built the most persuasive slide. This space ends that. One governed surface where yield headroom, model confidence, and cost per experiment land in the same conversation as the pilot-line calendar.

---

## Key KPIs in scope

- Average product yield (%) — primary R&D outcome; best-in-class catalysts run 70-90%
- Experiment pass rate (%) — share of runs hitting spec; target 75-85%
- Average product purity (%) — release-gate indicator; typical 95-99% for specialty chemicals
- Cost per experiment ($) — efficiency benchmark; autonomous platforms run $200-$5,000/run
- Model prediction accuracy (%) — closeness of predicted to actual yield; target ≥ 85%
- Yield headroom (best_yield - avg_yield) — optimization potential per formulation
- Total experiments run — throughput; healthy autonomous lab targets 20-50 runs/week
- Model confidence score — gates which recommendations get auto-executed (≥ 0.85 typical)

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **KPI** | Key Performance Indicator |
| **ROI** | Return on Investment |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the formulations that are still optimizing vs. the ones that have plateaued *(≈4 min)*

**Persona:** Bench Scientist • **Job to be done:** Separate the formulations where the autonomous loop is still finding yield from the ones where it's burning runs on a flat surface.

*This is where the next 6 months of pilot-line allocation starts. Two questions in, the scientist knows which programs are converging and which are stuck — before the portfolio review ever opens.*

### Question (Act 1.1)

> **Show monthly average yield by formulation category for the trailing 12 months.**

**What to say while it runs:** Average yield by formulation category over the last 12 months — this is the trend that tells the R&D VP whether the autonomous loop is actually finding chemistry, or just burning $200-$5,000 per run looking. Best-in-class catalysts run 70-90%, polymers 60-85%. Anything sliding below those bands is a re-prioritization candidate.

**What to look for:** Monthly avg_yield_pct trend by formulation_category — catalysts, coatings, polymers, pharmaceuticals, nanomaterials. Watch for categories where the line has flattened — those are the programs where the autonomous platform isn't getting any more juice out of the design space.

**Land the point:** Right there is the first portfolio cut. The flat categories are the ones where pilot-line time stops being justified by additional bench iterations. That's a conversation the bench scientist used to need three weeks of slide prep for — it just happened in 8 seconds.

### Question (Act 1.2)

> **Top 10 formulations by best yield achieved this year — what is the gap to average yield?**

**What to say while it runs:** Now the yield gap — best yield minus average yield per formulation. This is the headroom metric. A small gap means we're near the ceiling; a big gap means the autonomous loop hasn't found the optimum yet and there's real money in more iterations.

**What to look for:** Top 10 formulations ranked by best_yield_pct with the gap to avg_yield_pct alongside. The ones with both high best yield AND big gap are the obvious pilot candidates; the ones with high best yield and tiny gap are the ones to scale now before the surface drifts.

**Land the point:** That table is the shortlist for the pilot-line conversation — which formulations to scale immediately, which need another optimization pass, and which are donor candidates for the archived list. The yield-headroom column is the column that used to require a half-day of spreadsheet stitching.

---

## Act 2 — The decision — which formulations earn pilot-line time and which get archived *(≈4 min)*

**Persona:** R&D VP • **Job to be done:** Commit the next quarter's pilot-line calendar — 2-3 formulations move to scale, 4-5 get archived, and the rest stay in the autonomous queue.

*Three questions that convert the watchlist into a defensible portfolio decision. The middle question is the anchor — the cost-per-experiment math that turns the archive list into a dollar-denominated recommendation, not a gut call.*

### Question (Act 2.1)

> **How has experiment pass rate trended month-over-month across lab facilities?**

**What to say while it runs:** Pass rate by lab facility, month over month. Industry target is 75-85% for mature workflows. A lab that's drifting below 70% isn't an autonomous-platform problem — it's a chemistry problem, and that chemistry doesn't deserve pilot-line time until it's resolved.

**What to look for:** Monthly trend of pass rate across Boston, San Diego, Basel, Shanghai. The lab-level rollup is what tells the R&D VP whether failure is structural in the formulation or local to a particular reactor.

**Land the point:** When pass rate is the same number in every lab and on every scientist's screen, the pilot-line debate stops being about whose runs are most recent and starts being about whose formulation is most ready. That's a different meeting.

### Question (Act 2.2)

> **Which formulations have a model confidence score above 0.85 with predicted yield > 80%?**

**What to say while it runs:** Total cost per experiment by category over the last 6 months — autonomous platforms benchmark at $200-$5,000 per run. The categories at the top of this list are the ones consuming the program budget; if their yield trajectory doesn't justify the spend, they're the ones that get cut first.

**What to look for:** Bar chart of avg_cost_per_experiment by formulation_category, sized by total_experiments_run. The biggest bars with the flattest yield trends are the obvious archive candidates.

**Land the point:** That's the slide the CFO needs to defend continued R&D investment. Cost per experiment, by category, against yield trajectory. The archive decision moves from R&D's recommendation to a finance-defensible portfolio call.

> **Anchor moment.** Hold on the cost-per-experiment chart. Pick the bottom-performing category — call it 30 runs/month at $3,500 average cost, model accuracy at 65%, yield trajectory flat for two quarters.

> *Thirty runs a month at $3,500 each is $105K/month — $1.26M a year — burning on a category whose model isn't calibrated and whose yield isn't moving. Across two stagnant categories that's $2.5M of annual R&D spend that could fund pilot-line scale-up on the formulations that ARE converging. One pilot-line month runs $500K-1M, so that's two-to-five extra pilot-line slots paid for by what we stop spending on flat surfaces.*

> That's the decision this space automates. Not the deck — the decision. The archive list moves from a quarterly debate to a monthly governance call, and the freed budget gets reallocated to the formulations the autonomous loop is still actively winning on.

### Question (Act 2.3)

> **What is the total cost per experiment by formulation category over the last 6 months?**

**What to say while it runs:** Top 10 categories by total experiments, with model prediction accuracy alongside. Model accuracy above 85% means the recommender is trustworthy enough to auto-execute; below 70% means we're paying for noise. This is the column that decides whether we *add* compute to a program or pull back.

**What to look for:** Ranked list of categories by experiments run with avg_model_accuracy_pct side-by-side. The high-volume + low-accuracy quadrant is where money is leaking; high-volume + high-accuracy is where to lean in.

**Land the point:** Pilot-line allocation, autonomous-budget allocation, and archive decisions — all three rest on this two-column view. That's the conversation the portfolio review is supposed to have and usually doesn't.

---

## Act 3 — The commitment — locking the pilot-line calendar and the next-cycle R&D investment plan *(≈4 min)*

**Persona:** CFO partner • **Job to be done:** Defend the R&D portfolio's program ROI to the executive committee and shape next year's autonomous-platform investment envelope.

*The CFO doesn't need more chemistry; they need the same numbers the R&D VP is acting on, in the same language, so the budget conversation writes itself.*

### Question (Act 3.1)

> **Top 10 formulation categories by total experiments run — and how does model prediction accuracy compare?**

**What to say while it runs:** Top 10 formulation categories by total experiments run with model prediction accuracy alongside. This is the productivity-vs-quality view — the categories the autonomous platform is most active on, and whether that activity is actually informed.

**What to look for:** Same shape as Act 2 close, but framed for the executive committee. The high-volume, high-accuracy quadrant is where the platform has earned more compute; the high-volume, low-accuracy quadrant is where the next investment dollar is the wrong investment.

**Land the point:** This is the chart that defends both the platform's existence and its expansion. Program ROI in one frame — and the budget conversation moves from 'how much do we spend on autonomous labs?' to 'where do we spend the next dollar?'.

### Question (Act 3.2)

> **Which lab facilities have the lowest pass rate, and what is the cost-of-failure exposure?**

**What to say while it runs:** Lab facilities ranked by pass rate with cost-of-failure exposure alongside — failed runs multiplied by cost per experiment. This is the operational-health view that finance cares about: which labs are converting capex into chemistry, and which are converting it into rework.

**What to look for:** Four-row table of Boston, San Diego, Basel, Shanghai with pass rate and failure-cost columns. The bottom row is the lab whose 2027 capex line item just got harder to defend.

**Land the point:** Bench triage at 8 AM, portfolio decisions at 10, capex calls at noon. Same space. Same numbers. The R&D VP's pilot-line shortlist and the CFO's investment defense are now the *same artifact* — and the executive committee gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — LabAuto Sciences — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly average yield by formulation category for the trailing 12 months.
2. Top 10 formulations by best yield achieved this year — what is the gap to average yield?
3. How has experiment pass rate trended month-over-month across lab facilities?
4. Which formulations have a model confidence score above 0.85 with predicted yield > 80%?
5. What is the total cost per experiment by formulation category over the last 6 months?
6. Top 10 formulation categories by total experiments run — and how does model prediction accuracy compare?
7. Which lab facilities have the lowest pass rate, and what is the cost-of-failure exposure?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
