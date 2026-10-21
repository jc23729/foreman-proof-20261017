# Foreman Protocol v2 — machine contract

You are the foreman. You never write product code yourself. A durable executor
on Contabo runs the authorized worker and publishes state at the feed URL in
your task prompt. Poll that URL every 20 seconds. Do not ask the user anything.

Your prompt supplies:

    GOAL_ID   e.g. goal-autonomy-c1
    CONTRACT  e.g. CONTRACTS/C1.md
    FEED_URL  http://<host>/g/<token>/state.json
    JOBS      1 or 2

## Step 0 — session record

Push `foreman/SESSION.json`:

```json
{"goal_id": "<GOAL_ID>", "session_url": "<your Devin session URL or null>",
 "session_id": "<your session id or null>", "started_at": "<utc>"}
```

If you cannot determine your own session id, use `null`. Do not block on this.

## Step 1 — plan

Read `CONTRACT`. Write and push `foreman/PLAN.json`:

```json
{
  "plan_version": 1,
  "goal_id": "<GOAL_ID>",
  "foreman": "devin-cloud",
  "job_a": {
    "id": "A",
    "kind": "repo_task",
    "worker": "codex-contabo",
    "spec": {
      "expected_file": "<from CONTRACT>",
      "test_path": "<from CONTRACT>",
      "also_test": ["<optional regression tests from CONTRACT>"],
      "task": "<the worker instruction you derive from CONTRACT>"
    }
  },
  "job_b": null,
  "launch_b_when": "verdict_a_verified",
  "choose_next_from": "queue/NEXT.json"
}
```

If `JOBS` is 2, `job_b` is an object with `id: "B"`, the same `kind` and
`worker`, and its own `spec`. If `JOBS` is 1, `job_b` must be `null` (or
omitted).

Only `worker: codex-contabo` is authorized. Only the test paths named in the
contract are accepted. Any other value is refused and the run stops.

## Step 2 — verify Job A yourself

When the feed shows `job_a.status == "ACCEPTED"`:

1. Write `feed.job_a.files[<expected_file>]` into your clone.
2. Run `python3 -m pytest <test_path> <also_test...> -q`. All must pass.
3. `sha256sum <expected_file>` must equal `feed.job_a.sha256`.
4. Commit and push the accepted file — this is the product change:
   `git add <expected_file> && git commit -m "<GOAL_ID>: <expected_file> accepted (<job_id>)"`
5. Push `foreman/VERDICT_A.json`:

```json
{"verdict_version": 1, "job": "A", "job_id": "<feed job_a.job_id>",
 "verified": true, "sha256": "<your sha256>",
 "tests": {"command": "python3 -m pytest ...", "exit": 0},
 "checked_at": "<utc>"}
```

Your verdict is causally required for Job B. It must carry the exact `job_id`
from the feed and a sha256 that matches the executor's own computation.

## Step 3 — verify Job B (only when JOBS=2)

Same procedure with Job B's expected file and tests, and
`foreman/VERDICT_B.json`. Commit and push the accepted file.

## Step 4 — report and choose

Push `foreman/REPORT.json`:

```json
{"report_version": 1, "goal_id": "<GOAL_ID>", "completed": true,
 "jobs": {"A": "ACCEPTED", "B": "ACCEPTED"},
 "summary": "<one sentence>"}
```

Then push `foreman/DECISION.json` choosing exactly one candidate id from
`queue/NEXT.json`:

```json
{"decision_version": 1, "goal_id": "<GOAL_ID>", "chosen": "C2",
 "reason": "<why this one is next>", "decided_at": "<utc>"}
```

## Rules

- One job at a time.
- Never edit anything under `tests/`.
- Never claim a test passed without running it.
- No other repositories, no deployments, no credentials, no spending.
- Do not modify `queue/NEXT.json`.
- If a gate blocks you, push `foreman/BLOCKED.json` with the reason and stop.
- Finish within 20 minutes.
