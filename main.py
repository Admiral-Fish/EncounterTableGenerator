from Gen3 import gen3
from Gen4 import dp, hgss, pt

if __name__ == "__main__":
    # Gen 3 tables
    gen3.emerald()
    gen3.rs()
    gen3.frlg()

    # Gen 4 tables
    dp.encounters()
    pt.encounters()
    hgss.encounters()
    hgss.bug()
