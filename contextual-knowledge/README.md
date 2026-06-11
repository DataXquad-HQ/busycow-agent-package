# Contextual Knowledge

Background knowledge **shared across the entire agent team**.

This is not structured data (that lives in `../structural-data/`) —
it's prose context that agents load when they need broader understanding
of who we are, what we build, and how the team works.

---

## What belongs here

- Company background: industry, mission, customers
- Product and service descriptions
- Team roster and roles
- Strategic context: goals, constraints, priorities
- Glossary of internal terminology

## What does NOT belong here

- Schema definitions → `../structural-data/`
- Installation guides → `../core/` or `../third-party-tools/`
- Agent-specific context → `../agent-teams/<agent>/CONTEXT.md`

## File format

Plain Markdown. One file per topic. Keep files under ~500 lines.

## Adding a new knowledge file

1. Create a descriptive filename: `company-overview.md`, `product-lines.md`, `team-roster.md`
2. Start with a `# Title` and a one-paragraph summary
3. Add a row to the table below

## Index

| File | What it covers |
|------|---------------|
| *(add files here as you create them)* | |
