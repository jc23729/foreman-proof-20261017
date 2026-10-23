"""Print a job status report from a JSON or CSV file."""

import argparse
import csv
import json
import sys

# Reporting must not create bytecode cache files.
sys.dont_write_bytecode = True

from job_report import summarize_jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON or CSV file containing jobs")
    parser.add_argument("--json", action="store_true", help="emit a JSON summary")
    parser.add_argument("--format", choices=("text", "markdown"), default="text",
                        help="output format (default: text)")
    args = parser.parse_args()

    try:
        with open(args.input, encoding="utf-8", newline="") as source:
            if args.input.endswith(".csv"):
                reader = csv.DictReader(source, strict=True)
                fields = reader.fieldnames
                if (not fields or len(set(fields)) != len(fields)
                        or not {"id", "state", "priority"}.issubset(fields)):
                    raise ValueError("CSV header must contain id, state, priority")
                jobs = []
                for row in reader:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("CSV row does not match header")
                    try:
                        priority = int(row["priority"])
                    except ValueError as exc:
                        raise ValueError("priority must be an integer") from exc
                    jobs.append({"id": row["id"], "state": row["state"],
                                 "priority": priority})
            else:
                data = json.load(source)
                if not isinstance(data, dict) or "jobs" not in data:
                    raise ValueError("input must contain a top-level jobs array")
                jobs = data["jobs"]
        summary = summarize_jobs(jobs)
    except (OSError, UnicodeError, ValueError, RecursionError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            key: summary[key]
            for key in ("total", "done", "running", "queued", "blocked", "next_queued")
        }))
        return 0

    print("# Job Status")
    if args.format == "markdown":
        print()
        print("| Metric | Count |")
        print("| --- | --- |")
        for key in ("total", "done", "running", "queued", "blocked"):
            print(f"| {key.capitalize()} | {summary[key]} |")
        print()
    else:
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
