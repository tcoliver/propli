from io import StringIO

from attrs import define
from ruamel.yaml import YAML

from .abc import FileTypeAbstractBase

# Global yaml config
_yaml = YAML(typ="safe", pure=True)
_yaml.default_flow_style = False


@define(frozen=True)
class Yaml(FileTypeAbstractBase):
    """The yaml file type."""

    @property
    def name(self):
        return "yaml"

    @property
    def extensions(self):
        return (
            ".yaml",
            ".yml",
        )

    def load(self, file) -> dict:
        return _yaml.load(file)

    def loads(self, data) -> dict:
        return _yaml.load(data)

    def dump(self, data, file) -> None:
        _yaml.dump(data, file)

    def dumps(self, data) -> str:
        stream = StringIO()
        _yaml.dump(data, stream)
        return stream.getvalue()


__all__ = ["Yaml"]
