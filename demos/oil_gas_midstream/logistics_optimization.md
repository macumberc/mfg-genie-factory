# PipeRoute Midstream — Demo Script

**Space:** Oil & Gas Midstream — PipeRoute Midstream - Logistics Optimization 🚚
**Runtime:** ~15 minutes • 7 questions
**Audience:** VP Pipeline Operations + COO, Commercial Director, Network Planning Lead
**KPIs touched:** Throughput, Pipeline utilization, Tariff capture, On-time delivery, Pressure, Logistics event count & severity
**Big decision automated:** How to rebalance the network — which underutilized segments to remarket or idle, which segments earn the next compressor / pump-station capex, and which shippers we move from rail to pipeline before next contract season.

---

## Pre-demo checklist

- Open the Genie space `PipeRoute Midstream - Logistics Optimization 🚚`.
- Confirm the SQL warehouse is **warm** — first-query latency is the only thing that flattens the opener.
- Click the SQL panel once and close it, so you know where it is when someone asks "is it making this up?"
- Have one customer-specific opener ready: *"Last week your team mentioned [their actual pain]. Watch what happens when that becomes a one-line question."*

---

## Scenario framing (60 seconds, verbal)

> PipeRoute Midstream runs 20 segments across crude, refined products, and natural gas systems serving multiple basins and Gulf Coast markets. Today the daily throughput lives in the SCADA historian extract, the unplanned-event log lives in the integrity team's incident workbook, and the tariff capture and on-time-delivery numbers live in the Commercial Director's monthly shipper report. Three workbooks, same pipes — and the segment-investment ranking, the contract-season pitch to shippers, and the unplanned-downtime root-cause review all get built from three different views of the same network. This space ends that. One governed surface where throughput_bpd, capacity_utilization_pct, revenue_impact_usd, and on_time_delivery_pct line up by segment — so the capex queue and the shipper pitch are built from the same dollars.

---

## Key KPIs in scope

- Throughput (bpd) — primary volumetric driver of tariff revenue
- Pipeline utilization (%) — healthy contracted lines run ~85-95%
- Tariff capture ($/bbl) — benchmark $0.50-$3.00/bbl depending on basin
- On-time delivery (%) — shipper-facing reliability metric (target >97%)
- Pressure (psi) — integrity and flow assurance indicator
- Logistics event count & severity — unplanned downtime exposure
- Volume impact (bbl) & revenue impact ($) per event
- Segment status mix (Operating / Restricted / Maintenance / Idle)

---

## Acronyms & domain terms

*Quick reference for the room — read these once before you start. Industry-specific terms appear in the questions and KPI definitions.*

| Term | Meaning |
| --- | --- |
| **KPI** | Key Performance Indicator |

---

## Act 1 — The signal — which segments are leaking revenue and which are running full *(≈4 min)*

**Persona:** Pipeline Operations VP • **Job to be done:** Surface the segments and pipeline types that drove throughput and revenue erosion in the last 6 months, before the contract-season planning cycle starts.

*This is the moment the next year's segment investment narrative starts to form. Two questions in, the VP has the throughput trend and the revenue-impact ranking that used to take a quarter of cross-system reconciliation.*

### Question (Act 1.1)

> **Show monthly total throughput in bpd by pipeline type for the trailing 12 months.**

**What to say while it runs:** Monthly throughput by pipeline type — crude vs. products vs. gas — is the demand-vs-supply view. Healthy contracted lines run 85-95% utilization; anything trending flat or down for two quarters is either a producer-side dropoff or a competitor pipeline winning share, and the response is different in each case.

**What to look for:** Monthly bars of avg_throughput_bpd by pipeline_type over 12 months — DATE_TRUNC('month', reading_date) shape. The room should notice which pipeline type is the steady earner and which is the volatile one.

**Land the point:** Now the Ops VP walks into the planning offsite with the demand picture already framed — and the conversation that used to start 'show me throughput trends' starts 'here's where we expand and here's where we idle.'

### Question (Act 1.2)

> **Top 10 segments by total revenue impact from logistics events over the last 6 months.**

**What to say while it runs:** Top 10 segments by total revenue_impact_usd from logistics events over the last 6 months is the unplanned-downtime story. Pipelines don't lose money on the days they run — they lose it on the days they don't. Revenue impact ranks segments by dollars, not by event count, which is the right way to triage integrity capex.

**What to look for:** Ranked table of segment_name with total_revenue_impact_usd. The top 3 segments typically own 50%+ of the revenue impact — those are the integrity-capex candidates that actually move the financial result.

**Land the point:** That list used to take a quarter to assemble across the historian, the incident log, and the commercial reconciliation. Now it's a question — and the integrity capex queue gets built on dollars, not on the loudest engineer's email.

---

## Act 2 — The decision — pipe, rail, or truck mix and which segments earn capex *(≈4 min)*

**Persona:** Commercial Director • **Job to be done:** Decide which underutilized segments to remarket or idle and which shippers to move from rail to pipeline ahead of contract season.

*Three questions that turn the throughput view into a contract-season strategy and a capex allocation. The middle question is the anchor — the tariff-capture-to-dollars math that converts an ops view into a commercial decision.*

### Question (Act 2.1)

> **Which segments are currently running below 70% capacity utilization, and what is the tariff on each?**

**What to say while it runs:** Segments below 70% capacity_utilization with their tariff_usd_bbl is the slack-capacity view. Below 70% on a contracted line means either we're under-marketing the segment or the shipper base has migrated — and the tariff number tells us whether re-marketing this segment is worth a commercial campaign or whether it should go on the idle list.

**What to look for:** Table of segment_name with capacity_utilization_pct and tariff_usd_bbl filtered below 70%. High-tariff, low-utilization segments are remarketing candidates; low-tariff, low-utilization segments are idle candidates.

**Land the point:** That filter used to take a back-and-forth between Ops and Commercial. Now the Director sees both sides in one view — and the segment-by-segment 'remarket vs. idle' decision becomes the input to the contract-season campaign.

### Question (Act 2.2)

> **How has average tariff $/bbl trended month-over-month across crude vs. refined products?**

**What to say while it runs:** Average tariff $/bbl trended month-over-month for crude vs. refined is the pricing-power view. Crude tariffs usually run $0.50-$2.00/bbl; refined-products tariffs run higher with demand charges. If our crude tariff is declining while basin volumes are stable, we're losing pricing power to a competing pipe.

**What to look for:** Monthly trend of avg_tariff by pipeline_type. The slope between crude and refined is the story — divergent slopes signal competitive dynamics we have to either match or differentiate against.

**Land the point:** When the Director can see tariff trend by commodity in one place, the next shipper renegotiation walks in with the pricing-power picture already on the wall — and that's the difference between defending a tariff cut and proposing a tariff floor.

> **Anchor moment.** Hold on the revenue-impact ranking from Act 1 and the under-70%-utilization table on screen. Take the worst segment — call it 200,000 bpd of avg throughput on a 350,000 bpd line, $1.20/bbl tariff, 45 days of cumulative unplanned downtime over the last year.

> *150,000 bpd of slack capacity at $1.20/bbl tariff is $180K/day, or roughly $65M/year of theoretical incremental tariff revenue if we filled the line. Cut that to a realistic remarketing recovery of 30% and it's still ~$20M/year. Meanwhile, 45 days of downtime at the contracted 350,000 bpd × $1.20 = $19M of pure revenue loss. A targeted compressor or pump-station upgrade runs $8-15M and historically takes downtime from 45 days to under 10. Payback inside a year on one segment. Across the top 3 revenue-impact segments, that's $40-60M/year of recoverable tariff — and that's the AFE conversation.*

> That's the decision this space automates. Not the monthly KPI deck. The network rebalance. Remarketing, idling, and capex queues get built on dollars and utilization at the same time, not in separate meetings that never reconcile.

### Question (Act 2.3)

> **Which pipeline types have the highest event severity mix this quarter?**

**What to say while it runs:** Pipeline types with the highest event severity mix this quarter is the integrity-risk view. Severity drives both the cost of remediation and the regulatory escalation risk — High severity events on crude segments aren't the same conversation as Medium events on refined.

**What to look for:** Pipeline_type with the severity distribution. The shape of the mix — what fraction is High vs. Medium vs. Low — is what determines whether the integrity-capex case is regulatory or pure-economic.

**Land the point:** That mix tells the Director whether the next segment capex pitches as integrity-driven (regulatory) or commercial-driven (revenue) — and that framing changes who signs the AFE and how fast it gets approved.

---

## Act 3 — The commitment — locking the network plan and the shipper book *(≈4 min)*

**Persona:** COO • **Job to be done:** Defend the network capex plan to the board and lock the next-cycle shipper-contract framework with Commercial and Operations aligned.

*The COO doesn't need a third dashboard; they need the same throughput, OTD, and revenue-impact numbers the Ops and Commercial teams are running on, so the board capex pitch and the shipper-contract framework are built off one source.*

### Question (Act 3.1)

> **Top 10 segments by total volume impact from unplanned events year-to-date.**

**What to say while it runs:** Top 10 segments by total volume_impact_bbl from unplanned events YTD is the integrity-priority view. Volume impact is the OTD story the shippers actually feel — and OTD penalties show up in the contract renewals if we don't fix it.

**What to look for:** Ranked table of segment_name with total_volume_impact_bbl. The top 5 are exactly the segments where the next integrity-program dollar earns the most contract-renewal goodwill.

**Land the point:** When the COO can pair the integrity priority list with the upcoming shipper renewals, the capex argument lands with both the CFO (who wants returns) and the Commercial team (who wants a clean renewal pitch). Same numbers, both audiences.

### Question (Act 3.2)

> **How has on-time delivery percentage trended monthly across the network?**

**What to say while it runs:** On-time delivery trended monthly across the network is the shipper-facing reliability story. Investment-grade midstream targets above 97%. Anything trending below that is a contract-renewal liability, and the slope is what shippers ask about during the negotiation.

**What to look for:** Monthly trend of on_time_delivery_pct. A flat-to-rising line above 97% is what we want to put in front of the top 3 shippers before contract season.

**Land the point:** Triage in the integrity meeting at 8 AM, contract-season planning by afternoon, board capex pitch by Friday. Same space. Same numbers. The Ops VP's segment list and the Commercial Director's shipper deck and the COO's board narrative are now the same artifact.

---

## Strategic close (~60 seconds)

Three things to lock in before you stop sharing your screen:

1. **One governed source of truth.** Unity Catalog governs the underlying data; metric views standardize the KPI definitions. When the executive and the practitioner both ask about the same KPI, they get the same number.
2. **Conversational, not dashboard sprawl.** Every chart in this demo was generated by a question. The next question — the one they haven't asked yet — is also a one-liner. No BI ticket. No two-week wait.
3. **Time-to-question equals time-to-answer.** The first hour of the morning, recovered. Monthly review prep, recovered. Capex prioritization, sharpened.

**Soft CTA:**

> "This is one space — PipeRoute Midstream — built in days. Now picture the same shape across your other use cases: same governance, same conversational entry point, same team behind it. That's the conversation we should have next."

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

1. Show monthly total throughput in bpd by pipeline type for the trailing 12 months.
2. Top 10 segments by total revenue impact from logistics events over the last 6 months.
3. Which segments are currently running below 70% capacity utilization, and what is the tariff on each?
4. How has average tariff $/bbl trended month-over-month across crude vs. refined products?
5. Which pipeline types have the highest event severity mix this quarter?
6. Top 10 segments by total volume impact from unplanned events year-to-date.
7. How has on-time delivery percentage trended monthly across the network?

**Three "land the point" beats not to miss:** the Act 1 triage moment (morning-Excel-ritual → seconds), the Act 2 anchor (loss/deferred KPI × unit value = real money), the Act 3 governance moment (one definition across teams).
