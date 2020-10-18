from domain.Graph import *
from domain.Node import *
from domain.permission import *
from domain.Attemp import *
from domain.ResultRoadList import *

def CoreAlgorithm(Graph:Graph,OutNode:Node):#这里可以写在类里，待商榷
    print(OutNode.label)
    signal = 0 #标记符号，用以区分是否回朔
    if Graph.checkNode(OutNode)==True:
        Attacklist = GraphA.AttackTable.get(OutNode)
        if Attacklist != [] and Attacklist != None:
            signal = 0#没有发生回朔
            AnotherNode = Attacklist.pop()
            OutNode.permission.AttackRoadList.append(AnotherNode)
            AnotherNode.permission.AttackedRoadList.append(OutNode)
            CoreAlgorithm(Graph,AnotherNode)
        elif Attacklist ==[] or Attacklist == None:
            if OutNode.permission.AttackedRoadList !=[]:
                signal = 1#发生回朔
                Graph.AttackTable[OutNode]=copy.deepcopy(OutNode.permission.AttackRoadList)#这条代码会改变原本结点的地址
                AnotherNode = OutNode.permission.AttackedRoadList.pop()
                CoreAlgorithm(Graph,AnotherNode)
            else:
                return True
    else:
        print(Graph.checkNode(OutNode))
        print(OutNode)
        print("Error!The Node isn't in the Graph")



GraphA = Graph('GraphA')
#建立攻击模版
bAttempV0 = Attemp('B(v0)', ['CVE-1'], 1, 1, 0.5)
bAttempV1 = Attemp('B(v1)', ['CVE-2'], 0, 1, 0.2)
cAttempV0 = Attemp('C(v0)', ['CVE-3'], 0, 1, 0.1)
cAttempV1 = Attemp('C(v1)', ['CVE-4'], 1, 2, 0.3)
cAttempV2 = Attemp('C(v2)', ['CVE-5'], 2, 3, 0.7)
dAttempV0 = Attemp('D(v0)', ['CVE-6'], 0, 0, 0.4)
eAttempV0 = Attemp('E(v0)', ['CVE-7'], 0, 0, 0.2)
fAttempV0 = Attemp('F(v0)', ['CVE-8'], 0, 0, 0.9)

#建立点：
Anode = Node('nodeA',0,[8086],[])
Bnode = Node('nodeB',1,[1123],[bAttempV0,bAttempV1])
Cnode = Node('nodeC',0,[2222],[cAttempV0,cAttempV1,cAttempV2])
Dnode = Node('nodeD',1,[2231],[dAttempV0])
Enode = Node('nodeE',1,[3112],[eAttempV0])
Fnode = Node('nodeF',2,[4445],[fAttempV0])
GraphA.setNodeList([Anode,Bnode,Cnode,Dnode,Enode,Fnode])

#建立邻接多重表
GraphA.AttackTable = {
    Anode:[Bnode,Cnode,Dnode],
    Bnode:[Cnode,Enode],
    Cnode:[Enode],
    Dnode:[Cnode,Fnode],
    Enode:[Fnode],
    Fnode:[]
}

CoreAlgorithm(GraphA,Anode)

for node in GraphA.ShowNodeList():
    print(node.toString())
