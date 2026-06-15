from dataclasses import dataclass

@dataclass
class Persona:
    name: str
    base_score: float
    score_variance: float
    fatigue_rate: float
    confidence_gap: float
    contradiction_prob: float

personas = {
    "StrongCandidate": Persona("StrongCandidate", 0.85, 0.05, 0.02, 0.05, 0.01),
    "WeakCandidate": Persona("WeakCandidate", 0.35, 0.10, 0.05, 0.15, 0.20),
    "FatiguedCandidate": Persona("FatiguedCandidate", 0.80, 0.10, 0.15, 0.10, 0.05),
    "InconsistentCandidate": Persona("InconsistentCandidate", 0.60, 0.30, 0.05, 0.25, 0.30),
    "NervousCandidate": Persona("NervousCandidate", 0.70, 0.15, 0.05, 0.20, 0.05),
    "BorderlineCandidate": Persona("BorderlineCandidate", 0.55, 0.10, 0.05, 0.10, 0.10),
}
