# Ghost

[Ghost](https://ghost.org) is the self-hosted blog platform used for content publishing.

## Why self-hosted

- Full control over blog content, SEO settings, and publish workflow
- Ghost API accessible at `localhost:2368` — agents can draft and publish posts programmatically
- No per-post fees or platform restrictions
- Custom domain via Cloudflare Tunnel

## Agent access

Agents interact with Ghost via its Admin API:

```
http://localhost:2368/ghost/api/admin/   ← Admin API (create/update posts)
http://localhost:2368/ghost/api/content/ ← Content API (read published posts)
```

External browser access: `https://blog.{{DOMAIN}}` (via Cloudflare Tunnel)

## Stack

Ghost + MySQL 8.0, running as Docker Compose services.

## Setup

### 1. Create directories

```bash
mkdir -p /mnt/disks/data/ghost/volumes/{content,db}
cd /mnt/disks/data/ghost
```

### 2. Write docker-compose.yml

See `docker-compose.yml` in this directory — update:
- `url` → your public domain (e.g. `https://blog.{{DOMAIN}}`)
- All passwords → generate strong random values

### 3. Start

```bash
docker compose up -d
```

Verify:
```bash
curl -s http://localhost:2368/ghost/api/admin/site/ | python3 -m json.tool
```

### 4. Admin setup

Open `https://blog.{{DOMAIN}}/ghost` in browser (once Cloudflare Tunnel is running).
Complete Ghost onboarding: create admin account, name the publication.

### 5. Generate API key for agents

1. Ghost Admin → Settings → Integrations → Add custom integration
2. Name it `Hermes`
3. Copy the **Admin API Key** (format: `id:secret`)

Store securely — agents need this to publish posts.

### 6. Add Cloudflare Tunnel route

```bash
cloudflared tunnel route dns {{TUNNEL_NAME}} blog.{{DOMAIN}}
```

Add to `/etc/cloudflared/config.yml`:
```yaml
  - hostname: blog.{{DOMAIN}}
    service: http://localhost:2368
```

Then: `sudo systemctl restart cloudflared`

## Maintenance

```bash
# Upgrade Ghost
cd /mnt/disks/data/ghost
docker compose pull && docker compose up -d

# Backup content
docker exec ghost-db-1 mysqldump -u ghost -pghostpassword ghost > backup_$(date +%Y%m%d).sql
cp -r volumes/content backup_content_$(date +%Y%m%d)
```

## Related skill

`../../shared-skills/` — the `blog-content-crew` skill handles the full blog
pipeline: ideation → drafting → publishing to Ghost.
