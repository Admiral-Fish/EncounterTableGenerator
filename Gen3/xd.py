import io
import os
import struct

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

POKEMON = {
    27: 27, # Sandshrew
    207: 207, # Gligar
    332: 328, # Trapinch

    187: 187, # Hoppip
    231: 231, # Phanphy
    311: 283, # Surskit

    41: 41, # Zubat
    382: 304, # Aron
    194: 194 # Wooper
}


def encounters(text: bool):
    XD_ENCOUNTERS = f"{SCRIPT_FOLDER}/xd/pokespot.bin"

    with open(XD_ENCOUNTERS, "rb") as f:
        encounters = []
        for i in range(3):
            encounters.append(f.read(36))

    xd = bytes()
    for map_number, encounter in enumerate(encounters):
        encounter_data = bytes()
        encounter_data += map_number.to_bytes(1, "little")
        encounter_data += b"\x00" # 1 byte padding

        stream = io.BytesIO(encounter)
        stream.seek(0)

        for i in range(3):
            min_level = stream.read(1)
            max_level = stream.read(1)
            specie = POKEMON[struct.unpack(">H", stream.read(2))[0]].to_bytes(2, "little") # Specie
            stream.read(4) # Encounter rate
            stream.read(4) # Snack steps

            encounter_data += specie
            encounter_data += max_level
            encounter_data += min_level

        xd += encounter_data

    with open("xd.bin", "wb+") as f:
        f.write(xd)

    if text:
        map_names = [(0, "Rock Poke Spot"), (1, "Oasis Poke Spot"), (2, "Cave Poke Spot")]
        with open("gales_en.txt", "w+") as f:
            map_names.sort(key=lambda x: x[0])
            for i, (num, name) in enumerate(map_names):
                f.write(f"{num},{name}")
                if i != len(map_names) - 1:
                    f.write("\n")
