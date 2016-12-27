# !/usr/bin/python
# coding=utf8

# 计算机综合课程设计：qt-mini-IDE
# Created by Shengjia Yan @2016-12-19

from codeeditor import *
from console import *
from sidebar import *


# 总控程序
class Nucleon(QMainWindow):
    def __init__(self):
        super(Nucleon, self).__init__()

        self.currentFile = ''           # 当前已保存文件带路径的文件名，当前无文件为空字符串, 新建文件未保存时为 untitled
        self.shownName = ''             # 初始文件名
        self.shownPath = ''             # 初始文件路径
        self.doclist = []               # 打开过的文件列表
        self.docquantity = len(self.doclist)    # 文件个数

        self.flagConsoleVisible = True  # 是否显示控制台
        self.flagAddDocTab = True       # 是否添加 DocTab
        self.flagPrintDoclist = True    # 是否打印 doclist

        self.initUI()

        self.createActions()
        self.createMenus()
        self.createToolBar()
        self.createStatusBar()

        # 当编辑框内容改变，在窗体上显示修改标志
        self.textedit_docbar.textedit.edit.document().contentsChanged.connect(self.documentWasModified)

    # 删除 doclist 中下标为 index 的元素
    def delete(self, index):
        self.doclist = self.doclist[:index] + self.doclist[index + 1:]

    # 动作集
    def createActions(self):

        ### File ###

        # 新建文件
        self.newFileAct = QAction('&New', self)
        self.newFileAct.setShortcut(QKeySequence.New)
        self.connect(self.newFileAct, SIGNAL('triggered()'), self.newFile)

        # 打开文件
        self.openFileAct = QAction('&Open', self)
        self.openFileAct.setShortcut(QKeySequence.Open)
        self.connect(self.openFileAct, SIGNAL('triggered()'), self.open)

        # 保存文件
        self.saveFileAct = QAction('&Save', self)
        self.saveFileAct.setShortcut(QKeySequence.Save)
        self.connect(self.saveFileAct, SIGNAL('triggered()'), self.save)

        # 文件另存为
        self.saveAsAct = QAction('Save &As', self)
        self.saveAsAct.setShortcut(QKeySequence.SaveAs)
        self.connect(self.saveAsAct, SIGNAL('triggered()'), self.saveAs)

        ### Edit ###

        # 剪切
        self.cutAct = QAction('&Cut', self)
        self.cutAct.setShortcut(QKeySequence.Cut)
        self.connect(self.cutAct, SIGNAL('triggered()'), self.textedit_docbar.textedit.edit.cut)

        # 复制
        self.copyAct = QAction('&Copy', self)
        self.copyAct.setShortcut(QKeySequence.Copy)
        self.connect(self.copyAct, SIGNAL('triggered()'), self.textedit_docbar.textedit.edit.copy)

        # 粘贴
        self.pasteAct = QAction('&Paste', self)
        self.pasteAct.setShortcut(QKeySequence.Paste)
        self.connect(self.pasteAct, SIGNAL('triggered()'), self.textedit_docbar.textedit.edit.paste)

        # 撤销
        self.undoAct = QAction('&Undo', self)
        self.undoAct.setShortcut(QKeySequence.Undo)
        self.connect(self.undoAct, SIGNAL('triggered()'), self.textedit_docbar.textedit.edit.undo)

        # 能剪切时才能剪切，能复制时才能复制，能撤销时才能撤销
        self.cutAct.setEnabled(False)
        self.copyAct.setEnabled(False)
        self.undoAct.setEnabled(False)
        self.textedit_docbar.textedit.edit.copyAvailable.connect(self.cutAct.setEnabled)
        self.textedit_docbar.textedit.edit.copyAvailable.connect(self.copyAct.setEnabled)
        self.textedit_docbar.textedit.edit.copyAvailable.connect(self.undoAct.setEnabled)

        ### View ###

        # Toggle ToolBar
        self.toggleToolBarAct = QAction('Toggle &ToolBar', self)
        self.connect(self.toggleToolBarAct, SIGNAL('triggered()'), self.hideToolBar)

        # Toggle DocBar
        self.toggleDocBarAct = QAction('Toggle &DocBar', self)
        self.connect(self.toggleDocBarAct, SIGNAL('triggered()'), self.hideDocBar)

        # Toggle SideBar
        self.toggleSideBarAct = QAction('Toggle &SideBar', self)
        self.connect(self.toggleSideBarAct, SIGNAL('triggered()'), self.hideSideBar)

        # Toggle Console
        self.toggleConsoleAct = QAction('Toggle &Console', self)
        self.connect(self.toggleConsoleAct, SIGNAL('triggered()'), self.hideConsole)

        # Toggle StatusBar
        self.toggleStatusBarAct = QAction('Toggle &StatusBar', self)
        self.connect(self.toggleStatusBarAct, SIGNAL('triggered()'), self.hideStatusBar)


        ### Code ###

        # Run
        # self.runAct = QAction('&Run', self)
        # self.connect(self.runAct, SIGNAL('triggered()'), self.console_runbutton.buttonbar.runbutton.clicked())

        # C Code
        # self.CCodeAct = QAction('C &Code', self)

        # ASM Code
        # self.ASMCodeAct = QAction('ASM &Code', self)

        # COE Code
        # self.COECodeAct = QAction('COE &Code', self)



        ### About ###

        # 关于 Nucleon
        self.aboutNucleonAct = QAction('&About', self)
        self.connect(self.aboutNucleonAct, SIGNAL('triggered()'), self.about)

        # 关于 Qt
        self.aboutQtAct = QAction('About &Qt', self)
        self.connect(self.aboutQtAct, SIGNAL('triggered()'), self.aboutQt)


    # 创建菜单栏
    def createMenus(self):
        self.menubar = self.menuBar()

        # File Menu
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.newFileAct)
        self.fileMenu.addAction(self.openFileAct)
        self.fileMenu.addAction(self.saveFileAct)
        self.fileMenu.addAction(self.saveAsAct)

        # Edit Menu
        self.editMenu = self.menubar.addMenu('&Edit')
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addAction(self.undoAct)

        # View Menu
        self.viewMenu = self.menubar.addMenu('&View')
        self.viewMenu.addAction(self.toggleToolBarAct)
        self.viewMenu.addAction(self.toggleDocBarAct)
        self.viewMenu.addAction(self.toggleSideBarAct)
        self.viewMenu.addAction(self.toggleConsoleAct)
        self.viewMenu.addAction(self.toggleStatusBarAct)

        # Code Menu
        self.codeMenu = self.menubar.addMenu('&Code')
        # self.codeMenu.addAction(self.runAct)
        # self.codeMenu.addAction(self.CcodeAct)
        # self.codeMenu.addAction(self.ASMcodeAct)
        # self.codeMenu.addAction(self.COEcodeAct)

        # About Menu
        # 蜜汁问题！！！
        self.aboutMenu = self.menubar.addMenu('&About')
        self.aboutMenu.addAction(self.aboutNucleonAct)
        self.aboutMenu.addAction(self.aboutQtAct)

        # Help Menu
        self.helpMenu = self.menubar.addMenu('&Help')



    # 工具栏
    def createToolBar(self):

        # File Tool
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newFileAct)
        self.fileToolBar.addAction(self.openFileAct)
        self.fileToolBar.addAction(self.saveFileAct)
        self.fileToolBar.addAction(self.saveAsAct)

        # Edit Tool
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)
        self.editToolBar.addAction(self.undoAct)

        # 一开始不显示 ToolBar
        self.fileToolBar.setVisible(False)
        self.editToolBar.setVisible(False)


    # ToolBar的隐藏与显示
    def hideToolBar(self):
        vToolBar = self.fileToolBar.isVisible()
        self.fileToolBar.setVisible(not vToolBar)
        self.editToolBar.setVisible(not vToolBar)

    # DocBar的隐藏与显示
    def hideDocBar(self):
        vDocBar = self.textedit_docbar.docbar.isVisible()
        self.textedit_docbar.docbar.setVisible(not vDocBar)

    # SideBar的隐藏与显示
    def hideSideBar(self):
        vSideBar = self.sidebar.isVisible()
        self.sidebar.setVisible(not vSideBar)

    # Console的隐藏与显示
    def hideConsole(self):
        vConsole = self.console_button.isVisible()
        self.console_button.setVisible(not vConsole)

    # StatusBar的隐藏与显示
    def hideStatusBar(self):
        vStatusBar = self.statusbar.isVisible()
        self.statusbar.setVisible(not vStatusBar)


    # 创建状态栏
    def createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Welcome to Nucleon!")


    # 设置当前文件，获取 当前文件名 和 当前路径
    # 新建文件 currentFile == 'untitled'
    # 打开文件 currentFile == '打开的文件的带路径的文件名'
    # self.shownName: 当前文件名
    # self.shownPath: 当前路径
    def setCurrentFile(self, fileName):
        self.currentFile = fileName
        self.textedit_docbar.textedit.setModified(False)
        self.setWindowModified(False)

        if self.currentFile:
            self.shownName = self.pureName(self.currentFile)
            self.shownPath = self.purePath(self.currentFile)
        else:
            self.shownName = 'untitled'

        if self.shownName == 'untitled':
            self.setWindowTitle('untitled')
        else:
            self.setWindowTitle("%s  %s" % (self.shownName, self.shownPath))

        self.console_button.buttonbar.doclabel.setText(self.shownName)


    # 新建文件
    def newFile(self):
        if self.maybeSave():    # 新建文件前如果在编辑框输入了内容会询问是否要保存
            self.textedit_docbar.textedit.edit.clear()  # 清空编辑框
            self.setCurrentFile('untitled')     # 设置当前文件名为 untitled

            self.doclist.append('null') # 文件列表添加 null
            self.textedit_docbar.docbar.addDocTab(self.shownName)   # 在 DocBar 添加 DocTab

            if self.flagPrintDoclist:
                print self.doclist


            # statusbar
            self.statusbar.showMessage("File created!")


    # 打开文件
    def open(self):
        if self.maybeSave():    # 打开文件前如果在编辑框中输入了内容会询问是否保存
            fileName = QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)
                self.doclist.append(self.currentFile)  # 将打开的带路径的文件名加入 doclist
                self.textedit_docbar.docbar.addDocTab(self.shownName)   # 添加对应的 DocTab

                if self.flagPrintDoclist:
                    print self.doclist

                self.sidebar.updateSideBar(self.shownPath)              # 更新对应的 SideBar

                self.statusbar.showMessage("File opened!")


    # 载入文件到编辑框
    # fileName 是带路径的文件名
    def loadFile(self, fileName):

        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(
                self, "Warning",
                "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textedit_docbar.textedit.setText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.statusbar.showMessage("File loaded!")


    # 保存文件
    def save(self):
        if self.currentFile != 'untitled':    # 如果当前文件是被打开的，直接保存在原路径
            return self.saveFile(self.currentFile)

        return self.saveAs()    # 如果当前文件是新建的，文件另存为

    # 文件另存为
    def saveAs(self):
        fileName = QFileDialog.getSaveFileName(self)

        if fileName:
            ret = self.saveFile(fileName)

            currentIndex = self.textedit_docbar.docbar.currentIndex()

            # 更新 DocBar
            self.textedit_docbar.docbar.updateDocTab(currentIndex, self.shownName)

            # 更新 SideBar
            self.sidebar.updateSideBar(self.shownPath)

            # 更新 doclist
            self.doclist[currentIndex] = fileName

            if self.flagPrintDoclist:
                print self.doclist

        return False


    # 保存文件
    def saveFile(self, fileName):

        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(
                self, "Warning",
                "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.textedit_docbar.textedit.edit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusbar.showMessage("File saved!")
        return True


    # 最近文件
    # def recentFile(self):


    # 关于 Nucleon
    def about(self):
        QMessageBox.about(
            self,
            "About",
            "Nucleon 1.0 a lightweight and elegant IDE")


    # 关于 Qt
    def aboutQt(self):
        QMessageBox.aboutQt(self, "About Qt")


    # 关闭程序时询问是否退出
    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    # 修改的文件内容是否需要保存
    def maybeSave(self):
        if self.textedit_docbar.textedit.getText() == '' and self.currentFile == 'untitled' and self.textedit_docbar.docbar.tabquantity == 1:
            return True

        if self.textedit_docbar.textedit.isModified():
            ret = QMessageBox.warning(
                self, "Message",
                u"Do you want to save the changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            elif ret == QMessageBox.Cancel:
                return False
        return True


    # 返回不带路径的文件名
    def pureName(self, fileName):
        return QFileInfo(fileName).fileName()

    # 返回不带文件名的路径
    def purePath(self, fileName):
        return QFileInfo(fileName).path()

    # 文件是否被修改，被修改在窗体显示修改标志，初始修改增加DocTab
    def documentWasModified(self):
        self.setWindowModified(self.textedit_docbar.textedit.isModified())

        # # DocBar 没有 DocTab 时，修改编辑框内容可以添加 DocTab
        # if self.textedit_docbar.docbar.count() == 0:
        #     self.flagAddDocTab = True
        #
        # # 当前文件为空 且 能添加 DocTab 时 添加DocTab，只能添加一次
        # if self.currentFile == '' and self.flagAddDocTab:
        #     self.textedit_docbar.docbar.addDocTab(self.shownName)
        #     self.flagAddDocTab = False




    # 窗体居中
    def center(self):
        screen = QDesktopWidget().screenGeometry()  # 计算屏幕像素，获取屏幕宽高
        size = self.geometry()  # 获取窗体宽高
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)  # 将窗体移到屏幕中心，向右向下移动

    # UI初始化
    def initUI(self):

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # 控件
        self.sidebar = SideBar(self)
        self.console_button = ConsolewithButton(self)
        self.textedit_docbar = TextEditwithDocBar(self)

        # 初始隐藏或显示 Console
        if self.flagConsoleVisible:
            self.console_button.setVisible(True)
        else:
            self.console_button.setVisible(False)

        # 右部水平分割线
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.textedit_docbar)
        self.splitter1.addWidget(self.console_button)
        self.splitter1.setStretchFactor(5, 1)  # textedit_docbar 与 console_runbutton 的宽度之比为1:5
        self.splitter1.setHandleWidth(1)

        # 垂直分割线
        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.sidebar)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setStretchFactor(1, 7)   # sidebar 与 splitter1 的宽度之比为1:5
        self.splitter2.setHandleWidth(1)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)      # 去除控件间距
        hbox.setContentsMargins(1, 1, 1, 1)     # layout四周外边距
        hbox.addWidget(self.splitter2)
        self.widget.setLayout(hbox)

        # 窗体标题，大小，居中
        self.setWindowTitle('Nucleon')
        self.resize(960, 720)
        self.center()