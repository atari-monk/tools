#!/usr/bin/env python3
from __future__ import annotations

import argparse
from PIL import Image


def resize_image(input_path: str, output_path: str, width: int, height: int) -> None:
    with Image.open(input_path) as img:
        img = img.convert("RGBA")

        resized = img.resize( # type: ignore
            (width, height),
            Image.Resampling.LANCZOS,
        )

        resized.save(output_path)

    print(f"Saved: {output_path} ({width}x{height})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI image resizer")

    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("width", type=int, help="Target width")
    parser.add_argument("height", type=int, help="Target height")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    resize_image(
        input_path=args.input,
        output_path=args.output,
        width=args.width,
        height=args.height,
    )


if __name__ == "__main__":
    main()