# -*- coding: utf-8 -*-
from json import dumps, loads
from pathlib import Path
from shutil import rmtree
from time import localtime, strftime, time
from typing import List

from PySide2.QtWidgets import QMessageBox, QTableWidgetItem


DATA_DIR = Path("./data")
if not DATA_DIR.is_dir(): DATA_DIR.mkdir()

class Item:
    """数据项类"""
    def __init__(self, name):
        self.name = name

        self._home = Path(DATA_DIR, self.name)
        self._info_file = Path(self._home, "info.json")
        self._text_file = Path(self._home, "content.md")

    def __str__(self):
        return self.name

    def mkitem(self, desc=""):
        info = {
            "name": self.name,  # 名称
            "desc": desc,  # 说明
            "ctime": time(),  # 创建时间
        }
        self._home.mkdir()
        self.write_info(info)
        self.write_text("")
        
    def rmitem(self):
        rmtree(self._home)

    def rename(self, new_name: str):
        # 创建新项目
        item = Item(new_name)
        item.mkitem()
        # 迁移原项目信息
        info = self.read_info()
        info["name"] = new_name
        item.write_info(info)
        item.write_text("")
        # 删除原项目目录
        self.rmitem()
        # 更新类属性
        self.__init__(new_name)

    def redesc(self, desc):
        info = self.read_info()
        info["desc"] = desc
        self.write_info(info)

    def write_info(self, info: dict):
        self._info_file.write_text(dumps(info), encoding="utf-8")

    def read_info(self):
        info = loads(self._info_file.read_text(encoding="utf-8"))
        # 使用遗忘曲线解析式求出近似记忆百分比
        # 解析式源于百度百科: https://baike.baidu.com/item/遗忘曲线#1
        past_second = time() - info["ctime"]
        past_hour = past_second / 60**2
        forget_percent = (1 - 0.56 * past_hour**0.06) * 100
        info["fgpct"] = round(forget_percent, 2) if forget_percent >= 0 else 0
        return info

    def write_text(self, text: str):
        self._text_file.write_text(text, encoding="utf-8")

    def read_text(self):
        return self._text_file.read_text(encoding="utf-8")


class Data:
    """数据操作类"""
    def __init__(self, window) -> None:
        self.window = window

    def setItems(self):
        """刷新数据"""
        items = [Item(item.name) for item in DATA_DIR.glob("*")]
        item_count = len(items)
        self.window.ui.view.setRowCount(item_count)  # 根据项目数设定行数
        for index in range(item_count):
            info = Item(str(items[index])).read_info()
            # 名称
            name = QTableWidgetItem(info["name"])
            self.window.ui.view.setItem(index, 0, name)
            # 记忆量
            forget_percent = QTableWidgetItem(str(info["fgpct"]) + "%")
            self.window.ui.view.setItem(index, 1, forget_percent)
            # 创建时间
            creat_time = strftime("%Y-%m-%d %T", localtime(info["ctime"]))
            creat_time = QTableWidgetItem(creat_time)
            self.window.ui.view.setItem(index, 2, creat_time)
            # 说明
            desc = QTableWidgetItem(info["desc"])
            self.window.ui.view.setItem(index, 3, desc)

    def getCurrent(self):
        """获取选中的索引和项目"""
        row = self.window.ui.view.currentRow()
        item = Item(self.window.ui.view.item(row, 0).text())
        return {"row": row, "item": item}

    def addItem(self) -> Item:
        """槽: 菜单 添加项 窗口 确认"""
        name = self.window.add_window.ui.name.text()
        desc = self.window.add_window.ui.desc.text()
        item = Item(name)
        messagebox = QMessageBox()
        try:
            item.mkitem(desc)
            self.window.add_window.close()
            self.setItems()
        except FileExistsError:
            messagebox.critical(self.window.add_window, "错误", "项目已存在")        

    def rmItem(self):
        """槽: 菜单 删除项"""
        current = self.getCurrent()
        choice = QMessageBox.question(self.window, "确认", "确认删除？", defaultButton=QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.window.ui.view.removeRow(current["row"])
            current["item"].rmitem()
            self.setItems()

    def chItem(self):
        current = self.getCurrent()
        new_desc = self.window.change_window.ui.desc.text()
        current["item"].redesc(new_desc)
        try:
            new_name = self.window.change_window.ui.name.text()  
            if new_name != str(current["item"]):
                current["item"].rename(new_name)
                self.window.ui.view.removeRow(current["row"])
        except FileExistsError:  # 名称未变更
            pass
        self.setItems()
        self.window.change_window.close()
