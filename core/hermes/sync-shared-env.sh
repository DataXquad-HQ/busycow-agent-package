#!/bin/bash
# sync-shared-env.sh
# Pushes keys from shared.env into every profile's .env.
# Only ADDS missing keys — never overwrites profile-specific values.
#
# Usage:
#   ./sync-shared-env.sh           → sync all profiles
#   ./sync-shared-env.sh leo maya  → sync specific profiles only
#
# Run this whenever you add or update a key in shared.env.
# Place shared.env at: ~/.hermes/shared.env

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SHARED="$HERMES_HOME/shared.env"

if [[ ! -f "$SHARED" ]]; then
  echo "❌  shared.env not found at $SHARED"
  exit 1
fi

# Determine target profiles
if [[ $# -gt 0 ]]; then
  PROFILE_DIRS=()
  for name in "$@"; do
    PROFILE_DIRS+=("$HERMES_HOME/profiles/$name")
  done
else
  PROFILE_DIRS=("$HERMES_HOME/profiles"/*)
fi

added_total=0

for profile_dir in "${PROFILE_DIRS[@]}"; do
  [[ -d "$profile_dir" ]] || continue
  name="$(basename "$profile_dir")"
  env_file="$profile_dir/.env"

  # Create .env if it doesn't exist yet
  if [[ ! -f "$env_file" ]]; then
    touch "$env_file"
    chmod 600 "$env_file"
    echo "  created $env_file"
  fi

  added=0
  while IFS= read -r line; do
    # Skip comments and blank lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]]           && continue

    key="${line%%=*}"

    # Only add if this key is not already present in the profile env
    if ! grep -q "^${key}=" "$env_file" 2>/dev/null; then
      echo "$line" >> "$env_file"
      ((added++))
    fi
  done < "$SHARED"

  if [[ $added -gt 0 ]]; then
    echo "  ✓ $name  (+$added keys)"
  else
    echo "  · $name  (already up to date)"
  fi
  ((added_total += added))
done

echo ""
echo "Done. $added_total key(s) added across all profiles."
echo "Note: existing profile-specific keys were not touched."
