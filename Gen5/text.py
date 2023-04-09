import os
import struct

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def read_map_names(path):
    file = open(path, "rb")

    main_key = 31881
    name_sections, = struct.unpack("<H", file.read(2))
    name_count, = struct.unpack("<H", file.read(2))

    section_size, = struct.unpack("<I", file.read(4))
    file.read(4)

    section_offset, = struct.unpack("<I", file.read(4))

    map_names = []
    for i in range(name_count):
        file.seek(section_offset)
        section_size, = struct.unpack("<I", file.read(4))

        file.seek(i * 8, 1)
        string_offset, = struct.unpack("<I", file.read(4))
        string_size, = struct.unpack("<H", file.read(2))
        string_unknown, = struct.unpack("<H", file.read(2))

        file.seek(section_offset + string_offset)
        text = ""
        key = main_key
        for j in range(string_size):
            char = struct.unpack("<H", file.read(2))[0] ^ key
            if char == 0xffff:
                pass
            elif char == 0xf100:
                text += "\xf100"
            elif char == 0xfffe:
                text += "\n"
            elif char > 20 and char <= 0xfff0 and char != 0xf000:
                text += chr(char)
            else:
                text += chr(char)

            key = ((key << 3) | (key >> 13)) & 0xffff

        main_key += 0x2983
        if main_key > 0xffff:
            main_key -= 0x10000

        map_names.append(text)

    return map_names
