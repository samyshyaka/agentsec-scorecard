import json
import sys
from agentsec_scorecard.scorecard import Scorecard

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