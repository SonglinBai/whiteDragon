import sys
import os
from MainWindow import MainWindow
from domain.Graph import *
from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QAction, QApplication, QDesktopWidget, QFrame,
                               QHBoxLayout, QMainWindow, QMenu, QMenuBar,
                               QSplitter, QWidget, QFileDialog)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("UI/network.png"))
mainWindow = MainWindow()

nodz = mainWindow.nodz

filePath = ""

def saveGraph(graph: Graph):
    data = dict()

    data["NAME"] = graph.name
    nodeList = graph.ShowNodeList()
    data["NODES"] = []
    for node in nodeList:
        data["NODES"].append(node.toString())


# Nodes
@QtCore.Slot(str)
def on_nodeCreated(nodeName):
    print('node created : ', nodeName)


@QtCore.Slot(str)
def on_nodeDeleted(nodeName):
    print('node deleted : ', nodeName)


@QtCore.Slot(str, str)
def on_nodeEdited(nodeName, newName):
    print('node edited : {0}, new name : {1}'.format(nodeName, newName))


@QtCore.Slot(str)
def on_nodeSelected(nodesName):
    print('node selected : ', nodesName)


@QtCore.Slot(str, object)
def on_nodeMoved(nodeName, nodePos):
    print('node {0} moved to {1}'.format(nodeName, nodePos))


@QtCore.Slot(str)
def on_nodeDoubleClick(nodeName):
    print('double click on node : {0}'.format(nodeName))


# Attrs
@QtCore.Slot(str, int)
def on_attrCreated(nodeName, attrId):
    print('attr created : {0} at index : {1}'.format(nodeName, attrId))


@QtCore.Slot(str, int)
def on_attrDeleted(nodeName, attrId):
    print('attr Deleted : {0} at old index : {1}'.format(nodeName, attrId))


@QtCore.Slot(str, int, int)
def on_attrEdited(nodeName, oldId, newId):
    print('attr Edited : {0} at old index : {1}, new index : {2}'.format(nodeName, oldId, newId))


# Connections
@QtCore.Slot(str, str, str, str)
def on_connected(srcNodeName, srcPlugName, destNodeName, dstSocketName):
    print('connected src: "{0}" at "{1}" to dst: "{2}" at "{3}"'.format(srcNodeName, srcPlugName, destNodeName,
                                                                        dstSocketName))


@QtCore.Slot(str, str, str, str)
def on_disconnected(srcNodeName, srcPlugName, destNodeName, dstSocketName):
    print('disconnected src: "{0}" at "{1}" from dst: "{2}" at "{3}"'.format(srcNodeName, srcPlugName, destNodeName,
                                                                             dstSocketName))


# Graph
@QtCore.Slot()
def on_graphSaved():
    print('graph saved !')


@QtCore.Slot()
def on_graphLoaded():
    print('graph loaded !')


@QtCore.Slot()
def on_graphCleared():
    print('graph cleared !')


@QtCore.Slot()
def on_graphEvaluated():
    print('graph evaluated !')


# Other
@QtCore.Slot(object)
def on_keyPressed(key):
    print('key pressed : ', key)


@QtCore.Slot()
def on_actSaveTriggered():
    if len(filePath) <= 0:
        mainWindow.actSaveAs.trigger()
    else:
        nodz.saveGraph(filePath)


@QtCore.Slot()
def on_actSaveAsTriggered():
    filePath = QFileDialog.getSaveFileName(mainWindow, mainWindow.tr('Save'), os.environ['HOME'],
                                           mainWindow.tr('Json files (*.json)'))[0]

    nodz.saveGraph(filePath)


mainWindow.actSaveAs.triggered.connect(on_actSaveAsTriggered)
mainWindow.actSave.triggered.connect(on_actSaveTriggered)

nodz.signal_NodeCreated.connect(on_nodeCreated)
nodz.signal_NodeDeleted.connect(on_nodeDeleted)
nodz.signal_NodeEdited.connect(on_nodeEdited)
nodz.signal_NodeSelected.connect(on_nodeSelected)
nodz.signal_NodeMoved.connect(on_nodeMoved)
nodz.signal_NodeDoubleClicked.connect(on_nodeDoubleClick)

nodz.signal_AttrCreated.connect(on_attrCreated)
nodz.signal_AttrDeleted.connect(on_attrDeleted)
nodz.signal_AttrEdited.connect(on_attrEdited)

nodz.signal_PlugConnected.connect(on_connected)
nodz.signal_SocketConnected.connect(on_connected)
nodz.signal_PlugDisconnected.connect(on_disconnected)
nodz.signal_SocketDisconnected.connect(on_disconnected)

nodz.signal_GraphSaved.connect(on_graphSaved)
nodz.signal_GraphLoaded.connect(on_graphLoaded)
nodz.signal_GraphCleared.connect(on_graphCleared)
nodz.signal_GraphEvaluated.connect(on_graphEvaluated)

nodz.signal_KeyPressed.connect(on_keyPressed)

print("test")
print(nodz.evaluateGraph())

sys.exit(app.exec_())
