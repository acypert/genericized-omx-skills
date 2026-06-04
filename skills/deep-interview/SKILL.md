---
name: deep-interview
description: Socratic requirements interview with ambiguity gating before execution
argument-hint: "[--quick|--standard|--deep] <idea or vague description>"
---

# Deep Interview

Deep Interview turns vague ideas into execution-ready specifications by asking focused questions about intent, scope, constraints, success criteria, and decision boundaries.

## When To Use

- The request is broad, ambiguous, or missing concrete acceptance criteria.
- The user asks to be interviewed, challenged, or not to assume.
- A durable requirements artifact is needed before planning or implementation.
- The cost of building the wrong thing is high.

Do not use this skill when the request has concrete file targets, clear acceptance criteria, and no meaningful unresolved choices.

## Depth Profiles

- `--quick`: target ambiguity `<= 0.30`, maximum 5 rounds.
- `--standard`: target ambiguity `<= 0.20`, maximum 12 rounds.
- `--deep`: target ambiguity `<= 0.15`, maximum 20 rounds.

Default to `--standard`.

## Core Rules

- Ask one question per round.
- Ask about intent and boundaries before implementation details.
- Inspect available code, docs, and artifacts before asking the user for project facts.
- Prefer evidence-backed confirmation questions: "I found X in Y. Should this change follow that pattern?"
- Do not hand off to implementation while ambiguity is above the selected threshold unless the user explicitly accepts the residual risk.
- Do not crystallize while non-goals or decision boundaries are unresolved.
- Save artifacts under `docs/`, never under runtime-specific hidden state directories.

## Preflight Context

1. Parse the request and derive a short slug.
2. Load the latest matching snapshot from `docs/context/{slug}-*.md` if present.
3. If no snapshot exists, create `docs/context/{slug}-{timestamp}.md` with:
   - task statement
   - desired outcome
   - stated solution
   - probable intent
   - known facts and evidence
   - constraints
   - unknowns
   - decision-boundary unknowns
   - likely codebase touchpoints

## Interview Loop

Repeat until ambiguity is below threshold, readiness gates are satisfied, the user exits, or the round cap is reached.

1. Score the current clarity dimensions:
   - intent
   - outcome
   - scope
   - constraints
   - success criteria
   - codebase context, for brownfield work
2. Ask the highest-leverage unresolved question.
3. Pressure-test the answer with evidence, assumptions, examples, or tradeoffs.
4. Re-score ambiguity and report the remaining gap.
5. Continue on the same thread when the answer is still vague.

Mandatory readiness gates:

- Non-goals are explicit.
- Decision boundaries are explicit.
- At least one prior answer has been revisited with an assumption, evidence, or tradeoff follow-up.

## Challenge Modes

Use each mode at most once when useful:

- Contrarian: challenge a core assumption.
- Simplifier: find the smallest useful scope.
- Ontologist: reframe symptoms into the underlying purpose.

## Artifact Output

When the interview is complete, write:

- Transcript summary: `docs/interviews/{slug}-{timestamp}.md`
- Execution-ready spec: `docs/specs/deep-interview-{slug}.md`

The spec should include:

- metadata: profile, rounds, final ambiguity, threshold, context type
- context snapshot path
- clarity breakdown
- intent
- desired outcome
- in-scope work
- out-of-scope work
- decision boundaries
- constraints
- testable acceptance criteria
- exposed assumptions and resolutions
- pressure-pass findings
- codebase evidence and inference notes
- full or condensed transcript

## Handoff Options

After artifact generation, offer the appropriate next step:

- Create a plan from the spec.
- Implement directly from the spec.
- Delegate parallel work if the runtime has reliable worker support.
- Refine the interview further.

Preserve any residual-risk warning in the handoff. Do not implement inside Deep Interview unless the user explicitly exits the interview and asks to proceed.

## Final Checklist

- [ ] Context snapshot exists under `docs/context/`
- [ ] Ambiguity score was shown each round
- [ ] Non-goals are explicit
- [ ] Decision boundaries are explicit
- [ ] At least one assumption or tradeoff was pressure-tested
- [ ] Transcript was written under `docs/interviews/`
- [ ] Spec was written under `docs/specs/`
- [ ] No runtime-specific hidden state path was used
