from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = None
    title: Optional[str] = None
    expire_after_days: Optional[int] = None

class URLCreate(URLBase):
    pass

class URLResponse(URLBase):
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int = 0

    class Config:
        from_attributes = True

class URL(BaseModel):
    short_code: str
    original_url: HttpUrl
    title: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int = 0
    is_custom: bool = False

class Setting(BaseModel):
    setting_name: str
    setting_value: str
    updated_at: datetime