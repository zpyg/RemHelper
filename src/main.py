# -*- coding: utf-8 -*-
# 将工作目录添加到环境变量
import sys
sys.path.append(".")
# 海龟编辑器时使用，可从其他工作目录切换至正常工作目录
# import sys
# import os
# from pathlib import Path
# WORKDIR = Path(__file__).parents[1].__str__()
# sys.path.append(WORKDIR)
# os.chdir(WORKDIR)

from os import startfile

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QFontDatabase
from PySide2.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QMessageBox

from uic import ui_main
from src.data import Data
from src.editor import MarkdownEditor, InfoEditor, FindEditor


APP = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # 加载UI
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        # 加载数据
        self.data = Data(self)
        self.data.setItems()
        # 绑定槽函数
        ## 数据.添加项
        self.add_window = InfoEditor()
        self.ui.item_add.triggered.connect(self.add_window.show)  # 显示窗口
        self.add_window.ui.ok.clicked.connect(self.data.addItem)  # (窗口) 确认
        self.add_window.ui.close.clicked.connect(self.add_window.close)  # (窗口) 关闭
        ## 数据.删除项
        self.ui.item_remove.triggered.connect(self.data.rmItem)
        ## 编辑.信息
        self.change_window = InfoEditor()
        self.ui.item_change.triggered.connect(self.chitem_show) # 显示窗口
        self.change_window.ui.ok.clicked.connect(self.data.chItem) # (窗口) 确认
        self.change_window.ui.close.clicked.connect(self.change_window.close) # (窗口) 关闭
        ## 编辑.内容
        self.markdown_editor = MarkdownEditor()
        self.ui.content.triggered.connect(self.markdown_editor_show) # 显示窗口
        self.markdown_editor.ui.open.triggered.connect(self.markdown_editor_open)
        self.markdown_editor.ui.save.triggered.connect(self.markdown_editor_save)
        self.markdown_editor.ui.view.triggered.connect(self.markdown_editor_view)
        ## 查找.排序
        self.ui.sort.triggered.connect(self.item_sort)
        ## 查找.搜索
        self.search_window = FindEditor()
        self.ui.search.triggered.connect(self.search_window.show)
        self.search_window.ui.submit.clicked.connect(self.item_find)

    def item_find(self):
        messagebox = QMessageBox()
        kwd = self.search_window.ui.input.text()
        rst = self.ui.view.findItems(kwd, Qt.MatchContains)
        cnt = len(rst)
        messagebox.information(self.search_window, "结果", f"找到{cnt}个结果")
        for i in range(cnt):
            item = rst[i]
            self.ui.view.setItemSelected(item, True)
            self.ui.view.verticalScrollBar().setSliderPosition(item.row())
            choice = messagebox.question(self.search_window, "浏览", f"当前结果({i}/{cnt}), 是否继续?")
            if choice == QMessageBox.No:
                break
            self.ui.view.setItemSelected(item, True)
        self.search_window.close()

    def item_sort(self):
        self.ui.view.sortItems(1, Qt.AscendingOrder) # 以记忆量升序排列

    def chitem_show(self):
        info = self.data.getCurrent()["item"].read_info()
        self.change_window.ui.name.setText(info["name"])
        self.change_window.ui.desc.setText(info["desc"])
        self.change_window.show()
    
    def markdown_editor_open(self):
        file = self.data.getCurrent()["item"]._text_file
        startfile(file.absolute())
        self.markdown_editor.close()
    
    def markdown_editor_save(self):
        item = self.data.getCurrent()["item"]
        text = self.markdown_editor.editor.toPlainText()
        item.write_text(text)
    
    def markdown_editor_view(self):
        text = self.markdown_editor.editor.toPlainText()
        self.markdown_editor.browser.setMarkdown(text)

    def markdown_editor_show(self):
        item = self.data.getCurrent()["item"]
        content = item.read_text()
        self.markdown_editor.editor.setPlainText(content)
        self.markdown_editor.browser.setMarkdown(content)
        self.markdown_editor.show()

window = MainWindow()
# 窗口信息设置
window.setWindowTitle("RemHelper")
window.setWindowIcon(QIcon("./img/favicon.ico"))
# QTableWidget设置
window.ui.view.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置选择整行
window.ui.view.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只可单选
window.ui.view.setAlternatingRowColors(True)  # 设置间隔行底色
window.ui.view.setColumnWidth(0, 150)  # 名称宽
window.ui.view.setColumnWidth(1, 80)  # 记忆量宽
window.ui.view.setColumnWidth(2, 200)  # 创建时间宽
# 加载字体
QFontDatabase.addApplicationFont("./font/JetBrainsMono.ttf")
# 加载样式
with open("./ui/style.qss", encoding="utf-8") as qss:
    APP.setStyleSheet(qss.read())
# 显示
window.show()

APP.exec_()
