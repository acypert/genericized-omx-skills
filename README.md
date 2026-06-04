# Genericized OMX Skills

Generic agent skills adapted from a local oh-my-codex skill install.

These versions remove the runtime-specific OMX/Ralph/Team/Ultrawork control layer and keep the reusable workflows as ordinary agent skills. Durable artifacts are directed to `docs/` instead of `.omx/`.

## Included Skills

- `ai-slop-cleaner`
- `ask-claude`
- `ask-gemini`
- `code-review`
- `codex-feature-pipeline`
- `commit`
- `deep-interview`
- `durable-agentic-workflow`
- `hatch-pet`
- `note`
- `plan`
- `prd`
- `ship`
- `skill`
- `visual-verdict`
- `web-clone`
- `wiki`
- `writing-plans`

OMX runtime-control skills such as setup, doctor, hud, cancel, team, worker, ralph, and ultrawork are intentionally not included as active skills.

## Install

```bash
git clone https://github.com/acypert/genericized-omx-skills.git
cd genericized-omx-skills
python3 scripts/quick_validate.py
./install.sh
```

By default, `install.sh` refuses to overwrite existing skills. To replace existing copies, run:

```bash
./install.sh --force
```

The installer copies skills into:

```text
${AGENTS_HOME:-$HOME/.agents}/skills/
```

Existing skills overwritten with `--force` are backed up under:

```text
${AGENTS_HOME:-$HOME/.agents}/skills-backup/
```

## Notes

- `ask-claude` and `ask-gemini` expect local `claude` and `gemini` CLI binaries.
- `hatch-pet` still packages Codex pet assets under `${CODEX_HOME:-$HOME/.codex}/pets/`, because that is the Codex app pet loading contract.
- `ship` delegates to the local `codex-feature-pipeline` skill after installation.

## Validate

```bash
python3 scripts/quick_validate.py
```

The validator checks skill frontmatter, directory/name consistency, and stale OMX runtime references in the packaged skill files.
