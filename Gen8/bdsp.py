import json
import os

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def encounters():
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
        if map_number in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46):
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

        # FormProb, Nazo, Annoon Table
        # Literally no clue what these are used for, skip for now

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
            p += entry["monsNo"].to_bytes(2, "little")

        # Swarm modifiers (same level)
        for entry in encounter["tairyo"]:
            p += entry["monsNo"].to_bytes(2, "little")

        # Day modifiers (same level)
        for entry in encounter["day"]:
            p += entry["monsNo"].to_bytes(2, "little")

        # Night modifiers (same level)
        for entry in encounter["night"]:
            p += entry["monsNo"].to_bytes(2, "little")

        # Radar modifiers (same level)
        for entry in encounter["swayGrass"]:
            p += entry["monsNo"].to_bytes(2, "little")

        # FormProb, Nazo, Annoon Table
        # Literally no clue what these are used for, skip for now

        # Skipping dual slot encounters, the switch doesn't have a GBA reader

        # Surf
        p += encounter["encRate_wat"].to_bytes(1, "little")
        for entry in encounter["water_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            p += entry["monsNo"].to_bytes(2, "little")

        # Old rod
        p += encounter["encRate_turi_boro"].to_bytes(1, "little")
        for entry in encounter["boro_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            p += entry["monsNo"].to_bytes(2, "little")

        # Good rod
        p += encounter["encRate_turi_ii"].to_bytes(1, "little")
        for entry in encounter["ii_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            p += entry["monsNo"].to_bytes(2, "little")

        # Super rod
        p += encounter["encRate_sugoi"].to_bytes(1, "little")
        for entry in encounter["sugoi_mons"]:
            p += entry["maxlv"].to_bytes(1, "little")
            p += entry["minlv"].to_bytes(1, "little")
            p += entry["monsNo"].to_bytes(2, "little")

    with open("bd.bin", "wb+") as f:
        f.write(d)

    with open("sp.bin", "wb+") as f:
        f.write(p)

    with open("bdsp_en.txt", "w+", encoding="utf-8") as f:
        map_names.sort(key=lambda x: x[0])
        for i, (num, name) in enumerate(map_names):
            f.write(f"{num},{name}")
            if i != len(map_names) - 1:
                f.write("\n")

def underground():
    UG_ENCOUNT_02 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_02.json"
    UG_ENCOUNT_03 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_03.json"
    UG_ENCOUNT_04 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_04.json"
    UG_ENCOUNT_05 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_05.json"
    UG_ENCOUNT_06 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_06.json"
    UG_ENCOUNT_07 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_07.json"
    UG_ENCOUNT_08 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_08.json"
    UG_ENCOUNT_09 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_09.json"
    UG_ENCOUNT_10 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_10.json"
    UG_ENCOUNT_11 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_11.json"
    UG_ENCOUNT_12 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_12.json"
    UG_ENCOUNT_20 = f"{SCRIPT_FOLDER}/bdsp/UgEncount_20.json"
    UG_SPECIAL_POKEMON = f"{SCRIPT_FOLDER}/bdsp/UgSpecialPokemon.json"
    UG_RAND_MARK = f"{SCRIPT_FOLDER}/bdsp/UgRandMark.json"
    TAMAGO_WAZA_TABLE = f"{SCRIPT_FOLDER}/bdsp/TamagoWazaTable.json"
    TAMAGO_WAZA_IGNORE_TABLE = f"{SCRIPT_FOLDER}/bdsp/UgTamagoWazaIgnoreTable.json"
    UG_POKEMON_DATA = f"{SCRIPT_FOLDER}/bdsp/UgPokemonData.json"

    with open(UG_ENCOUNT_02, "r") as f:
        ug_encount_02 = json.load(f)["table"]

    with open(UG_ENCOUNT_03, "r") as f:
        ug_encount_03 = json.load(f)["table"]

    with open(UG_ENCOUNT_04, "r") as f:
        ug_encount_04 = json.load(f)["table"]

    with open(UG_ENCOUNT_05, "r") as f:
        ug_encount_05 = json.load(f)["table"]

    with open(UG_ENCOUNT_06, "r") as f:
        ug_encount_06 = json.load(f)["table"]

    with open(UG_ENCOUNT_07, "r") as f:
        ug_encount_07 = json.load(f)["table"]

    with open(UG_ENCOUNT_08, "r") as f:
        ug_encount_08 = json.load(f)["table"]

    with open(UG_ENCOUNT_09, "r") as f:
        ug_encount_09 = json.load(f)["table"]

    with open(UG_ENCOUNT_10, "r") as f:
        ug_encount_10 = json.load(f)["table"]

    with open(UG_ENCOUNT_11, "r") as f:
        ug_encount_11 = json.load(f)["table"]

    with open(UG_ENCOUNT_12, "r") as f:
        ug_encount_12 = json.load(f)["table"]

    with open(UG_SPECIAL_POKEMON, "r") as f:
        ug_special_encounters = json.load(f)["Sheet1"]

    with open(UG_RAND_MARK, "r") as f:
        ug_rand_mark_json = json.load(f)["table"]

    with open(TAMAGO_WAZA_TABLE, "r") as f:
        tamago_waza_table_json = json.load(f)["Data"]

    with open(TAMAGO_WAZA_IGNORE_TABLE, "r") as f:
        tamago_waza_ignore_table_json = json.load(f)["Sheet1"]

    with open(UG_POKEMON_DATA, "r") as f:
        ug_pokemon_data_json = json.load(f)["table"]

    ug_encount = bytes()
    ug_special_pokemon = bytes()
    ug_rand_mark = bytes()
    tamago_waza_table = bytes()
    tamago_waza_ignore_table = bytes()
    ug_pokemon_data = bytes()

    ug_encount += len(ug_encount_02).to_bytes(1, "little")
    for pokemon in ug_encount_02:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_03).to_bytes(1, "little")
    for pokemon in ug_encount_03:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_04).to_bytes(1, "little")
    for pokemon in ug_encount_04:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_05).to_bytes(1, "little")
    for pokemon in ug_encount_05:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_06).to_bytes(1, "little")
    for pokemon in ug_encount_06:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_07).to_bytes(1, "little")
    for pokemon in ug_encount_07:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_08).to_bytes(1, "little")
    for pokemon in ug_encount_08:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_09).to_bytes(1, "little")
    for pokemon in ug_encount_09:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_10).to_bytes(1, "little")
    for pokemon in ug_encount_10:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_11).to_bytes(1, "little")
    for pokemon in ug_encount_11:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    ug_encount += len(ug_encount_12).to_bytes(1, "little")
    for pokemon in ug_encount_12:
        ug_encount += pokemon["monsno"].to_bytes(2, "little")
        ug_encount += pokemon["version"].to_bytes(1, "little")
        ug_encount += pokemon["zukanflag"].to_bytes(1, "little")

    for pokemon in ug_special_encounters:
        ug_special_pokemon += pokemon["id"].to_bytes(1, "little")
        ug_special_pokemon += pokemon["monsno"].to_bytes(2, "little")
        ug_special_pokemon += pokemon["version"].to_bytes(1, "little")
        ug_special_pokemon += pokemon["Dspecialrate"].to_bytes(2, "little")
        ug_special_pokemon += pokemon["Pspecialrate"].to_bytes(2, "little")

    for entry in ug_rand_mark_json:
        if entry["id"] != 1 and entry["id"] != 20:
            ug_rand_mark += entry["id"].to_bytes(1, "little")
            encount_id = int(entry["FileName"].replace("UgEncount_", ""))
            ug_rand_mark += encount_id.to_bytes(1, "little")
            ug_rand_mark += entry["min"].to_bytes(1, "little")
            ug_rand_mark += entry["max"].to_bytes(1, "little")
            ug_rand_mark += entry["smax"].to_bytes(1, "little")
            ug_rand_mark += entry["mmax"].to_bytes(1, "little")
            ug_rand_mark += entry["lmax"].to_bytes(1, "little")
            ug_rand_mark += entry["llmax"].to_bytes(1, "little")
            for rate in entry["typerate"]:
                ug_rand_mark += rate.to_bytes(1, "little")

    for entry in tamago_waza_table_json:
        tamago_waza_table += entry["no"].to_bytes(2, "little")
        tamago_waza_table += entry["formNo"].to_bytes(1, "little")
        waza = entry["wazaNo"]
        tamago_waza_table += len(waza).to_bytes(1, "little")
        for move_no in waza:
            tamago_waza_table += move_no.to_bytes(2, "little")

    for entry in tamago_waza_ignore_table_json:
        tamago_waza_ignore_table += entry["MonsNo"].to_bytes(2, "little")
        for move_no in entry["Waza"]:
            tamago_waza_ignore_table += move_no.to_bytes(2, "little")

    for entry in ug_pokemon_data_json:
        ug_pokemon_data += entry["monsno"].to_bytes(2, "little")
        ug_pokemon_data += entry["type1ID"].to_bytes(1, "little")
        type_2 = entry["type2ID"]
        if type_2 == -1:
            ug_pokemon_data += (18).to_bytes(1, "little")
        else:
            ug_pokemon_data += entry["type2ID"].to_bytes(1, "little")
        ug_pokemon_data += entry["size"].to_bytes(1, "little")
        for rate in entry["flagrate"]:
            ug_pokemon_data += rate.to_bytes(1, "little")
        ug_pokemon_data += entry["rateup"].to_bytes(1, "little")

    with open("ug_encount.bin", "wb+") as f:
        f.write(ug_encount)

    with open("ug_special_pokemon.bin", "wb+") as f:
        f.write(ug_special_pokemon)

    with open("ug_rand_mark.bin", "wb+") as f:
        f.write(ug_rand_mark)

    with open("tamago_waza_table.bin", "wb+") as f:
        f.write(tamago_waza_table)

    with open("tamago_waza_ignore_table.bin", "wb+") as f:
        f.write(tamago_waza_ignore_table)
        
    with open("ug_pokemon_data.bin", "wb+") as f:
        f.write(ug_pokemon_data)
