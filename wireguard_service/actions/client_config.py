import logging

from sqlalchemy.orm import Session
from wireguard_service.storages.servers import get_server
from wireguard_service.helpers import render_client_config

logger = logging.getLogger(__name__)

def get_client_config(db: Session, server_name: str, client_private_key: str, client_address: str) -> str:
    server = get_server(db=db, server_name=server_name)
    return render_client_config(server, client_private_key, client_address)
