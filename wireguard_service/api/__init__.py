from fastapi import APIRouter

from .views.config_view import router as show_view

router = APIRouter(
    prefix="/api",
)
router.include_router(show_view)
