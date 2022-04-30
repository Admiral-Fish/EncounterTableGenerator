import io
import json
import os
import struct

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
    map_names.append((149, "Safari Zone (Plains)"))
    map_names.append((150, "Safari Zone (Meadow)"))
    map_names.append((151, "Safari Zone (Savannah)"))
    map_names.append((152, "Safari Zone (Peak)"))
    map_names.append((153, "Safari Zone (Rocky Beach)"))
    map_names.append((154, "Safari Zone (Wetland)"))
    map_names.append((155, "Safari Zone (Forest)"))
    map_names.append((156, "Safari Zone (Swamp)"))
    map_names.append((157, "Safari Zone (Marshland)"))
    map_names.append((158, "Safari Zone (Wasteland)"))
    map_names.append((159, "Safari Zone (Mountain)"))
    map_names.append((160, "Safari Zone (Desert)"))
    with open("hgss_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: x[0])
        for i, (num, name) in enumerate(map_names):
            f.write(f"{num},{name}")
            if i != len(map_names) - 1:
                f.write("\n")


def bug():
    BUG_ENCOUNT = f"{SCRIPT_FOLDER}/hgss/mushi_encount.bin"

    with open(BUG_ENCOUNT, "rb") as f:
        bug_stream = io.BytesIO(f.read())

    bug = bytearray()
    LOCATION_START = 142
    for i in range(4):
        bug += (LOCATION_START + i).to_bytes(1, "little")
        for _ in range(10):
            bug += struct.unpack("<H", bug_stream.read(2))[0].to_bytes(2, "little") # Specie
            bug += bug_stream.read(1) # Min level
            bug += bug_stream.read(1) # Max level
            bug_stream.read(4)

    with open("hgss_bug.bin", "wb") as f:
        f.write(bug)


def headbutt():
    HG_HEADBUTT_ENCOUNT = Narc(f"{SCRIPT_FOLDER}/hgss/hg_headbutt").get_elements()
    SS_HEADBUTT_ENCOUNT = Narc(f"{SCRIPT_FOLDER}/hgss/ss_headbutt").get_elements()

    locations = (
        111, 112, 113, 114, 115, 116, 117, 118, 121, 92, 122, 123,
        124, 125, 127, 129, 131, 103, 104, 105, 1, 3, 4, 8,
        17, 21, 22, 25, 26, 38, 39, 52, 57, 59, 67, 68,
        95, 96, 147, 97, 98, 99, 100, 0, 2, 5, 146, 27,
        58, 85, 128, 24, 20, 137, 71, 102, 148, 136, 125, 87
    )

    index = 0
    hg_headbutt = bytearray()
    ss_headbutt = bytearray()
    # HG and SS encounters fairly match except for minor differences in levels
    for hg_encounter, ss_encounter in zip(HG_HEADBUTT_ENCOUNT, SS_HEADBUTT_ENCOUNT):
        # If there are no trees, then skip
        if hg_encounter[0] == 0 and hg_encounter[2] == 0:
            continue

        # Skip double Route 16
        if index == 58:
            index += 1
            continue
        else:
            hg_headbutt += locations[index].to_bytes(1, "little")
            ss_headbutt += locations[index].to_bytes(1, "little")
            index += 1

        hg_special_trees = 1 if hg_encounter[2] != 0 else 0
        ss_special_trees = 1 if ss_encounter[2] != 0 else 0

        hg_headbutt += hg_special_trees.to_bytes(1, "little")
        ss_headbutt += ss_special_trees.to_bytes(1, "little")

        hg_stream = io.BytesIO(hg_encounter)
        hg_stream.seek(4)

        ss_stream = io.BytesIO(ss_encounter)
        ss_stream.seek(4)

        # Add normal tree tables
        for _ in range(12):
            # Species
            hg_headbutt += struct.unpack("<H", hg_stream.read(2))[0].to_bytes(2, "little")
            hg_headbutt += hg_stream.read(1) # Min level
            hg_headbutt += hg_stream.read(1) # Max level

            # Species
            ss_headbutt += struct.unpack("<H", ss_stream.read(2))[0].to_bytes(2, "little")
            ss_headbutt += ss_stream.read(1) # Min level
            ss_headbutt += ss_stream.read(1) # Max level

        # Check for special trees
        if hg_special_trees != 0:
            for _ in range(6):
                # Species
                hg_headbutt += struct.unpack("<H", hg_stream.read(2))[0].to_bytes(2, "little")
                hg_headbutt += hg_stream.read(1) # Min level
                hg_headbutt += hg_stream.read(1) # Max level

                # Species
                ss_headbutt += struct.unpack("<H", ss_stream.read(2))[0].to_bytes(2, "little")
                ss_headbutt += ss_stream.read(1) # Min level
                ss_headbutt += ss_stream.read(1) # Max level

    with open("hg_headbutt.bin", "wb") as f:
        f.write(hg_headbutt)

    with open("ss_headbutt.bin", "wb") as f:
        f.write(ss_headbutt)


def safari():
    SAFARI_ENCOUNT = Narc(f"{SCRIPT_FOLDER}/hgss/safari").get_elements()

    safari = bytearray()
    LOCATION_START = 149
    # HG and SS encounters match
    for index, safari_encounter in enumerate(SAFARI_ENCOUNT):
        safari += (LOCATION_START + index).to_bytes(1, "little")

        # Water flag
        water_flag = index not in (1, 4, 5, 7, 8)
        safari += b"\x00" if water_flag else b"\x01"

        safari_stream = io.BytesIO(safari_encounter)

        tall_grass_encounters = safari_encounter[0] # 10
        surfing_encounters = safari_encounter[1] # 3
        old_rod_encounters = safari_encounter[2] # 2
        good_rod_encounters = safari_encounter[3] # 2
        super_rod_encounters = safari_encounter[4] # 2

        encounters = (
            tall_grass_encounters, surfing_encounters, old_rod_encounters,
            good_rod_encounters, super_rod_encounters
        )

        safari_stream.seek(8)

        # Grass, Surfing, Old Rod, Good Rod, Super Rod
        for encounter_index, encounter in enumerate(encounters):
            for normal_slot in range(30):
                # Species
                safari += struct.unpack("<H", safari_stream.read(2))[0].to_bytes(2, "little")
                safari += safari_stream.read(1) # Level
                safari_stream.read(1) # Padding

            for block_slot in range(encounter * 3):
                # Block Species
                safari += struct.unpack("<H", safari_stream.read(2))[0].to_bytes(2, "little")
                safari += safari_stream.read(1) # Level
                safari_stream.read(1) # Padding

            for _ in range(encounter):
                # Blocks
                safari += safari_stream.read(1) # First Block Object Type
                safari += safari_stream.read(1) # First Block Object Quantity
                safari += safari_stream.read(1) # Second Block Object Type
                safari += safari_stream.read(1) # Second Block Object Quantity

            # Skip water encounters in areas without water
            if water_flag:
                break

    with open("hgss_safari.bin", "wb") as f:
        f.write(safari)
