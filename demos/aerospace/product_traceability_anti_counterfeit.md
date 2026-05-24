# AeroTrace Systems — Demo Script

**Space:** Aerospace — AeroTrace Systems - Product Traceability & Anti-Counterfeit 🛡️
**Runtime:** ~15 minutes • 7 questions
**Audience:** Chief Compliance Officer + Compliance Officer, VP of Quality
**KPIs touched:** Counterfeit risk score, Custody gap event count, AD compliance %, Days until certification expiry, Serviceable component count vs. unserviceable / scrapped, Documentation completeness %
**Big decision automated:** Which suppliers and component lots to quarantine this week, and which serial numbers must be pulled from in-service aircraft before the next FAA audit cycle.

---

## Pre-demo checklist

- Open the Genie space `AeroTrace Systems - Product Traceability & Anti-Counterfeit 🛡️`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> AeroTrace Systems governs AS5553 / AS6081 chain-of-custody for 20 serialized aerospace components — engine parts, avionics, landing gear, and structures — flowing through a multi-tier supply network. Today the counterfeit-risk score lives in the Compliance Officer's audit workbook, the chain-of-custody gap log lives in the receiving inspector's spreadsheet, and the Airworthiness Directive (AD) compliance rollup lives in the audit-prep binder the Chief Compliance Officer rebuilds before every FAA/EASA visit. Three artifacts, same 20 components — and the 'which parts come off the aircraft' decision gets made on whichever spreadsheet was most recently updated, with no shared view of which serial numbers are actually exposed. This space ends that. One governed surface where custody gaps, counterfeit risk, AD compliance, and certification expiry sit together, so the quarantine-and-pull decision becomes a defensible regulatory action, not an after-the-fact scramble during the audit.

---

## Key KPIs in scope

- Counterfeit risk score (0-100; flag >70 for investigation)
- Custody gap event count — chain-of-custody violations
- AD (Airworthiness Directive) compliance % (target 100% for serviceable parts)
- Days until certification expiry — flag <30 days for renewal
- Serviceable component count vs. unserviceable / scrapped
- Documentation completeness % (AS9100 requires 100% on flight-critical)
- Overdue AD count (zero-tolerance regulatory metric)
- High-risk event count — counterfeit_risk_score > 70

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the components whose paper trail is breaking before the auditor finds them *(≈4 min)*

**Persona:** Compliance Officer • **Job to be done:** Identify which component types are accumulating risk signals and which custody gaps need an immediate corrective-action response.

*This is the moment the quarantine list starts forming. Two queries in, the compliance officer already has the parts that need a chain-of-custody investigation before the next FAA visit.*

### Question (Act 1.1)

> **Top 10 component types by counterfeit risk score this quarter.**

**What to say while it runs:** Component types ranked by counterfeit risk this quarter. We investigate anything above 70. Hot-section engine parts and avionics tend to cluster at the top because that's where the gray market is most active — secondary-distributor relabeling is the usual mechanism. The ranking is the investigation priority list.

**What to look for:** A ranked table of 10 component types by avg_counterfeit_risk_score. The room should see that the top entries are the flight-critical categories — that's the regulatory exposure conversation.

**Land the point:** Right there is the supplier-investigation shortlist. The compliance officer can name the 3 component types that need a paper-trail audit this week — and the conversation with sourcing moves from 'all parts are fine' to 'these get held until we re-verify provenance.'

### Question (Act 1.2)

> **Show monthly trend in custody gap events by criticality over the trailing 12 months.**

**What to say while it runs:** Now custody gap events by criticality over 12 months. Chain-of-custody gaps on Flight-Critical components are the metric the FAA audit team opens with. A rising trend is the leading indicator of either receiving-process drift or a compromised distributor.

**What to look for:** Monthly custody_gap_events by criticality using `DATE_TRUNC('month', ...)`. Watch for Flight-Critical lines that are climbing — those are the conversations that need to happen before the auditor walks in.

**Land the point:** Before this space, that chart was a quarterly audit-prep artifact. Now it's the compliance officer's first question of the morning — and the conversation about which receiving processes need a CAPA starts a quarter earlier.

---

## Act 2 — The decision — which lots get quarantined, which serial numbers get pulled, which suppliers get suspended *(≈4 min)*

**Persona:** VP of Quality • **Job to be done:** Commit a quarantine-and-pull action plan — naming exactly which component lots get held and which serial numbers get pulled from service before the audit.

*Three questions that turn the risk watchlist into a defensible regulatory action. The middle question is the anchor — converting overdue AD exposure into the airworthiness-certificate risk math the Chief Compliance Officer will sign off on.*

### Question (Act 2.1)

> **Which component types have the highest count of overdue AD compliance, and what is the average days-until-expiry?**

**What to say while it runs:** Component types with the highest overdue AD compliance count and their average days-until-expiry. Airworthiness Directive overdues are zero-tolerance — every overdue AD on a Flight-Critical component is a potential aircraft grounding from the FAA. The days-until-expiry view is the prioritization knob.

**What to look for:** Component types ranked by overdue_ad_count with their avg_days_until_expiry. The combination tells you which categories need an AD action this week vs. this quarter.

**Land the point:** That table is the AD action plan. Two queries in, the VP of Quality has a defensible recommendation to walk into the regulatory call — and the conversation moves from 'we're behind on ADs' to 'here are the 6 component types, here's the close-out schedule.'

### Question (Act 2.2)

> **Top 10 facilities by high-risk lifecycle events in the last 6 months.**

**What to say while it runs:** Top 10 facilities by high-risk lifecycle events over 6 months. High-risk events — counterfeit_risk_score above 50, chain-of-custody gap — concentrated at a single facility is a process-control conversation; spread across many is a sourcing-policy conversation. The shape determines the corrective action.

**What to look for:** Facilities ranked by high_risk_events. Watch for facilities where one or two account for a disproportionate share — those are the facility-level audit candidates.

**Land the point:** That's the receiving-process audit list. The compliance officer and the VP of Quality now know which facilities get a process-quality visit this quarter — defensible, on data, not on rumor.

> **Anchor moment.** Stay on the overdue-AD and high-risk-event views. Pick the worst-exposed component type — say it has 8 serial numbers with overdue ADs and an average 12 days until certification expiry.

> *Each overdue AD on a flight-critical part is a potential aircraft grounding from the FAA — the operator can't dispatch that aircraft until the AD is closed. An aircraft grounding is roughly $50-100K per aircraft-day in lost utilization, ferry costs, and replacement-lift contracting. If 8 serial numbers are spread across 4 aircraft and each takes 3 days to close out under FAA observation, that's 4 aircraft × 3 days × $75K = $900K of grounding cost on this exposure alone. Across the full portfolio at AeroTrace's scale, getting ahead of the AD cycle saves $5-8M annually in avoided ground time — before counting the airworthiness-certificate risk, which is existential.*

> That's the decision this space defends. The quarantine list, the pull list, and the supplier-suspension memo get written from the same view. The Chief Compliance Officer walks into the FAA audit with a defensible posture, not a binder of overdue items.

### Question (Act 2.3)

> **How has scrapped component count trended month-over-month by component type?**

**What to say while it runs:** Scrapped component count trend by component type over 12 months. Scrap rate is the leading indicator of an upstream quality or counterfeit issue. A rising scrap line on a component type usually means receiving is catching what production used to miss — that's a supplier escalation, not a yield issue.

**What to look for:** Monthly scrapped_count by component_type. The shape — flat, climbing, or spiking — is what shapes the supplier-quality escalation list.

**Land the point:** That comparison is the difference between knowing scrap is up and knowing where it's coming from. The first is a finance metric; the second is a supplier-suspension decision.

---

## Act 3 — The commitment — defending airworthiness to the regulator and locking next-year supplier policy *(≈4 min)*

**Persona:** Chief Compliance Officer • **Job to be done:** Defend the airworthiness certificate posture to FAA/EASA, shape next-year supplier qualification policy, and approve the budget for chain-of-custody investments.

*The Chief Compliance Officer doesn't need a new report — they need the same custody-gap and AD-compliance numbers the compliance team is acting on, packaged for the regulator and consistent across every supplier conversation.*

### Question (Act 3.1)

> **Which components are currently unserviceable, and what is their criticality breakdown?**

**What to say while it runs:** Components currently unserviceable with criticality breakdown. This is the immediate exposure view — what's already off-aircraft, what's in quarantine, and how flight-critical the open items are. Anything Flight-Critical-and-unserviceable is the conversation that opens the audit.

**What to look for:** Components filtered to airworthiness_status = 'Unserviceable' grouped by criticality. The Flight-Critical row is the row the regulator asks about first.

**Land the point:** When the Chief Compliance Officer can pull this view live in front of the FAA audit team, the conversation moves from 'let us check' to 'here's the current exposure, here's the close-out plan, here's the date.' That's how audits get closed, not extended.

### Question (Act 3.2)

> **Show monthly trend in serviceable component count by criticality for the trailing 12 months.**

**What to say while it runs:** Monthly serviceable component count by criticality. The shape over 12 months is the regulatory health line — climbing is a healthy supply chain; flat or declining on Flight-Critical is a supplier-qualification problem and a budget conversation.

**What to look for:** Monthly serviceable_count by criticality. Watch the Flight-Critical line — its slope determines whether the supplier-qualification policy gets tightened next cycle.

**Land the point:** Receiving inspectors, the compliance team, and the regulator now share one view. The supplier-policy decision and the audit-defense story are written from the same numbers. One space. One airworthiness story.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — AeroTrace Systems — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 component types by counterfeit risk score this quarter.
2. Show monthly trend in custody gap events by criticality over the trailing 12 months.
3. Which component types have the highest count of overdue AD compliance, and what is the average days-until-expiry?
4. Top 10 facilities by high-risk lifecycle events in the last 6 months.
5. How has scrapped component count trended month-over-month by component type?
6. Which components are currently unserviceable, and what is their criticality breakdown?
7. Show monthly trend in serviceable component count by criticality for the trailing 12 months.

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
