from langchain_core.prompts import ChatPromptTemplate

class MockPlanningLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "plan" in prompt or "forecast" in prompt or "simulate" in prompt:
            return {"output": "**SAP Analytics Cloud (SAC) Plan**:\n- Scenario: 'Aggressive Growth'\n- Revenue Forecast: +12% YoY\n- Margin Impact: -2% (due to marketing spend)\n\n*Confidence*: 88% (Predictive Model)."}
            
        return {"output": "I can help with Predictive Planning and Simulations (SAC)."}

def create_planning_agent():
    return MockPlanningLLM()
