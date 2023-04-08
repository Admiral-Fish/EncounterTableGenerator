from . import emerald, frlg, rs, xd


def create_encounters(text: bool):
    emerald.encounters(text)

    rs.encounters(text)

    frlg.encounters(text)

    xd.encounters(text)
