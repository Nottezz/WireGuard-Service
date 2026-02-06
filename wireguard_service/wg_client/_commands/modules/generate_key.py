from .._base import WGCommand

class Genkey(WGCommand):
    """
    Generates a new private or pub key and writes it to stdout
    """
    def __init__(self, key: str, *, stdin: str | None = None,options: list[str] | None = None) -> None:
        arguments = [key]
        super().__init__(
            options=options,
            arguments=arguments,
            stdin=stdin,
        )
