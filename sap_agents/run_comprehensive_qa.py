import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent

def run_qa_suite():
    print("==================================================")
    print("🚀 STARTING COMPREHENSIVE QA SUITE")
    print("==================================================")
    print("Initializing Orchestrator...")
    orchestrator = OrchestratorAgent()
    
    test_cases = [
        # Core Domains
        {"domain": "Sales", "prompt": "Check status of SO-5001", "expected_agent": "SalesOrderAssistant", "expected_keyword": "Shipped"},
        {"domain": "Finance", "prompt": "Check status of INV-9002", "expected_agent": "FinanceReconciliationAgent", "expected_keyword": "Paid"},
        {"domain": "HR", "prompt": "Get info for employee EMP-101", "expected_agent": "HREmployeeAssistant", "expected_keyword": "Developer"},
        
        # Strategic Domains
        {"domain": "Analytics", "prompt": "How is the business doing?", "expected_agent": "AnalyticsAgent", "expected_keyword": "Revenue"},
        {"domain": "Procurement", "prompt": "Negotiate with supplier for laptops", "expected_agent": "ProcurementNegotiationAssistant", "expected_keyword": "Strategy"},
        {"domain": "Supply Chain", "prompt": "Check demand for product IBP-4001", "expected_agent": "SupplyChainAgent", "expected_keyword": "Forecast"},
        {"domain": "Projects", "prompt": "Check status of project PROJ-6001", "expected_agent": "ProjectSystemAgent", "expected_keyword": "Budget"},
        
        # New Operational Domains
        {"domain": "Manufacturing", "prompt": "Check status of PO-1001", "expected_agent": "ManufacturingAgent", "expected_keyword": "In Progress"},
        {"domain": "Asset Mgmt", "prompt": "Check status of EQ-5001", "expected_agent": "AssetManagementAgent", "expected_keyword": "Operational"},
        {"domain": "Service", "prompt": "Check status of TKT-3001", "expected_agent": "CustomerServiceAgent", "expected_keyword": "Open"}
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"\n🔹 Testing Domain: {test['domain']}")
        print(f"   Prompt: '{test['prompt']}'")
        
        try:
            # Plan
            plan = orchestrator.plan(test['prompt'], user_id="qa_tester")
            planned_agent = plan['steps'][0].get('agent_criteria', 'Unknown')
            
            # Execute
            response = orchestrator.execute()
            
            # Verify
            agent_match = test['expected_agent'] == planned_agent
            keyword_match = test['expected_keyword'] in response
            error_free = "Critical Execution Error" not in response
            
            if agent_match and keyword_match and error_free:
                print(f"   ✅ PASS: Routed to {planned_agent} | Response contains '{test['expected_keyword']}'")
                passed += 1
            else:
                print(f"   ❌ FAIL: Agent: {planned_agent} (Exp: {test['expected_agent']}) | Keyword Found: {keyword_match}")
                print(f"   Response Snippet: {response[:100]}...")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ CRITICAL FAIL: Exception {str(e)}")
            failed += 1
            
    print("\n==================================================")
    print(f"🏁 QA COMPLETE: {passed}/{len(test_cases)} Passed")
    print("==================================================")

if __name__ == "__main__":
    run_qa_suite()
