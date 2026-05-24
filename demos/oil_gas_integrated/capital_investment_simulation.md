# CapVenture Energy — Demo Script

**Space:** Oil & Gas Integrated — CapVenture Energy - Capital Investment Simulation 💰
**Runtime:** ~15 minutes • 7 questions
**Audience:** CFO and VP of Project Finance + CapEx Committee Chair, Project Finance Lead, Asset Manager
**KPIs touched:** NPV, IRR, ROIC, Cost variance, Schedule adherence, Cumulative capex
**Big decision automated:** Which 4-5 AFE-class projects in the 20-project portfolio get sanctioned at the next CapEx Committee, which get deferred to the next price window, and which get killed outright — and how the freed capital is re-allocated against the corporate ROIC hurdle.

---

## Pre-demo checklist

- Open the Genie space `CapVenture Energy - Capital Investment Simulation 💰`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CapVenture Energy is running 20 active exploration and development projects worth a combined ~$8B of remaining sanctioned capex — Gulf of Mexico deepwater tiebacks, Permian shale pads, an LNG export train, and midstream takeaway. Today the NPV/IRR ranking lives in a Project Finance analyst's Excel model, the cost-variance pull is reconciled out of SAP each Monday by Controllership, and the risk rating is owned by the Strategy & Risk group's quarterly PowerPoint. Three artifacts, same projects — and at the quarterly CapEx Committee the Board hears three slightly different versions of which project is winning. This space ends that. NPV, IRR, ROIC, cost variance and risk rating are answered out of one governed surface, in the same conversation, against the same hurdle rate.

---

## Key KPIs in scope

- NPV ($MM) — primary economic decision metric
- IRR (%) — corporate hurdle typically 10-15% for major projects
- ROIC (%) — portfolio capital efficiency; IOC target 8-12%
- Cost variance (%) — actual vs. budget at the project level
- Schedule adherence (%) — on-time delivery against FID schedule
- Cumulative capex ($MM) — committed and drawn capital by project
- Budget remaining (%) — discretionary spend headroom
- Risk rating mix — share of portfolio at High/Critical risk

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **LNG** | Liquefied Natural Gas |

---

## Act 1 — The signal — which projects are still earning their place in the portfolio *(≈4 min)*

**Persona:** Project Finance Lead • **Job to be done:** Walk into the CapEx Committee pre-read with the current NPV ranking and a defensible view of monthly capital pacing — not the version that was true at quarter-end.

*This is the analyst's working hour before the CapEx Committee. Two questions in, the NPV ranking and the spend-pacing curve that used to take a day of model refresh are on screen.*

### Question (Act 1.1)

> **Top 10 projects by average NPV in millions.**

**What to say while it runs:** NPV is still the primary economic decision metric on the committee. For majors the hurdle is usually a 10-15% IRR with NPV positive at a $50-60 conservative price deck. The point of this ranking isn't the top — it's the bottom. Anything in the bottom quartile of avg_npv_mm is a sanction-deferral conversation, not a continue-as-planned one.

**What to look for:** A clean ranked table of 10 projects by avg_npv_mm in $MM. The room should notice the spread — top projects in the multi-hundred-million range, bottom projects barely positive or negative. That spread is the re-allocation opportunity.

**Land the point:** Now the Project Finance Lead can hand the committee a defensible NPV ranking in minutes — that's the AFE sanction conversation that used to require a full quarter of model refresh and a steering committee to align on which number was current.

### Question (Act 1.2)

> **Show monthly total capital spend by project type for the trailing 12 months.**

**What to say while it runs:** Now the capital pacing — monthly total spend by project type over 12 months. This is the chart Controllership and Project Finance argue about every month. Deepwater pulls capex in chunky FID-driven blocks; shale draws it steady-state per pad. If a project type is overrunning its monthly burn, that's a leading indicator of cost variance before the snapshot reports it.

**What to look for:** Monthly bars by project_type — DATE_TRUNC('month', transaction_date). Watch for the project type whose line is climbing faster than the others; that's where the next variance call comes from.

**Land the point:** When the same pacing curve is in the Project Finance Lead's hand and the CFO's hand by 8 AM, the monthly capex review stops being a reconciliation exercise and starts being a capital-re-allocation conversation.

---

## Act 2 — Sanction, defer, or kill — locking the CapEx Committee recommendation *(≈4 min)*

**Persona:** CapEx Committee Chair • **Job to be done:** Commit to the sanction list for the next funding window: which projects move ahead, which are deferred, and which are removed from the portfolio.

*Three questions that turn 20 projects into a defensible 5-on / 3-defer / 2-kill recommendation. The middle question — risk vs. returns on overrun projects — is where the math gets uncomfortable.*

### Question (Act 2.1)

> **Which projects are flagged as High or Critical risk, and what is their NPV and IRR?**

**What to say while it runs:** Risk rating of High or Critical with the NPV and IRR side-by-side. This is the de-sanction shortlist. A High-risk project still earning 18% IRR is a manageable bet; a High-risk project at 9% IRR is below corporate hurdle and the committee is being asked to fund downside.

**What to look for:** A table of projects with risk_rating IN ('High','Critical') showing npv_mm and irr_pct. Watch for the rows where IRR sits below the 10-15% hurdle — those are the kill candidates the committee actually came here to discuss.

**Land the point:** That list used to be three slides assembled by three teams. Now it's the input to the kill-or-defer decision that the committee actually has authority to make in the room.

### Question (Act 2.2)

> **Which projects have cost variance greater than 10% over budget, by basin region?**

**What to say while it runs:** Cost variance over 10% by basin region. Industry rule of thumb on major capital projects: cost variance over 10% means the original economic case is no longer valid and the project needs to be re-FID'd. Anything over 25% is a stop-work-and-investigate threshold.

**What to look for:** A ranked table of projects with cost_variance_pct > 10 grouped by basin_region. The Gulf of Mexico deepwater rows are the ones to dwell on — those are the projects where a single percentage point of variance is $10-50M of real money.

**Land the point:** When cost variance and NPV update against the same governed source, the committee stops arguing about which model is right and starts arguing about which projects to re-baseline. That's the conversation that protects the next $500M of capital.

> **Anchor moment.** Hold on the cost-variance table and the High/Critical risk list together. Pick the worst project — a deepwater tieback or LNG train running 15% over budget on a $500M sanctioned capex, currently risk-rated Critical.

> *15% over budget on $500M of sanctioned capex is $75M of unplanned capital. At CapVenture's 12% portfolio ROIC target, that $75M needs to generate $9M/year in incremental EBITDA just to stand still. Hold the project, that $9M comes off the dividend. Defer one quarter, the NPV compresses another 2-3%. Across a 20-project portfolio with this kind of overrun on 3-4 projects, you're looking at $200-300M of stranded capital chasing diluted returns — capital that, re-allocated to the top-quartile NPV shale tieback projects, lifts portfolio ROIC by 1-2 full points.*

> That's the call this space converts from a steering-committee exercise to a CapEx Committee decision. Not whether to defer — *which* project to defer, in dollars, against the hurdle, in the same meeting the question came up.

### Question (Act 2.3)

> **Top 10 projects by average IRR — and how do they compare on schedule adherence?**

**What to say while it runs:** IRR ranking against schedule adherence. An 18% IRR project that's six months behind FID schedule is not actually an 18% IRR project anymore — every quarter of slip compresses the NPV by 8-10% from discounting and lost first-oil. The schedule adherence column is the IRR adjustment most analysts forget to make.

**What to look for:** Top 10 by avg_irr_pct with schedule_adherence_pct alongside. Look for the rows where IRR looks great but adherence is in the 60s or 70s — those projects are not what they appear to be on the headline.

**Land the point:** That cross-check is the difference between sanctioning an IRR and sanctioning a delivery. Now the committee gets both views in the same answer, and the AFE list reflects the projects that will actually deliver.

---

## Act 3 — The commitment — re-baselining the portfolio ahead of the Board *(≈4 min)*

**Persona:** Asset Manager • **Job to be done:** Pre-wire the Board with a defensible portfolio narrative: where ROIC is heading, where capital concentration risk sits, and which segments earn the next $1B of capex.

*The Asset Manager carries the recommendation up the chain. Their job is to make sure the segment-level ROIC story holds together before it lands in the Board pack.*

### Question (Act 3.1)

> **How has portfolio ROIC trended month-over-month across the deepwater and shale segments?**

**What to say while it runs:** Portfolio ROIC by segment — deepwater versus shale, month over month. The IOC investor case is anchored on consistent ROIC at or above corporate hurdle. If deepwater is dragging ROIC down while shale is lifting it, the next capital allocation is structurally biased to shale. That's a Board-level capital-mix decision.

**What to look for:** Monthly portfolio_roic_pct trends split by project_type or basin segment. Watch for divergence — segments going opposite directions are where the Board will ask the hardest questions.

**Land the point:** When the Asset Manager walks into the Board pre-read with this curve, the conversation is no longer about whether ROIC is on track — it's about which segments earn the next billion. That's a programmatic capital-allocation conversation.

### Question (Act 3.2)

> **What is the total approved capex by spend category and phase across the active portfolio?**

**What to say while it runs:** Approved capex by spend category and phase across the active portfolio. This is the chart that tells the Board where commitments are locked in versus where there's still optionality. Sanctioned-and-spent capex is irreversible; sanctioned-and-uncommitted is the lever.

**What to look for:** A grouped table of total approved amount_usd by spend_category and phase. Look at the phase=Pre-FID and phase=FID columns — that's the discretionary pool that the next 12 months of decisions touch.

**Land the point:** Pre-FID capital is where the CapEx Committee still has full optionality. Knowing exactly how much sits there, by category, is the difference between the Board hearing 'we'll re-balance' and the Board seeing the specific $1B that's already on the table.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CapVenture Energy — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Top 10 projects by average NPV in millions.
2. Show monthly total capital spend by project type for the trailing 12 months.
3. Which projects are flagged as High or Critical risk, and what is their NPV and IRR?
4. Which projects have cost variance greater than 10% over budget, by basin region?
5. Top 10 projects by average IRR — and how do they compare on schedule adherence?
6. How has portfolio ROIC trended month-over-month across the deepwater and shale segments?
7. What is the total approved capex by spend category and phase across the active portfolio?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
