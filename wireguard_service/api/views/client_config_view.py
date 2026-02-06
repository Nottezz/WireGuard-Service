from fastapi import APIRouter

from wireguard_service.actions import get_client_config

from ..dependencies import DateBaseDepends

router = APIRouter(prefix="/client_config/{server_name}", tags=["Client config"])


@router.get("/")
def render_client_config(
    db: DateBaseDepends, server_name: str, client_private_key: str, client_address: str
):
    return get_client_config(db, server_name, client_private_key, client_address)
