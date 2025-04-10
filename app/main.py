from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import init_db
from .routes import router
from .errors import URLShortenerError
from .utils.rate_limit import check_rate_limit
from .utils.scheduler import scheduled_cleanup
from .utils.tasks import run_maintenance_tasks
from .utils.metrics import metrics
import logging
import asyncio

app = FastAPI(title="URL Shortener")

# Setup logging
logger = logging.getLogger(__name__)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Store background tasks
cleanup_task = None
maintenance_task = None

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    check_rate_limit(request)
    response = await call_next(request)
    return response

# Metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    metrics.track_request()
    response = await call_next(request)
    return response

# Initialize database and settings
@app.on_event("startup")
async def startup_event():
    logger.info("Starting URL Shortener application")
    init_db()
    # Start background tasks
    global cleanup_task, maintenance_task
    cleanup_task = asyncio.create_task(scheduled_cleanup())
    maintenance_task = asyncio.create_task(run_maintenance_tasks())

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down URL Shortener application")
    for task in [cleanup_task, maintenance_task]:
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

# Error handlers
@app.exception_handler(URLShortenerError)
async def url_shortener_exception_handler(request: Request, exc: URLShortenerError):
    logger.error(f"Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/manage")
async def manage(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})

# Metrics endpoint
@app.get("/metrics")
async def get_metrics(request: Request):
    return metrics.get_stats()

app.include_router(router)