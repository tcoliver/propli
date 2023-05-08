import sys
from pathlib import Path

from .console import console
from .file_types import FileTypeChoice, FileType


class File:
    def __init__(
        self,
        path: Path | str,
        explicit_type: FileType | FileTypeChoice | str | None = None,
    ):
        self.path: Path = Path(path)
        self.type: FileType = self._infer_type(explicit_type=explicit_type)

    @property
    def exists(self) -> bool:
        return self.path.exists()

    @property
    def suffix(self) -> str:
        return self.path.suffix

    def _infer_type(
        self,
        explicit_type: FileType | FileTypeChoice | str | None = None,
    ) -> FileType:
        """Infer the file type from the path suffix or explicit type."""
        try:
            if explicit_type is not None:
                if isinstance(explicit_type, FileType):
                    return explicit_type
                elif isinstance(explicit_type, FileTypeChoice):
                    return FileType.from_choice(explicit_type)
                elif isinstance(explicit_type, str):
                    return FileType[explicit_type.lower()]
                raise ValueError(f"File type unknown: {explicit_type}")
            else:
                if self.path == Path("-"):
                    return FileType.yaml  # default to yaml for stdin and stdout
                suffix = self.path.suffix.lower()
                return FileType.from_extension(suffix)
        except KeyError:
            raise ValueError(f"File type unknown: {explicit_type}")

    def read(self) -> dict:
        if self.path == Path("-"):
            return self.type.value.loads(sys.stdin.buffer.read())
        else:
            with self.path.open("rb") as f:
                return self.type.value.load(f)

    def write(self, data: dict) -> None:
        if self.path == Path("-"):
            dumped_data = self.type.value.dumps(data)
            if type(dumped_data) is bytes:
                dumped_data = dumped_data.decode()
                console.print(dumped_data)
        else:
            with self.path.open("wb") as f:
                self.type.value.dump(data, f)
