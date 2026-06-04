---
name: durable-agentic-workflow
description: Design, evaluate, or migrate to durable long-running agent workflows with checkpointed state, retries, leases, and resume safety. Use when replacing fragile loop-based agents, building multi-step autonomous flows, adding crash recovery, or introducing human approval gates in long-running tasks.
---

# Durable Agentic Workflow

Design long-running agent systems that can pause, resume, retry, and recover deterministically.

Read [references/patterns.md](references/patterns.md) when choosing an orchestration runtime or failure policy.

## Workflow

1. Classify the workload
2. Select execution runtime
3. Define state and step contracts
4. Add reliability controls
5. Add observability and evaluation gates
6. Validate failure recovery paths

## 1) Classify The Workload

Capture these constraints first:

- Max run duration (minutes, hours, days)
- Need for resume after process crash or deploy restart
- Degree of parallelism and fan-out
- Human review checkpoints required or not
- External side effects (writes, purchases, messages)
- Reproducibility and audit requirements

If any answer implies state must survive restarts, treat the workflow as durable by default.

## 2) Select Execution Runtime

Choose one runtime family:

- Full durable orchestrator (`Temporal`, `LangGraph durable runtime`) for complex long-lived flows and strong replay semantics.
- Queue + DB checkpoint pattern for medium complexity and incremental adoption.
- Local in-memory loop only for short-lived, low-risk tasks with no durability requirements.

Use the decision matrix in [references/patterns.md](references/patterns.md).

## 3) Define State And Step Contracts

Model explicit workflow state:

- `run_id`
- `workflow_type`
- `status` (`pending|running|waiting_human|succeeded|failed|dead_lettered`)
- `current_step`
- `attempt`
- `lease_expires_at`
- `input_hash`
- `output_summary`
- `last_error`
- `updated_at`

Define each step with:

- deterministic input contract
- deterministic output contract
- idempotency key strategy
- retry policy (max attempts, backoff)
- timeout and cancellation behavior

## 4) Add Reliability Controls

Require these controls in every durable workflow:

- Step idempotency for all side effects
- Leases or locks for distributed workers
- Heartbeats for long-running steps
- Dead-letter handling after retry exhaustion
- Human approval gate for irreversible actions

Never rely on implicit process memory as the source of truth.

## 5) Add Observability And Evaluation Gates

Emit structured run telemetry:

- run lifecycle events (`run_started`, `step_started`, `step_succeeded`, `step_failed`, `run_finished`)
- per-step latency and retry counts
- queue lag and active lease counts
- evaluator gate verdicts and rationale

Add explicit evaluator gates before finalization for high-impact outputs.

## 6) Validate Failure Recovery Paths

Run failure drills before calling the workflow production ready:

- crash the worker mid-step and verify safe resume
- force transient dependency failures and verify retry/backoff
- force permanent failures and verify dead-letter routing
- test duplicate message delivery and confirm idempotent behavior
- test stale lease takeover

## Migration Pattern From Fragile Iteration Loops

Use this sequence to migrate incrementally:

1. Wrap the current loop in a tracked `run_id` envelope.
2. Persist step checkpoints between loop iterations.
3. Move tool calls into idempotent step handlers.
4. Introduce lease + heartbeat.
5. Add evaluator and human approval gates where needed.
6. Replace ad-hoc loop control with workflow state transitions.

## Output Template

When asked to propose a durable workflow, output:

1. Runtime recommendation and why
2. Workflow state schema
3. Step graph (ordered list or state machine)
4. Retry and timeout policy
5. Human approval checkpoints
6. Observability metrics and alerts
7. Failure drill test plan
