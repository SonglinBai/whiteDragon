import sys

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIcon, QCursor
from PySide2.QtWidgets import (QAction, QApplication, QDesktopWidget, QFrame,
                               QHBoxLayout, QMainWindow, QMenu, QSplitter, QWidget, QListWidget, QListWidgetItem)
from UI.testFrame import testFrame
from Nodz.nodz_main import Nodz
from QtPropertyBrowser.QtProperty.qtpropertymanager import (
    QtBoolPropertyManager,
    QtIntPropertyManager,
    QtStringPropertyManager,
    QtSizePropertyManager,
    QtRectPropertyManager,
    QtSizePolicyPropertyManager,
    QtEnumPropertyManager,
    QtGroupPropertyManager
)
from QtPropertyBrowser.QtProperty.qteditorfactory import (    QtCheckBoxFactory,
    QtSpinBoxFactory,
    QtSliderFactory,
    QtScrollBarFactory,
    QtLineEditFactory,
    QtEnumEditorFactory
)
from QtPropertyBrowser.QtProperty.qtgroupboxpropertybrowser import QtGroupBoxPropertyBrowser
from QtPropertyBrowser.libqt5.pyqtcore import QMap, QList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set window title and icon
        self.setWindowTitle('WhiteDragon')
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

        self.itemListFrame = NodeListWidget()
        self.itemListFrame.setFrameShape(QFrame.StyledPanel)

        self.resultFrame = ResultListWidget()
        self.resultFrame.setFrameShape(QFrame.StyledPanel)

        self.nodz = Nodz(None)
        self.nodz.initialize()
        self.nodz.setFrameShape(QFrame.StyledPanel)

        self.PropertiesFrame = PropertyBrowserWidget()
        # self.PropertiesFrame.setFrameShape(QFrame.StyledPanel)

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


class NodeListWidget(QListWidget):
    def __init__(self):
        super(NodeListWidget, self).__init__()
        self.createContextMenu()
        self.itemClicked.connect(self.showClickedItem)

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction(u'添加结点')
        self.actionB = self.contextMenu.addAction(u'删除结点')

    def showContextMenu(self):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QCursor().pos())
        self.contextMenu.show()

    @Slot(QListWidgetItem)
    def showClickedItem(self, item: QListWidgetItem):
        print(item.text())

class ResultListWidget(QListWidget):
    def __init__(self):
        super(ResultListWidget, self).__init__()
        self.createContextMenu()
        self.itemClicked.connect(self.showClickedItem)

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction(u'添加结点')
        self.actionB = self.contextMenu.addAction(u'删除结点')

    def showContextMenu(self):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QCursor().pos())
        self.contextMenu.show()

    @Slot(QListWidgetItem)
    def showClickedItem(self, item: QListWidgetItem):
        print(item.text())

class PropertyBrowserWidget(QtGroupBoxPropertyBrowser):
    def __init__(self):
        super(PropertyBrowserWidget, self).__init__()

    def testData(self):
        boolManager = QtBoolPropertyManager(w)
        intManager = QtIntPropertyManager(w)
        stringManager = QtStringPropertyManager(w)
        sizeManager = QtSizePropertyManager(w)
        rectManager = QtRectPropertyManager(w)
        sizePolicyManager = QtSizePolicyPropertyManager(w)
        enumManager = QtEnumPropertyManager(w)
        groupManager = QtGroupPropertyManager(w)

        item0 = groupManager.addProperty("QObject")

        item1 = stringManager.addProperty("objectName")
        item0.addSubProperty(item1)

        item2 = boolManager.addProperty("enabled")
        item0.addSubProperty(item2)

        item3 = rectManager.addProperty("geometry")
        item0.addSubProperty(item3)

        item4 = sizePolicyManager.addProperty("sizePolicy")
        item0.addSubProperty(item4)

        item5 = sizeManager.addProperty("sizeIncrement")
        item0.addSubProperty(item5)

        item7 = boolManager.addProperty("mouseTracking")
        item0.addSubProperty(item7)

        item8 = enumManager.addProperty("direction")
        enumNames = QList()
        enumNames.append("Up")
        enumNames.append("Right")
        enumNames.append("Down")
        enumNames.append("Left")

        enumManager.setEnumNames(item8, enumNames)
        enumIcons = QMap()
        enumIcons[0] = QIcon(":/demo/images/up.png")
        enumIcons[1] = QIcon(":/demo/images/right.png")
        enumIcons[2] = QIcon(":/demo/images/down.png")
        enumIcons[3] = QIcon(":/demo/images/left.png")
        enumManager.setEnumIcons(item8, enumIcons)
        item0.addSubProperty(item8)

        item9 = intManager.addProperty("value")
        intManager.setRange(item9, -100, 100)
        item0.addSubProperty(item9)

        checkBoxFactory = QtCheckBoxFactory(self)
        spinBoxFactory = QtSpinBoxFactory(self)
        sliderFactory = QtSliderFactory(self)
        scrollBarFactory = QtScrollBarFactory(self)
        lineEditFactory = QtLineEditFactory(self)
        comboBoxFactory = QtEnumEditorFactory(self)

        self.setFactoryForManager(boolManager, checkBoxFactory)
        self.setFactoryForManager(intManager, spinBoxFactory)
        self.setFactoryForManager(stringManager, lineEditFactory)
        self.setFactoryForManager(sizeManager.subIntPropertyManager(), spinBoxFactory)
        self.setFactoryForManager(rectManager.subIntPropertyManager(), spinBoxFactory)
        self.setFactoryForManager(sizePolicyManager.subIntPropertyManager(), spinBoxFactory)
        self.setFactoryForManager(sizePolicyManager.subEnumPropertyManager(), comboBoxFactory)
        self.setFactoryForManager(enumManager, comboBoxFactory)

        self.addProperty(item0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # set app icon
    app.setWindowIcon(QIcon('icon/network.png'))
    mainWindow = MainWindow()
    sys.exit(app.exec_())
