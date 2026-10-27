#!/usr/bin/env python3
"""Copy bundled eval notes to a new disposable vault; never overwrite a vault."""
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--destination", required=True, help="New, nonexistent disposable vault directory")
args = parser.parse_args()
destination = Path(args.destination).expanduser().resolve()
if destination.exists():
    parser.error("Destination already exists; choose a new disposable directory.")
source = Path(__file__).resolve().parent / "fixtures" / "vault"
shutil.copytree(source, destination)
for folder in []:
    (destination / folder).mkdir(exist_ok=True)
print(destination)
