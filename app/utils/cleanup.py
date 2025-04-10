from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database import URL
import logging

# Configure logging to match other utilities
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='data/url_shortener.log'
)
logger = logging.getLogger(__name__)

def cleanup_expired_urls(session: Session) -> int:
    """Delete expired URLs from the database and return count of deleted entries."""
    try:
        now = datetime.utcnow()
        # Use delete with synchronize_session=False for batch deletion
        result = session.query(URL).filter(
            URL.expires_at.isnot(None),
            URL.expires_at < now
        ).delete(synchronize_session=False)
        
        session.commit()
        logger.info(f"Successfully deleted {result} expired URLs")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Database error during cleanup: {str(e)}")
        session.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error during cleanup: {str(e)}")
        session.rollback()
        raise