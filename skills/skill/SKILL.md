---
name: skill
description: Manage local agent skills in user and project skill roots
argument-hint: "<command> [args]"
---

# Skill Management

Use this skill to inventory, create, edit, migrate, or remove local agent skills.

## Skill Roots

- User skills: `~/.agents/skills/`
- Project skills: `.agents/skills/`

Treat `~/.codex/skills/` and `.codex/skills/` as compatibility roots only. Do not install new user-authored skills there unless the user explicitly asks for Codex-home compatibility.

## Commands

### `skill list`

Scan user and project roots and show:

- name
- description
- path
- scope
- whether the skill has helper scripts, references, assets, or templates

Also report compatibility-root skills separately if they exist.

### `skill search <query>`

Search names, descriptions, frontmatter, and markdown content across:

- `~/.agents/skills/`
- `.agents/skills/`
- compatibility roots, if present

Return concise matches with paths and one relevant context line.

### `skill add <name>`

Create `SKILL.md` in `~/.agents/skills/<name>/` unless the user requests project scope.

Required frontmatter:

```yaml
---
name: <name>
description: <one-line trigger and purpose>
argument-hint: "<optional args>"
---
```

Body template:

```markdown
# <Skill Name>

## Purpose

## When To Use

## Workflow

## Verification
```

### `skill edit <name>`

Find the skill, read the current file, and make the smallest safe edit. Preserve local structure and existing helper files. If multiple skills match, show the matches and ask which one to edit.

### `skill remove <name>`

Never delete without explicit confirmation. When removal is approved, prefer moving the skill to `~/.agents/skills-archive/<timestamp>-<name>/` over permanent deletion unless the user requests deletion.

### `skill migrate <name-or-root>`

Use this when moving skills from compatibility roots into the generic agent root.

1. Inspect source and destination paths.
2. Detect name conflicts.
3. Rewrite runtime-specific artifact paths to `docs/` when applicable.
4. Move the active skill to `~/.agents/skills/<name>/`.
5. Move obsolete runtime-only skills to `~/.agents/skills-archive/<timestamp>/`.
6. Verify migrated skills no longer reference unwanted hidden state paths.

## Design Rules

- Search for an existing skill before creating a new one.
- Keep each skill focused on one job.
- Prefer explicit workflows and verification steps over broad behavioral essays.
- Put reusable scripts under `scripts/`.
- Put reusable examples under `examples/`.
- Put durable user/project artifacts under `docs/`, not under runtime-specific hidden state directories.
- Avoid hard-coding absolute local paths unless the skill is machine-specific.

## Safety

- Preserve user changes.
- Do not overwrite a destination skill without comparing contents.
- Do not remove compatibility-root skills until the migrated copy exists and has been checked.
- Report any archived skills and why they were not kept active.
