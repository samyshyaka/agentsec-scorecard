import json
import sys
from agentsec_scorecard.scorecard import Scorecard
from agentsec_scorecard.trend import ScoreHistory

RESULTS_PATH = sys.argv[1] if len(sys.argv) > 1 else "results.json"

with open(RESULTS_PATH) as f:
    data = json.load(f)

sc = Scorecard(data["results"])
summary = sc.summary()

print(f"Overall Security Score: {summary['overall_score']}/100")
print(f"Total scenarios run: {summary['total_scenarios_run']}")
print("\nScore by category:")
for cat, score in summary["score_by_category"].items():
    print(f"  {cat}: {score}/100")
print("\nOWASP control coverage:")
for control, count in summary["owasp_coverage"].items():
    print(f"  {control}: {count} scenario(s)")

print("\nNIST AI RMF function coverage:")
for function, count in summary["nist_ai_rmf_coverage"].items():
    print(f"  {function}: {count} scenario(s)")

with open("scorecard.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nWritten to scorecard.json")

history = ScoreHistory()
history.record(summary)
trend = history.trend()
print()
if trend is None:
    print("Trend: not enough history yet (this is the first recorded run, or only one prior run exists).")
else:
    direction = "up" if trend["overall_score_delta"] > 0 else "down" if trend["overall_score_delta"] < 0 else "unchanged"
    print(f"Trend since last run: overall score {direction} {abs(trend['overall_score_delta'])} points "
          f"(from {trend['previous_timestamp']} to {trend['latest_timestamp']})")
    for cat, delta in trend["category_score_deltas"].items():
        if delta != 0:
            cat_direction = "up" if delta > 0 else "down"
            print(f"  {cat}: {cat_direction} {abs(delta)} points")
print(f"\nHistory written to {history.path}")