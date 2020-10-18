from domain.Node import *
from typing import List, Union, Optional

class permission(object):
    def __init__(self,permissionTable:dict,AttackRoadList:List,AttackedRoadList:List):
        self.permissionTable = permissionTable  #权限表
        self.AttackRoadList = AttackRoadList    #该结点所有攻击的路径
        self.AttackedRoadList = AttackedRoadList    #所有攻击该结点的路径
        self.RoadList = []


    def toString(self):
        data = {
            "permissionTable": self.permissionTable,
            "attackRoadList" =
        }

