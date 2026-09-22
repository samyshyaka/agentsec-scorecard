# AgentSec-Scorecard

Standardized security scoring and reporting for AI agent evaluation results.

## Status

Working prototype.

AgentSec-Scorecard consumes the results.json output from
[AgentSec-Bench](https://github.com/samyshyaka/agentsec-bench) and produces:
- An overall security score (percentage of attempted attacks caught by any detection mechanism)
- A per-category breakdown (unauthorized tool invocation, prompt injection, etc.)
- OWASP control coverage counts
- NIST AI RMF function coverage counts (Govern/Map/Measure/Manage), using the same
  threat-category mapping as agentsec-crosswalk
- Score trending across runs: each run is recorded (with a timestamp) to
  `scorecard_history.json`, and the CLI reports whether the overall score and
  each category moved up, down, or stayed the same since the previous run.
  Unlike `scorecard.json`/`results.json` (single-run output), this history
  file is committed to the repo so the trend survives across weekly runs and PRs.

Tested directly against AgentSec-Bench's real output.

Note on interpretation: a high score reflects that known, deliberately-constructed
attack scenarios were caught. It is not a claim of general invulnerability -
coverage is bounded by the scenarios currently defined in AgentSec-Bench.

## Project layout

- `agentsec_scorecard/scorecard.py` - the scoring logic: overall score, per-category breakdown, OWASP coverage, and NIST AI RMF coverage, computed from AgentSec-Bench's `results.json`.
- `agentsec_scorecard/trend.py` - reads/writes `scorecard_history.json` and compares the two most recent runs to report score trends.
- `scripts/generate_scorecard.py` - CLI entry point that runs the scorer, records the run to history, and prints the scorecard plus the trend since the last run.
- `tests/test_trend.py` - test suite for the trend-tracking logic.

## Not yet done

- Integration into AgentSec-Bench's own HTML report as a single combined view