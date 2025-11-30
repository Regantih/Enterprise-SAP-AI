from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Sustainability (Green Ledger)
CARBON_METRICS = {
    "Plant-Berlin": {"co2_emissions": "1,200 tons", "trend": "-5% (YoY)", "status": "On Track"},
    "Plant-NewYork": {"co2_emissions": "3,500 tons", "trend": "+2% (YoY)", "status": "Warning"}
}

class MockSustainabilityLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "carbon" in prompt or "emission" in prompt or "footprint" in prompt:
            return {"output": "**Green Ledger (Sustainability)**:\n- Berlin Plant: **1,200 tons** CO2 (⬇️ 5%)\n- New York Plant: **3,500 tons** CO2 (⬆️ 2%)\n\n*Alert*: New York is exceeding emission targets."}
            
        if "esg" in prompt or "safety" in prompt:
            return {"output": "**ESG Scorecard**: 85/100 (Leader). Safety Incidents: 0 this month."}

        return {"output": "I can help with Sustainability, Carbon Footprint, and ESG metrics."}

def create_sustainability_agent():
    return MockSustainabilityLLM()
