from datetime import datetime, timezone
from schemas.response import DecisionResponse

class ExplainabilityLayer:
    @staticmethod
    def build(context: dict) -> DecisionResponse:
        # Generate dynamic explanation if none provided or it needs formatting
        explanation = context.get("explanation_template", "")
        if not explanation:
            explanation = f"Action {context.get('action')} was selected based on rule {context.get('rule_triggered')}."
            
        # Insert trace event
        if "trace" not in context:
            context["trace"] = []
        context["trace"].append("explanation_generated")
        
        return DecisionResponse(
            action=context.get("action", "unknown"),
            composite_score=round(context.get("composite_score", 0.0), 3),
            confidence_level=context.get("confidence_level", "unknown"),
            reasons=context.get("reasons", []),
            decision_trace=context.get("trace", []),
            rule_triggered=context.get("rule_triggered"),
            explanation=explanation,
            session_id=context.get("session_id"),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
