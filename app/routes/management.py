from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import URL, Setting, get_session
from ..models import URLResponse, Setting, SettingUpdate
from ..errors import URLNotFoundError, InvalidSettingError
from ..utils.cleanup import cleanup_expired_urls
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/urls/", response_model=list[URLResponse])
async def list_urls(request: Request, session: Session = Depends(get_session)):
    logger.info("Listing all URLs")
    urls = session.query(URL).order_by(URL.created_at.desc()).all()
    return urls

@router.delete("/urls/{short_code}")
async def delete_url(request: Request, short_code: str, session: Session = Depends(get_session)):
    url = session.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        logger.warning(f"Attempted to delete non-existent URL: {short_code}")
        raise URLNotFoundError(short_code)
    
    session.delete(url)
    session.commit()
    logger.info(f"Deleted URL: {short_code}")
    return {"message": "URL deleted successfully"}

@router.post("/cleanup")
async def cleanup_urls(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    logger.info("Starting URL cleanup")
    deleted_count = cleanup_expired_urls(session)
    return {"message": f"Cleaned up {deleted_count} expired URLs"}

@router.get("/settings/", response_model=list[Setting])
async def list_settings(request: Request, session: Session = Depends(get_session)):
    logger.info("Fetching application settings")
    settings = session.query(Setting).all()
    return settings

@router.put("/settings/{setting_name}")
async def update_setting(
    request: Request,
    setting_name: str,
    setting_update: SettingUpdate,
    session: Session = Depends(get_session)
):
    setting = session.query(Setting).filter(Setting.setting_name == setting_name).first()
    if not setting:
        logger.error(f"Attempted to update non-existent setting: {setting_name}")
        raise InvalidSettingError(setting_name)
    
    setting.setting_value = setting_update.setting_value
    session.commit()
    logger.info(f"Updated setting {setting_name}: {setting_update.setting_value}")
    return setting