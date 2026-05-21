---
name: migrating-data-to-new-disk
description: Use when user wants to move large directories from the system disk to a new data disk (e.g. GCP persistent disk mounted at /mnt/disks/data). Covers rsync + symlink strategy, Docker data-root migration, and pitfalls around root-owned files and systemctl blocks.
version: 1.0.0
tags: [disk, storage, migration, docker, symlink, gcp]
---

# Migrating Data to a New Disk

## Context

GCP VM: system disk (/dev/sda, ~60GB), data disk (/dev/sdb, ~200GB) mounted at /mnt/disks/data.
Strategy: rsync everything to new disk, delete original, replace with symlink. Apps see no path change.

## Step 1 — Audit what's worth moving

```bash
sudo du -sh ~/* ~/.* 2>/dev/null | sort -rh | head -30
sudo du -sh /var/lib/docker /var/log /var/cache/apt 2>/dev/null | sort -rh
df -h /
```

Targets in priority order (biggest wins):
- `~/.local`     — Python venvs/pip, often 5-7GB
- `/var/lib/docker`             — Docker images/volumes, often 5-15GB
- `~/.npm`       — npm cache
- `~/.cache`     — general cache
- `~/.bun`       — bun runtime
- `~/.claude`    — Claude data
- `~/gbrain`     — GBrain source
- `~/.gbrain`    — GBrain data dir
- `~/.nvm`       — Node version manager
- Any large project dirs

## Step 2 — Create target dir on new disk

```bash
mkdir -p /mnt/disks/data/home
```

## Step 3 — rsync all non-Docker targets

```bash
for dir in .local .npm .cache .bun .claude .nvm .gbrain gbrain obsidian-app dify projects; do
  echo "Syncing $dir..."
  rsync -a ~/$dir/ /mnt/disks/data/home/$dir/
  echo "Done: $dir"
done
```

## Step 4 — Verify sizes match

```bash
for dir in .local .npm .cache .bun .claude .nvm .gbrain gbrain obsidian-app projects; do
  orig=$(du -sh ~/$dir 2>/dev/null | cut -f1)
  new=$(du -sh /mnt/disks/data/home/$dir 2>/dev/null | cut -f1)
  echo "$dir: orig=$orig new=$new"
done
```

## Step 5 — Replace originals with symlinks

```bash
cd ~
for dir in .local .npm .cache .bun .claude .nvm .gbrain gbrain obsidian-app dify projects; do
  if [ -d "$dir" ] && [ ! -L "$dir" ]; then
    rm -rf "$dir"
    ln -s /mnt/disks/data/home/$dir "$dir"
    echo "Symlinked: $dir"
  fi
done
```

PITFALL: Some dirs (e.g. dify) contain Docker volumes with root-owned files.
`rm -rf` will fail with "Permission denied". Use sudo:

```bash
sudo rm -rf ~/dify
ln -s /mnt/disks/data/home/dify ~/dify
```

## Step 6 — Migrate Docker data-root

Docker needs special handling — daemon.json is cleaner than pure symlink,
though symlink also works as a fallback.

### 6a — Stop all containers first

```bash
docker stop $(docker ps -q)
```

### 6b — Stop Docker daemon

PITFALL: `sudo systemctl stop docker docker.socket` is blocked by the Hermes
tool safety guard. You MUST ask the user to run this manually in their terminal:

  "Please run: sudo systemctl stop docker docker.socket"

Wait for confirmation before proceeding.

### 6c — rsync Docker data

```bash
sudo rsync -a /var/lib/docker/ /mnt/disks/data/docker/
# Verify
sudo du -sh /var/lib/docker /mnt/disks/data/docker
```

### 6d — Configure daemon.json and symlink

```bash
sudo mkdir -p /etc/docker
echo '{"data-root": "/mnt/disks/data/docker"}' | sudo tee /etc/docker/daemon.json

sudo rm -rf /var/lib/docker
sudo ln -s /mnt/disks/data/docker /var/lib/docker
ls -la /var/lib/docker
```

### 6e — Start Docker and containers back up

```bash
sudo systemctl start docker
sleep 3
sudo systemctl is-active docker

# Start containers (adjust names as needed)
docker start $(docker ps -a --format "{{.Names}}" | grep -v Exited)
sleep 5
docker ps --format "{{.Names}}\t{{.Status}}"
```

## Step 7 — Verify final disk usage

```bash
df -h /
df -h /mnt/disks/data
```

Expected: system disk drops from ~68% to ~45% or lower.

## Already-migrated items (as of May 2026)

- `~/.hermes` → `~/.hermes` (done earlier, symlink in place)
- All items above done in this session

## Notes

- The data disk must be mounted with a persistent entry in /etc/fstab or via GCP boot-time mount config, otherwise symlinks break on reboot.
- Check mount persistence: `cat /etc/fstab | grep sdb` or `grep data /etc/fstab`
- If the disk is not in fstab, add it or use GCP's "Keep disk mounted" option.
