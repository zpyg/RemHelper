# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMainWindow, QDialog
from PySide2.QtGui import QIcon

from uic import ui_markdown_editor
from uic import ui_info_editor


class InfoEditor(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = ui_info_editor.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Info Editor")
        self.setWindowIcon(QIcon("./img/editor.ico"))

class MarkdownEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = ui_markdown_editor.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Markdown Editor")
        self.setWindowIcon(QIcon("./img/editor.ico"))

        preview = self.ui.toolBar.addAction("预览")
        preview.triggered.connect(self.view)
        self.save = self.ui.toolBar.addAction("保存")

    def view(self):
        text = self.ui.editor.toPlainText()
        self.ui.browser.setMarkdown(text)
