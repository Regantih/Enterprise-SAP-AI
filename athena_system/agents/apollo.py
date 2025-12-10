import json
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from athena_system.config import MOCK_MODE, OPENAI_API_KEY
from athena_system.utils.tracing import setup_tracing

tracer = setup_tracing("apollo-agent")

class ApolloAgent:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()
        self.llm = None
        if not MOCK_MODE:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=OPENAI_API_KEY)

    def research(self, topic):
        with tracer.start_as_current_span("research") as span:
            span.set_attribute("apollo.topic", topic)
            print(f"🔍 Apollo: Researching '{topic}'...")
            
            # 1. Execute Search
            try:
                with tracer.start_as_current_span("execute_search"):
                    search_results = self.search_tool.run(topic)
                    span.set_attribute("apollo.results_length", len(search_results))
            except Exception as e:
                span.record_exception(e)
                return f"Error performing search: {e}"

            # 2. Analyze Results
            if MOCK_MODE:
                return self._mock_analysis(topic, search_results)
            else:
                return self._llm_analysis(topic, search_results)

    def _mock_analysis(self, topic, results):
        print("🤖 Apollo: Generating MOCK analysis...")
        return f"""
# Research Report: {topic}

## Executive Summary
(Mock Analysis) The research indicates significant activity in this domain.

## Key Findings
{results}

## Strategic Implications
- Opportunity for Knowledge Arbitrage.
- Recommended Action: Create a blog post summarizing these findings.
"""

    def _llm_analysis(self, topic, results):
        print("🧠 Apollo: Generating AI analysis...")
        prompt = ChatPromptTemplate.from_template("""
        You are Apollo, the Research Agent for the Strategic Navigator.
        Analyze the following search results on '{topic}':
        
        {results}
        
        Produce a structured Markdown report with:
        1. Executive Summary
        2. Key Trends/Findings
        3. Strategic Implications for Enterprise AI
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"topic": topic, "results": results})
        return response.content

if __name__ == "__main__":
    agent = ApolloAgent()
    report = agent.research("Agentic AI trends 2025")
    print("\n" + "="*30)
    print(report)
    print("="*30)
