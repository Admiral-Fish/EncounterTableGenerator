import json
import re

import requests

from .pack import pack_encounter_gen3
from .text import clean_string, load_pokemon


def encounters(text: bool):
    DATA = "https://raw.githubusercontent.com/pret/pokeemerald/master/src/data/wild_encounters.json"
    MAPS = "https://raw.githubusercontent.com/pret/pokeemerald/master/include/constants/map_groups.h"

    with requests.get(DATA) as r:
        data = json.loads(r.content)

    with requests.get(MAPS) as r:
        matches = re.findall(r"#define (\S+)\s+(\(.+\))", r.content.decode("utf-8"))
        maps = {}
        for map, num in matches:
            maps[map] = eval(num)

    pokemon = load_pokemon()

    encounters = data["wild_encounter_groups"][0]["encounters"]
    emerald = bytes()
    map_names = []
    for map_number, encounter in enumerate(encounters):
        # Altering cave has 8 unused tables
        if re.match(r"gAlteringCave[2-9]", encounter["base_label"]):
            continue

        # Cave of Origin has 3 unused tables
        if "Unused" in encounter["base_label"]:
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        emerald += map_number.to_bytes(1, "little")
        emerald += pack_encounter_gen3(encounter, pokemon)

    with open("emerald.bin", "wb+") as f:
        f.write(emerald)

    if text:
        with open("e_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
