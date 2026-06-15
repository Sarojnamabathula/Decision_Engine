from rules.registry import registry
from rules.handlers import RuleHandlers

class RuleEvaluator:
    @staticmethod
    def evaluate(context: dict) -> dict:
        context["reasons"] = []
        rules = registry.get_rules()
        
        for rule in rules:
            context["trace"].append(f"evaluating_rule_{rule['id']}")
            if RuleHandlers.evaluate_rule(context, rule):
                context["action"] = rule["action"]
                context["rule_triggered"] = rule["id"]
                context["reasons"].append(rule["reason"])
                context["explanation_template"] = rule.get("explanation", "")
                context["trace"].append(f"rule_matched_{rule['id']}")
                return context
                
        context["trace"].append("no_rule_matched")
        return context
