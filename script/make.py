#!/usr/bin/env python3
from pathlib import Path
import sys
from os import remove
from shutil import rmtree, copytree, copy
from subprocess import run

sys.path.append(".")
### make ###
from script import gen_uic
run(["pyinstaller",
    "--windowed", "--onedir",
    "--icon=./img/favicon.ico",
    "--log-level=WARN",
    "./src/main.py"])
### copy file ###
Path("./dist/main").rename("./dist_")
rmtree("./dist")
Path("./dist_").rename("./dist")

Path("./dist/ui").mkdir()
copy("./ui/style.qss", "./dist/ui/style.qss")

copytree("./font", "./dist/font")
Path("./dist/data").mkdir()

copytree("./img", "./dist/img")
### clean ###
rmtree("./build")
remove("./main.spec")