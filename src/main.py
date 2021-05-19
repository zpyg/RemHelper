# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path
WORKDIR = Path(__file__).parents[1].__str__()
sys.path.append(WORKDIR)
os.chdir(WORKDIR)

from time import strftime, localtime

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QFontDatabase
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

from uic import ui_main
from src.data import Data
from src.editor import MarkdownEditor, InfoEditor


app = QApplication(sys.argv)
# 加载样式表
with open("./ui/style.qss", encoding="utf-8") as f: style = f.read()
app.setStyleSheet(style)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # 设置窗口信息
        self.resize(1200, 100)
        self.setWindowIcon(QIcon("./img/favicon.ico"))
        # 加载字体
        QFontDatabase.addApplicationFont("./font/JetBrainsMono.ttf")
        ## 显示主界面
        self.ui = ui_main.Ui_MainWindow() # 主窗口
        self.ui.setupUi(self)
        self.ui.view.setAlternatingRowColors(True) # 表格交替颜色
        self.data = Data() # 数据
        self.setItems() # 加载所有项
        # 初始化子窗口
        self.create_window = InfoEditor() # 菜单 添加项 子窗口
        self.ui.item_add.triggered.connect(self.create_window.show) # 菜单 添加项 显示
        self.create_window.ui.ok.clicked.connect(self.addItem) # 菜单 添加项 子窗口 确认按钮
        self.create_window.ui.close.clicked.connect(self.create_window.close) # 菜单 添加项 子窗口 退出按钮

        self.ui.item_remove.triggered.connect(self.rmItem) #菜单 删除项 子窗口 确认

        self.change_window = InfoEditor() # 菜单 更改项 子窗口
        self.change_window.ui.ok.clicked.connect(self.changeItem) # 菜单 更改项 子窗口 确认按钮
        self.change_window.ui.close.clicked.connect(self.change_window.close) # 菜单 更改项 子窗口 退出按钮
        self.ui.item_change.triggered.connect(self.change_window_show) # 菜单 更改项 子窗口 显示

        self.markdown_editor = MarkdownEditor() # Markdown 编辑器
        self.ui.content.triggered.connect(self.markdown_editor_show) # Markdown 编辑器 显示
        self.markdown_editor.save.triggered.connect(self.editor_save) # Markdown 编辑器 工具栏 保存按钮
    
    def get_selected_item_info(self):
        row = self.ui.view.currentRow()
        name = self.ui.view.item(row, 0).text()
        desc = self.ui.view.item(row, 3).text()
        return {"row": row, "desc": desc, "name": name}

    def change_window_show(self):
        """显示 菜单 更改项 子窗口"""
        info = self.get_selected_item_info()
        self.change_window.ui.name.setText(info["name"])
        self.change_window.ui.desc.setText(info["desc"])
        self.change_window.show()

    def changeItem(self):
        """菜单 更改项"""
        info = self.get_selected_item_info()
        self.ui.view.removeRow(info["row"])
        new_name = self.change_window.ui.name.text()
        new_desc = self.change_window.ui.desc.text()
        item = self.data.getItem(info["name"])
        item.redesc(new_desc)
        try:
            item.rename(new_name)
        except FileExistsError: pass
        self.setItems()
        self.change_window.close()
    
    def editor_save(self):
        """Markdown 保存"""
        info = self.get_selected_item_info()
        item = self.data.getItem(info["name"])
        content = self.markdown_editor.ui.editor.toPlainText()
        item.write_text(content)

    def markdown_editor_show(self):
        "Markdown 编辑器 显示"
        info = self.get_selected_item_info()
        item = self.data.getItem(info["name"])
        content = item.read_text()
        self.markdown_editor.ui.editor.setPlainText(content)
        self.markdown_editor.ui.browser.setMarkdown(content)
        self.markdown_editor.show()

    def rmItem(self):
        """菜单 删除项"""
        info = self.get_selected_item_info()
        item = self.data.getItem(info["name"])
        choice = QMessageBox.question(self, "确认", f"确认删除 {info['name']} 吗？")
        if choice == QMessageBox.Yes:
            self.ui.view.removeRow(info["row"])
            item.rmitem()

    def addItem(self):
        """菜单 添加项"""
        name = self.create_window.ui.name.text()
        desc = self.create_window.ui.desc.text()
        messagebox = QMessageBox()
        try:
            self.data.addItem(name, desc)
            self.setItems()
            self.create_window.close()
        except ValueError:
            messagebox.critical(self.create_window, "错误", "名称不能为空！")
        except FileExistsError:
            messagebox.critical(self.create_window, "错误", "项目已存在")

    def setItems(self) -> None:
        """加载项目"""
        items = self.data.glob("*")
        items_count = len(items)
        for index in range(items_count):
            info = self.data.getItem(str(items[index])).read_info()
            # 不插入多余行
            if self.ui.view.rowCount() < items_count:
                self.ui.view.insertRow(index)
            # 名称
            name = QTableWidgetItem(info["name"])
            name.setTextAlignment(Qt.AlignCenter) # 居中
            self.ui.view.setItem(index, 0, name)
            self.ui.view.setColumnWidth(0, 150)
            # 记忆量
            forget_percent = QTableWidgetItem(str(info["fgpct"]) + "%")
            forget_percent.setTextAlignment(Qt.AlignCenter)
            self.ui.view.setItem(index, 1, forget_percent)
            self.ui.view.setColumnWidth(1, 80)
            # 创建时间
            creat_time = strftime("%Y-%m-%d %T", localtime(info["ctime"]))
            creat_time = QTableWidgetItem(creat_time)
            creat_time.setTextAlignment(Qt.AlignCenter)
            self.ui.view.setItem(index, 2, creat_time)
            self.ui.view.setColumnWidth(2, 200)
            # 说明
            desc =  QTableWidgetItem(info["desc"])
            self.ui.view.setItem(index, 3, desc)

window = MainWindow()
window.setWindowTitle("RemHelper")
window.show()
app.exec_()
