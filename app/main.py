from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import init_db

app = FastAPI(title="URL Shortener")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Import and include routers
from .routes import shortener, management

# Include routers with prefixes
app.include_router(shortener.router)
app.include_router(management.router, prefix="/manage", tags=["management"])

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Root endpoint for homepage
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Management interface endpoint
@app.get("/manage")
async def manage(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})