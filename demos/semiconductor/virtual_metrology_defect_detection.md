# FabSight Analytics — Demo Script

**Space:** Semiconductor — FabSight - Virtual Metrology & Defect Detection 🔬
**Runtime:** ~15 minutes • 7 questions
**Audience:** Director of Yield + VP of Process Engineering, alongside Equipment Engineering and Yield Engineering
**KPIs touched:** Critical dimension, Overlay error, Film thickness deviation, Virtual metrology prediction error %, Defect density per cm², Kill ratio %
**Big decision automated:** Reset APC/SPC thresholds on the 2 process steps with the worst CD drift, take one inspection tool down for re-qualification, and authorize the $20M VM-model retrain that unlocks the 1pp flagship yield uplift.

---

## Pre-demo checklist

- Open the Genie space `FabSight - Virtual Metrology & Defect Detection 🔬`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> FabSight Analytics runs inline metrology and defect inspection across 20 process recipes spanning litho, etch, CMP, deposition, and implant on advanced-node wafers (3nm CD ~20nm, overlay <2nm spec, ±5% film thickness control). Today the wafer_measurements feed lives in the metrology MES across 6 tools, the virtual-metrology prediction batches live in the data-science Jupyter notebooks, and defect-density and kill-ratio rollups sit in the yield-engineering review deck. Three artifacts, one yield-improvement cycle — and the last APC/SPC threshold reset took 5 weeks because the team couldn't agree on which tool was driving the CD spread until they reconciled the metrology MES and the VM model logs manually. A 1pp yield uplift on the flagship is worth $10-100M/year; an unplanned tool down for re-qualification is $50-200K/hour. This space ends the reconciliation lag. One governed surface where Process Engineering, Equipment Engineering, and the Director of Yield see CD drift, overlay error, VM prediction error, and kill ratio in the same conversation that authorizes threshold resets and tool re-qualification.

---

## Key KPIs in scope

- Critical dimension (cd_nm) — mean wafer CD; advanced-node targets tight control, e.g. 3nm gate CD ~20 nm with <1.5% within-wafer variation
- Overlay error (nm) — layer-to-layer alignment; 3nm/5nm nodes require <2 nm
- Film thickness deviation (nm) — process drift signal; spec typically ±5%
- Virtual metrology prediction error % — actual vs predicted; target <3% MAPE
- Defect density per cm² — fab-wide defectivity; mature <0.10, ramping <0.30
- Kill ratio % — share of defects that cause die failure; lower kill-ratio = healthier defect mix
- Out-of-spec measurement count — excursion driver for process holds
- Wafers inspected per month — sampling coverage; ML inspection enables 100% virtual coverage

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CD** | Critical Dimension |
| **CMP** | Chemical Mechanical Planarization |
| **MAPE** | Mean Absolute Percentage Error |
| **VM** | Virtual Metrology |

---

## Act 1 — The signal — which recipes are drifting and which steps are throwing out-of-spec *(≈4 min)*

**Persona:** Process Engineering lead • **Job to be done:** Get yesterday's metrology and defect-inspection results into a ranked list of recipes and process steps that are drifting — by avg_defect_density and out_of_spec_count — before the APC threshold review.

*This is where the threshold-reset conversation actually starts — not in the monthly review, but in the avg_defect_density and out_of_spec_count lines. Two questions in, the lead has the recipes and process steps that need attention ranked by the dollars at stake.*

### Question (Act 1.1)

> **Which 10 process recipes have the highest average defect density in the trailing 12 months?**

**What to say while it runs:** Top 10 process recipes by avg_defect_density_per_cm2 over 12 months — mature processes run <0.10 and ramping nodes <0.30. Any recipe chronically above 0.30 on a flagship product is yield-improvement scope; above 0.50 is a recipe-of-record review.

**What to look for:** Ranked table from defect_detection_metrics with avg_defect_density. The recipes at the top are where Process Engineering capacity reallocates this quarter — and those are typically the litho and etch steps on the leading-edge product.

**Land the point:** Right there is the yield-improvement scope. Now the Process lead can name the 5 recipes that earn the next FMEA in minutes — that's the methodology investment conversation that used to require a 90-minute working group.

### Question (Act 1.2)

> **Show monthly out-of-spec measurement count by process step for the trailing 12 months.**

**What to say while it runs:** Monthly out_of_spec_count by process_step over 12 months — litho vs etch vs CMP vs deposition vs implant. The step whose excursion line is climbing is the step driving the process-hold escalations, and that's the step where the APC threshold band needs to tighten or the tool needs intervention.

**What to look for:** Monthly trend, DATE_TRUNC('month', measurement_date) shape, broken out by process_step from wafer_measurement_metrics. Watch for the step diverging upward against the others.

**Land the point:** Before this space, that chart was an Equipment Engineering admin export from the MES. Now Process Engineering opens with it — and the APC threshold conversation starts in the morning standup.

---

## Act 2 — The decision — threshold reset, tool re-qualification, or model retrain *(≈4 min)*

**Persona:** Equipment Engineering lead • **Job to be done:** Commit which APC/SPC thresholds get reset this week, which inspection tool gets pulled for re-qualification, and whether the virtual-metrology model needs an emergency retrain.

*Three questions that turn the drift watchlist into a defensible engineering authorization. The middle question is the anchor — the prediction-error-and-kill-ratio conversation that converts metrology signals into yield-uplift dollars.*

### Question (Act 2.1)

> **Which defect types are driving the highest kill ratios this quarter — what are we losing yield to?**

**What to say while it runs:** Defect types ranked by avg_kill_ratio_pct this quarter — kill ratio is the share of defects that actually cause die failure. Lower kill ratio = healthier defect mix; rising kill ratio means the defects we are catching are increasingly the ones that take down die. That's where the yield-improvement dollars belong.

**What to look for:** Ranked table from defect_detection_metrics with avg_kill_ratio_pct and total_defects_found. The defect types with rising kill ratios are this quarter's FMEA priority.

**Land the point:** That ranking used to be a manual Jupyter notebook query against the defect log. Now it's the input to the corrective-action authorization the Equipment Engineering lead signs at standup.

### Question (Act 2.2)

> **Rank metrology tools by average overlay error — which of the 6 tools need re-qualification?**

**What to say while it runs:** Average overlay_nm by tool_id — 3nm and 5nm nodes require <2nm; if any of the 6 metrology tools is averaging above 2.5nm or the spread between tools is wider than 1.5nm, the tool itself is the dominant noise source. That's a re-qualification call, and re-qualification is 1-4 weeks of lost capacity.

**What to look for:** Per-tool ranking from wafer_measurements aggregated to avg_overlay_nm. The worst tool is the next re-qualification candidate; the spread tells you whether it's a tool issue or a methodology issue.

**Land the point:** When Process Engineering, Equipment Engineering, and the Director of Yield all query overlay error the same way and see the same number, the meeting stops being whose MES export is current and starts being which tool comes down for re-qual next week.

> **Anchor moment.** Stop on the kill-ratio table and the overlay-by-tool ranking on screen. Pick the worst case — call it 2 process steps with cd_nm standard deviation creeping outside the ±1.5% within-wafer envelope, one inspection tool averaging 3nm overlay error, and the VM model prediction_error_pct climbing from 2.5% to 5% over 4 months.

> *A 1pp yield uplift on the flagship product is worth $10-100M/year; call it $40M for this product. The CD drift on those 2 process steps is sitting on roughly 0.7-1.2pp of yield exposure based on the within-wafer spread, so resetting the APC thresholds and tightening the SPC bands recovers about $30-40M annualized. Pulling the worst inspection tool down for a 2-week re-qualification costs $50-200K/hour × ~50 production-hours of lost coverage = call it $5-10M of forgone capacity, but it removes the overlay noise that's been masking the real defect signature. The VM model retrain is a $15-20M data-science investment that takes 8-12 weeks but unlocks 100% virtual coverage on 3 additional process steps — that's $30M of annual sampling-cost reduction plus the pull-ahead yield-engineering capacity. Net call: reset thresholds on 2 process steps Monday, pull the inspection tool for re-qual next maintenance window, authorize the $20M VM retrain.*

> That's the decision this space automates. Not the slide. The decision. Two thresholds reset, one tool down for re-qual, one model retrain authorized — in one conversation, with one set of numbers, before the monthly yield review.

### Question (Act 2.3)

> **How has average VM prediction error trended monthly — is the model drifting?**

**What to say while it runs:** Now monthly avg prediction_error_pct from metrology_predictions — VM target is <3% MAPE. If the prediction error is climbing month over month while the model_version stays constant, the model is drifting and an emergency retrain is on the table. If model_version is rolling forward but error isn't dropping, the feature set is the problem.

**What to look for:** Monthly trend of avg prediction_error_pct from metrology_predictions. An inflecting line is the cue to authorize the next VM retrain; a flat-high line is the cue to revisit feature engineering.

**Land the point:** That comparison is the difference between knowing the VM model is off and knowing whether it's data drift or model drift. The first is a data-science observation; the second is a $20M retrain authorization.

---

## Act 3 — The commitment — shaping next year's metrology investment and the sampling strategy *(≈4 min)*

**Persona:** Director of Yield • **Job to be done:** Defend the yield-improvement roadmap to the executive team, lock in the VM-model investment, and shape next year's sampling-coverage strategy.

*The Director doesn't need another dashboard; they need the same CD, overlay, prediction-error, and kill-ratio numbers Process and Equipment Engineering are acting on — so the yield-roadmap pitch and the daily standup are the same artifact.*

### Question (Act 3.1)

> **Which process steps have the highest standard deviation of cd_nm across recent measurements, and which tools are driving the spread?**

**What to say while it runs:** Process steps with the highest standard deviation of cd_nm across recent measurements, with the dominant tool_id alongside. Where the spread is largest is where the next metrology-tool investment dollar has to land — and the tool driving the spread is the candidate for replacement or upgrade.

**What to look for:** Process_step ranking with stddev of cd_nm from wafer_measurements, broken out by tool_id. The combinations at the top are the focus of the next year's metrology capex.

**Land the point:** When this view is in the Director's hand before the yield-roadmap review, the executive conversation moves from reactive to programmatic — and the team stops being told about CD excursions after the yield miss is already in the quarterly numbers.

### Question (Act 3.2)

> **What is the total wafers inspected by process step in the trailing 6 months — where is sampling coverage lowest?**

**What to say while it runs:** Total wafers_inspected by process_step over 6 months from defect_detections — sampling coverage is the leading indicator of which steps the VM model can virtualize next. The steps with lowest coverage are where the next ML inspection deployment unlocks the biggest cost reduction.

**What to look for:** Per-step total wafers_inspected. The lowest-coverage steps that are also high-defect-density are where the next VM expansion has to focus.

**Land the point:** Triage at the morning standup, threshold and tool decisions at the engineering review, yield-roadmap defense at the executive meeting. Same space. Same numbers. The Process Engineering watchlist and the Director of Yield's roadmap pitch are now the same artifact — and the executive team gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — FabSight Analytics — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Which 10 process recipes have the highest average defect density in the trailing 12 months?
2. Show monthly out-of-spec measurement count by process step for the trailing 12 months.
3. Which defect types are driving the highest kill ratios this quarter — what are we losing yield to?
4. Rank metrology tools by average overlay error — which of the 6 tools need re-qualification?
5. How has average VM prediction error trended monthly — is the model drifting?
6. Which process steps have the highest standard deviation of cd_nm across recent measurements, and which tools are driving the spread?
7. What is the total wafers inspected by process step in the trailing 6 months — where is sampling coverage lowest?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
