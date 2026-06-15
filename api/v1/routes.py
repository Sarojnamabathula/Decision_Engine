from fastapi import APIRouter, Depends, HTTPException
from schemas.request import DecisionRequest
from schemas.response import DecisionResponse
from .dependencies import get_engine, get_logger, get_metrics, get_registry
from core.engine import DecisionEngine
from services.metrics_service import MetricsService
import time

router = APIRouter()

@router.post("/decide", response_model=DecisionResponse)
def decide(
    request: DecisionRequest,
    engine: DecisionEngine = Depends(get_engine),
    logger = Depends(get_logger),
    metrics: MetricsService = Depends(get_metrics)
):
    start_time = time.time()
    try:
        response = engine.process_decision(request)
        latency = (time.time() - start_time) * 1000
        
        metrics.record_decision(response)
        
        logger.info("decision_made", extra={
            "session_id": response.session_id,
            "action": response.action,
            "composite_score": response.composite_score,
            "rule_triggered": response.rule_triggered,
            "latency_ms": round(latency, 2)
        })
        return response
    except Exception as e:
        logger.error(f"Error processing decision: {str(e)}", extra={"session_id": request.session_id})
        raise HTTPException(status_code=500, detail="Internal server error during decision processing")

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/metrics")
def get_system_metrics(metrics: MetricsService = Depends(get_metrics)):
    return metrics.get_metrics()

@router.get("/rules")
def get_active_rules(registry = Depends(get_registry)):
    return {"rules": registry.get_rules()}
