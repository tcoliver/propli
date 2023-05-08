import plistlib

from attrs import define

from .abc import FileTypeAbstractBase


@define(frozen=True)
class Plist(FileTypeAbstractBase):
    """The plist file type."""

    @property
    def name(self):
        return "plist"

    @property
    def extensions(self):
        return (
            ".plist",
            ".recipe",
            ".mobileconfig",
        )

    def load(self, file):
        return plistlib.load(file)

    def loads(self, data):
        return plistlib.loads(data)

    def dump(self, data, file):
        plistlib.dump(data, file)

    def dumps(self, data):
        return plistlib.dumps(data)


__all__ = ["Plist"]
