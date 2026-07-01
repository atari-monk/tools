import argparse
import json
import subprocess
from pathlib import Path
from typing import TypeAlias

PromptFileMap: TypeAlias = dict[str, list[Path]]
PromptFileMapRaw: TypeAlias = dict[str, list[str]]
PromptMapRaw: TypeAlias = dict[str, PromptFileMapRaw]
FilesContext: TypeAlias = dict[str, list[str]]


PROMPTS: dict[str, str] = {
    "question": "Answer my question",
    "implementation": "Implement requirements (code generation)",
}

PROJECTS: dict[str, str] = {
    "tools": "Tools project",
    "simple-sprite": "Sprite generator",
    "box-game": "Mini game about sorting boxes",
    "bowling-game": "Mini game about bowling",
}

PROMPTS_ROOT = Path("/home/atari-monk/atari-monk/project/prompts/prompts")
PROJECTS_ROOT = Path("/home/atari-monk/atari-monk/project")

CODE_SUFFIXES: set[str] = {
    "py",
    "ts",
    "js",
    "jsx",
    "tsx",
    "java",
    "go",
    "rs",
    "cpp",
    "c",
    "h",
    "hpp",
    "cs",
    "kt",
    "swift",
    "php",
    "rb",
    "sh",
}


def load_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def convert_prompt_group(group: PromptFileMapRaw) -> PromptFileMap:
    return {key: [Path(value) for value in values] for key, values in group.items()}


def load_paths(path: Path, prompt_key: str) -> PromptFileMap:
    raw: PromptMapRaw = json.loads(path.read_text(encoding="utf-8"))

    if prompt_key not in raw:
        raise ValueError(f"Prompt '{prompt_key}' not found in prompt map")

    return convert_prompt_group(raw[prompt_key])


def is_code_file(path: Path) -> bool:
    return path.suffix.lstrip(".") in CODE_SUFFIXES


def load_file(path: Path, show_path: bool) -> str:
    content = path.read_text(encoding="utf-8")

    if not is_code_file(path):
        return content

    language = path.suffix.lstrip(".")
    parts: list[str] = []

    if show_path:
        parts.append(str(path.resolve()))

    parts.append(f"```{language}\n{content}\n```")

    return "\n".join(parts)


def load_context(paths: PromptFileMap, show_path: bool) -> FilesContext:
    return {
        key: [load_file(path, show_path) for path in values]
        for key, values in paths.items()
    }


def inject(template: str, ctx: FilesContext) -> str:
    result = template

    for key, values in ctx.items():
        result = result.replace(f"[[{key}]]", "\n\n-----\n\n".join(values))

    return result


def copy_to_clipboard(text: str) -> None:
    subprocess.run(
        ["xclip", "-selection", "clipboard"],
        input=text,
        text=True,
        check=True,
    )


def build_prompt(prompt_name: str, project_name: str, show_code_path: bool) -> str:
    template_path = PROMPTS_ROOT / f"{prompt_name}.md"

    map_path = PROJECTS_ROOT / project_name / ".config" / "prompt-map.json"

    template = load_markdown(template_path)
    paths = load_paths(map_path, prompt_name)
    context = load_context(paths, show_code_path)

    return inject(template, context)


def list_items() -> None:
    print("Available prompts:\n")

    for key, value in PROMPTS.items():
        print(f"  {key:<30} {value}")

    print("\nAvailable projects:\n")

    for key, value in PROJECTS.items():
        print(f"  {key:<30} {value}")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt", description="Prompt builder tool")

    parser.add_argument("command", nargs="?", help="Prompt name or 'list'")
    parser.add_argument("project", nargs="?", help="Project name")

    parser.add_argument(
        "-cp",
        "--code-path",
        action="store_true",
        help="Print absolute path before code blocks",
    )

    parser.add_argument(
        "-p",
        "--print",
        dest="print_result",
        action="store_true",
        help="Print result to console",
    )

    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "list":
        list_items()
        return 0

    if args.command is None or args.project is None:
        parser.print_help()
        return 1

    prompt_name: str = args.command
    project_name: str = args.project

    if prompt_name not in PROMPTS:
        parser.print_help()
        return 1

    if project_name not in PROJECTS:
        parser.print_help()
        return 1

    result = build_prompt(prompt_name, project_name, args.code_path)

    if args.print_result:
        print(result)

    copy_to_clipboard(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
