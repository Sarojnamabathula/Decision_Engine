from pydantic import BaseModel
from typing import List, Optional

class DecisionResponse(BaseModel):
    action: str
    composite_score: float
    confidence_level: str
    reasons: List[str]
    decision_trace: List[str]
    rule_triggered: Optional[str]
    explanation: str
    session_id: Optional[str]
    timestamp: str
