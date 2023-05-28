import re


def clean_string(map_string: str):
    map_string = map_string.replace("MAP_", "").replace("_", " ")

    strings = map_string.split()
    for i, string in enumerate(strings):
        if (match := re.match(r"Route(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Route {match.group(1)}"
        elif (match := re.match(r"Room(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Room {match.group(1)}"
        elif string == "SSANNE":
            strings[i] = "S.S Anne"
        elif string == "UNDERWATER1":
            strings[i] = "Underwater Route 124"
        elif string == "UNDERWATER2":
            strings[i] = "Underwater Route 126"
        elif re.match(r"B(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)R", string):
            strings[i] = string
        else:
            strings[i] = string.capitalize()

    return " ".join(strings)
