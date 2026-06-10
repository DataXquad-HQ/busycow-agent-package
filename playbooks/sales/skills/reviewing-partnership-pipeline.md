1|---
2|name: reviewing-partnership-pipeline
3|description: Review all active partnerships for health — detect silence (14+ days no engagement), flag dormant partners, and create re-engagement tasks. Can be triggered manually ("幫我看一下 partnership 狀況") or automatically by daily cron. Mirrors reviewing-sales-pipeline but for the Partnership table.
4|version: 2.0.0
5|author: Leo (BD Director Agent)
6|metadata:
7|  hermes:
8|    tags: [sales, partnership, pipeline, crm, lark-base]
9|    related_skills: [managing-partnership-pipeline, reviewing-sales-pipeline, engagement-logging]
10|---
11|
12|# Reviewing Partnership Pipeline
13|
14|## When to Use
15|
16|**Manual trigger:**
17|- "幫我看一下 partnership 狀況"
18|- "有哪些 partner 沒動靜了"
19|- Any on-demand partnership health check
20|
21|**Automatic trigger (via cron):**
22|- Daily 07:00 — scan all active partnerships, flag dormant, create re-engagement tasks
23|- Silent if all partnerships are healthy
24|
25|## Two Modes
26|
27|### Mode A: Specific Partnership
28|Check health of a named partner. Pull last engagement, status, open tasks.
29|
30|### Mode B: Full Scan (cron or on-demand)
31|Scan all active partnerships. Flag any with 14+ days no engagement. Create tasks. Report summary.
32|
33|---
34|
35|## Step 1: Fetch Active Partnerships
36|
37|Query Partnerships table ({{TABLE_ID}}):
38|- Status ≠ Inactive / Closed
39|- Fields: Partner Name, Status, Last Engagement Date, Owner, Related Tasks
40|
41|---
42|
43|## Step 2: Evaluate Each Partnership
44|
45|For each partnership:
46|```
47|days_since_engagement = today - Last Engagement Date
48|
49|if days_since_engagement > 14:
50|    → flag as Needs Follow-up
51|    → check if re-engagement task already exists (open, created within 7 days)
52|    → if no existing task: create Task
53|```
54|
55|Task fields:
56|- Title: `[PARTNER] {Partner Name} — Re-engagement check`
57|- Related Partnership: link to partnership record
58|- Deadline: today
59|- Priority: 🟡 Medium
60|- Agent Advice: last engagement summary + suggested re-engagement approach
61|
62|---
63|
64|## Step 3: Output
65|
66|### Mode A output
67|```
68|🤝 Partnership Health — [Partner Name]
69|
70|Status: [Current status]
71|Last Engagement: [N days ago — type + summary]
72|Open Tasks: [N]
73|
74|Assessment: [Healthy / Needs Follow-up / At Risk]
75|Recommended Action: [One sentence]
76|```
77|
78|### Mode B output (cron or full scan)
79|If no issues found → **silent**. Do not send anything.
80|
81|If dormant partnerships found:
82|```
83|🤝 Partnership Health Check — [Date]
84|
85|Dormant (14+ days no engagement): [N]
86|Tasks Created: [N]
87|
88|[Partner Name] — [N] days
89|→ [Recommended action]
90|
91|[Partner Name] — [N] days
92|→ [Recommended action]
93|```
94|
95|---
96|
97|## Pitfalls
98|
99|1. **Silent when healthy** — Do not send "all good" messages. Only report when there is something to act on.
100|
101|2. **Don't duplicate tasks** — Check if an open re-engagement task already exists for this partner in the last 7 days before creating a new one.
102|
103|3. **New partnerships get a grace period** — Partners onboarded in the last 14 days should not be flagged, even if no engagement is logged yet.
104|