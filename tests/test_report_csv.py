"""Acceptance for CONTRACTS/C3.md — CSV input."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "jobs.csv"


def run(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "report_cli.py"), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_csv_text_report():
    proc = run("--input", str(FIXTURE))
    assert proc.returncode == 0, proc.stderr
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert lines == [
        "# Job Status",
        "Total: 4 | Done: 1 | Running: 0 | Queued: 2 | Blocked: 1",
        "Next: J-02",
    ]


def test_csv_json_report():
    proc = run("--input", str(FIXTURE), "--json")
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout) == {
        "total": 4,
        "done": 1,
        "running": 0,
        "queued": 2,
        "blocked": 1,
        "next_queued": "J-02",
    }


def test_csv_rejects_malformed_input(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("id,state,priority\nJ-01,unknown,1\n", encoding="utf-8")
    proc = run("--input", str(bad))
    assert proc.returncode != 0
    assert proc.stderr.strip()
