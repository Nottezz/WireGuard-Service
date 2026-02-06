import logging
from itertools import chain
from typing import Any

from wireguard_service.wg_client._parameters import (
    WGArgsList,
    WGExecutable,
    WGOption,
    WGOptionList,
    WGPrefix,
)
from wireguard_service.wg_client._protocols import SSHClient

logger = logging.getLogger(__name__)

_NOT_SET: Any = object()

class WGError(Exception):
    """"""


class _WGCommandBase:

    prefix: WGPrefix | str = WGPrefix.SUDO
    executable: WGExecutable | str = "wg"
    options: WGOptionList | list[WGOption | str]
    arguments: WGArgsList = None
    stdin: str | None = None

    def __init__(
        self,
        *,
        prefix: WGPrefix = None,
        executable: WGExecutable = None,
        options: list[str] | None = None,
        arguments: list[str] | None = None,
        stdin: str | None = None,
    ) -> None:
        self.prefix = WGPrefix(prefix or self.prefix)
        self.executable = WGExecutable(executable or self.executable)
        self.stdin = stdin
        self.options = WGOptionList(
            self._normalize(chain(getattr(self, "options", []) or [], options or []))
        )

        self.arguments = WGArgsList(
            self._normalize(chain(self.arguments or [], arguments or []))
        )

    def execute(self, ssh_client: SSHClient) -> tuple[str, str]:
        command = self._get_command()
        logger.info("Executing command: %s", command)

        stdin_stream, stdout, stderr = ssh_client.exec_command(command)

        if self.stdin:
            stdin_stream.write(self.stdin)
            stdin_stream.flush()
            stdin_stream.channel.shutdown_write()

        stdout, stderr = stdout.read().decode(), stderr.read().decode()

        logger.debug("stdout: %s", stdout)
        logger.debug("stderr: %s", stderr)

        stdout, stderr = self._check_errors(stdout, stderr)

        logger.info("Done executing command: %s", command)
        return stdout, stderr

    def _get_command(self) -> str:
        parts = [
            self.prefix,
            self.executable,
            *self.options,
            *self.arguments,
        ]
        return " ".join(map(str, parts))

    def _normalize(self, values):
        return [str(v) for v in values if v is not None and v is not _NOT_SET]

    def _check_errors(self, stdout: str, stderr: str) -> tuple[str, str]:
        if stderr and not stderr.startswith("[#]"):
            raise WGError('Error received. Output: \n%s, \n%s', stdout, stderr)

        return stdout, stderr



class WGCommand(_WGCommandBase):
    """
    Command class
    """
