# BuildBid Engineering — Demo Script

**Space:** Construction & Engineering — BuildBid Engineering - Bid Creation & Cost Estimation 📝
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Construction + CFO, Estimating Lead, Cost Engineer
**KPIs touched:** Bid win rate, Estimate accuracy, Bid markup / target margin, Average competitors per bid, Pipeline coverage, Cost mix
**Big decision automated:** Go/no-go on the next $50M-200M EPC pursuit list and the exact target margin to bid each one at, so we stop losing winnable work to under-priced competitors and stop winning losers at 6% margin.

---

## Pre-demo checklist

- Open the Genie space `BuildBid Engineering - Bid Creation & Cost Estimation 📝`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> BuildBid Engineering pursues 20 active EPC bids per year across bridges, highways, tunnels, water, commercial, industrial, and energy work — individual project values run $5M to $200M. Today the cost build-up sits in the Cost Engineer's HCSS HeavyBid file, the win/loss log sits in the Estimating Lead's Excel pursuit tracker, and the pipeline coverage and estimate-accuracy slides get rebuilt every month for the CFO's deck. Three artifacts, three owners, and a target-margin number that gets set in the bid-room hallway 15 minutes before submission. That's how a $120M highway pursuit gets bid at 7% when the market was clearing 11%, and how a $40M parking deck gets won at a margin so thin it eats its own contingency. This space replaces the hallway conversation with one governed surface — estimate accuracy, win rate, average competitors, and target margin in the same view as the pipeline coverage the CFO defends to the board.

---

## Key KPIs in scope

- Bid win rate (%) — industry benchmark 20-35% on hard-bid public work, 40-60% on negotiated
- Estimate accuracy (%) — target >90% vs. as-built (AACE Class 2 estimates)
- Bid markup / target margin (%) — typical 8-15% on competitive lump-sum work
- Average competitors per bid — directional pricing pressure indicator
- Pipeline coverage ($) — target 3-4x trailing annual revenue
- Cost mix (labor/material/equipment/subcontractor) — used for risk-loaded contingency
- Contingency (%) — typical 3-10% depending on design maturity
- Total bid value submitted ($) — top-of-funnel volume

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **EPC** | Engineering, Procurement, Construction |
| **VP** | Vice President |

---

## Act 1 — The signal — reading the pursuit funnel before the next bid-room call *(≈4 min)*

**Persona:** Estimating Lead • **Job to be done:** Decide which lanes are still winnable at acceptable margin and which have commoditized — before committing estimating hours to the next pursuit.

*This is the conversation that should happen before a Cost Engineer starts pricing labor. Two questions tell the Estimating Lead whether the pursuit deserves a full-cost build-up or a polite no-bid letter.*

### Question (Act 1.1)

> **Show monthly bid win count and total bid value trended over the trailing 12 months.**

**What to say while it runs:** Total bid value submitted and bids won by month — that's the top-of-funnel volume that drives pipeline coverage. CFO wants 3-4x trailing revenue in the funnel; below that and we starve next year. Notice whether the won-count line is keeping pace with the submitted line or whether we're just churning estimating hours.

**What to look for:** Twelve months of bars: total_bid_amount on one axis, won_count on the other. The room should notice the gap — submission volume looks healthy, but won_count tells the real story.

**Land the point:** Now the Estimating Lead can defend the pursuit plan on numbers, not vibes — that's the go/no-go conversation that used to require pulling three spreadsheets and a steering-committee invite.

### Question (Act 1.2)

> **Top 10 project types by win rate this year — and how does that compare to average target margin?**

**What to say while it runs:** Win rate by project type with avg_target_margin alongside. Hard-bid public work clears 20-35%, negotiated work 40-60%. Anything below 20% and we're paying to lose. The interesting tell is where high win-rate lanes also have collapsing target margins — that's a commoditized lane we should exit, not double-down on.

**What to look for:** Ranked table of project types: bid_count, won_count, win_rate%, avg_target_margin%. Watch for the inverse — high win-rate, low margin = race to the bottom.

**Land the point:** That table replaces the gut-feel pursuit-strategy meeting. Now the Estimating Lead walks into Monday's go/no-go with a defensible list of *which lanes earn the next 200 estimating hours* — not which ones the BD team is loudest about.

---

## Act 2 — The decision — pricing the next big pursuit at a margin that wins and protects *(≈4 min)*

**Persona:** Cost Engineer • **Job to be done:** Set target margin and contingency on a specific $80M pursuit — high enough to protect the as-built outcome, low enough to actually win against 5+ competitors.

*The Estimating Lead has cleared the lane; now the Cost Engineer is pricing the bid. Three questions convert the estimate-accuracy history and the competitive-intensity signal into a defensible markup number.*

### Question (Act 2.1)

> **Which regions have the lowest estimate accuracy over the last 6 months, and what's the total pipeline value at risk?**

**What to say while it runs:** Estimate accuracy by region over the last 6 months, with total pipeline value at risk. AACE Class 2 target is >90% accurate vs. as-built; under 85% means our build-ups are systematically wrong and the contingency line is the only thing protecting margin. Regions below 85% need a hard look at unit-rate assumptions before we submit.

**What to look for:** Regions ranked low-to-high on avg_estimate_accuracy, total_pipeline alongside. The room should notice which regions are bidding aggressively with the worst accuracy track record — that's where overruns turn into earnings calls.

**Land the point:** Right there is the conversation about which regional estimating teams need a unit-rate refresh before the next submission — not after another $5M overrun finds it for us.

### Question (Act 2.2)

> **How has average competitors per bid trended monthly across the network?**

**What to say while it runs:** Average competitors per bid month-over-month — directional pricing pressure. Five or more competitors and the lane is commoditized; the market will price you off the page if you bid for margin. Three or fewer and the room has room to hold the line on 10-12%.

**What to look for:** Trend line of avg_competitors by month. The room should notice that competitive intensity has been climbing on highway and parking work — that's where we need to drop markup or no-bid.

**Land the point:** Now the markup decision has a number behind it. The Cost Engineer can defend a 9% target margin on a 6-bidder pursuit without the VP overriding it in the hallway.

> **Anchor moment.** Pause on the competitive-intensity trend and the project leaderboard. Pick the next pursuit on the funnel — call it a $120M highway interchange, market clearing at 5 competitors, our historical accuracy in that region at 84%.

> *At 5 competitors, the win-probability gradient is roughly 100 basis points of markup per percentage point of win rate. A 1% markup point on $120M TCV is $1.2M of margin per bid. Drop markup from 10% to 9% on three pursuits like this and we move from winning 1 of 3 at $1.2M margin ($1.2M) to winning 2 of 3 at $10.8M ($21.6M). On the *other* side: a lost bid at this scale is $5-20M of revenue and the 3,000 estimating hours that went into pricing it. Across 20 bids a year at this scale, the gap between *priced by gut* and *priced by funnel data* is $10-15M of annual contribution margin.*

> That's the decision this space automates. Target margin gets set with the funnel data on the same screen as the build-up — not in a hallway 15 minutes before submission. The next big pursuit gets priced once, defended once, and the as-built tells us whether the rule needs to tighten.

### Question (Act 2.3)

> **Top 10 projects by total bid value submitted this year, with bid result and target margin.**

**What to say while it runs:** Top 10 projects by total bid value submitted this year with bid_result and target_margin alongside. This is the leaderboard — we'll see whether the biggest swings landed at acceptable margin or got won at 6% and lost at 14%.

**What to look for:** Ranked list: project_name, project_type, bid_amount_usd, bid_result, target_margin_pct. The room should notice the won-at-low-margin projects (winner's curse) and the lost-at-high-margin projects (left money on the table).

**Land the point:** That comparison is the difference between knowing we won and knowing we won *profitably*. The first is a press release; the second is the pursuit-pricing rule we apply to the next $80M bid going out Friday.

---

## Act 3 — The commitment — pipeline coverage and pursuit policy for the next fiscal year *(≈4 min)*

**Persona:** VP Construction • **Job to be done:** Defend the pursuit-mix and target-margin policy to the CFO and the board — lock in which lanes get estimating capacity next year and which get a 'negotiated work only' policy.

*The VP doesn't need another dashboard. They need the same numbers the Estimating Lead and the Cost Engineer are acting on, in board-deck form, so the pursuit strategy writes itself.*

### Question (Act 3.1)

> **What is the monthly trend in total pipeline value by project type for the trailing 12 months?**

**What to say while it runs:** Monthly trend in total_pipeline by project type over 12 months. Coverage target is 3-4x trailing revenue. The mix tells us whether the pursuit pipeline is concentrated in the lanes where we *actually win profitably* — or whether it's still over-indexed to commoditized public work because that's what BD is comfortable pursuing.

**What to look for:** Stacked monthly trend, total_pipeline by project_type. Watch the share of Bridge / Highway / Tunnel / Energy over time. If the high-margin lanes are flat and the commoditized lanes are growing, the pursuit policy is mis-allocating estimating capacity.

**Land the point:** When that chart is on the VP's screen for the board meeting, the pursuit-mix conversation becomes programmatic — next year's estimating hours get allocated by win-rate-×-margin, not by who BD called first.

### Question (Act 3.2)

> **Which project types have the highest average contingency percentage, and how does that correlate with win rate?**

**What to say while it runs:** Project types with the highest avg contingency_pct and how that correlates with win rate. Contingency is the risk-load — typical range is 3-10% based on design maturity. Where we routinely carry 9-10% contingency and still lose bids, design isn't mature enough at submission and we're padding to compensate — that's an estimating-process change, not a pricing one.

**What to look for:** Project types ranked by avg contingency_pct with win_rate% alongside. The Tunnel and Energy categories typically run high contingency; if they win less often, the buyer is rejecting the risk-load.

**Land the point:** Triage at noon, pipeline strategy at 2 PM, board pitch at 5. Same space. Same numbers. The Estimating Lead, the Cost Engineer, the VP Construction, and the CFO are now defending the same pursuit policy — and the question stops being 'whose number is right' and becomes 'which lanes do we actually want to be in next year'.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — BuildBid Engineering — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly bid win count and total bid value trended over the trailing 12 months.
2. Top 10 project types by win rate this year — and how does that compare to average target margin?
3. Which regions have the lowest estimate accuracy over the last 6 months, and what's the total pipeline value at risk?
4. How has average competitors per bid trended monthly across the network?
5. Top 10 projects by total bid value submitted this year, with bid result and target margin.
6. What is the monthly trend in total pipeline value by project type for the trailing 12 months?
7. Which project types have the highest average contingency percentage, and how does that correlate with win rate?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
