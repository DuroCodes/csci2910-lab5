import argparse
from pokepaste import generate_pokepaste, upload_pokepaste
from team_builder import build_team

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a Pokemon team")
    parser.add_argument("pokemon", nargs="?", help="Pokemon name to build team around")
    args = parser.parse_args()

    pokemon_name = args.pokemon
    if not pokemon_name:
        pokemon_name = input("Enter Pokemon name: ").strip()

    team = build_team(pokemon_name)
    if not team:
        print("No team found")
        exit(1)

    output = generate_pokepaste(team)
    paste_url = upload_pokepaste(output)

    print("\nPokePaste URL:")
    print(f"╰─ {paste_url}")
