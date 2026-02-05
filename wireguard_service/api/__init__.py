from fastapi import APIRouter

from .views import peers_router, tools_router, servers_router, interfaces_router


router = APIRouter(
    prefix="/api",
)
router.include_router(servers_router)
router.include_router(interfaces_router)
router.include_router(peers_router)
router.include_router(tools_router)
