from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import URL, get_session
from .models import URLCreate, URLResponse
from .utils import generate_short_code, calculate_expiry_date, fetch_page_title
from datetime import datetime

router = APIRouter()

@router.post("/urls", response_model=URLResponse)
async def create_url(url_create: URLCreate, session: Session = Depends(get_session)):
    short_code = url_create.custom_code or generate_short_code()
    
    existing_url = session.query(URL).filter(URL.short_code == short_code).first()
    if existing_url:
        raise HTTPException(status_code=400, detail="Short code already exists")
    
    expires_at = None
    if url_create.expire_after_days:
        expires_at = calculate_expiry_date(url_create.expire_after_days)
    
    title = url_create.title
    if not title:
        title = await fetch_page_title(str(url_create.url))
    
    db_url = URL(
        original_url=str(url_create.url),
        short_code=short_code,
        expires_at=expires_at,
        title=title
    )
    session.add(db_url)
    session.commit()
    session.refresh(db_url)
    return db_url

@router.get("/{short_code}")
async def redirect_url(short_code: str, session: Session = Depends(get_session)):
    url = session.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url.expires_at and url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="URL has expired")
    
    url.clicks += 1
    session.commit()
    return {"url": url.original_url}

@router.get("/urls/", response_model=list[URLResponse])
async def list_urls(session: Session = Depends(get_session)):
    urls = session.query(URL).order_by(URL.created_at.desc()).all()
    return urls