from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, ConfigDict, IPvAnyAddress


class ServerBase(BaseModel):
    host: IPvAnyAddress
    port: int
    username: str
    server_name: Annotated[str, Len(min_length=5, max_length=100)]

    model_config = ConfigDict(from_attributes=True)


class ServerCreate(ServerBase):
    """
    Schema for server creation
    """


class ServerUpdate(ServerBase):
    """
    Schema for server update
    """

    host: IPvAnyAddress | None = None
    port: int | None = None
    username: str | None = None
    public_key: str | None = None
    server_name: Annotated[str, Len(min_length=5, max_length=100)] | None = None


class ServerRead(ServerBase):
    """
    Schema for read server information
    """

    public_key: str | None = None
