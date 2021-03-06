import sys
from os import path

from PySide2.QtCore import QObject, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QAction, QApplication, QDesktopWidget, QFrame,
                               QHBoxLayout, QMainWindow, QMenu, QMenuBar,
                               QSplitter, QWidget)
from testFrame import testFrame
from Nodz.nodz_main import Nodz

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set window title and icon
        self.setWindowTitle('WhiteDragon')
        self.setWindowIcon(QIcon('network.png'))

        # move main window to center of screen
        self.resize(1280, 720)
        self.setMinimumSize(400, 300)
        fg = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.move(fg.topLeft())

        # set satus bar
        self.statusBar()

        # init menubar
        self.initMenuBar()

        # set layout
        self.initLayout()

        # show mainwindow
        self.show()

    def initMenuBar(self):
        # get menubar of mainwindow
        menubar = self.menuBar()

        # add about and preference action to appmenu
        self.actAbout = QAction()
        self.actAbout.setMenuRole(QAction.AboutRole)
        self.actPreference = QAction()
        self.actPreference.setMenuRole(QAction.PreferencesRole)
        self.appMenu = QMenu()
        self.appMenu.addAction(self.actPreference)
        self.appMenu.addAction(self.actAbout)
        menubar.addMenu(self.appMenu)

        # add actions to file menu
        self.menuFile = QMenu(self.tr('File'))
        self.actNewFile = QAction(self.tr('New'))
        self.actOpenFile = QAction(self.tr('Open'))
        self.actSave = QAction(self.tr('Save'))
        self.actSaveAs = QAction(self.tr('Save as'))
        self.actNewFile.setShortcut('Ctrl+N')
        self.actOpenFile.setShortcut('Ctrl+O')
        self.actSave.setShortcut('Ctrl+S')
        self.actSaveAs.setShortcut('Ctrl+Shift+S')
        self.menuFile.addAction(self.actNewFile)
        self.menuFile.addAction(self.actOpenFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actSave)
        self.menuFile.addAction(self.actSaveAs)
        menubar.addMenu(self.menuFile)

        # add actions to Edit menu
        self.menuEdit = QMenu(self.tr('Edit'))
        self.actUndo = QAction(self.tr('Undo'))
        self.actRedo = QAction(self.tr('Redo'))
        self.actCut = QAction(self.tr('Cut'))
        self.actCopy = QAction(self.tr('Copy'))
        self.actPaste = QAction(self.tr('Paste'))
        self.actUndo.setShortcut('Ctrl+Z')
        self.actRedo.setShortcut('Ctrl+Y')
        self.actCut.setShortcut('Ctrl+X')
        self.actCopy.setShortcut('Ctrl+C')
        self.actPaste.setShortcut('Ctrl+V')
        self.menuEdit.addAction(self.actUndo)
        self.menuEdit.addAction(self.actRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actCut)
        self.menuEdit.addAction(self.actCopy)
        self.menuEdit.addAction(self.actPaste)
        menubar.addMenu(self.menuEdit)

    def initLayout(self):
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout(self)

        self.itemListFrame = testFrame('list')
        self.itemListFrame.setFrameShape(QFrame.StyledPanel)

        self.resultFrame = testFrame('result')
        self.resultFrame.setFrameShape(QFrame.StyledPanel)

        self.nodz = Nodz(None)
        self.nodz.initialize()
        self.nodz.setFrameShape(QFrame.StyledPanel)

        self.PropertiesFrame = testFrame('properties')
        self.PropertiesFrame.setFrameShape(QFrame.StyledPanel)

        self.mainWidget.setLayout(self.mainLayout)
        sp = QSplitter(Qt.Vertical)
        sp.addWidget(self.itemListFrame)
        sp.addWidget(self.resultFrame)
        sp.setMinimumWidth(300)

        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(sp)
        splitter.addWidget(self.nodz)
        splitter.addWidget(self.PropertiesFrame)
        self.mainLayout.addWidget(splitter)
        self.setCentralWidget(self.mainWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # set app icon
    app.setWindowIcon(QIcon('network.png'))
    mainWindow = MainWindow()
    sys.exit(app.exec_())
