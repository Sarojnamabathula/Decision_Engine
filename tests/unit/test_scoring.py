import pytest
from core.scoring import ScoringEngine

def test_scoring_high_quality():
    context = {"score": 0.9, "confidence": 0.9, "topic_relevance": 0.9, "sentiment_score": 1.0, "response_time": 30.0, "question_difficulty": "medium", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["composite_score"] > 0.8
    assert res["in_uncertainty_zone"] is False

def test_scoring_low_quality():
    context = {"score": 0.2, "confidence": 0.9, "topic_relevance": 0.2, "sentiment_score": 0.0, "response_time": 30.0, "question_difficulty": "medium", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["composite_score"] < 0.5
    assert res["in_uncertainty_zone"] is True # 0.9 - 0.2 = 0.7 > 0.35

def test_scoring_fast_response():
    context = {"score": 0.9, "confidence": 0.9, "topic_relevance": 0.9, "sentiment_score": 1.0, "response_time": 2.0, "question_difficulty": "medium", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["composite_score"] < 0.85 # Penalized for fast time

def test_scoring_slow_response():
    context = {"score": 0.9, "confidence": 0.9, "topic_relevance": 0.9, "sentiment_score": 1.0, "response_time": 250.0, "question_difficulty": "medium", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["composite_score"] < 0.85 # Penalized for slow time

def test_difficulty_easy():
    context = {"score": 0.9, "confidence": 0.9, "topic_relevance": 0.9, "sentiment_score": 1.0, "response_time": 30.0, "question_difficulty": "easy", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["composite_score"] > 0.85

def test_difficulty_hard():
    context = {"score": 0.9, "confidence": 0.9, "topic_relevance": 0.9, "sentiment_score": 1.0, "response_time": 30.0, "question_difficulty": "hard", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["composite_score"] < 0.85

def test_uncertainty_zone():
    context = {"score": 0.5, "confidence": 0.9, "topic_relevance": 0.5, "sentiment_score": 0.5, "response_time": 30.0, "question_difficulty": "medium", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["in_uncertainty_zone"] is True

def test_certainty_zone():
    context = {"score": 0.5, "confidence": 0.5, "topic_relevance": 0.5, "sentiment_score": 0.5, "response_time": 30.0, "question_difficulty": "medium", "trace": []}
    res = ScoringEngine.compute(context)
    assert res["in_uncertainty_zone"] is False
