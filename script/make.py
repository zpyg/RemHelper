#!/usr/bin/env python3
import sys
sys.path.append(".")

from pathlib import Path
from os import remove
from shutil import rmtree, copytree, copy
import subprocess

PYINSTALLER_ARGS = [
    "--onedir",
    "--icon=./img/favicon.ico",
    "--windowed",
    "--log-level=WARN"
]


def gen_uic():
    """生成ui文件的python代码"""
    import subprocess
    uic_dir = Path("./uic")
    if not uic_dir.is_dir(): uic_dir.mkdir()
    for ui in Path("./ui").glob("*.ui"):
        with open(f"{uic_dir}/ui_{ui.stem}.py", "w") as uic:
            subprocess.run(["pyside2-uic", ui], stdout=uic)


def compil():
    """使用pyinstaller编译源码"""
    # 编译
    gen_uic()
    subprocess.run(["pyinstaller", *PYINSTALLER_ARGS, "./src/main.py"])
    # 调整目录结构
    Path("./dist/main").rename("./dist_")
    rmtree("./dist")
    rmtree("./build")
    remove("./main.spec")
    Path("./dist_").rename("./dist")
    # 复制需要文件
    Path("./dist/ui").mkdir()
    copy("./ui/style.qss", "./dist/ui/style.qss")
    copytree("./font", "./dist/font")
    copytree("./img", "./dist/img")


def install():
    """使用Inno Setup生成安装程序"""
    compil()
    if Path("./release").is_dir(): rmtree("./release")
    subprocess.run(["ISCC", "./script/installer.iss"])


def run():
    """运行程序"""
    gen_uic()
    subprocess.run(["python", "./src/main.py"])


def gen_test_data():
    """生成测试数据"""
    from src.data import Item
    from faker import Faker
    from time import time
    from random import uniform
    faker = Faker(locale="zh_CN")
    for _ in range(128):
        item = Item(faker.word() + faker.user_name() + faker.word())
        item.mkitem(faker.sentence())
        info = item.read_info()
        now = time()
        info["ctime"] = uniform(now-604800, now)
        item.write_info(info)


def test():
    """编译后运行, 并生成测试数据"""
    gen_uic()
    compil()
    gen_test_data()
    copytree("./data", "./dist/data")
    subprocess.run(["./dist/main.exe"])
    rmtree("./data")
    rmtree("./dist")


def clean():
    """删除非必须目录"""
    rmtree("./data", ignore_errors=True)
    rmtree("./uic", ignore_errors=True)
    rmtree("./dist", ignore_errors=True)
    rmtree("./release", ignore_errors=True)
    rmtree("./data", ignore_errors=True)
    rmtree("./src/__pycache__", ignore_errors=True)


__doc__ = f"""\
run {run.__doc__}
test {test.__doc__}
compil {compil.__doc__}
install {install.__doc__}
gen_uic {gen_uic.__doc__}
gen_test_data {gen_test_data.__doc__}
clean {clean.__doc__}
"""
if __name__ == "__main__":
    try:
        eval(f"{sys.argv[1]}()")
    except IndexError:
        run()
    except NameError:
        print(__doc__)
