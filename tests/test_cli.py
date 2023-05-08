from propli.cli import get_dynamic_target
from propli.file import File
from propli.file_types import FileType

from pathlib import Path
import pytest


class TestGetDynamicTarget:
    """Tests for the dynamic target function."""

    @pytest.mark.parametrize(
        "source_path, target_format, target_ext, expected_path, expected_suffix, expected_type",
        [
            (
                "path/to/file.plist",
                None,
                None,
                "path/to/file.yaml",
                ".yaml",
                FileType.yaml,
            ),
            (
                "path/to/file.recipe",
                None,
                None,
                "path/to/file.recipe.yaml",
                ".yaml",
                FileType.plist,
            ),
            (
                "path/to/file.yaml",
                None,
                None,
                "path/to/file.plist",
                ".plist",
                FileType.plist,
            ),
            (
                "path/to/file.recipe.yaml",
                None,
                None,
                "path/to/file.recipe",
                ".recipe",
                FileType.plist,
            ),
        ],
    )
    def test_yaml_with_defaults(self, source_path, explicit_type, expected_type):
        """Test get_dynamic_target with yaml and no target_format or target_ext."""
        target = get_dynamic_target(File(Path(source_path)))
        assert target.path == Path("path/to/file.plist")
        assert target.suffix == ".plist"
        assert target.type == FileType.plist
