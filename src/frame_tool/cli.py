import argparse
import os
from typing import Tuple, Dict
from PIL import Image, ImageDraw, ImageFont


Color = Tuple[int, int, int, int]


COLOR_MAP: Dict[str, Color] = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "yellow": (255, 255, 0, 255),
    "orange": (255, 165, 0, 255),
    "purple": (128, 0, 128, 255),
    "pink": (255, 192, 203, 255),
    "gray": (128, 128, 128, 255),
}


def load_font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()


def parse_color(value: str) -> Color:
    v = value.strip().lower()

    if v in COLOR_MAP:
        return COLOR_MAP[v]

    if v.startswith("#"):
        v = v.lstrip("#")
        return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), 255)

    parts = v.split(",")
    if len(parts) == 3:
        return (int(parts[0]), int(parts[1]), int(parts[2]), 255)

    raise ValueError(f"Invalid color: {value}")


def create_image(number: int, out_dir: str, base_name: str, color: Color):
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = load_font(140)
    text = str(number)

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (256 - w) // 2 - bbox[0]
    y = (256 - h) // 2 - bbox[1]

    draw.text((x, y), text, font=font, fill=color)

    path = os.path.join(out_dir, f"{base_name}_{number}.png")
    img.save(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("count", type=int)
    parser.add_argument("out_dir", type=str)
    parser.add_argument("base_name", type=str)
    parser.add_argument("color", type=str)

    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    color = parse_color(args.color)

    for i in range(args.count):
        create_image(i, args.out_dir, args.base_name, color)


if __name__ == "__main__":
    main()