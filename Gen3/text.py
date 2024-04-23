import re


def clean_string(map_string: str):
    map_string = map_string.replace("MAP_", "").replace("_", " ")

    if map_string.startswith("ABANDONED SHIP"):
        map_string = "ABANDONED SHIP"

    if map_string.startswith("MAGMA HIDEOUT"):
        map_string = "MAGMA HIDEOUT"

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
