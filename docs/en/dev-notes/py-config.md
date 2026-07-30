## Python Config

### File: `/home/atari-monk/atari-monk/project/tools/pyrightconfig.json`

```json
{
  "typeCheckingMode": "strict",
  "reportMissingImports": true,
  "reportMissingTypeStubs": true,
  "reportUnknownParameterType": true,
  "reportUnknownVariableType": true,
  "reportUntypedFunctionDecorator": true,
  "reportUntypedClassDecorator": true,
  "reportUntypedBaseClass": true,
  "reportUnknownMemberType": true,
  "reportUnknownArgumentType": true,
  "reportGeneralTypeIssues": true,
  "reportOptionalMemberAccess": true,
  "reportOptionalSubscript": true,
  "reportOptionalCall": true
}
```

---

### File: `/home/atari-monk/atari-monk/project/tools/pyproject.toml`

```toml
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

---

### Install formatting tool (Ruff)

```bash
pip install ruff
```

### (Optional but recommended) Install Black

```bash
pip install black
```

### VSCode setup (Python type checking)

Install extension:

* Python (Microsoft)
* Pylance

Then ensure Pyright strict mode is active via the `pyrightconfig.json` above.

### Format code usage

Ruff:

```bash
ruff check .
ruff format .
```

Black:

```bash
black .
```

### Tasks

- [x] Create pyrightconfig.json
- [x] Create pyproject.toml
- [x] Install ruff
- [x] Install black
- [x] Install Python (Microsoft) extension
- [x] Install Pylance (Microsoft) extension