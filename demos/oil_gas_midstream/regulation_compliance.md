# CompliFlow Systems — Demo Script

**Space:** Oil & Gas Midstream — CompliFlow Systems - Regulation & Compliance 📋
**Runtime:** ~15 minutes • 7 questions
**Audience:** Chief Compliance Officer + EH&S Director, General Counsel, Operations VP
**KPIs touched:** Compliance score, Open findings, Overdue actions, Total fines, Avg resolution days, Violation count
**Big decision automated:** Which assets and compliance areas earn the next remediation capex ahead of the PHMSA / FERC deadline — and which findings we accept the fine on to redirect dollars where the enforcement risk is higher.

---

## Pre-demo checklist

- Open the Genie space `CompliFlow Systems - Regulation & Compliance 📋`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CompliFlow Systems operates pipeline systems under PHMSA pipeline-safety rules, EPA OOOOb methane rules, FERC tariff orders, and a patchwork of state PUC requirements. Today the open-findings list lives in the EH&S team's audit tracker, the fine exposure and NOPV log lives in a Legal spreadsheet, and the audit closure rate lives in the Chief Compliance Officer's monthly board metric. Three workbooks, same regulators — and the remediation-capex queue, the enforcement-escalation defense, and the corporate-attestation sign-off all get built from snapshots that don't reconcile. This space ends that. One governed surface where total_fines_usd, open_findings, overdue_actions, and compliance_score line up by regulatory body and compliance area — so the remediation queue gets ranked by enforcement risk, not by audit cycle.

---

## Key KPIs in scope

- Compliance score (0-100) — composite audit and findings score (target >90)
- Open findings — backlog of unresolved audit items
- Overdue actions — past-due remediation items (target = 0)
- Total fines ($) — enforcement exposure by regulatory body
- Avg resolution days — speed of closing violations (target <30 days)
- Violation count — Notices of Probable Violation issued
- Closure rate (%) — % of findings closed on time
- Training completion (%) — workforce compliance readiness

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **FERC** | Federal Energy Regulatory Commission |

---

## Act 1 — The signal — where the enforcement exposure is concentrating *(≈4 min)*

**Persona:** EH&S Director • **Job to be done:** Identify the regulatory bodies and compliance areas driving fine exposure before the next executive risk review.

*This is the moment the next quarter's remediation plan starts to take shape. Two questions in, EH&S has the fines-by-body trend and the violation-by-area ranking that used to take a quarter of audit-tracker cleanup.*

### Question (Act 1.1)

> **Show monthly total fines by regulatory body for the trailing 12 months.**

**What to say while it runs:** Monthly total fines by regulatory body over the trailing 12 is the enforcement-pressure view. PHMSA can fine up to $250K per day per violation; EPA OOOOb has its own escalator; FERC sits separately on tariff and reporting. If the curve on any one body is climbing two quarters in a row, that's a structural exposure that needs a capex response.

**What to look for:** Monthly bars of total_fines_usd by regulatory_body — DATE_TRUNC('month', event_date) shape. The room should notice whether PHMSA, EPA, or FERC is the dominant exposure and whether it's trending up or normalizing.

**Land the point:** Now the EH&S Director walks into the risk committee with the dominant exposure already named — and the conversation that used to start 'where are we on compliance' starts 'PHMSA exposure is climbing, here's the plan.'

### Question (Act 1.2)

> **Rank compliance areas by violation count year-to-date.**

**What to say while it runs:** Ranking compliance areas by violation_count YTD is the where-the-work-is view. Integrity management, OQ qualification, control-room management, OOOOb fugitive emissions — they're different programs with different remediation costs and different escalation paths. Highest-count areas are where the program either gets refunded or restructured.

**What to look for:** Ranked table of compliance_area with violation_count. A handful of areas typically own most of the volume — those are the program-level investment candidates.

**Land the point:** That ranking used to be the output of a quarterly audit review. Now it's a question — and the program-restructure conversation happens at +30 days, not +90.

---

## Act 2 — The decision — which assets we upgrade before deadline and which fines we accept *(≈4 min)*

**Persona:** Chief Compliance Officer • **Job to be done:** Lock the remediation-capex queue against the PHMSA / FERC / EPA enforcement calendar and decide which findings get capital and which get accepted as a known-fine cost.

*Three questions that turn the violation backlog into a capital-allocation decision and a defensible legal posture. The middle question is the anchor — the fine-exposure-to-dollars math that converts a compliance dashboard into a board conversation.*

### Question (Act 2.1)

> **Which regulations currently have the most overdue actions, and what is the compliance score for each?**

**What to say while it runs:** Regulations with the most overdue_actions and their compliance_score is the imminent-escalation view. Overdue actions are exactly what auditors anchor on in the next visit — anything with non-zero overdue and a compliance_score below 80 is a Notice of Probable Violation waiting to happen.

**What to look for:** Regulation_name with overdue_actions and compliance_score. High-overdue, low-score is the top of the queue; low-overdue, high-score is the part of the portfolio we can defend on its own.

**Land the point:** When the CCO can see overdue work and compliance score in the same view, the remediation conversation moves from 'fix everything by Q4' to 'fix these three regulations by Q4, the rest are on a known plan.' That's a defensible posture.

### Question (Act 2.2)

> **How has average resolution days trended month-over-month across PHMSA findings?**

**What to say while it runs:** Average resolution_days trended monthly across PHMSA findings is the program-velocity view. Best-in-class operators close findings inside 30 days; the regulator pays attention when the trend goes the wrong way. PHMSA specifically uses resolution speed as an enforcement-discretion input.

**What to look for:** Monthly trend of avg_resolution_days for PHMSA findings. A flat-to-declining line under 30 days is what the regulator wants to see; anything climbing above 60 is a behavioral red flag.

**Land the point:** When that curve is in the CCO's hand a quarter before the audit cycle, the enforcement-discretion conversation with PHMSA happens with evidence, not promises. That's the difference between a warning letter and a consent order.

> **Anchor moment.** Hold on the overdue-actions table and the PHMSA resolution-days trend. Take the worst compliance area — call it 12 overdue PHMSA actions across two compressor stations with a compliance_score of 72.

> *At PHMSA's $250K per-violation-per-day exposure, 12 overdue actions sitting open another 60 days is a theoretical $180M ceiling — obviously not the realistic outcome, but the prosecutorial maximum. The actual settlement math for an operator at compliance_score 72 historically runs $1-3M per significant finding once it converts to NOPV. Twelve open items at expected $1.5M each is $18M of fine exposure on the books. Compare that to a targeted $5-8M integrity-capex spend that closes the actions and lifts the score above 90 — payback inside 12 months on avoided fines alone, before counting the consent-decree risk we sidestep.*

> That's the decision this space automates. Not the audit close pack. The capex sequencing. Remediation gets prioritized on fine exposure and deadline pressure, not on which finding the EH&S team happened to hear about last.

### Question (Act 2.3)

> **Top 10 compliance events by fine amount in the last 6 months.**

**What to say while it runs:** Top 10 compliance events by fine_amount in the last 6 months is the where-the-dollars-are view. PHMSA's per-day per-violation maximum is north of $250K — a single integrity event can put $1-3M of fine exposure on the books, and we want those isolated and triaged immediately.

**What to look for:** Ranked table of event_id with fine_amount_usd and severity. The top 3-5 events typically carry most of the fine exposure — those are the ones General Counsel needs to drive the defense on.

**Land the point:** That list is the input to the next legal-strategy session. The CCO and GC walk in with the fine-exposure picture already framed — and the decisions about which fines to litigate vs. settle vs. accept get made in one meeting, not three.

---

## Act 3 — The commitment — defending the compliance posture to the board and the regulator *(≈4 min)*

**Persona:** General Counsel • **Job to be done:** Lock the legal-strategy framework for active findings and present the residual enforcement exposure to the board's risk committee.

*The GC doesn't need a fourth tracker; they need the same compliance scores, fine exposure, and closure-rate numbers EH&S is running on — so the board pitch and the regulator dialogue are built off one record.*

### Question (Act 3.1)

> **What is the average compliance score by regulatory body, and which are below 90?**

**What to say while it runs:** Average compliance score by regulatory_body and which sit below 90 is the where-we're-vulnerable view. Below 90 is where the next audit either escalates or doesn't; we want every regulatory body sitting above 90 going into the next cycle.

**What to look for:** Regulatory_body with avg_compliance_score. Anything below 90 is the body where the next dollar of remediation capex earns the most regulator goodwill.

**Land the point:** When GC can show the board a compliance-score trajectory by body, the enforcement-risk conversation moves from anecdotes to a managed portfolio. That's the difference between a risk committee that's worried and one that signs off.

### Question (Act 3.2)

> **How has closure rate percentage trended monthly across the compliance portfolio?**

**What to say while it runs:** Closure rate percent trended monthly is the program-credibility view. Best-in-class operators close above 95% on time; anything trending below that is what the regulator points to in the next audit. The slope matters more than any single month.

**What to look for:** Monthly trend of closure_rate_pct. A flat-to-rising line above 95% is the story the next audit cycle wants to hear.

**Land the point:** Same numbers EH&S closes findings on, GC defends the company on, and the board signs off on. That's the consistency the regulator looks for — and now we can answer it in real time, not in the next 10-K.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CompliFlow Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total fines by regulatory body for the trailing 12 months.
2. Rank compliance areas by violation count year-to-date.
3. Which regulations currently have the most overdue actions, and what is the compliance score for each?
4. How has average resolution days trended month-over-month across PHMSA findings?
5. Top 10 compliance events by fine amount in the last 6 months.
6. What is the average compliance score by regulatory body, and which are below 90?
7. How has closure rate percentage trended monthly across the compliance portfolio?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
