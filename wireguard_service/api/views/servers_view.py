from fastapi import APIRouter
from sqlalchemy.orm import Session

from wireguard_service.schemas import ServerRead, ServerCreate
from wireguard_service.storages import servers

router = APIRouter(
    prefix="/server",
)

@router.get("/")
def get_servers(db: Session) -> list[ServerRead]:
    return servers.get_list_servers(db)

@router.get("/{server_name}")
def get_server(db: Session, server_name: str) -> ServerRead:
    return servers.get_server(db, server_name)


@router.post("/")
def create_server(db: Session, server_in: ServerCreate) -> ServerRead:
    return servers.add_server(db, server_in)

@router.delete("/{server_name}")
def delete_server(db: Session, server_name: str) -> ServerRead:
    return servers.delete_server(db, server_name)
