from domain.Node import *
from domain.Attemp import *


class block(object):
    def __init__(self, data: [str, Attemp]):
        self.data = data
        self.next: block = None
        self.prev: block = None


class DoubleList(object):
    def __init__(self):
        self.head = block([1])  # 头结点，初始概率为1
        self.length = 0
        self.allLabelName = []

    def travel(self):  # 循环遍历所有结点
        result = ""
        cur = self.head  # 创立游标
        for i in range(self.length):
            NodeName = cur.next.data[0]  # 结点名字
            AttempName = cur.next.data[1].label  # 漏洞名字
            prob = cur.next.data[1].prob  # 漏洞概率
            cur = cur.next
            print("(%s,%s,%s)->" % (NodeName, AttempName, prob), end=" ")
            result += str("(%s,%s,%s)->" % (NodeName, AttempName, prob))
        result += str(self.head.data[0])
        return result

    def append(self, newData: [str, Attemp]):  # 在结尾处添加新的结点
        NewBlock = block(newData)
        cur = self.head  # 创建游标
        if self.length == 0:
            self.head.next = NewBlock
            NewBlock.prev = self.head
            self.length += 1
            self.head.data[0] = self.head.data[0] * newData[1].prob


        else:
            for i in range(self.length):
                cur = cur.next
            NewBlock.prev = cur
            cur.next = NewBlock
            self.length += 1
            self.head.data[0] = self.head.data[0] * newData[1].prob

    def calculateNodeProb(self,nodename:str)->int:
        cur = self.head.next #创建游标
        prob = 1
        if self.length == 0:
            print('error')
            return False
        else:
            for i in range(self.length):
                if cur.data[0]==nodename:

                    return prob
                else:
                    if cur.data[0]==cur.next.data[0]:
                        cur = cur.next
                    else:
                        prob = prob * cur.data[1].prob
                        cur = cur.next











    def coverAppend(self, newData: [str, Attemp]):  # 用以计算一个结点的路径概率
        NewBlock = block(newData)
        cur = self.head  # 创建游标
        if self.length == 0:
            self.head.next = NewBlock
            NewBlock.prev = self.head
            self.length += 1
            self.head.data[0] = self.head.data[0] * newData[1].prob
        else:
            for i in range(self.length):
                cur = cur.next
            if cur.data[0] == newData[0]:
                self.head.data[0] = self.head.data[0] / cur.data[1].prob
            NewBlock.prev = cur
            cur.next = NewBlock
            self.length += 1
            self.head.data[0] = self.head.data[0] * newData[1].prob

    def findBlock(self, AttempName: Attemp):  # 查询漏洞是否在路径中
        cur = self.head.next  # 创建游标
        for i in range(self.length):
            if cur.data[1].label == AttempName.label:
                #     print("find out!")
                return cur
            else:
                cur = cur.next

        # print("fail !")
        return False

    def findNodeAttmp(self, nodename:str):  # 查询一个结点的最后路径
        cur = self.head.next
        signal = 0
        for i in range(self.length):
            if cur.data[0] == nodename:
                signal = 1
                cur = cur.next
            else:
                if signal == 0:
                    cur = cur.next
                else:
                    # print(cur.prev.data[0].label)
                    # print(cur.prev.data[1].label)
                    return cur.prev


class AllListGroup(object):
    def __init__(self):
        self.ListGroup = []  # 所有路径的列表
        self.ListNumber = 0  # 所有路径的个数

    def CopyListGroup(self, CopiedRoad: DoubleList, EndCopyBlock: block):
        # 被复制的双向链表， 复制到哪一个结点，复制后的结果
        NewRoad = DoubleList()
        NewRoad.head = block([1])
        curCopied = CopiedRoad.head  # 创建复制表的游标
        NewRoad.head = copy.deepcopy(CopiedRoad.head)
        NewRoad.head.data[0] = 1
        for i in range(CopiedRoad.length):
            if curCopied.next.data == EndCopyBlock.data:
                data = curCopied.next.data
                NewRoad.append(data)
                self.ListGroup.append(NewRoad)
                # print("done")
                return True
            else:
                data = curCopied.next.data
                NewRoad.append(data)
                curCopied = curCopied.next

    def listGroupAppend(self, road: DoubleList):
        self.ListGroup.append(road)
        self.ListNumber = self.ListNumber + 1

    def clear(self):
        self.ListGroup.clear()
        self.ListNumber = 0




# testList = DoubleList()
#
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
# Anode = Node('nodeA',0,[],[8086],[])
# Bnode = Node('nodeB',1,[],[1123],[bAttempV0,bAttempV1])
# Cnode = Node('nodeC',0,[],[2222],[cAttempV0,cAttempV1,cAttempV2])
# Dnode = Node('nodeD',1,[],[2231],[dAttempV0])
# Enode = Node('nodeE',1,[],[3112],[eAttempV0])
# Fnode = Node('nodeF',2,[],[4445],[fAttempV0])
#
# testList.append(['nodeC',cAttempV0])
# testList.append(['nodeC',cAttempV1])
# testList.append(['nodeC',cAttempV2])
# testList.append(['nodeE',eAttempV0])
# testList.append(['nodeF',fAttempV0])
# m = testList.findNodeAttmp('nodeC')
# allList = AllListGroup()
# blacklist = DoubleList()
# testList.travel()
# print(testList.head.data[0])
# print(testList.calculateNodeProb('nodeE'))
#
#
#
#
#
# c = testList.findBlock(fAttempV0)






