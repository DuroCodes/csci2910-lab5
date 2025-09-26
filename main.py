import pokepaste
import team_builder

if __name__ == "__main__":
    team = team_builder.build_team("pikachu")
    output = pokepaste.generate_pokepaste(team)
    print(output)
    print(pokepaste.upload_pokepaste(output))
