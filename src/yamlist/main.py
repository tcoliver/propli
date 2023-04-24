import typer
import plistlib
import yaml
from typing import Optional
from rich.console import Console

from pathlib import Path

app = typer.Typer()
console = Console()


@app.command()
def main(source: Path, target: Optional[Path] = typer.Argument(None), binary: bool = False):
    """Convert between plist and yaml files"""
    if target is None:
        if source.suffix == ".plist":
            target = source.with_suffix(".yaml")
        elif source.suffix == ".yaml":
            target = source.with_suffix(".plist")

    if source.suffix == target.suffix:
        raise ValueError("Source and target file types must be different")
    elif source.suffix not in [".plist", ".yaml"]:
        raise ValueError("Source file type must be .plist or .yaml")
    elif target.suffix not in [".plist", ".yaml"]:
        raise ValueError("Target file type must be .plist or .yaml")

    if source.suffix == ".plist":
        with open(source, "rb") as f:
            data = plistlib.load(f)
    elif source.suffix == ".yaml":
        with open(source, "r") as f:
            data = yaml.safe_load(f)

    if target.suffix == ".plist":
        if binary:
            plist_format = plistlib.FMT_BINARY
        else:
            plist_format = plistlib.FMT_XML
        with open(target, "wb") as f:
            plistlib.dump(data, f, fmt=plist_format)
    elif target.suffix == ".yaml":
        with open(target, "w") as f:
            yaml.dump(data, f)

    console.print(f"[green]Converted {source} to {target}")

if __name__ == "__main__":
    app()
