from pydantic import BaseModel, HttpUrl, validator, Field
from typing import Optional
from datetime import datetime
import re

class URLBase(BaseModel):
    url: HttpUrl = Field(..., description="The original URL to be shortened")
    custom_code: Optional[str] = Field(None, min_length=3, max_length=32, description="Optional custom short code")
    title: Optional[str] = Field(None, max_length=200, description="Optional URL title")
    expire_after_days: Optional[int] = Field(None, gt=0, le=365, description="Days until URL expires")

    @validator('custom_code')
    def validate_custom_code(cls, v):
        if v is not None and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Custom code must contain only letters, numbers, underscores, and hyphens')
        return v

class URLCreate(URLBase):
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/very/long/url/path",
                "custom_code": "my-url",
                "title": "My Custom URL",
                "expire_after_days": 30
            }
        }

class URLResponse(URLBase):
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int = 0

    class Config:
        from_attributes = True

class Setting(BaseModel):
    setting_name: str = Field(..., pattern=r'^[a-z_]+$')
    setting_value: str
    updated_at: datetime

    class Config:
        from_attributes = True

class SettingUpdate(BaseModel):
    setting_value: str = Field(..., min_length=1)

    @validator('setting_value')
    def validate_setting_value(cls, v, values, **kwargs):
        if not v.strip():
            raise ValueError('Setting value cannot be empty or whitespace')
        return v.strip()