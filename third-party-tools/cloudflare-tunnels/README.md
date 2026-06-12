# Cloudflare Tunnels

Exposes self-hosted tools (Twenty CRM, Ghost, etc.) via a public domain
**without opening any firewall ports** and without a Zero Trust subscription.

## Why Cloudflare Tunnels

- Self-hosted tools run on `localhost` inside the VM
- Team members and clients need browser access from outside the VM
- Cloudflare Tunnels creates a secure outbound connection from the VM to Cloudflare's edge
- Traffic routes: `https://tool.yourdomain.com → Cloudflare edge → cloudflared daemon → localhost:PORT`

## Key facts

- **Free tier** — Tunnels are free. Do NOT use the Zero Trust dashboard (now requires credit card even on free plan)
- **CLI-only management** — all setup and routing is done via `cloudflared` CLI
- **Systemd service** — `cloudflared` runs as a system service, auto-starts on boot
- **One tunnel, many routes** — a single tunnel can serve all tools via different subdomains

## Current services map

| Subdomain | Internal port | Tool |
|-----------|--------------|------|
| `hermes.{{DOMAIN}}` | 8787 | Hermes Web UI |
| `dashboard.{{DOMAIN}}` | 9119 | Hermes Dashboard |
| `sales.{{DOMAIN}}` | 3001 | Twenty CRM |
| `blog.{{DOMAIN}}` | 2368 | Ghost |

_Add new rows as new tools are deployed._

## ⚠️ Agent access rule

Cloudflare tunnel URLs are **for human browser access only**.
Agent code must always use `http://localhost:PORT` directly.

## Setup steps

### 1. Install cloudflared

```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
cloudflared --version
```

### 2. Login (one-time — generates cert.pem)

Run in background so it doesn't time out:

```bash
cloudflared tunnel login 2>&1 | tee /tmp/cf_login.log &
```

- Copy the URL from `/tmp/cf_login.log`, open in browser
- Sign in and **select your domain**
- Wait for `~/.cloudflared/cert.pem` to appear

```bash
ls -la ~/.cloudflared/cert.pem   # verify
```

> ⚠️ Each login attempt generates a NEW URL. Don't reuse old ones from timed-out runs.

### 3. Create tunnel

```bash
cloudflared tunnel create {{TUNNEL_NAME}}
# Note the tunnel UUID from output
```

### 4. Write config.yml

`~/.cloudflared/config.yml`:

```yaml
tunnel: {{TUNNEL_UUID}}
credentials-file: /home/{{USER}}/.cloudflared/{{TUNNEL_UUID}}.json

ingress:
  - hostname: hermes.{{DOMAIN}}
    service: http://localhost:8787
  - hostname: sales.{{DOMAIN}}
    service: http://localhost:3001
  - hostname: blog.{{DOMAIN}}
    service: http://localhost:2368
  # Required fallback — must be last
  - service: http_status:404
```

### 5. Add DNS records

```bash
cloudflared tunnel route dns {{TUNNEL_NAME}} hermes.{{DOMAIN}}
cloudflared tunnel route dns {{TUNNEL_NAME}} sales.{{DOMAIN}}
cloudflared tunnel route dns {{TUNNEL_NAME}} blog.{{DOMAIN}}
```

### 6. Install as systemd service

```bash
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/config.yml
sudo cp ~/.cloudflared/{{TUNNEL_UUID}}.json /etc/cloudflared/{{TUNNEL_UUID}}.json
sudo cp ~/.cloudflared/cert.pem /etc/cloudflared/cert.pem

# Update credentials path in the copied config
sudo sed -i 's|/home/{{USER}}/.cloudflared/|/etc/cloudflared/|g' /etc/cloudflared/config.yml

sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

### Adding a new service later

1. Add hostname + service block to `/etc/cloudflared/config.yml` (before the 404 fallback)
2. `cloudflared tunnel route dns {{TUNNEL_NAME}} new-tool.{{DOMAIN}}`
3. `sudo systemctl restart cloudflared`

## Pitfalls

- `cert.pem` won't download if the login command times out — always background it
- `systemd` reads from `/etc/cloudflared/`, NOT `~/.cloudflared/` — copy files and update paths
- The fallback `- service: http_status:404` is required — config validation fails without it
- Zero Trust dashboard now requires a credit card to access — ignore it, use CLI only
