# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMainWindow, QDialog, QTextEdit, QTextBrowser
from PySide2.QtGui import QIcon

from uic import ui_markdown_editor
from uic import ui_info_editor
from uic import ui_find_editor


class InfoEditor(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = ui_info_editor.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Item Edit")
        self.setWindowIcon(QIcon("./img/editor.png"))


class MarkdownEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = ui_markdown_editor.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Markdown Edit")
        self.setWindowIcon(QIcon("./img/editor.png"))
        self.setStyleSheet("QHeaderView::section {border-style: none solid solid solid;border-color: #689d6a;border-width: 1px;}")

        self.editor = QTextEdit()
        self.browser = QTextBrowser()
        self.ui.group.setCellWidget(0, 0, self.editor)
        self.ui.group.setCellWidget(0, 1, self.browser)
        self.ui.group.setRowHeight(0, 700)
        self.ui.group.setColumnWidth(0, 450)

class FindEditor(QDialog):
    def __init__(self) -> None:
            super().__init__()
            self.ui = ui_find_editor.Ui_Form()
            self.ui.setupUi(self)

            self.setWindowIcon(QIcon("./img/search.png"))
            self.setWindowTitle("Search")
