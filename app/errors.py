from fastapi import HTTPException, status

class URLShortenerError(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class URLNotFoundError(URLShortenerError):
    def __init__(self, short_code: str):
        super().__init__(
            detail=f"URL with short code '{short_code}' not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class URLExpiredError(URLShortenerError):
    def __init__(self, short_code: str):
        super().__init__(
            detail=f"URL with short code '{short_code}' has expired",
            status_code=status.HTTP_410_GONE
        )

class ShortCodeExistsError(URLShortenerError):
    def __init__(self, short_code: str):
        super().__init__(
            detail=f"Short code '{short_code}' already exists",
            status_code=status.HTTP_409_CONFLICT
        )

class InvalidSettingError(URLShortenerError):
    def __init__(self, setting_name: str):
        super().__init__(
            detail=f"Invalid setting: {setting_name}",
            status_code=status.HTTP_400_BAD_REQUEST
        )