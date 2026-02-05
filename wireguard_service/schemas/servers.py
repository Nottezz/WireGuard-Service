from pydantic import BaseModel, IPvAnyAddress
from annotated_types import Len
from typing import Annotated

class ServerBase(BaseModel):
    host: IPvAnyAddress
    port: int
    username: str
    server_name: Annotated[str, Len(min_length=5, max_length=100)]

class ServerCreate(ServerBase):
    """
    Schema for server creation
    """

class ServerUpdate(ServerBase):
    """
    Schema for server update
    """

class Server(ServerBase):
    """
    Schema for read server information
    """
