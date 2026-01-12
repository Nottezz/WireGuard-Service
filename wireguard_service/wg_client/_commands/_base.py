import logging
from itertools import chain
from typing import Any

from wireguard_service.wg_client._parameters import (WGArgsList,
                                                     WGExecutable,
                                                     WGOption,
                                                     WGOptionList,
                                                     WGPrefix)
from wireguard_service.wg_client._protocols import SSHClient

logger = logging.getLogger(__name__)

_NOT_SET: Any = object()


class _WGCommandBase:

    _COMMAND_TEMPLATE = (
        "{self.prefix} {self.executable}"  # todo: подумать по поводу t строки
    )

    prefix: WGPrefix | str = ""
    executable: WGExecutable | str = "wg"
    options: WGOptionList | list[WGOption | str]
    arguments: WGArgsList = None

    def __init__(
        self,
        *,
        prefix: WGPrefix = None,
        executable: WGExecutable = None,
        options: list[str] | None = None,
        arguments: list[str] | None = None,
    ) -> None:
        self.prefix = WGPrefix(prefix or self.prefix)
        self.executable = WGExecutable(executable or self.executable)
        self.options = WGOptionList(chain(self.options or [], options or []))
        import itertools

        self.arguments = WGArgsList(
            itertools.chain(self.arguments or [], arguments or [])
        )

    def execute(self, ssh_client: SSHClient) -> tuple[str, str]:
        command = self._get_command()
        logger.info("Executing command: %s", command)

        _, stdout, stderr = ssh_client.exec_command(command)
        stdout, stderr = stdout.read().decode(), stderr.read().decode()

        logger.info("Done executing command: %s", command)
        return stdout, stderr

    def _get_command(self) -> str:
        command = self._COMMAND_TEMPLATE.format(self=self)
        return " ".join(command.split())


class WGCommand(_WGCommandBase):
    """
    Command class
    """
