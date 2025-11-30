import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.human_handoff import confidence_engine

def verify_confidence():
    print("🚀 Testing Enhanced Confidence Engine")
    print("-------------------------------------")
    
    # Test Case 1: High Confidence (Sales Agent, Good Response)
    print("\n🔹 Case 1: High Confidence")
    resp1 = "Order SO-1001 is confirmed with amount $5000. It is scheduled for delivery next Tuesday."
    audit1 = confidence_engine.evaluate(resp1, "SalesOrderAssistant")
    formatted1 = confidence_engine.append_audit_info(resp1, audit1)
    
    print(f"   Score: {audit1['confidence_score']}")
    print(f"   Certainty: {audit1['certainty_level']}")
    print(f"   Reasoning: {audit1['reasoning']}")
    
    assert audit1['certainty_level'] == "High"
    assert "Boost: Data pattern detected" in str(audit1['reasoning'])
    
    # Test Case 2: Low Confidence (Uncertainty Keyword)
    print("\n🔹 Case 2: Low Confidence (Uncertainty)")
    resp2 = "I am unsure, maybe check the portal."
    audit2 = confidence_engine.evaluate(resp2, "SalesOrderAssistant")
    
    print(f"   Score: {audit2['confidence_score']}")
    print(f"   Certainty: {audit2['certainty_level']}")
    print(f"   Reasoning: {audit2['reasoning']}")
    
    assert "Penalty: Uncertainty detected" in str(audit2['reasoning'])
    assert audit2['certainty_level'] != "High"
    
    print("\n✅ Confidence Engine Verification Passed!")

if __name__ == "__main__":
    verify_confidence()
