1|---
2|name: engagement-logging
3|description: Use when a customer interaction update is provided. Multi-turn conversation to extract engagement details, log Activity, mark completed Tasks, and trigger deal-progressing.
4|version: 2.0.0
5|author: Leo (BD Director Agent)
6|license: MIT
7|platforms: [linux, macos, windows]
8|metadata:
9|  hermes:
10|    tags: [sales, pipeline, engagement, crm, lark-base, deal-progression]
11|    related_skills: [deal-progressing, deal-monitoring, managing-sales-pipeline]
12|---
13|
14|# Engagement Logging
15|
16|## Overview
17|
18|This skill automates the capture and logging of customer interactions into the CRM. When a user provides an update about a deal interaction, Leo enters a structured multi-turn conversation to extract:
19|
20|1. **Engagement Outcome**: How did the interaction go? (Positive / Neutral / Negative)
21|2. **Key Learnings**: What did you learn? (Business needs, technical concerns, stakeholder info, etc.)
22|3. **Next Actions**: What happens next? (Specific task, owner, timeline)
23|
24|The skill then:
25|- Creates an **Engagement record** in the Engagements table
26|- **Updates completed Tasks** to "Done" if mentioned
27|- **Auto-creates new Tasks** for follow-up actions
28|- **Triggers deal-progressing** to {{RECORD_ID}} deal status, priority, and risk
29|
30|Use this as the primary entry point for all customer interactions in your BD pipeline.
31|
32|## When to Use
33|
34|- Customer conversation, meeting, or call just happened
35|- Email exchange or message thread needs logging
36|- Internal stakeholder update about a deal
37|- Any "what happened today" interactions that move deals forward
38|- Scheduling a future meeting → create a **Planned** Engagement (Status: Planned, date = meeting date)
39|
40|## Planned vs Completed Engagements
41|
42|Engagements have two statuses:
43|- **Planned** — future meeting/call already booked. Used as trigger for meeting-prep cron (scans for Planned Engagements happening tomorrow).
44|- **Completed** — interaction already happened. Used for deal-progressing analysis.
45|
46|Planned Engagements do NOT need a Next Action filled in at creation time — that comes after the meeting.
47|
48|## Nurture Engagements (no Deal/Partnership)
49|
50|When logging a nurture outreach (check-in email, WhatsApp to a cold contact):
51|- Set Account + Contact as normal
52|- **Leave Related Deal empty** — do not link to any Deal
53|- **Leave Related Partnership empty**
54|- This keeps nurture activity out of the pipeline view
55|- Notes field: record what content/article was shared
56|
57|**Don't use for:**
58|- Internal process notes (use Tasks directly)
59|- Market research or account enrichment (separate skill)
60|- Closed deals (use invoice/contract workflows instead)
61|
62|## Data Model
63|
64|### Engagement Log Flow
65|
66|```
67|User Input
68|  ↓
69|[Extract via Multi-Turn]
70|  ├─ Engagement Outcome (Positive/Neutral/Negative)
71|  ├─ Key Learnings (text)
72|  ├─ Next Actions (text)
73|  └─ Completed Tasks (if any)
74|  ↓
75|[Create Engagement Record]
76|  └─ Engagements table ({{TABLE_ID}})
77|  ↓
78|[Update Completed Tasks]
79|  └─ Mark related Tasks as Done in 💼 Sales Tasks ({{TABLE_ID}})
80|  ↓
81|[Auto-Create Follow-up Tasks (if needed)]
82|  └─ Link to Opportunity via Tasks field
83|  ↓
84|[Trigger deal-progressing]
85|  └─ Recalculate deal state, priority, risk
86|```
87|
88|### Engagements Table Schema ({{TABLE_ID}}) — verified 2026-06-10
89|
90|| Field Name | Field ID | Type | Required | Notes |
91||---|---|---|---|---|
92|| Title | fldF2k7HxR | Text | Yes | Primary field. Format: "YYYY-MM-DD — Account (context)" |
93|| Status | fldlctLkA6 | SingleSelect | Yes | Planned / Completed |
94|| Account | fldPVkkWZn | DuplexLink | No | back-link to Accounts table |
95|| Contact | fldJYZpois | DuplexLink | No | who participated |
96|| Related Deal | fldunqTRM7 | DuplexLink | No | back-link to Deals. Leave EMPTY for Nurture engagements |
97|| Related Partnership | fldd3taDf1 | DuplexLink | No | back-link to Partnerships |
98|| Date | fldW8Gzklj | DateTime | Yes | When did this happen (ms timestamp) |
99|| Type | flddjaPI6K | SingleSelect | Yes | Phone Call / In-person Visit / Online Meeting / WhatsApp / LINE / Demo / Message / Email / Event |
100|| Notes | fld5Q9sXhJ | Text | No | Free-form notes and key learnings |
101|| Next Action | fld7UQpmkI | Text | No | What happens next |
102|| Owner | fldcKW3qqs | User | No | Who was involved |
103|
104|**Key design rule:** Engagements do NOT need to link to a Deal or Partnership. A Contact-level engagement (e.g. nurture outreach) should leave Related Deal and Related Partnership empty — this keeps it out of the pipeline views.
105|
106|### Tasks Table Integration
107|
108|When the user mentions completed tasks or next actions:
109|
110|| Field Name | Field ID | Type | Reference |
111||---|---|---|---|
112|| Title | fld2Z0Yi15 | Text | Primary field (task name) |
113|| Done | fldEBSzJLw | Checkbox | Completion flag |
114|| Deadline | fldDIaKjCR | DateTime | Due date |
115|| Business Line | fldDvd3nth | SingleSelect | [Product] / [Product] / etc. |
116|| Priority | fld0kpXg4L | SingleSelect | 🔴 High / 🟡 Medium / 🟢 Low |
117|| Responsible Person | fldbU06WCv | User | Assignee |
118|| Description | fldp3pHhSW | Text | Task details |
119|| Agent Advice | fldXvVWDRd | Text | Leo's strategic advice for this task |
120|| Related Deal | fldxTM0Op2 | DuplexLink | back-link to Opportunity |
121|| Related Partnership | flderan4Kb | DuplexLink | back-link to Partnership |
122|| Output Link | fldjiF87Cu | Url | Link to output doc/file |
123|
124|## Workflow
125|
126|### Step 1: Multi-Turn Extraction
127|
128|When user provides initial update, Leo asks clarifying questions in this order:
129|
130|```
131|Q1: "What type of interaction? (Call / Meeting / Email / Message / Other)"
132|    → Capture Engagement Type
133|
134|Q2: "How did it go? (Positive / Neutral / Negative)"
135|    → Capture Engagement Outcome
136|
137|Q3: "What was the key learning or new information?"
138|    → Capture Key Learnings
139|
140|Q4: "What happens next? Any action items?"
141|    → Capture Next Actions + Auto-create Tasks if mentioned
142|
143|Q5: "Did you complete any existing tasks today?"
144|    → Capture completed Task names → Will mark as Done
145|```
146|
147|Each response is validated and confirmed before moving to next question.
148|
149|### Step 2: Engagement Record Creation
150|
151|Build Engagement record from extracted data:
152|
153|```python
154|engagement_record = {
155|    "fields": {
156|        "Engagement Name": f"{interaction_date} — {contact_name}",
157|        "Opportunity": [opportunity_id],
158|        "Contact": [contact_id],
159|        "Engagement Type": engagement_type,  # option_id from SingleSelect
160|        "Engagement Outcome": outcome,    # option_id from SingleSelect
161|        "Key Learnings": learnings,
162|        "Next Actions": next_actions,
163|        "Engagement Date": interaction_timestamp,
164|        "Owner": [user_id],
165|        "Notes": notes_if_any
166|    }
167|}
168|```
169|
170|POST to Lark Bitable API:
171|```
172|POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
173|Path: app_token={{LARK_APP_TOKEN}}
174|       table_id={{TABLE_ID}}
175|```
176|
177|### Step 3: Task Status Updates
178|
179|For each completed task mentioned by user:
180|
181|```python
182|# 1. Query Tasks table to find matching records
183|# Filter: Opportunity = current_opportunity_id AND Task Name contains user_input
184|
185|# 2. For each match found:
186|task_update = {
187|    "fields": {
188|        "Status": "optDone"  # SingleSelect option_id for "Done"
189|    }
190|}
191|
192|# PATCH to update
193|PATCH /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
194|```
195|
196|### Step 4: Auto-Create New Tasks (if Next Actions Mentioned)
197|
198|If user describes follow-up actions, create Task records:
199|
200|```python
201|task_record = {
202|    "fields": {
203|        "Title": action_description,          # Primary field
204|        "Related Deal": [opportunity_id],     # DuplexLink
205|        "Deadline": calculated_due_date,      # DateTime (ms timestamp)
206|        "Priority": "🔴 High",               # or 🟡 Medium / 🟢 Low
207|        "Business Line": business_line,       # SingleSelect option name
208|        "Agent Advice": strategic_advice,     # Leo's advice for this task
209|        "Responsible Person": user_id,        # User field (open_id)
210|    }
211|}
212|
213|# POST to {{TABLE_ID}} (Tasks table)
214|```
215|
216|### Step 5: Trigger Deal-Progressing
217|
218|After Activity is created:
219|
220|```
221|INVOKE deal-progressing skill
222|  Input: opportunity_id, newly_created_engagement_id
223|  Output: Updated Opportunity record with:
224|    - Current Status Summary ({{RECORD_ID}})
225|    - Next Action Summary ({{RECORD_ID}})
226|    - Priority ({{RECORD_ID}})
227|    - Risk Indicator ({{RECORD_ID}})
228|    - Last Update Date (set to now)
229|```
230|
231|### Step 6: GBrain Sync
232|
233|After deal-progressing completes, sync the engagement data to GBrain so the knowledge base stays current with every customer interaction.
234|
235|**6a. Add Timeline Entry to the Account's GBrain page**
236|
237|```python
238|mcp_gbrain_add_timeline_entry(
239|    slug=f"companies/{account_slug}",   # e.g. companies/acme-corp
240|    date=engagement_date,               # YYYY-MM-DD
241|    summary=f"{engagement_type} — {engagement_outcome}",  # e.g. "Online Meeting — Positive"
242|    detail=f"Key Learnings: {key_learnings}\n\nNext Action: {next_action}",
243|    source="lark-crm"
244|)
245|```
246|
247|**6b. Extract Facts from engagement notes**
248|
249|```python
250|mcp_gbrain_extract_facts(
251|    turn_text=f"{notes}\n\n{key_learnings}",
252|    entity_hints=[f"companies/{account_slug}"]
253|)
254|```
255|
256|**6c. Update ## Recent Insights on the company page (conditional)**
257|
258|If the engagement outcome is **Negative**, OR if the notes mention a key decision, blocker, or risk, also call:
259|
260|```python
261|mcp_gbrain_put_page(
262|    slug=f"companies/{account_slug}",
263|    content=<existing_page_content_with_updated_recent_insights_section>
264|)
265|```
266|
267|Prepend a new bullet to the `## Recent Insights` section:
268|```
269|- **YYYY-MM-DD** — [one-sentence summary of the decision/blocker/negative signal]
270|```
271|
272|> **Pitfall — Always resolve the Account GBrain slug before Step 6.**
273|> Query the Account record from Lark Base to get the Company Name, then derive the slug by lowercasing, stripping punctuation, and replacing spaces with hyphens (e.g. "Acme Corp" → `companies/acme-corp`). If the GBrain page does not exist yet, create it first with `mcp_gbrain_put_page` (minimal frontmatter + empty body) before calling `mcp_gbrain_add_timeline_entry`.
274|
275|## Planned Engagements
276|
277|Engagements are not only for interactions that already happened. Use `Status: Planned` for scheduled future meetings.
278|
279|**When to create a Planned Engagement:**
280|- A meeting has been agreed and a date/time is confirmed
281|- The date is more than a day away (otherwise just log it as Completed when done)
282|
283|**Fields for Planned:**
284|- Status: `Planned`
285|- Date: the scheduled meeting time (ms timestamp)
286|- Type: Online Meeting / In-person Visit / Phone Call / Demo
287|- Notes: known context — who's attending, agenda, known concerns
288|- Next Action: what to do after the meeting
289|
290|**What happens next:**
291|- `meeting-prep-daily` cron scans for Planned Engagements happening tomorrow at 09:00 and auto-delivers a meeting brief
292|- After the meeting, update Status to `Completed` and fill in Notes with what actually happened, then trigger `deal-progressing`
293|
294|
295|
296|Required:
297|
298|```bash
299|LARK_APP_ID=<app_id>
300|LARK_APP_SECRET=<app_secret>
301|LARK_TENANT_ACCESS_TOKEN=<cached_token>  # or auto-refresh via app credentials
302|```
303|
304|Lark SDK (Python):
305|
306|```python
307|from lark_oapi import Client
308|from lark_oapi.apis.bitable_v1 import *
309|
310|client = Client.builder()
311|    .app_id(os.getenv("LARK_APP_ID"))
312|    .app_secret(os.getenv("LARK_APP_SECRET"))
313|    .build()
314|```
315|
316|## Common Pitfalls
317|
318|1. **Searching for Deal by client name keyword — will miss most records**
319|   - Deal Names in the CRM are NOT always the client name. They follow patterns like "[Client] — Odoo ERP + marketing automation" or "[Product] Malaysia Resale — [Client]". Searching `Deal Name contains "[Client]"` may return zero results even when the deal exists.
320|   - **Correct approach**: First find the Account record by `Company Name contains "X"` in the Accounts table ({{TABLE_ID}}), get the Account `record_id`, then scan all Deals and match by `Client.link_record_ids` containing that record_id.
321|   ## Common Pitfalls
322|
323|   1. **Field names must match exactly — verify before first write in a new session**
324|      - Discovered 2026-06-10: Tasks table field names differed from what was recorded (`Task Name` → `Title`, `Status` → `Done` checkbox, `Opportunity` → `Related Deal`, `Owner` → `Responsible Person`, `Due Date` → `Deadline`)
325|      - Symptom: `FieldNameNotFound` from Lark API
326|      - Fix: call `mcp_lark_bitable_v1_appTableField_list` on the target table if you get this error
327|      - Trust the Tasks Table Integration section in this skill — it reflects the verified correct names
328|
329|   2. **Not confirming contact/opportunity before logging**
330|      - Always verify: "This activity is for Deal [X] with Contact [Y], correct?"
331|      - Linking to wrong opportunity = corrupted pipeline data
332|
333|   2. **Engagement Outcome not matching user's tone**
334|      - If user says "they're interested but need budget approval", that's Neutral, not Positive
335|      - Positive = deal moved forward, commitment made
336|      - Neutral = good info gathered, but no commitment yet
337|      - Negative = deal stalled, objection raised, or NRF
338|
339|   3. **Auto-creating tasks for vague next actions**
340|      - "Follow up soon" ≠ actionable task
341|      - Always ask: "Who should do this? When? What's the specific next step?"
342|      - If user can't answer, don't create the task
343|
344|   4. **Forgetting to update completed tasks**
345|      - User might mention "I finally got sign-off on that contract review" in passing
346|      - Always ask: "Did you complete any of the outstanding tasks related to this deal?"
347|
348|   5. **Not handling multi-day interactions**
349|      - If user says "we had a series of emails back and forth over 3 days", create ONE Activity (set date to most recent)
350|      - Or ask: "Should I log this as one multi-day engagement or separate daily records?"
351|
352|   6. **Triggering deal-progressing before Activity is saved**
353|      - Always confirm Activity record created successfully (got record_id back) before triggering next skill
354|      - If API fails, ask user to retry or create manually
355|
356|   7. **Using wrong field names for Tasks table** — confirmed correct schema:
357|      - Primary field is `Title` (not "Task Name")
358|      - Completion is `Done` checkbox (not a Status select)
359|      - Link to deal is `Related Deal` (not "Opportunity")
360|      - Assignee is `Responsible Person` (not "Owner")
361|      - Due date is `Deadline` (not "Due Date")
362|      - Always check field schema before writing if unsure
363|
364|## Verification Checklist
365|
366|- [ ] User described an actual customer interaction (not internal process)
367|- [ ] Multi-turn extracted: Engagement Type, Engagement Outcome, Key Learnings, Next Actions
368|- [ ] Opportunity and Contact verified and linked
369|- [ ] Engagement record created (got record_id response from Lark API)
370|- [ ] Completed tasks marked Done (if any mentioned)
371|- [ ] New tasks auto-created with clear names and owners (if applicable)
372|- [ ] deal-progressing triggered and completed
373|- [ ] GBrain timeline entry added for related Account
374|- [ ] Facts extracted from engagement notes
375|- [ ] User received confirmation: "Engagement logged for [Deal Name]. Deal status updated."
376|
377|## Integration with Deal Monitoring
378|
379|When triggered from deal-monitoring skill (automatic escalation), follow same flow but:
380|
381|- Set Engagement Outcome to "Negative" (auto-escalation = deal at risk)
382|- Pre-populate Next Actions as "Review deal health and determine recovery strategy"
383|- Auto-create Escalation Task with higher priority
384|