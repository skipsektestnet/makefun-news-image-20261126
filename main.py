"""Entrypoint: copy the pre-drawn entry.png to the output directory.

Stdlib only, no network, deterministic: the same bytes every run.
The image is drawn by generate.py and shipped in this repository.
"""

import os
import shutil

ENTRY = "entry.png"
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, ENTRY),
                    os.path.join(out_dir, ENTRY))


if __name__ == "__main__":
    main()
