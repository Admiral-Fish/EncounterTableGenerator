from ctypes import Structure, c_uint8, c_uint16


class DynamicSlot(Structure):
    _fields_ = [
        ("specie", c_uint16),
        ("min_level", c_uint8),
        ("max_level", c_uint8)
    ]


class StaticSlot(Structure):
    _fields_ = [
        ("specie", c_uint16),
        ("level", c_uint8)
    ]


class EncounterSeason(Structure):
    _fields_ = [
        ("grassRate", c_uint8),
        ("grassDoubleRate", c_uint8),
        ("grassSpecialRate", c_uint8),
        ("surfRate", c_uint8),
        ("surfSpecialRate", c_uint8),
        ("fishRate", c_uint8),
        ("fishSpecialRate", c_uint8),
        ("grass", StaticSlot * 12),
        ("grassDouble", StaticSlot * 12),
        ("grassSpecial", StaticSlot * 12),
        ("surf", DynamicSlot * 5),
        ("surfSpecial", DynamicSlot * 5),
        ("fish", DynamicSlot * 5),
        ("fishSpecial", DynamicSlot * 5),
    ]


class Encounter(Structure):
    _fields_ = [
        ("seasons", EncounterSeason * 1)
    ]


class EncounterSeasons(Structure):
    _fields_ = [
        ("seasons", EncounterSeason * 4)
    ]


class Phenomenon:
    NONE = 0
    BRIDGE = 1
    CAVE = 2
    GRASS = 3
    WATER = 4


phenomenonBW = {
    3   : Phenomenon.GRASS,  # Dreamyard Ruins
    5   : Phenomenon.GRASS,  # Pinwheel Forest (Exterior)
    6   : Phenomenon.GRASS,  # Pinwheel Forest (Interior)
    40  : Phenomenon.GRASS,  # Cold Storage
    41  : Phenomenon.CAVE,   # Chargestone Cave 1F
    42  : Phenomenon.CAVE,   # Chargestone Cave B1F
    43  : Phenomenon.CAVE,   # Chargestone Cave B2F
    44  : Phenomenon.CAVE,   # Twist Mountain (Upper Level)
    45  : Phenomenon.CAVE,   # Twist Mountain (Middle Level)
    46  : Phenomenon.CAVE,   # Twist Mountain (Lower Level)
    47  : Phenomenon.CAVE,   # Twist Mountain (Lowest Level)
    48  : Phenomenon.GRASS,  # Dragonspiral Tower (Entrance)
    49  : Phenomenon.GRASS,  # Dragonspiral Tower (Outside)
    53  : Phenomenon.CAVE,   # Victory Road 1F (Middle)
    54  : Phenomenon.CAVE,   # Victory Road 2F (Left)
    55  : Phenomenon.CAVE,   # Victory Road 3F (Middle)
    56  : Phenomenon.CAVE,   # Victory Road 4F (Middle)
    57  : Phenomenon.CAVE,   # Victory Road 2F (Right)
    58  : Phenomenon.CAVE,   # Victory Road 1F (Right)
    59  : Phenomenon.CAVE,   # Victory Road 3F (Right)
    60  : Phenomenon.CAVE,   # Victory Road 1F (Left)
    61  : Phenomenon.CAVE,   # Victory Road 3F (Left)
    62  : Phenomenon.CAVE,   # Victory Road 4F (Left)
    63  : Phenomenon.CAVE,   # Victory Road 5F
    64  : Phenomenon.CAVE,   # Victory Road 6F
    65  : Phenomenon.CAVE,   # Victory Road 4F (Right)
    66  : Phenomenon.CAVE,   # Victory Road 7F
    67  : Phenomenon.CAVE,   # Trial Chamber
    68  : Phenomenon.GRASS,  # Giant Chasm (Entrance)
    69  : Phenomenon.CAVE,   # Giant Chasm (Cave)
    70  : Phenomenon.GRASS,  # Giant Chasm (Crater Forest)
    71  : Phenomenon.CAVE,   # Giant Chasm (Cave Depths)
    72  : Phenomenon.GRASS,  # P2 Laboratory
    74  : Phenomenon.BRIDGE, # Driftveil Drawbridge
    75  : Phenomenon.GRASS,  # Village Bridge
    76  : Phenomenon.BRIDGE, # Marvelous Bridge
    77  : Phenomenon.GRASS,  # Route 1
    78  : Phenomenon.GRASS,  # Route 2
    79  : Phenomenon.GRASS,  # Route 3
    80  : Phenomenon.CAVE,   # Wellspring Cave 1F
    81  : Phenomenon.CAVE,   # Wellspring Cave B1F
    83  : Phenomenon.GRASS,  # Route 5
    84  : Phenomenon.GRASS,  # Route 6
    85  : Phenomenon.CAVE,   # Mistralton Cave 1F
    86  : Phenomenon.CAVE,   # Mistralton Cave 2F
    87  : Phenomenon.CAVE,   # Guidance Chamber
    88  : Phenomenon.GRASS,  # Route 7
    95  : Phenomenon.GRASS,  # Route 9
    96  : Phenomenon.CAVE,   # Challenger's Cave 1F
    97  : Phenomenon.CAVE,   # Challenger's Cave B1F
    98  : Phenomenon.CAVE,   # Challenger's Cave B2F
    99  : Phenomenon.GRASS,  # Route 10
    100 : Phenomenon.GRASS,  # Route 10 (Basic Badge Gate)
    101 : Phenomenon.GRASS,  # Route 11
    102 : Phenomenon.GRASS,  # Route 12
    103 : Phenomenon.GRASS,  # Route 13
    104 : Phenomenon.GRASS,  # Route 14
    105 : Phenomenon.GRASS,  # Abundant Shrine
    106 : Phenomenon.GRASS,  # Route 15
    107 : Phenomenon.GRASS,  # Route 16
    108 : Phenomenon.GRASS,  # Lostlorn Forest
    109 : Phenomenon.GRASS,  # Route 18
}


phenomenonBW2 = {
	1   : Phenomenon.GRASS,  # Castelia City
	6   : Phenomenon.GRASS,  # Dreamyard (Ruins)
	8   : Phenomenon.GRASS,  # Pinwheel Forst (Exterior)
	9   : Phenomenon.GRASS,  # Pinwheel Forst (Interior)
	20  : Phenomenon.CAVE,   # Chargestone Cave 1F
	21  : Phenomenon.CAVE,   # Chargestone Cave B1F
	22  : Phenomenon.CAVE,   # Chargestone Cave B2F
	23  : Phenomenon.CAVE,   # Twist Mountain (Upper Level)
	24  : Phenomenon.CAVE,   # Twist Mountain (Middle Level)
	25  : Phenomenon.CAVE,   # Twist Mountain (Lower Level)
	26  : Phenomenon.CAVE,   # Twist Mountain (Lowest Level)
	27  : Phenomenon.GRASS,  # Dragonspiral Tower (Entrance)
	28  : Phenomenon.GRASS,  # Dragonspiral Tower (Outside)
	31  : Phenomenon.CAVE,   # Victory Road 4F
	32  : Phenomenon.GRASS,  # Giant Chasm (Entrance)
	33  : Phenomenon.CAVE,   # Giant Chasm (Cave)
	34  : Phenomenon.GRASS,  # Giant Chasm (Crater Forest)
	36  : Phenomenon.CAVE,   # Giant Chasm (Cave Depths)
	42  : Phenomenon.GRASS,  # P2 Laboratory
	45  : Phenomenon.GRASS,  # Floccesy Ranch
	46  : Phenomenon.GRASS,  # Virbank Complex (Entrance)
	47  : Phenomenon.GRASS,  # Virbank Complex (Inside)
	48  : Phenomenon.GRASS,  # Reversal Mountain
	49  : Phenomenon.CAVE,   # Reversal Mountain 1F
	50  : Phenomenon.CAVE,   # Reversal Mountain B1F
	52  : Phenomenon.CAVE,   # Reversal Mountain B1F (Chamber)
	72  : Phenomenon.GRASS,  # Victory Road (Grove)
	73  : Phenomenon.GRASS,  # Victory Road (Outside 1)
	74  : Phenomenon.CAVE,   # Victory Road 2F
	75  : Phenomenon.CAVE,   # Victory Road 2F (Back)
	76  : Phenomenon.GRASS,  # Victory Road (Outside 2)
	77  : Phenomenon.CAVE,   # Victory Road 3F
	80  : Phenomenon.CAVE,   # Victory Road 3F (Back)
	81  : Phenomenon.CAVE,   # Relic Passage (Castelia City Exit)
	82  : Phenomenon.CAVE,   # Relic Passage (Middle)
	83  : Phenomenon.CAVE,   # Relic Passage (Driftveil City Exit)
	85  : Phenomenon.CAVE,   # Clay Tunnel
	87  : Phenomenon.CAVE,   # Underground Ruins
	90  : Phenomenon.CAVE,   # Rock Peak Chamber
	91  : Phenomenon.CAVE,   # Iceberg Chamber
	92  : Phenomenon.CAVE,   # Iron Chamber
	93  : Phenomenon.CAVE,   # Seaside Cave 1F
	94  : Phenomenon.CAVE,   # Seaside Cave B1F
	95  : Phenomenon.GRASS,  # Nature Preserve
	96  : Phenomenon.BRIDGE, # Driftveil Drawbridge
	97  : Phenomenon.GRASS,  # Village Bridge
	98  : Phenomenon.BRIDGE, # Marvelous Bridge
	99  : Phenomenon.GRASS,  # Route 1
	100 : Phenomenon.GRASS,  # Route 2
	101 : Phenomenon.GRASS,  # Route 3
	102 : Phenomenon.CAVE,   # Wellspring Cave 1F
	103 : Phenomenon.CAVE,   # Wellspring Cave B1F
	106 : Phenomenon.GRASS,  # Route 5
	107 : Phenomenon.GRASS,  # Route 6
	108 : Phenomenon.CAVE,   # Mistralton Cave 1F
	109 : Phenomenon.CAVE,   # Mistralton Cave B1F
	110 : Phenomenon.CAVE,   # Guidance Chamber
	111 : Phenomenon.GRASS,  # Route 7
	118 : Phenomenon.GRASS,  # Route 9
	119 : Phenomenon.GRASS,  # Route 11
	120 : Phenomenon.GRASS,  # Route 12
	121 : Phenomenon.GRASS,  # Route 13
	122 : Phenomenon.GRASS,  # Route 14
	123 : Phenomenon.GRASS,  # Abundant Shrine
	124 : Phenomenon.GRASS,  # Route 15
	125 : Phenomenon.GRASS,  # Route 16
	126 : Phenomenon.GRASS,  # Lostlorn Forest
	127 : Phenomenon.GRASS,  # Route 18
	128 : Phenomenon.GRASS,  # Route 19
	129 : Phenomenon.GRASS,  # Route 20
	130 : Phenomenon.GRASS,  # Route 22
	131 : Phenomenon.GRASS,  # Route 23
}


def pack_encounter_gen5(location: int, bw: bool, encounter: bytes):
    if len(encounter) == 232:
        entry = Encounter.from_buffer_copy(encounter)
    else:
        entry = EncounterSeasons.from_buffer_copy(encounter)

    data = location.to_bytes(1, "little")
    data += len(entry.seasons).to_bytes(1, "little")
    if bw:
        data += phenomenonBW.get(location, 0).to_bytes(1, "little")
    else:
        data += phenomenonBW2.get(location, 0).to_bytes(1, "little")
    data += b"\x00" # 1 byte padding

    for season in entry.seasons:
        data += season.grassRate.to_bytes(1, "little")
        data += season.grassDoubleRate.to_bytes(1, "little")
        data += season.grassSpecialRate.to_bytes(1, "little")
        data += season.surfRate.to_bytes(1, "little")
        data += season.surfSpecialRate.to_bytes(1, "little")
        data += season.fishRate.to_bytes(1, "little")
        data += season.fishSpecialRate.to_bytes(1, "little")
        data += b"\x00"  # 1 byte padding

        # Grass
        for slot in season.grass:
            data += slot.specie.to_bytes(2, "little")
            data += slot.level.to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding

        # Grass Double
        for slot in season.grassDouble:
            data += slot.specie.to_bytes(2, "little")
            data += slot.level.to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding

        # Grass Special
        for slot in season.grassSpecial:
            data += slot.specie.to_bytes(2, "little")
            data += slot.level.to_bytes(1, "little")
            data += b"\x00"  # 1 byte padding

        # Surf
        for slot in season.surf:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

        # Surf Special
        for slot in season.surfSpecial:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

        # Fish
        for slot in season.fish:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

        # Fish Special
        for slot in season.fishSpecial:
            data += slot.specie.to_bytes(2, "little")
            data += slot.max_level.to_bytes(1, "little")
            data += slot.min_level.to_bytes(1, "little")

    return data
