#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def collect_paths(root: Path) -> str:
    paths = sorted(str(p.resolve()) for p in root.rglob("*"))
    return json.dumps(paths, indent=2)


def copy_to_clipboard(text: str) -> None:
    if shutil.which("wl-copy"):
        subprocess.run(["wl-copy"], input=text, text=True, check=True)
        return

    if shutil.which("xclip"):
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text,
            text=True,
            check=True,
        )
        return

    if shutil.which("xsel"):
        subprocess.run(
            ["xsel", "--clipboard", "--input"],
            input=text,
            text=True,
            check=True,
        )
        return

    raise SystemExit(
        "No clipboard utility found. Install wl-clipboard, xclip, or xsel."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()

    root = Path(args.folder)

    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    output = collect_paths(root)
    copy_to_clipboard(output)
    print(output)


if __name__ == "__main__":
    main()