# Rules Engine Guide

The core intelligence of the system relies on a declarative, YAML-based rule matrix (`rules/rules.yaml`).

## Rule Structure
Rules are defined as an array of dictionaries.
- `id`: The unique identifier (e.g., `STRONG_ANSWER`).
- `priority`: Integer defining evaluation order. **Lower numbers are evaluated first.**
- `condition`: A dictionary of field thresholds using operators (`gte`, `lte`, `eq`, `neq`).
- `action`: The resulting decision if conditions are met (`next_question`, `follow_up`, `end_interview`).

## Current Rule Matrix

1. **`LOOP_GUARD` (Priority 1)**: Forces `end_interview` if `follow_up_count >= 3`. Protects against infinite clarification loops.
2. **`HIGH_FATIGUE` (Priority 2)**: Forces `end_interview` if candidate exhaustion metrics exceed critical thresholds.
3. **`CONTRADICTION` (Priority 3)**: Forces `follow_up` if a severe contradiction is detected in the candidate's answers.
4. **`STRONG_ANSWER` (Priority 10)**: Progresses the interview (`next_question`) if both `composite_score` and `confidence` are extremely high.
5. **`EVALUATOR_UNCERTAINTY` (Priority 15)**: Intercepts high scores that have low evaluator confidence by forcing a `follow_up`.
6. **`BORDERLINE_SCORE_LOW_CONFIDENCE` (Priority 20)**: Triggers clarification for mediocre answers with poor evaluator signal.
7. **`POOR_ANSWER` (Priority 25)**: Safely probes for more signal if the candidate entirely missed the mark.
8. **`DEFAULT_FALLBACK`**: Automatically applied by the Action Selector if no rules match. Default is `follow_up`.
