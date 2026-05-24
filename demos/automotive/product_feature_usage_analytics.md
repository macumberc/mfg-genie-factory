# AutoMetrics Corp — Demo Script

**Space:** Automotive — AutoMetrics - Feature Usage & Adoption Analytics 📱
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director, Connected Services + Connected Services GM, ADAS/Infotainment Product Manager, Subscription P&L owner
**KPIs touched:** Feature events volume, Failed activation count, Average session duration, Engagement score, Power-user count, High churn-risk count
**Big decision automated:** Which connected-services features earn next year's software-investment dollar, which get deprecated, and which pricing tier to push at-risk owners into before renewal.

---

## Pre-demo checklist

- Open the Genie space `AutoMetrics - Feature Usage & Adoption Analytics 📱`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> Apex Motor Group's AutoMetrics connected-services business covers a portfolio of 20 vehicle SKUs spanning 11 nameplates (Nexus Sedan, Trailblazer SUV, Hauler Truck, Volt EV, Metro Compact, Voyager Wagon, Sprint Coupe, Cargo Van, Ridgeline Pickup, and their hybrid variants) across Basic / Premium / Elite subscription tiers. Today the failed-activation count sits in the Product Manager's Jira-export Excel, the engagement score and churn-risk flag live in the Connected Services GM's Mode dashboard, and the renewal-likelihood number is a CSV the Subscription P&L owner gets emailed every Tuesday. Three spreadsheets, same vehicles — and the *which features to deprecate, which to invest in, which owners to win back before renewal* call gets made on whichever number landed in inbox first. Industry data says ADAS subscriptions are running 15–25% annual churn and pay-per-use is now ~16% of subscription value, so engagement intensity is the only leading indicator that actually matters. This space replaces those three workbooks with one governed surface where features, engagement, and renewal likelihood live next to each other — and the product-investment and pricing-tier decisions happen in the same conversation.

---

## Key KPIs in scope

- Feature events volume — total in-vehicle feature activations per period
- Failed activation count — events that did not complete (UX or eligibility issues)
- Average session duration (sec) — engagement depth signal
- Engagement score — composite per-vehicle 0–100 rollup
- Power-user count — vehicles in the top engagement tier
- High churn-risk count — vehicles flagged for likely non-renewal
- Renewal likelihood (%) — forward-looking subscription forecast
- Adoption forecast error (%) — actual vs forecasted feature adoption

---

## Act 1 — The signal — which features earn the next investment dollar vs. which are quietly broken *(≈4 min)*

**Persona:** ADAS/Infotainment Product Manager • **Job to be done:** Decide which features in the in-vehicle portfolio to invest in for next OTA, which to deprecate, and which are quietly failing customers without anyone noticing.

*Every feature in the in-vehicle portfolio costs engineering, certification, and OTA-bandwidth dollars to keep alive. The Product Manager has to walk into the roadmap review with a defensible kill/invest list — not a gut call.*

### Question (Act 1.1)

> **Show the monthly trend in total feature events by feature category for the trailing 12 months.**

**What to say while it runs:** Monthly trend in `total_feature_events` by `feature_category` — ADAS, Infotainment, Convenience, Safety. The category curves are the leading indicator on which buckets the customer is leaning into and which they're walking away from.

**What to look for:** Four stacked or paired lines from `feature_events_metrics`, trailing 12 months by `DATE_TRUNC('month', event_date)`. Watch where ADAS goes flat or declines while Infotainment climbs — that's the next-OTA prioritization staring back at you.

**Land the point:** Now the Product Manager can walk into the roadmap meeting with *here's where the customer is actually spending their attention* — instead of letting the loudest engineering manager win the OTA-slot debate.

### Question (Act 1.2)

> **Top 10 features by failed activation count — where is the in-vehicle UX breaking down?**

**What to say while it runs:** Top 10 features by `failed_activation_count` — where is the in-vehicle UX breaking down? An activation failure is the worst signal in this space: the customer wanted the feature, paid for it, and the car said no. Repeat that 3 times and they unsubscribe.

**What to look for:** Ranked list — feature_name × `failed_activation_count`. Watch for ADAS features (Adaptive Cruise Control, Lane Keep Assist) at the top — those are the ones with the highest churn-leverage if they're failing.

**Land the point:** Right there is the bug-fix backlog — and the deprecation candidate list. The Product Manager doesn't need a customer-research study; the data already named the features that need an engineering sprint vs. an obituary.

---

## Act 2 — The decision — who to win back, who to upsell, who to let go *(≈4 min)*

**Persona:** Connected Services GM • **Job to be done:** Commit to the renewal-cycle play — which segments of the install base get a win-back outreach, which get a tier-upgrade pitch, and which get policy pricing.

*Three questions that turn the engagement scoreboard into a subscription-cycle action plan. The middle question is the anchor — the churn-dollars-at-stake number that decides the win-back budget.*

### Question (Act 2.1)

> **How many vehicles are flagged high churn-risk by feature tier, and what is their average engagement score?**

**What to say while it runs:** How many vehicles are flagged `high_churn_risk` by `feature_tier`, and what's their average `engagement_score`? If Premium tier is showing a stack of high-risk vehicles with engagement under 40, that's a pricing-vs-product diagnostic — they're not getting enough value to justify Premium.

**What to look for:** A table — feature_tier × `high_churn_risk_count` × `avg_engagement_score` from `user_engagement_metrics`. The Premium row is what the GM watches; it's where the dollars live.

**Land the point:** That table is the win-back targeting list. Premium customers with low engagement get a feature-tour outreach; Elite customers with low engagement get a personal call. The GM walks into the renewal-cycle planning meeting with the segmented playbook, not a generic *email everyone* campaign.

### Question (Act 2.2)

> **Which models have the highest power-user count this quarter, and how does that compare to last quarter?**

**What to say while it runs:** Which models have the highest `power_user_count` this quarter, and how does that compare to last quarter? Power users are the renewal floor — they're not churning. The interesting question is which models are *converting* casual users into power users quarter-over-quarter; that's the model where the feature mix is working.

**What to look for:** Top 10 models by `power_user_count` with a Q/Q delta column. The Trailblazer SUV Elite or Volt EV Elite rising 30% Q/Q is the upsell story; the Metro Compact Basic falling is the pricing-floor problem.

**Land the point:** Now the GM can see which models earn the Elite-tier marketing push and which need a Basic-to-Premium upgrade prompt. That's a $4–8M annual revenue lever depending on conversion — and it's a row in this table, not a market-research engagement.

> **Anchor moment.** Stop on the high-churn-risk table and the model-by-power-user ranking. Pick the Premium tier — say it's showing 18% of vehicles flagged high churn risk with average engagement under 45.

> *Apex's Premium subscription runs ~$30/month — $360/year. Across the Premium install base, 18% high-churn-risk vehicles is the exposure. At the install-base scale this space covers (the connected fleet running through `feature_events`), even 10,000 Premium vehicles flagged high-risk = ~$3.6M/year of subscription revenue at imminent churn. ADAS subscriptions run 15–25% annual churn industry-wide; if a targeted win-back campaign recovers even a third of the high-risk pool, that's $1.2M/year saved on one tier — and the same playbook applied to Elite (where ARPU is 2–3x higher) is another $2–5M/year of renewal protection.*

> That's the decision this space automates. Not the renewal dashboard. The renewal-cycle action plan. Win-back outreach gets pointed at the Premium engagement-under-45 cohort, not the whole base — and the marketing dollar earns its keep.

### Question (Act 2.3)

> **What is the trend in average session duration month-over-month by feature category?**

**What to say while it runs:** Average `session_duration_sec` month-over-month by `feature_category`. Session duration is the engagement-depth signal — and it's where ADAS subscriptions usually die. If average session length is dropping in ADAS while staying flat in Infotainment, the customer has stopped trusting the autonomy stack.

**What to look for:** Monthly trend by category from `feature_events_metrics`. Watch the ADAS line — a steady decline over 2 quarters is a renewal-cycle red flag.

**Land the point:** That curve is the warning that next renewal cycle will miss target. The GM can act on it in March instead of finding out in June when the renewal numbers come in.

---

## Act 3 — The commitment — shaping next year's subscription P&L and OTA roadmap *(≈4 min)*

**Persona:** Subscription P&L owner • **Job to be done:** Defend the subscription P&L plan upstream — feature-investment, tier-pricing, and renewal-likelihood-driven cohort marketing for the next 12 months.

*The P&L owner doesn't need a new dashboard; they need the same numbers the GM and Product Manager are acting on, in the language the CFO actually asks about — forward-looking renewal likelihood and forecast accuracy.*

### Question (Act 3.1)

> **Top 10 models by renewal likelihood for the upcoming subscription cycle.**

**What to say while it runs:** Top 10 models by `renewal_likelihood` for the upcoming subscription cycle. The forward-looking renewal score is the only number the CFO trusts — and the model ranking inside it is where the feature/tier strategy gets locked.

**What to look for:** Ranked list of models from `feature_adoption_monthly` by predicted `renewal_likelihood`. The top of the list defends current pricing; the bottom of the list is where the discount-vs-deprecation argument lives.

**Land the point:** When the P&L owner walks into the budget review with this list, the question isn't *what's our renewal target* — it's *which models do we lean into and which do we hedge*. That's the conversation that used to need a quarterly steering committee.

### Question (Act 3.2)

> **How does actual feature adoption compare to forecasted adoption by feature tier over the trailing 12 months?**

**What to say while it runs:** Actual vs forecasted feature adoption by `feature_tier` over the trailing 12 months. The `adoption_error_pct` is the credibility check on every other number in this space — if forecasts are missing by 10+ points, the OTA roadmap and tier-pricing model both need to be rebuilt on cleaner signal.

**What to look for:** Twin bars by `feature_tier` — `forecasted_adoption_pct` vs `actual_adoption_pct`, with `adoption_error_pct` as a delta column. Watch for Elite tier missing high — that's where we're under-investing; watch for Basic missing low — that's where we're over-promising.

**Land the point:** Three artifacts — feature kill-list, win-back cohort plan, renewal-likelihood ranking — all from the same governed surface. The Product Manager, the GM, and the P&L owner are now committing to the *same* numbers. The OTA-investment conversation and the pricing-tier conversation become one conversation. That's the subscription-P&L commitment that used to need three meetings and a Friday email.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AutoMetrics Corp — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show the monthly trend in total feature events by feature category for the trailing 12 months.
2. Top 10 features by failed activation count — where is the in-vehicle UX breaking down?
3. How many vehicles are flagged high churn-risk by feature tier, and what is their average engagement score?
4. Which models have the highest power-user count this quarter, and how does that compare to last quarter?
5. What is the trend in average session duration month-over-month by feature category?
6. Top 10 models by renewal likelihood for the upcoming subscription cycle.
7. How does actual feature adoption compare to forecasted adoption by feature tier over the trailing 12 months?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
