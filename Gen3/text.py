import re

import requests


def clean_string(map_string: str):
    map_string = map_string.replace("MAP_", "").replace("_", " ")

    strings = map_string.split()
    for i, string in enumerate(strings):
        if (match := re.match(r"Route(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Route {match.group(1)}"
        elif (match := re.match(r"Room(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Room {match.group(1)}"
        elif re.match(r"B(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)R", string):
            strings[i] = string
        else:
            strings[i] = string.capitalize()

    return " ".join(strings)


def load_pokemon():    
    POKEMON = "https://raw.githubusercontent.com/Admiral-Fish/PokeFinder/master/Source/Core/Resources/i18n/en/species_en.txt"

    with requests.get(POKEMON) as r:
        pokemon = {}
        for i, name in enumerate(r.content.decode("utf-8-sig").splitlines()):
            if name == "Nidoran♂":
                name = "NIDORAN_M"
            elif name == "Nidoran♀":
                name = "NIDORAN_F"

            pokemon[f"SPECIES_{name.upper()}"] = i + 1

        return pokemon
