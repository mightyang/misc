#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yNode.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.12.2018
# Last Modified Date: 11.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yKit
import yStructure
import yParameter
import yPort
import types
import logging


class yNodeStructure(yStructure.yStructure):
    def __init__(self):
        super(yNodeStructure, self).__init__()
        self.parameters = yParameter.yParamContainer()
        self.input = []
        self.output = []
        self.filter = ['all']

    def go(self, values):
        '''
        get value from input node, and return result to output node.
        '''
        return None

    def setInputEvent(self, event):
        '''
        Set input event
        '''
        pass

    def setOutputEvent(self, event):
        '''
        Set output event
        '''
        pass


class yNode(yKit.yKit):
    def __new__(cls, ns):
        if yNodeStructure in ns.__bases__:
            return object.__new__(cls, ns)
        else:
            logging.error('TypeError: need "yNodeStructure" type, but receive a "{0}" type.'.format(type(ns).__name__))

    def __init__(self, ns):
        super(yNode, self).__init__()
        self.nodeStructure = ns()

    def __getitem__(self, key):
        pass

    def __setitem__(self, key):
        pass

    def setInput(self, input=None, i=0):
        iNum = len(self.input)
        if iNum > i or iNum < 0:
            logging.error('IndexError: list index out of range')
        else:
            self.input[i].connect(input)

    def goWrapper(self):
        if self.input:
            result = []
            for inputNode in self.input:
                try:
                    result.append(inputNode.goWrapper())
                except Exception, e:
                    raise e
            self.go(result)

    def init(self):
        # initialize parameters.
        for param in self.nodeStructure.parameters:
            if isinstance(param, yParameter.yParameter):
                self.parameters.append(param)
            else:
                logging.error('TypeError: need "yParameterStructure" type, but receive a "{0}" type.'.format(type(param).__name__))
        # initialize inputs
        for port in self.nodeStructure.input():
            if isinstance(port, yPort.yPort):
                self.input.append(port)
            else:
                logging.error(
                    'TypeError: need "yPort" type, but receive a "{0}" type.'.format(type(port).__name__))

    def __getattr__(self, name):
        if hasattr(self.nodeStructure, name):
            if isinstance(getattr(self.nodeStructure, name), types.MethodType):

                def wrapper(*args, **kwargs):
                    getattr(self.nodeStructure, name)(*args, **kwargs)

                return wrapper
            else:
                return getattr(self.nodeStructure, name)

        else:
            logging.error('there is no attribute: {}'.format(name))
