import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from athena_system.config import MOCK_MODE, OPENAI_API_KEY

class HermesAgent:
    def __init__(self):
        self.llm = None
        if not MOCK_MODE:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0.7, api_key=OPENAI_API_KEY)

    def identify_leads(self, criteria):
        print(f"🕵️  Hermes: Scouting for leads matching '{criteria}'...")
        
        if MOCK_MODE:
            return [
                {"company": "Acme Corp", "industry": "Manufacturing", "contact": "John Doe (CTO)", "pain_point": "Supply Chain AI Risk"},
                {"company": "FinTech Global", "industry": "Finance", "contact": "Jane Smith (CRO)", "pain_point": "Regulatory Compliance"},
                {"company": "HealthPlus", "industry": "Healthcare", "contact": "Dr. A. Gupta (CIO)", "pain_point": "Patient Data Privacy"}
            ]
        else:
            # In a real scenario, this would connect to a CRM or Lead Gen tool
            return self._llm_lead_gen(criteria)

    def draft_outreach(self, lead):
        print(f"📧 Hermes: Drafting outreach for {lead['company']}...")
        
        if MOCK_MODE:
            return self._mock_email(lead)
        else:
            return self._llm_email(lead)

    def _mock_email(self, lead):
        return f"""
Subject: Mitigating {lead['pain_point']} at {lead['company']} - Strategic Navigator

Dear {lead['contact']},

I noticed {lead['company']} is innovating in {lead['industry']}. With the rise of Agentic AI, addressing {lead['pain_point']} is critical.

Our POTENTIAL-X Framework helps enterprises like yours deploy AI safely.

Best,
[Your Name]
"""

    def _llm_email(self, lead):
        prompt = ChatPromptTemplate.from_template("""
        You are Hermes, the Client Agent.
        Draft a personalized cold email to {contact} at {company}.
        Focus on their likely pain point: {pain_point}.
        Value Prop: POTENTIAL-X Framework for Enterprise-Safe AI.
        Keep it under 150 words.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke(lead)
        return response.content

if __name__ == "__main__":
    agent = HermesAgent()
    leads = agent.identify_leads("Enterprise AI Risk")
    print(f"Found {len(leads)} leads.")
    email = agent.draft_outreach(leads[0])
    print("\n" + "="*30)
    print(email)
    print("="*30)
