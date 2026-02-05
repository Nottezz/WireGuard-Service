from typing import List, Optional
from pydantic import BaseModel

from .peer import Peer


class InterfaceBase(BaseModel):
    name: str
    public_key: Optional[str] = None
    private_key: Optional[str] = None
    listening_port: Optional[int] = None
    peers: List[Peer] = []

class Interface(InterfaceBase):
    """
    Base model for all interfaces.
    """
