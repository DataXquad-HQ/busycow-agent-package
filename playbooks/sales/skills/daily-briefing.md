1|---
2|name: daily-briefing
3|description: Generate and format daily action briefing for BD team. Pulls At-Risk deals and today's due tasks, organizes by priority, sends to Lark group chat.
4|version: 1.0.0
5|author: Leo (BD Director Agent)
6|license: MIT
7|platforms: [linux, macos, windows]
8|metadata:
9|  hermes:
10|    tags: [sales, briefing, automation, crm, lark-base, lark-im]
11|    related_skills: [deal-progressing, managing-sales-pipeline]
12|---
13|
14|# Daily Briefing
15|
16|## Overview
17|
18|This skill runs every morning at 08:00 Taiwan time (via cron job). It generates a human-friendly action briefing for the BD team by:
19|
20|1. **Reading overnight diagnostics** — All At-Risk deals and partnership flags created by 03:00 health checks
21|2. **Querying tasks** — All tasks due TODAY (regardless of category)
22|3. **Organizing** — Priority order: At-Risk Deals → Today's Due Tasks
23|4. **Formatting** — Clean, scannable Lark message
24|5. **Sending** — Posted to Sales/BD group chat at exactly 08:00
25|
26|**No computation**: The skill only reads CRM data (already processed by health checks at 03:00) and formats it. This keeps the briefing fast and reliable.
27|
28|## When to Use
29|
30|- **Scheduled**: Daily cron job (08:00 Taiwan time) — autonomous
31|- **Manual**: Run on-demand if you want to see today's priorities outside the scheduled time
32|
33|Don't use for:
34|- Deal analysis (use deal-progressing instead)
35|- Partnership deep-dives (use daily-partnership-health-check instead)
36|- Historical reporting (use reviewing-sales-pipeline instead)
37|
38|## Data Model
39|
40|### Input: Read-Only
41|
42|#### Opportunities Table ({{TABLE_ID}})
43|
44|Query for all deals where:
45|- `Stage` ≠ "Won" AND ≠ "Lost" (open deals only)
46|- `Risk Indicator` = "High" (at-risk flag set by 03:00 health check)
47|
48|Return fields:
49|| Field | Purpose |
50||---|---|
51|| Deal Name | Title |
52|| Client | Account name |
53|| Risk Indicator | Risk level (already computed) |
54|| Priority | Priority level (already computed) |
55|| Last Update Date | For context (e.g., "Last updated 2h ago") |
56|| Next Action Summary | Action to take today |
57|
58|#### Tasks Table ({{TABLE_ID}})
59|
60|Query for all tasks where:
61|- `Due Date` = TODAY
62|- `Status` ≠ "Done" (open tasks only)
63|- `Assigned To` = Anyone (not filtered; show all team's tasks)
64|
65|Return fields:
66|| Field | Purpose |
67||---|---|
68|| Task Name | Title |
69|| Due Date | Confirm it's today |
70|| Status | Current state (Pending, In Progress, etc.) |
71|| Assigned To | Who owns it |
72|| Priority | Task priority (if available) |
73|
74|### Output: Lark Message
75|
76|Send formatted message to Sales/BD group chat:
77|
78|```
79|🎯 Daily Briefing — 2026-06-11
80|
81|⚠️ At Risk Deals (Need Action Today)
82|  • Acme Corp ([Product]) — 9d since last contact — Call to re-engage
83|  • TechStart AI ([Product]) — Awaiting proposal response (due today)
84|
85|📋 Tasks Due Today
86|  • Follow up with Acme on contract terms @leo
87|  • Prepare [Product] demo for Global Logistics @maya
88|  • Send invoice to Acme Corp @hunter
89|
90|---
91|Generated at 08:00 • Powered by Leo BD Agent
92|```
93|
94|## Algorithm
95|
96|```python
97|# 1. Fetch At-Risk Deals
98|at_risk_deals = fetch_from_lark(
99|    table_id="{{TABLE_ID}}",
100|    fields=["Deal Name", "Client", "Next Action Summary", "Last Update Date"],
101|    filter='fields."Risk Indicator" = "High" AND fields."Stage" != "Won" AND fields."Stage" != "Lost"'
102|)
103|
104|# 2. Fetch Today's Due Tasks
105|today = datetime.now().date()
106|due_tasks = fetch_from_lark(
107|    table_id="{{TABLE_ID}}",
108|    fields=["Task Name", "Due Date", "Status", "Assigned To", "Priority"],
109|    filter=f'fields."Due Date" = {today.isoformat()} AND fields."Status" != "Done"'
110|)
111|
112|# 3. Sort & Limit
113|at_risk_deals.sort_by("Last Update Date", reverse=True)  # Oldest first (most urgent)
114|due_tasks.sort_by("Priority")  # High priority first
115|
116|# 4. Format Lark message
117|briefing = format_briefing(at_risk_deals, due_tasks)
118|
119|# 5. Send to group chat
120|send_to_lark_chat(
121|    chat_id=SALES_BD_GROUP_CHAT_ID,
122|    message=briefing
123|)
124|```
125|
126|## Message Format
127|
128|Use this exact format for clarity:
129|
130|```markdown
131|🎯 Daily Briefing — {DATE}
132|
133|⚠️ At Risk Deals (Need Action Today)
134|{if at_risk_deals:
135|  • {Deal Name} ({Account}) — {Days since update} — {Next Action Summary}
136|  • ...
137|else:
138|  No deals at risk. Good day ahead! ✨
139|}
140|
141|📋 Tasks Due Today
142|{if due_tasks:
143|  • {Task Name} @{Owner}
144|  • ...
145|else:
146|  No tasks due today.
147|}
148|
149|---
150|Generated at 08:00 • Powered by Leo BD Agent
151|```
152|
153|**Style notes**:
154|- Use emoji for visual scanning (⚠️, 📋)
155|- Keep deal descriptions to one line
156|- Use @mentions for task owners (Lark will highlight them)
157|- Always include timestamp (shows when briefing was generated)
158|
159|## Implementation Notes
160|
161|### Lark Base Query
162|
163|Use lark-oapi SDK to query Opportunities and Tasks tables:
164|
165|```python
166|from lark_oapi import Client
167|from lark_oapi.service.bitable.v1 import *
168|
169|client = Client.builder() \
170|    .app_id(LARK_APP_ID) \
171|    .app_secret(LARK_APP_SECRET) \
172|    .build()
173|
174|# Query at-risk deals
175|deal_request = SearchAppTableRecordRequest.builder() \
176|    .app_token("{{LARK_APP_TOKEN}}") \
177|    .table_id("{{TABLE_ID}}") \
178|    .filter('fields."Risk Indicator" = "High"') \
179|    .page_size(100) \
180|    .build()
181|
182|deal_response = client.bitable.v1.appTableRecord.search(deal_request)
183|deals = deal_response.data.items
184|```
185|
186|### Lark IM Send
187|
188|Use Lark IM API to post message:
189|
190|```python
191|from lark_oapi.service.im.v1 import *
192|
193|message_request = CreateMessageRequest.builder() \
194|    .receive_id_type("chat_id") \
195|    .receive_id(SALES_BD_GROUP_CHAT_ID) \
196|    .msg_type("text") \
197|    .content(json.dumps({
198|        "text": briefing_message
199|    })) \
200|    .build()
201|
202|response = client.im.v1.message.create(message_request)
203|```
204|
205|### Environment Variables
206|
207|- `LARK_APP_ID` — Lark app ID
208|- `LARK_APP_SECRET` — Lark app secret
209|- `SALES_BD_GROUP_CHAT_ID` — Target group chat ID (get from Lark URL or API)
210|
211|## Verification Checklist
212|
213|- [ ] Connected to Lark Base
214|- [ ] At-Risk deals fetched (filter by Risk Indicator = High)
215|- [ ] Today's due tasks fetched (filter by Due Date = today and Status ≠ Done)
216|- [ ] Deals sorted by recency (oldest updates first)
217|- [ ] Tasks sorted by priority
218|- [ ] Message formatted cleanly
219|- [ ] Lark IM API response successful (got 200 OK)
220|- [ ] Message posted to correct group chat
221|
222|## Common Pitfalls
223|
224|1. **Querying all deals instead of filtering by Risk = High**
225|   - This bloats the briefing and makes it useless
226|   - Only show At-Risk deals (already flagged by health check)
227|
228|2. **Including completed tasks (Status = Done)**
229|   - Filter them out
230|   - Only show open tasks
231|
232|3. **Showing tasks from past days**
233|   - Strictly: Due Date = TODAY only
234|   - Don't include overdue tasks (those should be shown separately in escalation)
235|
236|4. **Forgetting to use @mentions for task owners**
237|   - Use @open_id format so Lark highlights them
238|   - Makes it clear who needs to take action
239|
240|5. **Posting to wrong chat**
241|   - Verify SALES_BD_GROUP_CHAT_ID before deploying
242|   - Test with small group first (ask for feedback on format)
243|
244|6. **No timezone handling**
245|   - All times should be in Taiwan timezone (UTC+8)
246|   - Verify datetime.now() is using correct TZ
247|
248|## Cron Integration
249|
250|**Schedule**: Every day at 08:00 Taiwan time
251|**Frequency**: `0 8 * * *` (cron expression)
252|
253|**Dependencies**:
254|- `daily-deal-health-check` must complete before this (runs at 03:00)
255|- `daily-partnership-health-check` should complete before this (runs at 03:00)
256|
257|**Next scheduled run**: [auto-filled by cron system]
258|**Delivery**: Lark message to Sales/BD group chat
259|
260|## Sample Output
261|
262|```
263|🎯 Daily Briefing — 2026-06-11
264|
265|⚠️ At Risk Deals (Need Action Today)
266|  • Acme Corp ([Product]) — 9d ago — Call VP Engineering to unblock proposal
267|  • TechStart AI ([Product]) — Proposal due today — Check if feedback arrived, follow up if not
268|  • Global Logistics (Data) — 11d ago — Re-engagement call needed (was awaiting pricing)
269|
270|📋 Tasks Due Today
271|  • Prepare contract addendum for Acme @leo
272|  • Send demo video link to TechStart @maya
273|  • Invoice Global Logistics @hunter
274|
275|---
276|Generated at 08:00 • Powered by Leo BD Agent
277|```
278|