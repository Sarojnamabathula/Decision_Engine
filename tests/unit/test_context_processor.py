import pytest
from core.context_processor import ContextProcessor
from schemas.request import DecisionRequest

def test_context_processor_normalizes_sentiment(base_request_dict):
    base_request_dict["sentiment"] = "positive"
    req = DecisionRequest(**base_request_dict)
    ctx = ContextProcessor.process(req)
    assert ctx["sentiment_score"] == 1.0

def test_context_processor_imputes_confidence(base_request_dict):
    base_request_dict["confidence"] = None
    req = DecisionRequest(**base_request_dict)
    ctx = ContextProcessor.process(req)
    assert ctx["confidence"] == 0.50

def test_context_processor_flags_fast_noise(base_request_dict):
    base_request_dict["response_time"] = 0.5
    req = DecisionRequest(**base_request_dict)
    ctx = ContextProcessor.process(req)
    assert ctx["is_noisy"] is True

def test_context_processor_flags_slow_noise(base_request_dict):
    base_request_dict["response_time"] = 350.0
    req = DecisionRequest(**base_request_dict)
    ctx = ContextProcessor.process(req)
    assert ctx["is_noisy"] is True

def test_context_processor_no_noise(base_request_dict):
    base_request_dict["response_time"] = 30.0
    req = DecisionRequest(**base_request_dict)
    ctx = ContextProcessor.process(req)
    assert ctx["is_noisy"] is False

def test_context_processor_adds_trace(base_request):
    ctx = ContextProcessor.process(base_request)
    assert "input_normalized" in ctx["trace"]
