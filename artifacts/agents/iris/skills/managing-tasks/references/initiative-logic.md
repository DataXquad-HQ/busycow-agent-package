# Auto-Initiative & Auto-Goal Logic

## Step 1 — Classify the task
Extract: Business Line, Type, Theme keywords (client name, project name, activity)

## Step 2 — Match to existing Initiative
Fuzzy-match on business line + keywords:

| Signal | Initiative pattern | Suggested action |
|--------|--------------------|------------------|
| PM system / migration | `[Client] — PM system migration` | link to the matching existing initiative when confidence is high |
| university / exchange event | `university exchange event` | link if an event initiative already exists |
| reseller / fire-response use case | `[Product] reseller fire-response use case` | route to the most relevant commercial or partner initiative |
| GTM / recurring revenue | `[Product] GTM and commercial strategy reset` | link to the active GTM strategy initiative |
| regional reseller / new market | `[Product] x [Partner] — regional resale` | link to the existing market-entry initiative |
| water utility / engineering progress | `[Product] x utility — engineering progress tracking` | link to the active delivery or engineering initiative |
| internal systems / pipeline / automation | `[Org] internal systems and pipeline optimization` | route to the internal-ops initiative |
| portfolio company / AI deployment | `[Portfolio Company] — AI agent deployment plan` | route to the company-specific deployment initiative |
| productization / templates / add-ons | `[Product] — productization strategy` | route to the active productization initiative |

- **>80% confidence** → link silently, mention inline: "→ Assigned to [Initiative Name]"
- **Ambiguous** → ask once: "I think this task belongs under [X] or [Y]. Which is right?"
- **No match** → propose new Initiative (see Step 4)

## Step 3 — Map Initiative to Goal
| Business Line | Goal Record ID |
|---------------|----------------|
| [Product] | `{{GOAL_RECORD_ID_PRODUCT}}` |
| [Portfolio Company] | `{{GOAL_RECORD_ID_PORTFOLIO_COMPANY}}` |
| [Org] | `{{GOAL_RECORD_ID_ORG}}` |

Always set Goal field (`fldQ5gGqoy`) when creating an Initiative.

## Step 4 — Create new Initiative if needed
1. Propose: Name, Type, Business Line, Target Finished
2. Say: "This looks like a new initiative. I suggest creating "[Name]" under [Goal]. Confirm and I will create it."
3. Wait for confirmation, then create and record for the session.
