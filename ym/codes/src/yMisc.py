#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yMisc.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 18.10.2019
# Last Modified Date: 20.10.2019
# Last Modified By  : yang <mightyang@hotmail.com>


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
            print('major need a int number, but receive a {}'.format(type(num)))

    def setMinor(self, num):
        if isinstance(num, int):
            self.__minor = num
        else:
            print('minor need a int number, but receive a {}'.format(type(num)))

    def setRevision(self, num):
        if isinstance(num, int):
            self.__revision = num
        else:
            print('revision need a int number, but receive a {}'.format(type(num)))

    def setBuild(self, num):
        if isinstance(num, int):
            self.__build = num
        else:
            print('build need a int number, but receive a {}'.format(type(num)))

    def setVersion(self, major, minor, revision, build):
        self.setMajor(major)
        self.setMinor(minor)
        self.setRevision(revision)
        self.setBuild(build)
