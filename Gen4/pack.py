import io
import struct


def pack_encounter_dppt(encounter: bytes):
    header = bytes()
    body = bytes()
    stream = io.BytesIO(encounter)
    stream.seek(0)

    # Grass
    header += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(12):
        level = struct.unpack("<I", stream.read(4))[0]
        specie = struct.unpack("<I", stream.read(4))[0]

        body += specie.to_bytes(2, "little")
        body += level.to_bytes(1, "little")
        body += b"\x00" # 1 byte padding

    # Swarm
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Noon
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Night
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Radar
    for _ in range(4):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Forms (impacts Shellos/Gastrodon, skipping)
    for _ in range(5):
        stream.read(4)

    # AnnoonTable (used for unown)
    stream.read(4)

    # Ruby
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Sapphire
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Emerald
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Fire Red
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Leaf Green
    for _ in range(2):
        body += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Surf
    header += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        max_level = struct.unpack("<B", stream.read(1))[0]
        min_level = struct.unpack("<B", stream.read(1))[0]
        stream.read(2)
        specie = struct.unpack("<I", stream.read(4))[0]

        body += specie.to_bytes(2, "little")
        body += max_level.to_bytes(1, "little")
        body += min_level.to_bytes(1, "little")

    # Rock smash (no actual rock smash encounters in DPPt)
    stream.read(4)
    for _ in range(5):
        stream.read(8)

    # Old rod
    header += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        max_level = struct.unpack("<B", stream.read(1))[0]
        min_level = struct.unpack("<B", stream.read(1))[0]
        stream.read(2)
        specie = struct.unpack("<I", stream.read(4))[0]

        body += specie.to_bytes(2, "little")
        body += max_level.to_bytes(1, "little")
        body += min_level.to_bytes(1, "little")

    # Good rod
    header += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        max_level = struct.unpack("<B", stream.read(1))[0]
        min_level = struct.unpack("<B", stream.read(1))[0]
        stream.read(2)
        specie = struct.unpack("<I", stream.read(4))[0]

        body += specie.to_bytes(2, "little")
        body += max_level.to_bytes(1, "little")
        body += min_level.to_bytes(1, "little")

    # Super rod
    header += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        max_level = struct.unpack("<B", stream.read(1))[0]
        min_level = struct.unpack("<B", stream.read(1))[0]
        stream.read(2)
        specie = struct.unpack("<I", stream.read(4))[0]

        body += specie.to_bytes(2, "little")
        body += max_level.to_bytes(1, "little")
        body += min_level.to_bytes(1, "little")

    return header + body


def pack_encounter_hgss(encounter: bytes):
    stream = io.BytesIO(encounter)
    stream.seek(0)

    data = stream.read(1) # Grass
    data += stream.read(1) # Surf
    data += stream.read(1) # Rock
    data += stream.read(1) # Old Rod
    data += stream.read(1) # Good Rod
    data += stream.read(1) # Super Rod
    
    stream.read(2)
    data += b"\x00" # 1 byte padding

    # Grass
    levels = []

    # Levels
    for _ in range(12):
        levels.append(stream.read(1))

    # Morning
    for _ in range(12):
        data += stream.read(2)

    # Day
    for _ in range(12):
        data += stream.read(2)

    # Night
    for _ in range(12):
        data += stream.read(2)

    for level in levels:
        data += level

    # Hoenn Radio
    for _ in range(2):
        data += stream.read(2)

    # Sinnoh Radio
    for _ in range(2):
        data += stream.read(2)

    # Surf
    for _ in range(5):
        min_level = stream.read(1)
        max_level = stream.read(1)
        specie = stream.read(2)

        data += specie
        data += max_level
        data += min_level

    # Rock Smash
    for _ in range(5):
        min_level = stream.read(1)
        max_level = stream.read(1)
        specie = stream.read(2)

        data += specie
        data += max_level
        data += min_level

    # Old Rod
    for _ in range(5):
        min_level = stream.read(1)
        max_level = stream.read(1)
        specie = stream.read(2)

        data += specie
        data += max_level
        data += min_level

    # Good Rod
    for _ in range(5):
        min_level = stream.read(1)
        max_level = stream.read(1)
        specie = stream.read(2)

        data += specie
        data += max_level
        data += min_level

    # Super Rod
    for _ in range(5):
        min_level = stream.read(1)
        max_level = stream.read(1)
        specie = stream.read(2)

        data += specie
        data += max_level
        data += min_level

    # Swarm
    for _ in range(4):
        data += stream.read(2)

    return data
