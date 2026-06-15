import argparse
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import DecisionEngine
from rules.registry import registry
from configs.settings import settings
from simulations.personas import personas
from simulations.engine import SimulationEngine

def run_simulation(persona_name):
    registry.initialize(settings.rules_file_path)
    engine = DecisionEngine()
    sim_engine = SimulationEngine(engine)
    
    if persona_name == "all":
        target_personas = personas.values()
    else:
        if persona_name not in personas:
            print(f"Persona '{persona_name}' not found.")
            sys.exit(1)
        target_personas = [personas[persona_name]]
        
    for persona in target_personas:
        print(f"\n--- Running Simulation for {persona.name} ---")
        result = sim_engine.run_persona(persona)
        for step in result["history"]:
            print(f"Turn {step['turn']}: Score={step['request']['score']:.2f}, Action={step['response']['action']}, Rule={step['response']['rule_triggered']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI Interview Simulations")
    parser.add_argument("--persona", type=str, default="all", help="Persona name to run (or 'all')")
    args = parser.parse_args()
    run_simulation(args.persona)
