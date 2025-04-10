from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.database import get_session, URL, Setting
from app.models import URLCreate, URLResponse, SettingUpdate
from app.utils.url_utils import generate_short_code, calculate_expiry_date
from app.utils.security import validate_url, validate_custom_code
from app.utils.rate_limit import check_rate_limit
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_data: URLCreate,
    request: Request,
    session: Session = Depends(get_session)
) -> URLResponse:
    """Create a shortened URL."""
    try:
        check_rate_limit(request)
        validated_url = validate_url(str(url_data.url))
        
        # Handle custom code
        short_code = url_data.custom_code
        if short_code:
            if not validate_custom_code(short_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid custom code format"
                )
            if session.query(URL).filter(URL.short_code == short_code).first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Custom code already in use"
                )
        else:
            settings = session.query(Setting).filter(
                Setting.setting_name == "short_code_length"
            ).first()
            length = int(settings.setting_value) if settings else 6
            short_code = generate_short_code(length)
            while session.query(URL).filter(URL.short_code == short_code).first():
                short_code = generate_short_code(length)

        # Calculate expiration
        settings = session.query(Setting).filter(
            Setting.setting_name == "default_expiry_days"
        ).first()
        default_days = int(settings.setting_value) if settings else 30
        expires_at = calculate_expiry_date(url_data.expire_after_days or default_days)

        new_url = URL(
            short_code=short_code,
            original_url=validated_url,
            title=url_data.title,
            expires_at=expires_at,
            is_custom=bool(url_data.custom_code)
        )
        session.add(new_url)
        session.commit()
        return URLResponse.model_validate(new_url)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating shortened URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating shortened URL"
        )

@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    request: Request,
    session: Session = Depends(get_session)
):
    """Redirect to the original URL from a short code."""
    try:
        check_rate_limit(request)
        
        url = session.query(URL).filter(URL.short_code == short_code).first()
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found"
            )
            
        if url.expires_at and url.expires_at < datetime.utcnow():
            session.delete(url)
            session.commit()
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="URL has expired"
            )

        url.click_count += 1
        session.commit()
        
        return Response(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": url.original_url}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error redirecting URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing redirect"
        )