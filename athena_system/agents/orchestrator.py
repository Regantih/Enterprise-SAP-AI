import json
import os
import sys
from datetime import datetime

# Path to the new registry
REGISTRY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'registry.json')

class OrchestratorAgent:
    def __init__(self):
        self.registry = self._load_registry()
        self.trace_log = []

    def _load_registry(self):
        try:
            with open(REGISTRY_PATH, 'r') as f:
                return json.load(f)['agents']
        except FileNotFoundError:
            print(f"⚠️ Registry not found at {REGISTRY_PATH}")
            return []

    def _log(self, step, details):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "details": details
        }
        self.trace_log.append(entry)

    def find_best_agent(self, task_description):
        """
        Deterministic selection of agent based on keyword matching.
        """
        self._log("Agent Selection", f"Searching for agent to handle: {task_description}")
        
        best_agent = None
        highest_score = 0
        
        task_words = set(task_description.lower().split())
        
        domain_keywords = {
            "Legal": ["nda", "contract", "agreement", "compliance", "sue", "lawsuit", "regulation"],
            "Finance": ["audit", "tax", "budget", "revenue", "expense", "cost", "profit"],
            "HR": ["hiring", "onboarding", "payroll", "benefits", "employee", "interview"],
            "Supply Chain": ["logistics", "shipment", "inventory", "supplier", "procurement"],
            "Sales": ["lead", "customer", "deal", "pipeline", "churn", "revenue"],
            "IT": ["server", "cloud", "network", "security", "patch", "outage"],
            "R&D": ["patent", "prototype", "innovation", "research", "feasibility"],
            "Manufacturing": ["production", "quality", "yield", "maintenance", "factory"]
        }

        for agent in self.registry:
            score = 0
            # Score based on category match
            if agent['category'].lower() in task_description.lower():
                score += 5
            # Score based on name match
            if agent['name'].lower() in task_description.lower():
                score += 10
            # Score based on description keywords
            desc_words = set(agent['description'].lower().split())
            common = task_words.intersection(desc_words)
            score += len(common)
            
            # Score based on domain keywords (Semantic Mapping)
            for keyword in domain_keywords.get(agent['category'], []):
                if keyword in task_description.lower():
                    score += 15
            
            if score > highest_score:
                highest_score = score
                best_agent = agent
        
        if best_agent:
            self._log("Agent Selected", f"Selected '{best_agent['name']}' (ID: {best_agent['id']}) with score {highest_score}")
            return best_agent
        else:
            self._log("Agent Selection Failed", "No suitable agent found.")
            return None

    def route_request(self, prompt):
        """
        Simulates routing a request to the best agent.
        """
        agent = self.find_best_agent(prompt)
        if agent:
            return {
                "status": "success",
                "agent": agent['name'],
                "category": agent['category'],
                "message": f"Routed to {agent['name']} for execution."
            }
        else:
            return {
                "status": "failure",
                "message": "No suitable agent found."
            }
