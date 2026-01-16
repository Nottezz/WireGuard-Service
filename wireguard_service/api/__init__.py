from fastapi import APIRouter

from .views.config_view import router as show_view
from .views.generate_key import router as generate_key

router = APIRouter(
    prefix="/api",
)
router.include_router(show_view)
router.include_router(generate_key)
