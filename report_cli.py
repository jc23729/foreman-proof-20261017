"""Print a job status report from a JSON file."""

import argparse
import json
import sys

# Reporting must not create bytecode cache files.
sys.dont_write_bytecode = True

from job_report import summarize_jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON file containing jobs")
    parser.add_argument("--json", action="store_true", help="emit a JSON summary")
    args = parser.parse_args()

    try:
        with open(args.input, encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict) or "jobs" not in data:
            raise ValueError("input must contain a top-level jobs array")
        summary = summarize_jobs(data["jobs"])
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            key: summary[key]
            for key in ("total", "done", "running", "queued", "blocked", "next_queued")
        }))
        return 0

    print("# Job Status")
    print(
        f"Total: {summary['total']} | Done: {summary['done']} | "
        f"Running: {summary['running']} | Queued: {summary['queued']} | "
        f"Blocked: {summary['blocked']}"
    )
    next_job = summary["next_queued"]
    print(f"Next: {next_job if next_job is not None else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
