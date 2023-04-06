import io
import struct

def pack_encounter_gen5(encounter: bytes):
    data = bytes()
    stream = io.BytesIO(encounter)
    stream.seek(0)    

    seasons = int(len(encounter) / 232)
    data += seasons.to_bytes(1, byteorder="little")

    for season in range(seasons):
        data += stream.read(1) # Grass rate
        data += stream.read(1) # Grass double rate
        data += stream.read(1) # Grass special rate
        data += stream.read(1) # Surf rate
        data += stream.read(1) # Surf special rate
        data += stream.read(1) # Fish rate
        data += stream.read(1) # Fish special rate
        stream.read(1) # pad

        # Grass
        for _ in range(12):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            level = stream.read(1)
            stream.read(1) # pad

            data += specie
            data += level
            data += b"\x00" # 1 byte padding

        # Grass Double
        for _ in range(12):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            level = stream.read(1)
            stream.read(1) # pad

            data += specie
            data += level
            data += b"\x00" # 1 byte padding

        # Grass Special
        for _ in range(12):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            level = stream.read(1)
            stream.read(1) # pad

            data += specie
            data += level
            data += b"\x00" # 1 byte padding

        # Surf
        for _ in range(5):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            min_level = stream.read(1)
            max_level = stream.read(1)

            data += specie
            data += max_level
            data += min_level

        # Surf Special
        for _ in range(5):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            min_level = stream.read(1)
            max_level = stream.read(1)

            data += specie
            data += max_level
            data += min_level

        # Fish
        for _ in range(5):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            min_level = stream.read(1)
            max_level = stream.read(1)

            data += specie
            data += max_level
            data += min_level

        # Fish Special
        for _ in range(5):
            specie = struct.unpack("<H", stream.read(2))[0].to_bytes(2, "little")
            min_level = stream.read(1)
            max_level = stream.read(1)

            data += specie
            data += max_level
            data += min_level

    return data
