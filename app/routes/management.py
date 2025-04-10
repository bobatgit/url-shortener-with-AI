from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from ..database import URL, Setting, get_session
from ..models import URLResponse, Setting, SettingUpdate
from ..errors import URLNotFoundError, InvalidSettingError
from ..utils.cleanup import cleanup_expired_urls
import logging
from app.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

manage_router = APIRouter(prefix="/manage")

@manage_router.get("/urls")
async def list_urls():
    with get_db() as db:
        urls = db.execute("SELECT * FROM urls ORDER BY created_at DESC").fetchall()
        return [dict(url) for url in urls]

@manage_router.delete("/urls/{short_code}")
async def delete_url(short_code: str):
    with get_db() as db:
        result = db.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="URL not found")
        return {"message": "URL deleted"}

@router.get("/urls/", response_model=list[URLResponse])
async def list_urls(session: Session = Depends(get_session)):
    urls = session.query(URL).order_by(URL.created_at.desc()).all()
    return urls

@router.delete("/urls/{short_code}")
async def delete_url(short_code: str, session: Session = Depends(get_session)):
    url = session.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    session.delete(url)
    session.commit()
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