from fastapi.templating import Jinja2Templates

from wireguard_service.config import TEMPLATE_DIR

templates = Jinja2Templates(directory=TEMPLATE_DIR)
