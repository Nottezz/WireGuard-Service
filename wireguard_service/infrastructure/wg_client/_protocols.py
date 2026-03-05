from typing import Protocol


class SSHClient(Protocol):
    def exec_command(self, command: str):
        """
        Execute command on client
        """
