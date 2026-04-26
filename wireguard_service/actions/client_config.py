import logging

from infrastructure.wireguard import WGClient
from sqlalchemy.orm import Session

from wireguard_service.helpers import render_client_config
from wireguard_service.storages.servers import get_server
from wireguard_service.storages.wireguard import crud as wg_crud

logger = logging.getLogger(__name__)


def get_client_config(
    db: Session,
    wg_client: WGClient,
    server_name: str,
    client_private_key: str,
    client_address: str,
    interface,
) -> str:
    server = get_server(db=db, server_name=server_name)
    server_config = wg_crud.get_config(wg_client, interface=interface)
    server_listening_port = server_config.listening_port
    return render_client_config(
        server, server_listening_port, client_private_key, client_address
    )
