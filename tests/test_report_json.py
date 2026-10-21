"""Acceptance for CONTRACTS/C1.md — machine-readable report output."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "jobs.json"


def run(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "report_cli.py"), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_json_summary_matches_fixture():
    proc = run("--input", str(FIXTURE), "--json")
    assert proc.returncode == 0, proc.stderr
    assert proc.stderr == ""
    data = json.loads(proc.stdout)
    assert data == {
        "total": 4,
        "done": 1,
        "running": 0,
        "queued": 2,
        "blocked": 1,
        "next_queued": "J-02",
    }


def test_json_rejects_broken_input(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    proc = run("--input", str(bad), "--json")
    assert proc.returncode != 0
    assert proc.stderr.strip()
    assert proc.stdout.strip() == ""
