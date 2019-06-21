#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : test.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 03.12.2018
# Last Modified Date: 13.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yNode
import yParameter


class test(yNode.yNodeStructure):
    def __init__(self):
        super(test, self).__init__()

    def parameterInit(self):
        pass


class a():
    pass


class b(a):
    pass


t = yParameter.yEnum([1, 23, 4, 5, 6])
print t[0]
t.append(123)
print t
print t.index(23)
print t.pop()
print t
