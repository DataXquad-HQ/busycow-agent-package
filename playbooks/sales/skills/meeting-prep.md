1|---
2|name: meeting-prep
3|description: Use when preparing for a scheduled meeting with a prospect or client. Can be triggered manually ("幫我準備明天的會議") or automatically by cron. Scans Planned Engagements, pulls Deal + Account context, and generates a focused meeting brief.
4|version: 2.0.0
5|author: Leo (BD Director Agent)
6|license: MIT
7|metadata:
8|  hermes:
9|    tags: [sales, meetings, preparation, leo-bd]
10|    related_skills: [deal-advisory, follow-up-email, engagement-logging]
11|---
12|
13|# Meeting Prep
14|
15|## When to Use
16|
17|**Manual trigger:**
18|- Hunter says "幫我準備明天的會議"、"prep for [Client]"、"meeting prep"
19|- Any confirmed meeting in the next 1–7 days
20|
21|**Automatic trigger (via cron):**
22|- Daily 9:00 AM — scan for Planned Engagements happening tomorrow
23|- If none found → stay silent
24|- If found → generate brief and deliver to Feishu
25|
26|## Two Modes
27|
28|### Mode A: Specific Meeting
29|Hunter names a specific meeting or deal. Leo fetches that Engagement + Deal + Account and generates the brief.
30|
31|### Mode B: Tomorrow Scan (cron or "幫我準備明天的")
32|Leo scans Engagements table for all Planned meetings tomorrow, generates one brief per meeting.
33|
34|---
35|
36|## Step 1: Find the Engagement(s)
37|
38|### Mode A — specific meeting
39|Search Engagements table ({{TABLE_ID}}) by deal name or account name mentioned by Hunter.
40|
41|### Mode B — tomorrow scan
42|Calculate tomorrow's date range (UTC+8):
43|- start_ts = tomorrow 00:00:00 in ms
44|- end_ts = tomorrow 23:59:59 in ms
45|
46|Query Engagements table:
47|- Status = "Planned"
48|- Date >= start_ts AND Date <= end_ts
49|
50|Fields to fetch: Title, Date, Type, Notes, Next Action, Account, Related Deal, Contact
51|
52|**If no Planned Engagements found → silent. Do not output anything.**
53|
54|---
55|
56|## Step 2: For Each Engagement, Pull Context
57|
58|**From Deals table ({{TABLE_ID}}):**
59|- Deal Name, Stage, Current Status Summary, Next Action Summary, Priority, Health Check, Business Line
60|
61|**From Accounts table ({{TABLE_ID}}):**
62|- Company Name, Description, Country, Industry, Enrichment Overview
63|
64|**From Engagements table — past Completed engagements for same deal:**
65|- Last 2–3 interactions: Date, Type, Notes
66|- This gives context: what happened before, what was discussed
67|
68|---
69|
70|## Step 3: Classify Meeting Type
71|
72|Based on Deal Stage + Engagement Notes, classify:
73|
74|| Stage | Typical Meeting Type |
75||-------|---------------------|
76|| Lead | Discovery Call |
77|| Qualified | Solution Presentation |
78|| Proposal | Demo / Proposal Review |
79|| Negotiation | Objection Handling / Executive Alignment |
80|
81|Override if Engagement Notes or Type suggests otherwise (e.g., Type = "Demo" → always Solution Presentation format).
82|
83|---
84|
85|## Step 4: Generate Brief
86|
87|Output format (繁體中文):
88|
89|```
90|📅 明日會議準備 — [Deal Name]
91|
92|【會議資訊】
93|時間：[Date + Time]
94|類型：[Engagement Type]
95|對象：[Account Name]
96|出席：[Who's attending if known]
97|Deal 階段：[Stage]
98|
99|【背景】
100|[2–3 句：這個 deal 目前在哪裡、上次互動發生了什麼、客戶核心疑慮是什麼]
101|
102|【這次目標】
103|[一句話：這次會議結束後，成功長什麼樣子]
104|
105|【三個必打點】
106|① [最重要的 talking point + 為什麼]
107|② [第二點]
108|③ [第三點]
109|
110|【預期異議 & 應對】
111|❓ [預期異議 1]
112|→ [應對話術]
113|
114|❓ [預期異議 2（如有）]
115|→ [應對話術]
116|
117|【會後立刻要做的事】
118|- [Next action 1]
119|- [Next action 2]
120|
121|【成功標準】
122|- [ ] [Checkbox 1]
123|- [ ] [Checkbox 2]
124|- [ ] [Checkbox 3]
125|```
126|
127|---
128|
129|## Output Delivery
130|
131|- **Manual trigger:** Reply directly in the conversation
132|- **Cron trigger:** Deliver to origin Feishu chat
133|- **Multiple meetings tomorrow:** One brief per meeting, separated by `---`
134|- **No meetings found (Mode B):** Silent — do not send anything
135|
136|## Where Briefs Are Stored
137|
138|**Briefs are NOT archived.** Their lifecycle ends after the meeting. The meeting outcome goes into the Engagement Notes field (Status: Completed), not back into the brief. Do not create a document, save to GBrain, or attach to the Deal record.
139|
140|---
141|
142|## Pitfalls
143|
144|1. **Brief 不需要存檔** — 用完就沒有生命週期了。開完會的結果記在 Engagement Notes，不是在 brief 裡。
145|
146|2. **Mode B 找不到 Planned Engagement 就靜默** — 不要發「今天沒有會議」這種訊息，那是噪音。
147|
148|3. **出席者很重要** — 如果知道股東會出席（不只窗口），talking points 要針對決策者設計，不是針對窗口。
149|
150|4. **不要重複上次說過的話** — 先看 past Engagements，避免在 brief 裡建議 Hunter 說他上次已經說過的東西。
151|
152|5. **目標只有一個** — 不要列三個目標。一次會議一個清楚的 ask，否則什麼都推不動。
153|