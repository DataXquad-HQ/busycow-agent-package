1|---
2|name: follow-up-email
3|description: Use when you need to draft a follow-up email to a prospect or client. Generate context-aware copy based on deal stage, last interaction, and relationship history.
4|version: 1.0.0
5|author: Hermes Agent
6|license: MIT
7|metadata:
8|  hermes:
9|    tags: [sales, outreach, email, leo-bd]
10|    related_skills: [deal-advisory, engagement-logging, managing-sales-pipeline]
11|---
12|
13|# Follow-Up Email
14|
15|## Overview
16|
17|Drafting follow-up emails is a core BD activity. The challenge: **tone and content must match deal stage, relationship depth, and last interaction context.** A re-engagement email after 14 days of silence reads very different from a "one more thing" email after a positive call.
18|
19|This skill helps you generate draft follow-up emails by analyzing the deal context from Lark Base CRM and proposing copy that:
20|- Matches the relationship stage (first touch vs. warm lead vs. active negotiation)
21|- References specific prior context (names, meeting dates, discussed problems)
22|- Sets clear expectations (request, timeline, next step)
23|- Avoids common pitfalls (too salesy, too presumptuous, too formal, too casual)
24|
25|**This is a drafting tool.** You review, edit, and approve before sending—Leo never sends emails directly.
26|
27|## When to Use
28|
29|- You're following up on a meeting or call and want to summarize action items
30|- A prospect went quiet and you need a re-engagement email (gentle or firm)
31|- You're responding to an objection or concern raised by the client
32|- You're confirming next steps after an agreement in principle
33|- You're closing out a deal professionally (whether won, lost, or paused)
34|
35|**Don't use for:**
36|- First outreach to a cold lead (use your own voice or account-enrichment context)
37|- Automated campaigns or batch emails (these need personal, 1:1 context)
38|- Customer success or post-sale support (use support processes)
39|- Internal alignment emails (keep those off-channel)
40|
41|## How to Invoke
42|
43|Call this skill with:
44|- **Deal identifier:** Opportunity ID or deal context (company name, product, contact)
45|- **Email context:** What's the trigger? (e.g., "following up after our demo", "client said pricing is too high—need to respond", "want to re-engage after 10 days quiet")
46|- **Your intent:** What do you want to happen? (e.g., "confirm next meeting", "ask if they're still interested", "propose revised pricing")
47|- **Tone preference:** (Optional) "warm and casual" vs. "professional and direct" vs. "empathetic rebuttal"
48|
49|Leo will retrieve the deal and engagement history, identify the relationship stage and last interaction context, and draft a specific email for you to review.
50|
51|## Drafting Framework
52|
53|### Step 1: Retrieve Deal & Engagement Context
54|- Fetch Opportunity record (client, stage, last activity date, key contact details)
55|- Retrieve last 3–5 Engagements (type, date, who participated, outcome, any next steps mentioned)
56|- Check Tasks linked to this opportunity (what was supposed to happen next?)
57|- Identify relationship warmth: is this a repeat contact or first outreach?
58|
59|### Step 2: Classify Email Type & Tone Template
60|
61|**Summation Email** (after a meeting)
62|- Trigger: Just had a call, email recap + confirm next step
63|- Tone: Warm, specific, brief
64|- Template: "Thanks for taking time today. I heard [key point], we agreed to [action], next step is [X by date]."
65|
66|**Re-Engagement Email** (silence 7–14 days)
67|- Trigger: Client went quiet; you're gently checking in
68|- Tone: Casual, low-pressure, confident
69|- Template: "Wanted to circle back on [topic]. Are you still evaluating, or should we pause for now?"
70|
71|**Critical Re-Engagement** (silence 14+ days)
72|- Trigger: Extended silence; you need clarity
73|- Tone: Professional, direct, respect their time
74|- Template: "I know things move fast on your end. Quick question: is [product] still a priority, or should we look at this again in [timeframe]?"
75|
76|**Objection Rebuttal** (client raised concern)
77|- Trigger: Price too high, feature missing, competitive comparison
78|- Tone: Empathetic, confident, data-backed
79|- Template: "I hear that [concern]. Many clients had the same question; here's how we think about it: [reframe + data]."
80|
81|**Close-Out Email** (deal lost, paused, or won)
82|- Trigger: You've decided to close this deal (lost to competitor, client deprioritized, or moving to close)
83|- Tone: Professional, warm, door open
84|- Template: "Really appreciated working with [client]. Whether or not it's the right time now, [offer value: feedback, resource, connection]."
85|
86|### Step 3: Draft Email
87|
88|Generate email with:
89|- **Subject line:** Specific, not generic (e.g., "[Product] – pricing structure" vs. "Re: follow-up")
90|- **Opening:** Address by name; reference specific prior context (date, topic, person)
91|- **Body:** 3–4 sentences max. State what you heard, what you agreed to, what you're asking now
92|- **CTA (Call-to-Action):** One clear ask with a timeline (e.g., "Can you reply by EOD Friday?" or "Are you available for a 20-min call next Tuesday?")
93|- **Closing:** Warm but professional; offer specific help (not just "let me know if you have questions")
94|
95|## Output Format
96|
97|Leo returns a draft email structured like this:
98|
99|```
100|[FOLLOW-UP EMAIL DRAFT]
101|
102|TO: [recipient name + email]
103|SUBJECT: [proposed subject line]
104|
105|[Draft body]
106|
107|---
108|CONTEXT NOTES
109|├─ Email Type: [Summation | Re-Engagement | Objection Rebuttal | Close-Out]
110|├─ Relationship Stage: [Cold | Warm | Active | Mature]
111|├─ Days Since Last Engagement: [N]
112|├─ Last Interaction: [Date, Type, Who, Key Outcome]
113|└─ Tone Rationale: [Why this tone matches the situation]
114|
115|REVISION SUGGESTIONS
116|├─ If they don't respond in 3 days, try: [alternative angle]
117|├─ If they object to [X], counter with: [reframe]
118|└─ If relationship stalls again, escalate to: [Hunter | Kevin | Different contact]
119|```
120|
121|## Common Pitfalls
122|
123|1. **Over-explaining.** If it's been quiet, don't send a 5-paragraph email. Start with a soft question, then escalate if they don't respond.
124|
125|2. **Copy-pasting old emails.** Each follow-up must reference the specific prior context (date, name, last topic). Generic = low response rate.
126|
127|3. **Assuming they remember.** Even if you had a great meeting, they might not recall details. Remind them briefly: "Following up on our chat about [topic] on [date]."
128|
129|4. **Wrong CTA timing.** "Can you reply by tomorrow?" is aggressive after 2 weeks of silence. "Let me know your thoughts" is too vague. Aim for: "Can you confirm by end of week?"
130|
131|5. **Mixing multiple asks.** "Also, are you interested in our other product?" weakens the main CTA. Stay focused.
132|
133|6. **Apologizing for following up.** Don't say "sorry for the late follow-up." Say "wanted to circle back." Confidence > apology.
134|
135|7. **Ignoring relationship context.** A re-engagement email to someone who's been dormant for 20+ days should be warmer and more humble than one after 7 days. Match the depth of silence to the tone.
136|
137|## Verification Checklist
138|
139|- [ ] Email references specific prior context (name, date, topic)
140|- [ ] Subject line is specific, not generic
141|- [ ] Email is 3–4 sentences; body is scannable in <30 seconds
142|- [ ] CTA is clear and has a specific timeline
143|- [ ] Tone matches the deal stage and days-since-contact
144|- [ ] You've proofread for typos and tone
145|- [ ] You've decided: will you send as-is, edit, or take a different approach?
146|
147|## One-Shot Recipe: Re-engage after 10 days of silence
148|
149|**Scenario:** You sent a proposal to Acme Corp's CTO (Sam Chen) 10 days ago after a demo. No response.
150|
151|**Steps:**
152|1. Fetch deal: Acme Corp / [Product] / Proposal stage / Last engagement: demo call with Sam on [date]
153|2. Classify: Re-Engagement Email (7–14 day window)
154|3. Tone: Warm, casual, low-pressure
155|4. Draft:
156|   ```
157|   TO: sam.chen@acmecorp.com
158|   SUBJECT: [Product] – quick question on your timeline
159|
160|   Hi Sam,
161|
162|   Following up on the proposal we reviewed together on [date]. 
163|   Have you had a chance to loop in your team, or are you still evaluating?
164|
165|   If now's not the right time, no problem—just want to know so I can check back at the right moment.
166|
167|   Best,
168|   [Your name]
169|   ```
170|5. Note: This is a **question, not a pitch.** If Sam responds, you pitch again. If silence continues to day 20, escalate.
171|
172|