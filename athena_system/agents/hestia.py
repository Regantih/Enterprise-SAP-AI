import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from athena_system.config import MOCK_MODE, OPENAI_API_KEY

class HestiaAgent:
    def __init__(self):
        self.llm = None
        if not MOCK_MODE:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0.1, api_key=OPENAI_API_KEY)

    def generate_business_report(self, period="Weekly"):
        print(f"📊 Hestia: Generating {period} Business Review...")
        
        # 1. Fetch Data (Mocked CRM/Finance API)
        data = self._fetch_business_data()
        
        # 2. Analyze & Insight Generation
        if MOCK_MODE:
            return self._mock_analysis(data)
        else:
            return self._llm_analysis(data)

    def _fetch_business_data(self):
        # Simulating data from HubSpot/QuickBooks
        return {
            "revenue_mtd": 45000,
            "revenue_target": 50000,
            "pipeline_value": 120000,
            "active_engagements": 3,
            "margin": 0.32, # 32%
            "margin_target": 0.35, # 35%
            "alerts": ["Client X contract renewal due in 14 days", "Pipeline coverage low for Q3"]
        }

    def _mock_analysis(self, data):
        status = "🟢 On Track" if data['revenue_mtd'] >= data['revenue_target'] * 0.9 else "🟡 At Risk"
        
        return f"""
# 📈 Weekly Business Review

**Status**: {status}

## Financials
- **Revenue MTD**: ${data['revenue_mtd']:,} (Target: ${data['revenue_target']:,})
- **Net Margin**: {data['margin']*100}% (Target: {data['margin_target']*100}%)
  - *Insight*: Margin is slightly below target (32% vs 35%). Recommend reviewing sub-contractor costs.

## Pipeline Health
- **Total Value**: ${data['pipeline_value']:,}
- **Coverage**: 2.4x (Healthy)

## 🚨 Proactive Alerts
1. **{data['alerts'][0]}**: Action required immediately.
2. **{data['alerts'][1]}**: Suggest launching a new 'Knowledge Arbitrage' campaign via Apollo/Clio.

## Strategic Recommendation
Focus on closing the gap in Q3 pipeline. Deploy Hermes to target 'FinTech' sector.
"""

    def _llm_analysis(self, data):
        prompt = ChatPromptTemplate.from_template("""
        You are Hestia, the Operations Agent.
        Analyze the following business metrics for the Strategic Navigator practice:
        
        {data}
        
        Generate a "Weekly Business Review" in Markdown.
        Include:
        1. Executive Status (Red/Yellow/Green)
        2. Financial Analysis (Revenue & Margin)
        3. Pipeline Health
        4. Proactive Alerts & Recommended Actions
        
        Be concise and action-oriented.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"data": data})
        return response.content

if __name__ == "__main__":
    agent = HestiaAgent()
    report = agent.generate_business_report()
    print("\n" + report)
