import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def verify_extensibility():
    print("🚀 Testing Extensibility: Treasury & Integrations")
    print("-----------------------------------------------")
    
    orchestrator = OrchestratorAgent()
    
    test_cases = [
        {"prompt": "Check global cash position", "expected": "Global Cash Position"},
        {"prompt": "What is the liquidity forecast?", "expected": "Liquidity Forecast"},
        {"prompt": "Create a ServiceNow ticket for VPN issue", "expected": "ServiceNow"},
        {"prompt": "Check Salesforce opportunities", "expected": "Salesforce"},
        {"prompt": "Trigger n8n workflow for data sync", "expected": "n8n"}
    ]
    
    passed = 0
    
    for test in test_cases:
        print(f"\n🔹 Testing: '{test['prompt']}'")
        try:
            # Plan
            plan = orchestrator.plan(test['prompt'], user_id="ext_tester")
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
    verify_extensibility()
