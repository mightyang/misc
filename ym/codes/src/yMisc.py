#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yMisc.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 18.10.2019
# Last Modified Date: 03.11.2019
# Last Modified By  : yang <mightyang@hotmail.com>

from yException import yTypeErrorException
from yLogging import lg


class yVersion():
    __major = 0
    __minor = 0
    __revision = 0
    __build = 0

    def __init__(self, major=0, minor=0, revision=0, build=0):
        self.setVersion(major, minor, revision, build)

    def version(self):
        return "{}.{}.{}.{}".format(self.__major, self.__minor, self.__revision, self.__build)

    def setMajor(self, num):
        if isinstance(num, int):
            self.__major = num
        else:
            lg.error('TypeError: major need a int, but receive a {}'.format(type(num).__name__))
            raise yTypeErrorException(int.__name__, type(num).__name__)

    def setMinor(self, num):
        if isinstance(num, int):
            self.__minor = num
        else:
            lg.error('TypeError: minor need a int, but receive a {}'.format(type(num).__name__))
            raise yTypeErrorException(int.__name__, type(num).__name__)

    def setRevision(self, num):
        if isinstance(num, int):
            self.__revision = num
        else:
            lg.error('TypeError: revision need a int, but receive a {}'.format(type(num).__name__))
            raise yTypeErrorException(int.__name__, type(num).__name__)

    def setBuild(self, num):
        if isinstance(num, int):
            self.__build = num
        else:
            lg.error('TypeError: build need a int, but receive a {}'.format(type(num).__name__))
            raise yTypeErrorException(int.__name__, type(num).__name__)

    def setVersion(self, major, minor, revision, build):
        self.setMajor(major)
        self.setMinor(minor)
        self.setRevision(revision)
        self.setBuild(build)


if __name__ == '__main__':
    t = yVersion()
    t.setVersion(1, 3, 4, 'a')
