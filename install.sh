#!/usr/bin/env bash
set -euo pipefail

force=false
dry_run=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      force=true
      shift
      ;;
    --dry-run)
      dry_run=true
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage: ./install.sh [--force] [--dry-run]

Copies packaged skills into ${AGENTS_HOME:-$HOME/.agents}/skills.

Options:
  --force    overwrite existing skills after backing them up
  --dry-run  print planned actions without copying files
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$repo_dir/skills"
agents_home="${AGENTS_HOME:-$HOME/.agents}"
target_dir="$agents_home/skills"
backup_dir="$agents_home/skills-backup/genericized-omx-skills-$(date -u +%Y%m%dT%H%M%SZ)"

if [[ ! -d "$source_dir" ]]; then
  echo "Missing skills directory: $source_dir" >&2
  exit 1
fi

conflicts=()
for skill_dir in "$source_dir"/*; do
  [[ -d "$skill_dir" ]] || continue
  name="$(basename "$skill_dir")"
  if [[ -e "$target_dir/$name" && "$force" != true ]]; then
    conflicts+=("$name")
  fi
done

if [[ ${#conflicts[@]} -gt 0 ]]; then
  echo "Refusing to overwrite existing skills without --force:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  exit 1
fi

if [[ "$dry_run" == true ]]; then
  echo "Would install skills into $target_dir"
  if [[ "$force" == true ]]; then
    echo "Would back up overwritten skills into $backup_dir"
  fi
  find "$source_dir" -mindepth 1 -maxdepth 1 -type d -print | sort
  exit 0
fi

mkdir -p "$target_dir"

for skill_dir in "$source_dir"/*; do
  [[ -d "$skill_dir" ]] || continue
  name="$(basename "$skill_dir")"
  target="$target_dir/$name"

  if [[ -e "$target" ]]; then
    mkdir -p "$backup_dir"
    cp -R "$target" "$backup_dir/$name"
    rm -rf "$target"
  fi

  cp -R "$skill_dir" "$target"
  echo "Installed $name"
done

echo "Installed skills into $target_dir"
if [[ -d "$backup_dir" ]]; then
  echo "Backups written to $backup_dir"
fi
