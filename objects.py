from dataclasses import dataclass


@dataclass
class Beer:
    name: str
    alc_prod: str
    count: str
    reference: str
    new_references: list
