import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse
from ..errors import URLShortenerError
from typing import Any, Dict, Optional

logger = structlog.get_logger(__name__)

async def url_shortener_exception_handler(
    request: Request,
    exc: URLShortenerError
) -> JSONResponse:
    """Handle application-specific exceptions with structured logging."""
    log_context = {
        "error_type": exc.__class__.__name__,
        "status_code": exc.status_code,
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host,
    }
    
    if hasattr(exc, "detail"):
        log_context["detail"] = exc.detail
    
    logger.error("request_error", **log_context)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions with structured logging."""
    log_context = {
        "error_type": exc.__class__.__name__,
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host,
    }
    
    logger.exception("unexpected_error", exc_info=exc, **log_context)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again later."
        }
    )