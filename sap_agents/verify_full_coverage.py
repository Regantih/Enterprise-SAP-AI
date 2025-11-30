import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def test_full_coverage():
    print("Initializing Orchestrator...")
    orchestrator = OrchestratorAgent()
    
    test_cases = [
        ("Manufacturing (PP)", "Check status of PO-1001"),
        ("Asset Management (EAM)", "Check status of EQ-5001"),
        ("Customer Service (CS)", "Check status of TKT-3001")
    ]
    
    for domain, prompt in test_cases:
        print(f"\n--- Testing {domain} ---")
        print(f"Prompt: {prompt}")
        
        plan = orchestrator.plan(prompt, user_id="plant_manager")
        print(f"Plan Agent: {plan['steps'][0].get('agent_criteria', 'Unknown')}")
        
        response = orchestrator.execute()
        print("Response Snippet:", response.split('\n')[0]) # Print first line
        
        if "Critical Execution Error" in response:
            print("❌ Test Failed!")
        else:
            print("✅ Test Passed!")

if __name__ == "__main__":
    test_full_coverage()
