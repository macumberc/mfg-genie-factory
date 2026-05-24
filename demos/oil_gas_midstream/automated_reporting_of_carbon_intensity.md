# CarbonTrack Midstream — Demo Script

**Space:** Oil & Gas Midstream — CarbonTrack Midstream - Carbon Intensity Reporting 🌱
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Sustainability + Chief Sustainability Officer, EH&S Director, ESG / Investor Relations Lead
**KPIs touched:** Total CO2e, Methane emissions, Carbon intensity, Methane intensity, Leak count, Reduction target progress
**Big decision automated:** Which compressor stations and pipeline segments earn the next $5M of methane LDAR + electrification capex — and which emission categories the ESG team defends to lenders pricing our sustainability-linked debt.

---

## Pre-demo checklist

- Open the Genie space `CarbonTrack Midstream - Carbon Intensity Reporting 🌱`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> CarbonTrack Midstream operates compressor stations, gathering segments, and processing facilities across multiple basins. Today the Scope-1 number lives in the Sustainability Officer's GHG inventory workbook, the methane-intensity number lives in an EH&S engineer's OGMP 2.0 tracker, and the leak-count list lives in a PHMSA integrity spreadsheet. Three workbooks, same molecules — and the LDAR capex ranking, the sustainability-linked-debt covenant defense, and the OOOOb compliance attestation all get built from different versions of the truth. This space ends that. One governed surface that lines up CO2e tons, methane intensity, and leak count against the actual facility list so the next decarb dollar lands on the worst-emitting asset, not the loudest one.

---

## Key KPIs in scope

- Total CO2e (metric tons) — Scope 1 inventory
- Methane emissions (tons) — most material GHG for midstream
- Carbon intensity (kg CO2e / boe) — industry leaders ~5-8 kg/boe
- Methane intensity (%) — target <0.20% under EPA OOOOb/c & OGMP 2.0 Gold
- Leak count — LDAR triggers and integrity events
- Reduction target progress (tons) — vs. corporate decarb plan
- Offset credits (tons) — voluntary or compliance offsets
- Compliance status — Compliant / Warning / Non-Compliant vs. EPA/state thresholds

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **ESG** | Environmental, Social, Governance |

---

## Act 1 — The signal — finding the methane hotspots before the OGMP audit does *(≈4 min)*

**Persona:** Sustainability Officer • **Job to be done:** Surface the facilities and emission categories driving the bulk of Scope-1 CO2e and methane tons, before they show up in the next disclosure cycle.

*This is the moment the LDAR target list starts to form. Two questions in, the sustainability team has the methane-source ranking that used to take a quarter of cross-system stitching.*

### Question (Act 1.1)

> **Show monthly total CO2e by facility type for the trailing 12 months.**

**What to say while it runs:** Total CO2e by facility type — compressor stations vs. processing vs. pipeline. Industry leaders sit at 5-8 kg CO2e per boe; anything materially above that is where the disclosure narrative breaks down. Watch the trailing-12 shape, not just the latest month.

**What to look for:** Monthly bars of total_co2e_tons by facility_type over 12 months — DATE_TRUNC('month', reading_date) shape. The room should notice which facility type dominates the stack and whether the line is bending down or flat.

**Land the point:** Now the sustainability officer can show the board which facility class owns the inventory — and that's the conversation that frames the next decarb capex ask, not a follow-up tasked to FP&A.

### Question (Act 1.2)

> **Top 10 emission sources by total methane tons year-to-date.**

**What to say while it runs:** Methane tons is the material number for midstream — it's where social cost of carbon ($50-150/ton) and OGMP 2.0 Gold reporting both hit. Top 10 sources by total_methane_tons YTD is the LDAR target list before we've spent a dime walking the right-of-way.

**What to look for:** Ranked table of source_name with total_methane_tons. The top 3-5 sources typically carry 40-60% of the methane footprint — those are the LDAR candidates that move the corporate intensity number.

**Land the point:** That list used to be the output of EH&S quarterly bottoms-up reporting. Now it's the input to the LDAR program ranking — and the budget conversation moves from 'fund LDAR generally' to 'fund LDAR on these specific four stations.'

---

## Act 2 — The decision — which assets earn the LDAR + electrification capex *(≈4 min)*

**Persona:** EH&S Director • **Job to be done:** Lock the LDAR + compressor-electrification capex queue against the methane and intensity numbers the disclosure team will actually have to defend.

*Three questions that turn the inventory into a capital-allocation ranking. The middle question is the anchor — the methane-tons-to-dollars conversion that converts an EH&S program into a finance conversation.*

### Question (Act 2.1)

> **Which facilities have a carbon intensity above the company average, and what is the throughput at each?**

**What to say while it runs:** Carbon intensity above the company average flags the structurally worst assets — and we want intensity in the same frame as throughput_boe, because a high-intensity low-throughput asset and a high-intensity high-throughput asset are two different capex stories.

**What to look for:** Facility-level table with carbon_intensity_kg_boe and total_throughput_boe side by side. The high-intensity, high-throughput row is the one that earns electrification dollars first.

**Land the point:** When intensity and throughput land in the same view, the LDAR vs. electrification vs. retire conversation stops being three meetings and becomes one ranked list the director can sign off on.

### Question (Act 2.2)

> **How has total leak count trended month-over-month across the network?**

**What to say while it runs:** Leak count month-over-month is where the LDAR program either pays back or doesn't. If total_leaks is climbing while spend is climbing, the program is failing — and that's a vendor conversation. Watch the slope, not the latest month.

**What to look for:** Monthly trend of total_leaks across the network. The shape — flat, declining, climbing — tells you whether the LDAR contractor's optical-gas-imaging cadence is actually working.

**Land the point:** Now the director can defend the LDAR contract renewal — or terminate it — on data the contractor sees the same week we do. That's the procurement conversation that used to take six months of evidence-building.

> **Anchor moment.** Hold on the methane-tons ranking from Act 1 and the leak-count trend on screen. Take the top compressor station — call it 120 metric tons of methane per year, 40 leak events.

> *120 metric tons of methane is roughly 3,000 metric tons of CO2e at GWP 25. At the $50-150/ton social cost of carbon — call it $80/ton in a sustainability-linked-debt covenant model — that's $240K/year of carbon liability on one station. A targeted LDAR + vapor-recovery retrofit runs $300-500K. Payback inside 18 months on one station. Multiply across the top 5 stations and the conversation isn't 'can we afford LDAR' — it's 'which station gets the optical-gas-imaging crew first and which station earns full electrification in next year's AFE.'*

> That's the decision this space automates. Not the disclosure slide. The capex queue. LDAR + electrification ranked on methane tons and intensity, not on whichever facility the EH&S audit happened to visit last.

### Question (Act 2.3)

> **What is the total offset credits by emission category this year?**

**What to say while it runs:** Offset credits by emission category tells us where the residual gap is. We don't want to be the operator offsetting our way to net-zero on methane — that's a covenant-pricing risk under sustainability-linked debt. We want offsets concentrated on combustion CO2 and the gap closing on methane.

**What to look for:** Total offset_credits by emission_category YTD. The mix is the story — if methane offsets are growing, we have a structural problem the lenders will price in.

**Land the point:** That mix shows up directly in the sustainability-linked bond margin. Moving methane offsets to abatement at the source is the difference between flat coupon and a step-up trigger — and that's the CFO conversation this view actually enables.

---

## Act 3 — The commitment — locking the decarb plan and defending it to the lenders *(≈4 min)*

**Persona:** ESG / Investor Relations Lead • **Job to be done:** Defend the decarb trajectory to sustainability-linked-debt lenders and rating agencies, and lock the next-cycle reduction targets the board has to certify.

*The IR lead doesn't need another dashboard; they need the same methane and intensity numbers the EH&S director is acting on, so the lender narrative writes itself when the next covenant report comes due.*

### Question (Act 3.1)

> **Top 10 emission sources by average carbon intensity in kg per boe.**

**What to say while it runs:** Top 10 sources by average carbon_intensity_kg_boe is the IR view — these are the assets the rating agency will ask about by name in the next ESG review. We want a reduction commitment against each of them, not a portfolio-level number.

**What to look for:** Ranked table of source_name with avg_carbon_intensity over a defensible window. The top 10 names are exactly the assets the corporate sustainability report and the lender deck have to align on.

**Land the point:** When IR can cite intensity by asset name and pair it with the LDAR / electrification capex queue, the sustainability-linked-bond covenant conversation moves from 'trust us on the trajectory' to 'here's the asset-level plan' — and that's the spread compression we need.

### Question (Act 3.2)

> **Which emission categories are flagged Non-Compliant on compliance status, and what monthly CO2e do they represent?**

**What to say while it runs:** Non-Compliant emission categories with the monthly CO2e they represent is the enforcement-risk view. EPA OOOOb has real teeth and FERC will look at the same record — anything sitting in Non-Compliant for two months running needs a capex commitment before it becomes a Notice of Violation.

**What to look for:** Categories flagged Non-Compliant on compliance_status with monthly_co2e_tons attached. The tons are how we triage — high-tons, Non-Compliant is the queue topper.

**Land the point:** Triage at the EH&S desk in the morning, enforcement risk defended in the boardroom by afternoon. Same space. Same numbers. The sustainability officer's LDAR list and the IR lead's covenant story are now the same artifact — and the next debt issuance gets priced on a trajectory we can actually evidence.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — CarbonTrack Midstream — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total CO2e by facility type for the trailing 12 months.
2. Top 10 emission sources by total methane tons year-to-date.
3. Which facilities have a carbon intensity above the company average, and what is the throughput at each?
4. How has total leak count trended month-over-month across the network?
5. What is the total offset credits by emission category this year?
6. Top 10 emission sources by average carbon intensity in kg per boe.
7. Which emission categories are flagged Non-Compliant on compliance status, and what monthly CO2e do they represent?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
