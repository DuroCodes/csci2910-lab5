import enum
from models import PokemonSet

@enum.unique
class Role(enum.Enum):
    HAZARD_SETTER = "hazard_setter"
    HAZARD_REMOVER = "hazard_remover"
    SPEED_CONTROL = "speed_control"
    PIVOT = "pivot"
    UTILITY = "utility"
    SETUP_SWEEPER = "setup_sweeper"


def identify_roles(pokemon_set: PokemonSet) -> list[str]:
    roles = []
    moves = [move.lower() for move in pokemon_set.moves]

    if any(move in ["stealth rock", "spikes", "toxic spikes", "sticky web"] for move in moves):
        roles.append(Role.HAZARD_SETTER)

    if any(move in ["defog", "rapid spin"] for move in moves):
        roles.append(Role.HAZARD_REMOVER)

    item_str = pokemon_set.item if isinstance(pokemon_set.item, str) else str(pokemon_set.item)
    if "choice scarf" in item_str.lower():
        roles.append(Role.SPEED_CONTROL)

    if any(move in ["u-turn", "volt switch", "flip turn", "teleport"] for move in moves):
        roles.append(Role.PIVOT)

    if any(move in ["knock off", "toxic", "thunder wave", "taunt", "encore"] for move in moves):
        roles.append(Role.UTILITY)

    if any(move in ["swords dance", "nasty plot", "calm mind", "dragon dance"] for move in moves):
        roles.append(Role.SETUP_SWEEPER)

    return roles


