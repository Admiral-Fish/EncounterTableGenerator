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

        # Ruins of Alpha interior all share the same table
        if encounter_id in (11, 12, 13):
            continue

        if (encounter_id := map_header[0]) != 255:
            location_number = map_header[18]
            location_name = MAP_NAMES[location_number]
            if location_name in location_modifiers and str(encounter_id) in location_modifiers[location_name]:
                location_name = location_modifiers[location_name][str(encounter_id)]

            map_name = (encounter_id, location_name)
            map_names.append(map_name)

            # HG
            hg += encounter_id.to_bytes(1, "little")
            hg += compress_encounter_hgss(HG_ENCOUNTERS[encounter_id])

            # SS
            ss += encounter_id.to_bytes(1, "little")
            ss += compress_encounter_hgss(SS_ENCOUNTERS[encounter_id])

    with open("heartgold.bin", "wb+") as f:
        f.write(hg)

    with open("soulsilver.bin", "wb+") as f:
        f.write(ss)

    map_names.append((142, "Bug Contest"))
    map_names.append((143, "Bug Contest (Tuesday)"))
    map_names.append((144, "Bug Contest (Thursday)"))
    map_names.append((145, "Bug Contest (Saturday)"))
    map_names.append((146, "Azalea Town"))
    map_names.append((147, "Pewter City"))
    map_names.append((148, "Safari Zone Gate"))
    with open("hgss_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: x[0])
        for i, (num, name) in enumerate(map_names):
            f.write(f"{num},{name}")
            if i != len(map_names) - 1:
                f.write("\n")


def bug():
    BUG_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/mushi_encount.bin"

    with open(BUG_ENCOUNT, "rb") as f:
        data = f.read()

    bug = bytearray()
    LOCATION_START = 142
    for i in range(4):
        bug += (LOCATION_START + i).to_bytes(1, "little")
        for j in range(10):
            offset = (i * 80) + (j * 8)

            species = data[offset] | (data[offset + 1] << 8)
            min_level = data[offset + 2]
            max_level = data[offset + 3]

            bug += min_level.to_bytes(1, "little")
            bug += max_level.to_bytes(1, "little")
            bug += species.to_bytes(2, "little")

    with open("hgss_bug.bin", "wb") as f:
        f.write(bug)


def headbutt():
    HG_HEADBUTT_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/hg_headbutt"
    SS_HEADBUTT_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/ss_headbutt"

    with open(HG_HEADBUTT_ENCOUNT, "rb") as f:
        hg_data = f.read()

    with open(SS_HEADBUTT_ENCOUNT, "rb") as f:
        ss_data = f.read()

    locations = [
    111, 112, 113, 114, 115, 116, 117, 118, 121, 92, 122,
    123, 124, 125, 127, 129, 131, 103, 104, 105, 1, 3,
    4, 8, 17, 21, 22, 25, 26, 38, 39, 52, 57, 59,
    67, 68, 95, 96, 147, 97, 98, 99, 100, 0, 2, 5,
    146, 27, 58, 85, 128, 24, 20, 137, 71, 102, 148,
    136, 125, 87]

    hg_headbutt = bytearray()
    ss_headbutt = bytearray()
    offset = 4408
    for i in range(60):
        # skip double Route 16
        if i != 58:
            hg_headbutt += locations[i].to_bytes(1, "little")
            ss_headbutt += locations[i].to_bytes(1, "little")

        hg_normal_trees = hg_data[offset]
        ss_normal_trees = ss_data[offset]
        offset += 2

        hg_special_trees = hg_data[offset]
        ss_special_trees = ss_data[offset]
        hg_special_trees_flag = 1 if hg_special_trees != 0 else 0
        ss_special_trees_flag = 1 if ss_special_trees != 0 else 0
        offset += 2

        # skip double Route 16
        if i != 58:
            hg_headbutt += hg_special_trees_flag.to_bytes(1, "little")
            ss_headbutt += ss_special_trees_flag.to_bytes(1, "little")

        # normal1, normal2
        for tree_type in range(2):
            # skip double Route 16
            if i != 58:
                hg_headbutt += tree_type.to_bytes(1, "little")
                ss_headbutt += tree_type.to_bytes(1, "little")

            for n in range(6):
                hg_species = hg_data[offset] | (hg_data[offset + 1] << 8)
                ss_species = ss_data[offset] | (ss_data[offset + 1] << 8)
                offset += 2

                hg_min_level = hg_data[offset]
                ss_min_level = ss_data[offset]
                offset += 1

                hg_max_level = hg_data[offset]
                ss_max_level = ss_data[offset]
                offset += 1

                # skip double Route 16
                if i != 58:
                    hg_headbutt += hg_min_level.to_bytes(1, "little")
                    hg_headbutt += hg_max_level.to_bytes(1, "little")
                    hg_headbutt += hg_species.to_bytes(2, "little")
                    ss_headbutt += ss_min_level.to_bytes(1, "little")
                    ss_headbutt += ss_max_level.to_bytes(1, "little")
                    ss_headbutt += ss_species.to_bytes(2, "little")

        # special
        if hg_special_trees != 0:
            tree_type = 2

            # skip double Route 16
            if i != 58:
                hg_headbutt += tree_type.to_bytes(1, "little")
                ss_headbutt += tree_type.to_bytes(1, "little")

            for s in range(6):
                hg_s_species = hg_data[offset] | (hg_data[offset + 1] << 8)
                ss_s_species = ss_data[offset] | (ss_data[offset + 1] << 8)
                offset += 2

                hg_s_min_level = hg_data[offset]
                ss_s_min_level = ss_data[offset]
                offset += 1

                hg_s_max_level = hg_data[offset]
                ss_s_max_level = ss_data[offset]
                offset += 1

                # skip double Route 16
                if i != 58:
                    hg_headbutt += hg_s_min_level.to_bytes(1, "little")
                    hg_headbutt += hg_s_max_level.to_bytes(1, "little")
                    hg_headbutt += hg_s_species.to_bytes(2, "little")
                    ss_headbutt += ss_s_min_level.to_bytes(1, "little")
                    ss_headbutt += ss_s_max_level.to_bytes(1, "little")
                    ss_headbutt += ss_s_species.to_bytes(2, "little")
        else: # skip in case there aren't any special trees
            offset += 24

        # skips trees coordinates
        offset += (hg_normal_trees + hg_special_trees) * 24

        # skip padding between every area
        if i < 59:
            while hg_data[offset] == 0:
                offset += 1

    with open("hg_headbutt.bin", "wb") as f:
        f.write(hg_headbutt)

    with open("ss_headbutt.bin", "wb") as f:
        f.write(ss_headbutt)
