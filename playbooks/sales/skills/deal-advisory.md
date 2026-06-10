1|---
2|name: deal-advisory
3|description: Use when a deal is stalled or stuck. Analyze deal history, client context, and engagement cadence to diagnose bottlenecks and recommend next actions.
4|version: 1.0.0
5|author: Hermes Agent
6|license: MIT
7|metadata:
8|  hermes:
9|    tags: [sales, deal-analysis, advisory, leo-bd]
10|    related_skills: [deal-progressing, engagement-logging, managing-sales-pipeline]
11|---
12|
13|# Deal Advisory
14|
15|## Overview
16|
17|When a deal stalls or you're unsure how to move it forward, use this skill to systematically analyze the situation and receive actionable {{RECORD_ID}}. This is a **human-triggered, advisory-only skill** — Leo gathers context, diagnoses the issue, and proposes options, but you make the final decision on next steps.
18|
19|Deal stalls typically fall into four categories:
20|1. **Information gap** — you don't know where the client stands
21|2. **Timing mismatch** — client is busy, decision-maker unavailable, budget cycle mismatch
22|3. **Competitive loss** — client chose a competitor
23|4. **Deal structure issue** — pricing, scope, or terms are misaligned
24|
25|The goal is to identify which category applies, understand the root cause, and recommend whether to: re-engage, pivot, or close the loop professionally.
26|
27|## When to Use
28|
29|- A deal has been quiet for 7+ days with no forward movement
30|- Client said "we'll get back to you" but went silent
31|- You received negative feedback but want to diagnose recovery options
32|- You're unsure whether to follow up or abandon the deal
33|- You need to decide: is this worth salvaging?
34|
35|**Don't use for:**
36|- Deals actively progressing (use `deal-progressing` for status updates instead)
37|- Leads that are still in qualification (use `account-enrichment` or lead scoring)
38|- Post-close activities (use customer success processes)
39|
40|## How to Invoke
41|
42|Call this skill when you have a deal identifier (Opportunity ID, company name, or deal stage context). Provide:
43|- **Deal context:** Opportunity ID, client name, product, last known stage
44|- **Your question:** What specifically is stuck? (e.g., "no response for 10 days", "client said pricing is too high", "waiting on their legal review")
45|- **Background:** Any recent context (last email date, last interaction type, known blockers)
46|
47|Leo will retrieve the full deal history from Lark Base CRM, analyze engagement cadence, and return a diagnostic summary with {{RECORD_ID}} actions.
48|
49|## Diagnostic Framework
50|
51|### Step 1: Gather Deal Intelligence
52|- Fetch Opportunity record (status, stage, last activity date, contact, account)
53|- Retrieve all Engagements (meetings, calls, emails) in reverse chronological order
54|- Check most recent Task entries (who did what, when, outcome)
55|- Identify key contacts and their roles (decision-maker, economic buyer, influencer)
56|
57|### Step 2: Diagnose the Stall Category
58|
59|**Information Gap:**
60|- Last engagement was a pitch/demo with no clear next step
61|- No follow-up scheduled; you don't know if client is interested
62|- Action: Send a low-pressure check-in email or request a brief sync
63|
64|**Timing Mismatch:**
65|- Client said "get back to you in [timeframe]" and that window hasn't closed yet, OR
66|- Known budget cycle / approval process is still in progress, OR
67|- Key decision-maker is on leave / unavailable
68|- Action: Respect the timeline; schedule a soft re-engagement for the promised date
69|
70|**Competitive Loss:**
71|- Client explicitly chose a competitor, OR
72|- Client said "we'll evaluate multiple options" and went silent (likely comparing)
73|- Action: Ask directly; if lost, request a close-out conversation for feedback
74|
75|**Deal Structure Issue:**
76|- Client objected to price, scope, or terms and negotiations stalled, OR
77|- Client has unanswered questions that block decision
78|- Action: Clarify assumptions, propose a revised structure, or escalate internally
79|
80|### Step 3: Calculate Risk & Recommendation Priority
81|
82|**Low Risk (likely {{RECORD_ID}}):**
83|- <7 days since last contact
84|- Clear next step defined and in the client's calendar
85|- Active negotiation or RFQ cycle ongoing
86|
87|**Medium Risk (needs gentle push):**
88|- 7–14 days since last contact
89|- Unclear next step, but recent engagement was positive
90|- Client promised decision within timeframe
91|
92|**High Risk (at critical juncture):**
93|- 14+ days since last contact with no engagement cadence plan
94|- Client radio silence after multiple touches
95|- Negative feedback received but not yet rebutted
96|
97|**Critical (likely lost):**
98|- 21+ days of silence with no explanation
99|- Client explicitly chose competitor or deprioritized
100|- Evaluation criteria or decision-maker changed unfavorably
101|
102|## Output Format
103|
104|Leo returns a structured advisory:
105|
106|```
107|[DEAL ADVISORY] <Client Name> — <Product>
108|
109|DEAL STATUS SNAPSHOT
110|├─ Current Stage: [stage from CRM]
111|├─ Days Since Last Engagement: [N]
112|├─ Last Interaction: [Date, Type, Outcome]
113|└─ Key Contact: [Name, Title, Status]
114|
115|DIAGNOSIS
116|├─ Category: [Information Gap | Timing Mismatch | Competitive Loss | Deal Structure Issue]
117|├─ Root Cause: [2–3 sentence explanation]
118|└─ Confidence: [High | Medium | Low]
119|
120|RECOMMENDATION
121|├─ Risk Level: [Low | Medium | High | Critical]
122|├─ Next Action: [Specific step]
123|├─ Timeline: [e.g., "within 2 days", "next Monday"]
124|├─ Message Tone: [e.g., "casual check-in", "confident rebuttal", "professional close-out"]
125|└─ Alternative Paths: [If primary doesn't work, try…]
126|
127|ESCALATION (if needed)
128|├─ Should I involve Hunter/Kevin? [Yes | No | Only if X condition]
129|└─ Reason: [e.g., "custom pricing required", "strategic account"]
130|```
131|
132|## Common Pitfalls
133|
134|1. **Waiting too long to diagnose.** By day 14 of silence, momentum is lost. Diagnose at day 7–10 when you still have a window to re-engage credibly.
135|
136|2. **Confusing "no response" with "no interest."** Many stalls are timing-driven, not deal-killers. Separate the two before deciding to close.
137|
138|3. **Recommending a big ask after silence.** If it's been quiet, re-engage with a soft, low-commitment question first (e.g., "checking in to see if you're still evaluating"). Save the detailed proposal for after they've re-engaged.
139|
140|4. **Forgetting to check the calendar.** If the client said "end of Q3," don't follow up on day 3. Diagnose timing assumptions carefully.
141|
142|5. **Not tracking competitor intel.** If you know a competitor is also pitching, that affects the urgency and tone. Capture that context when logging engagements.
143|
144|6. **Over-personalizing rejections.** Sometimes deals don't fit. Acknowledge it professionally and close the loop—don't keep pushing.
145|
146|## Verification Checklist
147|
148|- [ ] Deal Opportunity ID identified and record fetched from Lark Base
149|- [ ] All Engagements (past 90 days minimum) reviewed and timeline mapped
150|- [ ] Last interaction type and outcome clearly documented
151|- [ ] Diagnosis category matches the evidence (not guessed)
152|- [ ] Recommended next action is specific and has a clear timeline
153|- [ ] If escalation suggested, reason is documented for Hunter/Kevin review
154|- [ ] You've decided: will you implement the {{RECORD_ID}}, get input, or modify it?
155|
156|## One-Shot Recipe: "Deal went quiet for 12 days, should I follow up?"
157|
158|**Scenario:** You pitched Acme Corp on [Product] 12 days ago. The CFO said "looks good, I'll run it by the board." Radio silence since.
159|
160|**Steps:**
161|1. Fetch the Opportunity: Acme Corp / [Product] / Stage: Proposal
162|2. Check engagements: Last was a 30-min demo call 12 days ago; no follow-up tasks created
163|3. Diagnose: Timing Mismatch (board review cycle, not disinterest)
164|4. Risk: Medium (within normal decision window, but no checkpoint scheduled)
165|5. Recommend: Send an email *exactly* like this—
166|   ```
167|   Subject: Acme Corp – [Product] board timeline check
168|   Hi [CFO Name],
169|   
170|   Just checking in on the board review timeline you mentioned. 
171|   Are we still looking at [date]? Happy to clarify anything in the meantime.
172|   
173|   Best, [Your name]
174|   ```
175|6. Schedule next check-in for 7 days out if no response. If that passes, escalate to Hunter.
176|