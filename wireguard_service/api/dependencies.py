import logging
from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.orm import Session

from wireguard_service.config import Settings
from wireguard_service.storages.database import get_db
from wireguard_service.storages.servers import get_server
from wireguard_service.infrastructure.wg_client import WGClient

logger = logging.getLogger(__name__)


def get_settings() -> Settings:
    return Settings()


def wg_client(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    server_name: str = Path(...),
) -> WGClient:
    server = get_server(db, server_name)
    ssh_kwargs = settings.ssh_config.kwargs

    ssh_args = {
        "host": str(server.host),
        "port": server.port,
        "username": server.username,
        "ssh_extra_kwargs": ssh_kwargs,
    }
    logger.debug("SSH information: %s", ssh_args)
    logger.info("Connecting: %s@%s:%s" % (server.username, server.host, server.port))
    return WGClient.with_ssh(**ssh_args)


WGClientDepends = Annotated[WGClient, Depends(wg_client)]
DateBaseDepends = Annotated[Session, Depends(get_db)]
