## Raw json

One way of dealing with json in python is to use basic types to define json structure in memory.  
For example given json:

```json
{
    "prompt-name": {
        "key": [
            "value",
            "value"
        ],
        "other-key": [
            "value"
        ]
    }
}
```

One can use primitive types to define memory structure for json like this:

```py
MapRaw: TypeAlias = dict[str, list[str]]
MapsRaw: TypeAlias = dict[str, MapRaw]
```

and load data:

```py
def load_map(path: Path) -> MapsRaw:
    return json.loads(
        path.read_text(encoding="utf-8")
    )
```

This allows to type json strictly but in a generic way without dataclasses with hard coded properties.  
It is allways posible to parse data into some structure later.