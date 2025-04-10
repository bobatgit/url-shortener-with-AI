from fastapi import APIRouter
from .shortener import router as shortener_router
from .management import router as management_router
from .monitoring import router as monitoring_router

router = APIRouter()
router.include_router(shortener_router)
router.include_router(management_router)
router.include_router(monitoring_router)