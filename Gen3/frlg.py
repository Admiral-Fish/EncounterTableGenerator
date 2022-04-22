import json
import re

import requests

from .text import clean_string, load_pokemon


def create_encounter(encounter: dict, map_number: int, pokemon: dict):
    encounter_data = bytes()
    encounter_data += map_number.to_bytes(1, "little")

    if (land := "land_mons" in encounter):
        encounter_data += encounter["land_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00"

    if (water := "water_mons" in encounter):
        encounter_data += encounter["water_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00"

    if (rock := "rock_smash_mons" in encounter):
        encounter_data += encounter["rock_smash_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00"

    if (fish := "fishing_mons" in encounter):
        encounter_data += encounter["fishing_mons"]["encounter_rate"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00"

    if land:
        for slot in encounter["land_mons"]["mons"]:
            level = slot["min_level"]
            species = pokemon[slot["species"]]

            encounter_data += level.to_bytes(1, "little")
            encounter_data += species.to_bytes(2, "little")
    else:
        encounter_data += b"\x00" * (12 * 3)

    if water:
        for slot in encounter["water_mons"]["mons"]:
            min_level = slot["min_level"]
            max_level = slot["max_level"]
            species = pokemon[slot["species"]]

            encounter_data += min_level.to_bytes(1, "little")
            encounter_data += max_level.to_bytes(1, "little")
            encounter_data += species.to_bytes(2, "little")
    else:
        encounter_data += b"\x00" * (5 * 4)

    if rock:
        for slot in encounter["rock_smash_mons"]["mons"]:
            min_level = slot["min_level"]
            max_level = slot["max_level"]
            species = pokemon[slot["species"]]

            encounter_data += min_level.to_bytes(1, "little")
            encounter_data += max_level.to_bytes(1, "little")
            encounter_data += species.to_bytes(2, "little")
    else:
        encounter_data += b"\x00" * (5 * 4)

    if fish:
        for slot in encounter["fishing_mons"]["mons"]:
            min_level = slot["min_level"]
            max_level = slot["max_level"]
            species = pokemon[slot["species"]]

            encounter_data += min_level.to_bytes(1, "little")
            encounter_data += max_level.to_bytes(1, "little")
            encounter_data += species.to_bytes(2, "little")
    else:
        encounter_data += b"\x00" * (10 * 4)

    return encounter_data


def encounters():
    DATA = "https://raw.githubusercontent.com/pret/pokefirered/master/src/data/wild_encounters.json"
    MAPS = "https://raw.githubusercontent.com/pret/pokefirered/master/include/constants/map_groups.h"

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

    fr = bytearray()
    for map_number, encounter in enumerate(filter(lambda x: "FireRed" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        fr += create_encounter(encounter, map_number, pokemon)

    lg = bytearray()
    for map_number, encounter in enumerate(filter(lambda x: "LeafGreen" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        lg += create_encounter(encounter, map_number, pokemon)

    with open("firered.bin", "wb+") as f:
        f.write(fr)

    with open("leafgreen.bin", "wb+") as f:
        f.write(lg)

    with open("frlg_en.txt", "w+") as f:
        map_names.sort(key=lambda x: x[0])
        for i, (num, name) in enumerate(map_names):
            f.write(f"{num},{name}")
            if i != len(map_names) - 1:
                f.write("\n")
