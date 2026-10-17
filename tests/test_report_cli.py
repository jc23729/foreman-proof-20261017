import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_cli_happy_path():
    p = subprocess.run([sys.executable, str(ROOT/"report_cli.py"), "--input",
        str(ROOT/"tests/fixtures/jobs.json")], cwd=ROOT, text=True, capture_output=True)
    assert p.returncode == 0, p.stderr
    assert "# Job Status" in p.stdout
    assert "Total: 4 | Done: 1 | Running: 0 | Queued: 2 | Blocked: 1" in p.stdout
    assert "Next: J-02" in p.stdout

def test_cli_bad_json(tmp_path):
    f=tmp_path/"broken.json"
    f.write_text("{not json",encoding="utf-8")
    p=subprocess.run([sys.executable,str(ROOT/"report_cli.py"),"--input",str(f)],
        cwd=ROOT,text=True,capture_output=True)
    assert p.returncode != 0
    assert p.stderr
