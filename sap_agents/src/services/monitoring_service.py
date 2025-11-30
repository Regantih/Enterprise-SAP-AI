import json
import os
from datetime import datetime

AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'audit_log.json')

class MonitoringService:
    def __init__(self):
        self._ensure_log_exists()

    def _ensure_log_exists(self):
        if not os.path.exists(AUDIT_LOG_PATH):
            os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
            with open(AUDIT_LOG_PATH, 'w') as f:
                json.dump([], f)

    def get_system_health(self):
        """
        Calculates system KPIs from the audit log.
        """
        try:
            with open(AUDIT_LOG_PATH, 'r') as f:
                logs = json.load(f)
        except Exception:
            logs = []

        total_requests = 0
        successful_requests = 0
        total_rating = 0
        rated_requests = 0
        active_agents = set()
        errors = 0

        for entry in logs:
            if entry.get('step') == 'TRANSACTION':
                total_requests += 1
            
            if entry.get('step') == 'OUTCOME' and entry.get('status') == 'SUCCESS':
                successful_requests += 1
            
            if entry.get('step') == 'FEEDBACK':
                rating = entry.get('detail', {}).get('rating', 0)
                if rating > 0:
                    total_rating += rating
                    rated_requests += 1
            
            if entry.get('step') == 'DECISION':
                # Extract agent name from "Routed to X"
                detail = entry.get('detail', '')
                if "Routed to" in detail:
                    agent = detail.replace("Routed to ", "").strip()
                    active_agents.add(agent)

            if entry.get('status') == 'FAIL' or entry.get('status') == 'CRITICAL':
                errors += 1

        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 100
        avg_rating = (total_rating / rated_requests) if rated_requests > 0 else 5.0

        # Simulated Business Metrics (Demo Mode)
        # In a real app, these would query the Sales/Finance/ESG agents or DB
        business_health = {
            "revenue_ytd": "12.5M",
            "revenue_trend": "+4.2%",
            "open_orders": 1240,
            "esg_score": 92,
            "csat_score": 4.8
        }

        return {
            "system": {
                "total_requests": total_requests,
                "success_rate": round(success_rate, 1),
                "avg_rating": round(avg_rating, 1),
                "active_agents_count": len(active_agents),
                "error_count": errors,
                "status": "Healthy" if success_rate > 90 else "Degraded"
            },
            "business": business_health
        }

def create_monitoring_service():
    return MonitoringService()

# Singleton
monitoring_service = create_monitoring_service()
