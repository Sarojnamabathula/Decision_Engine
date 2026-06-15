import pytest

def test_api_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_api_metrics(client):
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_decisions" in data

def test_api_rules(client):
    response = client.get("/api/v1/rules")
    assert response.status_code == 200
    data = response.json()
    assert "rules" in data
    assert len(data["rules"]) > 0

def test_api_decide_valid(client, base_request_dict):
    response = client.post("/api/v1/decide", json=base_request_dict)
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "next_question"
    assert "X-Request-ID" in response.headers

def test_api_decide_missing_fields(client):
    response = client.post("/api/v1/decide", json={"score": 0.5})
    assert response.status_code == 422 # Unprocessable Entity

def test_api_decide_invalid_score(client, base_request_dict):
    base_request_dict["score"] = 1.5 # Must be <= 1.0
    response = client.post("/api/v1/decide", json=base_request_dict)
    assert response.status_code == 422

def test_api_decide_invalid_type(client, base_request_dict):
    base_request_dict["question_type"] = "invalid"
    response = client.post("/api/v1/decide", json=base_request_dict)
    assert response.status_code == 422

def test_api_decide_records_metrics(client, base_request_dict):
    # Send request
    client.post("/api/v1/decide", json=base_request_dict)
    # Check metrics
    response = client.get("/api/v1/metrics")
    data = response.json()
    assert data["total_decisions"] > 0

def test_api_decide_correlation_id(client, base_request_dict):
    base_request_dict["session_id"] = "test_correlation"
    response = client.post("/api/v1/decide", json=base_request_dict)
    assert response.json()["session_id"] == "test_correlation"
