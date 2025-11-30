from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Supply Chain (IBP)
DEMAND_PLANS = {
    "IBP-4001": {"product": "Laptop TG-11", "forecast": 1500, "accuracy": "95%", "location": "Berlin"},
    "IBP-4002": {"product": "Monitor TG-12", "forecast": 3000, "accuracy": "88%", "location": "San Francisco"}
}

class MockSupplyChainLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"]
        
        if "IBP-" in prompt:
            for pid, data in DEMAND_PLANS.items():
                if pid in prompt:
                    return {"output": f"**Demand Plan {pid}**:\n- Product: {data['product']}\n- Forecast: **{data['forecast']} units**\n- Accuracy: {data['accuracy']}"}
            return {"output": "Demand Plan not found."}
            
        return {"output": "I can help with Demand Plans (IBP-)."}

def update_demand_forecast(product: str, quantity: int):
    """
    Updates the demand forecast for a product based on new sales orders.
    """
    print(f"   [Supply Chain Agent] 📈 Receiving Demand Signal: {quantity} units for {product}...")
    
    # Simple logic: Find matching plan or create new
    for pid, data in DEMAND_PLANS.items():
        if data['product'] in product:
            current = int(data['forecast'])
            new_forecast = current + quantity
            data['forecast'] = new_forecast
            print(f"   [Supply Chain Agent] ✅ Updated Forecast for {pid}: {current} -> {new_forecast}")
            return f"Demand updated for {pid}. New Forecast: {new_forecast}"
            
    return "No matching demand plan found."

def create_supply_chain_agent():
    return MockSupplyChainLLM()
