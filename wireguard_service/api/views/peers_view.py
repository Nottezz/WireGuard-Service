from fastapi import APIRouter

from wireguard_service.schemas.peer import AddPeer
from wireguard_service.storages.wireguard import crud as wg_crud

from ..dependencies import WGClientDepends

router = APIRouter(
    prefix="/peers/{server_name}",
    tags=["Peers"],
)


@router.post("/add")
def add_new_peer(
    wg_client: WGClientDepends, peer_in: AddPeer, interface: str = "wg0"
) -> dict[str, str]:
    return wg_crud.add_peer(wg_client, interface, **peer_in.model_dump())


@router.delete("/remove")
def delete_peer(
    wg_client: WGClientDepends, peer_pub_key: str, interface: str = "wg0"
) -> dict[str, str]:
    return wg_crud.remove_peer(wg_client, interface, peer_pub_key)
