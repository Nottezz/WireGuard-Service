from wireguard_service.infrastructure.wireguard._commands._base import \
    WGCommand


class Show(WGCommand):
    """
    wg show { <interface> | all | interfaces }
    [public-key | private-key | listen-port | fwmark | peers | preshared-keys | endpoints | allowed-ips | latest-handshakes | transfer | persistent-keepalive | dump]
    """

    def __init__(
        self,
        key: str,
        interface: str = "all",
        *,
        public_key: bool = False,
        private_key: bool = False,
        listen_port: bool = False,
        peers: bool = False,
        endpoints: bool = False,
        latest_handshakes: bool = False,
        options: list[str] | None = None,
    ):
        arguments = [key, interface]

        if public_key:
            arguments.append("public-key")
        if private_key:
            arguments.append("private-key")
        if listen_port:
            arguments.append("listen-port")
        if peers:
            arguments.append("peers")
        if endpoints:
            arguments.append("endpoints")
        if latest_handshakes:
            arguments.append("latest-handshakes")

        super().__init__(
            options=options,
            arguments=arguments,
        )
