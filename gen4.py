
import csv
import re
import requests


def clean_string(map_string: str):
    map_string = map_string.replace("MAPSEC_", "").replace("_", " ")

    strings = map_string.split()
    for i, string in enumerate(strings):
        strings[i] = string.capitalize()

    return " ".join(strings)


def hgss_bug():
    DATA = "https://raw.githubusercontent.com/pret/pokeheartgold/master/files/data/mushi/mushi_encount.csv"
    POKEMON = "https://raw.githubusercontent.com/pret/pokeheartgold/master/include/constants/species.h"

    with requests.get(DATA) as r:
        csv_file = csv.reader(r.content.decode("utf-8").splitlines())
        next(csv_file)
        data = [row for row in csv_file]

    with requests.get(POKEMON) as r:
        matches = re.findall(r"#define\s+(\S+)\s+(\d+)", r.content.decode("utf-8"))
        pokemon = {}
        for name, num in matches:
            pokemon[name.strip()] = int(num)

    bug = bytearray()
    LOCATION_START = 120
    for i in range(4):
        bug += (LOCATION_START + i).to_bytes(1, "big")
        for j in range(10):
            offset = (i * 10) + j
            species, min_level, max_level, _, _ = data[offset]

            bug += int(min_level).to_bytes(1, "big")
            bug += int(max_level).to_bytes(1, "big")
            bug += pokemon[species].to_bytes(2, "big")

    with open("heartgold_bug.bin", "wb") as f:
        f.write(bug)


def hgss():
    DATA_HG = "https://raw.githubusercontent.com/pret/pokeheartgold/master/files/fielddata/encountdata/g_enc_data.csv"
    DATA_SS = "https://raw.githubusercontent.com/pret/pokeheartgold/master/files/fielddata/encountdata/s_enc_data.csv"
    MAPS = "https://raw.githubusercontent.com/pret/pokeheartgold/master/include/constants/map_sections.h"
    MAP_HEADERS = "https://raw.githubusercontent.com/pret/pokeheartgold/master/src/map_header.c"
    POKEMON = "https://raw.githubusercontent.com/pret/pokeheartgold/master/include/constants/species.h"

    with requests.get(DATA_HG) as r:
        csv_file = csv.reader(r.content.decode("utf-8").splitlines())
        next(csv_file)
        data_hg = [row for row in csv_file]

    with requests.get(DATA_SS) as r:
        csv_file = csv.reader(r.content.decode("utf-8").splitlines())
        next(csv_file)
        data_ss = [row for row in csv_file]

    with requests.get(MAPS) as r:
        matches = re.findall(r"#define\s+(MAPSEC_\S+)\s+(\d+)",
                             r.content.decode("utf-8"))
        maps = {}
        for map, num in matches:
            maps[map.strip()] = int(num)

    with requests.get(MAP_HEADERS) as r:
        matches = re.findall(r"(ENCDATA_\S+),.+(MAPSEC_\S+),", r.content.decode("utf-8"))
        map_headers = {}
        for encounter, map in matches:
            if encounter != "ENCDATA_NA":
                map_headers[encounter] = map

    with requests.get(POKEMON) as r:
        matches = re.findall(r"#define\s+(\S+)\s+(\d+)", r.content.decode("utf-8"))
        pokemon = {}
        for name, num in matches:
            pokemon[name.strip()] = int(num)

    hg = bytearray()
    map_names = []
    for row in data_hg:
        if f"ENCDATA_{row[0]}" in map_headers.keys():
            location = maps[map_headers[f"ENCDATA_{row[0]}"]]
            hg += location.to_bytes(2, "big")

            map_name = (location, clean_string(map_headers[f"ENCDATA_{row[0]}"]))
            if map_name not in map_names:
                map_names.append(map_name)

            for i in range(1, len(row)):
                item = row[i]
                if "SPECIES" in item:
                    hg += pokemon[item].to_bytes(2, "big")
                else:
                    hg += int(item).to_bytes(1, "big")


    ss = bytearray()
    for row in data_ss:
        if f"ENCDATA_{row[0]}" in map_headers.keys():
            location = maps[map_headers[f"ENCDATA_{row[0]}"]]
            ss += location.to_bytes(2, "big")

            map_name = (location, clean_string(map_headers[f"ENCDATA_{row[0]}"]))
            if map_name not in map_names:
                map_names.append(map_name)

            for i in range(1, len(row)):
                item = row[i]
                if "SPECIES" in item:
                    ss += pokemon[item].to_bytes(2, "big")
                else:
                    ss += int(item).to_bytes(1, "big")

    with open("hg.bin", "wb+") as f:
        f.write(hg)

    with open("ss.bin", "wb+") as f:
        f.write(ss)

    with open("hgss_en.txt", "w+") as f:
        map_names.sort(key=lambda x: x[0])
        for num, name in map_names:
            f.write(f"{num},{name}\n")


def dp():
    pass


def pt():
    pass


if __name__ == "__main__":
    hgss()
    hgss_bug()
