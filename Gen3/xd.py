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


def encounters():
    XD_ENCOUNTERS = f"{SCRIPT_FOLDER}/xd/pokespot.bin"

    with open(XD_ENCOUNTERS, "rb") as f:
        encounters = []
        for i in range(3):
            encounters.append(f.read(36))

    xd = bytearray()
    for map_number, encounter in enumerate(encounters):
        encounter_data = bytearray()
        encounter_data += map_number.to_bytes(1, "little")

        stream = io.BytesIO(encounter)
        stream.seek(0)

        for i in range(3):
            encounter_data += stream.read(1) # Min level
            encounter_data += stream.read(1) # Max level
            encounter_data += POKEMON[struct.unpack(">H", stream.read(2))[0]].to_bytes(2, "little") # Specie
            stream.read(4) # Encounter rate
            stream.read(4) # Snack steps

        xd += encounter_data

    with open("xd.bin", "wb+") as f:
        f.write(xd)

    map_names = [(0, "Rock Poke Spot"), (1, "Oasis Poke Spot"), (2, "Cave Poke Spot")]
    with open("gales_en.txt", "w+") as f:
        map_names.sort(key=lambda x: x[0])
        for i, (num, name) in enumerate(map_names):
            f.write(f"{num},{name}")
            if i != len(map_names) - 1:
                f.write("\n")
