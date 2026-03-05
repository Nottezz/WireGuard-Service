from wireguard_service.infrastructure.wireguard._commands._base import \
    WGCommand
from wireguard_service.infrastructure.wireguard._parameters import WGExecutable


class WGQuickSave(WGCommand):
    """
    Usage: wg-quick [ up | down | save | strip ] [ CONFIG_FILE | INTERFACE ]
    """

    def __init__(
        self,
        interface: str = "all",
        options: list[str] | None = None,
    ):
        arguments = ["save", interface]
        super().__init__(
            executable=WGExecutable.WG_QUICK,
            arguments=arguments,
            options=options,
        )
