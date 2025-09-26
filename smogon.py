import requests
from functools import lru_cache

from models import PokemonSet
from utils import get_first_item


BASE_URL = "https://pkmn.github.io/smogon/data/sets"


@lru_cache(maxsize=8)
def get_gen_sets(gen=8) -> dict[str, dict[str, dict]]:
    try:
        url = f"{BASE_URL}/gen{gen}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


@lru_cache(maxsize=256)
def get_pokemon_sets(pokemon_name: str, gen=8) -> list[PokemonSet]:
    sets_data = get_gen_sets(gen)
    pokemon_sets = []

    if pokemon_name in sets_data:
        for _, tier_data in sets_data[pokemon_name].items():
            for set_name, set_data in tier_data.items():
                # some moves are arrays, so we need to flatten them
                moves = [get_first_item(move) for move in set_data.get("moves", [])]
                item = get_first_item(set_data.get("item", ""))
                ability = get_first_item(set_data.get("ability", ""))
                nature = set_data.get("nature", "")

                pokemon_sets.append(
                    PokemonSet(
                        name=set_name,
                        moves=moves,
                        ability=ability,
                        item=item,
                        nature=nature,
                        evs=set_data.get("evs", {}),
                    )
                )

    return pokemon_sets


@lru_cache(maxsize=8)
def get_available_pokemon_names(gen=8) -> set[str]:
    return set(get_gen_sets(gen).keys())
