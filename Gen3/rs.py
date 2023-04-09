import json
import re

import requests

from .pack import pack_encounter_gen3
from .text import clean_string, load_pokemon


def encounters(text: bool):
    DATA = "https://raw.githubusercontent.com/pret/pokeruby/master/src/data/wild_encounters.json"
    MAPS = "https://raw.githubusercontent.com/pret/pokeruby/master/include/constants/map_groups.h"

    with requests.get(DATA) as r:
        data = json.loads(r.content)

    with requests.get(MAPS) as r:
        matches = re.findall(r"#define (\S+)\s+(\(.+\))", r.content.decode("utf-8"))
        maps = {}
        for map, num in matches:
            maps[map] = eval(num)

    pokemon = load_pokemon()

    encounters = data["wild_encounter_groups"][0]["encounters"]
    map_names = []

    ruby = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "Ruby" in x["base_label"], encounters)):
        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        ruby += map_number.to_bytes(1, "little")
        ruby += pack_encounter_gen3(encounter, pokemon)

    sapphire = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "Sapphire" in x["base_label"], encounters)):
        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        sapphire += map_number.to_bytes(1, "little")
        sapphire += pack_encounter_gen3(encounter, pokemon)

    with open("ruby.bin", "wb+") as f:
        f.write(ruby)

    with open("sapphire.bin", "wb+") as f:
        f.write(sapphire)

    if text:
        with open("rs_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
