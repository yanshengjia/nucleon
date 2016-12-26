# !/usr/bin/python
# coding=utf8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# 文件栏
class DocBar(QTabBar):
    def __init__(self, parent=None):
        QTabBar.__init__(self, parent)

        self.setTabsClosable(True)  # tab可关闭
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeDocTab)  # 点击tab上的关闭按钮触发该tab被移除



    # 关闭文件Tab
    def closeDocTab(self, currentIndex):
        self.removeTab(currentIndex)


    # 添加文件Tab
    def addDocTab(self, fileName):
        tab = self.addTab(fileName)


