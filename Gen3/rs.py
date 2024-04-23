import json
import os

from .pack import pack_encounter_gen3
from .text import clean_string

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    DATA = f"{SCRIPT_FOLDER}/rs/wild_encounters.json"

    with open(DATA, "r") as f:
        encounters = json.load(f)

    map_names = []

    ruby = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "Ruby" in x["base_label"], encounters)):
        # Abandoned Ship has the same table for all locations
        if map_number == 51:
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        ruby += map_number.to_bytes(1, "little")
        ruby += pack_encounter_gen3(encounter)

    sapphire = bytes()
    for map_number, encounter in enumerate(filter(lambda x: "Sapphire" in x["base_label"], encounters)):
        # Abandoned Ship has the same table for all locations
        if map_number == 51:
            continue

        map_name = (map_number, clean_string(encounter["map"]))
        if map_name not in map_names:
            map_names.append(map_name)

        sapphire += map_number.to_bytes(1, "little")
        sapphire += pack_encounter_gen3(encounter)

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
