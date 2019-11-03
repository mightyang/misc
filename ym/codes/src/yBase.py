#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yBase.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 18.10.2019
# Last Modified Date: 03.11.2019
# Last Modified By  : yang <mightyang@hotmail.com>

from yMisc import yVersion


class yBase(object):
    '''
    基础类
    所有的类都继承自该类
    '''
    version = None

    def __init__(self):
        # 初始化版本号
        self.version = yVersion()

    def v(self):
        # 返回版本号
        return self.version.version()
