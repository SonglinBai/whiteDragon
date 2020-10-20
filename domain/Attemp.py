from typing import List, Union, Optional

class Attemp(object):
    def __init__(self,label:str,valueList:list,requestPermission:int,result:int,prob:float):
        self.valueList = valueList
        self.requestPermission = requestPermission#漏洞需要的权限等级
        self.prob = prob
        self.label = label#漏洞的名字
        self.result = result#漏洞造成的影响

    def toJson(self):
        data = {
            "label": self.label,
            "vulneList": self.valueList,
            "requestPermission": self.requestPermission,
            "prob": self.prob,
            "result": self.result
        }
        return data