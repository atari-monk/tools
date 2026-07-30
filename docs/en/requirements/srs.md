## Software Requirements Specification

### Goal

- SRS Documentation tool
- Software Requirements Specification
- Structure and partial automation for requirements docs

### Environment

- Python
- CLI
- Ubuntu
- Single file

### Paths

- project_root = `/home/atari-monk/atari-monk/project/`

### Rules

- Define commands logic in functions and `hook it up` to cli commands boilerplate
- Use best method to avoid typing problems with code and data
- Strict type file schemas so that pylance dosent give errors

### Add Command

- Command `srs add -p project -f feature -n name -l line`
- Create file `feature.json` in folder `project_root + project/.docs/requirements` if not aleready exists
- Add new json object with name and items array with line, or append line if already exists
- Invoke doc command on these args

### Doc Command

- Command `srs doc -p project -f feature`
- Create file `feature.md` in folder `project_root + project/docs/en/requirements` by converting `feature.json` file to given scheme
