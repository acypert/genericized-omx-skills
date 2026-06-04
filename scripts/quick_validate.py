#!/usr/bin/env python3
"""Validate packaged skill metadata and stale runtime references."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

FORBIDDEN_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"oh-my-codex",
        r"oh my codex",
        r"\.omx",
        r"~/\.omx",
        r"\bomx[ .-]",
        r"\bralph\b",
        r"\bralplan\b",
        r"\bultrawork\b",
        r"\$team\b",
        r"\$ralph\b",
        r"\$autopilot\b",
        r"\bautopilot\b",
    ]
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")

    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc

    result: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def iter_text_files(skill_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".md", ".py", ".yaml", ".yml", ".json", ".sh", ".txt"}:
            paths.append(path)
    return paths


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        return [f"missing skills directory: {SKILLS_DIR}"]

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        return ["no skill directories found"]

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        try:
            metadata = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(f"{skill_dir.name}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not name:
            errors.append(f"{skill_dir.name}: missing frontmatter name")
        if not description:
            errors.append(f"{skill_dir.name}: missing frontmatter description")
        if name and name != skill_dir.name:
            errors.append(f"{skill_dir.name}: frontmatter name is {name!r}")

        for text_file in iter_text_files(skill_dir):
            content = text_file.read_text(encoding="utf-8", errors="ignore")
            for pattern in FORBIDDEN_PATTERNS:
                match = pattern.search(content)
                if match:
                    rel = text_file.relative_to(ROOT)
                    errors.append(f"{rel}: stale runtime reference {match.group(0)!r}")
                    break

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    count = len([path for path in SKILLS_DIR.iterdir() if path.is_dir()])
    print(f"Validated {count} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
