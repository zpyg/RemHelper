# -*- coding: utf-8 -*-
from json import dumps, loads
from pathlib import Path
from shutil import rmtree
from time import time
from typing import List


class Item:
    """数据项类"""
    def __init__(self, home: Path):
        self.__root = home.parent
        self.__home = home
        self.__info_file = Path(home, "info.json")
        self.__text_file = Path(home, "content.md")

    def __str__(self):
        return self.__home.name

    def mkitem(self):
        self.__home.mkdir()

    def rmitem(self):
        rmtree(self.__home)

    def rename(self, target: str):
        # 创建新项目
        item = Item(Path(self.__root, target))
        item.mkitem()
        # 迁移原项目信息
        info = self.read_info()
        info["name"] = target
        item.write_info(info)
        item.write_text("")
        # 删除原项目
        self.rmitem()
        # 返回新的 Item 对象
        return item

    def redesc(self, desc):
        info = self.read_info()
        info["desc"] = desc
        self.write_info(info)

    def write_info(self, info: dict):
        self.__info_file.write_text(dumps(info), encoding="utf-8")

    def read_info(self):
        info = loads(self.__info_file.read_text(encoding="utf-8"))
        # 使用遗忘曲线解析式求出近似记忆百分比
        # 解析式源于百度百科: https://baike.baidu.com/item/遗忘曲线#1
        past_second = time() - info["ctime"]
        past_hour = past_second / 60**2
        forget_percent = (1 - 0.56 * past_hour**0.06) * 100
        info["fgpct"] = round(forget_percent, 2) if forget_percent >= 0 else 0
        return info

    def write_text(self, text: str):
        self.__text_file.write_text(text, encoding="utf-8")

    def read_text(self):
        return self.__text_file.read_text(encoding="utf-8")


class Data:
    """数据操作类"""
    def __init__(self) -> None:
        self.__root = Path("./data")
        if not self.__root.is_dir():
            self.__root.mkdir()

    def getItem(self, name: str) -> Item:
        """获取项目对象"""
        return Item(Path(self.__root, name))

    def addItem(self, name: str, desc: str = None) -> Item:
        """添加项目"""
        info = {
            "name": name,  # 名称
            "desc": desc,  # 说明
            "ctime": time(),  # 创建时间
        }
        item = self.getItem(name)
        item.mkitem()
        item.write_info(info)
        item.write_text("")
        return item

    def glob(self, pattern: str) -> List[Item]:
        """使用 glob pattern 搜索"""
        return [Item(item) for item in self.__root.glob(pattern)]
