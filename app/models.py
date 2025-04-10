from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = None
    expire_after_days: Optional[int] = None
    title: Optional[str] = None

class URLResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int
    title: Optional[str]

    class Config:
        from_attributes = True