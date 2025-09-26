# CSCI 2910 - Lab 5 (Pokémon Team Builder)

> [!WARNING] This probably isn't very polished, but it works (for the most part)

## Overview

This project aims to create a competitive Pokémon team using the PokeAPI and Smogon data based on the user's input seed Pokémon.

The team is created by first identifying the roles that the seed Pokémon can fill, and then finding other Pokémon that can fill those roles. There are a few key roles that the team needs to fill in order to be viable.

Once the roles are identified, the system will create a team of 6 Pokémon that can fill the roles and return a PokePaste output of the team. You should also be able to upload this to https://pokepast.es to see the team in a better format.

### Roles

- Hazard Setter → Pokémon with stealth rock, spikes, toxic spikes, or sticky web
- Hazard Removal → Pokémon with defog or rapid spin
- Speed Control → Pokémon holding choice scarf
- Pivot → Pokémon with u-turn, volt switch, flip turn, or teleport
- Utility → Pokémon with knock off, toxic, thunder wave, taunt, or encore
- Setup Sweeper → Pokémon with swords dance, nasty plot, calm mind, or dragon dance

## Usage

```bash
python main.py <pokemon_name>
```

If no Pokemon name is provided, you will be prompted to enter one.
