## Install cli script globally

### Add to `pyproject.toml`

```toml
[project.scripts]
prompt = "prompt_tool.cli:main"
```

### pipx (global CLI tool)

Install:

```bash
sudo apt install pipx
pipx ensurepath
```

Deactivate venv, then:

```bash
pipx install -e .
```

Now:

```bash
prompt
```

works globally.