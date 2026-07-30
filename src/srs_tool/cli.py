import argparse
import json
from pathlib import Path
from typing import TypedDict


PROJECT_ROOT = Path("/home/atari-monk/atari-monk/project")


class Requirement(TypedDict):
    name: str
    items: list[str]


class RequirementsDocument(TypedDict):
    requirements: list[Requirement]


def get_srs_json_path(project: str, feature: str) -> Path:
    return PROJECT_ROOT / project / ".docs" / "requirements" / f"{feature}.json"


def get_srs_md_path(project: str, feature: str) -> Path:
    return PROJECT_ROOT / project / "docs" / "en" / "requirements" / f"{feature}.md"


def load_srs_json(path: Path) -> RequirementsDocument:
    if not path.exists():
        return {"requirements": []}

    with path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    requirements: list[Requirement] = []

    for item in raw_data.get("requirements", []):
        requirements.append(
            {
                "name": str(item.get("name", "")),
                "items": [
                    str(value)
                    for value in item.get("items", [])
                ],
            }
        )

    return {"requirements": requirements}


def save_srs_json(path: Path, document: RequirementsDocument) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(document, file, indent=4)


def add_requirement(project: str, feature: str, name: str, line: str) -> None:
    json_path = get_srs_json_path(project, feature)
    document = load_srs_json(json_path)

    requirement = next(
        (
            item
            for item in document["requirements"]
            if item["name"] == name
        ),
        None,
    )

    if requirement is None:
        document["requirements"].append(
            {
                "name": name,
                "items": [line],
            }
        )
    elif line not in requirement["items"]:
        requirement["items"].append(line)

    save_srs_json(json_path, document)
    generate_doc(project, feature)


def generate_doc(project: str, feature: str) -> None:
    json_path = get_srs_json_path(project, feature)
    md_path = get_srs_md_path(project, feature)
    document = load_srs_json(json_path)

    lines: list[str] = [
        "## Software Requirements Specification",
        "",
    ]

    for requirement in document["requirements"]:
        lines.extend(
            [
                f"### {requirement['name']}",
                "",
            ]
        )

        lines.extend(
            f"- {item}"
            for item in requirement["items"]
        )

        lines.append("")

    md_path.parent.mkdir(parents=True, exist_ok=True)

    with md_path.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def handle_add_command(args: argparse.Namespace) -> None:
    add_requirement(
        str(args.project),
        str(args.feature),
        str(args.name),
        str(args.line),
    )


def handle_doc_command(args: argparse.Namespace) -> None:
    generate_doc(
        str(args.project),
        str(args.feature),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="srs")

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = commands.add_parser("add")
    add_parser.add_argument("-p", "--project", required=True)
    add_parser.add_argument("-f", "--feature", required=True)
    add_parser.add_argument("-n", "--name", required=True)
    add_parser.add_argument("-l", "--line", required=True)

    doc_parser = commands.add_parser("doc")
    doc_parser.add_argument("-p", "--project", required=True)
    doc_parser.add_argument("-f", "--feature", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        handle_add_command(args)

    elif args.command == "doc":
        handle_doc_command(args)


if __name__ == "__main__":
    main()