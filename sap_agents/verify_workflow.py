import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.tools.sales_tools import create_sales_order
from src.agents.supply_chain_agent import DEMAND_PLANS

def verify_workflow():
    print("🚀 Testing Agentic Workflow: Sales -> Supply Chain")
    print("------------------------------------------------")
    
    # 1. Check Initial Demand
    initial_forecast = DEMAND_PLANS["IBP-4001"]["forecast"]
    print(f"1. Initial Demand for Laptop TG-11 (IBP-4001): {initial_forecast}")
    
    # 2. Create Sales Order
    print("\n2. Creating Sales Order for 'Laptop TG-11'...")
    result = create_sales_order("TechCorp, Laptop TG-11")
    print(f"   Result: {result}")
    
    # 3. Verify Demand Update
    new_forecast = DEMAND_PLANS["IBP-4001"]["forecast"]
    print(f"\n3. New Demand for Laptop TG-11 (IBP-4001): {new_forecast}")
    
    if new_forecast == initial_forecast + 1:
        print("\n✅ SUCCESS: Sales Order automatically triggered Demand Update!")
    else:
        print("\n❌ FAIL: Demand did not update correctly.")

if __name__ == "__main__":
    verify_workflow()
