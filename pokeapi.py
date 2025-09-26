from collections import defaultdict
from functools import lru_cache
from models import Pokemon
from utils import normalize_pokemon_name
import requests


BASE_URL = "https://pokeapi.co/api/v2/"


@lru_cache(maxsize=128)
def get_pokemon(name: str) -> Pokemon | None:
    try:
        api_name = normalize_pokemon_name(name)
        url = f"{BASE_URL}/pokemon/{api_name}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pokemon = Pokemon(
            name=data["name"],
            types=[t["type"]["name"] for t in data["types"]],
            abilities=[a["ability"]["name"] for a in data["abilities"]],
            stats={s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
        )

        return pokemon
    except Exception:
        # silent fail to not crash, probably due to a name not caught by the normalize_pokemon_name function
        return None


def get_type_weaknesses(pokemon: Pokemon) -> dict[str, float]:
    try:
        url = f"{BASE_URL}/type/{pokemon.types[0]}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return {}

    weaknesses = defaultdict(float)

    for weak_type in data["damage_relations"]["double_damage_from"]:
        weaknesses[weak_type["name"]] = 2.0

    for resist_type in data["damage_relations"]["half_damage_from"]:
        weaknesses[resist_type["name"]] = 0.5

    for immune_type in data["damage_relations"]["no_damage_from"]:
        weaknesses[immune_type["name"]] = 0.0

    return weaknesses


def get_pokemon_names_by_type(type_name: str) -> list[str]:
    try:
        url = f"{BASE_URL}/type/{type_name}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return [p["pokemon"]["name"] for p in data["pokemon"]]
    except Exception:
        return []
