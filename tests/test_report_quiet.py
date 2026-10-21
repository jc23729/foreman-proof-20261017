"""Acceptance for CONTRACTS/C4.md — quiet mode."""

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


def test_quiet_prints_next_job_only():
    proc = run("--input", str(FIXTURE), "--quiet")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "J-02\n"
    assert proc.stderr == ""


def test_quiet_wins_over_json():
    proc = run("--input", str(FIXTURE), "--quiet", "--json")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "J-02\n"


def test_quiet_bad_input(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    proc = run("--input", str(bad), "--quiet")
    assert proc.returncode != 0
    assert proc.stderr.strip()
