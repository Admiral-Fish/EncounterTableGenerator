from . import bw, bw2

def create_encounters(text: bool):
    bw.encounters(text)

    bw2.encounters(text)
    bw2.hidden_grotto()
