from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def get_key_metrics(period: str = "Q4") -> str:
    """
    Retrieves key financial and operational metrics for the specified period.
    Simulates a high-level dashboard view.
    """
    return f"""
    **Key Metrics for {period}:**
    - **Revenue**: $15.2M (+12% YoY)
    - **EBITDA**: $3.4M (+5% YoY)
    - **Operating Margin**: 22.3% (Down from 24% last Q)
    - **Employee Churn**: 4.5% (Stable)
    - **Customer Satisfaction (NPS)**: 72 (+2 points)
    """

@tool
def simulate_outcome(scenario: str) -> str:
    """
    Simulates business outcomes based on a strategic decision.
    """
    if "price increase" in scenario.lower():
        return "Simulation: A 5% price increase is projected to boost Revenue by $1.1M but may reduce Volume by 2%."
    elif "hiring freeze" in scenario.lower():
        return "Simulation: A hiring freeze will save $500k in OpEx but risks delaying the 'Project Phoenix' launch by 2 months."
    else:
        return f"Simulation for '{scenario}': Projected impact is neutral to slightly positive based on current trends."

@tool
def get_strategic_advice(topic: str) -> str:
    """
    Provides strategic advice based on current metrics.
    """
    return """
    **Strategic Advice:**
    1. **Margin Protection**: Supplier costs are rising. Recommend renegotiating with top 3 vendors (Procurement).
    2. **Growth**: Sales in the EMEA region are lagging. Consider a targeted marketing campaign.
    3. **Talent**: Engineering churn is slightly above average. Review compensation packages (HR).
    """

class MockAnalyticsLLM:
    """
    Simulates a high-intelligence 'Wall Street Analyst' LLM.
    """
    def invoke(self, input_dict):
        prompt = input_dict.get("input", "")
        if "business doing" in prompt.lower() or "metrics" in prompt.lower() or "strategy" in prompt.lower():
            # 1. Analyze Real Data from Audit Log
            try:
                from src.services.monitoring_service import monitoring_service
                health = monitoring_service.get_system_health()
                sys_stats = health['system']
                biz_stats = health['business']
                
                # 2. Generate Insights
                insights = []
                if sys_stats['success_rate'] < 95:
                    insights.append(f"⚠️ **Operational Risk**: System success rate is {sys_stats['success_rate']}%. Investigate recent failures in {sys_stats['error_count']} transactions.")
                else:
                    insights.append(f"✅ **Operational Excellence**: System is running at {sys_stats['success_rate']}% reliability.")
                    
                if sys_stats['active_agents_count'] > 3:
                     insights.append(f"🚀 **High Adoption**: {sys_stats['active_agents_count']} different agents are actively being used.")

                # 3. Strategic Advice
                advice = """
**Strategic Advisor Report**:
1.  **Revenue & Growth**: Revenue is up {trend} ({rev}). Continue aggressive expansion in the APAC region.
2.  **Customer Sentiment**: CSAT is {csat}/5. Maintain current support levels but monitor response times.
3.  **ESG Impact**: ESG Score is {esg}. Consider 'Green Logistics' initiative to break 95.
""".format(
                    trend=biz_stats['revenue_trend'], 
                    rev=biz_stats['revenue_ytd'], 
                    csat=biz_stats['csat_score'],
                    esg=biz_stats['esg_score']
                )

                return {
                    "output": f"""
**Executive Summary (Real-Time)**:
{chr(10).join(['- ' + i for i in insights])}

{advice}
"""
                }
            except Exception as e:
                return {"output": f"Error generating analytics: {str(e)}"}

        return {"output": "I can analyze business performance, metrics, and strategy."}

def create_analytics_agent():
    """
    Creates the Strategic Analytics Agent (Mocked for Robustness).
    """
    return MockAnalyticsLLM()
