class ConfidenceAnalyzer:
    @staticmethod
    def analyze(context: dict) -> dict:
        # Assess overall signal reliability
        conf = context["confidence"]
        
        if conf >= 0.8:
            conf_level = "high"
        elif conf >= 0.5:
            conf_level = "medium"
        elif conf >= 0.3:
            conf_level = "low"
        else:
            conf_level = "very_low"
            
        context["confidence_level"] = conf_level
        
        # If uncertainty exceeds threshold, we might adjust action
        if context["in_uncertainty_zone"] and context.get("action") == "next_question":
            # Override high certainty action if we are actually in uncertainty zone
            context["action"] = "follow_up"
            context["reasons"].append("uncertainty_override")
            context["trace"].append("uncertainty_override_applied")
        
        context["trace"].append("confidence_analyzed")
        return context
