class ScoringEngine:
    @staticmethod
    def compute(context: dict) -> dict:
        W_score = 0.40
        W_conf = 0.20
        W_relevance = 0.20
        W_sentiment = 0.10
        W_time = 0.10
        
        # Time score normalization: peak around 10-60 seconds, penalize extremes
        rt = context["response_time"]
        if rt < 5:
            time_score = 0.2
        elif rt > 180:
            time_score = max(0.0, 1.0 - (rt - 180) / 120.0)
        else:
            time_score = 1.0
            
        composite = (
            (W_score * context["score"]) +
            (W_conf * context["confidence"]) +
            (W_relevance * context["topic_relevance"]) +
            (W_sentiment * context["sentiment_score"]) +
            (W_time * time_score)
        )
        
        # Difficulty multiplier
        difficulty_multiplier = {"easy": 1.0, "medium": 0.95, "hard": 0.88}
        adjusted_composite = composite * difficulty_multiplier.get(context["question_difficulty"], 1.0)
        
        # Uncertainty band
        gap = abs(context["score"] - context["confidence"])
        in_uncertainty_zone = gap > 0.35
        
        context["composite_score"] = adjusted_composite
        context["score_confidence_gap"] = gap
        context["in_uncertainty_zone"] = in_uncertainty_zone
        
        context["trace"].append("scoring_computed")
        return context
