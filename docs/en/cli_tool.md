## CLI `new_tool`

Goal is to automate adding new tool to project, with given template.

### Requirements

- Py, cli, ubuntu
- Args:
    - name
- Consts:
    - project root `/home/atari-monk/atari-monk/project/tools`
- Create folder name_tool in `[[root]]/src` if not already exists
- Create file `__init__.py` if not already exists
- Create file `cli.py` if not already exists
- Create file `[[root]]/docs/en/[[name]]_tool.md` if not already exists

### Index

- In file `[[root]]/docs/index.md`

````md
## Content

### Config

- [Virtual Environment](en/virtual-environment.md)
- [Python Config](en/py-config.md)
- [Installing Script](en/installing-script.md)

### Scripts

- [Log](en/log.md)

### Python

- [Raw json](en/raw-json.md)

---

- [Dev Notes](https://atari-monk.github.io/dev-notes/)

---
````

Append `- [[[name]]](en/[[name]]_tool.md)` to scripts section

### Pyproject

- In file `[[root]]/pyproject.toml`

```toml
[project]
name = "tools"
version = "0.1.0"
dependencies = [
    "Pillow"
]

[tool.setuptools.packages.find]
where = ["src"]

[project.scripts]
prompt = "prompt_tool.cli:main"
alarm = "alarm_tool.cli:main"
sprite = "sprite_tool.cli:main"
resize = "resize_tool.cli:main"
frame = "frame_tool.cli:main"
rename = "rename_tool.cli:main"
inject = "inject_tool.cli:main"
extract = "extract_tool.cli:main"
list = "list_tool.cli:main"
paths = "paths_tool.cli:main"

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
ignore = []
```

Add `name = "name_tool.cli:main"` to [project.scripts]

### List Tool

For file `[[root]]/src/list_tool/tools.json` (part shown)

```json
[
    {
        "name": "alarm",
        "description": "pomodoro or any time based alarm"
    },
    {
        "name": "extract",
        "description": "extracts message and lines nr form pylance problems info"
    },
]
```

Append secion for new tool

### Reload lib

This is what i do in terminal to add new tool
Automate it

```sh
cd [[root]]
deactivate
pipx uninstall tools
pipx install -e .
```