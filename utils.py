from models import TeamMember


def normalize_pokemon_name(name: str) -> str:
    """Smogon's sets use different naming scheme than PokeAPI, so we need to normalize certain Pokémon names"""

    name_mappings = {
        "tapukoko": "tapu-koko",
        "tapulele": "tapu-lele",
        "tapubulu": "tapu-bulu",
        "tapufini": "tapu-fini",
        "keldeo": "keldeo-ordinary",
        "thundurus": "thundurus-incarnate",
        "thundurustherian": "thundurus-therian",
        "landorus": "landorus-incarnate",
        "landorustherian": "landorus-therian",
        "tornadus": "tornadus-incarnate",
        "tornadustherian": "tornadus-therian",
        "deoxys": "deoxys-normal",
        "deoxysattack": "deoxys-attack",
        "deoxysdefense": "deoxys-defense",
        "deoxysspeed": "deoxys-speed",
        "giratina": "giratina-altered",
        "giratinoorigin": "giratina-origin",
        "shaymin": "shaymin-land",
        "shayminsky": "shaymin-sky",
        "basculin": "basculin-red-striped",
        "basculinbluestripe": "basculin-blue-striped",
        "darmanitan": "darmanitan-standard",
        "darmanitanzen": "darmanitan-zen",
        "meloetta": "meloetta-aria",
        "meloettapirouette": "meloetta-pirouette",
        "aegislash": "aegislash-shield",
        "aegislashblade": "aegislash-blade",
        "pumpkaboo": "pumpkaboo-average",
        "pumpkaboosmall": "pumpkaboo-small",
        "pumpkaboolarge": "pumpkaboo-large",
        "pumpkaboosuper": "pumpkaboo-super",
        "gourgeist": "gourgeist-average",
        "gourgeistsmall": "gourgeist-small",
        "gourgeistlarge": "gourgeist-large",
        "gourgeistsuper": "gourgeist-super",
        "zygarde": "zygarde-50",
        "zygarde10": "zygarde-10",
        "zygardecomplete": "zygarde-complete",
        "oricorio": "oricorio-baile",
        "oricoriopom": "oricorio-pom-pom",
        "oricoriopau": "oricorio-pau",
        "oricoriosensu": "oricorio-sensu",
        "lycanroc": "lycanroc-midday",
        "lycanrocmidnight": "lycanroc-midnight",
        "lycanrocdusk": "lycanroc-dusk",
        "wishiwashi": "wishiwashi-solo",
        "wishiwashischool": "wishiwashi-school",
        "minior": "minior-red-meteor",
        "miniororange": "minior-orange-meteor",
        "minioryellow": "minior-yellow-meteor",
        "miniorgreen": "minior-green-meteor",
        "miniorblue": "minior-blue-meteor",
        "miniorindigo": "minior-indigo-meteor",
        "miniorviolet": "minior-violet-meteor",
        "miniorred": "minior-red",
        "miniororangecore": "minior-orange",
        "minioryellowcore": "minior-yellow",
        "miniorgreencore": "minior-green",
        "miniorbluecore": "minior-blue",
        "miniorindigocore": "minior-indigo",
        "miniorvioletcore": "minior-violet",
        "necrozma": "necrozma-dusk-mane",
        "necrozmadawnwings": "necrozma-dawn-wings",
        "necrozmaultra": "necrozma-ultra",
        "mimikyu": "mimikyu-disguised",
        "mimikyubusted": "mimikyu-busted",
        "toxtricity": "toxtricity-amped",
        "toxtricitylowkey": "toxtricity-low-key",
        "indeedee": "indeedee-male",
        "morpeko": "morpeko-full-belly",
        "morpekohangry": "morpeko-hangry",
        "eiscue": "eiscue-ice",
        "eiscuenoice": "eiscue-noice",
        "zacian": "zacian-hero",
        "zaciancrowned": "zacian-crowned",
        "zamazenta": "zamazenta-hero",
        "zamazentacrowned": "zamazenta-crowned",
        "urshifu": "urshifu-single-strike",
        "urshifurapidstrike": "urshifu-rapid-strike",
        "calyrex": "calyrex",
        "calyrexice": "calyrex-ice-rider",
        "calyrexshadow": "calyrex-shadow-rider",
        "enamorus": "enamorus-incarnate",
        "enamorustherian": "enamorus-therian",
    }

    normalized = name.lower().replace(" ", "").replace("'", "").replace(".", "")

    if normalized in name_mappings:
        return name_mappings[normalized]

    return name


def normalize_for_comparison(name: str) -> str:
    return normalize_pokemon_name(name).lower().replace(" ", "").replace("'", "").replace(".", "")


def get_first_item(item: str | list[str]) -> str:
    return item[0] if isinstance(item, list) else item
