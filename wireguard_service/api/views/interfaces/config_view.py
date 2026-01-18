from fastapi import APIRouter, Depends

from schemas.interface import Interface
from api.dependencies import WGClientDepends


router: APIRouter = APIRouter(
    prefix="/show_config",
)

@router.get("/")
def get_wg_config(wg_client: WGClientDepends, interface: str) -> Interface:
    return wg_client.show(interface=interface)
