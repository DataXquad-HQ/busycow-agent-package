# Tavily

[Tavily](https://tavily.com) is the web search API used by Hermes agents for
real-time internet research.

## Why Tavily

Hermes Agent's `web_search` tool requires an external search provider.
Tavily is optimised for LLM-powered agents — it returns clean, structured
results (not raw HTML) and supports advanced filtering.

## Setup

1. Sign up at https://app.tavily.com and get an API key
2. Configure in Hermes:

```bash
hermes config set search.tavily_api_key YOUR_API_KEY
```

3. Verify:

```bash
hermes tools list    # web_search should appear as available
```

## How agents use it

The `web_search` tool is available to all agents automatically once configured.
Agents call it like:

```
web_search(query="...", limit=5)
```

No additional skill loading required — it's a built-in Hermes tool.

## Pricing

Tavily has a free tier (1,000 searches/month). Upgrade if agents hit the limit.

## Docs

https://docs.tavily.com
