from fastapi import APIRouter
from schemas.client_config import ClientConfig

from wireguard_service.actions import get_client_config

from ..dependencies import DateBaseDepends, WGClientDepends

router = APIRouter(prefix="/client_config/{server_name}", tags=["Client config"])


@router.post("/render")
def render_client_config(
    db: DateBaseDepends,
    wg_client: WGClientDepends,
    server_name: str,
    client_config: ClientConfig,
):
    return get_client_config(db, wg_client, server_name, **client_config.model_dump())
