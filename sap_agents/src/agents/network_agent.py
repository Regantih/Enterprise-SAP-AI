from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Business Network (Ariba)
RFQS = {
    "RFQ-1001": {"item": "Laptops", "bids": 3, "best_bid": "$800/unit (TechSupplier)"},
    "RFQ-1002": {"item": "Office Chairs", "bids": 5, "best_bid": "$120/unit (OfficeDepot)"}
}

class MockNetworkLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "rfq" in prompt or "bid" in prompt:
            return {"output": "**Ariba Network RFQs**:\n- RFQ-1001 (Laptops): 3 Bids, Best: $800\n- RFQ-1002 (Chairs): 5 Bids, Best: $120\n\n*Status*: Ready for Award."}
            
        if "supplier" in prompt and "network" in prompt:
            return {"output": "Connected to **25,000+ Suppliers** on SAP Business Network."}

        return {"output": "I can help with Ariba Network (RFQs, Bids, Supplier Collaboration)."}

def create_network_agent():
    return MockNetworkLLM()
