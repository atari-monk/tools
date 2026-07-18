from __future__ import annotations

import argparse
from pathlib import Path


def rename_frames(folder: str, animation_name: str) -> None:
    folder_path = Path(folder)

    if not folder_path.is_dir():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    files: list[Path] = sorted(
        (
            path
            for path in folder_path.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".png"
            and path.stem.isdigit()
        ),
        key=lambda path: int(path.stem),
    )

    if not files:
        raise FileNotFoundError(
            f"No numbered PNG files found in '{folder}'."
        )

    temp_files: list[Path] = []

    # Rename to temporary names first to avoid collisions.
    for index, file in enumerate(files):
        temp_path = folder_path / f"__tmp__{index}.png"
        file.rename(temp_path)
        temp_files.append(temp_path)

    # Rename to final names.
    for index, temp_file in enumerate(temp_files):
        final_path = folder_path / f"{animation_name}_{index}.png"
        temp_file.rename(final_path)
        print(f"{temp_file.name} -> {final_path.name}")

    print(f"\nRenamed {len(files)} files.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rename numbered PNG frames to animation_<index>.png"
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Folder containing numbered PNG frames (e.g. 0001.png)",
    )

    parser.add_argument(
        "-a",
        "--animation",
        required=True,
        help="Animation name (e.g. idle, walk_down, attack)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rename_frames(args.input, args.animation)


if __name__ == "__main__":
    main()