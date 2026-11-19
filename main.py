#!/usr/bin/env python3
"""news-image-20261118 entry: write the day's front page to the output.

The image (entry.png) is drawn by make_image.py in this repository and
sums up the world news of Wednesday 18 November 2026. This program writes
the same bytes on every run: it copies the file, nothing else, with no
network and no randomness.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
