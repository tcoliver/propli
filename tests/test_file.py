from pathlib import Path

import pytest

from propli.file import File
from propli.file_types import FileType


class TestFile:
    """Test the File class"""

    @pytest.mark.parametrize(
        "path, expected_type",
        [
            ("path/to/file.plist", FileType.plist),
            ("path/to/file.recipe", FileType.plist),
            ("path/to/file.yaml", FileType.yaml),
            ("path/to/file.recipe.yaml", FileType.yaml),
        ],
    )
    def test_init_working_case(self, path: str, expected_type: FileType):
        """Test the working case of File.__init__"""
        file = File(Path(path))
        assert file.path == Path(path)
        assert file.type == expected_type

    @pytest.mark.parametrize("path", ["path/to/file.txt", "path/to/file", "file.xml"])
    def test_init_failed_case(self, path):
        """Test the failed case of File.__init__"""
        with pytest.raises(ValueError):
            File(Path(path))
