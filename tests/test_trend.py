import json
import os
from agentsec_scorecard.trend import ScoreHistory


def _cleanup(path):
    if os.path.exists(path):
        os.remove(path)


def test_first_run_has_no_trend():
    path = "test_history_1.json"
    _cleanup(path)
    history = ScoreHistory(path=path)
    history.record({"overall_score": 80.0, "score_by_category": {"prompt_injection": 90.0}, "total_scenarios_run": 9})
    assert history.trend() is None
    _cleanup(path)


def test_trend_detects_improvement():
    path = "test_history_2.json"
    _cleanup(path)
    history = ScoreHistory(path=path)
    history.record({"overall_score": 70.0, "score_by_category": {"prompt_injection": 60.0}, "total_scenarios_run": 9})
    history.record({"overall_score": 85.0, "score_by_category": {"prompt_injection": 75.0}, "total_scenarios_run": 9})
    trend = history.trend()
    assert trend is not None
    assert trend["overall_score_delta"] == 15.0
    assert trend["category_score_deltas"]["prompt_injection"] == 15.0
    _cleanup(path)


def test_trend_detects_regression():
    path = "test_history_3.json"
    _cleanup(path)
    history = ScoreHistory(path=path)
    history.record({"overall_score": 90.0, "score_by_category": {}, "total_scenarios_run": 9})
    history.record({"overall_score": 80.0, "score_by_category": {}, "total_scenarios_run": 9})
    trend = history.trend()
    assert trend["overall_score_delta"] == -10.0
    _cleanup(path)


def test_history_persists_across_instances():
    path = "test_history_4.json"
    _cleanup(path)
    ScoreHistory(path=path).record({"overall_score": 50.0, "score_by_category": {}, "total_scenarios_run": 5})
    reloaded = ScoreHistory(path=path)
    assert len(reloaded.load()) == 1
    _cleanup(path)