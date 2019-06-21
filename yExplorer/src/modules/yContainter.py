#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yContainter.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.12.2018
# Last Modified Date: 11.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yStructure
import yNode
import logging
import yKit
import types


class yContainerStructure(yStructure.yStructure):
    def __init__(self):
        super(yContainerStructure, self).__init__()
        self.nodes = []


class yContainer(yKit.yKit):
    def __new__(cls, cs):
        if isinstance(cs, yContainerStructure):
            return object.__new__(cls, cs)
        else:
            logging.error('TypeError: need "yContainerStructure" type, but receive a "{0}" type.'.format(type(cs).__name__))

    def __init__(self, cs):
        super(yContainer, self).__init__()
        self.containerStructure = cs

    def __getattr__(self, name):
        if hasattr(self.containerStructure, name):
            if isinstance(
                    getattr(self.containerStructure, name), types.MethodType):

                def wrapper(*args, **kwargs):
                    getattr(self.containerStructure, name)(*args, **kwargs)

                return wrapper
            else:
                return getattr(self.containerStructure, name)

        else:
            logging.error('Error: there is no attribute: {}'.format(name))

    def addNode(self, node):
        if isinstance(node, yNode.yNode):
            self.nodes.append(node)
        else:
            logging.error(
                'TypeError: need "yNode" type, but receive a "{0}" type.'.format(type(node).__name__))

    def preAddNodeEvent(self, event):
        '''
        Called before adding node.
        '''
        pass

    def postAddNodeEvent(self, event):
        '''
        Called after adding node.
        '''
        pass
