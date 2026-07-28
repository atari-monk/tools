# models.py

from dataclasses import dataclass


@dataclass(slots=True)
class Tool:
    name: str
    description: str