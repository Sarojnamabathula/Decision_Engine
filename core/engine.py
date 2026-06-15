from schemas.request import DecisionRequest
from schemas.response import DecisionResponse
from .context_processor import ContextProcessor
from .scoring import ScoringEngine
from .rule_evaluator import RuleEvaluator
from .confidence_analyzer import ConfidenceAnalyzer
from .action_selector import ActionSelector
from .explainability import ExplainabilityLayer

class DecisionEngine:
    def process_decision(self, request: DecisionRequest) -> DecisionResponse:
        # Step 1: Normalize & Enqueue
        context = ContextProcessor.process(request)
        
        # Step 2: Compute composite score and uncertainty
        context = ScoringEngine.compute(context)
        
        # Step 3: Evaluate against externalized rules
        context = RuleEvaluator.evaluate(context)
        
        # Step 4: Calibrate signal reliability
        context = ConfidenceAnalyzer.analyze(context)
        
        # Step 5: Determine final action & fallback
        context = ActionSelector.select(context)
        
        # Step 6: Construct explainability trace
        response = ExplainabilityLayer.build(context)
        
        return response
