# !/usr/bin/python
# coding=utf8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from codeeditor import *

# 文件栏
class DocBar(QTabBar):
    def __init__(self, parent = None):
        QTabBar.__init__(self, parent)

        self.parent_TextEditwithDocBar = parent

        self.tabselected = 0    # 选中的 tab index
        self.tabquantity = self.count()    # tab 数量

        self.setTabsClosable(True)  # tab可关闭
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeDocTab)
        self.connect(self, SIGNAL("currentChanged(int)"), self.tabSelected)
        self.connect(self, SIGNAL("currentChanged(int)"), self, SLOT("setCurrentIndex(int)"))

    # 点击tab上的关闭按钮触发该tab被移除
    # 关闭文件Tab，currentIndex是当前关闭的tab索引
    def closeDocTab(self, currentIndex):

        self.tabquantity = self.count()     # 移除tab前的tab数量

        if self.tabquantity == 1:   # tabbar 只有一个tab，移除tab后清空编辑框
            self.parent_TextEditwithDocBar.parent_Nucleon.doclist = []  # 清空doclist
            self.removeTab(currentIndex)    # 移除tab
            self.parent_TextEditwithDocBar.parent_Nucleon.setCurrentFile('')    # 设置当前文件为空
            self.parent_TextEditwithDocBar.parent_Nucleon.textedit_docbar.textedit.setText('')  # 清空编辑框
        elif currentIndex == self.tabquantity - 1:   # tabbar不只一个tab，且关闭的tab是tabbar最右边的tab
            self.parent_TextEditwithDocBar.parent_Nucleon.delete(currentIndex)  # 移除doclist[currentIndex]
            self.removeTab(currentIndex)  # 移除tab
            if self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected] != 'null':
                self.parent_TextEditwithDocBar.parent_Nucleon.loadFile(self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected])
        else:   # tabbar不只一个tab，且关闭的tab不是tabbar最右边的tab
            self.parent_TextEditwithDocBar.parent_Nucleon.delete(currentIndex)  # 移除doclist[currentIndex]
            self.removeTab(currentIndex)  # 移除tab
            if self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected] != 'null':
                self.parent_TextEditwithDocBar.parent_Nucleon.loadFile(self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected])  # 设置当前文件为doclist[currentIndex]，因为doclist中移除了一个元素，所以移除文件右边文件的下标仍然为currentIndex


    # 添加文件Tab
    def addDocTab(self, fileName):
        self.addTab(fileName)

    # 更新文件Tab
    def updateDocTab(self, index, text):
        self.setTabText(index, text)

    # 选中Tab显示其对应的文件, 更新windowtitle
    def tabSelected(self):
        self.tabselected = self.currentIndex()
        # print self.tabselected
        # print self.parent_TextEditwithDocBar.parent_Nucleon.doclist
        if self.tabselected != -1:  # self.currentIndex() == -1 表示当前没有可见的tab

            # update doclabel && windowtitle

            if self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected] == 'null':
                self.parent_TextEditwithDocBar.parent_Nucleon.setWindowTitle('untitled')
                self.parent_TextEditwithDocBar.parent_Nucleon.console_button.buttonbar.doclabel.setText('untitled')

            if self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected] != 'null':
                self.parent_TextEditwithDocBar.parent_Nucleon.loadFile(self.parent_TextEditwithDocBar.parent_Nucleon.doclist[self.tabselected])

                docName = self.parent_TextEditwithDocBar.parent_Nucleon.shownName
                self.parent_TextEditwithDocBar.parent_Nucleon.console_button.buttonbar.doclabel.setText(docName)

                shownName = self.parent_TextEditwithDocBar.parent_Nucleon.shownName
                shownPath = self.parent_TextEditwithDocBar.parent_Nucleon.shownPath

                self.parent_TextEditwithDocBar.parent_Nucleon.setWindowTitle("%s  %s" % (shownName, shownPath))

