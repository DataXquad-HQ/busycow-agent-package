1|---
2|name: account-onboarding
3|type: procedure
4|domain: sales
5|trigger: manual (user adds new Account to CRM)
6|owner: Leo (Revenue & Partnerships Agent)
7|created: 2026-06-10
8|updated: 2026-06-10
9|description: Complete workflow for adding a new Account to CRM. Collects company details, creates GBrain page, updates Lark Base, and triggers first enrichment.
10|dependencies:
11|  - account-enrichment (skill)
12|  - mcp_gbrain_put_page
13|  - mcp_lark_bitable_v1_appTableRecord_create
14|  - mcp_lark_contact_v3_user_batchGetId
15|---
16|
17|# Account Onboarding
18|
19|**Purpose**: Structured process for adding a new company (Account) to CRM. Ensures all required fields are captured, GBrain page is created, and initial enrichment is triggered.
20|
21|**When to use**: 
22|- User met with a company and wants to track it in the pipeline
23|- User received an inbound lead and needs to create an Account record
24|- Leo is adding a prospect company identified via partner outreach
25|
26|---
27|
28|## Workflow
29|
30|### Phase 1: Information Gathering
31|
32|**Ask user for the following details:**
33|
34|```
35|1. Company Name (English) *required
36|   - Example: "TechCorp Inc"
37|
38|2. Company Name (Chinese) [optional]
39|   - Example: "科技集团公司"
40|
41|3. Company Website *required
42|   - Example: "https://techcorp.com"
43|
44|4. Industry/Vertical *required
45|   - Options: IoT | Agriculture | Smart City | Manufacturing | Other
46|   - Free text allowed
47|
48|5. Geography (HQ Location) *required
49|   - Country and/or Region
50|   - Example: "Taiwan" or "Singapore, Southeast Asia"
51|
52|6. Company Size [optional]
53|   - Options: <50 | 50-200 | 200-1000 | 1000+
54|   - Used for lead scoring
55|
56|7. How did we discover them? *required
57|   - Options: Outbound research | Partner referral | Inbound inquiry | Conference | Other
58|   - Source field in Base
59|
60|8. Key Contact(s) [optional]
61|   - Name, Email, Title
62|   - Can add later via account-contact-linkage skill
63|
64|9. Brief notes on company [optional]
65|   - What they do, why we're interested, etc.
66|```
67|
68|**Verification**: Confirm company is not already in CRM before proceeding.
69|
70|### Phase 2: Create GBrain Company Page
71|
72|**Generate slug from company name:**
73|```
74|Format: companies/{slugified-name}
75|Example: "TechCorp Inc" → "companies/techcorp-inc"
76|
77|Rules:
78|- Lowercase
79|- Replace spaces with hyphens
80|- Remove special characters (except hyphens)
81|- Max 64 characters
82|```
83|
84|**Create GBrain page structure:**
85|
86|```markdown
87|---
88|slug: companies/{company_slug}
89|type: company
90|title: {Company Name}
91|website: {company_website}
92|industry: {industry}
93|geography: {geography}
94|company_size: {size}
95|discovered_via: {source}
96|created_date: {today's date}
97|last_enriched_date: null
98|---
99|
100|## Background
101|
102|{Brief company description from user notes, or placeholder}
103|
104|## Timeline
105|
106|(Will be populated after first enrichment)
107|
108|## Recent Insights
109|
110|(Will be populated after first enrichment)
111|
112|## Links
113|
114|(Outbound connections to other Accounts, Contacts, Partners)
115|
116|## Facts
117|
118|(Structured claims about company metrics, funding, products, etc.)
119|```
120|
121|**Action**:
122|```
123|mcp_gbrain_put_page(
124|  slug='companies/{company_slug}',
125|  content='[structured markdown above]'
126|)
127|```
128|
129|**Output**: GBrain page created and accessible at `companies/{company_slug}`
130|
131|### Phase 3: Create Lark Base Record
132|
133|**Insert new Account record into Lark Base:**
134|
135|```
136|mcp_lark_bitable_v1_appTableRecord_create(
137|  app_token="{{LARK_APP_TOKEN}}",
138|  table_id="tbl{accounts_table_id}",
139|  fields={
140|    "company_name": "{company_name}",
141|    "company_name_zh": "{company_name_zh}",
142|    "company_website": "{company_website}",
143|    "industry": "{industry}",
144|    "geography": "{geography}",
145|    "company_size": "{size}",
146|    "account_slug": "companies/{company_slug}",
147|    "source": "{discovered_via}",
148|    "account_status": "prospect",
149|    "notes": "{user_notes}",
150|    "created_date": "{today's date}",
151|    "last_enriched_date": null,
152|    "enrichment_notes": ""
153|  }
154|)
155|```
156|
157|**Important fields**:
158|- `account_slug`: Links Base record to GBrain page
159|- `account_status`: Always start as "prospect"
160|- `last_enriched_date`: null (will be set after first enrichment)
161|
162|**Output**: Lark Base record created with record_id returned for next step
163|
164|### Phase 4: Trigger First Enrichment
165|
166|**After Base record is created, run account-enrichment skill:**
167|
168|```
169|skill run account-enrichment \
170|  --company-name "{company_name}" \
171|  --account-slug "companies/{company_slug}" \
172|  --lark-record-id "{record_id}"
173|```
174|
175|**Why**: First enrichment populates initial intel, sets `last_enriched_date`, and fills `enrichment_notes`.
176|
177|**Result**: GBrain page now contains news/insights from Tavily search. Lark Base record has summary notes.
178|
179|### Phase 5: Link Primary Contact (optional, if provided)
180|
181|**If user provided contact information:**
182|
183|```
184|1. Resolve contact to open_id using mcp_lark_contact_v3_user_batchGetId
185|   OR create new Contact record in Lark Base if external contact
186|
187|2. Create relationship between Account and Contact
188|   (This step depends on your Contact-Account linking pattern)
189|```
190|
191|**Note**: Can be deferred if contact details come later.
192|
193|---
194|
195|## Verification Checklist
196|
197|After onboarding completes:
198|
199|- ✅ Company name exists in Lark Base (English + Chinese if provided)
200|- ✅ Company website is valid URL
201|- ✅ Account record has `account_slug` matching GBrain page slug
202|- ✅ GBrain page exists at `companies/{slug}` with Background section populated
203|- ✅ First enrichment completed: `last_enriched_date` is set to today
204|- ✅ Enrichment results visible in GBrain's "Recent Insights" section
205|- ✅ Summary notes visible in Lark Base's `enrichment_notes` field
206|- ✅ Account status is "prospect"
207|
208|---
209|
210|## Error Handling
211|
212|| Scenario | Action |
213||----------|--------|
214|| Company already in CRM | Stop. Ask user which record to update instead of creating duplicate. |
215|| Website URL is invalid | Warn user. Allow them to correct or skip. |
216|| Company name is empty | Reject. Company name is required. |
217|| GBrain page creation fails | Retry once. If fails again, create Base record but log error. User can manually create GBrain page later. |
218|| First enrichment returns 0 results | Still mark record as created. User can retry enrichment manually later when company news appears. |
219|| Lark Base insert fails (API error) | Log error. User should check Lark Base permissions. |
220|
221|---
222|
223|## Pitfalls & Gotchas
224|
225|1. **Duplicate company detection**: Before creating, check if company_name or company_website already exists in Base. Warn user if similar names found.
226|
227|2. **Company slug collisions**: If two companies have identical slugified names, append a number: `companies/techcorp-inc-2`. Unlikely but possible.
228|
229|3. **Empty geography field**: If user doesn't specify, default to "Unknown" or ask again. Geography is useful for filtering later.
230|
231|4. **Timezone in created_date**: Ensure timestamps use consistent timezone (Taiwan UTC+8 or UTC, depending on setup).
232|
233|5. **Account status vs maturity**: Don't confuse:
234|   - `account_status` = "prospect" (never changes from this on creation)
235|   - `account_maturity` = "cold"/"warm"/"hot" (changes based on Contact activity)
236|
237|6. **GBrain slug format**: Must match `account_slug` in Base exactly. Mismatch will break the link.
238|
239|7. **Contact linking deferred**: It's OK to create Account without Contact. But if Contact is provided, resolve their Lark ID carefully (email vs open_id).
240|
241|---
242|
243|## Manual Execution
244|
245|When user manually initiates this workflow:
246|
247|```bash
248|hermes skill run account-onboarding \
249|  --interactive
250|```
251|
252|**Interactive mode should**:
253|1. Prompt for each field in order
254|2. Validate inputs
255|3. Show summary before confirmation
256|4. Execute all steps in sequence
257|5. Display final result with GBrain page link
258|
259|---
260|
261|## Decision Tree
262|
263|```
264|User wants to add Account
265|  ↓
266|Is company already in Base?
267|  ├─ YES → Ask: Update existing or create duplicate?
268|  └─ NO → Proceed to gathering phase
269|  
270|  Gather all required fields
271|  ↓
272|  Confirm company details with user
273|  ↓
274|  Create GBrain page
275|  ├─ Success → Proceed
276|  └─ Fail → Log, continue to Lark Base anyway
277|  
278|  Create Lark Base record
279|  ├─ Success → Proceed
280|  └─ Fail → Stop, resolve Base API issue
281|  
282|  Trigger first enrichment
283|  ├─ Success → Mark Account as "ready"
284|  ├─ No results → Mark as "created, enrichment pending"
285|  └─ Fail → Log, user can retry later
286|  
287|  Link Contact (if provided)
288|  ├─ Success → Done
289|  └─ Deferred → Flag for user to do manually
290|```
291|
292|---
293|
294|## Integration with Other Workflows
295|
296|- **After onboarding**: Account enters "prospect" status. User begins outreach via opportunity tracking.
297|- **Scheduled enrichment**: Account joins the 15th/30th enrichment cron job automatically.
298|- **Partner routing**: Account may be routed to a Partner. Update Account's `assigned_partner` field when that happens.
299|
300|---
301|
302|## Future Enhancements
303|
304|- [ ] Duplicate detection via fuzzy name matching
305|- [ ] Auto-generate suggested Company Size based on website crawl
306|- [ ] Automatic Contact discovery (find employees via LinkedIn API integration)
307|- [ ] Pre-fill company info from public APIs (Crunchbase, PitchBook)
308|- [ ] Create associated Opportunity record in same flow
309|