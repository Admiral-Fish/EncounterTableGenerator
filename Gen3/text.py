import re


def clean_string_frlg(map_string: str):
    map_string = map_string[4:].replace("_", " ")

    if map_string == "VICTORY_ROAD_1F":
        return "Victory Road 1F/3F"

    if map_string == "POKEMON_MANSION_1F":
        return "Pokemon Mansion 1F-3F"

    if map_string == "MAP_POKEMON_TOWER_4F":
        return "Pokemon Tower 4F-5F"

    if map_string == "MT_EMBER_SUMMIT_PATH_1F":
        return "Mt Ember Summit Path 1F/3F"

    if map_string == "FOUR_ISLAND_ICEFALL_CAVE_1F":
        return "Four Island Icefall Cave 1F/B1F"

    if map_string == "FIVE_ISLAND_LOST_CAVE_ROOM1":
        return "Five Island Lost Cave"

    if map_string == "MAP_FIVE_ISLAND_LOST_CAVE_ROOM11":
        return "Five Island Lost Cave Item Room"

    if map_string == "ROUTE21_NORTH":
        return "Route 21"

    return clean_string(map_string)


def clean_string_rse(map_string: str):
    map_string = map_string[4:].replace("_", " ")

    if map_string == "MT_PYRE_1F":
        return "Mt Pyre 1F-3F"

    if map_string.startswith("ABANDONED SHIP"):
        return "Abandoned Ship"

    if map_string == "MT_PYRE_4F":
        return "Mt Pyre 4F-6F"

    if map_string == "SEAFLOOR_CAVERN_ROOM6":
        return "Seafloor Cavern"

    if map_string == "SHOAL_CAVE_LOW_TIDE_INNER_ROOM":
        return "Shoal Cave"

    if map_string.startswith("MAGMA HIDEOUT"):
        return "Magma Hideout"

    if map_string == "MIRAGE_TOWER_1F":
        return "Mirage Tower"

    if map_string == "ARTISAN_CAVE_B1F":
        return "Artisan Cave"

    if map_string == "CAVE_OF_ORIGIN_1F":
        return "Cave Of Origin 1F-B3F"

    map_string = map_string.replace(" LOW TIDE ", "")

    return clean_string(map_string)


def clean_string(map_string: str):
    strings = map_string.split()
    for i, string in enumerate(strings):
        if (match := re.match(r"Route(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Route {match.group(1)}"
        elif (match := re.match(r"Room(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Room {match.group(1)}"
        elif string == "SSANNE":
            strings[i] = "S.S Anne"
        elif string == "UNDERWATER1":
            strings[i] = "Route 124 Underwater"
        elif string == "UNDERWATER2":
            strings[i] = "Route 126 Underwater"
        elif re.match(r"B(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)R", string):
            strings[i] = string
        else:
            strings[i] = string.capitalize()

    return " ".join(strings)
