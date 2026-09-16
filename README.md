# AgentSec-Scorecard

Standardized security scoring and reporting for AI agent evaluation results.

## Status

Architecture design phase. Not yet implemented.

AgentSec-Scorecard is designed to consume the results.json output from
[AgentSec-Bench](https://github.com/samyshyaka/agentsec-bench) and produce a
standardized, comparable security score across agents and scenarios, with
mappings to recognized frameworks (NIST, OWASP).

AgentSec-Bench's own HTML report generator is currently the working prototype
of this idea; Scorecard will generalize it into a standalone tool once
Bench's result schema is stable across more scenarios.

Implementation will begin once AgentSec-Bench has broader scenario coverage.