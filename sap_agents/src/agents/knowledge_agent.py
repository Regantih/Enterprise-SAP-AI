from langchain_core.prompts import ChatPromptTemplate

# Mock Vector Database (Document Index)
VECTOR_DB = {
    "travel_policy": {
        "content": "Employees are allowed Business Class for flights over 6 hours. Per diem is $75/day.",
        "metadata": {"source": "Global Travel Policy 2025.pdf"}
    },
    "hr_handbook": {
        "content": "Remote work is permitted up to 3 days a week with manager approval. Core hours are 10am-3pm.",
        "metadata": {"source": "Employee Handbook v4.pdf"}
    },
    "it_security": {
        "content": "Passwords must be changed every 90 days. MFA is mandatory for all VPN access.",
        "metadata": {"source": "IT Security Guidelines.docx"}
    }
}

class MockKnowledgeLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        # Simulated Retrieval
        retrieved_docs = []
        if "travel" in prompt or "flight" in prompt or "class" in prompt:
            retrieved_docs.append(VECTOR_DB["travel_policy"])
        if "remote" in prompt or "work" in prompt or "home" in prompt:
            retrieved_docs.append(VECTOR_DB["hr_handbook"])
        if "password" in prompt or "vpn" in prompt or "security" in prompt:
            retrieved_docs.append(VECTOR_DB["it_security"])
            
        if retrieved_docs:
            context = "\n".join([f"- {doc['content']} (Source: {doc['metadata']['source']})" for doc in retrieved_docs])
            return {"output": f"**RAG Knowledge Base**:\nBased on the retrieved documents:\n{context}"}

        return {"output": "I can help you find information in company policies and documents (PDFs/Wikis)."}

def create_knowledge_agent():
    return MockKnowledgeLLM()
