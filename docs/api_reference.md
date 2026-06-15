# API Reference

The Decision Engine is accessible via a RESTful JSON API powered by FastAPI.

## `POST /api/v1/decide`
Evaluates an incoming interview signal and determines the next action.

**Request Payload (`DecisionRequest`)**
```json
{
  "session_id": "req-1234",
  "score": 0.85,
  "confidence": 0.90,
  "topic_relevance": 0.95,
  "sentiment": "positive",
  "response_time": 45.5,
  "follow_up_count": 0,
  "attempts": 1,
  "candidate_fatigue": 0.10,
  "contradiction_detected": false,
  "question_difficulty": "medium",
  "question_type": "technical",
  "evaluator_type": "llm"
}
```

**Response Payload (`DecisionResponse`)**
```json
{
  "action": "next_question",
  "composite_score": 0.825,
  "confidence_level": "high",
  "reasons": [
    "strong_confident_answer"
  ],
  "decision_trace": [
    "input_normalized",
    "scoring_computed",
    "evaluating_rule_LOOP_GUARD",
    "evaluating_rule_HIGH_FATIGUE",
    "evaluating_rule_CONTRADICTION",
    "rule_matched_STRONG_ANSWER",
    "confidence_analyzed",
    "action_selected",
    "explanation_generated"
  ],
  "rule_triggered": "STRONG_ANSWER",
  "explanation": "Candidate demonstrated strong understanding with high evaluator confidence.",
  "session_id": "req-1234",
  "timestamp": "2023-10-27T10:00:00Z"
}
```

## `GET /api/v1/health`
Checks API and rule registry health.

## `GET /api/v1/metrics`
Returns system observability metrics including decision distributions and rule hit rates.

## `GET /api/v1/rules`
Returns the currently loaded deterministic rule schema.
