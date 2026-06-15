class RuleHandlers:
    @staticmethod
    def evaluate_condition(context: dict, field: str, constraints: dict) -> bool:
        if field not in context:
            return False
            
        val = context[field]
        for op, target in constraints.items():
            if op == "gte" and not (val >= target): return False
            if op == "lte" and not (val <= target): return False
            if op == "gt" and not (val > target): return False
            if op == "lt" and not (val < target): return False
            if op == "eq" and not (val == target): return False
            if op == "neq" and not (val != target): return False
        return True

    @staticmethod
    def evaluate_rule(context: dict, rule: dict) -> bool:
        conditions = rule.get("condition", {})
        for field, constraints in conditions.items():
            if not RuleHandlers.evaluate_condition(context, field, constraints):
                return False
        return True
