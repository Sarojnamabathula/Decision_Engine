from .loader import RuleLoader

class RuleRegistry:
    def __init__(self):
        self.rules = []

    def initialize(self, file_path: str):
        self.rules = RuleLoader.load_rules(file_path)
        # Sort rules by priority (lowest number = highest priority)
        self.rules.sort(key=lambda r: r.get("priority", 999))

    def get_rules(self):
        return self.rules

registry = RuleRegistry()
