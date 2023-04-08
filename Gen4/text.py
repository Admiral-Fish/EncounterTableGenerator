import json
import os
import struct

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

def read_map_names(path):
    file = open(path, "rb")

    with open(f"{SCRIPT_FOLDER}/characters.json", "r", encoding="utf-8") as f:
        characters = json.load(f)

    string_count, = struct.unpack("<H", file.read(2))
    initial_key, = struct.unpack("<H", file.read(2))

    key1 = (initial_key * 0x2fd) & 0xffff
    key2 = 0
    real_key = 0
    special_char_on = False

    current_offset = []
    current_size = []

    for i in range(string_count):
        key2 = (key1 * (i + 1)) & 0xffff
        real_key = key2 | (key2 << 16)
        current_offset.append(struct.unpack("<I", file.read(4))[0] ^ real_key)
        current_size.append(struct.unpack("<I", file.read(4))[0] ^ real_key)

    map_names = []
    for i in range(string_count):
        key1 = (0x91bd3 * (i + 1)) & 0xffff
        file.seek(current_offset[i])

        text = ""
        for _ in range(current_size[i]):
            char = struct.unpack("<H", file.read(2))[0] ^ key1

            if char == 0xe000:
                text += "\n"
            elif char == 0x25bc:
                text += "\r"
            elif char == 0x25bd:
                text += "\f"
            elif char == 0xfffe:
                text += "\v"
                special_char_on = True
            elif char == 0xffff:
                text += ""
            else:
                if special_char_on:
                    text += ":4X".format(char)
                    special_char_on = False
                else:
                    text += characters[str(char)]

            key1 += 0x493d
            key1 &= 0xffff

        map_names.append(text)

    return map_names
