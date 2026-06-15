from core.engine import DecisionEngine
from services.logging_service import logger
from services.metrics_service import metrics_service
from rules.registry import registry

engine = DecisionEngine()

def get_engine() -> DecisionEngine:
    return engine

def get_logger():
    return logger

def get_metrics():
    return metrics_service

def get_registry():
    return registry
