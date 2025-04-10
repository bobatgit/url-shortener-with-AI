import pytest
from datetime import datetime, timedelta
from app.utils.url_utils import generate_short_code, calculate_expiry_date
from app.utils.security import validate_url, validate_custom_code
from fastapi import HTTPException

def test_generate_short_code():
    code1 = generate_short_code()
    code2 = generate_short_code()
    assert len(code1) == 6
    assert code1 != code2
    assert code1.isalnum()

def test_calculate_expiry_date():
    days = 7
    expiry = calculate_expiry_date(days)
    expected = datetime.utcnow() + timedelta(days=days)
    assert abs((expiry - expected).total_seconds()) < 1

def test_validate_url():
    # Valid URLs
    assert validate_url("https://example.com") == "https://example.com"
    assert validate_url("http://test.com/path?q=1") == "http://test.com/path?q=1"
    
    # Invalid URLs
    with pytest.raises(HTTPException):
        validate_url("not-a-url")
    with pytest.raises(HTTPException):
        validate_url("ftp://example.com")

def test_validate_custom_code():
    # Valid codes
    assert validate_custom_code("abc123")
    assert validate_custom_code("test-url")
    assert validate_custom_code("my_url_2")
    
    # Invalid codes
    assert not validate_custom_code("")
    assert not validate_custom_code("a" * 33)  # Too long
    assert not validate_custom_code("special$chars")