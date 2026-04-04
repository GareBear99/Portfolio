# Auto-updating GitHub profile README setup

This package updates your profile README automatically with:
- monthly commit + public repo count
- top starred public repo
- last 3 projects you most recently committed to

## What updates automatically

The GitHub Action rewrites these marker blocks in `README.md`:
- `MONTHLY_GITHUB_STATS`
- `TOP_STARRED_REPO`
- `RECENT_PROJECTS`

## Schedule

The workflow is set to run hourly.
You can also trigger it manually from the Actions tab.

## Setup

1. Push this package into your special GitHub profile repository named exactly `GareBear99`.
2. Make sure GitHub Actions is enabled for the repo.
3. The included workflow uses the built-in `GITHUB_TOKEN`, so no extra secret is normally needed.
4. After the first workflow run, your placeholder lines will be replaced with live data.

## Notes

- The recent projects section uses your recent public `PushEvent` activity, so it reflects repos you actually committed to rather than repos that were merely pushed or updated.
- It keeps only the latest entry for each repo and displays the 3 most recent unique repos.
- The updater skips the profile README repo itself so it does not list itself as one of your recent projects.
- If the schedule ever stops running, re-enable the workflow in the GitHub Actions tab.
