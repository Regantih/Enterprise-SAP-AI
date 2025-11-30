from langchain_core.prompts import ChatPromptTemplate

class MockProcessLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "process" in prompt or "mining" in prompt or "efficiency" in prompt:
            return {"output": "**Process Mining (Signavio)**:\n- Process: 'Order-to-Cash'\n- Bottleneck: 'Credit Check' (taking 2.5 days avg)\n- Recommendation: Automate credit checks for orders < $5k.\n\n*Potential Savings*: $50k/year."}
            
        return {"output": "I can help with Process Mining and Optimization (Signavio)."}

def create_process_agent():
    return MockProcessLLM()
