# Content Engine Integration — Lead Nurturing

## Current Status (as of 2026-06-10)
**NOT YET CONNECTED.** Content Engine Lark Base does not exist yet.

## What to Do Until It's Ready
When running Mode A or Mode B, if no article URL is provided by the user:
- Draft a pure check-in message (no article link)
- Note in the draft: "[Optional: add article link when Content Engine is ready]"
- Do NOT fabricate or guess article URLs

## What Content Engine Will Look Like (once built)
Hunter will create a Lark Base called "Content Engine" with:
- Each row = one published article
- Fields: Article Title, Ghost URL, Website URL, Published Date, Tags/Topics

Once built, Hunter will provide the app_token. Update this file with the token and table_id.

## Article Selection Logic (for when it's ready)
1. Fetch latest 3 articles from Content Engine table
2. Match against Contact's industry, role, and past Engagement Notes
3. Check Engagement Notes for previously sent links — do NOT repeat
4. Select most relevant; if none is clearly relevant, use most recent
5. Prefer website URL over Ghost URL for external sharing

## Same Article Rule
Never send the same article URL to the same Contact twice.
Check: query Contact's Engagement Notes for the article URL before including it.
