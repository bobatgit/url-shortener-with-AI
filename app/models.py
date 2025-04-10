from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = Field(None, min_length=3, max_length=32)
    title: Optional[str] = None
    expire_after_days: Optional[int] = Field(None, gt=0, le=365)

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
    short_code: str = Field(..., min_length=3, max_length=32)
    original_url: HttpUrl
    title: Optional[str] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    click_count: int = Field(default=0, ge=0)
    is_custom: bool = False

    class Config:
        from_attributes = True

class Setting(BaseModel):
    setting_name: str
    setting_value: str
    updated_at: datetime

    class Config:
        from_attributes = True

class SettingUpdate(BaseModel):
    setting_value: str