# Durable Workflow Patterns

Use this sheet to choose an orchestration approach and baseline reliability policy.

## Runtime Decision Matrix

| Option | Choose when | Pros | Trade-offs |
| --- | --- | --- | --- |
| Temporal | Long-lived critical workflows, strict replay semantics, multi-service orchestration | Strong durability primitives, mature retries/timers/signals | Higher operational complexity |
| LangGraph durable runtime | LLM-first graph workflows with checkpointing and branch control | Natural fit for agent graphs and evaluator loops | Runtime model still requires careful infra and governance |
| Queue + DB checkpoints | Incremental migration from loop workers, moderate complexity | Simple adoption, transparent state model, low lock-in | More custom reliability code to maintain |
| In-memory loop only | Short, low-risk tasks that can restart from scratch | Fastest to implement | No durable resume or audit guarantees |

## Baseline State Schema

Use a single source-of-truth record per run.

```json
{
  "run_id": "uuid",
  "workflow_type": "string",
  "status": "pending|running|waiting_human|succeeded|failed|dead_lettered",
  "current_step": "string",
  "attempt": 1,
  "lease_owner": "worker-id",
  "lease_expires_at": "2026-04-14T10:00:00Z",
  "input_hash": "sha256",
  "output_summary": "string",
  "last_error": "string|null",
  "updated_at": "2026-04-14T10:00:00Z"
}
```

## Retry Policy Defaults

- Transient failures: 3-5 attempts, exponential backoff with jitter.
- Permanent failures: no retry after classification, move to dead-letter.
- Timeout: set per step from expected p95 latency plus safety margin.
- Cancellation: require cooperative cancellation checks for long steps.

## Idempotency Rules

- Assign idempotency keys to side-effecting steps.
- Persist sent-request fingerprints before external calls when possible.
- Validate dedupe keys on resume and duplicate delivery.
- Prefer upsert semantics for internal writes.

## Human-Gate Placement

Require human approval before:

- financial transactions
- customer-visible bulk actions
- irreversible destructive changes
- production config rollout

## Failure Drill Checklist

- Kill worker process during side-effecting step.
- Delay downstream dependency to trigger timeout.
- Return repeated 5xx from dependency and verify backoff.
- Deliver duplicate queue message and verify dedupe.
- Expire lease and verify takeover by another worker.
