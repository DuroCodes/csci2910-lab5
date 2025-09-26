from dataclasses import dataclass


@dataclass
class Pokemon:
    name: str
    types: list[str]
    abilities: list[str]
    stats: dict[str, int]


@dataclass
class PokemonSet:
    name: str
    moves: list[str]
    ability: str
    item: str
    nature: str
    evs: dict[str, int]


@dataclass
class TeamMember:
    pokemon: Pokemon
    set: PokemonSet
