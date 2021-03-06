from typing import List, Union, Optional
import copy
from domain.permission import *

from domain.Attemp import *
class Node(object):
    def __init__(self,label: str,type:int,port:list,Attemp:List[Attemp]):
        self.label = label#编号
        self.type = type #0-主机 1-服务器
        self.port = port#开放端口
        self.Attemp = Attemp#攻击模版
        self.permission = permission({},[],[]) #权限表 权限表默认创建时为空


    def toString(self):
        data = {
            "label": self.label,
            "type": self.type,
            "port": self.port,
            "attemp": [],
            "permission": self.permission
        }
        for attemp in self.Attemp:
            data["attemp"].append(attemp.toString())

        return data



















"""
#以下为测试数据
AttempC = Attemp("add",["CVE-11"],0.8)
nodeA = Node('hi',1,[8086],AttempC)
#print(nodeA.label)
"""