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

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(559):
            map_headers.append(f.read(24))

    d = bytes()
    p = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[14] | (map_header[15] << 8)
        if encounter_id != 65535:
            location_number = map_header[18] | (map_header[19] << 8)
            location_name = MAP_NAMES[location_number]

            map_name = (location_number, location_name)
            if map_name not in map_names:
                map_names.append(map_name)
            else:
                count = sum([1 for _, name in map_names if name == location_name])
                location_number |= (count << 8)
                map_names.append((location_number, location_name))

            # Diamond
            d += location_number.to_bytes(2, "little")
            d += compress_encounter_dppt(D_ENCOUNTERS[encounter_id])

            # Pearl
            p += location_number.to_bytes(2, "little")
            p += compress_encounter_dppt(P_ENCOUNTERS[encounter_id])

    with open("diamond.bin", "wb+") as f:
        f.write(d)

    with open("pearl.bin", "wb+") as f:
        f.write(p)

    with open("dppt_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: (x[1], x[0]))
        for num, name in map_names:
            f.write(f"{num},{name}\n")
