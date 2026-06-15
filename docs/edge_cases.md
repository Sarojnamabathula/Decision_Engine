# Edge Cases & Guardrails

The Decision Engine employs robust safety mechanisms to ensure an AI interview remains fluid, productive, and user-friendly, even when the LLM evaluators generate erratic signals.

## 1. Infinite Clarification Loops
**Problem:** The LLM repeatedly asks follow-ups because it is perpetually uncertain.
**Solution:** `LOOP_GUARD` (Rule #1). If `follow_up_count` hits 3, the engine forces the interview to end. A secondary hard guardrail in the `ActionSelector` physically blocks any follow-ups past 4, bypassing the rules entirely as an ultimate safety net.

## 2. Candidate Fatigue
**Problem:** Long, intense interviews cause candidate performance to decay.
**Solution:** `HIGH_FATIGUE` (Rule #2). Overrides excellent scores to end the interview early if the extracted `candidate_fatigue` vector hits critical mass (>= 0.85).

## 3. The "Uncertainty Zone"
**Problem:** An LLM might grant a high score (0.90) but tag it with extremely low confidence (0.40) because it hallucinated or failed to parse the transcript context.
**Solution:** `ConfidenceAnalyzer` automatically monitors the gap between score and confidence. If the gap exceeds 0.35, the system intercepts any `next_question` actions and forces a `follow_up` to stabilize the context.

## 4. Signal Noise
**Problem:** Impossible inputs like a response time of 0.001 seconds or missing confidence metrics.
**Solution:** `ContextProcessor` normalizes all missing parameters to safe mathematical defaults (e.g., Confidence -> 0.50) and tags extreme speed or stalling as `fast_response_noise` to penalize the composite score dynamically.
