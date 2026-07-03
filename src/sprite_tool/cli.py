from PIL import Image
import os
import argparse
from typing import List, Dict


def get_frames(input_folder: str, anim: str) -> List[Image.Image]:
    frames: List[Image.Image] = []
    index: int = 0

    while True:
        path: str = os.path.join(input_folder, f"{anim}_{index}.png")
        if not os.path.exists(path):
            break

        frames.append(Image.open(path).convert("RGBA"))
        index += 1

    if not frames:
        raise FileNotFoundError(f"No frames found for animation: {anim}")

    return frames


def build_sprite_sheet(
    input_folder: str,
    output_file: str,
    frame_size: int,
    rows_order: List[str],
    pad_to_max: bool = True,
) -> None:

    animations: Dict[str, List[Image.Image]] = {
        anim: get_frames(input_folder, anim) for anim in rows_order
    }

    max_frames: int = max(len(frames) for frames in animations.values())

    sheet_width: int = frame_size * max_frames
    sheet_height: int = frame_size * len(rows_order)

    sheet: Image.Image = Image.new(
        "RGBA",
        (sheet_width, sheet_height),
        (0, 0, 0, 0),
    )

    for row_index, anim in enumerate(rows_order):
        frames = animations[anim]

        for col_index, frame in enumerate(frames):
            x: int = col_index * frame_size
            y: int = row_index * frame_size
            sheet.paste(frame, (x, y))

    sheet.save(output_file)
    print(f"Sprite sheet saved: {output_file}")


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Build sprite sheet from variable-length animations"
    )

    parser.add_argument("-i", "--input", default="frames")
    parser.add_argument("-o", "--output", default="sprite_sheet.png")
    parser.add_argument("-s", "--size", type=int, default=256)

    parser.add_argument(
        "--rows",
        nargs="+",
        default=["idle", "walk_down", "walk_left", "walk_right", "walk_up"],
    )

    parser.add_argument(
        "--no-pad",
        action="store_true",
        help="Do not pad rows to max animation length",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    build_sprite_sheet(
        input_folder=args.input,
        output_file=args.output,
        frame_size=args.size,
        rows_order=args.rows,
        pad_to_max=not args.no_pad,
    )


if __name__ == "__main__":
    main()