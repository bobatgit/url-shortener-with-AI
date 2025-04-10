import asyncio
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .cleanup import cleanup_expired_urls

logger = logging.getLogger(__name__)

async def scheduled_cleanup(interval_hours: int = 24):
    while True:
        try:
            session = SessionLocal()
            cleanup_expired_urls(session)
        except Exception as e:
            logger.error(f"Error during scheduled cleanup: {e}")
        finally:
            session.close()
        
        await asyncio.sleep(interval_hours * 3600)