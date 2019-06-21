#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yParameter.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.12.2018
# Last Modified Date: 13.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yKit
import yStructure
import logging
import yData
import exceptions


class yParameterStructure(yStructure.yStructure):
    def __init__(self):
        super(yParameterStructure, self).__init__()
        self.structureClass = yData.Y_PARAMETER


class yInt(yParameterStructure):
    def __new__(cls, value=0):
        if isinstance(value, int):
            return object.__new__(cls, value)
        else:
            logging.error('TypeError: need "int" type, but receive a "{0}" type.'.format(type(value).__name__))

    def __init__(self, value=0):
        super(yInt, self).__init__()
        if isinstance(value, int):
            self.__val = value
        else:
            logging.error('TypeError: need "int" type, but receive a "{0}" type.'.format(type(value).__name__))

    def __str__(self):
        return str(self.__val)

    def __repr__(self):
        return str(self.__val)

    def __add__(self, value):
        return self.__val + value

    def __sub__(self, value):
        return self.__val - value

    def __or__(self, value):
        return self.__val | value

    def __cmp__(self, value):
        if self.__val > value:
            return 1
        elif self.__val < value:
            return -1
        else:
            return 0

    def __eq__(self, value):
        return self.__val == value

    def __ne__(self, value):
        return self.__val != value

    def __lt__(self, value):
        return self.__val < value

    def __le__(self, value):
        return self.__val <= value

    def __gt__(self, value):
        return self.__val > value

    def __ge__(self, value):
        return self.__val >= value


class yStr(yParameterStructure):
    def __new__(cls, value=0):
        if isinstance(value, str):
            return object.__new__(cls, value)
        else:
            logging.error('TypeError: need "str" type, but receive a "{0}" type.'.format(type(value).__name__))

    def __init__(self, value=''):
        super(yStr, self).__init__()
        if isinstance(value, str):
            self.__val = value
        else:
            logging.error('TypeError: need "str" type, but receive a "{0}" type.'.format(type(value).__name__))

    def __str__(self):
        return self.__val

    def __repr__(self):
        return self.__val

    def __len__(self):
        return len(self.__val)

    def __add__(self, value):
        return self.__val + str(value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, name, value):
        pass


class yEnum(yParameterStructure):
    def __new__(cls, value=[]):
        if isinstance(value, list):
            return object.__new__(cls, value)
        else:
            logging.error('TypeError: need "list" type, but receive a "{0}" type.'.format(type(value).__name__))

    def __init__(self, value=[]):
        super(yEnum, self).__init__()
        if isinstance(value, list):
            self.__val = value
        else:
            logging.error('TypeError: need "list" type, but receive a "{0}" type.'.format(type(value).__name__))

    def __str__(self):
        return str(self.__val)

    def __repr__(self):
        return str(self.__val)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__val[index]
        else:
            logging.error('TypeError: need "int" type, but receive a "{0}" type.'.format(type(index).__name__))

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.__val[index] = value
        else:
            logging.error('TypeError: need "int" type, but receive a "{0}" type.'.format(type(index).__name__))

    def append(self, value):
        self.__val.append(value)

    def index(self, i):
        if i in self.__val:
            return self.__val.index(i)

    def pop(self, i=-1):
        return self.__val.pop(i)


class yParameter(yKit.yKit):
    def __new__(cls, ps):
        if yParameterStructure in ps.__bases__:
            return object.__new__(cls, ps)
        else:
            logging.error('TypeError: need "yParameterStructure" type, \
                but receive a "{0}" type.'.format(type(ps).__name__))

    def __init__(self, ps):
        super(yParameter, self).__init__()
        self.paramStructure = yParameterStructure()

    def getValue(self):
        pass

    def setValue(self):
        pass

    def valueChangedEvent(self, event):
        pass


class yParamContainer(yKit.yKit):
    def __init__(self):
        super(yParamContainer, self).__init__()
        self.container = []

    def addParam(self, param):
        if isinstance(param, yParameter):
            self.container.append(param)
        else:
            logging.error('TypeError: need "yParameter" type, \
                but receive a "{0}" type.'.format(type(param).__name__))

    def delParam(self, param):
        if isinstance(param, yParameter) and param in self.container:
            self.container.remove(param)
        else:
            logging.error('TypeError: need "yParameter" type, \
                but receive a "{0}" type.'.format(type(param).__name__))

    def getParam(self, name):
        for param in self.container:
            if param.name == name:
                return param
