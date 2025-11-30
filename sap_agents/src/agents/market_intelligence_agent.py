from langchain_core.prompts import ChatPromptTemplate

# Mock External Knowledge Graph
MARKET_DATA = {
    "competitor_rd": {
        "content": "Competitor X has filed 15 new patents in Solid State Batteries this quarter. Estimated R&D spend: $50M.",
        "source": "Global Patent Database"
    },
    "ev_trends": {
        "content": "Global demand for EV batteries is projected to grow by 18% YoY. Lithium prices are stabilizing.",
        "source": "MarketWatch 2025 Report"
    },
    "macro_policy": {
        "content": "New EU tariffs on imported steel may increase production costs by 5-8% starting Q3.",
        "source": "EuroTrade Policy Brief"
    }
}

class MockMarketIntelligenceLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        # Simulated External Research
        insights = []
        if "competitor" in prompt or "r&d" in prompt or "patent" in prompt:
            insights.append(MARKET_DATA["competitor_rd"])
        if "trend" in prompt or "ev" in prompt or "battery" in prompt or "market" in prompt:
            insights.append(MARKET_DATA["ev_trends"])
        if "tariff" in prompt or "policy" in prompt or "macro" in prompt or "tax" in prompt:
            insights.append(MARKET_DATA["macro_policy"])
            
        if insights:
            context = "\n".join([f"- {item['content']} (Source: {item['source']})" for item in insights])
            return {"output": f"**Market Intelligence (Strategy)**:\nBased on external signals:\n{context}"}

        return {"output": "I can analyze Competitors, Market Trends, and Macro Policies. Try asking about 'Competitor R&D' or 'EV Trends'."}

def create_market_intelligence_agent():
    return MockMarketIntelligenceLLM()
