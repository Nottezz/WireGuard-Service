from fastapi import APIRouter

from .detail_peer import router as detail_peer

router = APIRouter(
    prefix="/peers",
    tags=["Peers"],
)
router.include_router(detail_peer)
