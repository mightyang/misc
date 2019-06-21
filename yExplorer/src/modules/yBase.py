#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yBase.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 03.12.2018
# Last Modified Date: 06.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yVersion


class yBase(object):
    '''
    It is a base class of yExplorer.
    So far, it's just for keeping version info.
    '''
    def __init__(self, *args, **kwargs):
        self.version = yVersion.yVersion(major=0, minor=0, build=0, revision=0)

    def getVersion(self):
        '''
        Return version info, format: major.minor.build.revision.
        '''
        return "%d.%d.%d.%d" % (self.version.major, self.version.minor,
                                self.version.build, self.version.revision)

    def getVersionMajor(self):
        '''
        Return major number of version.
        '''
        return self.version.major

    def getVersionMinor(self):
        '''
        Return minor number of version.
        '''
        return self.version.minor

    def getVersionBuild(self):
        '''
        Return build number of version.
        '''
        return self.version.build

    def getVersionRevision(self):
        '''
        Return revision number of version.
        '''
        return self.version.revision
