import logging.config
import os
from pathlib import Path

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": LOG_DIR / "url_shortener.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": LOG_DIR / "error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": "ERROR",
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file", "error_file"],
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "file", "error_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

def setup_logging():
    """Initialize logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)