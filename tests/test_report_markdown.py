"""Acceptance for CONTRACTS/C2.md — Markdown table rendering."""

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


def test_markdown_table():
    proc = run("--input", str(FIXTURE), "--format", "markdown")
    assert proc.returncode == 0, proc.stderr
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert lines == [
        "# Job Status",
        "| Metric | Count |",
        "| --- | --- |",
        "| Total | 4 |",
        "| Done | 1 |",
        "| Running | 0 |",
        "| Queued | 2 |",
        "| Blocked | 1 |",
        "Next: J-02",
    ]


def test_markdown_rejects_broken_input(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("[]", encoding="utf-8")
    proc = run("--input", str(bad), "--format", "markdown")
    assert proc.returncode != 0
    assert proc.stderr.strip()
