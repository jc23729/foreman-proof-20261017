"""Summarize job counts and select the next queued job."""


def summarize_jobs(jobs):
    """Return state counts and the queued ID ordered by priority, then ID.

    Invalid job records raise ValueError. The input is never modified.
    """
    if not isinstance(jobs, list):
        raise ValueError("jobs must be a list")

    states = ("queued", "running", "done", "blocked")
    result = dict.fromkeys(states, 0)
    result.update(total=len(jobs), next_queued=None)
    next_job = None

    for job in jobs:
        if not isinstance(job, dict) or not all(
            key in job for key in ("id", "state", "priority")
        ):
            raise ValueError("each job must contain id, state, and priority")
        state = job["state"]
        priority = job["priority"]
        if not isinstance(state, str) or state not in states:
            raise ValueError("unknown job state")
        if type(priority) is not int or priority <= 0:
            raise ValueError("priority must be a positive integer")
        if job["id"] is None:
            raise ValueError("job id must not be None")

        result[state] += 1
        if state == "queued":
            candidate = (priority, job["id"])
            try:
                if next_job is None or candidate < next_job:
                    next_job = candidate
            except (TypeError, ValueError) as exc:
                raise ValueError("job IDs must be comparable") from exc

    if next_job is not None:
        result["next_queued"] = next_job[1]
    return result
