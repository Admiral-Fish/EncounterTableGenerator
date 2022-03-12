import os
import json

from .compress import compress_encounter_hgss
from .narc import Narc
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    HG_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/hgss/hg_encount").get_elements()
    SS_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/hgss/ss_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/hgss/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/hgss/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(540):
            map_headers.append(f.read(24))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["hgss"]

    hg = bytes()
    ss = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[0]

        # Sprout Tower has the same tables for the entire location
        if encounter_id == 7:
            continue

        # Future note: 23/24 National Park tables depend on national dex or not

        # Bell Tower has the same tables for the entire location
        if encounter_id in (31, 32, 33, 34, 35, 36, 37, 84):
            continue

        # Mt. Moon has two seperate location inside the cave with the same tables
        if encounter_id == 107:
            continue

        if (encounter_id := map_header[0]) != 255:
            location_number = map_header[18]
            location_name = MAP_NAMES[location_number]
            if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
                location_name = location_modifiers[location_name][str(encounter_id)]

            map_name = (encounter_id, location_name)
            map_names.append(map_name)

            # HG
            hg += encounter_id.to_bytes(2, "little")
            hg += compress_encounter_hgss(HG_ENCOUNTERS[encounter_id])

            # SS
            ss += encounter_id.to_bytes(2, "little")
            ss += compress_encounter_hgss(SS_ENCOUNTERS[encounter_id])

    with open("hg.bin", "wb+") as f:
        f.write(hg)

    with open("ss.bin", "wb+") as f:
        f.write(ss)

    map_names.append((142, "Bug Contest"))
    map_names.append((143, "Bug Contest (Tuesday)"))
    map_names.append((144, "Bug Contest (Thursday)"))
    map_names.append((145, "Bug Contest (Saturday)"))
    with open("hgss_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: (x[1], x[0]))
        for num, name in map_names:
            f.write(f"{num},{name}\n")


def bug():
    BUG_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/mushi_encount.bin"

    with open(BUG_ENCOUNT, "rb") as f:
        data = f.read()

    bug = bytearray()
    LOCATION_START = 142
    for i in range(4):
        bug += (LOCATION_START + i).to_bytes(1, "little")
        for j in range(10):
            offset = (i * 10) + (j * 8)

            species = data[offset] | (data[offset + 1] << 8)
            min_level = data[offset + 2]
            max_level = data[offset + 3]

            bug += min_level.to_bytes(1, "little")
            bug += max_level.to_bytes(1, "little")
            bug += species.to_bytes(2, "little")

    with open("heartgold_bug.bin", "wb") as f:
        f.write(bug)
