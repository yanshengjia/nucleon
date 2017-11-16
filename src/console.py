# !/usr/bin/python
# coding=utf8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from nucleon import *

# 带运行按钮的控制台
class ConsolewithButton(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.parent_Nucleon = parent

        self.setMinimumHeight(30)

        self.console = Console(self)
        self.buttonbar = ButtonBar(self)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.buttonbar)
        layout.addWidget(self.console)
        layout.setStretchFactor(self.buttonbar, 1)
        layout.setStretchFactor(self.console, 5)
        self.setLayout(layout)


# 控制台
class Console(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.parent_ConsolewithButton = parent

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Window, QColor("#080808"))
        self.setPalette(p)

    def updateConsole(self):
        return True


# 按钮栏
class ButtonBar(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.parent_ConsolewithButton = parent

        self.setMinimumHeight(20)
        self.setMaximumHeight(20)
        self.setStyleSheet("font-family: Monaco")

        # 运行按钮
        self.runbutton = RunButton(self)
        self.runbutton.setFixedSize(50, 20)

        # 文件标签
        self.doclabel = DocButton(self)
        self.doclabel.setMinimumHeight(20)
        self.doclabel.setMaximumHeight(20)

        layout = QHBoxLayout()
        layout.setSpacing(22)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.runbutton)
        layout.addWidget(self.doclabel)
        layout.setAlignment(Qt.AlignLeft)

        self.setLayout(layout)
        self.setStyleSheet(open("../qss/buttonbar.qss", 'r').read())


# 运行按钮
class RunButton(QPushButton):
    def __init__(self, parent = None):
        QPushButton.__init__(self, parent)

        self.parent_ButtonBar = parent

        self.setText("Run")


# 文件按钮 伪装成文件标签
class DocButton(QPushButton):
    def __init__(self, parent = None):
        QPushButton.__init__(self, parent)

        self.parent_ButtonBar = parent




