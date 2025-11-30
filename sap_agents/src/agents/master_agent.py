import json
import os
import sys
import importlib.util

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.procurement_agent import create_procurement_agent, run_offline_agent

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'registry.json')

def load_registry():
    with open(REGISTRY_PATH, 'r') as f:
        return json.load(f)

def get_agent_metadata(agent_id):
    registry = load_registry()
    for agent in registry['agents']:
        if agent['id'] == agent_id:
            return agent
    return None

def run_generic_agent(agent_meta, prompt):
    """
    A generic agent that simulates behavior based on metadata.
    """
    return {
        "output": f"[{agent_meta['name']}] I have received your request: '{prompt}'.\n\n"
                  f"As a specialist in {agent_meta['category']}, I am analyzing the data...\n"
                  f"Based on my role as {agent_meta['description']}, here is the result: [Simulated Output]"
    }

def route_request(agent_id, prompt):
    print(f"Routing request to Agent ID: {agent_id}")
    
    # 1. Check if it's the specific Pilot Agent
    if agent_id == "procurementnegotiationassistant":
        print(">> Activating Procurement Negotiation Assistant")
        # Try to run the real/mock procurement agent
        executor = create_procurement_agent()
        if executor:
            try:
                res = executor.invoke({"input": prompt})
                return res
            except Exception as e:
                return {"output": f"Error running agent: {str(e)}"}
        else:
            # Fallback to offline function if create_procurement_agent returns None (no API key)
            return run_offline_agent(prompt)

    # 2. Check if it's a valid agent from registry
    meta = get_agent_metadata(agent_id)
    if meta:
        print(f">> Activating Generic Agent: {meta['name']}")
        return run_generic_agent(meta, prompt)
    
    return {"output": f"Error: Agent ID '{agent_id}' not found in registry."}

if __name__ == "__main__":
    # Simple CLI test
    if len(sys.argv) > 2:
        aid = sys.argv[1]
        p = sys.argv[2]
        print(route_request(aid, p))
    else:
        print("Usage: python master_agent.py <agent_id> <prompt>")
