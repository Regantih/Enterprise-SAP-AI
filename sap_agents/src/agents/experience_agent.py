from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Experience Management (Qualtrics)
SURVEYS = {
    "EMP-SAT": {"type": "Employee", "score": 78, "trend": "Up", "top_issue": "Work-Life Balance"},
    "CUST-NPS": {"type": "Customer", "score": 45, "trend": "Down", "top_issue": "Delivery Delays"}
}

class MockExperienceLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "sentiment" in prompt or "satisfaction" in prompt or "score" in prompt:
            return {"output": "**Experience Insights (Qualtrics)**:\n- Employee Engagement: **78/100** (Trend: ⬆️)\n- Customer NPS: **45** (Trend: ⬇️)\n\n*Action*: Investigate delivery delays to improve NPS."}
            
        return {"output": "I can help with Experience Data (Sentiment, NPS, Surveys)."}

def create_experience_agent():
    return MockExperienceLLM()
