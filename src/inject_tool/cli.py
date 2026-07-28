#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
import sys


LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".ps1": "powershell",
    ".md": "markdown",
    ".txt": "text",
}


def fence_lang(path: str) -> str:
    return LANG_MAP.get(Path(path).suffix.lower(), "text")


@dataclass(frozen=True)
class Marker:
    path: str
    start: int
    next_pos: int


def read_include(path_str: str) -> str:
    return Path(path_str.strip()).read_text(encoding="utf-8").rstrip()


def parse_marker(text: str, pos: int) -> Marker | None:
    start = text.find("[[", pos)
    if start == -1:
        return None

    end = text.find("]]", start + 2)
    if end == -1:
        raise ValueError(f"Unclosed include starting at {start}")

    path = text[start + 2 : end].strip()
    next_pos = end + 2

    return Marker(path=path, start=start, next_pos=next_pos)


def assemble(text: str) -> str:
    result = ""
    pos = 0

    while True:
        marker = parse_marker(text, pos)

        if marker is None:
            result += text[pos:]
            break

        result += text[pos:marker.start]
        
        lang = fence_lang(marker.path)
        content = read_include(marker.path)
        result += f"```{lang}\n{content}\n```"

        pos = marker.next_pos

    return result


def output_path_for(source_path: Path) -> Path:
    name = source_path.name[1:] if source_path.name.startswith("_") else source_path.name
    return source_path.with_name(name)


def build(source_path: Path) -> Path:
    text = source_path.read_text(encoding="utf-8")
    output = assemble(text)

    out_path = output_path_for(source_path)
    out_path.write_text(output, encoding="utf-8")

    return out_path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input.md>", file=sys.stderr)
        return 1

    out = build(Path(sys.argv[1]))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())