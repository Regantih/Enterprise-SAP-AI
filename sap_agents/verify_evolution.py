import sys
import os
import json
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.orchestrator import OrchestratorAgent
from src.services.audit_service import create_audit_service
from src.services.evolution_engine import create_evolution_engine

def verify_evolution():
    print("🚀 Testing Self-Evolving Audit Loop")
    print("-----------------------------------")
    
    orchestrator = OrchestratorAgent()
    audit_service = create_audit_service()
    evolution_engine = create_evolution_engine()
    
    # 1. Run Transaction
    print("\n🔹 Step 1: Running Transaction...")
    prompt = "Check status of SO-1001"
    response, transaction_id = orchestrator.run(prompt, user_id="audit_tester")
    print(f"   Response: {response[:50]}...")
    print(f"   Transaction ID: {transaction_id}")
    
    # 2. Verify Audit Log
    print("\n🔹 Step 2: Verifying Audit Log...")
    trail = audit_service.get_audit_trail(transaction_id)
    steps = [e['step'] for e in trail]
    print(f"   Logged Steps: {steps}")
    
    if "TRANSACTION" in steps and "DECISION" in steps and "ACTION" in steps and "OUTCOME" in steps:
        print("   ✅ Audit Trail Complete")
    else:
        print("   ❌ Audit Trail Incomplete")
        
    # 3. Simulate Negative Feedback
    print("\n🔹 Step 3: Simulating Negative Feedback...")
    feedback_comment = "Response too short and vague."
    audit_service.log_feedback(transaction_id, 1, feedback_comment)
    
    # 4. Trigger Evolution
    print("\n🔹 Step 4: Triggering Evolution Engine...")
    evolution_result = evolution_engine.analyze_feedback(transaction_id, 1, feedback_comment)
    print(f"   Engine Output: {evolution_result}")
    
    # 5. Verify Evolution Log
    print("\n🔹 Step 5: Verifying Evolution Log...")
    trail_after = audit_service.get_audit_trail(transaction_id)
    evolution_step = next((e for e in trail_after if e['step'] == "EVOLUTION"), None)
    
    if evolution_step:
        print(f"   ✅ Evolution Logged: {evolution_step['detail']}")
    else:
        print("   ❌ Evolution NOT Logged")

if __name__ == "__main__":
    verify_evolution()
