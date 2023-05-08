import abc

from attrs import define


@define(frozen=True)
class FileTypeAbstractBase(abc.ABC):
    """The abstract base class for all file types."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def extensions(self) -> tuple[str]:
        ...

    @abc.abstractmethod
    def load(self, file) -> dict:
        ...

    @abc.abstractmethod
    def loads(self, data) -> dict:
        ...

    @abc.abstractmethod
    def dump(self, data, file) -> None:
        ...

    @abc.abstractmethod
    def dumps(self, data) -> str:
        ...
