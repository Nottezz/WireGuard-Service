from fastapi import APIRouter

from wireguard_service.schemas import ServerRead, ServerCreate
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

@router.get("/check/{server_name}")
def check_server_connection(db: DateBaseDepends, server_name: str, wg_client: WGClientDepends) -> bool:
    server = servers.get_server(db, server_name)
    return wg_client.check_connection(str(server.host), server.port, server.username)

@router.post("/")
def create_server(db: DateBaseDepends, server_in: ServerCreate) -> ServerRead:
    return servers.add_server(db, server_in)

@router.delete("/{server_name}")
def delete_server(db: DateBaseDepends, server_name: str) -> ServerRead:
    return servers.delete_server(db, server_name)
