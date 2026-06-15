import random
import uuid
from schemas.request import DecisionRequest
from core.engine import DecisionEngine

class SimulationEngine:
    def __init__(self, decision_engine: DecisionEngine):
        self.engine = decision_engine
        
    def run_persona(self, persona, max_turns=10):
        session_id = f"sim_{persona.name}_{str(uuid.uuid4())[:8]}"
        history = []
        fatigue = 0.0
        follow_up_count = 0
        
        for turn in range(1, max_turns + 1):
            # Generate inputs based on persona
            score = min(1.0, max(0.0, random.gauss(persona.base_score, persona.score_variance)))
            confidence = min(1.0, max(0.0, score - random.uniform(0, persona.confidence_gap)))
            fatigue = min(1.0, fatigue + persona.fatigue_rate)
            contradiction = random.random() < persona.contradiction_prob
            
            # Nervous candidate takes longer
            if persona.name == "NervousCandidate":
                response_time = random.uniform(45.0, 150.0)
                sentiment = "neutral"
            else:
                response_time = random.uniform(15.0, 60.0)
                sentiment = random.choice(["positive", "neutral"])

            request = DecisionRequest(
                score=score,
                confidence=confidence,
                question_type="technical",
                candidate_fatigue=fatigue,
                contradiction_detected=contradiction,
                attempts=1,
                follow_up_count=follow_up_count,
                response_time=response_time,
                answer_length=random.randint(50, 300),
                topic_relevance=min(1.0, score + 0.1),
                sentiment=sentiment,
                question_difficulty="medium",
                session_id=session_id
            )
            
            response = self.engine.process_decision(request)
            
            history.append({
                "turn": turn,
                "request": request.model_dump(),
                "response": response.model_dump()
            })
            
            if response.action == "follow_up":
                follow_up_count += 1
            else:
                follow_up_count = 0
                
            if response.action == "end_interview":
                break
                
        return {"session_id": session_id, "persona": persona.name, "history": history}
