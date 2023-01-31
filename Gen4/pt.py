import os

from .compress import compress_encounter_dppt
from .narc import Narc

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    PT_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/pt/pl_enc_data.narc").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/pt/mapheaders.bin"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(593):
            map_headers.append(f.read(24))

    pt = bytes()
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
        if encounter_id in (31, 33, 35, 36, 37, 38, 39, 44, 45, 46):
            continue

        if encounter_id != 65535:
            # Platinum
            pt += encounter_id.to_bytes(1, "little")
            pt += compress_encounter_dppt(PT_ENCOUNTERS[encounter_id])

    with open("platinum.bin", "wb+") as f:
        f.write(pt)
