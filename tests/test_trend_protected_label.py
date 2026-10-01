import os
from agentsec_scorecard.trend import ScoreHistory


def _cleanup(path):
    if os.path.exists(path):
        os.remove(path)


def test_record_without_protected_defaults_to_none():
    path = "test_history_protected_1.json"
    _cleanup(path)
    history = ScoreHistory(path=path)
    entry = history.record({"overall_score": 80.0, "score_by_category": {}, "total_scenarios_run": 9})
    assert entry["protected"] is None
    _cleanup(path)


def test_record_with_protected_true_is_labeled():
    path = "test_history_protected_2.json"
    _cleanup(path)
    history = ScoreHistory(path=path)
    entry = history.record({"overall_score": 95.0, "score_by_category": {}, "total_scenarios_run": 9}, protected=True)
    assert entry["protected"] is True
    _cleanup(path)


def test_record_with_protected_false_is_labeled():
    path = "test_history_protected_3.json"
    _cleanup(path)
    history = ScoreHistory(path=path)
    entry = history.record({"overall_score": 60.0, "score_by_category": {}, "total_scenarios_run": 9}, protected=False)
    assert entry["protected"] is False
    _cleanup(path)


def test_label_persists_across_instances():
    path = "test_history_protected_4.json"
    _cleanup(path)
    ScoreHistory(path=path).record({"overall_score": 70.0, "score_by_category": {}, "total_scenarios_run": 5}, protected=True)
    reloaded = ScoreHistory(path=path)
    history = reloaded.load()
    assert len(history) == 1
    assert history[0]["protected"] is True
    _cleanup(path)


def test_existing_unlabeled_history_entries_still_load():
    # Backward compatibility: entries recorded before this field existed
    # have no "protected" key at all - load() must not choke on that.
    path = "test_history_protected_5.json"
    _cleanup(path)
    import json
    with open(path, "w") as f:
        json.dump([{"timestamp": "2026-01-01T00:00:00+00:00", "overall_score": 50.0, "score_by_category": {}, "total_scenarios_run": 5}], f)
    history = ScoreHistory(path=path)
    loaded = history.load()
    assert len(loaded) == 1
    assert "protected" not in loaded[0]
    _cleanup(path)
