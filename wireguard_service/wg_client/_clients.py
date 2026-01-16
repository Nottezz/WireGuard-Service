from typing import Any

import paramiko

from helpers import parse_wg_show
from schemas.show import Interface
from ._commands import WGCommand, modules
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
        if stderr:
            raise RuntimeError(f"WG command failed: {stderr.strip()}")
        return parse_wg_show(stdout)

    def genkey(self):
        stdout, stderr = self.exec(command=modules.generate_key.Genkey("genkey"))
        if stderr:
            raise RuntimeError(f"WG command failed: {stderr.strip()}")
        return stdout

    def genpsk(self):
        stdout, stderr = self.exec(command=modules.generate_key.Genkey("genpsk"))
        if stderr:
            raise RuntimeError(f"WG command failed: {stderr.strip()}")
        return stdout
