from enum import Enum

from .plist import Plist
from .yaml import Yaml


class FileTypeChoice(Enum):
    plist = "plist"
    yaml = "yaml"


class FileType(Enum):
    plist = Plist()
    yaml = Yaml()

    @staticmethod
    def from_extension(ext: str) -> "FileType":
        ext = ext.lower() if ext.startswith(".") else f".{ext}".lower()
        for file_type in FileType:
            if ext in file_type.value.extensions:
                return file_type
        raise ValueError(f"Unknown file extension: {ext}")

    @staticmethod
    def from_choice(choice: FileTypeChoice) -> "FileType":
        try:
            return FileType[choice.value]
        except KeyError:
            raise ValueError(f"Invalid file type: {choice}")
