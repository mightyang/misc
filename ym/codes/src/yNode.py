#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yNode.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 18.10.2019
# Last Modified Date: 03.11.2019
# Last Modified By  : yang <mightyang@hotmail.com>

from yBase import yBase
from yLogging import lg
from yException import yTypeErrorException, yKeyErrorException
import types


class yNode(yBase):
    '''
    基本节点
    用于保存各种属性与方法的类
    '''

    def __init__(self, name=''):
        super(yNode, self).__init__()
        self.version.setVersion(0, 0, 0, 0)
        self.inputNodes = []
        self.outputNodes = []
        self.attributes = {}
        self.funcs = {}
        self.name = name
        self.id = 0

    def addAttr(self, key='', value=None):
        # 添加属性
        if isinstance(key, str):
            self.attributes[key] = value
        else:
            lg.error(yTypeErrorException(str.__name__, type(key).__name__))

    def delAttr(self, key=''):
        # 删除属性
        if isinstance(key, str):
            if key in self.attributes:
                del self.attributes[key]
            else:
                lg.error(yKeyErrorException(key, type(self.attributes).__name__, 'attributes'))
        else:
            lg.error(yTypeErrorException(str.__name__, type(key).__name__))

    def getAttrs(self):
        return self.attributes.keys()

    def addFunc(self, key, func, *args):
        # 添加方法
        if not isinstance(key, str):
            lg.error(yTypeErrorException(str.__name__, type(key).__name__))
        elif not isinstance(func, types.FunctionType):
            lg.error(yTypeErrorException('function', type(func).__name__))
        else:
            self.funcs[key] = (func, args)

    def delFunc(self, key):
        # 删除方法
        if isinstance(key, str):
            if key in self.attributes:
                del self.attributes[key]
            else:
                lg.error(yKeyErrorException(key, type(self.attributes).__name__, 'attributes'))
        else:
            lg.error(yTypeErrorException(str.__name__, type(key).__name__))

    def setInput(self, n=None, i=0):
        # 连接输入
        if len(self.inputNodes) <= i:
            self.inputNodes.append(n)
        else:
            self.inputNodes[i] = n

    def setOutput(self, n=None, i=0):
        # 连接输出
        if len(self.inputNodes) <= i:
            self.outputNodes.append(n)
        else:
            self.outputNodes[i] = n

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

    def __init__(self, inputNode=None, outputNode=None):
        super(yConnection, self).__init__()
        self.version.setVersion(0, 0, 0, 0)
        self.setInput(inputNode)
        self.setOutput(outputNode)

    def setInput(self, node):
        if isinstance(node, yNode):
            self.inputNode = node
        elif node is None:
            self.inputNode = None
        else:
            lg.error(yTypeErrorException(yNode.__name__, type(node).__name__))

    def setOutput(self, node):
        if isinstance(node, yNode):
            self.outputNode = node
        elif node is None:
            self.inputNode = None
        else:
            lg.error(yTypeErrorException(yNode.__name__, type(node).__name__))

    def disconnect(self):
        self.inputNode = None
        self.outputNode = None

    def input(self):
        return self.inputNode

    def output(self):
        return self.outputNode


if __name__ == '__main__':
    c = yNode()
    d = yNode()
    c.setInput(d)
    c.addAttr('test', 'hhh')
    print(c.getAttrs())
    c.delAttr('haha')
