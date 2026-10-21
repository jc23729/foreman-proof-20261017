# Foreman Protocol v1 — machine contract

You are the foreman. You never write `job_report.py` or `report_cli.py` yourself.
A durable executor on Contabo runs the authorized worker and publishes state at:

    http://217.76.48.5:47821/state.json

Poll that URL every 20 seconds. Do not ask the user anything.

## Step 1 — plan

Write and push `foreman/PLAN.json`:

```json
{
  "plan_version": 1,
  "goal_id": "goal-autonomy-20261021",
  "foreman": "devin-cloud",
  "job_a": {
    "id": "A",
    "kind": "repo_task",
    "worker": "codex-contabo",
    "spec": {
      "expected_file": "job_report.py",
      "test_path": "tests/test_job_report.py",
      "task": "<the Job A instruction from TASKS.md>"
    }
  },
  "job_b": {
    "id": "B",
    "kind": "repo_task",
    "worker": "codex-contabo",
    "spec": {
      "expected_file": "report_cli.py",
      "test_path": "tests/test_report_cli.py",
      "carry_files": ["job_report.py"],
      "task": "<the Job B instruction from TASKS.md>"
    }
  },
  "launch_b_when": "verdict_a_verified",
  "choose_next_from": "queue/NEXT.json"
}
```

Only `worker: codex-contabo` is authorized. Only the two test paths above are
accepted. Any other value is refused, and the run stops.

## Step 2 — verify Job A yourself

When `state.json` shows `job_a.status == "ACCEPTED"`:

1. Write `state.json.job_a.files["job_report.py"]` into your clone.
2. Run `python3 -m pytest tests/test_job_report.py -q`.
3. Compute `sha256sum job_report.py`.
4. Push `foreman/VERDICT_A.json`:

```json
{"verdict_version":1,"job":"A","verified":true,
 "sha256":"<your computed sha256>",
 "tests":{"command":"python3 -m pytest tests/test_job_report.py -q","exit":0},
 "checked_at":"<utc>"}
```

Your verdict is causally required: Job B is not dispatched unless your verdict
says `verified: true` and your sha256 matches the executor's own computation.

## Step 3 — verify Job B yourself

Same procedure with `report_cli.py`, `tests/test_report_cli.py`, and
`foreman/VERDICT_B.json`. Run that job's test with Job A's file present.

## Step 4 — report and choose

Push `foreman/REPORT.json`:

```json
{"report_version":1,"goal_id":"goal-autonomy-20261021","completed":true,
 "jobs":{"A":"ACCEPTED","B":"ACCEPTED"},"summary":"<one sentence>"}
```

Then push `foreman/DECISION.json` choosing exactly one candidate id from
`queue/NEXT.json`:

```json
{"decision_version":1,"chosen":"C1","reason":"<why this one is next>",
 "decided_at":"<utc>"}
```

## Rules

- One job at a time. Never dispatch Job B before your own VERDICT_A is pushed.
- Never claim a test passed without running it.
- No other repositories, no deployments, no credentials, no spending.
- If a gate blocks you, push `foreman/BLOCKED.json` with the reason and stop.
