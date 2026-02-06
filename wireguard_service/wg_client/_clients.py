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

    def generate_private_key(self) -> str:
        stdout, stderr = self.exec(command=modules.generate_key.Genkey("genkey"))
        return stdout.removesuffix("\n")

    def generate_public_key(self, private_key: str) -> str:
        stdout, stderr = self.exec(command=modules.generate_key.Genkey("pubkey"), stdin=private_key)
        if stderr:
            raise RuntimeError(f"WG command failed: {stderr.strip()}")
        return stdout.removesuffix("\n")

    def gen_keypair(self) -> tuple[str, str]:
        """
        Returns: (private_key, public_key)
        """
        # 1. private key
        private_key = self.generate_private_key()

        # 2. public key from private
        stdout, stderr = self.exec(
            command=modules.generate_key.Genkey(
                "pubkey",
                stdin=private_key,
            )
        )
        if stderr:
            raise RuntimeError(f"wg pubkey failed: {stderr.strip()}")

        public_key = stdout.strip()

        return private_key, public_key

    def add_peer_with_keys(
            self,
            interface: str,
            allowed_ips: list[str],
            endpoint: str | None = None,
            persistent_keepalive: int | None = None,
    ) -> dict:
        private_key, public_key = self.gen_keypair()

        peer = PeerConfig(
            public_key=public_key,
            allowed_ips=allowed_ips,
            endpoint=endpoint,
            persistent_keepalive=persistent_keepalive,
        )

        command = Set(interface, options=self.options).add_peer(peer)
        self.exec(command)

        return {
            "private_key": private_key,
            "public_key": public_key,
        }

    def remove_peer_from_interface(
            self,
            interface: str,
            public_key: str,
    ) -> dict[str, str]:
        self.exec(
            Set(interface, options=self.options).remove_peer(public_key)
        )
        return {"status": "success", "message": f"Peer <{public_key}> removed from interface"}
