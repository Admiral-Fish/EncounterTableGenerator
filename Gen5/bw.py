import os

from .narc import Narc
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    B_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw/b_encount").get_elements()
    W_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/bw/w_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/bw/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/bw/mapnames.bin")

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(427):
            map_headers.append(f.read(48))

    b = bytes()
    w = bytes()
    map_names = []
    for map_header in map_headers:
        encounter_id = map_header[20] | (map_header[21] << 8)
        if encounter_id != 65535:
            location_number = map_header[26]
            location_name = MAP_NAMES[location_number]

            map_name = (location_number, location_name)
            if map_name not in map_names:
                map_names.append(map_name)
            else:
                count = sum([1 for _, name in map_names if name == location_name])
                location_number |= (count << 8)
                map_names.append((location_number, location_name))

            # Black
            b += location_number.to_bytes(2, "little")
            b += B_ENCOUNTERS[encounter_id]

            # White
            w += location_number.to_bytes(2, "little")
            w += W_ENCOUNTERS[encounter_id]

    with open("black.bin", "wb+") as f:
        f.write(b)

    with open("white.bin", "wb+") as f:
        f.write(w)

    with open("bw_en.txt", "w+") as f:
        map_names.sort(key=lambda x: (x[1], x[0]))
        for num, name in map_names:
            f.write(f"{num},{name}\n")
