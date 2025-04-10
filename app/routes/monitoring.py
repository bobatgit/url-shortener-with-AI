from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_session
from ..utils.monitoring import check_database, get_system_stats, get_application_stats
from ..utils.metrics import metrics
from ..utils.metrics_handler import get_metrics, update_active_urls_count

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/health")
async def health_check(session: Session = Depends(get_session)):
    db_healthy = check_database(session)
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected"
    }

@router.get("/stats")
async def system_stats(session: Session = Depends(get_session)):
    app_stats = get_application_stats(session)
    update_active_urls_count(app_stats["active_urls"])
    return {
        "system": get_system_stats(),
        "application": app_stats,
        "metrics": metrics.get_stats()
    }

@router.get("/metrics")
async def prometheus_metrics():
    return get_metrics()