import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def verify_market_intelligence():
    print("🚀 Testing Market Intelligence Agent (Strategy)")
    print("---------------------------------------------")
    
    orchestrator = OrchestratorAgent()
    
    test_cases = [
        {"prompt": "Analyze competitor R&D spend", "expected": "Competitor X"},
        {"prompt": "What are the EV battery trends?", "expected": "Lithium prices"},
        {"prompt": "How will new tariffs impact us?", "expected": "EU tariffs"}
    ]
    
    passed = 0
    
    for test in test_cases:
        print(f"\n🔹 Testing: '{test['prompt']}'")
        try:
            # Plan
            plan = orchestrator.plan(test['prompt'], user_id="strategy_user")
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
    verify_market_intelligence()
