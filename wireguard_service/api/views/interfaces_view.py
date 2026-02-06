from fastapi import APIRouter

from wireguard_service.schemas.interface import Interface

from ..dependencies import DateBaseDepends, WGClientDepends

router = APIRouter(
    prefix="/interfaces/{server_name}",
    tags=["Interfaces"],
)


@router.get("/get_config")
def get_wireguard_config(
    wg_client: WGClientDepends, interface: str = "wg0"
) -> Interface:
    return wg_client.show(interface=interface)
