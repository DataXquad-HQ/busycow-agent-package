---
name: cloudflare-tunnels
description: >
  Use when setting up, configuring, or updating Cloudflare Tunnels to expose
  self-hosted services on this VM to a public domain ({{DOMAIN}}) — without
  opening firewall ports or paying for Zero Trust. Covers first-time login,
  tunnel creation, per-service routing, and systemd service setup.
triggers:
  - "cloudflare tunnel"
  - "cloudflared"
  - "expose service to domain"
  - "self-host subdomain"
  - "no subdomain / path-based routing"
  - "connect VM service to domain"
---

# Cloudflare Tunnels — Self-Hosted Service Routing

## Context

Domain: `{{DOMAIN}}` (Cloudflare-managed DNS)
VM: GCP Linux (`{{USER}}@...`)
`cloudflared` binary: `/usr/local/bin/cloudflared` (already installed, keep updated)
Cert path: `~/.cloudflared/cert.pem` (written by login step)
Tunnel config: `~/.cloudflared/config.yml`

## Key Principle

**Zero Trust dashboard is NOT required.** Cloudflare Tunnels are free and work entirely via the `cloudflared` CLI. The Zero Trust dashboard now requires a credit card just to access — ignore it. Use the CLI-only flow below.

## Step 1 — Login (one-time, generates cert.pem)

```bash
cloudflared tunnel login
```

- This prints a URL. User must open it, sign into Cloudflare, and **select {{DOMAIN}}**.
- The command must stay running until the cert is downloaded. Run it in background:

```bash
cloudflared tunnel login 2>&1 | tee /tmp/cf_login.log &
```

- Poll `/tmp/cf_login.log` or watch `~/.cloudflared/cert.pem` to appear.
- **Pitfall**: If the command times out (foreground with short timeout), the cert never downloads even if the user completed browser auth. Always run as background process and watch for cert file.
- **Pitfall**: Each `tunnel login` call generates a NEW token URL. Do not reuse old URLs from a timed-out run. Always copy the fresh URL from the current run's output.

Verify success:
```bash
ls -la ~/.cloudflared/cert.pem
```

## Step 2 — Create the Tunnel

```bash
cloudflared tunnel create {{TUNNEL_NAME}}
```

This creates a tunnel and writes a credentials JSON to `~/.cloudflared/<UUID>.json`.
Note the tunnel UUID from output.

## Step 3 — Write config.yml

File: `~/.cloudflared/config.yml`

```yaml
tunnel: <UUID>
credentials-file: /home/{{USER}}/.cloudflared/<UUID>.json

ingress:
  # Hermes Web UI
  - hostname: hermes.{{DOMAIN}}
    service: http://localhost:8787
  # Hermes Dashboard
  - hostname: dashboard.{{DOMAIN}}
    service: http://localhost:9119
  # Plane (project management)
  - hostname: plane.{{DOMAIN}}
    service: http://localhost:8090
  # Twenty CRM
  - hostname: sales.{{DOMAIN}}
    service: http://localhost:3001
  # OpenHands
  - hostname: openhands.{{DOMAIN}}
    service: http://localhost:3000
  # Temporal UI
  - hostname: temporal.{{DOMAIN}}
    service: http://localhost:8080
  # Postiz (social scheduling)
  - hostname: postiz.{{DOMAIN}}
    service: http://localhost:4007
  # Open Design
  - hostname: design.{{DOMAIN}}
    service: http://localhost:7456
  # Spotlight
  - hostname: spotlight.{{DOMAIN}}
    service: http://localhost:8969
  # Fallback — required, must be last
  - service: http_status:404
```

## Step 4 — Add DNS Records (one per hostname)

```bash
cloudflared tunnel route dns {{TUNNEL_NAME}} hermes.{{DOMAIN}}
cloudflared tunnel route dns {{TUNNEL_NAME}} dashboard.{{DOMAIN}}
cloudflared tunnel route dns {{TUNNEL_NAME}} plane.{{DOMAIN}}
# ... repeat for each hostname
```

These create CNAME records in Cloudflare DNS pointing to the tunnel.

## Step 5 — Run Tunnel (test first)

```bash
cloudflared tunnel run {{TUNNEL_NAME}}
```

Verify at least one service is reachable externally, then proceed to systemd.

## Step 6 — Install as systemd Service

**Critical order**: copy files to `/etc/cloudflared/` BEFORE running `service install` — the install command fails if it can't find config there.

```bash
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/config.yml
sudo cp ~/.cloudflared/<UUID>.json /etc/cloudflared/<UUID>.json
sudo cp ~/.cloudflared/cert.pem /etc/cloudflared/cert.pem
# Update credentials-file path in config to /etc/cloudflared/<UUID>.json
sudo sed -i 's|/home/{{USER}}/.cloudflared/|/etc/cloudflared/|g' /etc/cloudflared/config.yml
# Now install
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

The service auto-enables on install (no separate `systemctl enable` needed).

## Adding a New Service

1. Add a new `hostname` + `service` block to `config.yml` (before the 404 fallback)
2. Run `cloudflared tunnel route dns {{TUNNEL_NAME}} <new-hostname>.{{DOMAIN}}`
3. Restart: `sudo systemctl restart cloudflared`

## Current Services Map

| Subdomain | Port | Service |
|-----------|------|---------|
| hermes.{{DOMAIN}} | 8787 | Hermes Web UI |
| dashboard.{{DOMAIN}} | 9119 | Hermes Dashboard |
| plane.{{DOMAIN}} | 8090 | Plane |
| sales.{{DOMAIN}} | 3001 | Twenty CRM |
| openhands.{{DOMAIN}} | 3000 | OpenHands |
| temporal.{{DOMAIN}} | 8080 | Temporal UI |
| postiz.{{DOMAIN}} | 4007 | Postiz |
| design.{{DOMAIN}} | 7456 | Open Design |
| spotlight.{{DOMAIN}} | 8969 | Spotlight |

## Pitfalls

- **Do NOT use Zero Trust dashboard** — it's now gated behind credit card even on free plan. All tunnel management is CLI-only.
- **Cert doesn't download if login command times out** — always background it with `tee /tmp/cf_login.log` and watch for cert.pem.
- **Each login attempt generates a new URL** — don't send the user a URL from a timed-out run; always send the fresh one.
- **systemd service reads from /etc/cloudflared/** not `~/.cloudflared/` — copy both config.yml and credentials JSON there, and update the path in config.yml.
- **Fallback ingress rule is mandatory** — config.yml must end with `- service: http_status:404` or tunnel validation fails.
