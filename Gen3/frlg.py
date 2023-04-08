import json
import re

import requests

from .text import clean_string, load_pokemon

UNOWN = {
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER": [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 27],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER": [2,  2,  2,  3,  3,  3,  7,  7,  7, 20, 20, 14],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER": [13, 13, 13, 13, 18, 18, 18, 18,  8,  8,  4,  4],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER": [15, 15, 11, 11,  9,  9, 17, 17, 17, 16, 16, 16],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER": [24, 24, 19, 19,  6,  6,  6,  5,  5,  5, 10, 10],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER": [21, 21, 21, 22, 22, 22, 23, 23, 12, 12,  1,  1],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER": [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 26]
}


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

    encounter_data += b"\x00" # 1 byte padding

    if land:
        for i, slot in enumerate(encounter["land_mons"]["mons"]):
            species = pokemon[slot["species"]]
            if encounter["map"] in UNOWN.keys():
                form = UNOWN[encounter["map"]][i]
                species = (form << 11) | species

            encounter_data += species.to_bytes(2, "little")
            encounter_data += slot["min_level"].to_bytes(1, "little")
            encounter_data += b"\x00" # 1 byte padding
    else:
        encounter_data += b"\x00" * (12 * 4)

    if water:
        for slot in encounter["water_mons"]["mons"]:
            encounter_data += pokemon[slot["species"]].to_bytes(2, "little")
            encounter_data += slot["max_level"].to_bytes(1, "little")
            encounter_data += slot["min_level"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00" * (5 * 4)

    if rock:
        for slot in encounter["rock_smash_mons"]["mons"]:
            encounter_data += pokemon[slot["species"]].to_bytes(2, "little")
            encounter_data += slot["max_level"].to_bytes(1, "little")
            encounter_data += slot["min_level"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00" * (5 * 4)

    if fish:
        for slot in encounter["fishing_mons"]["mons"]:
            encounter_data += pokemon[slot["species"]].to_bytes(2, "little")
            encounter_data += slot["max_level"].to_bytes(1, "little")
            encounter_data += slot["min_level"].to_bytes(1, "little")
    else:
        encounter_data += b"\x00" * (10 * 4)

    return encounter_data


def encounters(text: bool):
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

    fr = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "FireRed" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        fr += create_encounter(encounter, map_number, pokemon)

    lg = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "LeafGreen" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        lg += create_encounter(encounter, map_number, pokemon)

    with open("firered.bin", "wb+") as f:
        f.write(fr)

    with open("leafgreen.bin", "wb+") as f:
        f.write(lg)

    if text:
        with open("frlg_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
