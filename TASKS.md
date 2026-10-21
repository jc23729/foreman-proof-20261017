# Two Jobs — Execution Contract

Manager rule: Dispatch ONLY one code writer at a time. Independently validate A with the given tests and inspect the diff. After A is accepted, AUTOMATICALLY dispatch B using the actual accepted A code. Do not ask the user for a B prompt. Run all tests when B ends. Record proof with exact commit/file hashes, worker identity, A-to-B timeline and whether a scheduled check or restart works. If a real gate blocks a step, stop without inventing proof. Never enter other repositories or access private projects.

## Job A — Generic job summarizer
Create job_report.py exporting summarize_jobs(jobs).

Input: list of dictionaries with id, state and priority (positive integer), where state is queued, running, done, or blocked.
Output: dict containing total, queued, running, done, blocked, and next_queued (ID of queued job with the lowest priority number, breaking ties by ID). For no queued jobs, next_queued is None. Reject any unknown state or malformed entry with ValueError. Do not mutate input. Pass tests/test_job_report.py.

## Job B — Human-readable status command
ONLY after independent acceptance of A, create report_cli.py.
Support python3 report_cli.py --input tests/fixtures/jobs.json.
Load JSON with a top-level jobs array, use the accepted summarize_jobs from Job A (no copied logic), and print:
# Job Status
Total: N | Done: N | Running: N | Queued: N | Blocked: N
Next: JOB_ID (or Next: none).
Make no file changes when reading or reporting. Handle bad input with a nonzero exit and a short error. Pass tests/test_report_cli.py.

## Queue C — follow-on work

C1, C2 and C3 are defined in `CONTRACTS/C1.md`, `CONTRACTS/C2.md` and
`CONTRACTS/C3.md`, and selected from `queue/NEXT.json`. The protocol is
`FOREMAN_PROTOCOL.md` v2. Each contract names its acceptance tests; the worker
may change only `report_cli.py`, and no test file may be edited.

## Finish criteria
Both jobs have actual source files, independent acceptance, all tests green and automatic A -> B worker dispatch proven by the manager's session records. Do not call two jobs done just because one manager writes both in a single answer, or because a prompt was prepared. No push/PR/merge/deploy required after the first repository setup.
