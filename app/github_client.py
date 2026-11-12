"""Small GitHub Actions helper. Uses a personal access token only if supplied."""
from __future__ import annotations

import requests


def get_latest_workflow_runs(owner: str, repo: str, token: str = "", limit: int = 10):
    if not owner.strip() or not repo.strip():
        raise ValueError("Enter both a GitHub owner and repository name.")

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, params={"per_page": min(limit, 20)}, timeout=20)
    response.raise_for_status()
    payload = response.json()

    runs = []
    for run in payload.get("workflow_runs", []):
        runs.append({
            "workflow": run.get("name") or run.get("path") or "Workflow",
            "branch": run.get("head_branch", ""),
            "status": run.get("status", ""),
            "conclusion": run.get("conclusion") or "In progress",
            "created_at": run.get("created_at", ""),
            "html_url": run.get("html_url", ""),
        })
    return runs
