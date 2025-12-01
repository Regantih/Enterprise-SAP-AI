from fastapi import APIRouter
from src.services.monitoring_service import monitoring_service
from src.services.enterprise_formula import enterprise_formula

router = APIRouter()

@router.get("/health")
async def health_check():
    return monitoring_service.get_system_health()

@router.get("/formula")
async def get_formula():
    # Get raw metrics from monitoring service
    health_data = monitoring_service.get_system_health()
    
    # Map to EHS metrics (0-100 scale)
    metrics = {
        "performance": health_data['system']['success_rate'],
        "efficiency": health_data['system']['avg_rating'] * 20, # Convert 5-star to 100-scale
        "innovation": health_data['system']['active_agents_count'] * 10, # 10 pts per active agent
        "risk": 10 - (health_data['system']['success_rate'] / 10) # Inverse of success rate
    }
    
    return enterprise_formula.calculate_score(metrics)
