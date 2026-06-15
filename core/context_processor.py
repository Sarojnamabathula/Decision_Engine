from schemas.request import DecisionRequest

class ContextProcessor:
    @staticmethod
    def process(request: DecisionRequest) -> dict:
        if isinstance(request, dict):
            context = request.copy()
        else:
            context = request.model_dump()
        
        # Impute missing values
        if context["confidence"] is None:
            context["confidence"] = 0.50
            
        # Encode categoricals
        sentiment_map = {"positive": 1.0, "neutral": 0.5, "negative": 0.0}
        context["sentiment_score"] = sentiment_map.get(context["sentiment"], 0.5)
        
        # Flag noisy inputs (e.g. suspiciously fast or extremely slow response)
        noisy = False
        if context["response_time"] < 1.0 or context["response_time"] > 300.0:
            noisy = True
            
        context["is_noisy"] = noisy
        context["trace"] = ["input_normalized"]
        
        return context
