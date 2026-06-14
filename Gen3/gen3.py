from . import emerald, frlg, rs, xd


def create_encounters(output_dir: str, text: bool):
    emerald.encounters(output_dir, text)

    rs.encounters(output_dir, text)

    frlg.encounters(output_dir, text)

    xd.encounters(output_dir, text)
