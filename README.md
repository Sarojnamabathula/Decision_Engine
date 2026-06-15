# AI Interview Decision Engine

![Decision Engine Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen) ![FastAPI](https://img.shields.io/badge/Framework-FastAPI-blue) ![Test Coverage](https://img.shields.io/badge/Coverage-100%25-success)

The **AI Interview Decision Engine** is a deterministic, production-grade orchestration layer built for AI interview platforms. It acts as the "Core Intelligence Controller", interpreting multi-dimensional signals from an LLM Evaluator (scores, confidence, fatigue, timing) and determining the optimal next action in an interview sequence (`next_question`, `follow_up`, or `end_interview`).

## Key Features

- **Hybrid Intelligence Architecture:** Combines weighted heuristic scoring with a priority-ordered, declarative YAML rules engine.
- **Explainable AI (XAI):** Every decision generates a comprehensive `decision_trace` outlining the exact pipeline steps and the business rules triggered.
- **Robust Edge Case Handling:** Automatically intercepts infinite clarification loops, detects candidate fatigue, and forces follow-ups when the LLM enters an "Uncertainty Zone."
- **Simulation Tested:** Validated against 6 simulated candidate personas (Strong, Weak, Fatigued, Nervous, Inconsistent, Borderline).
- **Production Ready:** Built with FastAPI, Pydantic validation, structured JSON logging, and full test suite coverage (59 passing tests).

## Project Structure
```text
Decision_Engine/
├── api/             # FastAPI routing and DI
├── app/             # Application factory and middleware
├── configs/         # Environment variables and Settings schema
├── core/            # The 6-layer pipeline (Context, Scoring, Confidence, Rules, Action, XAI)
├── docs/            # Architecture, API Reference, and Onboarding guides
├── rules/           # YAML matrix and evaluator mechanics
├── schemas/         # Strict Pydantic I/O models
├── services/        # Singleton services (Logging, Metrics)
├── simulations/     # Multi-persona automated testing
└── tests/           # 59 Unit, Integration, and Edge Case tests
```

## Quick Start

1. **Clone & Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp configs/.env.example configs/.env
   ```

2. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```
   *Navigate to `http://127.0.0.1:8000/docs` to test endpoints.*

3. **Run the Test Suite:**
   ```bash
   python -m pytest tests/ -v
   ```

## Documentation

For a deep dive into the system mechanics, see the following documentation:
- [System Architecture](docs/architecture.md)
- [Rules Engine Guide](docs/rules_guide.md)
- [Edge Cases & Guardrails](docs/edge_cases.md)
- [API Reference](docs/api_reference.md)
- [Developer Onboarding](docs/onboarding.md)
