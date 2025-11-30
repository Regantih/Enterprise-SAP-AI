import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def test_analytics():
    print("Initializing Orchestrator...")
    orchestrator = OrchestratorAgent()
    
    prompt = "How is the business doing?"
    print(f"Planning for: {prompt}")
    
    plan = orchestrator.plan(prompt, user_id="cfo")
    print("Plan:", plan)
    
    print("Executing...")
    response = orchestrator.execute()
    print("Response:", response)

if __name__ == "__main__":
    test_analytics()
