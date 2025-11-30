from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Mock Data for Customer Service (CS)
TICKETS = {
    "TKT-3001": {"customer": "TechCorp", "issue": "System Outage", "status": "Open", "priority": "Critical"},
    "TKT-3002": {"customer": "AlphaInc", "issue": "Login Failure", "status": "Resolved", "priority": "Medium"},
    "TKT-3003": {"customer": "BetaLtd", "issue": "Feature Request", "status": "In Progress", "priority": "Low"}
}

WARRANTIES = {
    "WAR-7001": {"product": "Turbine Blade", "customer": "TechCorp", "expiry": "2026-12-31", "status": "Active"},
    "WAR-7002": {"product": "Pump Housing", "customer": "AlphaInc", "expiry": "2024-12-31", "status": "Expired"}
}

class MockCSLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"]
        
        # Ticket Lookup
        if "TKT-" in prompt:
            for tkt_id, data in TICKETS.items():
                if tkt_id in prompt:
                    return {"output": f"**Service Ticket {tkt_id}**:\n- Customer: {data['customer']}\n- Issue: {data['issue']}\n- Status: **{data['status']}**\n- Priority: {data['priority']}"}
            return {"output": "Ticket not found."}
            
        # Warranty Lookup
        if "WAR-" in prompt or "warranty" in prompt.lower():
            for war_id, data in WARRANTIES.items():
                if war_id in prompt:
                    return {"output": f"**Warranty {war_id}**:\n- Product: {data['product']}\n- Customer: {data['customer']}\n- Status: **{data['status']}**\n- Expiry: {data['expiry']}"}
            return {"output": "Warranty not found."}

        return {"output": "I can help with Service Tickets (TKT-) and Warranties (WAR-)."}

def create_cs_agent():
    """
    Creates the Customer Service Agent (CS).
    """
    return MockCSLLM()
