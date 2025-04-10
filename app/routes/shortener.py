from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..database import URL, Setting, get_session
from ..models import URLCreate, URLResponse
from ..utils.url_utils import generate_short_code, calculate_expiry_date, fetch_page_title
from ..utils.metrics import metrics
from ..utils.security import validate_url, validate_custom_code
from ..utils.cache import url_cache
from ..errors import URLNotFoundError, URLExpiredError, ShortCodeExistsError
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def get_setting_value(name: str, session: Session) -> str:
    setting = session.query(Setting).filter(Setting.setting_name == name).first()
    return setting.setting_value if setting else None

@router.post("/urls", response_model=URLResponse)
async def create_url(request: Request, url_create: URLCreate, session: Session = Depends(get_session)):
    logger.info(f"Creating short URL for: {url_create.url}")
    
    # Validate input URL
    validate_url(str(url_create.url))
    
    if url_create.custom_code:
        allow_custom = await get_setting_value("allow_custom_urls", session)
        if allow_custom.lower() != "true":
            raise ShortCodeExistsError("Custom URLs are not allowed")
        
        if not validate_custom_code(url_create.custom_code):
            raise HTTPException(status_code=400, detail="Invalid custom code format")
        
        existing_url = session.query(URL).filter(URL.short_code == url_create.custom_code).first()
        if existing_url:
            raise ShortCodeExistsError(url_create.custom_code)
        short_code = url_create.custom_code
    else:
        code_length = int(await get_setting_value("short_code_length", session) or 6)
        short_code = generate_short_code(code_length)
    
    expires_at = None
    if url_create.expire_after_days:
        expires_at = calculate_expiry_date(url_create.expire_after_days)
    else:
        default_days = int(await get_setting_value("default_expiry_days", session) or 30)
        expires_at = calculate_expiry_date(default_days)
    
    title = url_create.title
    if not title:
        title = await fetch_page_title(str(url_create.url))
    
    db_url = URL(
        original_url=str(url_create.url),
        short_code=short_code,
        expires_at=expires_at,
        title=title,
        is_custom=bool(url_create.custom_code)
    )
    session.add(db_url)
    session.commit()
    session.refresh(db_url)
    
    metrics.track_url_creation()
    url_cache.set(short_code, db_url)
    logger.info(f"Created short URL: {short_code} -> {url_create.url}")
    return db_url

@router.get("/{short_code}")
async def redirect_url(request: Request, short_code: str, session: Session = Depends(get_session)):
    # Check cache first
    cached_url = url_cache.get(short_code)
    if cached_url:
        if cached_url.expires_at and cached_url.expires_at < datetime.utcnow():
            url_cache._remove(short_code)
        else:
            cached_url.clicks += 1
            session.merge(cached_url)
            session.commit()
            metrics.track_redirect(short_code)
            logger.info(f"Redirecting {short_code} -> {cached_url.original_url} (from cache)")
            return {"url": cached_url.original_url}
    
    # If not in cache, query database
    url = session.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        logger.warning(f"Attempted access to non-existent short code: {short_code}")
        raise URLNotFoundError(short_code)
    
    if url.expires_at and url.expires_at < datetime.utcnow():
        logger.info(f"Attempted access to expired URL: {short_code}")
        raise URLExpiredError(short_code)
    
    url.clicks += 1
    session.commit()
    
    metrics.track_redirect(short_code)
    url_cache.set(short_code, url)
    logger.info(f"Redirecting {short_code} -> {url.original_url}")
    return {"url": url.original_url}