# Wiki Setup

This directory contains the document templates that must be filled in before the agent team can operate effectively.

These documents are the **context layer** — they tell agents like Leo who you are, who you're selling to, and how you measure success. Without them, agents cannot make qualified decisions.

---

## Required Documents

### `sales-strategy.md` ← **Fill this in first**

**What it is:** Sales & Partnership Strategy — the single input source for Leo's Pipeline Health Check.

**Who fills it in:** Founders / Sales Lead

**When:** Before Leo runs his first Weekly Pipeline Health Check

**What Leo does with it:**
1. On first setup — extracts this document → stores in GBrain (structured) + Hindsight `dx-global` (semantic search)
2. Every Weekly Health Check — recalls this as the anchor before analysing CRM data
3. When the doc is updated — re-run extraction → GBrain / Hindsight auto-updates

**Sections to fill:**
1. Company Overview
2. Sales Goals
3. ICP (Ideal Customer Profile)
4. Sales Strategy
5. Partnership Goals
6. Partnership Strategy
7. Pipeline Benchmarks

---

## How to Set Up

1. Copy the templates from this directory into your company's `dx-internal-wiki/context/` repo
2. Fill in each section — use `[brackets]` as placeholders where you don't have data yet
3. Commit and push
4. Tell Leo: "Extract the sales strategy from the wiki" — Leo will handle the rest

---

## What Happens If You Skip This

Leo can still operate but will fall back to generic judgement with no company-specific anchors:
- No ICP = Leo cannot qualify leads beyond surface-level signals
- No pipeline benchmarks = Health Check cannot flag stalls relative to your cycle length
- No sales goals = Leo cannot prioritise deals by strategic fit

Fill in what you have. Partial data is better than none.
