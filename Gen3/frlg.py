import json
import re

import requests

from .text import clean_string


def encounters():
    DATA = "https://raw.githubusercontent.com/pret/pokefirered/master/src/data/wild_encounters.json"
    MAPS = "https://raw.githubusercontent.com/pret/pokefirered/master/include/constants/map_groups.h"
    POKEMON = "https://raw.githubusercontent.com/pret/pokefirered/master/include/constants/species.h"

    with requests.get(DATA) as r:
        data = json.loads(r.content)

    with requests.get(MAPS) as r:
        matches = re.findall(r"#define (\S+)\s+(\(.+\))", r.content.decode("utf-8"))
        maps = {}
        for map, num in matches:
            maps[map] = eval(num)

    with requests.get(POKEMON) as r:
        matches = re.findall(r"#define (.+) (\d+)", r.content.decode("utf-8"))
        pokemon = {}
        for name, num in matches:
            pokemon[name] = int(num)

    encounters = data["wild_encounter_groups"][0]["encounters"]
    fr = bytearray()
    lg = bytearray()
    map_names = []
    for encounter in encounters:
        encounter_data = bytearray()

        map_number = maps[encounter["map"]]
        encounter_data += map_number.to_bytes(2, "big")

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        if (land := "land_mons" in encounter):
            encounter_data += encounter["land_mons"]["encounter_rate"].to_bytes(1, "big")
        else:
            encounter_data += b"\x00"

        if (water := "water_mons" in encounter):
            encounter_data += encounter["water_mons"]["encounter_rate"].to_bytes(1, "big")
        else:
            encounter_data += b"\x00"

        if (rock := "rock_smash_mons" in encounter):
            encounter_data += encounter["rock_smash_mons"]["encounter_rate"].to_bytes(1, "big")
        else:
            encounter_data += b"\x00"

        if (fish := "fishing_mons" in encounter):
            encounter_data += encounter["fishing_mons"]["encounter_rate"].to_bytes(1, "big")
        else:
            encounter_data += b"\x00"

        if land:
            for slot in encounter["land_mons"]["mons"]:
                level = slot["min_level"]
                species = pokemon[slot["species"]]

                encounter_data += level.to_bytes(1, "big")
                encounter_data += species.to_bytes(2, "big")

        if water:
            for slot in encounter["water_mons"]["mons"]:
                min_level = slot["min_level"]
                max_level = slot["max_level"]
                species = pokemon[slot["species"]]

                encounter_data += min_level.to_bytes(1, "big")
                encounter_data += max_level.to_bytes(1, "big")
                encounter_data += species.to_bytes(2, "big")

        if rock:
            for slot in encounter["rock_smash_mons"]["mons"]:
                min_level = slot["min_level"]
                max_level = slot["max_level"]
                species = pokemon[slot["species"]]

                encounter_data += min_level.to_bytes(1, "big")
                encounter_data += max_level.to_bytes(1, "big")
                encounter_data += species.to_bytes(2, "big")

        if fish:
            for slot in encounter["fishing_mons"]["mons"]:
                min_level = slot["min_level"]
                max_level = slot["max_level"]
                species = pokemon[slot["species"]]

                encounter_data += min_level.to_bytes(1, "big")
                encounter_data += max_level.to_bytes(1, "big")
                encounter_data += species.to_bytes(2, "big")

        if "FireRed" in encounter["base_label"]:
            fr += encounter_data
        else:
            lg += encounter_data

    with open("firered.bin", "wb+") as f:
        f.write(fr)

    with open("leafgreen.bin", "wb+") as f:
        f.write(lg)

    with open("frlg_en.txt", "w+") as f:
        map_names.sort(key=lambda x: x[0])
        for num, name in map_names:
            f.write(f"{num},{name}\n")