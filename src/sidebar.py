# !/usr/bin/python
# coding=utf8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from nucleon import *

# 侧边栏
class SideBar(QTreeView):
    def __init__(self, parent = None):
        QTreeView.__init__(self, parent)

        self.parent_Nucleon = parent

        self.setMinimumWidth(30)
        self.setFocusPolicy(Qt.NoFocus)


    def updateSideBar(self, path):

        self.model = MyFileSystemModel(self)
        self.setModel(self.model)
        self.model.setRootPath(QDir.currentPath())  # 监控当前目录文件变化
        self.setRootIndex(self.model.index(path))   # 显示哪个目录的信息
        self.hideColumn(1)      # 隐藏 Size 列
        self.hideColumn(2)      # 隐藏 Type 列
        self.hideColumn(3)      # 隐藏 Data Modified 列

        # 单击 SideBar 中的文件
        self.connect(self.selectionModel(),
                     SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.sidebarItemSelection)

        return True

    def sidebarItemSelection(self, selected, deselected):
        print("hello!")
        print(selected)
        print(deselected)


# 重写 headerData，让第一列表头为 Project
class MyFileSystemModel(QFileSystemModel):
    def __init__(self, parent = None):
        QFileSystemModel.__init__(self, parent)

        self.setHeaderData(0, Qt.Horizontal, "Project", Qt.DisplayRole)

    def headerData(self, section, orientation, role=None):
        if section == 0 and role == Qt.DisplayRole:
            return "Project"
        else:
            return QFileSystemModel.headerData(self, section, orientation, role)
