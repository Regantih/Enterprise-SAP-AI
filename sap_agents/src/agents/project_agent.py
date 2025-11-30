from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Project System (PPM)
PROJECTS = {
    "PROJ-6001": {"name": "New HQ Construction", "budget": 5000000, "spent": 1200000, "status": "On Track"},
    "PROJ-6002": {"name": "IT Upgrade 2025", "budget": 200000, "spent": 50000, "status": "Delayed"}
}

class MockProjectLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"]
        
        if "PROJ-" in prompt:
            for pid, data in PROJECTS.items():
                if pid in prompt:
                    return {"output": f"**Project {pid} ({data['name']})**:\n- Status: **{data['status']}**\n- Budget: ${data['budget']}\n- Spent: ${data['spent']}"}
            return {"output": "Project not found."}
            
        return {"output": "I can help with Projects (PROJ-)."}

def create_project_agent():
    return MockProjectLLM()
