from typing import Optional

from pydantic import BaseModel


class PeerBase(BaseModel):
    public_key: str
    endpoint: str | None = None
    allowed_ips: list[str]


class Peer(PeerBase):
    latest_handshake: Optional[str] = None
    transfer: Optional[str] = None


class AddPeer(PeerBase):
    persistent_keepalive: int | None = None
