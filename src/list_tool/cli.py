import argparse
import json
from pathlib import Path

from .models import Tool


def load_tools() -> list[Tool]:
    path = Path(__file__).with_name("tools.json")

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    tools: list[Tool] = []

    for item in data:
        tools.append(
            Tool(
                name=item["name"],
                description=item["description"],
            )
        )

    return tools


def print_tools(
    tools: list[Tool],
    *,
    show_description: bool = False,
) -> None:
    if not show_description:
        for tool in tools:
            print(tool.name)
        return

    width = max(
        len(tool.name)
        for tool in tools
    )

    for tool in tools:
        print(
            f"{tool.name:<{width}} - {tool.description}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--desc",
        action="store_true",
        help="Show tool descriptions",
    )
    args = parser.parse_args()

    tools = load_tools()

    print_tools(
        tools,
        show_description=args.desc,
    )


if __name__ == "__main__":
    main()