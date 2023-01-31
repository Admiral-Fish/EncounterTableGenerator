import argparse
import os
import pathlib

from Gen3 import gen3
from Gen4 import gen4
from Gen5 import gen5
from Gen8 import gen8

if __name__ == "__main__":
    os.chdir(pathlib.Path(__file__).parent.absolute())

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default=False, action="store_true")
    args = parser.parse_args()

    gen3.create_encounters(args.text)
    gen4.create_encounters(args.text)
    gen5.create_encounters(args.text)
    gen8.create_encounters(args.text)
