# RestorePower Gen — Demo Script

**Space:** Power Generation — RestorePower Gen - Outage Response & Restoration 🔌
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP / Director of Generation + Plant Manager, Reliability Engineer, Fleet Performance lead
**KPIs touched:** Equivalent Forced Outage Rate, Equivalent Availability Factor, Mean Time To Repair hours, Forced outage count, Lost generation, Repair cost
**Big decision automated:** Which units get the next outage-recap capex tranche, how much mutual-aid and parts inventory to stage ahead of the next event, and which chronic offenders go on the early-retirement list before the PUC review.

---

## Pre-demo checklist

- Open the Genie space `RestorePower Gen - Outage Response & Restoration 🔌`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> RestorePower Gen runs 20 generating units across multiple stations — a mix of gas turbines, combined-cycle, steam, diesel, and hydro — typically a 4-6 GW portfolio. Today the EFOR number lives in the Reliability Engineer's NERC GADS submission workbook, the active-event restoration ETAs sit in the dispatcher's outage management spreadsheet, and the repair-cost variance to budget lives in the Plant Manager's monthly maintenance report. Three artifacts, same 20 units, three different versions of *which units are dragging the fleet availability number* — and the next capex prioritization call and the next mutual-aid staging recommendation get shaped by whichever artifact made it into the PUC reliability filing first. This space ends that. One governed surface where EFOR, MTTR, lost generation, and repair cost reconcile so the chronic-offender ranking, the active-event triage, and the long-cycle reliability defense all come from the same numbers.

---

## Key KPIs in scope

- Equivalent Forced Outage Rate (EFOR) — NERC GADS benchmark; fleet target <5%
- Equivalent Availability Factor (EAF) — industry target >90%
- Mean Time To Repair (MTTR) hours — restoration efficiency
- Forced outage count — reliability of unplanned downtime
- Lost generation (MWh) — revenue exposure from outages
- Repair cost ($) — maintenance budget driver
- Parts on hand (%) — supply-chain readiness for restoration
- Restoration progress (%) — active-event tracking

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **ETA** | Estimated Time of Arrival |
| **MTTR** | Mean Time To Repair |
| **NERC** | North American Electric Reliability Corporation |

---

## Act 1 — The signal — finding the forced-outage leaders before the monthly NERC report *(≈4 min)*

**Persona:** Reliability Engineer • **Job to be done:** Pull the next NERC GADS submittal out of yesterday's outage events and name the units dragging the fleet EFOR before they show up in the next monthly review.

*This is the moment the reliability briefing stops being a multi-day data assembly and becomes a daily read. Two questions in, the Reliability Engineer has the forced-outage trend and the lost-generation watchlist — that's the spine of the next monthly outage review.*

### Question (Act 1.1)

> **Show monthly forced outage count by unit type for the trailing 12 months.**

**What to say while it runs:** Monthly forced_outage_count by unit_type for the trailing 12 months is the NERC GADS story every reliability engineer reads first. Fleet target is EFOR below 5%; gas turbines typically run cleaner than steam, and any unit_type with a climbing forced-count slope is the *which technology is hurting us* signal months before it shows up in the rate case.

**What to look for:** Monthly bars of forced_outage_count broken out by unit_type — gas turbine, combined cycle, steam, diesel, hydro. Watch for the steam fleet's slope; aging steam units carry the fleet's worst EFOR, and the slope tells you whether that's improving or sliding.

**Land the point:** Now the Reliability Engineer can rank unit types on forced-outage trajectory in seconds instead of waiting for the monthly NERC GADS upload — that's the *which technology cohort hurts fleet EFOR* conversation that used to require a reliability analyst to manually reconcile the outage log.

### Question (Act 1.2)

> **Top 10 units by total lost generation MWh year-to-date.**

**What to say while it runs:** Top 10 units by total_lost_generation_mwh year-to-date is the *which units cost us the most production this year* ranking. That's the chronic-offender list — units that have either repeated forced outages or one long outage that wrecked the year. Either pattern is a capex conversation, and they need very different remedies.

**What to look for:** Ranked table — unit_name, station, total_lost_generation_mwh. The story is the spread; the top unit's lost generation versus the bottom of the top-10 is the size of the recoverable-availability prize.

**Land the point:** Right there is the recap-capex shortlist. Before this space, that list was rebuilt from outage-event extracts each month. Now it's the first question of the morning — and the *which units earn the next $50M of overhaul capex* conversation starts from defensible numbers.

---

## Act 2 — The decision — recap, refurb, retire, or stage mutual-aid *(≈4 min)*

**Persona:** Plant Manager • **Job to be done:** Decide which units get the next recap capex, which active events need mutual-aid escalation, and which cause codes signal a structural fleet problem rather than a one-off event.

*Three questions that turn the chronic-offender ranking into a defensible capital and operational commitment. The middle question is the anchor — the lost-generation-to-dollars conversion that decides whether the next outage gets a stage-up to mutual-aid or rides the in-house crew.*

### Question (Act 2.1)

> **Which cause codes drive the most repair cost this year, and what is the average duration?**

**What to say while it runs:** Top cause_codes by total_repair_cost this year, paired with avg_outage_duration_hours, is the root-cause investment view. Generator-end failures and steam-path damage are the high-cost, long-duration codes; balance-of-plant codes are usually shorter and cheaper. The cluster matters — if three units share the same cause code, that's a fleet-design conversation, not a unit-level one.

**What to look for:** Short table — cause_code, total_repair_cost, avg_duration_hours. Watch for cause codes that show up across multiple unit types; that's the cross-fleet engineering review that has to happen before the next refurb cycle.

**Land the point:** That cause-code rollup used to take the Reliability team three days of cross-referencing event reports. Now it's the *do we have a fleet-wide design issue or a unit-specific issue* answer — and the engineering-spend defense at the budget meeting moves from anecdote to data.

### Question (Act 2.2)

> **How has fleet average availability trended month-over-month, broken out by station?**

**What to say while it runs:** Fleet average availability month over month, broken out by station, is the EAF defense line. Industry target is 90%+; a station running consistently in the 80s is either the station-level maintenance program or the unit mix that station runs. Both fix differently — and the rate case needs to know which.

**What to look for:** Monthly trend of avg_availability_pct by station. The flatlines around 90 are clean; any station declining toward 85 is the conversation the Plant Manager has with the Fleet Performance lead before the PUC reliability filing.

**Land the point:** When the station-by-station availability slope is in the Plant Manager's hand a quarter before the next PUC filing, the recovery plan moves from defensive to programmatic — and the *which station earns the next $20M of refurb capex* discussion happens with data instead of with personalities.

> **Anchor moment.** Stop on the chronic-offender list from Act 1 and the cause-code spend ranking on screen. Pick the worst chronic offender — call it a single 250 MW steam unit at one station with 4,000 MWh of lost generation in 90 days and a generator-end cause code in two of those outages.

> *4,000 MWh of lost generation in 90 days at $50/MWh of foregone PPA revenue is $200K per quarter — call it $800K per year, plus another $400K of additional repair cost above maintenance budget. A generator-end refurb on that unit runs $8-15M of capex but recovers most of the EFOR penalty and adds 2-3 percentage points of availability against an EAF target of 90%. At fleet scale, a 1 percentage point fleet availability lift on a 5 GW portfolio is roughly $5-10M of margin per year. Across the top-five chronic offenders at RestorePower's scale, that's $30-50M of recoverable annual margin against a $40-75M multi-year recap AFE — and the SAIDI defense at the PUC for the same dollars.*

> That's the decision this space automates. Not the slide. The decision. The recap capex tranche gets ranked on lost-generation dollars actually leaking out today, not on equipment-age tables — and the Plant Manager's overhaul list and the Reliability Engineer's NERC submittal land in the same artifact.

### Question (Act 2.3)

> **Which units have an active repair with parts on hand below 80% and restoration progress below 50%?**

**What to say while it runs:** Active repairs with parts_on_hand below 80% and restoration_progress below 50% is the *which outage do I escalate to mutual-aid* triage view. Long-cycle repairs with thin parts coverage are the events that turn from week-long to month-long without intervention. Mutual-aid is expensive but cheaper than another week of lost generation.

**What to look for:** Repair snapshots filtered to parts_on_hand_pct < 80 AND restoration_progress_pct < 50 with cost_to_date_usd alongside. The list is the daily triage; the cost-to-date column tells you which events have already over-run the original repair-cost budget and which are still recoverable.

**Land the point:** That triage list used to live in the dispatcher's spreadsheet and update once a day. Now it's the live view both the Plant Manager and the Reliability Engineer act on — and the *call mutual-aid now or wait* conversation happens hours earlier in the event, not after the dispatcher's morning briefing.

---

## Act 3 — The commitment — PUC reliability defense and the early-retirement list *(≈4 min)*

**Persona:** Fleet Performance Lead • **Job to be done:** Defend the fleet's reliability trajectory to the PUC and the board, and recommend which chronic offenders earn refurb capex versus early-retirement.

*The Fleet Performance lead doesn't need more dashboards; the lead needs the same numbers the Reliability Engineer and the Plant Managers are operating on so the PUC filing and the board recap recommendation reconcile to operating reality.*

### Question (Act 3.1)

> **Top 10 outages by repair cost USD in the last 90 days — and how does that compare to the prior 90?**

**What to say while it runs:** Top 10 outages by repair_cost_usd in the last 90 days with a comparison to the prior 90 is the spending-trajectory view. Repair cost trending up faster than fleet activity is the *are we over-maintaining the wrong units* signal — that's the conversation the board has with the CFO before approving next year's O&M budget.

**What to look for:** Ranked table of recent outages with repair_cost_usd and prior-period delta. Outages where cost is materially higher than the prior period without a clear root cause are the budget-defense conversations the Fleet Performance lead needs to land in.

**Land the point:** When this list lands in the budget meeting in the same space the Reliability Engineer used to prep, the O&M defense and the recap AFE pitch line up — and the *which units earn refurb versus retirement* conversation becomes a single recommendation instead of three competing ones.

### Question (Act 3.2)

> **What is the monthly trend in average outage duration hours (MTTR) for forced outages?**

**What to say while it runs:** Monthly trend in avg_outage_duration_hours for forced outages is the MTTR story — the PUC, the rating agencies, and the analyst desk all read this differently. A flat or declining MTTR is reliability discipline; a rising MTTR with stable forced count is parts-availability or crew-staffing; a rising MTTR with rising forced count is a structural fleet problem.

**What to look for:** Monthly avg_outage_duration_hours filtered to outage_type = 'Forced'. The slope and the level both matter; the operating narrative reads off the combination.

**Land the point:** Triage in the morning outage call, capex commitment at the next quarterly budget meeting, PUC reliability defense at the next case. Same space, same numbers. The Reliability Engineer's chronic-offender list and the Fleet Performance lead's retirement recommendation are now the *same artifact* — and the PUC, the board, and the rating agencies all get one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — RestorePower Gen — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly forced outage count by unit type for the trailing 12 months.
2. Top 10 units by total lost generation MWh year-to-date.
3. Which cause codes drive the most repair cost this year, and what is the average duration?
4. How has fleet average availability trended month-over-month, broken out by station?
5. Which units have an active repair with parts on hand below 80% and restoration progress below 50%?
6. Top 10 outages by repair cost USD in the last 90 days — and how does that compare to the prior 90?
7. What is the monthly trend in average outage duration hours (MTTR) for forced outages?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
