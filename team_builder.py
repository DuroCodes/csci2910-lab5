import enum
from models import Pokemon, PokemonSet, TeamMember
from pokeapi import get_pokemon, get_type_weaknesses
from smogon import get_pokemon_sets, get_available_pokemon_names
from utils import normalize_for_comparison


@enum.unique
class Role(enum.Enum):
    HAZARD_SETTER = "hazard_setter"
    HAZARD_REMOVER = "hazard_remover"
    SPEED_CONTROL = "speed_control"
    PIVOT = "pivot"
    UTILITY = "utility"
    SETUP_SWEEPER = "setup_sweeper"
    TYPE_COVERAGE = "type_coverage"


def identify_roles(pokemon_set: PokemonSet) -> list[Role]:
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


def score_pokemon(
    pokemon: Pokemon,
    pokemon_set: PokemonSet,
    team_needs: dict[Role, list[str]],
    current_team: list[TeamMember],
) -> float:
    score = 0.0
    roles = identify_roles(pokemon_set)

    role_scores = {
        Role.HAZARD_SETTER: 3.0,
        Role.HAZARD_REMOVER: 3.0,
        Role.SPEED_CONTROL: 2.0,
        Role.PIVOT: 2.0,
        Role.UTILITY: 1.5,
        Role.SETUP_SWEEPER: 2.0,
    }

    score += sum(role_scores[role] for role in roles if role in team_needs)
    current_types = [type for member in current_team for type in member.pokemon.types]
    score -= 0.5 * sum(1 for type in pokemon.types if type in current_types)

    return score


def get_type_coverage_needs(seed_pokemon: Pokemon) -> list[str]:
    needs = []
    weaknesses = get_type_weaknesses(seed_pokemon)

    # always want to include steel for resists (https://www.youtube.com/watch?v=tBlnHwwax44)
    needs.append("steel")
    major_weaknesses = [t for t, mult in weaknesses.items() if mult >= 2.0]

    coverage_map = {"steel": "fire", "poison": "steel", "ground": "flying"}
    needs.extend(
        coverage_map[weakness] for weakness in major_weaknesses if weakness in coverage_map
    )

    return list(set(needs))


def build_team(seed_name: str) -> list[TeamMember]:
    print(f"Fetching data for {seed_name}...")
    seed_pokemon = get_pokemon(seed_name)
    if not seed_pokemon:
        print(f"Could not find Pokémon: {seed_name}")
        return []

    seed_sets = get_pokemon_sets(seed_pokemon.name.title())
    if not seed_sets:
        print(f"No sets found for {seed_pokemon.name} in gen8")
        return []

    seed_set = seed_sets[0]
    team = [TeamMember(seed_pokemon, seed_set)]

    print(f"\nSelected Set: {seed_set.name} ({seed_pokemon.name})")
    print(f"├─ Moves: {', '.join(seed_set.moves[:3])}{'...' if len(seed_set.moves) > 3 else ''}")
    print(f"├─ Item: {seed_set.item}")
    print(f"╰─ Ability: {seed_set.ability}")

    team_needs = {
        Role.HAZARD_SETTER: [],
        Role.HAZARD_REMOVER: [],
        Role.SPEED_CONTROL: [],
        Role.PIVOT: [],
        Role.UTILITY: [],
        Role.SETUP_SWEEPER: [],
        Role.TYPE_COVERAGE: get_type_coverage_needs(seed_pokemon),
    }

    seed_roles = identify_roles(seed_set)
    for role in team_needs:
        if role not in seed_roles and role != Role.TYPE_COVERAGE:
            team_needs[role].append(1)

    print("\nTeam Needs:")
    print(f"├─ Roles needed: {', '.join([role.value for role in team_needs.keys()])}")
    print(f"╰─ Types needed: {', '.join(team_needs[Role.TYPE_COVERAGE])}")

    print("\nFetching available Pokémon...")
    available_pokemon = get_available_pokemon_names()
    print(f"╰─ Found {len(available_pokemon)} available Pokémon")

    print(f"\nBuilding team ({len(team) + 1}/6)")
    while len(team) < 6:
        best_candidate = None
        best_score = -1
        candidates_evaluated = 0

        candidates_to_evaluate = list(available_pokemon)[:100]
        for pokemon_name in candidates_to_evaluate:
            candidate_normalized = normalize_for_comparison(pokemon_name)
            if any(
                normalize_for_comparison(member.pokemon.name) == candidate_normalized
                for member in team
            ):
                continue

            pokemon = get_pokemon(pokemon_name)
            if not pokemon:
                continue

            sets = get_pokemon_sets(pokemon_name)
            if not sets:
                continue

            candidates_evaluated += 1

            for pokemon_set in sets:
                score = score_pokemon(pokemon, pokemon_set, team_needs, team)
                if score > best_score:
                    best_score = score
                    best_candidate = (pokemon, pokemon_set)

        if best_candidate:
            team.append(TeamMember(pokemon=best_candidate[0], set=best_candidate[1]))
            print(
                f"├─ Added {best_candidate[0].name.title()} ({best_candidate[1].name}) ({best_score:.2f})"
            )
            print(f"├─ Moves: {', '.join(best_candidate[1].moves[:4])}")
            print(f"├─ Item: {best_candidate[1].item}")
            print(f"╰─ Ability: {best_candidate[1].ability}")

            new_roles = identify_roles(best_candidate[1])
            for role in new_roles:
                if role in team_needs and team_needs[role]:
                    team_needs[role].pop(0)
        else:
            print(f"No more suitable candidates found ({candidates_evaluated} evaluated)")
            break

        if len(team) < 6:
            print(f"\nBuilding team (slot {len(team) + 1}/6)...")

    return team
