import requests
import time

BASE_URL = "http://localhost:8000/api/chat"

def test_context():
    print("🚀 Starting Context Test...")
    
    # 1. First Query: Find leads
    print("\n1️⃣ Sending: 'Find leads for FinTech'")
    resp1 = requests.post(BASE_URL, json={"prompt": "Find leads for FinTech"})
    print(f"Response: {resp1.json()['response'][:100]}...")
    
    # 2. Second Query: Draft email to them (Context Dependent)
    print("\n2️⃣ Sending: 'Draft email to them'")
    resp2 = requests.post(BASE_URL, json={"prompt": "Draft email to them"})
    response_text = resp2.json()['response']
    print(f"Response: {response_text[:100]}...")
    
    # Verification
    if "Lead Gen" in response_text or "Hermes" in response_text or "Sales" in response_text:
        print("\n✅ Context Test PASSED: System understood 'them' refers to the leads.")
    else:
        print("\n❌ Context Test FAILED: System did not understand context.")

if __name__ == "__main__":
    test_context()
