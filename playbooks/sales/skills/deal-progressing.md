1|---
2|name: deal-progressing
3|description: Use when an Engagement is logged or deal state changes. Analyzes all Engagements, {{RECORD_ID}} deal status, priority, and risk, then updates Opportunity fields automatically.
4|version: 2.0.0
5|author: Leo (BD Director Agent)
6|license: MIT
7|platforms: [linux, macos, windows]
8|metadata:
9|  hermes:
10|    tags: [sales, pipeline, deal-analysis, crm, lark-base, automation]
11|    related_skills: [engagement-logging, deal-monitoring, managing-sales-pipeline]
12|---
13|
14|# Deal Progressing
15|
16|## Overview
17|
18|This skill runs after every Engagement is logged (or manually when deal status changes). It analyzes the full interaction history of a deal and {{RECORD_ID}}:
19|
20|1. **Current Status Summary** — Plain-English description of where the deal stands
21|2. **Next Action Summary** — What needs to happen next
22|3. **Priority** — High / Medium / Low / At Risk (based on deal health and momentum)
23|4. **Risk Indicator** — Low / Medium / High (based on stalled interactions, time decay, objections)
24|5. **Last Update Date** — Timestamp of {{RECORD_ID}}
25|
26|The skill is **autonomous**: it makes decisions based on objective signals (interaction frequency, outcome patterns, time elapsed), then presents {{RECORD_ID}} to the user for review before committing updates to the CRM.
27|
28|## When to Use
29|
30|- After engagement-logging completes (automatic trigger)
31|- When deal status or stage manually changes
32|- On daily automated monitoring (cron job checks all open deals)
33|- When user asks "what's the status of [Deal]?" → Real-time snapshot
34|
35|**Don't use for:**
36|- Closed deals (Won/Lost are terminal states)
37|- Initial qualification (use lead-scoring or account-onboarding instead)
38|- General pipeline reporting (use reviewing-sales-pipeline instead)
39|
40|## Data Model
41|
42|### Input: Opportunity Record
43|
44|Read from 💼 Opportunities table ({{TABLE_ID}}):
45|
46|| Field | Field ID | Purpose |
47||---|---|---|
48|| Deal Name | fldbmTAYzs | For context |
49|| Client | fldRsCk86x | Account link |
50|| Stage | fld1OpuNo4 | Current pipeline stage |
51|| Activities | fldzVENqAU | All related Engagements (read for analysis) |
52|| Tasks | fld2Fp7U7A | Related follow-up tasks |
53|| Last Update Date | fldHNxmuZ9 | Track recency |
54|| Current Status Summary | fldELp5uET | **OUTPUT** |
55|| Next Action Summary | fldODsPGAz | **OUTPUT** |
56|| Priority | fld013zURe | **OUTPUT** |
57|| Risk Indicator | fldSm89PNq | **OUTPUT** |
58|
59|### Input: Engagements Table (read only)
60|
61|From 💼 Engagements table ({{TABLE_ID}}):
62|
63|| Field | Field ID | Purpose |
64||---|---|---|
65|| Activity Date | fldDTVvJZO | Timeline |
66|| Engagement Outcome | fldCFxnmvD | Positive / Neutral / Negative |
67|| Key Learnings | fldW7KH1wt | Sentiment analysis |
68|| Activity Type | fldQk0zyJ1 | Call / Email / Meeting / Message |
69|
70|### Output: Updated Opportunity Record
71|
72|Write back to Opportunity:
73|
74|```python
75|update_payload = {
76|    "fields": {
77|        "Current Status Summary": str,      # Human-readable status
78|        "Next Action Summary": str,          # What's next
79|        "Priority": str,                     # option_id from SingleSelect
80|        "Risk Indicator": str,               # option_id from SingleSelect
81|        "Last Update Date": datetime         # Now
82|    }
83|}
84|```
85|
86|## Analysis Algorithm
87|
88|### Phase 1: Gather Signals
89|
90|```python
91|# From all Engagements for this Opportunity:
92|engagements = fetch_engagements(opportunity_id)
93|
94|signals = {
95|    "total_interactions": len(engagements),
96|    "last_interaction_date": max(e.engagement_date for e in engagements),
97|    "days_since_last_interaction": (now - last_interaction_date).days,
98|    "interaction_trend": analyze_recency_weighted(engagements),  # ↑ or ↓ or →
99|    "outcome_distribution": {
100|        "positive": count(o == "Positive"),
101|        "neutral": count(o == "Neutral"),
102|        "negative": count(o == "Negative")
103|    },
104|    "current_stage": opportunity.stage,  # Lead / Qualified / Proposal / Negotiation / Won / Lost
105|    "open_tasks": count(tasks where status != "Done"),
106|    "overdue_tasks": count(tasks where due_date < today and status != "Done"),
107|}
108|```
109|
110|### Phase 2: Score Deal Health
111|
112|```python
113|health_score = 0  # 0-100
114|
115|# Interaction frequency (0-30 points)
116|if days_since_last_interaction <= 3:
117|    health_score += 30
118|elif days_since_last_interaction <= 7:
119|    health_score += 20
120|elif days_since_last_interaction <= 14:
121|    health_score += 10
122|else:
123|    health_score += 0
124|
125|# Outcome positivity (0-40 points)
126|positive_ratio = positive_outcomes / total_interactions
127|if positive_ratio >= 0.67:
128|    health_score += 40
129|elif positive_ratio >= 0.5:
130|    health_score += 25
131|elif positive_ratio >= 0.33:
132|    health_score += 15
133|else:
134|    health_score += 0
135|
136|# Stage progression (0-20 points)
137|stage_scores = {
138|    "Lead": 5,
139|    "Qualified": 10,
140|    "Proposal": 15,
141|    "Negotiation": 18,
142|    "Won": 20,
143|    "Lost": 0
144|}
145|health_score += stage_scores[current_stage]
146|
147|# Task health (0-10 points)
148|if open_tasks == 0:
149|    health_score += 10
150|elif overdue_tasks == 0:
151|    health_score += 5
152|else:
153|    health_score += 0
154|```
155|
156|### Phase 3: Determine Priority
157|
158|```python
159|if health_score >= 80:
160|    priority = "High"
161|elif health_score >= 50:
162|    priority = "Medium"
163|elif health_score >= 25:
164|    priority = "Low"
165|else:
166|    priority = "At Risk"
167|
168|# Override: explicit signals (auto-escalation rules)
169|# — Rule 1: No activity > 7 days ALWAYS = At Risk (even if score is decent)
170|if days_since_last_interaction > 7:
171|    priority = "At Risk"
172|
173|# — Rule 2: Negotiation stage with high score = High priority (close attention)
174|if current_stage == "Negotiation" and health_score > 60:
175|    priority = "High"
176|
177|# — Rule 3: Closed deals don't get priority (terminal state)
178|if current_stage == "Won" or current_stage == "Lost":
179|    priority = None
180|```
181|
182|### Phase 4: Determine Risk
183|
184|```python
185|risk_level = "Low"  # default
186|
187|# Risk escalation rules
188|if days_since_last_interaction > 7:
189|    risk_level = "High"
190|elif days_since_last_interaction > 5:
191|    risk_level = "Medium"
192|
193|if overdue_tasks > 0:
194|    risk_level = "Medium" if risk_level == "Low" else "High"
195|
196|if negative_outcomes > 0 and current_stage not in ["Won", "Lost"]:
197|    risk_level = "Medium" if risk_level == "Low" else "High"
198|
199|if positive_outcomes == 0 and total_interactions > 3:
200|    # Many interactions but none positive = stuck deal
201|    risk_level = "High"
202|```
203|
204|### Phase 5: Generate Summaries
205|
206|```python
207|# Current Status Summary
208|if current_stage == "Won":
209|    status = f"Deal closed won. Last interaction: {last_interaction_date}."
210|elif current_stage == "Lost":
211|    status = f"Deal closed lost. Last interaction: {last_interaction_date}."
212|elif total_interactions == 0:
213|    status = "New opportunity, no interactions yet."
214|elif days_since_last_interaction > 7:
215|    status = f"⚠️ STALLED. No activity for {days_since_last_interaction} days. {outcome_distribution['positive']} positive, {outcome_distribution['negative']} negative interactions. Escalation task created."
216|else:
217|    trend = "gaining momentum" if interaction_trend == "↑" else "steady" if interaction_trend == "→" else "slowing"
218|    status = f"{current_stage} stage, {trend}. {total_interactions} interactions. Last: {last_interaction_date.format('MMM DD')}."
219|
220|# Next Action Summary
221|if current_stage == "Lead":
222|    next_action = "Qualification call scheduled. Confirm fit and budget authority."
223|elif current_stage == "Qualified":
224|    next_action = "Prepare proposal. Align on requirements with key stakeholder."
225|elif current_stage == "Proposal":
226|    if days_since_last_interaction <= 3:
227|        next_action = "Await client feedback on proposal. Follow up if no response by [date]."
228|    elif days_since_last_interaction <= 7:
229|        next_action = "Check proposal status and address any concerns. Schedule follow-up call."
230|    else:
231|        next_action = "🚨 CRITICAL: Re-engagement needed. Call or email to assess deal health and salvageability."
232|elif current_stage == "Negotiation":
233|    if days_since_last_interaction <= 3:
234|        next_action = "Negotiate terms. Key decision expected by [date]. Monitor contract status."
235|    else:
236|        next_action = "🚨 CRITICAL: Negotiation stalled. Call decision-maker to unblock and confirm timeline."
237|elif current_stage in ["Won", "Lost"]:
238|    next_action = "Deal closed. Execute next phase (invoice handoff, post-mortem, or renewal planning)."
239|else:
240|    next_action = "TBD — no stage set."
241|```
242|
243|## Implementation Notes
244|
245|### Option IDs (For Priority & Risk Indicator)
246|
247|**Priority (field_id: fld013zURe):**
248|- `optXErOsQD` = High
249|- `optLJGHG72` = Medium
250|- `optMiBa1Kx` = Low
251|- `optEWDcqFl` = At Risk
252|
253|**Risk Indicator (field_id: fldSm89PNq):**
254|- `opt6LlcNGa` = High
255|- `optUP93Toe` = Medium
256|- `optoI0jscP` = Low
257|
258|### API Update Flow
259|
260|```python
261|# 1. Build update payload
262|update = {
263|    "fields": {
264|        "Current Status Summary": status_text,
265|        "Next Action Summary": action_text,
266|        "Priority": priority_option_id,
267|        "Risk Indicator": risk_option_id,
268|        "Last Update Date": datetime.now().isoformat()
269|    }
270|}
271|
272|# 2. Submit to Lark Bitable
273|PATCH /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
274|    app_token={{LARK_APP_TOKEN}}
275|    table_id={{TABLE_ID}}
276|    record_id=<opportunity_record_id>
277|```
278|
279|## Verification Checklist
280|
281|- [ ] All Engagements for this Opportunity fetched
282|- [ ] Health score calculated (0-100)
283|- [ ] Priority determined (High / Medium / Low / At Risk)
284|- [ ] Risk Indicator determined (Low / Medium / High)
285|- [ ] Current Status Summary is human-readable and factual
286|- [ ] Next Action Summary is specific and actionable
287|- [ ] Update payload validated (no missing required fields)
288|- [ ] Opportunity record updated (got 200 response from API)
289|- [ ] User presented with proposed changes for review before commit
290|
291|## Common Pitfalls
292|
293|1. **Conflating Priority with Risk**
294|   - Priority = importance to business (which deals to work on first)
295|   - Risk = likelihood of slippage (which deals need intervention)
296|   - A high-value deal with low activity = High Priority + High Risk
297|   - A small deal with good momentum = Low Priority + Low Risk
298|
299|2. **Over-weighting recent interactions**
300|   - One good call after 2 weeks of silence doesn't mean the deal is healthy
301|   - Look at trend over time, not just last activity date
302|   - If days_since > 7, treat as at-risk regardless of one recent positive
303|
304|3. **Not accounting for stage context**
305|   - Negotiation deals have shorter acceptable silence periods (< 3 days)
306|   - Qualified leads can have longer gaps (up to 7 days is OK)
307|   - Adjust thresholds based on stage
308|
309|4. **Ignoring overdue tasks**
310|   - If a deal has open tasks overdue by > 3 days, automatically escalate risk
311|   - These are often blocker signals (waiting for contract legal review, etc.)
312|
313|5. **Setting Priority/Risk for closed deals**
314|   - Won/Lost deals are terminal; don't update Priority or Risk
315|   - Just update status to reflect closure reason
316|
317|## Tasks Table Schema ({{TABLE_ID}}) — Correct Field Names
318|
319|| Field Name | Field ID | Type | Notes |
320||---|---|---|---|
321|| Title | fld2Z0Yi15 | Text | Primary field (task name) |
322|| Done | fldEBSzJLw | Checkbox | true = completed |
323|| Deadline | fldDIaKjCR | DateTime | ms timestamp |
324|| Business Line | fldDvd3nth | SingleSelect | [Product] / [Product] / etc. |
325|| Priority | fld0kpXg4L | SingleSelect | 🔴 High / 🟡 Medium / 🟢 Low |
326|| Responsible Person | fldbU06WCv | User | open_id |
327|| Description | fldp3pHhSW | Text | |
328|| Agent Advice | fldXvVWDRd | Text | Leo's strategic advice |
329|| Related Deal | fldxTM0Op2 | DuplexLink | back-link to Deals table |
330|| Related Partnership | flderan4Kb | DuplexLink | back-link to Partnership table |
331|
332|## Daily Monitoring & Escalation
333|
334|This skill supports two modes:
335|
336|### Mode 1: Event-driven (after Engagement logged)
337|- User logs an engagement via engagement-logging skill
338|- deal-progressing runs automatically to update deal status
339|- Results pushed to Opportunity record
340|
341|### Mode 2: Scheduled batch (daily automated check)
342|- Daily cron job runs at 07:00 Taiwan time
343|- Fetches all open Opportunities (Stage ≠ Won/Lost)
344|- For each deal:
345|  - Invokes deal-progressing to calculate health
346|  - If days_since_last_interaction > 7:
347|    - Sets Priority to "At Risk"
348|    - Creates Escalation Task (subject: [ESCALATION] {Deal Name} — {N} days no activity)
349|    - Task due date: Tomorrow (forces immediate review)
350|    - Task owner: Same as Opportunity owner
351|  - Updates Opportunity record
352|- Sends summary report to Sales Lark channel
353|
354|**Example Daily Report**:
355|```
356|📊 Deal Health Check — 2026-06-11 07:05
357|
358|Open Deals: 47
359|Stalled (>7 days): 3
360|Escalated to At Risk: 3
361|
362|❌ Acme Corp ([Product]) — 9 days
363|❌ TechStart AI ([Product]) — 11 days
364|❌ Global Logistics (Data) — 8 days
365|
366|Check Tasks for re-engagement actions.
367|```
368|