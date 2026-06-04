---
name: plan
description: Strategic planning with optional interview, consensus, and review modes
---

# Plan

Create an actionable work plan before implementation when the task is broad, risky, ambiguous, or explicitly asks for planning.

## When To Use

- The user asks to plan, scope, or review a plan.
- The request has unclear requirements, ownership, risk, or acceptance criteria.
- The work spans multiple files, modules, services, or user-facing workflows.
- The user asks for multi-perspective planning with `--consensus`.

Do not use this skill for simple questions or narrow fixes with obvious scope. In those cases, inspect the code and execute directly.

## Modes

| Mode | Trigger | Behavior |
| --- | --- | --- |
| Interview | broad or vague request | Ask one focused question at a time, then produce a plan |
| Direct | `--direct` or detailed request | Generate a plan immediately after inspection |
| Consensus | `--consensus` | Planner -> Architect -> Critic review loop before final plan |
| Review | `--review` | Critic-only review of an existing plan |

## Core Rules

- Search the existing codebase before proposing new structure.
- Ground claims in inspected files, commands, docs, or other concrete evidence.
- Ask only for choices that cannot be discovered locally and materially affect scope.
- Keep implementation steps sized to the actual task instead of forcing a fixed count.
- Make acceptance criteria concrete and testable.
- Save durable plan artifacts under `docs/plans/`; save drafts under `docs/drafts/`.

## Interview Mode

1. Classify the request as broad, vague, or underspecified.
2. Inspect the repository first for codebase facts the user should not have to provide.
3. Ask one high-leverage question at a time.
4. Cover intent, scope, non-goals, constraints, success criteria, and decision boundaries.
5. Stop interviewing when the plan can be written without major assumptions.

## Direct Mode

1. Inspect relevant files, docs, tests, configuration, and existing patterns.
2. Identify requirements, constraints, risks, and likely touchpoints.
3. Produce a plan with acceptance criteria and verification steps.

## Consensus Mode

Use this when the task is high risk or the user asks for consensus planning.

1. Planner drafts the plan and includes:
   - principles
   - top decision drivers
   - at least two viable options, or a clear reason alternatives were rejected
   - risks and verification strategy
2. Architect reviews for design soundness, boundary violations, coupling, and tradeoffs.
3. Critic reviews for weak assumptions, missing tests, vague acceptance criteria, and unhandled risks.
4. Revise until the Critic approves or five iterations have completed.
5. Final output must include an ADR section: decision, drivers, alternatives considered, why chosen, consequences, and follow-ups.

When `--interactive` is used, ask the user before handing the plan to execution. Without `--interactive`, output the final plan and stop.

## Review Mode

1. Read the plan from the requested path, defaulting to `docs/plans/`.
2. Review as an independent critic, not as the author.
3. Return `APPROVED`, `REVISE`, or `REJECT` with specific reasons.
4. For cleanup or refactor plans, verify that behavior-preserving tests or explicit test gaps are included.

## Plan Format

Every plan should include:

- Requirements summary
- Non-goals and decision boundaries
- Acceptance criteria
- Implementation steps with file references where applicable
- Risks and mitigations
- Verification steps
- Open questions

For consensus plans, also include:

- Principles
- Decision drivers
- Options considered
- ADR

## Final Checklist

- [ ] Existing solution or pattern was searched first
- [ ] Plan references concrete files or evidence where applicable
- [ ] Acceptance criteria are testable
- [ ] Risks have mitigations
- [ ] Verification commands or test gaps are explicit
- [ ] Durable artifact path is under `docs/plans/` when a file is saved
