from fastapi import APIRouter

from .generate_key import router as generate_key_router

router = APIRouter(prefix="/tools")
router.include_router(generate_key_router)
