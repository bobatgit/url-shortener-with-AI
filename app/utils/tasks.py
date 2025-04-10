import asyncio
from datetime import datetime, timedelta
from sqlalchemy import text
from ..database import SessionLocal
from .cleanup import cleanup_expired_urls
from .cache import url_cache
import logging

logger = logging.getLogger(__name__)

async def run_maintenance_tasks():
    """Run periodic maintenance tasks."""
    while True:
        try:
            session = SessionLocal()
            try:
                # Cleanup expired URLs
                cleanup_expired_urls(session)
                
                # Remove inactive URLs from cache
                current_time = datetime.utcnow()
                results = session.execute(
                    text("SELECT short_code FROM urls WHERE expires_at < :current_time"),
                    {"current_time": current_time}
                )
                expired_codes = [row[0] for row in results]
                for code in expired_codes:
                    url_cache._remove(code)
                
                # Log maintenance completion
                logger.info("Maintenance tasks completed successfully")
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Error during maintenance tasks: {e}")
        
        # Run maintenance every hour
        await asyncio.sleep(3600)