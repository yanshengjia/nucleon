# !/usr/bin/python
# coding=utf8

# 计算机综合课程设计：代码编辑器
# Created by Shengjia Yan @2016-12-19

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# 侧边栏
class SideBar(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.setMinimumWidth(30)
        # self.setMaximumWidth(350)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Window, QColor("#080808"))
        self.setPalette(p)


# 控制台
class Console(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.setMinimumHeight(30)
        # self.setMaximumHeight(350)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Window, QColor("#080808"))
        self.setPalette(p)


# 带行号的文本编辑框
class LNTextEdit(QFrame):

    class NumberBar(QWidget):

        def __init__(self, edit):
            QWidget.__init__(self, edit)

            self.edit = edit
            self.adjustWidth(1)

        def paintEvent(self, event):
            self.edit.numberbarPaint(self, event)
            QWidget.paintEvent(self, event)

        def adjustWidth(self, count):
            width = self.fontMetrics().width(unicode(count)) + 10
            if self.width() != width:
                self.setFixedWidth(width)

        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                # It would be nice to do
                # self.update(0, rect.y(), self.width(), rect.height())
                # But we can't because it will not remove the bold on the
                # current line if word wrap is enabled and a new block is
                # selected.
                self.update()


    class PlainTextEdit(QPlainTextEdit):

        def __init__(self, *args):
            QPlainTextEdit.__init__(self, *args)

            self.setFrameStyle(QFrame.NoFrame)
            self.highlight()
            #self.setLineWrapMode(QPlainTextEdit.NoWrap)

            self.cursorPositionChanged.connect(self.highlight)

        def highlight(self):
            hi_selection = QTextEdit.ExtraSelection()

            hi_selection.format.setBackground(self.palette().alternateBase())
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, QVariant(True))
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()

            self.setExtraSelections([hi_selection])

        def numberbarPaint(self, number_bar, event):
            font_metrics = self.fontMetrics()
            current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1

            block = self.firstVisibleBlock()
            line_count = block.blockNumber()
            painter = QPainter(number_bar)
            painter.fillRect(event.rect(), self.palette().base())

            # Iterate over all visible text blocks in the document.
            while block.isValid():
                line_count += 1
                block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

                # Check if the position of the block is out side of the visible
                # area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break

                # # We want the line number for the selected line to be bold.
                # if line_count == current_line:
                #     font = painter.font()
                #     font.setBold(True)
                #     painter.setFont(font)
                # else:
                #     font = painter.font()
                #     font.setBold(False)
                #     painter.setFont(font)

                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
                painter.drawText(paint_rect, Qt.AlignCenter, unicode(line_count))

                block = block.next()

            painter.end()

    def __init__(self, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        self.edit = self.PlainTextEdit()
        self.number_bar = self.NumberBar(self.edit)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)

        self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
        self.edit.updateRequest.connect(self.number_bar.updateContents)

        # 设置字体
        font = QFont()
        font.setFamily("Monaco")
        font.setPointSize(14)
        self.setFont(font)


        # 语法高亮
        # MyHighlighter(self, "Classic")


    def getText(self):
        return unicode(self.edit.toPlainText())

    def setText(self, text):
        self.edit.setPlainText(text)

    def isModified(self):
        return self.edit.document().isModified()

    def setModified(self, modified):
        self.edit.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.edit.setLineWrapMode(mode)


# 带文件栏的文本编辑框
class TextEditwithDocBar(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.tabbar = TabBar(self)
        self.textedit = LNTextEdit(self)

        layout = QVBoxLayout()
        layout.addWidget(self.tabbar)
        layout.addWidget(self.textedit)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


# 文本编辑器的语法高亮
class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, theme):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        keyword = QTextCharFormat()
        reservedClasses = QTextCharFormat()
        assignmentOperator = QTextCharFormat()
        delimiter = QTextCharFormat()
        specialConstant = QTextCharFormat()
        boolean = QTextCharFormat()
        number = QTextCharFormat()
        comment = QTextCharFormat()
        string = QTextCharFormat()
        singleQuotedString = QTextCharFormat()

        self.highlightingRules = []

        # keyword
        brush = QBrush(Qt.darkBlue, Qt.SolidPattern)
        keyword.setForeground(brush)
        keyword.setFontWeight(QFont.Bold)
        keywords = QStringList(["break", "else", "for", "if", "in",
                                "next", "repeat", "return", "switch",
                                "try", "while"])
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, keyword)
            self.highlightingRules.append(rule)

        # reservedClasses
        reservedClasses.setForeground(brush)
        reservedClasses.setFontWeight(QFont.Bold)
        keywords = QStringList(["array", "character", "complex",
                                "data.frame", "double", "factor",
                                "function", "integer", "list",
                                "logical", "matrix", "numeric",
                                "vector"])
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, reservedClasses)
            self.highlightingRules.append(rule)

        # assignmentOperator
        brush = QBrush(Qt.yellow, Qt.SolidPattern)
        pattern = QRegExp("(<){1,2}-")
        assignmentOperator.setForeground(brush)
        assignmentOperator.setFontWeight(QFont.Bold)
        rule = HighlightingRule(pattern, assignmentOperator)
        self.highlightingRules.append(rule)

        # delimiter
        pattern = QRegExp("[\)\(]+|[\{\}]+|[][]+")
        delimiter.setForeground(brush)
        delimiter.setFontWeight(QFont.Bold)
        rule = HighlightingRule(pattern, delimiter)
        self.highlightingRules.append(rule)

        # specialConstant
        brush = QBrush(Qt.green, Qt.SolidPattern)
        specialConstant.setForeground(brush)
        keywords = QStringList(["Inf", "NA", "NaN", "NULL"])
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, specialConstant)
            self.highlightingRules.append(rule)

        # boolean
        boolean.setForeground(brush)
        keywords = QStringList(["TRUE", "FALSE"])
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, boolean)
            self.highlightingRules.append(rule)

        # number
        pattern = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
        pattern.setMinimal(True)
        number.setForeground(brush)
        rule = HighlightingRule(pattern, number)
        self.highlightingRules.append(rule)

        # comment
        brush = QBrush(Qt.blue, Qt.SolidPattern)
        pattern = QRegExp("#[^\n]*")
        comment.setForeground(brush)
        rule = HighlightingRule(pattern, comment)
        self.highlightingRules.append(rule)

        # string
        brush = QBrush(Qt.red, Qt.SolidPattern)
        pattern = QRegExp("\".*\"")
        pattern.setMinimal(True)
        string.setForeground(brush)
        rule = HighlightingRule(pattern, string)
        self.highlightingRules.append(rule)

        # singleQuotedString
        pattern = QRegExp("\'.*\'")
        pattern.setMinimal(True)
        singleQuotedString.setForeground(brush)
        rule = HighlightingRule(pattern, singleQuotedString)
        self.highlightingRules.append(rule)

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = text.indexOf(expression, index + length)
        self.setCurrentBlockState(0)


# 文本编辑器的语法高亮规则
class HighlightingRule():
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format


# 文件栏
class TabBar(QTabBar):
    def __init__(self, parent=None):
        QTabBar.__init__(self, parent)

        self.setTabsClosable(True)  # tab可关闭
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeTab)  # 点击tab上的关闭按钮触发该tab被移除

        tab1 = self.addTab("Test1")
        tab2 = self.addTab("Test2")
        tab3 = self.addTab("Test3")

    def closeTab(self, currentIndex):
        self.removeTab(currentIndex)


# 总控程序
class Nucleon(QMainWindow):
    def __init__(self):
        super(Nucleon, self).__init__()

        self.initUI()

        self.createActions()
        self.createMenus()
        # self.createToolBar()
        self.createStatusBar()
        # self.createTabbar()
        # self.createTreeView()




    def createActions(self):
        # 新建文件
        self.newFileAct = QAction('&New', self)
        self.newFileAct.setShortcut(QKeySequence.New)
        self.connect(self.newFileAct, SIGNAL('triggered()'), self.newFile)

        # 打开文件
        self.openFileAct = QAction('&Open', self)
        self.openFileAct.setShortcut(QKeySequence.Open)
        self.connect(self.openFileAct, SIGNAL('triggered()'), self.openFile)

        # 保存文件
        self.saveFileAct = QAction('&Save', self)
        self.saveFileAct.setShortcut(QKeySequence.Save)
        self.connect(self.saveFileAct, SIGNAL('triggered()'), self.saveFile)
        self.flagFileSaved = False  # 文件是否被修改，PlainTextEdit 并不能设置 setModified，所以自己做了一个旗帜

        # 文件另存为
        self.saveAsAct = QAction('Save &As', self)
        self.saveAsAct.setShortcut(QKeySequence.SaveAs)
        self.connect(self.openFileAct, SIGNAL('triggered()'), self.openFile)

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

        # 关于 Nucleon
        self.aboutAct = QAction('&About', self)
        self.connect(self.aboutAct, SIGNAL('triggered()'), self.aboutNucleon)

        # 关于 Qt
        self.aboutQtAct = QAction('About &Qt', self)
        self.connect(self.aboutQtAct, SIGNAL('triggered()'), QApplication.aboutQt)


    # 当前文件
    # def setCurrentFile(self, fileName):





    # 新建文件
    def newFile(self):
        if self.maybeSave():    # 新建文件时 maybeSave() 必为真
            self.textedit_docbar.textedit.clear()
            self.setCurrentFile('')

        self.statusBar().showMessage("File created!")

    # 另存为
    # def saveAs(self):

    # 最近文件
    # def recentFile(self):


    # 打开并读取文件到编辑框
    def openFile(self):
        self.currentFilePath = QFileDialog.getOpenFileName(self, 'Open file', '/Users/yanshengjia/Desktop')
        f = open(self.currentFilePath)
        data = f.read()
        self.textedit_docbar.textedit.setText(data)

        self.statusBar().showMessage("File loaded!")

    # 保存文件
    def saveFile(self):
        f = open(self.currentFilePath, 'w')
        f.write(self.textedit_docbar.textedit.edit.toPlainText())

        self.flagFileSaved = True
        self.statusBar().showMessage("File saved!")
        return True

    # 关于 Nucleon
    def aboutNucleon(self):
        QMessageBox.about(
            self,
            "About Nucleon",
            "Nucleon \n 1.0 \n a lightweight and elegant IDE")

    # 关闭程序时询问是否退出
    def closeEvent(self, event):
        if not self.flagFileSaved:
            if self.maybeSave():
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    # 检测文件内容是否修改
    def maybeSave(self):
        if self.textedit_docbar.textedit.edit.document().isModified():
            self.flagFileSaved = False
            ret = QMessageBox.warning(
                self, "Message",
                u"Do you want to save the changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    # 创建菜单栏
    def createMenus(self):
        menubar = self.menuBar()

        # File
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openFileAct)
        fileMenu.addAction(self.saveFileAct)

        # Edit
        editMenu = menubar.addMenu('&Edit')

        # View
        viewMenu = menubar.addMenu('&View')

        # Run
        runMenu = menubar.addMenu('&Run')

        # Window
        windowMenu = menubar.addMenu('&Window')

        # About
        aboutMenu = menubar.addMenu('&About')
        # aboutMenu.addAction(self.aboutAct)

    # 创建状态栏
    def createStatusBar(self):
        statusbar = self.statusBar()
        statusbar.showMessage("Welcome to Nucleon!")

    # 窗体居中
    def center(self):
        screen = QDesktopWidget().screenGeometry()  # 计算屏幕像素，获取屏幕宽高
        size = self.geometry()  # 获取窗体宽高
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)  # 将窗体移到屏幕中心，向右向下移动

    # UI初始化
    def initUI(self):

        widget = QWidget()
        self.setCentralWidget(widget)

        # 控件 SideBar, Console, TextEditwithDocBar
        self.sidebar = SideBar(self)
        self.console = Console(self)
        self.textedit_docbar = TextEditwithDocBar(self)

        # 右部水平分割线
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.textedit_docbar)
        splitter1.addWidget(self.console)
        splitter1.setHandleWidth(1)

        # 垂直分割线
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(self.sidebar)
        splitter2.addWidget(splitter1)
        splitter2.setHandleWidth(1)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)      # 去除控件间距
        hbox.setContentsMargins(0, 0, 0, 0)     # 去除layout四周外边距
        hbox.addWidget(splitter2)
        widget.setLayout(hbox)

        # 窗体标题，大小，居中
        self.setWindowTitle('Nucleon')
        self.resize(960, 720)
        self.center()


def main():
    app = QApplication([])
    window = Nucleon()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
