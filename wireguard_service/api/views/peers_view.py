from fastapi import APIRouter

from wireguard_service.schemas.peer import AddPeer

from ..dependencies import WGClientDepends

router = APIRouter(
    prefix="/peers/{server_name}",
    tags=["Peers"],
)


@router.post("/add")
def add_new_peer(
    wg_client: WGClientDepends, peer_in: AddPeer, interface: str = "wg0"
) -> dict[str, str]:
    return wg_client.add_peer_with_keys(**peer_in.model_dump(), interface=interface)


@router.delete("/remove")
def delete_peer(
    wg_client: WGClientDepends, peer_pub_key: str, interface: str = "wg0"
) -> dict[str, str]:
    return wg_client.remove_peer_from_interface(
        interface=interface, public_key=peer_pub_key
    )
