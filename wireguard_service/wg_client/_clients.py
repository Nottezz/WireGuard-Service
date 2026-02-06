import socket
from pathlib import Path
from typing import Any

import paramiko

from wireguard_service.helpers import parse_wg_show
from wireguard_service.schemas.interface import Interface
from ._commands import WGCommand, modules
from ._commands.modules.set import PeerConfig, Set
from ._protocols import SSHClient


class WGClient:
    def __init__(self, ssh_client: SSHClient) -> None:
        self.ssh_client = ssh_client
        self.options: list = []

    @classmethod
    def with_ssh(
        cls,
        host: str,
        port: int,
        username: str,
        key_filename: str | None = None,
        ssh_extra_kwargs: dict[str, Any] | None = None,
    ) -> "WGClient":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            key_filename=key_filename,
            **(ssh_extra_kwargs or {}),
        )
        return cls(ssh)

    @classmethod
    def check_connection(
            cls,
            host: str,
            port: int,
            username: str,
            key_filename: str | None = None,
            ssh_extra_kwargs: dict[str, Any] | None = None,
    ) -> bool:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                hostname=host,
                port=port,
                username=username,
                key_filename=key_filename,
                timeout=5,
                **(ssh_extra_kwargs or {}),
            )
            return True
        except (paramiko.AuthenticationException, paramiko.SSHException, socket.error):
            return False
        finally:
            ssh.close()

    def exec(self, command: WGCommand) -> tuple[str, str]:
        return command.execute(self.ssh_client)

    def show(
        self,
        interface: str | None = None,
        public_key: bool = False,
        private_key: bool = False,
        listen_port: bool = False,
        peers: bool = False,
        endpoints: bool = False,
        latest_handshakes: bool = False,
    ) -> Interface:
        stdout, stderr = self.exec(
            command=modules.show.Show(
                "show",
                interface=interface,
                public_key=public_key,
                private_key=private_key,
                listen_port=listen_port,
                peers=peers,
                endpoints=endpoints,
                latest_handshakes=latest_handshakes,
                options=self.options,
            )
        )
        return parse_wg_show(stdout)

    def genkey(self) -> str:
        stdout, stderr = self.exec(command=modules.generate_key.Genkey("genkey"))
        return stdout.removesuffix("\n")

    def genpsk(self) -> str:
        stdout, stderr = self.exec(command=modules.generate_key.Genkey("genpsk"))
        if stderr:
            raise RuntimeError(f"WG command failed: {stderr.strip()}")
        return stdout.removesuffix("\n")

    def add_peer(
        self,
        interface: str,
        public_key: str,
        allowed_ips: list[str],
        endpoint: str | None = None,
        preshared_key_file: str | None = None,
        persistent_keepalive: int | None = None,
    ) -> None:

        peer = PeerConfig(
            public_key=public_key,
            allowed_ips=allowed_ips,
            endpoint=endpoint,
            preshared_key_file=Path(preshared_key_file) if preshared_key_file else None,
            persistent_keepalive=persistent_keepalive,
        )

        command = Set(interface, options=self.options).add_peer(peer)
        self.exec(command)

    def remove_peer_from_interface(
        self,
        interface: str,
        public_key: str,
    ) -> None:

        self.exec(
            Set(interface, options=self.options).remove_peer(public_key)
        )
