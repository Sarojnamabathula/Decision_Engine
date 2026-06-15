class ActionSelector:
    @staticmethod
    def select(context: dict) -> dict:
        action = context.get("action")
        
        # Fallback if no rule matched
        if not action:
            context["action"] = "follow_up"
            context["reasons"].append("default_fallback")
            context["rule_triggered"] = "DEFAULT_FALLBACK"
            context["explanation_template"] = "No specific rules triggered. Defaulting to follow-up to gather more information."
            context["trace"].append("fallback_action_selected")
            
        # Final loop guard check (hard limit)
        if context.get("follow_up_count", 0) > 4 and context["action"] == "follow_up":
            context["action"] = "end_interview"
            context["reasons"].append("hard_loop_guard_triggered")
            context["trace"].append("hard_loop_guard_applied")
            context["explanation_template"] = "Hard limit on follow-ups reached. Ending interview."
            
        context["trace"].append("action_selected")
        return context
