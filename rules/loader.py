import yaml
import os

class RuleLoader:
    @staticmethod
    def load_rules(file_path: str) -> list:
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, file_path)
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Rules file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get("rules", [])
