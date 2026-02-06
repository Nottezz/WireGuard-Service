from fastapi import APIRouter

from ..dependencies import DateBaseDepends
from wireguard_service.actions import get_client_config

router = APIRouter(
    prefix="/{server_name}/client_config",
    tags=["Client config"]
)

@router.get("/")
def render_client_config(db: DateBaseDepends, server_name: str, client_private_key: str, client_address: str):
    return get_client_config(db, server_name, client_private_key, client_address)
