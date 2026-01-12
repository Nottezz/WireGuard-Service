import paramiko
from typing import Any
from ._protocols import SSHClient

from _commands import WGCommand, _NOT_SET, modules


class WGClient:
    def __init__(self, ssh_client: SSHClient) -> None:
        self.ssh_client = ssh_client

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
        public_key: str = _NOT_SET,
        private_key: str = _NOT_SET,
        listen_port: int = _NOT_SET,
        peers: bool = _NOT_SET,
        endpoints: bool = _NOT_SET,
        latest_handshakes: bool = _NOT_SET,
    ) -> tuple[str, str]:
        return self.exec(
            command=modules.show.Show(
                interface=interface,
                public_key=public_key,
                private_key=private_key,
                listen_port=listen_port,
                peers=peers,
                endpoints=endpoints,
                latest_handshakes=latest_handshakes,
            )
        )
