#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yException.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 02.11.2019
# Last Modified Date: 03.11.2019
# Last Modified By  : yang <mightyang@hotmail.com>


class yException(Exception):
    '''
    基本异常
    '''
    def __init__(self):
        self.err = ''


class yTypeErrorException(yException):
    def __init__(self, recvType, needType):
        super(yTypeErrorException, self).__init__()
        self.err = "TypeError: Parameter need a '{}', but receive a '{}'".format(recvType, needType)

    def __str__(self):
        return self.err


class yKeyErrorException(yException):
    def __init__(self, key, containerType, containerName):
        super(yKeyErrorException, self).__init__()
        self.err = "KeyError:  '{}' not in '{}' {}".format(key, containerName, containerType)

    def __str__(self):
        return self.err
