#!/usr/bin/env python3
from pathlib import Path
from os import system

uic_dir = Path("./uic")
if not uic_dir.is_dir():
    uic_dir.mkdir()

for ui in Path("./ui").glob("*.ui"):
    system(f"pyside2-uic {ui} > uic/ui_{ui.stem}.py")