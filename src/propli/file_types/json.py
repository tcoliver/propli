import json

from attrs import define

from .abc import FileTypeAbstractBase


@define(frozen=True)
class Json(FileTypeAbstractBase):
    """The json file type."""

    _name = "json"
    _extensions = ".json"

    @property
    def name(self):
        return "json"

    @property
    def extensions(self):
        return (".json",)

    def load(self, file) -> dict:
        return json.load(file)

    def loads(self, data) -> dict:
        return json.loads(data)

    def dump(self, data, file) -> None:
        json.dump(data, file, sort_keys=True, indent=2)

    def dumps(self, data) -> str:
        return json.dumps(data, sort_keys=True, indent=2)


__all__ = ["Json"]
