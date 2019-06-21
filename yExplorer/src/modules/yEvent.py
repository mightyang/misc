#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yEvent.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 03.12.2018
# Last Modified Date: 11.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase


class yEvent(yBase.yBase):
    pass


class yContainterEvent(yEvent):
    def __init__(self):
        super(yContainterEvent, self).__init__()


class yNodeEvent(yEvent):
    def __init__(self):
        super(yNodeEvent, self).__init__()
        self.node = None


class yParameterEvent(yEvent):
    def __init__(self):
        super(yParameterEvent, self).__init__()
