#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yKit.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 03.12.2018
# Last Modified Date: 10.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase


class yKit(yBase.yBase):
    '''
    Base class for container, node, parameter.
    '''

    def __init__(self, *args, **kwargs):
        super(yKit, self).__init__(*args, **kwargs)

    def preCreateEvent(self, event):
        '''
        Called before create kit.
        '''
        pass

    def postCreateEvent(self, event):
        '''
        Called after create kit.
        '''
        pass
