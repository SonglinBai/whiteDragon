import sys
import os
from UI.MainWindow import MainWindow
from domain.Graph import *
from Qt import QtCore
from Qt.QtGui import QIcon
from Qt.QtWidgets import (QApplication, QFileDialog, QListWidgetItem)
import utils

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("UI/icon/network.png"))
translator = QtCore.QTranslator()
translator.load("./zh_CN.qm")
app.installTranslator(translator)
mainWindow = MainWindow()

nodz = mainWindow.nodz

filePath = ""
graph = Graph('Untitled')


def saveGraph(graph: Graph, filePath):
    """
    Save Graph
    :type graph: graph.
    :param graph: the Graph you want to save
    :type filePath: str
    :param filePath: path you want to save
    """
    data = graph.toJson()
    try:
        utils._saveData(path=filePath, data=data)
    except:
        print('Invalid path : {0}'.format(filePath))
        print('Save aborted !')
        return False


def loadGraph(graph: Graph,filePath):

    """
        从json文件中载入
    """
    if os.path.exists(filePath):
        data = utils._loadData(filePath=filePath)
    else:
        print('Invalid path : {0}'.format(filePath))
        print('Load aborted !')
        return False

    graph.loadGraph(data)
    mainWindow.loadGraph(graph)

def CaculateGraph(graph):
    road = DoubleList()
    aAttempV0 = Attemp('StartPoint',['Strat'],0,0,1.00)
    road.append([graph.getNodeByLabel('nodeA'),aAttempV0])
    graph.CoreAlgorithm(graph.getNodeByLabel('nodeA'), road)
    updateResult(graph.AllRoad.ListGroup)

def updateResult(result: List):
    mainWindow.resultFrame.clear()
    for road in result:
        mainWindow.resultFrame.addItem(road.travel())


# Nodes
@QtCore.Slot(str)
def on_nodeCreated(nodeName):
    print('node created : ', nodeName)
    """
    1. 更新Graph
    2. 更新nodeListFrame
    """
    node = Node(nodeName,0,[0,0],[],[])
    graph.addNode(node)
    mainWindow.nodeListFrame.addNode(node)

@QtCore.Slot(str)
def on_nodeDeleted(nodeName):
    print('node deleted : ', nodeName)
    graph.delNodes(nodeName)
    mainWindow.nodeListFrame.update(graph)


@QtCore.Slot(str, str)
def on_nodeEdited(nodeName, newName):
    print('node edited : {0}, new name : {1}'.format(nodeName, newName))


@QtCore.Slot(str)
def on_nodeSelected(node):
    print(node)


#  print('node selected : ', node)


@QtCore.Slot(str, object)
def on_nodeMoved(nodeName, nodePos):
    print('node {0} moved to {1}'.format(nodeName, nodePos))

    graph.move(nodeName, [nodePos.x(),nodePos.y()])


@QtCore.Slot(str)
def on_nodeDoubleClick(nodeName):
    print('double click on node : {0}'.format(nodeName))
    mainWindow.attackTemplateWindow.show()


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
        saveGraph(graph, filePath)


@QtCore.Slot()
def on_actSaveAsTriggered():
    global filePath
    filePath = QFileDialog.getSaveFileName(mainWindow, mainWindow.tr('Save'), os.path.dirname(filePath),
                                           mainWindow.tr('Json files (*.json)'))[0]

    saveGraph(graph,filePath)


@QtCore.Slot()
def on_actOpenTriggered():
    global filePath
    filePath = QFileDialog.getOpenFileName(mainWindow, mainWindow.tr('Open'), os.path.dirname(filePath),
                                           mainWindow.tr('Json files (*.json)'))[0]
    loadGraph(graph,filePath)

@QtCore.Slot()
def on_actRunTriggered():
    CaculateGraph(graph)

mainWindow.actRun.triggered.connect(on_actRunTriggered)
mainWindow.actSaveAs.triggered.connect(on_actSaveAsTriggered)
mainWindow.actSave.triggered.connect(on_actSaveTriggered)
mainWindow.actOpenFile.triggered.connect(on_actOpenTriggered)

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

# GraphA = Graph('GraphA')
# #建立攻击模版
# bAttempV0 = Attemp('B(v0)', ['CVE-1'], 1, 1, 0.5)
# bAttempV1 = Attemp('B(v1)', ['CVE-2'], 0, 1, 0.2)
# cAttempV0 = Attemp('C(v0)', ['CVE-3'], 0, 1, 0.1)
# cAttempV1 = Attemp('C(v1)', ['CVE-4'], 1, 2, 0.3)
# cAttempV2 = Attemp('C(v2)', ['CVE-5'], 2, 3, 0.7)
# dAttempV0 = Attemp('D(v0)', ['CVE-6'], 0, 0, 0.4)
# eAttempV0 = Attemp('E(v0)', ['CVE-7'], 0, 0, 0.2)
# fAttempV0 = Attemp('F(v0)', ['CVE-8'], 0, 0, 0.9)
#
# #建立点：
# Anode = Node('nodeA',0,[8086],[])
# Bnode = Node('nodeB',1,[1123],[bAttempV0,bAttempV1])
# Cnode = Node('nodeC',0,[2222],[cAttempV0,cAttempV1,cAttempV2])
# Dnode = Node('nodeD',1,[2231],[dAttempV0])
# Enode = Node('nodeE',1,[3112],[eAttempV0])
# Fnode = Node('nodeF',1,[4445],[fAttempV0])
# GraphA.setNodeList([Anode,Bnode,Cnode,Dnode,Enode,Fnode])
#
# #建立邻接多重表
# GraphA.AttackTable = {
#     Anode:[Bnode,Cnode,Dnode],
#     Bnode:[Cnode,Enode],
#     Cnode:[Enode],
#     Dnode:[Cnode,Fnode],
#     Enode:[Fnode],
#     Fnode:[]
# }
# nodz.createNode('nodeA')
# nodz.createNode('nodeB')
# nodz.createNode('nodeC')
# nodz.createNode('nodeD')
# nodz.createNode('nodeE')
# nodz.createNode('nodeF')
# saveGraph(GraphA, "./test.json")

# loadGraph("./test.json")
#
# aAttempV0 = Attemp('StartPoint',['Strat'],0,0,1)
#
# road = DoubleList()
# Anode = graph.getNodeByLabel('nodeA')
# road.append([Anode,aAttempV0])
# graph.CoreAlgorithm(Anode, road)
# for i in graph.AllRoad.ListGroup:
#     i.travel()
#     print(i.head.data[0])

loadGraph(graph, "./test2.json")

sys.exit(app.exec_())
