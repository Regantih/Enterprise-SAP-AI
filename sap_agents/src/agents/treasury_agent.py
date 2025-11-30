from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Treasury (TRM)
CASH_POSITIONS = {
    "USD": {"balance": 5000000, "bank": "Chase", "status": "Surplus"},
    "EUR": {"balance": 2500000, "bank": "Deutsche Bank", "status": "Stable"},
    "JPY": {"balance": 100000000, "bank": "MUFG", "status": "Low"}
}

class MockTreasuryLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "cash" in prompt or "position" in prompt:
            summary = "\n".join([f"- {cur}: {data['balance']:,} ({data['bank']})" for cur, data in CASH_POSITIONS.items()])
            return {"output": f"**Global Cash Position**:\n{summary}\n\nTotal Liquidity: $8.2M (approx)."}
            
        if "liquidity" in prompt or "forecast" in prompt:
            return {"output": "**Liquidity Forecast (30 Days)**:\n- Inflow: $2.5M (Receivables)\n- Outflow: $1.8M (Payables)\n- Net Change: +$0.7M\n\nStatus: Healthy."}
            
        return {"output": "I can help with Cash Positions and Liquidity Forecasts."}

def create_treasury_agent():
    return MockTreasuryLLM()
