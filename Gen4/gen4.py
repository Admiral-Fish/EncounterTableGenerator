from . import dp, hgss, pt


def create_encounters(text: bool):
    hgss.encounters(text)
    hgss.bug()
    hgss.headbutt()
    hgss.safari()

    dp.encounters(text)
    dp.honey()

    pt.encounters()
    pt.honey()
