import os

from .narc import Narc

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    Pt_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/pt/pl_enc_data.narc").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/pt/mapheaders.bin"

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(593):
            map_headers.append(f.read(24))

    pt = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[14] | (map_header[15] << 8)
        if encounter_id != 65535:
            location_number = map_header[18]

            # Platinum
            pt += location_number.to_bytes(2, "little")
            pt += Pt_ENCOUNTERS[encounter_id]

    with open("platinum.bin", "wb+") as f:
        f.write(pt)
