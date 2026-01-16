from fastapi import APIRouter

from ..dependencies import WGClientDepends

router: APIRouter = APIRouter(
    prefix="/key",
    tags=["Generate private or public key"],
)

@router.get("/private")
def generate_private_key(wg_client: WGClientDepends) -> str:
    return wg_client.genkey()

@router.get("/public")
def generate_public_key(wg_client: WGClientDepends) -> str:
    return wg_client.genpsk()
