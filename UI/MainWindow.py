import sys

from domain.Graph import *
from Qt.QtCore import Qt, QPointF
from PyQt5.QtCore import QVariant
from Qt.QtGui import QIcon, QCursor
from Qt.QtWidgets import (QAction, QApplication, QDesktopWidget, QFrame,
                          QHBoxLayout, QMainWindow, QMenu, QSplitter, QWidget, QListWidget, QListWidgetItem,
                          QAbstractItemView)
from UI.Nodz.nodz_main import Nodz
from UI.QtPropertyBrowser.QtProperty.qtvariantproperty import QtVariantPropertyManager, QtVariantEditorFactory
from UI.QtPropertyBrowser.QtProperty.qttreepropertybrowser import QtTreePropertyBrowser
from UI.QtPropertyBrowser.libqt5.pyqtcore import QMap, QList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set window title and icon
        self.setWindowTitle(self.tr(u'WhiteDragon'))
        self.setWindowIcon(QIcon('icon/network.png'))

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
        self.menuFile = QMenu(self.tr(u'File'))
        self.actNewFile = QAction(self.tr(u'New'))
        self.actOpenFile = QAction(self.tr(u'Open'))
        self.actSave = QAction(self.tr(u'Save'))
        self.actSaveAs = QAction(self.tr(u'Save As'))
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
        self.menuEdit = QMenu(self.tr(u'Edit'))
        self.actUndo = QAction(self.tr(u'Undo'))
        self.actRedo = QAction(self.tr(u'Redo'))
        self.actCut = QAction(self.tr(u'Cut'))
        self.actCopy = QAction(self.tr(u'Copy'))
        self.actPaste = QAction(self.tr(u'Paste'))
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

        # add actions to Run menu
        self.menuRun = QMenu(self.tr(u'Analyse'))
        self.actRun = QAction(self.tr(u'NetWork Analyse'))
        self.actRunRisk = QAction(self.tr(u'High Risk Node'))
        self.actRunImport = QAction(self.tr(u'Important Node'))
        self.actRun.setShortcut('Ctrl+R')
        self.menuRun.addAction(self.actRun)
        self.menuRun.addSeparator()
        self.menuRun.addAction(self.actRunRisk)
        self.menuRun.addAction(self.actRunImport)
        menubar.addMenu(self.menuRun)

    def initLayout(self):
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout(self)

        self.nodeListFrame = NodeListWidget(self)
        self.nodeListFrame.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.nodeListFrame.setFrameShape(QFrame.StyledPanel)

        # connect single itemClicked to selectNode
        self.nodeListFrame.itemSelectionChanged.connect(self.selectNodes)

        self.resultFrame = ResultListWidget(self)
        self.resultFrame.setFrameShape(QFrame.StyledPanel)

        self.attackTemplateWindow = AttackTemplateWindow(self)

        self.nodz = Nodz(self)
        self.nodz.initialize()

        self.PropertiesFrame = PropertyBrowserWidget(self)

        self.mainWidget.setLayout(self.mainLayout)
        sp = QSplitter(Qt.Vertical)
        sp.addWidget(self.nodeListFrame)
        sp.addWidget(self.resultFrame)

        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(sp)
        splitter.addWidget(self.nodz)
        splitter.addWidget(self.PropertiesFrame)
        self.mainLayout.addWidget(splitter)
        self.setCentralWidget(self.mainWidget)

    def selectNodes(self):
        items = self.nodeListFrame.selectedItems()
        # cancel all node selection
        for node in self.nodz.scene().nodes.keys():
            self.nodz.scene().nodes[node].setSelected(False)
        # select node which name is item.text()
        for item in items:
            self.nodz.scene().nodes[item.text()].setSelected(True)

    def loadGraph(self, graph:Graph):
        # 清空节点列表,清空nodz图
        self.nodeListFrame.update(graph)
        self.nodz.loadGraph(graph)


class NodeListWidget(QListWidget):
    def __init__(self,parent=None):
        super(NodeListWidget, self).__init__(parent)
        self.createContextMenu()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction(self.tr(u'Add Node'))
        self.actionB = self.contextMenu.addAction(self.tr(u'Del Node'))

    def showContextMenu(self):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QCursor().pos())
        self.contextMenu.show()

    def addNode(self, node:Node):
        icon = ['UI/icon/pc.png','UI/icon/server.png']
        self.addItem(QListWidgetItem(QIcon(icon[node.type]), node.label))

    def update(self, graph:Graph):
        self.clear()
        for node in graph.ShowNodeList():
            self.addNode(node)


class ResultListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ResultListWidget, self).__init__(parent)
        self.createContextMenu()
        self.itemClicked.connect(self.showClickedItem)

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction(self.tr(u'Add Node'))
        self.actionB = self.contextMenu.addAction(self.tr(u'Del Node'))

    def showContextMenu(self):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QCursor().pos())
        self.contextMenu.show()

    def showClickedItem(self, item: QListWidgetItem):
        print(item.text())


class PropertyBrowserWidget(QtTreePropertyBrowser):
    def __init__(self, parent=None):
        super(PropertyBrowserWidget, self).__init__(parent)
        self.initData(parent)

    def initData(self, parent):
        variantManager = QtVariantPropertyManager(parent)

        topItem = variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), self.tr(u'Node'))

        labelItem = variantManager.addProperty(QVariant.String, self.tr(u'Label'))
        topItem.addSubProperty(labelItem)

        # portItem = variantManager.addProperty(QtVariantPropertyManager.groupTypeId(),"port")

        """
            add type selection item 
        """
        typeItem = variantManager.addProperty(QtVariantPropertyManager.enumTypeId(), self.tr(u'Type'))

        enumNames = QList()
        enumNames.append("PC")
        enumNames.append("Server")

        typeItem.setAttribute("enumNames", enumNames)
        enumIcons = QMap()
        enumIcons[0] = QIcon('UI/icon/pc.png')
        enumIcons[1] = QIcon('UI/icon/server.png')
        typeItem.setAttribute("enumIcons", enumIcons)

        topItem.addSubProperty(typeItem)

        """
            add permission table
        """
        permissionItem = variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), self.tr(u'Permission'))
        # for i in range(10):
        #     item = variantManager.addProperty(QVariant.String, "test")
        #     item.setValue(i)
        #     item.setAttribute("readOnly", True)
        #     permissionItem.addSubProperty(item)
        topItem.addSubProperty(permissionItem)

        attempListItem = variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), self.tr(u'Attack Templates'))
        # for i in range(10):
        #     item = variantManager.addProperty(QVariant.String, "label")
        #     item.setValue("test"+str(i))
        #     item.setAttribute("readOnly", True)
        #     attempListItem.addSubProperty(item)
        topItem.addSubProperty(attempListItem)

        variantFactory = QtVariantEditorFactory(parent)

        self.setFactoryForManager(variantManager, variantFactory)

        self.addProperty(topItem)


class AttackTemplateWindow(QListWidget):
    def __init__(self,parent=None):
        super(AttackTemplateWindow, self).__init__(parent)
        self.setWindowTitle(self.tr(u'Attack Templates'))
        self.setWindowIcon(QIcon('icon/network.png'))
        self.createContextMenu()
        # self.itemClicked.connect(self.showClickedItem)

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction(self.tr(u'Add Template'))
        self.actionB = self.contextMenu.addAction(self.tr(u'Del Template'))

    def showContextMenu(self):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QCursor().pos())
        self.contextMenu.show()

    # def showClickedItem(self, item: QListWidgetItem):
    #     print(item.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # set app icon
    app.setWindowIcon(QIcon('icon/network.png'))
    mainWindow = MainWindow()
    sys.exit(app.exec_())
