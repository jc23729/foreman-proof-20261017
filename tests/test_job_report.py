import copy
import pytest
from job_report import summarize_jobs

def test_summary_and_next():
    jobs = [
        {"id": "B", "state": "queued", "priority":2},
        {"id": "A", "state": "queued", "priority":1},
        {"id": "C", "state": "done", "priority":3},
        {"id": "D", "state": "blocked", "priority":4},
        {"id": "E", "state": "running", "priority":5},
    ]
    unchanged = copy.deepcopy(jobs)
    assert summarize_jobs(jobs) == {
        "total":5, "queued":2, "running":1, "done":1,
        "blocked":1, "next_queued":"A"
    }
    assert jobs == unchanged

def test_empty_or_no_queued():
    assert summarize_jobs([])["next_queued"] is None
    assert summarize_jobs([{"id":"A","state":"done","priority":1}])["next_queued"] is None

def test_tie_by_id():
    jobs = [{"id":"B","state":"queued","priority":1},{"id":"A","state":"queued","priority":1}]
    assert summarize_jobs(jobs)["next_queued"] == "A"

@pytest.mark.parametrize("bad", [
    [{"id":"X","state":"unknown","priority":1}],
    [{"id":"X","state":"queued","priority":0}],
    [{"id":"X","state":"queued"}],
    ["not-a-job"],
])
def test_reject_bad_entries(bad):
    with pytest.raises(ValueError):
        summarize_jobs(bad)
