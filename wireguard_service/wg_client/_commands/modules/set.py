from dataclasses import dataclass, field
from pathlib import Path
from typing import Self
from .._base import WGCommand


@dataclass
class PeerConfig:

    public_key: str
    remove: bool = False
    preshared_key_file: Path | None = None
    endpoint: str | None = None  # формат "ip:port"
    persistent_keepalive: int | None = None
    allowed_ips: list[str] = field(default_factory=list)

    def to_args(self) -> list[str]:
        args = ["peer", self.public_key]

        if self.remove:
            args.append("remove")
            return args

        if self.preshared_key_file:
            args.extend(["preshared-key", str(self.preshared_key_file)])

        if self.endpoint:
            args.extend(["endpoint", self.endpoint])

        if self.persistent_keepalive is not None:
            args.extend(["persistent-keepalive", str(self.persistent_keepalive)])

        if self.allowed_ips:
            args.extend(["allowed-ips", ",".join(self.allowed_ips)])

        return args


class Set(WGCommand):

    def __init__(self, interface: str, *, options: list[str] | None = None):
        super().__init__(options=options)
        self.interface = interface
        self._listen_port: int | None = None
        self._fwmark: int | None = None
        self._private_key_file: Path | None = None
        self._peers: list[PeerConfig] = []
        self._options = options or []

    def listen_port(self, port: int) -> Self:
        self._listen_port = port
        return self

    def fwmark(self, mark: int) -> Self:
        self._fwmark = mark
        return self

    def private_key_file(self, path: str | Path) -> Self:
        self._private_key_file = Path(path)
        return self

    def add_peer(self, peer: PeerConfig) -> Self:
        self._peers.append(peer)
        return self

    def remove_peer(self, public_key: str) -> Self:
        self._peers.append(PeerConfig(public_key=public_key, remove=True))
        return self

    def _build_arguments(self) -> list[str]:
        args = ["set", self.interface]

        if self._listen_port is not None:
            args.extend(["listen-port", str(self._listen_port)])

        if self._fwmark is not None:
            args.extend(["fwmark", str(self._fwmark)])

        if self._private_key_file:
            args.extend(["private-key", str(self._private_key_file)])

        for peer in self._peers:
            args.extend(peer.to_args())

        return args


    def execute(self, ssh_client):
        arguments = self._build_arguments()
        super().__init__(options=self._options, arguments=arguments)
        return super().execute(ssh_client)
