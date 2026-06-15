class MetricsService:
    def __init__(self):
        self.decision_counts = {"next_question": 0, "follow_up": 0, "end_interview": 0}
        self.rule_hits = {}
        self.total_decisions = 0
        
    def record_decision(self, response):
        self.total_decisions += 1
        action = response.action
        if action in self.decision_counts:
            self.decision_counts[action] += 1
            
        rule = response.rule_triggered
        if rule:
            self.rule_hits[rule] = self.rule_hits.get(rule, 0) + 1
            
    def get_metrics(self):
        return {
            "total_decisions": self.total_decisions,
            "decision_counts": self.decision_counts,
            "rule_hits": self.rule_hits
        }

metrics_service = MetricsService()
