1|---
2|name: lead-nurturing
3|description: Identify contacts with no active Deal or Partnership who haven't been engaged in 30+ days, draft personalised nurture messages (email or WhatsApp), and log the outreach as a Contact-level Engagement. Triggered manually or by monthly cron. Runs in Basic mode (no article) by default; Content Engine mode activates when a table token is provided.
4|version: 1.1.0
5|author: Leo (BD Director Agent)
6|metadata:
7|  hermes:
8|    tags: [sales, nurturing, crm, contacts, lark-base]
9|    related_skills: [engagement-logging, capturing-sales-intel, managing-sales-pipeline]
10|---
11|
12|# Lead Nurturing
13|
14|## What This Skill Does
15|
16|For every Contact in the CRM who currently has no active Deal or Partnership — send a personalised check-in message at least once a month.
17|
18|Not broadcast marketing. One-to-one personal outreach.
19|
20|**Rule:** If there is no active Deal right now AND the last engagement was 30+ days ago → that contact needs a nurture message.
21|
22|## Two Modes
23|
24|**Mode A — Manual (specific contact)**
25|Sales rep says "send a check-in to [name]" → Leo drafts the message for that contact.
26|
27|**Mode B — Monthly scan (cron)**
28|Every 1st of the month: scan all qualifying contacts, generate a batch of draft messages, deliver to the sales rep for review and send.
29|
30|---
31|
32|## Detection Logic
33|
34|A Contact qualifies for nurturing when ALL of these are true:
35|
36|1. **No active Deal** — contact's linked Deals have no record with Stage ≠ Won/Lost
37|2. **No active Partnership** — contact's linked Partnerships have no active record
38|3. **No engagement in 30+ days** — last Engagement Date for this contact is >30 days ago, or no Engagement record exists at all
39|
40|---
41|
42|## CRM Schema Reference
43|
44|### Contacts table ({{TABLE_ID}})
45|| Field | Notes |
46||-------|-------|
47|| Full Name | Contact name |
48|| 💼 Clients | Linked Account |
49|| 💼 Deals | Linked Deals (used to check for active deal) |
50|| 💼 Activities | Linked Engagements (used to check last interaction date) |
51|| Preferred Channel | Email / WhatsApp / LINE |
52|| Notes / Background | Background, last conversation topics, personal details |
53|
54|### Engagements table ({{TABLE_ID}}) — how to log nurture outreach
55|- Account: linked Account
56|- Contact: linked Contact
57|- **Related Deal: leave EMPTY** — do not link to a Deal; keeps nurture out of the pipeline view
58|- **Related Partnership: leave EMPTY**
59|- Type: Email / WhatsApp / LINE
60|- Status: Completed (after sending)
61|- Title: `[YYYY-MM-DD] — Nurture — [Contact Name]`
62|- Notes: what was sent, which article was included (URL)
63|
64|---
65|
66|## Step 1: Find Contacts to Nurture
67|
68|### Mode A
69|Query Contacts table directly by the name given by the sales rep.
70|
71|### Mode B (monthly scan)
72|1. Fetch all Contacts from {{TABLE_ID}}
73|2. For each Contact:
74|   - Check linked Deals — skip if any has Stage ≠ Won/Lost
75|   - Check linked Partnerships — skip if any is active
76|   - Check linked Engagements — get the most recent Date
77|   - If last Date > 30 days ago (or no Engagements) → add to nurture list
78|
79|---
80|
81|## Step 2: Pull Contact Context
82|
83|For each contact to nurture, collect:
84|- Name, company, role
85|- Last interaction date + summary (from most recent Engagement Notes)
86|- Personal background from Contact Notes (industry, interests, topics discussed before)
87|- Preferred Channel
88|
89|---
90|
91|## Step 3: Select Article — Two Modes
92|
93|### Mode 1 — Basic (default, no Content Engine)
94|
95|**Activate when:** no Content Engine table token has been provided by the user.
96|
97|Skip article selection entirely. Draft a pure check-in message with no article link.
98|
99|Message focus:
100|- **Personalised greeting** referencing the last interaction or the contact's background (industry, role, topics discussed before)
101|- **One genuine question or observation** relevant to their industry or role — something that shows you've been paying attention, not a generic opener
102|- **Light CTA** — coffee chat, quick call, a simple "would love to reconnect" — no hard sell
103|
104|See [Basic mode templates](#basic-mode-no-article) below.
105|
106|---
107|
108|### Mode 2 — With Content Engine (future)
109|
110|**Activate when:** the user provides a Content Engine Lark Base table token.
111|
112|See [`references/content-engine-integration.md`](references/content-engine-integration.md) for full integration plan and status.
113|
114|Fetch the 3 most recent articles (Ghost link + website link). Select the most relevant one based on the contact's industry, role, and interests.
115|
116|Selection criteria:
117|- Relevant to the contact's industry or known pain point
118|- Not an article already sent to this contact (check Engagement Notes for the URL)
119|- Prefer the most recently published
120|
121|**If no suitable article exists:** fall back to Basic mode. Do not force an irrelevant link.
122|
123|---
124|
125|## Step 4: Draft the Message
126|
127|### Principles
128|- **One-to-one tone** — reads like a personal note, not a newsletter
129|- **Specific hook** — mention the last conversation, something they said, or a topic relevant to them
130|- **Article is secondary, not the opener** — (Content Engine mode only) greet first, then introduce the article naturally
131|- **Short** — email ≤150 words, WhatsApp ≤80 words
132|- **Open ending** — no hard sell; close with a light question or invitation
133|
134|---
135|
136|### Basic mode (no article)
137|
138|#### Email — Basic
139|```
140|Subject: [personalised — reflects the check-in context, not "just checking in"]
141|
142|Hi [Name],
143|
144|[1–2 sentences: personalised greeting referencing the last interaction, something they mentioned, or a relevant observation about their industry/role]
145|
146|[1 sentence: genuine question or observation relevant to their world — shows you've been paying attention]
147|
148|[Light CTA — e.g. "Would love to grab a coffee and catch up." / "Happy to jump on a quick call if timing works."]
149|
150|[Signature]
151|```
152|*Target: under 120 words.*
153|
154|#### WhatsApp / LINE — Basic
155|```
156|Hi [Name],
157|
158|[1 sentence warm greeting referencing last interaction or their context]
159|
160|[1 genuine question relevant to their industry or role]
161|
162|[Light CTA — e.g. "Would love to catch up soon!"]
163|```
164|*3–4 lines max. Warm and personal. No links.*
165|
166|---
167|
168|### With Content Engine (article included)
169|
170|#### Email — with article
171|```
172|Subject: [personalised — not "sharing an article with you"]
173|
174|Hi [Name],
175|
176|[1–2 sentences: greeting referencing last interaction or something relevant to them]
177|
178|[1–2 sentences: natural lead-in to the article — why it made you think of them]
179|
180|[Article title + link]
181|
182|[Light closing question or invitation — e.g. "Would love to catch up when you have a moment."]
183|
184|[Signature]
185|```
186|
187|#### WhatsApp / LINE — with article
188|```
189|Hi [Name],
190|
191|[1 sentence greeting]
192|
193|Thought of you when I came across this — [why it's relevant to them]:
194|[Article title]
195|[Link]
196|
197|[Light closing question]
198|```
199|
200|---
201|
202|## Step 5: Deliver and Send
203|
204|### Who sends?
205|Based on relationship warmth and preferred channel:
206|- **Close relationship (met in person, frequent past interactions):** Sales rep sends directly — Leo prepares the draft
207|- **Acquaintance (know each other but infrequent contact):** Leo can send via email, or sales rep sends via WhatsApp
208|- **Unclear:** Default to presenting draft to sales rep for confirmation
209|
210|### Mode A output
211|```
212|📬 Nurture Draft — [Contact Name]
213|
214|Mode: Basic (check-in, no article) | Content Engine (article included)
215|Channel: [Email / WhatsApp]
216|Last contact: [N days ago — brief summary]
217|Article: [Title + link]  ← omit this line in Basic mode
218|
219|--- Draft ---
220|[message body]
221|---
222|
223|Should I send this, or would you prefer to send it yourself?
224|```
225|
226|### Mode B output
227|```
228|📬 Monthly Nurture List — [N] contacts
229|Mode: Basic (no Content Engine) | Content Engine active
230|
231|1. [Name] ([Company]) — last contact: [N days ago]
232|   Channel: [Email/WhatsApp]
233|   Draft: [first 30 chars preview...]
234|
235|2. [Name] ([Company]) — last contact: [N days ago]
236|   ...
237|
238|All drafts ready. Review one by one, or approve all for sending?
239|```
240|
241|---
242|
243|## Step 6: Log the Engagement
244|
245|After sending (whether sent by sales rep or Leo), immediately create an Engagement record:
246|- Title: `[YYYY-MM-DD] — Nurture — [Contact Name]`
247|- Type: Email / WhatsApp / LINE
248|- Status: Completed
249|- Date: send date
250|- Contact: linked contact
251|- Account: linked account
252|- Related Deal: **empty**
253|- Notes: message content summary + article URL used (if Content Engine mode); or "Basic check-in — no article" (if Basic mode)
254|
255|This ensures the next monthly scan correctly calculates days since last contact.
256|
257|---
258|
259|## Pitfalls
260|
261|1. **Do not link to Related Deal** — Nurture Engagements must not appear in pipeline views. Leave Related Deal and Related Partnership empty.
262|
263|2. **Basic mode is intentional, not a fallback.** A genuine personalised check-in with no article is often more effective than a generic article share. Do not apologise for not having content to share.
264|
265|3. **Mode B: always let the sales rep review before sending** — Relationship management requires human judgment. Never auto-send the full batch.
266|
267|4. **Never send the same article to the same contact twice** — Before drafting, check that contact's Engagement Notes for the article URL. If it appears, pick a different article.
268|
269|5. **Skip contacts with active Deals** — Those relationships are already managed by deal-progressing. Do not create duplicate outreach.
270|
271|6. **Content Engine is opt-in** — Basic mode is the default. Content Engine mode activates only when the user explicitly provides a Content Engine table token. Do not block or delay nurturing while waiting for the Content Engine to be built.
272|