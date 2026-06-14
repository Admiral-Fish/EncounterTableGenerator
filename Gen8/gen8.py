from . import bdsp


def create_encounters(output_dir: str, text: bool):
    bdsp.encounters(output_dir, text)
    bdsp.honey(output_dir)
    bdsp.underground(output_dir)
