import os
from ctypes import BigEndianStructure, Structure, c_uint8, c_uint16, c_uint32

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

POKEMON = {
    27: 27,  # Sandshrew
    207: 207,  # Gligar
    332: 328,  # Trapinch

    187: 187,  # Hoppip
    231: 231,  # Phanphy
    311: 283,  # Surskit

    41: 41,  # Zubat
    382: 304,  # Aron
    194: 194  # Wooper
}

class Slot(BigEndianStructure):
    _fields_ = [
        ("min_level", c_uint8),
        ("max_level", c_uint8),
        ("specie", c_uint16),
        ("encounter_rate", c_uint32),
        ("snack_steps", c_uint32) 
    ]

class Encounter(Structure):
    _fields_ = [
        ("slots", Slot * 3)
    ]


def encounters(text: bool):
    XD_ENCOUNTERS = f"{SCRIPT_FOLDER}/xd/pokespot.bin"

    with open(XD_ENCOUNTERS, "rb") as f:
        encounters = []
        for i in range(3):
            encounters.append(f.read(36))

    xd = bytes()
    for map_number, encounter in enumerate(encounters):
        xd += map_number.to_bytes(1, "little")
        xd += b"\x00"  # 1 byte padding

        entry = Encounter.from_buffer_copy(encounter)

        for slot in entry.slots:
            xd += POKEMON[slot.specie].to_bytes(2, "little")
            xd += slot.max_level.to_bytes(1, "little")
            xd += slot.min_level.to_bytes(1, "little")

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
