from pathlib import Path
from typing import Optional

import typer

from .console import console, err_console
from .file import File
from .file_types import FileTypeChoice, FileType

app = typer.Typer()


def get_dynamic_target(
    source_file: File,
    target_format: FileType | None = None,
    target_ext: str | None = None,
) -> File:
    if target_ext and not target_format:
        try:
            target_format = FileType.from_extension(target_ext)
        except ValueError:
            pass
    else:
        target_format = (
            FileType.plist if source_file.type == FileType.yaml else FileType.yaml
        )
        target_ext = target_format.value.extensions[0]

    return File(
        source_file.path.with_suffix(target_ext),
        explicit_type=target_format,
    )


def convert_choice_to_type(choice: Optional[FileTypeChoice]) -> Optional[FileType]:
    if choice is None:
        return None
    try:
        return FileType[choice.value]
    except KeyError:
        raise typer.BadParameter(f"Invalid file type: {choice}")


@app.command(name="print")
def print_command(
    source: Path = typer.Argument(
        ...,
        readable=True,
        resolve_path=True,
        show_default=False,
        dir_okay=False,
        allow_dash=True,
        help="The path to the file to read.",
    ),
    source_format: Optional[FileTypeChoice] = typer.Option(
        None,
        "--source-format",
        "-s",
        show_default=False,
        help="Optionally specify the format of the source file. If not specified, "
        "automatic detection is used.",
    ),
    print_format: Optional[FileTypeChoice] = typer.Option(
        None,
        "--print-format",
        "-f",
        show_default=False,
        help="Optionally specify the format of the target file. If not specified, "
        "the target will be based on the default target for the source file type. "
        "In most cases, this will be yaml.",
    ),
    pager: bool = typer.Option(
        False,
        "--pager",
        "-p",
    ),
    pager_style: bool = typer.Option(
        False,
        "--pager-style",
        "-P",
    ),
):
    """Print the file in the specified format."""
    if pager:
        with console.pager(styles=pager_style):
            convert_command(
                source,
                target=Path("-"),
                source_format=source_format,
                target_format=print_format,
            )
    else:
        convert_command(
            source,
            target=Path("-"),
            source_format=source_format,
            target_format=print_format,
        )


@app.command(name="convert")
def convert_command(
    source: Path = typer.Argument(
        ...,
        readable=True,
        resolve_path=True,
        show_default=False,
        dir_okay=False,
        allow_dash=True,
        help="The path to the file to convert.",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        writable=True,
        resolve_path=True,
        show_default=False,
        dir_okay=False,
        allow_dash=True,
        help="The path where the converted file will be written.",
    ),
    source_format: Optional[FileTypeChoice] = typer.Option(
        None,
        "--source-format",
        "-s",
        show_default=False,
        help="Optionally specify the format of the source file. If not specified, "
        "automatic detection is used.",
    ),
    target_format: Optional[FileTypeChoice] = typer.Option(
        None,
        "--target-format",
        "-f",
        show_default=False,
        help="Optionally specify the format of the target file. If not specified, "
        "the target will be based on the default target for the source file type. "
        "In most cases, this will be yaml.",
    ),
    target_ext: Optional[str] = typer.Option(
        None,
        "--target-ext",
        "-x",
        metavar="EXTENSION",
        show_default=False,
        help="Specify a file extension for the converted file. If not given, "
        "the default for the target format will be used. This option can be "
        "used to create files with non-standard file extensions for a file "
        "format. Additionally, if the target format is not specified, this "
        "option will determine the target format by extension. If a TARGET is "
        "specified, this option is ignored.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        show_default=False,
        help="Force overwrite of the target file if it already exists.",
    ),
):
    """Read file at SOURCE, convert, and output to TARGET"""

    # Gather source file information
    source_file = File(
        source,
        explicit_type=convert_choice_to_type(source_format),
    )
    if not source_file.exists:
        err_console.print(f'[red]ERROR: The file "{source}" does not exist.')

    # Gather target file information. If target is not specified, use the default
    # based on the source file type.
    if target is not None:
        target_file = File(
            target,
            explicit_type=convert_choice_to_type(target_format),
        )
    else:
        target_file = get_dynamic_target(
            source_file, convert_choice_to_type(target_format), target_ext
        )

    # Verify that the target file does not exist to prevent accidental overwrites
    # Force, skips this check
    if not force and target_file.exists:
        err_console.print(
            f'[yellow]WARNING: The target file "{target_file.path}" already exists. '
            "If you would like to overwrite it, use the --force flag."
        )
        typer.Exit(1)

    data = source_file.read()

    # TODO: Add support for binary plist
    # if target.type == FileType.plist
    #     if binary_plist:
    #         plist_format = plistlib.FMT_BINARY
    #     else:
    #         plist_format = plistlib.FMT_XML

    target_file.write(data)

    # err_console.print(f"[green]Converted {source_file} to {target_file}")


if __name__ == "__main__":
    app()
