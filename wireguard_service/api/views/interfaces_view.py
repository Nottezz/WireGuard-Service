from fastapi import APIRouter

from wireguard_service.schemas.interface import Interface
from wireguard_service.storages.wireguard import crud as wg_crud

from ..dependencies import DateBaseDepends, WGClientDepends

router = APIRouter(
    prefix="/interfaces/{server_name}",
    tags=["Interfaces"],
)


@router.get("/get_config")
def get_wireguard_config(
    wg_client: WGClientDepends, interface: str = "wg0"
) -> Interface:
    return wg_crud.get_config(wg_client, interface=interface)
