import json
import os
import re
from pathlib import Path

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters(text: bool):
    D_ENCOUNTERS = f"{SCRIPT_FOLDER}/bdsp/FieldEncountTable_d.json"
    P_ENCOUNTERS = f"{SCRIPT_FOLDER}/bdsp/FieldEncountTable_p.json"
    MAP_INFO = f"{SCRIPT_FOLDER}/bdsp/MapInfo.json"
    AREA_NAME = f"{SCRIPT_FOLDER}/bdsp/english_dp_fld_areaname.json"
    LOCATION_MODIFIERS = f"{SCRIPT_FOLDER}/location_modifier.json"

    with open(D_ENCOUNTERS, "r") as f:
        d_encounters = json.load(f)["table"]

    with open(P_ENCOUNTERS, "r") as f:
        p_encounters = json.load(f)["table"]

    with open(MAP_INFO, "r", encoding="utf-8") as f:
        map_info = json.load(f)["ZoneData"]

    with open(AREA_NAME, "r", encoding="utf-8") as f:
        area_name = json.load(f)["labelDataArray"]

    with open(LOCATION_MODIFIERS, "rb") as f:
        location_modifiers = json.load(f)["bdsp"]

    d = bytes()
    p = bytes()
    map_names = []

    for map_number, encounter in enumerate(d_encounters):
        # Mt Coronet Summit covers two maps, with the same tables
        if map_number == 14:
            continue

        # Old Chateau all share the same table
        if map_number in (126, 127, 128, 129, 130, 131, 132, 133):
            continue

        # Turnback Cave has duplicate entries based on pillars encountered
        if map_number in (64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80):
            continue

        # Solaceon Ruins all share the same table
        if map_number in (31, 33, 35, 36, 37, 38, 39, 44, 45, 46):
            continue

        zone_id = encounter["zoneID"]
        zone_data = next((zone for zone in map_info if zone["ZoneID"] == zone_id), None)
        if zone_data is None:
            continue

        place_name = zone_data["PokePlaceName"]
        label_data = next((label for label in area_name if label["labelName"] == place_name))
        if label_data is None:
            continue

        location_name = label_data["wordDataArray"][0]["str"]
        if location_name in location_modifiers and str(map_number) in location_modifiers[location_name]:
            location_name = location_modifiers[location_name][str(map_number)]

        map_name = (map_number, location_name)
        map_names.append(map_name)

        d += map_number.to_bytes(1, "little")

        # Grass encounters
        d += encounter["encRate_gr"].to_bytes(1, "little")
        for entry in encounter["ground_mons"]:
            d += entry["maxlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Swarm modifiers (same level)
        for entry in encounter["tairyo"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # Day modifiers (same level)
        for entry in encounter["day"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # Night modifiers (same level)
        for entry in encounter["night"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # Radar modifiers (same level)
        for entry in encounter["swayGrass"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # FormProb (impacts Shellos/Gastrodon, skipping)

        # Nazo (seems unused)

        # Annoon Table (Unown)

        # Skipping dual slot encounters, the switch doesn't have a GBA reader

        # Surf
        d += encounter["encRate_wat"].to_bytes(1, "little")
        for entry in encounter["water_mons"]:
            d += entry["maxlv"].to_bytes(1, "little")
            d += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Old rod
        d += encounter["encRate_turi_boro"].to_bytes(1, "little")
        for entry in encounter["boro_mons"]:
            d += entry["maxlv"].to_bytes(1, "little")
            d += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Good rod
        d += encounter["encRate_turi_ii"].to_bytes(1, "little")
        for entry in encounter["ii_mons"]:
            d += entry["maxlv"].to_bytes(1, "little")
            d += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Super rod
        d += encounter["encRate_sugoi"].to_bytes(1, "little")
        for entry in encounter["sugoi_mons"]:
            d += entry["maxlv"].to_bytes(1, "little")
            d += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

    for map_number, encounter in enumerate(p_encounters):
        # Mt Coronet Summit covers two maps, with the same tables
        if map_number == 14:
            continue

        # Old Chateau all share the same table
        if map_number in (126, 127, 128, 129, 130, 131, 132, 133):
            continue

        # Turnback Cave has duplicate entries based on pillars encountered
        if map_number in (64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80):
            continue

        # Solaceon Ruins all share the same table
        if map_number in (31, 33, 35, 36, 37, 38, 39, 44, 45, 46):
            continue

        zone_id = encounter["zoneID"]

        zone_data = next((zone for zone in map_info if zone["ZoneID"] == zone_id), None)
        if zone_data is None:
            continue

        place_name = zone_data["PokePlaceName"]
        label_data = next((label for label in area_name if label["labelName"] == place_name))
        if label_data is None:
            continue

        p += map_number.to_bytes(1, "little")

        # Grass encounters
        p += encounter["encRate_gr"].to_bytes(1, "little")
        for entry in encounter["ground_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Swarm modifiers (same level)
        for entry in encounter["tairyo"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # Day modifiers (same level)
        for entry in encounter["day"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # Night modifiers (same level)
        for entry in encounter["night"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # Radar modifiers (same level)
        for entry in encounter["swayGrass"]:
            d += entry["monsNo"].to_bytes(2, "little")

        # FormProb (impacts Shellos/Gastrodon, skipping)

        # Nazo (seems unused)

        # Annoon Table (Unown)

        # Skipping dual slot encounters, the switch doesn't have a GBA reader

        # Surf
        p += encounter["encRate_wat"].to_bytes(1, "little")
        for entry in encounter["water_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Old rod
        p += encounter["encRate_turi_boro"].to_bytes(1, "little")
        for entry in encounter["boro_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Good rod
        p += encounter["encRate_turi_ii"].to_bytes(1, "little")
        for entry in encounter["ii_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

        # Super rod
        p += encounter["encRate_sugoi"].to_bytes(1, "little")
        for entry in encounter["sugoi_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            d += entry["monsNo"].to_bytes(2, "little")

    with open("bd.bin", "wb+") as f:
        f.write(d)

    with open("sp.bin", "wb+") as f:
        f.write(p)

    if text:
        with open("bdsp_en.txt", "w+", encoding="utf-8") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")


def underground():
    ENCOUNT = [str(path) for path in Path(f"{SCRIPT_FOLDER}/bdsp/").rglob("UgEncount*")]
    POKEMON_DATA = f"{SCRIPT_FOLDER}/bdsp/UgPokemonData.json"
    RAND_MARK = f"{SCRIPT_FOLDER}/bdsp/UgRandMark.json"
    SPECIAL_POKEMON = f"{SCRIPT_FOLDER}/bdsp/UgSpecialPokemon.json"

    encount = {}
    for path in ENCOUNT:
        with open(path, "r") as f:
            name = re.search(r"(UgEncount_\d+)", path).group(0)
            encount[name] = json.load(f)["table"]

    with open(POKEMON_DATA, "r") as f:
        pokemon_data = json.load(f)["table"]

    with open(RAND_MARK, "r") as f:
        rand_mark = json.load(f)["table"]

    with open(SPECIAL_POKEMON, "r") as f:
        special_pokemon = json.load(f)["Sheet1"]

    d = bytes()
    p = bytes()

    for room_id in range(2, 20):
        special_pokemon_room = list(filter(lambda x: x["id"] == room_id, special_pokemon))

        special_pokemon_rates_d = filter(lambda x: x["version"] != 3, special_pokemon_room)
        special_pokemon_rates_d = list(map(lambda x: (x["monsno"], x["Dspecialrate"]), special_pokemon_rates_d))
        special_pokemon_rates_d.sort(key=lambda x: x[1], reverse=True)

        special_pokemon_rates_p = filter(lambda x: x["version"] != 2, special_pokemon_room)
        special_pokemon_rates_p = list(map(lambda x: (x["monsno"], x["Pspecialrate"]), special_pokemon_rates_p))
        special_pokemon_rates_p.sort(key=lambda x: x[1], reverse=True)

        d += room_id.to_bytes(1, "little")
        d += len(special_pokemon_rates_d).to_bytes(1, "little")
        for rate in special_pokemon_rates_d:
            d += rate[0].to_bytes(2, "little")
            d += rate[1].to_bytes(2, "little")

        p += room_id.to_bytes(1, "little")
        p += len(special_pokemon_rates_p).to_bytes(1, "little")
        for rate in special_pokemon_rates_p:
            p += rate[0].to_bytes(2, "little")
            p += rate[1].to_bytes(2, "little")

        rand_mark_room = list(filter(lambda x: x["id"] == room_id, rand_mark))[0]
        ug_encount = encount[rand_mark_room["FileName"]]

        d += rand_mark_room["min"].to_bytes(1, "little")
        d += rand_mark_room["max"].to_bytes(1, "little")
        for rate in rand_mark_room["typerate"]:
            d += rate.to_bytes(1, "little")

        p += rand_mark_room["min"].to_bytes(1, "little")
        p += rand_mark_room["max"].to_bytes(1, "little")
        for rate in rand_mark_room["typerate"]:
            p += rate.to_bytes(1, "little")

        enabled_pokemon_d = list(filter(lambda x: x["version"] != 3, ug_encount))
        d += len(enabled_pokemon_d).to_bytes(1, "little")
        for enabled_pokemon in enabled_pokemon_d:
            d += enabled_pokemon["zukanflag"].to_bytes(1, "little")
            d += enabled_pokemon["monsno"].to_bytes(2, "little")

            pokemon = list(filter(lambda x: x["monsno"] == enabled_pokemon["monsno"], pokemon_data))[0]
            d += pokemon["size"].to_bytes(1, "little")
            for rate in pokemon["flagrate"]:
                d += rate.to_bytes(1, "little")
            d += pokemon["rateup"].to_bytes(1, "little")

        enabled_pokemon_p = list(filter(lambda x: x["version"] != 2, ug_encount))
        p += len(enabled_pokemon_p).to_bytes(1, "little")
        for enabled_pokemon in enabled_pokemon_p:
            p += enabled_pokemon["zukanflag"].to_bytes(1, "little")
            p += enabled_pokemon["monsno"].to_bytes(2, "little")

            pokemon = list(filter(lambda x: x["monsno"] == enabled_pokemon["monsno"], pokemon_data))[0]
            p += pokemon["size"].to_bytes(1, "little")
            for rate in pokemon["flagrate"]:
                p += rate.to_bytes(1, "little")
            p += pokemon["rateup"].to_bytes(1, "little")

    with open("bd_underground.bin", "wb+") as f:
        f.write(d)

    with open("sp_underground.bin", "wb+") as f:
        f.write(p)
