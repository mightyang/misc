#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yNode.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 18.10.2019
# Last Modified Date: 20.10.2019
# Last Modified By  : yang <mightyang@hotmail.com>

from yBase import yBase


class yNode(yBase):
    '''
    基本节点
    用于保存各种属性与方法的类
    '''

    def __init__(self):
        super(yNode, self).__init__()
        self.version.setVersion(0, 0, 0, 0)
        self.inputConnection = []

    def addAttr(self):
        # 添加属性
        pass

    def delAttr(self):
        # 删除属性
        pass

    def setInput(self, n=None, i=0):
        # 连接输入
        self.inputNodes.insert(i, n)

    def setOutput(self, n=None, i=0):
        # 连接输出
        self.outputNodes.insert(i, n)

    def getInput(self):
        # 获取输入节点
        return self.inputNodes

    def getOutput(self):
        # 获取输出节点
        return self.outputNodes


class yConnection(yBase):
    '''
    连接
    用于记录连接点的类
    '''
    def __init__(self):
        super(yConnection, self).__init__()
        self.version.setVersion(0, 0, 0, 0)


if __name__ == '__main__':
    test = yNode()
    print test.v()
