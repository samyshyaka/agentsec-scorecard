"""
Tracks Scorecard summaries across runs, in a small JSON history file, so a
score's change over time is visible instead of only ever showing a single
snapshot. Unlike results.json/scorecard.json (single-run output, gitignored),
scorecard_history.json is meant to be committed - trending only means
something if it survives across weekly runs and PRs.
"""
import json
import os
from datetime import datetime, timezone


class ScoreHistory:
    """Reads/writes a simple JSON history file of past scorecard summaries."""

    def __init__(self, path: str = "scorecard_history.json"):
        self.path = path

    def load(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            return json.load(f)

    def record(self, summary: dict) -> dict:
        """Appends the given summary (with a timestamp) to history and
        returns the newly written entry."""
        history = self.load()
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_score": summary["overall_score"],
            "score_by_category": summary["score_by_category"],
            "total_scenarios_run": summary["total_scenarios_run"],
        }
        history.append(entry)
        with open(self.path, "w") as f:
            json.dump(history, f, indent=2)
        return entry

    def trend(self) -> dict | None:
        """Compares the two most recent entries. Returns None if there
        aren't at least two runs yet to compare."""
        history = self.load()
        if len(history) < 2:
            return None
        previous, latest = history[-2], history[-1]
        overall_delta = round(latest["overall_score"] - previous["overall_score"], 1)

        category_deltas = {}
        categories = set(previous["score_by_category"]) | set(latest["score_by_category"])
        for cat in categories:
            prev_score = previous["score_by_category"].get(cat)
            latest_score = latest["score_by_category"].get(cat)
            if prev_score is None or latest_score is None:
                continue
            category_deltas[cat] = round(latest_score - prev_score, 1)

        return {
            "previous_timestamp": previous["timestamp"],
            "latest_timestamp": latest["timestamp"],
            "overall_score_delta": overall_delta,
            "category_score_deltas": category_deltas,
        }