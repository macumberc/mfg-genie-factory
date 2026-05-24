# TraceCore Materials — Demo Script

**Space:** Chemicals & Materials — TraceCore Materials - Product & Process Traceability 📋
**Runtime:** ~15 minutes • 7 questions
**Audience:** Quality Director + Plant Quality Engineer, Quality Director, Supply Chain VP
**KPIs touched:** Traceability score, Recall readiness, Quality pass rate, Lots with full genealogy / lots produced, Quality holds count, Supplier audits completed
**Big decision automated:** Which lots to release vs. quarantine this week, which supplier to drop from the qualified list, and which facilities earn the next 18 months of traceability investment.

---

## Pre-demo checklist

- Open the Genie space `TraceCore Materials - Product & Process Traceability 📋`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> TraceCore Materials produces 20 products — resins, pigments, catalysts, surfactants, intermediates — across 5 facilities serving downstream customers under REACH, GHS, and TSCA. Today the lot-genealogy completeness number lives in the Quality Director's audit binder, the supplier failed-QC counts live on the Plant Quality Engineer's whiteboard, and the held-inventory write-down lives in the controller's monthly reconciliation. Three artifacts, same lots — and the lot-release / quarantine / supplier-de-qualification calls (each one a $20K-300K decision) get made by the loudest voice on the daily quality call. This space ends that. One governed surface where traceability score, recall-readiness hours, and supplier-failure data land in the same conversation as the lot-release queue.

---

## Key KPIs in scope

- Traceability score (%) — completeness of lot genealogy records; target ≥ 95%
- Recall readiness (hours) — time to trace a lot end-to-end; regulatory target < 4 hours
- Quality pass rate (%) — share of production events passing QC; target ≥ 95%
- Lots with full genealogy / lots produced — audit-readiness indicator
- Quality holds count — held-inventory exposure and working-capital lock
- Supplier audits completed — supply-chain compliance cadence
- Process step yield (output_kg / input_kg) — material efficiency by step
- Quarantined / recalled lot count — direct write-down and customer-notification trigger

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **CFO** | Chief Financial Officer |
| **QC** | Quality Control |
| **VP** | Vice President |

---

## Act 1 — The signal — finding the lots and suppliers that won't survive an audit *(≈4 min)*

**Persona:** Plant Quality Engineer • **Job to be done:** Pull tomorrow's quarantine candidates and the suppliers driving them — before the audit team asks for the trace.

*This is where the lot-release queue gets pre-built. Two questions in, the engineer already has the list that used to take a morning of binder-flipping.*

### Question (Act 1.1)

> **Show monthly average traceability score by product category for the trailing 12 months.**

**What to say while it runs:** Monthly average traceability score by product category over 12 months — resins, pigments, catalysts, surfactants, intermediates. Target is 95%+ for audit-ready inventory. Anything sliding below 90% means a meaningful share of lots can't be traced end-to-end in under 4 hours, which is the regulatory window for a mock recall.

**What to look for:** Monthly avg_traceability_score by product_category. Categories where the line has drifted below 90% are categories whose lots are quietly at risk of being un-releasable if an audit hits this week.

**Land the point:** Right there is the first conversation — which categories have a structural traceability gap, not a one-lot exception. That's a process-control fix, not a paperwork fix, and the engineer just identified it before the morning standup.

### Question (Act 1.2)

> **Rank suppliers by failed quality check count this year — which products are affected?**

**What to say while it runs:** Now suppliers ranked by failed_quality_checks year-to-date, with the products they touch. Industry expectation is a qualified supplier delivers 95%+ pass on incoming QC. A supplier showing up at the top of this list isn't a noisy month — they're the upstream cause of the held inventory we're paying to store.

**What to look for:** Ranked table of supplier_id by failed_quality_checks count, with the affected product_name list alongside. The repeat names on this list are the supplier-de-qualification shortlist.

**Land the point:** Before this space, that supplier ranking was rebuilt by hand for every quarterly supplier review. Now it's the engineer's first question of the day — and the de-qualification conversation starts with a defensible list, not a gut call.

---

## Act 2 — The decision — which lots to quarantine, which supplier to drop, which process step to lock *(≈4 min)*

**Persona:** Quality Director • **Job to be done:** Commit to the week's lot-release / quarantine decisions, the supplier-drop recommendation, and the process step that needs an immediate CAPA lock.

*Three questions that turn the supplier-and-lot watchlist into defensible commercial actions. The middle question is the anchor — the held-inventory dollar exposure that converts a quality call into a write-down decision.*

### Question (Act 2.1)

> **How has average recall readiness time (hours) trended month-over-month across facilities?**

**What to say while it runs:** Recall readiness time, month over month across facilities. Regulatory target is under 4 hours to trace a lot end-to-end. Facilities sitting above 6 or 8 hours aren't doing paperwork wrong — they have a structural genealogy gap that will fail the next mock recall, and that's a notifiable event with customers under contractual recall-response SLAs.

**What to look for:** Monthly trend of avg_recall_readiness_hours by facility_id. Facilities with a rising trend are the ones whose next REACH inspection becomes a 21 CFR-style finding, not a tour.

**Land the point:** That chart used to be the appendix slide nobody opened. Now it's the front of the quality director's weekly review — and the facilities at the top earn the next traceability investment dollar, not the ones the audit team happens to visit next.

### Question (Act 2.2)

> **Which products currently have lots in Quarantine or Recalled status, and what is the on-hand kg?**

**What to say while it runs:** Products currently in Quarantine or Recalled status, with quantity on hand. This is the held-inventory exposure that finance is going to ask about at month-end. For specialty chemicals, the average quarantined lot value runs $20K-100K; recalled lots run higher because of customer-side notification costs.

**What to look for:** Filtered list of lot_tracking_snapshots where lot_status is Quarantine or Recalled, sorted by quantity_on_hand_kg. The high-mass rows are the ones whose disposition decision either books a write-down or releases the inventory back to revenue.

**Land the point:** When the engineer, the director, and the CFO all query held-inventory the same way and see the same lot list, the release-vs-write-down debate stops being three meetings and starts being one decision. That's a structural change in how quality and finance interact.

> **Anchor moment.** Stop on the quarantined-lots table and the held-inventory column. Call it 40 lots currently quarantined across the network, averaging 8,000 kg each, with category-typical material value running $5-8/kg for specialty chemicals.

> *Forty lots at 8,000 kg each is 320,000 kg of held inventory. At $6/kg that's roughly $1.9M of working capital frozen in the quarantine zone. Industry average quality-hold disposition cycles take 3-6 weeks; this space, with full genealogy in one query, gets defensible release decisions down to days. Cutting hold time in half on this scale releases $900K-1M of working capital and avoids the $50K-300K write-down on the lots whose release window otherwise expires. Across 5 facilities over a year, $3-5M of recoverable inventory plus avoided write-downs.*

> That's the decision this space automates. Not the audit binder — the decision. Lot release runs on genealogy-dollar math, not gut. The supplier-drop list runs on quantified failure history, not the loudest plant manager. The CAPA lock runs on category drift, not the last bad batch.

### Question (Act 2.3)

> **What is the total quality holds count by product category over the last 6 months?**

**What to say while it runs:** Total quality holds count by product category over 6 months. This is the rolling-12 health check — categories with a climbing quality-holds trend are the ones whose CAPA program isn't closing the loop. That's a process-step lock decision, not a paperwork follow-up.

**What to look for:** Monthly trend of total_quality_holds by product_category. The categories whose hold count is climbing despite stable production volume are the ones with a structural process drift the QC team hasn't caught yet.

**Land the point:** That trend is the difference between knowing a process *had* a problem and knowing it's *still* drifting. The first is a status update; the second is a CAPA lock and a customer-notification call.

---

## Act 3 — The commitment — shaping the supplier panel and the next traceability capex cycle *(≈4 min)*

**Persona:** Supply Chain VP • **Job to be done:** Defend the supplier-qualification list to procurement and the executive committee, and shape the next 18 months of facility-level traceability investment.

*The Supply Chain VP doesn't need another quality dashboard; they need the same supplier-failure and traceability-score numbers the quality director is using, so the supplier-consolidation case writes itself.*

### Question (Act 3.1)

> **Top 10 facilities by total production output (kg) — and how do their quality pass rates compare?**

**What to say while it runs:** Top 10 facilities by total production output with quality pass rate alongside. The facilities producing the most volume with the lowest pass rate are the ones where supplier-quality issues hit the bottom line hardest, and they're the obvious candidates for the next round of supplier consolidation and inbound QC investment.

**What to look for:** Ranked table by total_output_kg with passed_quality_checks rate as a side-by-side column. The high-output, low-pass-rate quadrant is where the supply chain VP signs the consolidation memo.

**Land the point:** That's the chart that defends a supplier-panel cut to the executive committee. Volume, quality, and held-inventory dollars in one view — and the consolidation move stops being a procurement initiative and starts being a quality-driven margin recovery.

### Question (Act 3.2)

> **Which product categories have a traceability score below 90%, and what is the held-lot exposure?**

**What to say while it runs:** Categories with traceability score below 90% and the held-lot exposure attached. This is the capex-prioritization view — which facilities earn the next round of MES or batch-record system investment, and what the cost of *not* upgrading is over the next 18 months.

**What to look for:** Filtered list of categories with avg_traceability_score below 90% and the quantity-on-hand-kg of currently-held lots. The biggest exposure on a sub-90 category is the facility whose next capex case just wrote itself.

**Land the point:** Daily lot release at 8 AM, supplier decisions at 10, capex defense at noon. Same space. Same numbers. The quality director's release queue and the supply chain VP's capex pitch are now the same artifact — and the executive committee gets one story instead of three.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — TraceCore Materials — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly average traceability score by product category for the trailing 12 months.
2. Rank suppliers by failed quality check count this year — which products are affected?
3. How has average recall readiness time (hours) trended month-over-month across facilities?
4. Which products currently have lots in Quarantine or Recalled status, and what is the on-hand kg?
5. What is the total quality holds count by product category over the last 6 months?
6. Top 10 facilities by total production output (kg) — and how do their quality pass rates compare?
7. Which product categories have a traceability score below 90%, and what is the held-lot exposure?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
