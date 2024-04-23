import json
import os
import re

from .pack import pack_encounter_gen3
from .text import clean_string

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    DATA = f"{SCRIPT_FOLDER}/emerald/wild_encounters.json"

    with open(DATA, "r") as f:
        encounters = json.load(f)

    emerald = bytes()
    map_names = []
    for map_number, encounter in enumerate(encounters):
        # Altering cave has 8 unused tables
        if re.match(r"gAlteringCave[2-9]", encounter["base_label"]):
            continue

        # Cave of Origin has 3 unused tables
        if "Unused" in encounter["base_label"]:
            continue

        # Abandoned Ship has the same table for all locations
        if map_number == 56:
            continue

        # Magma Hideout has the same table for all locations
        if map_number in (100, 101, 102, 103, 104, 105, 106):
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        emerald += map_number.to_bytes(1, "little")
        emerald += pack_encounter_gen3(encounter)

    with open("emerald.bin", "wb+") as f:
        f.write(emerald)

    if text:
        with open("e_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
