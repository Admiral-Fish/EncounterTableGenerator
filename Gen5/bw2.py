import json
import os

from .narc import Narc
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    B_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw2/b2_encount").get_elements()
    W_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw2/w2_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/bw2/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/bw2/mapnames.bin")
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(615):
            map_headers.append(f.read(48))

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["bw2"]

    b = bytes()
    w = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[20]

        # Clay Tunnel tables are all the same, we opt to choose one that has the water tables included
        if encounter_id in (84, 86):
            continue

        # Floccessy Rance tables are the same, we opt to choose the one with the grass tables included
        if encounter_id == 44:
            continue

        # Giant Chasm Crater Forest has two tables that are the same
        if encounter_id == 35:
            continue

        # Route 4 has two tables that are the same
        if encounter_id == 105:
            continue

        # The lowest part in Relic Castle all share the same tables
        if encounter_id in (15, 16, 17):
            continue

        # The Volcarona room and it's entrance in Relic Castle share the same table
        if encounter_id == 19:
            continue

        # Reversal Mountain 1F all share the same table
        if encounter_id in (51, 53, 54, 55, 57, 59, 60):
            continue

        # Reversal Mountain B1F share the same table
        if encounter_id == 56:
            continue

        # Reversal Mountain B1F Chamber share the same table
        if encounter_id == 58:
            continue

        # Victory Road 1F has two identical tables
        if encounter_id == 78:
            continue

        # Victory Road (Outside 1) has two identical tables
        if encounter_id == 79:
            continue

        # Underground Ruins has 3 identical tables
        if encounter_id in (88, 89):
            continue

        # Strange House Entrance/Library share the same tables and also have duplicates
        if encounter_id in (62, 63, 64, 66):
            continue

        # Strange House Rooms 1-5 share the same table
        if encounter_id in (67, 68, 69, 70):
            continue

        # Castelia Sewers all have identical tables
        # Table 38 technically modifies levels of rippling water, but the map doesn't have any water
        if encounter_id in (38, 39, 40, 41):
            continue

        if encounter_id != 255:
            location_number = map_header[26]
            location_name = MAP_NAMES[location_number]
            if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
                location_name = location_modifiers[location_name][str(encounter_id)]

            map_name = (encounter_id, location_name)
            map_names.append(map_name)

            # Black 2
            b += location_number.to_bytes(2, "little")
            b += B_ENCOUNTERS[encounter_id]

            # White 2
            w += location_number.to_bytes(2, "little")
            w += W_ENCOUNTERS[encounter_id]

    with open("black2.bin", "wb+") as f:
        f.write(b)

    with open("white2.bin", "wb+") as f:
        f.write(w)

    with open("bw2_en.txt", "w+") as f:
        map_names.sort(key=lambda x: (x[1], x[0]))
        for num, name in map_names:
            f.write(f"{num},{name}\n")
