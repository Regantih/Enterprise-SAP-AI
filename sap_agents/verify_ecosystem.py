import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def verify_ecosystem():
    print("🚀 Testing Full Ecosystem: XM, Network, Travel, Planning, Process")
    print("---------------------------------------------------------------")
    
    orchestrator = OrchestratorAgent()
    
    test_cases = [
        {"prompt": "Check employee sentiment score", "expected": "Experience Insights"},
        {"prompt": "Check RFQ bids for Laptops", "expected": "Ariba Network"},
        {"prompt": "Book a trip to Berlin", "expected": "My Trips"},
        {"prompt": "Simulate aggressive growth plan", "expected": "SAP Analytics Cloud"},
        {"prompt": "Analyze process efficiency for Order-to-Cash", "expected": "Process Mining"}
    ]
    
    passed = 0
    
    for test in test_cases:
        print(f"\n🔹 Testing: '{test['prompt']}'")
        try:
            # Plan
            plan = orchestrator.plan(test['prompt'], user_id="eco_tester")
            planned_agent = plan['steps'][0].get('agent_criteria', 'Unknown')
            print(f"   Routed to: {planned_agent}")
            
            # Execute
            response = orchestrator.execute()
            print(f"   Response: {response[:100]}...")
            
            if test['expected'] in response:
                print("   ✅ PASS")
                passed += 1
            else:
                print(f"   ❌ FAIL: Expected '{test['expected']}'")
                
        except Exception as e:
            print(f"   ❌ CRITICAL FAIL: {e}")
            
    print(f"\n🏁 Result: {passed}/{len(test_cases)} Passed")

if __name__ == "__main__":
    verify_ecosystem()
