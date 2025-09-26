import requests
from urllib.parse import urlencode
from models import TeamMember


def generate_pokepaste(team: list[TeamMember]) -> str:
    # based on https://pokepast.es/syntax.html
    paste_lines = []

    for member in team:
        pokemon = member.pokemon
        pokemon_set = member.set

        item_line = f"{pokemon.name.title()}"
        if pokemon_set.item:
            item_line += f" @ {pokemon_set.item}"
        paste_lines.append(item_line)

        if pokemon_set.ability:
            paste_lines.append(f"Ability: {pokemon_set.ability}")

        if pokemon_set.evs:
            ev_parts = []
            for stat, value in pokemon_set.evs.items():
                ev_parts.append(f"{value} {stat.title()}")
            if ev_parts:
                paste_lines.append(f"EVs: {' / '.join(ev_parts)}")

        if pokemon_set.nature:
            paste_lines.append(f"{pokemon_set.nature} Nature")

        if pokemon_set.moves:
            paste_lines.append("- " + "\n- ".join(pokemon_set.moves[:4]))

        paste_lines.append("")

    return "\n".join(paste_lines)


def upload_pokepaste(paste: str) -> str:
    # pokepast.es expects CRLF, not LF for some reason
    paste_with_crlf = paste.replace("\n", "\r\n")
    data = {"paste": paste_with_crlf, "title": "", "author": "", "notes": ""}

    response = requests.post(
        "https://pokepast.es/create",
        data=data,
        allow_redirects=True,
    )
    return response.url
