from fastapi import APIRouter
from src.services.monitoring_service import monitoring_service
from src.services.enterprise_formula import enterprise_formula

router = APIRouter()

@router.get("/health")
async def health_check():
    return monitoring_service.get_system_health()

@router.get("/formula")
async def get_formula():
    return enterprise_formula.calculate()
