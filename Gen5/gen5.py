from . import bw, bw2


def create_encounters(output_dir: str, text: bool):
    bw.encounters(output_dir, text)

    bw2.encounters(output_dir, text)
    bw2.hidden_grotto(output_dir)
