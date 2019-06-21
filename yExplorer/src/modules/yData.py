#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yData.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.12.2018
# Last Modified Date: 11.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase
if 'variables_defined' not in vars():
    variables_defined = True
    Y_CONTAINER = 'y_container'
    Y_NODE = 'y_node'
    Y_PARAMETER = 'y_parameter'


class yData(yBase.yBase):
    def __init__(self):
        super(yData).__init__()
        self.__parameterType = {}
        self.__nodeType = {}

    def addNodeType(self, name, node):
        self.__nodeType[name] = node

    def addParameterType(self, name, param):
        self.__parameterType[name] = param
