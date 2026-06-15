# AI Interview Decision Engine: Architecture

The Decision Engine is the Core Intelligence Controller of the AI interview platform. It evaluates multi-dimensional signals from an interview and deterministically calculates the optimal next action (`next_question`, `follow_up`, or `end_interview`).

## High-Level Pipeline

The system is built as a pure function pipeline (`ContextProcessor -> ScoringEngine -> ConfidenceAnalyzer -> RuleEvaluator -> ActionSelector -> ExplainabilityLayer`).

### 1. ContextProcessor
**Goal:** Input normalization and signal extraction.
Normalizes incoming payload (e.g., standardizing `sentiment` to `sentiment_score`), bounds constraints, flags obvious noise, and ensures all fields are initialized.

### 2. ScoringEngine
**Goal:** Compute the composite candidate score.
Applies weighted heuristics to calculate a unified `composite_score` taking into account the raw score, topic relevance, sentiment, question difficulty, and timing.

### 3. ConfidenceAnalyzer
**Goal:** Assess evaluator signal reliability.
Categorizes confidence and identifies if the signals fall within the "Uncertainty Zone" (a large gap between actual score and evaluator confidence).

### 4. RuleEvaluator (The Brain)
**Goal:** Apply deterministic, business-logic rules.
Processes a priority-ordered list of declarative YAML rules (e.g., `LOOP_GUARD`, `HIGH_FATIGUE`, `STRONG_ANSWER`). The highest priority rule whose conditions match the context dictates the action.

### 5. ActionSelector
**Goal:** Hard limits and fallbacks.
If no rules match, it defaults to a fallback (`follow_up`). It also enforces absolute hard loop guards (e.g., forcing `end_interview` if follow-ups exceed 4), regardless of rule execution.

### 6. ExplainabilityLayer
**Goal:** Construct the transparent response.
Packages the final action, the triggered rule, and the comprehensive decision trace (a list of all operational steps the pipeline took) into the final API payload for full transparency.

## Tech Stack
- **Framework:** FastAPI
- **Validation:** Pydantic
- **Testing:** Pytest
- **Config:** YAML, Pydantic-Settings
