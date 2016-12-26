# !/usr/bin/python
# coding=utf8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# 侧边栏
class SideBar(QTreeView):
    def __init__(self, parent = None):
        QTreeView.__init__(self, parent)

        self.setMinimumWidth(30)
        self.setFocusPolicy(Qt.NoFocus)



    def test(self, selected, deselected):
        print("hello!")
        print(selected)
        print(deselected)

    def updateSideBar(self):

        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.setModel(model)
        self.setRootIndex(model.index("./"))
        QObject.connect(self.selectionModel(), SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.test)

        return True
