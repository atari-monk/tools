from pathlib import Path
import json
import subprocess
import sys

ROOT = Path("/home/atari-monk/atari-monk/project/tools")
SRC = ROOT / "src"
DOCS = ROOT / "docs"
INDEX = DOCS / "index.md"
PYPROJECT = ROOT / "pyproject.toml"
TOOLS_JSON = SRC / "list_tool" / "tools.json"


def ensure_package(name: str) -> None:
    package = SRC / f"{name}_tool"
    package.mkdir(parents=True, exist_ok=True)

    init_file = package / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")

    cli_file = package / "cli.py"
    if not cli_file.exists():
        cli_file.write_text(
            'def main() -> None:\n'
            '    print("Hello, world!")\n',
            encoding="utf-8",
        )


def ensure_doc(name: str) -> None:
    path = DOCS / "en" / f"{name}_tool.md"
    if not path.exists():
        path.write_text(f"## {name.capitalize()} CLI\n", encoding="utf-8")


def update_index(name: str) -> None:
    line = f"- [{name.capitalize()}](en/{name}_tool.md)"
    text = INDEX.read_text(encoding="utf-8")

    if line in text:
        return

    marker = "### Python"
    pos = text.find(marker)
    if pos == -1:
        raise RuntimeError("Python section not found")

    scripts_start = text.rfind("### Scripts", 0, pos)
    if scripts_start == -1:
        raise RuntimeError("Scripts section not found")

    insert_pos = pos
    updated = text[:insert_pos].rstrip() + "\n" + line + "\n\n" + text[insert_pos:]
    INDEX.write_text(updated, encoding="utf-8")


def update_pyproject(name: str) -> None:
    entry = f'{name} = "{name}_tool.cli:main"'
    text = PYPROJECT.read_text(encoding="utf-8")

    if entry in text:
        return

    marker = "[tool.black]"
    pos = text.find(marker)
    if pos == -1:
        raise RuntimeError("tool.black section not found")

    updated = text[:pos].rstrip() + "\n" + entry + "\n\n" + text[pos:]
    PYPROJECT.write_text(updated, encoding="utf-8")


def update_tools_json(name: str) -> None:
    items = json.loads(TOOLS_JSON.read_text(encoding="utf-8"))

    if any(item["name"] == name for item in items):
        return

    items.append(
        {
            "name": name,
            "description": "",
        }
    )

    TOOLS_JSON.write_text(json.dumps(items, indent=4) + "\n", encoding="utf-8")


def reload_package() -> None:
    subprocess.run(
        ["pipx", "uninstall", "tools"],
        cwd=ROOT,
        check=False,
    )
    subprocess.run(
        ["pipx", "install", "-e", "."],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: new_tool <name>")

    name = sys.argv[1]

    ensure_package(name)
    ensure_doc(name)
    update_index(name)
    update_pyproject(name)
    update_tools_json(name)
    reload_package()


if __name__ == "__main__":
    main()