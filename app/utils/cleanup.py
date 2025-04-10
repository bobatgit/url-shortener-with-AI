from sqlalchemy.orm import Session
from sqlalchemy import delete
from ..database import URL
from .metrics import metrics
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def cleanup_expired_urls(session: Session) -> int:
    """Remove expired URLs from the database and return the count of deleted entries."""
    stmt = delete(URL).where(URL.expires_at < datetime.utcnow())
    result = session.execute(stmt)
    deleted_count = result.rowcount
    session.commit()
    
    if deleted_count > 0:
        metrics.urls_expired += deleted_count
        logger.info(f"Cleaned up {deleted_count} expired URLs")
    return deleted_count