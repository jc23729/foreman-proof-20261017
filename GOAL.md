# Goal — autonomous foreman run

You are the foreman. Deliver the two-job contract in `TASKS.md`.

Job A must be planned and dispatched to an authorized worker. You must verify
Job A yourself against its real test file before Job B is allowed to start.
Job B must then run automatically, without the user writing another prompt.
When both jobs are verified, report completion and choose the next queued task
from `queue/NEXT.json`.

You do not write `job_report.py` or `report_cli.py` yourself. You plan, assign,
verify, decide, and record. The durable executor on Contabo runs the worker.
