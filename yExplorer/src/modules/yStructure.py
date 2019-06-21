#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yStructure.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 03.12.2018
# Last Modified Date: 10.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase


class yStructure(yBase.yBase):
    '''
    A basic structure class.
    '''

    def __init__(self):
        super(yStructure, self).__init__()
        self.name = ''
        self.structureClass = ''
