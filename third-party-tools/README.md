# Third-Party Tools

Self-hosted services that the agent team depends on.
Each subdirectory is a self-contained install guide for one tool.

---

## Tools

| Tool | Directory | Purpose | Internal port |
|------|-----------|---------|--------------|
| Twenty CRM | `twenty-crm/` | Open-source CRM — sales pipeline, partnerships, contacts | 3001 |
| Ghost | `ghost/` | Blog platform — content publishing with agent-accessible Admin API | 2368 |

---

## Access Convention

All agent code must use the **internal VM address** (e.g. `http://localhost:PORT`).
Never use Tailscale IPs or Cloudflare external URLs in agent code —
those are for human browser access only.

```
✅  http://localhost:3001    (Twenty CRM — use this in all agent code)
❌  http://100.x.x.x:3001   (Tailscale — browser only)
❌  https://crm.example.com  (Cloudflare tunnel — browser only)
```

---

## Adding a new tool

1. Create `<tool-name>/README.md` — what it is, why we self-host, access convention
2. Create `<tool-name>/SETUP.md` — step-by-step Docker / install guide
3. If agents need a Hermes skill to interact with it:
   - Add `<tool-name>/skills/<skill-name>.md` (tool-specific reference copy)
   - Add the canonical copy to `../../shared-skills/<skill-name>.md`
