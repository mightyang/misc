#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : test.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 26.06.2019
# Last Modified Date: 26.06.2019
# Last Modified By  : yang <mightyang@hotmail.com>

import re

print(re.findall(r'.+\s(http://){0,1}(.+)\s.+', 'GET http://baidu.com/?search= HTTP/1.1'))
