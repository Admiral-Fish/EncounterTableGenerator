import re

def clean_string(map_string: str):
    map_string = map_string.replace("MAP_", "").replace("_", " ")

    strings = map_string.split()
    for i, string in enumerate(strings):
        if (match := re.match(r"Route(\d+)", string, re.IGNORECASE)):
            strings[i] = f"Route {match.group(1)}"
        elif re.match(r"B(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)F", string):
            strings[i] = string
        elif re.match(r"(\d+)R", string):
            strings[i] = string
        else:
            strings[i] = string.capitalize()

    return " ".join(strings)