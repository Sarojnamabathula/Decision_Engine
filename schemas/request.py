from pydantic import BaseModel, Field
from typing import Optional, Literal

class DecisionRequest(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="Primary answer quality signal")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Evaluator certainty in its own score")
    question_type: Literal["technical", "behavioral", "situational"] = Field(..., description="Affects thresholds")
    candidate_fatigue: float = Field(..., ge=0.0, le=1.0, description="Physiological/temporal signal")
    contradiction_detected: bool = Field(..., description="Logical inconsistency flag from evaluator")
    attempts: int = Field(..., ge=1, description="Tries on current topic")
    follow_up_count: int = Field(..., ge=0, description="Consecutive follow-ups (loop guard)")
    response_time: float = Field(..., gt=0.0, description="Seconds to answer")
    answer_length: int = Field(..., gt=0, description="Token/word count")
    topic_relevance: float = Field(..., ge=0.0, le=1.0, description="Semantic relevance of answer to question")
    sentiment: Literal["positive", "neutral", "negative"] = Field(..., description="Sentiment of the answer")
    question_difficulty: Literal["easy", "medium", "hard"] = Field(..., description="Affects scoring weights")
    session_id: Optional[str] = Field(None, description="Correlation ID for audit logging")
