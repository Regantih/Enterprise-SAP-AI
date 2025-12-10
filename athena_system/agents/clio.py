import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from athena_system.config import MOCK_MODE, OPENAI_API_KEY
from athena_system.utils.tracing import setup_tracing

tracer = setup_tracing("clio-agent")

class ClioAgent:
    def __init__(self):
        self.llm = None
        if not MOCK_MODE:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0.7, api_key=OPENAI_API_KEY)

    def generate_content(self, research_data, content_type="linkedin"):
        with tracer.start_as_current_span("generate_content") as span:
            span.set_attribute("clio.content_type", content_type)
            print(f"✍️  Clio: Drafting {content_type} content based on research...")
            
            if MOCK_MODE:
                return self._mock_generation(research_data, content_type)
            else:
                return self._llm_generation(research_data, content_type)

    def _mock_generation(self, research_data, content_type):
        print("🤖 Clio: Generating MOCK content...")
        if content_type == "linkedin":
            return f"""
🚀 **Strategic Insight: The Future of Agentic AI**

{research_data[:100]}...

**Why it matters for Enterprise:**
- Scalability is key.
- Determinism is non-negotiable.

#AI #Enterprise #Strategy #Athena
"""
        elif content_type == "blog":
            return f"""
# The Strategic Navigator's Guide to Agentic AI

**Executive Summary**
{research_data[:200]}...

**Deep Dive**
As we transition from pilot to production...
"""
        return "Error: Unknown content type."

    def _llm_generation(self, research_data, content_type):
        print("🧠 Clio: Generating AI content...")
        
        if content_type == "linkedin":
            prompt = ChatPromptTemplate.from_template("""
            You are Clio, the Content Agent for the Strategic Navigator.
            Draft a high-impact LinkedIn post (max 200 words) based on this research:
            
            {research_data}
            
            Style: Professional, insightful, provocative. Use bullet points for readability.
            """)
        else:
             prompt = ChatPromptTemplate.from_template("""
            You are Clio, the Content Agent for the Strategic Navigator.
            Draft a comprehensive Blog Post based on this research:
            
            {research_data}
            
            Structure:
            - Catchy Title
            - The "Hook" (Why this matters now)
            - 3 Key Takeaways
            - Strategic Advice for Leaders
            """)
        
        chain = prompt | self.llm
        response = chain.invoke({"research_data": research_data})
        return response.content

if __name__ == "__main__":
    # Test with dummy data
    dummy_research = "Agentic AI is moving towards deterministic orchestration patterns."
    agent = ClioAgent()
    post = agent.generate_content(dummy_research, "linkedin")
    print("\n" + "="*30)
    print(post)
    print("="*30)
