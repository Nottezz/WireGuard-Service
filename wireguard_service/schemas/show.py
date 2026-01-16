from typing import List, Optional
from pydantic import BaseModel


class Peer(BaseModel):
    public_key: str
    endpoint: Optional[str] = None
    allowed_ips: Optional[str] = None
    latest_handshake: Optional[str] = None
    transfer: Optional[str] = None


class Interface(BaseModel):
    name: str
    public_key: Optional[str] = None
    private_key: Optional[str] = None
    listening_port: Optional[int] = None
    peers: List[Peer] = []
