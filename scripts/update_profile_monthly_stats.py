#!/usr/bin/env python3
import calendar
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "GareBear99")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
README_PATH = Path(os.environ.get("README_PATH", "README.md"))

if not TOKEN:
    raise SystemExit("Missing GH_TOKEN or GITHUB_TOKEN")


def http_json(url: str, method: str = "GET", data: bytes | None = None) -> dict | list:
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": f"{USERNAME}-profile-readme-updater",
        },
        method=method,
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


now = dt.datetime.now(dt.timezone.utc)
start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
if start.month == 12:
    end = start.replace(year=start.year + 1, month=1)
else:
    end = start.replace(month=start.month + 1)

graphql_query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
      totalCount
    }
    topStarred: repositories(
      ownerAffiliations: OWNER,
      privacy: PUBLIC,
      isFork: false,
      first: 1,
      orderBy: {field: STARGAZERS, direction: DESC}
    ) {
      nodes {
        nameWithOwner
        url
        stargazerCount
      }
    }
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
    }
  }
}
"""

graphql_payload = json.dumps({
    "query": graphql_query,
    "variables": {
        "login": USERNAME,
        "from": start.isoformat().replace("+00:00", "Z"),
        "to": end.isoformat().replace("+00:00", "Z"),
    },
}).encode("utf-8")

graph_data = http_json("https://api.github.com/graphql", method="POST", data=graphql_payload)
if graph_data.get("errors"):
    raise SystemExit(f"GraphQL error: {graph_data['errors']}")

user = graph_data["data"]["user"]
commit_count = user["contributionsCollection"]["totalCommitContributions"]
repo_count = user["repositories"]["totalCount"]
month_label = f"{calendar.month_name[start.month]} {start.year}"
monthly_line = f"{commit_count} commits · {repo_count} repos · {month_label} · solo"

top_nodes = user["topStarred"]["nodes"]
if top_nodes:
    top = top_nodes[0]
    top_repo_line = f"Top starred repo: [{top['nameWithOwner']}]({top['url']}) · ⭐ {top['stargazerCount']}"
else:
    top_repo_line = "Top starred repo: none found"

recent_commit_lines: list[str] = []
seen_repos: set[str] = set()

for page in range(1, 11):
    events_url = f"https://api.github.com/users/{urllib.parse.quote(USERNAME)}/events/public?per_page=100&page={page}"
    events = http_json(events_url)
    if not isinstance(events, list) or not events:
        break

    for event in events:
        if event.get("type") != "PushEvent":
            continue

        repo = (event.get("repo") or {}).get("name")
        if not repo or repo.lower() == USERNAME.lower():
            continue
        if repo in seen_repos:
            continue

        payload = event.get("payload") or {}
        commits = payload.get("commits") or []
        if not commits:
            continue

        message = (commits[-1].get("message") or "Commit update").strip().splitlines()[0]
        message = message.replace(""", "'")
        if len(message) > 72:
            message = message[:69].rstrip() + "..."

        created_at = event.get("created_at") or now.isoformat().replace("+00:00", "Z")
        commit_dt = dt.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        date_label = commit_dt.strftime("%b %d")
        repo_url = f"https://github.com/{repo}"

        recent_commit_lines.append(
            f'- [{repo}]({repo_url}) · commit: "{message}" · {date_label}'
        )
        seen_repos.add(repo)

        if len(recent_commit_lines) == 3:
            break

    if len(recent_commit_lines) == 3:
        break

if recent_commit_lines:
    recent_projects_block = "Last 3 projects committed to:
" + "
".join(recent_commit_lines)
else:
    recent_projects_block = "Last 3 projects committed to: none found"

text = README_PATH.read_text(encoding="utf-8")


def replace_between_markers(source: str, start_marker: str, end_marker: str, new_content: str) -> str:
    if start_marker not in source or end_marker not in source:
        raise SystemExit(f"README markers not found: {start_marker} / {end_marker}")
    before, remainder = source.split(start_marker, 1)
    _, after = remainder.split(end_marker, 1)
    return before + start_marker + "
" + new_content + "
" + end_marker + after


text = replace_between_markers(
    text,
    "<!-- MONTHLY_GITHUB_STATS_START -->",
    "<!-- MONTHLY_GITHUB_STATS_END -->",
    monthly_line,
)
text = replace_between_markers(
    text,
    "<!-- TOP_STARRED_REPO_START -->",
    "<!-- TOP_STARRED_REPO_END -->",
    top_repo_line,
)
text = replace_between_markers(
    text,
    "<!-- RECENT_PROJECTS_START -->",
    "<!-- RECENT_PROJECTS_END -->",
    recent_projects_block,
)

README_PATH.write_text(text, encoding="utf-8")
print(monthly_line)
print(top_repo_line)
print(recent_projects_block)
