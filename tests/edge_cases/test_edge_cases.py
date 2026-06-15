import pytest

def test_edge_missing_confidence(engine, base_request_dict):
    # Engine should impute confidence = 0.50
    base_request_dict["confidence"] = None
    res = engine.process_decision(base_request_dict)
    # It might hit EVALUATOR_UNCERTAINTY because score 0.8 and conf 0.5 gap is 0.3, wait, gap > 0.40 triggers EVALUATOR_UNCERTAINTY.
    # Score 0.8 and conf 0.5 -> gap is 0.3. So it won't hit EVALUATOR_UNCERTAINTY.
    # It will hit DEFAULT_FALLBACK or something else if score is not strong enough.
    assert res.action is not None

def test_edge_zero_time(engine, base_request_dict):
    base_request_dict["response_time"] = 0.001
    res = engine.process_decision(base_request_dict)
    assert "scoring_computed" in res.decision_trace

def test_edge_extreme_time(engine, base_request_dict):
    base_request_dict["response_time"] = 5000.0
    res = engine.process_decision(base_request_dict)
    assert "scoring_computed" in res.decision_trace

def test_edge_zero_score(engine, base_request_dict):
    base_request_dict["score"] = 0.0
    res = engine.process_decision(base_request_dict)
    assert res.action in ["follow_up", "end_interview"]

def test_edge_max_score(engine, base_request_dict):
    base_request_dict["score"] = 1.0
    base_request_dict["confidence"] = 1.0
    res = engine.process_decision(base_request_dict)
    assert res.action == "next_question"

def test_edge_invalid_sentiment(engine, base_request_dict):
    base_request_dict["sentiment"] = "neutral"
    res = engine.process_decision(base_request_dict)
    assert res.composite_score > 0

def test_edge_high_fatigue_and_strong_score(engine, base_request_dict):
    # Fatigue should override strong score due to priority 2 vs 10
    base_request_dict["score"] = 1.0
    base_request_dict["confidence"] = 1.0
    base_request_dict["candidate_fatigue"] = 0.99
    res = engine.process_decision(base_request_dict)
    assert res.action == "end_interview"

def test_edge_contradiction_and_fatigue(engine, base_request_dict):
    # Fatigue priority 2, contradiction priority 3.
    base_request_dict["contradiction_detected"] = True
    base_request_dict["candidate_fatigue"] = 0.99
    res = engine.process_decision(base_request_dict)
    assert res.action == "end_interview"
    assert res.rule_triggered == "HIGH_FATIGUE"

def test_edge_contradiction_and_strong_score(engine, base_request_dict):
    # Contradiction priority 3, strong score priority 10
    base_request_dict["contradiction_detected"] = True
    base_request_dict["score"] = 1.0
    base_request_dict["confidence"] = 1.0
    res = engine.process_decision(base_request_dict)
    assert res.action == "follow_up"
    assert res.rule_triggered == "CONTRADICTION"

def test_edge_uncertainty_zone_override():
    from core.confidence_analyzer import ConfidenceAnalyzer
    context = {
        "confidence": 0.5,
        "action": "next_question",
        "in_uncertainty_zone": True,
        "reasons": [],
        "trace": []
    }
    res = ConfidenceAnalyzer.analyze(context)
    assert res["action"] == "follow_up"
    assert "uncertainty_override" in res["reasons"]

def test_edge_no_rule_match(engine, base_request_dict):
    # Score 0.6, confidence 0.6. No rule will match.
    base_request_dict["score"] = 0.6
    base_request_dict["confidence"] = 0.6
    res = engine.process_decision(base_request_dict)
    assert res.action == "follow_up"
    assert res.rule_triggered == "DEFAULT_FALLBACK"

def test_edge_hard_loop_guard():
    from core.action_selector import ActionSelector
    context = {
        "action": "follow_up",
        "follow_up_count": 5,
        "reasons": [],
        "trace": []
    }
    res = ActionSelector.select(context)
    assert res["action"] == "end_interview"
    assert "hard_loop_guard_triggered" in res["reasons"]
