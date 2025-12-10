import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from athena_system.config import MOCK_MODE, OPENAI_API_KEY

class HephaestusAgent:
    def __init__(self):
        self.llm = None
        if not MOCK_MODE:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0.2, api_key=OPENAI_API_KEY) # Low temp for determinism

    def generate_risk_profile(self, project_description):
        print(f"🛡️  Hephaestus: Analyzing Risk Profile for '{project_description[:50]}...'")
        
        if MOCK_MODE:
            return self._mock_risk_profile(project_description)
        else:
            return self._llm_risk_profile(project_description)

    def generate_governance_charter(self, risk_profile):
        print(f"⚖️  Hephaestus: Designing Governance Charter based on Risk Level...")
        
        if MOCK_MODE:
            return self._mock_governance(risk_profile)
        else:
            return self._llm_governance(risk_profile)

    def _mock_risk_profile(self, description):
        # Mock logic based on keywords
        risk_level = "Medium"
        if "medical" in description.lower() or "financial" in description.lower():
            risk_level = "High"
        
        return {
            "overall_risk": risk_level,
            "dimensions": {
                "Technical": "Low - Standard Architecture",
                "Operational": "Medium - New Workflow Adoption",
                "Ethical": f"{risk_level} - Potential Bias/Privacy Issues",
                "Financial": "Low - Cost Control in place",
                "Reputational": "Medium - Customer Facing",
                "Compliance": "High - GDPR/EU AI Act"
            },
            "summary": f"This project carries a {risk_level} risk profile, primarily driven by Compliance and Ethical factors."
        }

    def _mock_governance(self, risk_profile):
        level = risk_profile["overall_risk"]
        
        committees = ["AI Steering Committee"]
        if level == "High":
            committees.append("Ethics Review Board")
            committees.append("Data Privacy Council")
            
        return f"""
# Governance Charter (Draft)

**Risk Level**: {level}

**Recommended Structure**:
- **Oversight**: {', '.join(committees)}
- **Decision Rights**:
  - Model Approval: CTO + Ethics Lead
  - Data Access: CISO

**Key Guardrails**:
1. Human-in-the-loop for all external outputs.
2. Weekly drift monitoring.
3. Bias testing pre-deployment.
"""

    def _llm_risk_profile(self, description):
        prompt = ChatPromptTemplate.from_template("""
        You are Hephaestus, the Delivery Agent for the Strategic Navigator.
        Analyze the following AI project description using the POTENTIAL-X Framework (P - Profile).
        
        Project: {description}
        
        Assess risk (High/Medium/Low) across these 6 dimensions:
        1. Technical
        2. Operational
        3. Ethical
        4. Financial
        5. Reputational
        6. Compliance
        
        Return a JSON object with 'overall_risk', 'dimensions' (dict), and 'summary'.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"description": description})
        # In a real app, we'd use a JSON parser here. For now, returning text.
        return response.content

    def _llm_governance(self, risk_profile):
        prompt = ChatPromptTemplate.from_template("""
        You are Hephaestus. Design a Governance Charter for a project with this risk profile:
        
        {risk_profile}
        
        Include:
        1. Recommended Committee Structure
        2. Key Decision Rights
        3. Mandatory Guardrails
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"risk_profile": risk_profile})
        return response.content

if __name__ == "__main__":
    agent = HephaestusAgent()
    profile = agent.generate_risk_profile("Deploying a medical diagnosis chatbot for patients.")
    print(json.dumps(profile, indent=2))
    charter = agent.generate_governance_charter(profile)
    print("\n" + charter)
