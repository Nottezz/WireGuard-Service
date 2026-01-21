from typing import Optional

from pydantic import BaseModel


class PeerBase(BaseModel):
    public_key: str
    endpoint: str | None = None
    allowed_ips: list[str]


class Peer(PeerBase):
    name: str | None = None # todo: подумать и сделать обязательным для заполнения
    latest_handshake: str | None = None
    transfer: str | None = None


class AddPeer(PeerBase):
    name: str
    persistent_keepalive: int | None = None
