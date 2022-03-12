import json
import os

from .compress import compress_encounter_dppt
from .narc import Narc
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    D_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/dp/d_enc_data.narc").get_elements()
    P_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/dp/p_enc_data.narc").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/dp/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/dp/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(559):
            map_headers.append(f.read(24))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["dppt"]

    d = bytes()
    p = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[14] | (map_header[15] << 8)

        # Mt Coronet Summit covers two maps, with the same tables
        if encounter_id == 14:
            continue

        # Old Chateau has only two tables that differ, skip the others
        if encounter_id in (126, 127, 128, 129, 130, 131, 133):
            continue

        # Turnback Cave has duplicate entries based on pillars encountered
        if encounter_id in (64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80):
            continue

        # Solaceon Ruins all share the same table
        if encounter_id in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46):
            continue

        if encounter_id != 65535:
            location_number = map_header[18] | (map_header[19] << 8)
            location_name = MAP_NAMES[location_number]
            if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
                location_name = location_modifiers[location_name][str(encounter_id)]

            map_name = (encounter_id, location_name)
            map_names.append(map_name)

            # Diamond
            d += encounter_id.to_bytes(2, "little")
            d += compress_encounter_dppt(D_ENCOUNTERS[encounter_id])

            # Pearl
            p += encounter_id.to_bytes(2, "little")
            p += compress_encounter_dppt(P_ENCOUNTERS[encounter_id])

    with open("diamond.bin", "wb+") as f:
        f.write(d)

    with open("pearl.bin", "wb+") as f:
        f.write(p)

    with open("dppt_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: (x[1], x[0]))
        for num, name in map_names:
            f.write(f"{num},{name}\n")
