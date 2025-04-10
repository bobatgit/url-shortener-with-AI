from sqlalchemy.orm import Session
from sqlalchemy import text
import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_database(session: Session) -> bool:
    try:
        session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

def get_system_stats() -> Dict[str, Any]:
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }

def get_application_stats(session: Session) -> Dict[str, Any]:
    try:
        url_count = session.execute(text("SELECT COUNT(*) FROM urls")).scalar()
        active_urls = session.execute(
            text("SELECT COUNT(*) FROM urls WHERE expires_at > CURRENT_TIMESTAMP")
        ).scalar()
        return {
            "total_urls": url_count,
            "active_urls": active_urls,
            "database_status": "healthy"
        }
    except Exception as e:
        logger.error(f"Error getting application stats: {e}")
        return {
            "total_urls": 0,
            "active_urls": 0,
            "database_status": "unhealthy"
        }