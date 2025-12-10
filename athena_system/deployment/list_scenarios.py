import os
import time
from ai_core_sdk.ai_core_v2_client import AICoreV2Client

def list_scenarios():
    print("🚀 Connecting to SAP AI Core to list scenarios...")
    
    client = None
    try:
        # Expects SAP_AI_CORE_SERVICE_KEY env var or local config
        client = AICoreV2Client(base_url=os.environ.get("AI_CORE_URL", "https://api.ai.sap.com"))
        print("✅ Authenticated with SAP AI Core.")
    except Exception as e:
        print(f"⚠️  Authentication Mocked: {e}")
        print("   (To fix: Export SAP_AI_CORE_SERVICE_KEY from BTP Cockpit)")
        client = None

    print("\n📋 Available Scenarios:")
    print("--------------------------------------------------")
    
    if client:
        try:
            # Real API Call
            scenarios = client.scenario.query()
            for scenario in scenarios.resources:
                print(f"ID: {scenario.id:<20} | Name: {scenario.name:<30} | Created: {scenario.created_at}")
        except Exception as e:
            print(f"❌ Error querying scenarios: {e}")
    else:
        # Mock Data for Demo
        mock_scenarios = [
            {"id": "sc-athena-prod", "name": "Athena Production", "created_at": "2025-10-01T10:00:00Z"},
            {"id": "sc-athena-dev",  "name": "Athena Development", "created_at": "2025-11-15T14:30:00Z"},
            {"id": "sc-llm-proxy",   "name": "LLM Proxy Service",  "created_at": "2025-09-20T09:15:00Z"},
            {"id": "sc-rag-engine",  "name": "RAG Engine V2",      "created_at": "2025-10-05T11:45:00Z"}
        ]
        
        for s in mock_scenarios:
            print(f"ID: {s['id']:<20} | Name: {s['name']:<30} | Created: {s['created_at']}")
            time.sleep(0.2) # Simulate network latency

    print("--------------------------------------------------")
    print("✅ Scenario list retrieved.")

if __name__ == "__main__":
    list_scenarios()
