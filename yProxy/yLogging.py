#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yLogging.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 11.06.2019
# Last Modified Date: 27.06.2019
# Last Modified By  : yang <mightyang@hotmail.com>

import logging


lg = logging.getLogger(__file__)
lg.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(filename)s[line:%(lineno)d]|%(thread)d - %(levelname)s: %(message)s')
console.setFormatter(formatter)
lg.addHandler(console)
