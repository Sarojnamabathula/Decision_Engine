import pytest
from core.engine import DecisionEngine
from rules.registry import registry
from configs.settings import settings
from schemas.request import DecisionRequest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def setup_rules():
    registry.initialize(settings.rules_file_path)
    
@pytest.fixture
def engine():
    return DecisionEngine()

@pytest.fixture
def base_request_dict():
    return {
        "score": 0.8,
        "confidence": 0.8,
        "question_type": "technical",
        "candidate_fatigue": 0.1,
        "contradiction_detected": False,
        "attempts": 1,
        "follow_up_count": 0,
        "response_time": 30.0,
        "answer_length": 150,
        "topic_relevance": 0.9,
        "sentiment": "positive",
        "question_difficulty": "medium",
        "session_id": "test_sess_1"
    }

@pytest.fixture
def base_request(base_request_dict):
    return DecisionRequest(**base_request_dict)

@pytest.fixture
def client():
    return TestClient(app)
