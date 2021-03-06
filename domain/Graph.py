
from domain.Node import *
from domain.ResultRoadList import *


def NodeCmp(nodeA:Node,nodeB:Node)->bool:  #比较两个结点是否相同 相同返回True 不同返回False
    if nodeA.label == nodeB.label and nodeA.type == nodeB.type  and nodeA.port == nodeB.port \
           and nodeA.Attemp == nodeB.Attemp:
       #注）此处Attemp比对的是Attemp的地址，只有地址相同这里判断才为True
        return True
    else :

        return False


class Graph(object):
    def __init__(self, name: str):
        self.name = name    #图的名字
        self.__nodeList: List[Node] = []  #结点的列表
        self.allNodeLabel: List[str] = []   #所有结点名字的罗列 （这里最好的设置是可以外部访问 但是外部不能修改）
        self.__nodeNum: int = 0   #结点的计数
        self.AttackTable = {} #攻击路径的邻接表
        self.AllRoad = AllListGroup() #结果列表
        self.signal = 0 #标记位（总会有用的）




    def setNodeList(self, nodeListOut: Optional[List[Node]]) -> bool:#添加新的结点
        for nodeOut in nodeListOut:
            for node in self.__nodeList:
                if NodeCmp(nodeOut,node) == True:
                    print("have the same node!")
                    return False #这里是直接退出程序 没写好，最好应该是跳过这个重复结点，继续下一次循环
            self.__nodeList.append(nodeOut)   #如果结点不在图中就输入结点
            self.__nodeNum += 1
            self.allNodeLabel.append(nodeOut.label)

        return True

    def ShowTheNodeNum(self):#返回结点数量
        #print(self.__nodeNum)
        return self.__nodeNum

    def CreatePermissionTable(self,OriginNode:Node,TargetNode:Node,PerLevel:int) -> bool:#创造权限
        if (OriginNode in self.__nodeList)==True and (TargetNode in self.__nodeList)==True:
            OriginNode.permission.permissionTable[TargetNode.label] = PerLevel
            return True
        else:
            print('Error!CreatePermissionTable')
            return False

    def ShowNodeList(self):#返回结点的列表

        return copy.deepcopy(self.__nodeList)

    def ShowVexList(self):
        return copy.deepcopy(self.__vexList)

    def checkNode(self,OutNode:Node) ->bool:#判断结点是否在图中
        if (OutNode.label in self.allNodeLabel)==True:
            #print('OK')
            return True
        else:
            #print('Error')
            return False

    def findNode(self,OutNode:Node) ->Node:
        for node in self.__nodeList:
            if  node.label == OutNode.label:
                return node

    def CoreAlgorithm(self, OutNode: Node,road:DoubleList):  # 核心算法，用以计算所有路径的攻击概率
     #   print(OutNode.label)
       # road.travel()
     #   print("done")
        if self.checkNode(OutNode) == True:
            Attacklist = self.AttackTable.get(OutNode)

            if Attacklist != [] and Attacklist != None:
                if self.signal == 0:#程序逐步推进 没有发生任何回朔
                    self.signal = 0  # 没有发生回朔
                    AnotherNode = Attacklist.pop()
                    if (AnotherNode in OutNode.permission.AttackRoadList) == False:
                        OutNode.permission.AttackRoadList.append(AnotherNode)
                    if (OutNode in AnotherNode.permission.AttackedRoadList) == False:
                        AnotherNode.permission.AttackedRoadList.append(OutNode)
                    self.CaluateOneNodeProb(OutNode,AnotherNode,road,0)
                    self.CoreAlgorithm(AnotherNode,road)

                elif self.signal == 1:   #程序从回朔状态转换到正常推进状态
                    self.signal = 0
                    self.AllRoad.listGroupAppend(road)
                    lastAttmp = road.findNodeAttmp(OutNode)
                    self.AllRoad.CopyListGroup(road,lastAttmp)
                    newRoad = self.AllRoad.ListGroup.pop()
                   # road.travel()
                   # print('done')

                    #newRoad.travel()

                    AnotherNode = Attacklist.pop()
                    OutNode.permission.AttackRoadList.append(AnotherNode)
                    AnotherNode.permission.AttackedRoadList.append(OutNode)
                    self.CaluateOneNodeProb(OutNode,AnotherNode,newRoad,0)
                    self.CoreAlgorithm(AnotherNode,newRoad)
            elif Attacklist == [] or Attacklist == None:
                if OutNode.permission.AttackedRoadList != []:
                    self.signal = 1  # 发生回朔

                    #self.AttackTable[OutNode] = copy.deepcopy(OutNode.permission.AttackRoadList)  # 这条代码会改变原本结点的地址
                    list = copy.deepcopy(OutNode.permission.AttackRoadList)

                    for i in range(len(list)):
                        list[i] = self.findNode(list[i])
                    self.AttackTable[OutNode] = list
                    AnotherNode = OutNode.permission.AttackedRoadList.pop()
                    self.CoreAlgorithm(AnotherNode,road)
                else:
                    self.AllRoad.listGroupAppend(road)
                    return True
        else:
            print(OutNode)
            print("Error!The Node isn't in the Graph")




    def CaluateOneNodeProb(self,AttackNode:Node,AttackedNode:Node,RoadList:DoubleList,StartLevel:int):
        self.CreatePermissionTable(AttackNode,AttackedNode,StartLevel)#默认权限为StartLevel
        signal = 1
#这里存在一个跳权限的问题 及 如果 新加入的权限为2 权限为1 的点造成的影响会直接跳过
        AttackPerLevel = AttackNode.permission.permissionTable['%s'%(AttackedNode.label)] #得到攻击结点拥有的权限
        for AttempRoad in AttackedNode.Attemp:#遍历
            if AttempRoad.requestPermission == AttackPerLevel:
                if RoadList.findBlock(AttempRoad)!= False:
                    return False
                newData = [AttackedNode,AttempRoad]
                RoadList.coverAppend(newData)
               # RoadList.head.data[0] = RoadList.head.data[0]/AttempRoad.prob
                NextLevel = AttempRoad.result
                signal = AttempRoad.prob
                self.CaluateOneNodeProb(AttackNode,AttackedNode,RoadList,NextLevel)

        return True




































#以下为测试数据
GraphA = Graph('GraphA')
#建立攻击模版
aAttempV0 = Attemp('StartPoint',['Strat'],0,0,1)
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

road = DoubleList()
road.append([Anode,aAttempV0])
GraphA.CoreAlgorithm(Anode,road)
print(GraphA.AllRoad.ListNumber)
for i in GraphA.AllRoad.ListGroup:
    i.travel()
    print(i.head.data[0])
