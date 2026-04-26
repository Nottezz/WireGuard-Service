from pydantic import BaseModel


class ClientConfigBase(BaseModel):
    client_private_key: str
    client_address: str
    interface: str


class ClientConfig(ClientConfigBase):
    """
    Client config
    """
