#!/usr/bin/env python3
import sys
sys.path.append(".")
from pathlib import Path
from os import remove
from shutil import rmtree, copytree, copy
import subprocess

def gen_uic():
    """生成ui文件的python代码"""
    uic_dir = Path("./uic")
    if not uic_dir.is_dir(): uic_dir.mkdir()
    for ui in Path("./ui").glob("*.ui"):
        with open(f"{uic_dir}/ui_{ui.stem}.py", "w") as uic:
            subprocess.run(["pyside2-uic", ui], stdout=uic)

def compil(debug: bool = False):
    """使用pyinstaller编译源码
    
    Args:
        debug: 使用调试模式。开启后将显示所有输出且不隐藏控制台
    """
    # 编译
    gen_uic()
    args = ["pyinstaller", "--onedir", "--icon=./img/favicon.ico", "./src/main.py"]
    if debug != True:
        args.insert(1, "--windowed")
        args.insert(1, "--log-level=WARN")
    subprocess.run(args)
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

def install(debug: bool = False):
    """使用Inno Setup生成安装程序"""
    compil(debug)
    if Path("./release").is_dir(): rmtree("./release")
    subprocess.run(["ISCC", "./script/installer.iss"])

def run():
    """以python运行程序"""
    gen_uic()
    subprocess.run(["python", "./src/main.py"])

def gen_test_data():
    """生成测试用的数据"""
    from src.data import Data
    s = """\
某君昆仲，今隐其名，皆余昔日在中学时良友；\
分隔多年，消息渐阙。日前偶闻其一大病；适归故乡，迂道往访，则仅晤一人，言病者其弟也。\
劳君远道来视，然已早愈，赴某地候补⑵矣。因大笑，出示日记二册，谓可见当日病状，不妨献诸旧友。\
持归阅一过，知所患盖“迫害狂”之类。语颇错杂无伦次，又多荒唐之言；亦不著月日，惟墨色字体不一，知非一时所书。\
间亦有略具联络者，今撮录一篇，以供医家研究。记中语误，一字不易；惟人名虽皆村人，不为世间所知，无关大体，然亦悉易去。\
至于书名，则本人愈后所题，不复改也。七年四月二日识。\
    """
    try:
        for x in [k for i in s.split("，") for j in i.split("；") for k in j.split("。")]:
            Data().addItem(x, x[::-1])
    except FileExistsError:
        pass

def test():
    """编译后运行, 并生成测试数据"""
    gen_uic()
    compil()
    gen_test_data()
    copytree("./data", "./dist/data")
    subprocess.run(["./dist/main.exe"])
    rmtree("./data")
    rmtree("./dist")


if __name__ == "__main__":
    try:
        eval(f"{sys.argv[1]}()")
    except IndexError:
        run()
