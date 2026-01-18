from fastapi import APIRouter

from schemas.peer import AddPeer
from api.dependencies import WGClientDepends

router: APIRouter = APIRouter(
    prefix="/{interface}",
)


@router.post("/add_peer")
def add_peer(
    wg_client: WGClientDepends,
    interface: str,
    peer: AddPeer,
):
    wg_client.add_peer(
        interface=interface,
        public_key=peer.public_key,
        allowed_ips=peer.allowed_ips,
        endpoint=peer.endpoint,
        persistent_keepalive=peer.persistent_keepalive,
    )
    return {"status": "success", "interface": interface}

@router.delete("/delete_peer/{public_key}")
async def remove_peer(
    wg_client: WGClientDepends,
    interface: str,
    public_key: str,
):
    wg_client.remove_peer_from_interface(
        interface=interface,
        public_key=public_key,
    )
    return {"status": "success", "message": f"Peer <{public_key!r}> removed from {interface}"}
