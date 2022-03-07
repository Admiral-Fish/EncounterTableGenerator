import os

from .narc import Narc
from .text import read_map_names

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
    HG_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/hgss/hg_encount").get_elements()
    SS_ENCOUNTERS = Narc(f"{SCRIPT_FOLDER}/hgss/ss_encount").get_elements()
    MAP_HEADERS = f"{SCRIPT_FOLDER}/hgss/mapheaders.bin"
    MAP_NAMES = read_map_names(f"{SCRIPT_FOLDER}/hgss/mapnames.bin")

    with open(MAP_HEADERS, "rb") as f:
        map_headers = []
        for _ in range(540):
            map_headers.append(f.read(24))

    hg = bytes()
    ss = bytes()
    map_names = []
    for map_header in map_headers:
        if (encounter_id := map_header[0]) != 255:
            location_number = map_header[18]
            location_name = MAP_NAMES[location_number]

            map_name = (location_number, location_name)
            if map_name not in map_names:
                map_names.append(map_name)
            else:
                count = sum([1 for _, name in map_names if name == location_name])
                location_number |= (count << 8)
                map_names.append((location_number, location_name))

            # HG
            hg += location_number.to_bytes(2, "little")
            hg += HG_ENCOUNTERS[encounter_id]

            # SS
            ss += location_number.to_bytes(2, "little")
            ss = SS_ENCOUNTERS[encounter_id]

    with open("hg.bin", "wb+") as f:
        f.write(hg)

    with open("ss.bin", "wb+") as f:
        f.write(ss)

    map_names.append((235, "Bug Contest"))
    map_names.append((236, "Bug Contest (Tuesday)"))
    map_names.append((237, "Bug Contest (Thursday)"))
    map_names.append((238, "Bug Contest (Saturday)"))
    with open("hgss_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: x[0])
        for num, name in map_names:
            f.write(f"{num},{name}\n")


def bug():
    BUG_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/mushi_encount.bin"

    with open(BUG_ENCOUNT, "rb") as f:
        data = f.read()

    bug = bytearray()
    LOCATION_START = 235
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
