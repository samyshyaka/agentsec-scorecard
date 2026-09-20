# AgentSec-Scorecard

Standardized security scoring and reporting for AI agent evaluation results.

## Status

Working prototype.

AgentSec-Scorecard consumes the results.json output from
[AgentSec-Bench](https://github.com/samyshyaka/agentsec-bench) and produces:
- An overall security score (percentage of attempted attacks caught by any detection mechanism)
- A per-category breakdown (unauthorized tool invocation, prompt injection, etc.)
- OWASP control coverage counts

Tested directly against AgentSec-Bench's real output.

Note on interpretation: a high score reflects that known, deliberately-constructed
attack scenarios were caught. It is not a claim of general invulnerability -
coverage is bounded by the scenarios currently defined in AgentSec-Bench.

## Project layout

- `agentsec_scorecard/scorecard.py` — the scoring logic: overall score, per-category breakdown, and OWASP coverage counts, computed from AgentSec-Bench's `results.json`.
- `generate_scorecard.py` — CLI entry point that runs the scorer and outputs the scorecard.

## Not yet done

- NIST control mapping (currently OWASP only)
- Score trending across multiple runs over time
- Integration into AgentSec-Bench's own HTML report as a single combined view