from schemas.peer import AddPeer, Peer
from wg_client import WGClient
from storages import storage
import logging

logger = logging.getLogger(__name__)

def add_peer(wg_client: WGClient, peer_in: AddPeer, interface: str = "all", ) -> Peer:
    peer = storage.create_or_raise_if_exists(peer_in)
    wg_client.add_peer(interface=interface, **peer.model_dump(exclude={"name"}))
    return peer

def delete_peer(wg_client: WGClient, public_key: str, interface: str = "all") -> None:
    peer = storage.get_peer(public_key)
    storage.delete(peer)
    return wg_client.remove_peer_from_interface(interface=interface, public_key=peer.public_key)
