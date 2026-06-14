from . import dp, hgss, pt


def create_encounters(output_dir: str, text: bool):
    hgss.encounters(output_dir, text)
    hgss.bug(output_dir)
    hgss.headbutt(output_dir)
    hgss.safari(output_dir)

    dp.encounters(output_dir, text)
    dp.honey(output_dir)

    pt.encounters(output_dir)
    pt.honey(output_dir)
