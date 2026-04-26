from typing import Optional

from pydantic import BaseModel


class PeerBase(BaseModel):
    endpoint: str | None = None
    allowed_ips: list[str] | None = None


class Peer(PeerBase):
    public_key: str
    latest_handshake: Optional[str] = None
    transfer: Optional[str] = None


class AddPeer(PeerBase):
    persistent_keepalive: int | None = None
