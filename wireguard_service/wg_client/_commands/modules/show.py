from wireguard_service.wg_client._commands._base import _NOT_SET, WGCommand


class Show(WGCommand):
    """
    wg show { <interface> | all | interfaces }
    [public-key | private-key | listen-port | fwmark | peers | preshared-keys | endpoints | allowed-ips | latest-handshakes | transfer | persistent-keepalive | dump]
    """

    def __init__(
        self,
        interface: str = "all",
        public_key: str = _NOT_SET,
        private_key: str = _NOT_SET,
        listen_port: int = _NOT_SET,
        peers: bool = _NOT_SET,
        endpoints: bool = _NOT_SET,
        latest_handshakes: bool = _NOT_SET,
        *,
        options: list[str] | None = None,
    ):
        arguments = []
        if interface is not _NOT_SET:
            arguments += [interface]
        if public_key is not _NOT_SET:
            arguments += [public_key]
        if private_key is not _NOT_SET:
            arguments += [private_key]
        if listen_port is not _NOT_SET:
            arguments += [listen_port]
        if peers is not _NOT_SET:
            arguments += ["peers"]
        if endpoints is not _NOT_SET:
            arguments += ["endpoints"]
        if latest_handshakes is not _NOT_SET:
            arguments += ["latest_handshakes"]

        super().__init__(
            options=options,
            arguments=arguments
        )
