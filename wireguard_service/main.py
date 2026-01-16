import logging

from fastapi import FastAPI

from wireguard_service.api import router as api_router
from wireguard_service.app_lifespan import lifespan
from wireguard_service.config import settings

logging.basicConfig(
    format=settings.logging.log_format,
    level=settings.logging.log_level,
    datefmt=settings.logging.log_date_format,
)
app = FastAPI(
    title="WireGuard API",
    description="Manage WireGuard VPN service",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(api_router)
