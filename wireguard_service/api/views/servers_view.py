from fastapi import APIRouter

from wireguard_service.schemas import ServerCreate, ServerRead, ServerUpdate
from wireguard_service.storages import servers

from ..dependencies import DateBaseDepends, WGClientDepends

router = APIRouter(
    prefix="/server",
    tags=["Servers"],
)


@router.get("/")
def get_servers(db: DateBaseDepends) -> list[ServerRead]:
    return servers.get_list_servers(db)


@router.get("/{server_name}")
def get_server(db: DateBaseDepends, server_name: str) -> ServerRead:
    return servers.get_server(db, server_name)


@router.get("/{server_name}/check")
def check_server_connection(
    db: DateBaseDepends, server_name: str, wg_client: WGClientDepends
) -> bool:
    server = servers.get_server(db, server_name)
    return wg_client.check_connection(str(server.host), server.port, server.username)


@router.post("/{server_name}")
def create_server(db: DateBaseDepends, server_in: ServerCreate) -> ServerRead:
    return servers.add_server(db, server_in)


@router.patch("/{server_name}")
def partial_update_server(
    db: DateBaseDepends, server_in: ServerUpdate, server_name: str
) -> ServerRead:
    return servers.partial_update_server_info(db, server_in, server_name=server_name)


@router.delete("/{server_name}")
def delete_server(db: DateBaseDepends, server_name: str) -> ServerRead:
    return servers.delete_server(db, server_name)
