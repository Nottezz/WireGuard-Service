from fastapi import APIRouter

from .views import tools_router, servers_router, interfaces_router, peers_router, client_config_router


router = APIRouter(
    prefix="/api",
)
router.include_router(servers_router)
router.include_router(interfaces_router)
router.include_router(peers_router)
router.include_router(client_config_router)
router.include_router(tools_router)
