from fastapi import APIRouter, Depends

from schemas.show import Interface
from ..dependencies import WGClientDepends


router: APIRouter = APIRouter(
    prefix="/show",
    tags=["Show configuration"],
)

@router.get("/")
def get_wg_config(wg_client: WGClientDepends, interface: str) -> Interface:
    return wg_client.show(interface=interface)
