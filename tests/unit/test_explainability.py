import pytest
from core.explainability import ExplainabilityLayer

def test_explainability_dynamic_template():
    context = {
        "action": "follow_up",
        "composite_score": 0.75,
        "confidence_level": "medium",
        "reasons": ["test_reason"],
        "trace": ["step1"],
        "rule_triggered": "TEST_RULE",
        "explanation_template": "",
        "session_id": "123"
    }
    resp = ExplainabilityLayer.build(context)
    assert "TEST_RULE" in resp.explanation
    assert resp.action == "follow_up"

def test_explainability_static_template():
    context = {
        "action": "next_question",
        "composite_score": 0.95,
        "confidence_level": "high",
        "reasons": ["strong"],
        "trace": ["step1"],
        "rule_triggered": "STRONG_RULE",
        "explanation_template": "Strong candidate rule hit.",
        "session_id": "123"
    }
    resp = ExplainabilityLayer.build(context)
    assert resp.explanation == "Strong candidate rule hit."
    assert "explanation_generated" in resp.decision_trace

def test_explainability_rounding():
    context = {
        "composite_score": 0.812345
    }
    resp = ExplainabilityLayer.build(context)
    assert resp.composite_score == 0.812

def test_explainability_defaults():
    context = {}
    resp = ExplainabilityLayer.build(context)
    assert resp.action == "unknown"
    assert resp.composite_score == 0.0
    
def test_explainability_timestamp():
    context = {}
    resp = ExplainabilityLayer.build(context)
    assert resp.timestamp is not None
