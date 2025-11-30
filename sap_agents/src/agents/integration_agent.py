from langchain_core.prompts import ChatPromptTemplate

# Mock Data for External Systems
TICKETS = {
    "INC-1001": {"system": "ServiceNow", "status": "New", "priority": "P2", "desc": "VPN Issue"},
    "INC-1002": {"system": "ServiceNow", "status": "Resolved", "priority": "P3", "desc": "Password Reset"}
}

OPPORTUNITIES = {
    "OPP-5001": {"system": "Salesforce", "stage": "Negotiation", "amount": 150000, "account": "MegaCorp"},
    "OPP-5002": {"system": "Salesforce", "stage": "Closed Won", "amount": 75000, "account": "StartUp Inc"}
}

class MockIntegrationLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        # ServiceNow Integration
        if "servicenow" in prompt or "ticket" in prompt:
            if "create" in prompt:
                return {"output": "✅ **ServiceNow**: Ticket #INC-9999 created successfully via n8n webhook. Priority: P3."}
            return {"output": "**ServiceNow Tickets**:\n- INC-1001: VPN Issue (New)\n- INC-1002: Password Reset (Resolved)"}
            
        # Salesforce Integration
        if "salesforce" in prompt or "opportunity" in prompt:
            return {"output": "**Salesforce Opportunities**:\n- OPP-5001: MegaCorp ($150k) - Negotiation\n- OPP-5002: StartUp Inc ($75k) - Closed Won"}
            
        # n8n General
        if "n8n" in prompt or "trigger" in prompt:
            return {"output": "✅ **n8n Workflow Triggered**: Data synced between SAP and External System."}

        return {"output": "I can help with ServiceNow, Salesforce, and n8n Integrations."}

def create_integration_agent():
    return MockIntegrationLLM()
