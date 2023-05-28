import json
import os
import re

from .pack import pack_encounter_gen3
from .text import clean_string

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    DATA = f"{SCRIPT_FOLDER}/frlg/wild_encounters.json"

    with open(DATA, "r") as f:
        encounters = json.load(f)

    map_names = []

    fr = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "FireRed" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        fr += map_number.to_bytes(1, "little")
        fr += pack_encounter_gen3(encounter)

    lg = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "LeafGreen" in x["base_label"], encounters)):
        # Altering Cave has 8 unused tables
        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            continue

        lg += map_number.to_bytes(1, "little")
        lg += pack_encounter_gen3(encounter)

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
