import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from athena_system.config import MOCK_MODE, OPENAI_API_KEY
from athena_system.utils.tracing import setup_tracing

tracer = setup_tracing("critic-agent")

class CriticAgent:
    def __init__(self):
        self.llm = None
        if not MOCK_MODE:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0.0, api_key=OPENAI_API_KEY) # Strict temp

    def review_content(self, content, content_type="general"):
        with tracer.start_as_current_span("review_content") as span:
            span.set_attribute("critic.content_type", content_type)
            print(f"🧐 Critic: Reviewing {content_type} for accuracy and safety...")
            
            if MOCK_MODE:
                result = self._mock_review(content)
            else:
                result = self._llm_review(content, content_type)
            
            span.set_attribute("critic.status", result.get("status", "Unknown"))
            span.set_attribute("critic.score", result.get("safety_score", 0.0))
            return result

    def _mock_review(self, content):
        # Simulating a review process
        # In a real system, this would check against a Fact Database or Policy Engine
        
        return {
            "status": "Approved",
            "safety_score": 0.98,
            "feedback": "Content is aligned with POTENTIAL-X guidelines. No bias detected.",
            "verification_stamp": "✅ Verified by Athena Critic"
        }

    def _llm_review(self, content, content_type):
        prompt = ChatPromptTemplate.from_template("""
        You are the Critic Agent for the Strategic Navigator.
        Review the following {content_type} for:
        1. Accuracy (Fact-checking)
        2. Tone (Professional & Strategic)
        3. Safety (Bias & Enterprise Suitability)
        
        Content:
        {content}
        
        Return a JSON object with:
        - status: "Approved" or "Rejected"
        - safety_score: Float (0.0 - 1.0)
        - feedback: Specific comments
        - verification_stamp: "✅ Verified" if approved
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"content": content, "content_type": content_type})
        return response.content # In real app, parse JSON

if __name__ == "__main__":
    agent = CriticAgent()
    review = agent.review_content("Agentic AI is the future.", "blog_post")
    print(json.dumps(review, indent=2))
