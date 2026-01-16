import logging
from typing import Annotated

from fastapi import Depends

from wg_client import WGClient
from wireguard_service.config import Settings

logger = logging.getLogger(__name__)

def get_settings() -> Settings:
    return Settings()


def wg_client(settings: Settings = Depends(get_settings)) -> WGClient:
    ssh_kwargs = settings.ssh_config.kwargs
    username = settings.ssh_config.username
    password = settings.ssh_config.password
    if password:
        ssh_kwargs["password"] = password

    ssh_args = {
        "host": settings.ssh_config.host,
        "port": settings.ssh_config.port,
        "username": username,
        "ssh_extra_kwargs": ssh_kwargs,
    }
    logger.info(
        "Connecting: %s@%s:%s" % (username, settings.ssh_config.host, settings.ssh_config.port)
    )
    return WGClient.with_ssh(**ssh_args)


WGClientDepends = Annotated[WGClient, Depends(wg_client)]
