from fastapi import APIRouter

from .config_view import router as config_router

router = APIRouter(
    prefix="/interfaces/{interface}",
    tags=["Interfaces"],
)
router.include_router(config_router)
