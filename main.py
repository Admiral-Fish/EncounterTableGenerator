#!/usr/bin/env python3

import argparse
import os
import pathlib

from Gen3 import gen3
from Gen4 import gen4
from Gen5 import gen5
from Gen8 import gen8

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=str)
    parser.add_argument("output_stamp", type=str)
    parser.add_argument("--text", default=False, action="store_true")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    gen3.create_encounters(args.output_dir, args.text)
    gen4.create_encounters(args.output_dir, args.text)
    gen5.create_encounters(args.output_dir, args.text)
    gen8.create_encounters(args.output_dir, args.text)

    stamp = pathlib.Path(args.output_stamp)
    stamp.touch()
