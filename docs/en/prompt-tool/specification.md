## Data

Prompt template example:

```md
## Some text

Some text

## Some text

[[key]]

## Some text

[[other-key]]
```

Prompt map example:

```json
{
    "prompt-name": {
        "key": [
            "absolute file path",
            "absolute file path"
        ],
        "other-key": [
            "absolute file path"
        ]
    }
}
```

## Functionality

Script runs as command `prompt prompt-name project-name`.  
Loads prompt template and prompt map.  
For each key placeholder list of separated file content is injected.  
Result is printed and put in clipboard.  