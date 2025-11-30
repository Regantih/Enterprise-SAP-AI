import sys
import os
import json
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.monitoring_service import create_monitoring_service, AUDIT_LOG_PATH

def verify_monitoring():
    print("🚀 Testing System Monitoring Service")
    print("-----------------------------------")
    
    # 1. Seed Mock Data
    print("\n🔹 Step 1: Seeding Mock Audit Data...")
    mock_logs = [
        {"step": "TRANSACTION", "detail": "Req 1"},
        {"step": "DECISION", "detail": "Routed to SalesAgent"},
        {"step": "OUTCOME", "status": "SUCCESS"},
        {"step": "FEEDBACK", "detail": {"rating": 5}},
        
        {"step": "TRANSACTION", "detail": "Req 2"},
        {"step": "DECISION", "detail": "Routed to FinanceAgent"},
        {"step": "OUTCOME", "status": "FAIL"},
        {"step": "FEEDBACK", "detail": {"rating": 1}},
        
        {"step": "TRANSACTION", "detail": "Req 3"},
        {"step": "DECISION", "detail": "Routed to SalesAgent"},
        {"step": "OUTCOME", "status": "SUCCESS"},
        {"step": "FEEDBACK", "detail": {"rating": 4}}
    ]
    
    with open(AUDIT_LOG_PATH, 'w') as f:
        json.dump(mock_logs, f)
        
    print("   Seeded 3 transactions (2 Success, 1 Fail).")
    
    # 2. Verify Metrics
    print("\n🔹 Step 2: Verifying Metrics Calculation...")
    monitor = create_monitoring_service()
    health = monitor.get_system_health()
    
    print(f"   Calculated Health: {health}")
    
    # Assertions
    assert health['total_requests'] == 3, f"Expected 3 requests, got {health['total_requests']}"
    assert health['success_rate'] == 66.7, f"Expected 66.7% success, got {health['success_rate']}"
    assert health['avg_rating'] == 3.3, f"Expected 3.3 rating, got {health['avg_rating']}"
    assert health['active_agents_count'] == 2, f"Expected 2 agents, got {health['active_agents_count']}"
    
    print("   ✅ Metrics Verified Successfully.")

if __name__ == "__main__":
    verify_monitoring()
