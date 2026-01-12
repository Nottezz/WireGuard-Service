import enum
from typing import Any, Iterable

from click import option


class Quotes(enum.Enum):
    NONE = 0
    SINGLE = 1
    DOUBLE = 2


class WGPrefix(enum.StrEnum):
    EMPTY = ""
    SUDO = "sudo"


class WGExecutable(enum.StrEnum):
    WG = "wg"


class WGArg:
    def __init__(self, value, quotes: Quotes = Quotes.DOUBLE) -> None:
        self.value = value
        self.quotes = quotes

    def __str__(self) -> str:
        if self.quotes == Quotes.NONE:
            return str(self.value)
        if self.quotes == Quotes.SINGLE:
            return f"'{self.value}'"
        if self.quotes == Quotes.DOUBLE:
            return f'"{self.value}"'

        raise ValueError(f"Unknown quotes type: {self.quotes}")


class WGOption:
    def __init__(self, key: str, value: Any = "") -> None:
        self.key = key
        self.value = value

    def __str__(self) -> str:
        return f"{self.key} {self.value}"


class WGOptionList(list[WGOption]):
    def __init__(self, iterable: Iterable[WGOption | str]) -> None:
        super().__init__(
            option if isinstance(option, WGOption) else WGOption(option)
            for option in iterable
        )


class WGArgsList(list[WGArg]):

    def __init__(self, iterable: Iterable[WGArg | str]):
        super().__init__(
            arg if isinstance(arg, WGArg) else WGArg(arg) for arg in iterable
        )

    def __str__(self) -> str:
        return " ".join(map(str, self))
