import argparse
import json
from pathlib import Path
from typing import Any


def extract_messages(data: list[dict[str, Any]]) -> str:
    messages: list[str] = []

    for item in data:
        message = item.get("message")
        start_line = item.get("startLineNumber")
        end_line = item.get("endLineNumber")

        if not isinstance(message, str):
            continue

        if not isinstance(start_line, int) or not isinstance(end_line, int):
            continue

        messages.append(
            "\n".join(
                [
                    f"Lines {start_line}-{end_line}",
                    message,
                ]
            )
        )

    return "\n\n".join(messages)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()

    path = Path(args.file_path)

    data: list[dict[str, Any]] = json.loads(path.read_text())

    extracted = extract_messages(data)

    path.write_text(extracted)


if __name__ == "__main__":
    main()