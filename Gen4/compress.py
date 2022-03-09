import io
import struct


def compress_encounter_dppt(encounter: bytes):
    data = bytes()
    stream = io.BytesIO(encounter)
    stream.seek(0)

    # Grass
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(12):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Morning
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Day
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Night
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Radar
    for _ in range(4):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Forms TODO: what does this mean
    for _ in range(5):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # TODO: what does this mean
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Ruby
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Sapphire
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Emerald
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Fire Red
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Leaf Green
    for _ in range(2):
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Surf
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        stream.read(2)
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Rock smash
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        stream.read(2)
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Old rod
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        stream.read(2)
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Good rod
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        stream.read(2)
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    # Super rod
    data += struct.unpack("<I", stream.read(4))[0].to_bytes(1, "little")
    for _ in range(5):
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        data += struct.unpack("<B", stream.read(1))[0].to_bytes(1, "little")
        stream.read(2)
        data += struct.unpack("<I", stream.read(4))[0].to_bytes(2, "little")

    return data


def compress_encounter_hgss(encounter: bytes):
    stream = io.BytesIO(encounter)
    stream.seek(0)

    data = stream.read(6)
    stream.read(2)
    data += stream.read()

    return data
