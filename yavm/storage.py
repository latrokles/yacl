from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Attribute:
    entity_id: str
    attribute: str
    value: ...


@dataclass
class Entity:
    entity_id: str
    entity_type: str
    attributes: list[Attribute]


@dataclass 
class TripleStore:
    attributes: list[Attribute]
