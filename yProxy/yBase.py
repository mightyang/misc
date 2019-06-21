#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yBase.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.06.2019
# Last Modified Date: 21.06.2019
# Last Modified By  : yang <mightyang@hotmail.com>

import re


DATA_BLOCKSIZE = 1024
MAX_CONNECTIONS = 1000


class yVersion():
    def __init__(self, major=0, minor=0, build=0, revision=0):
        self.major = major
        self.minor = minor
        self.build = build
        self.revision = revision


class yBase(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.version = yVersion()


if __name__ == '__main__':
    pass
