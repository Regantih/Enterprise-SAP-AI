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
        if "business doing" in prompt.lower() or "metrics" in prompt.lower():
            return {
                "output": """
**Executive Summary:**
The business is showing **strong resilience** with a **12% YoY Revenue Growth** ($15.2M). However, **Operating Margins** have compressed to 22.3% (vs 24% last Q), primarily driven by rising supplier costs in the Eurozone.

**Key Metrics (Q4):**
- 📈 **Revenue**: $15.2M (+12% YoY)
- 📉 **EBITDA**: $3.4M (+5% YoY) - *Lagging Revenue growth*
- ⚠️ **Churn**: 4.5% (Stable, but Engineering is at risk)

**Strategic Advice:**
1.  **Margin Recovery**: Initiate a strategic sourcing review with top 3 suppliers (Ariba) to claw back 150bps of margin.
2.  **Capital Allocation**: Reinvest Q4 surplus into 'Project Phoenix' to accelerate time-to-market.
3.  **Risk**: Monitor FX exposure in EMEA as the Euro weakens.
"""
            }
        return {"output": "I can only analyze business performance and metrics at this time."}

def create_analytics_agent():
    """
    Creates the Strategic Analytics Agent (Mocked for Robustness).
    """
    return MockAnalyticsLLM()
