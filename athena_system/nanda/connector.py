import json
import random

class NANDAConnector:
    """
    Simulates interaction with the NANDA Decentralized Agent Registry.
    Enables 'External Democracy' by allowing Athena to discover and vote on external agents.
    """
    
    def __init__(self):
        # Mock Registry of External Agents
        self.registry = [
            {
                "id": "oracle-ai-predictor-v1",
                "name": "Oracle AI Forecaster",
                "capabilities": ["financial_forecasting", "supply_chain_prediction"],
                "reputation_score": 0.95,
                "verified": True
            },
            {
                "id": "salesforce-crm-agent-v2",
                "name": "Salesforce Lead Manager",
                "capabilities": ["lead_scoring", "contact_update"],
                "reputation_score": 0.92,
                "verified": True
            },
            {
                "id": "servicenow-itsm-bot",
                "name": "ServiceNow Ticket Master",
                "capabilities": ["incident_creation", "status_check"],
                "reputation_score": 0.88,
                "verified": True
            }
        ]

    def discover_agents(self, capability):
        """
        Finds agents with a specific capability.
        """
        print(f"🌐 NANDA: Querying decentralized registry for '{capability}'...")
        matches = [a for a in self.registry if capability in a["capabilities"]]
        
        if matches:
            print(f"✅ NANDA: Found {len(matches)} verified agents.")
            return matches
        else:
            print("❌ NANDA: No matching agents found.")
            return []

    def verify_agent(self, agent_id):
        """
        Checks the reputation score of an external agent (The 'Democracy' aspect).
        """
        agent = next((a for a in self.registry if a["id"] == agent_id), None)
        if agent:
            print(f"🗳️  NANDA Democracy: Verifying reputation for {agent['name']}...")
            if agent["reputation_score"] > 0.9:
                print("✅ Approved: High Reputation.")
                return True
            else:
                print("⚠️  Caution: Moderate Reputation.")
                return True # Allow for now
        return False

if __name__ == "__main__":
    nanda = NANDAConnector()
    agents = nanda.discover_agents("financial_forecasting")
    if agents:
        nanda.verify_agent(agents[0]["id"])
