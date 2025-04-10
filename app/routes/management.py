from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database import URL, Setting, get_session
from ..models import URLResponse, SettingUpdate
from ..utils.cleanup import cleanup_expired_urls
from ..utils.rate_limit import check_rate_limit
import logging

router = APIRouter(tags=["management"])
logger = logging.getLogger(__name__)

@router.get("/urls/", response_model=list[URLResponse])
async def list_urls(
    request: Request,
    session: Session = Depends(get_session)
):
    """List all shortened URLs."""
    check_rate_limit(request)
    try:
        urls = session.query(URL).order_by(URL.created_at.desc()).all()
        return urls
    except SQLAlchemyError as e:
        logger.error(f"Database error listing URLs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving URLs"
        )

@router.delete("/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    short_code: str,
    request: Request,
    session: Session = Depends(get_session)
):
    """Delete a specific URL by short code."""
    check_rate_limit(request)
    try:
        url = session.query(URL).filter(URL.short_code == short_code).first()
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found"
            )
        
        session.delete(url)
        session.commit()
        logger.info(f"Deleted URL with short code: {short_code}")
        
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting URL: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting URL"
        )

@router.post("/cleanup", status_code=status.HTTP_200_OK)
async def cleanup_urls(
    background_tasks: BackgroundTasks,
    request: Request,
    session: Session = Depends(get_session)
):
    """Clean up expired URLs."""
    check_rate_limit(request)
    try:
        background_tasks.add_task(cleanup_expired_urls, session)
        return {"message": "Cleanup task initiated"}
    except Exception as e:
        logger.error(f"Error scheduling cleanup task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error scheduling cleanup task"
        )

@router.get("/settings/", response_model=list[Setting])
async def list_settings(
    request: Request,
    session: Session = Depends(get_session)
):
    """List all application settings."""
    check_rate_limit(request)
    try:
        settings = session.query(Setting).all()
        return settings
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving settings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving settings"
        )

@router.put("/settings/{setting_name}", response_model=Setting)
async def update_setting(
    setting_name: str,
    setting_update: SettingUpdate,
    request: Request,
    session: Session = Depends(get_session)
):
    """Update a specific setting value."""
    check_rate_limit(request)
    try:
        setting = session.query(Setting).filter(Setting.setting_name == setting_name).first()
        if not setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setting not found"
            )
        
        setting.setting_value = setting_update.setting_value
        session.commit()
        logger.info(f"Updated setting {setting_name}: {setting_update.setting_value}")
        return setting
        
    except SQLAlchemyError as e:
        logger.error(f"Database error updating setting: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating setting"
        )