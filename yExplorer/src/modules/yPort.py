#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yPort.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.12.2018
# Last Modified Date: 10.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase


class yPort(yBase.yBase):
    def __init__(self, name=""):
        self.name = name
        self.nodes = []

    def connect(self, node):
        if node not in self.node:
            self.nodes.appned(node)

    def disconnect(self, node):
        self.node.remove(node)

    def rename(self, name):
        self.name = name
