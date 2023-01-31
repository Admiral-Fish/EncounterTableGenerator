from . import emerald, rs, frlg, xd

def create_encounters(text: bool):
    emerald.encounters(text)

    rs.encounters(text)

    frlg.encounters(text)

    xd.encounters(text)
