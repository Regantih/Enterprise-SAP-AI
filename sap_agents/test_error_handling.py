import sys
import os
from unittest.mock import MagicMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def test_global_error_handling():
    print("Initializing Orchestrator...")
    orchestrator = OrchestratorAgent()
    
    # Monkey-patch _run_agent to raise an exception
    def crash_agent(agent, prompt):
        raise ValueError("Simulated Agent Crash!")
    
    orchestrator._run_agent = crash_agent
    
    prompt = "Check status of SO-5001"
    print(f"Planning for: {prompt}")
    
    # Create a dummy plan manually to skip planning phase
    orchestrator.current_plan = {
        "goal": prompt,
        "steps": [{"id": 1, "action": "delegate", "agent_criteria": "SalesOrderAssistant", "task": prompt}]
    }
    
    print("Executing (expecting graceful error)...")
    response = orchestrator.execute()
    print("Response:", response)
    
    if "Critical Execution Error" in response:
        print("✅ Global Error Handling Verified!")
    else:
        print("❌ Error Handling Failed!")

if __name__ == "__main__":
    test_global_error_handling()
