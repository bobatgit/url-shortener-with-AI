from fastapi import APIRouter
from .shortener import router as shortener_router
from .management import router as management_router

router = APIRouter()
router.include_router(shortener_router)
router.include_router(management_router)