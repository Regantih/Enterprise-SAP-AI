import argparse
import json
from athena_system.agents.hephaestus import HephaestusAgent

def run_delivery_workflow(project_description):
    print(f"🚀 Starting POTENTIAL-X Delivery Workflow for: '{project_description}'")
    
    hephaestus = HephaestusAgent()
    
    # 1. Risk Profiling (P - Profile)
    print("\n--- Step 1: Risk Profiling ---")
    risk_profile = hephaestus.generate_risk_profile(project_description)
    print(json.dumps(risk_profile, indent=2))
    
    # 2. Governance Design (O - Orchestrate)
    print("\n--- Step 2: Governance Design ---")
    charter = hephaestus.generate_governance_charter(risk_profile)
    print(charter)

    print("\n✅ Delivery Workflow Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run POTENTIAL-X Delivery Workflow')
    parser.add_argument('--project', type=str, required=True, help='Project Description')
    args = parser.parse_args()
    
    run_delivery_workflow(args.project)
