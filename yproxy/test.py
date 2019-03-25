#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : test.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 23.03.2019
# Last Modified Date: 25.03.2019
# Last Modified By  : yang <mightyang@hotmail.com>

#  import urllib
#  url = 'http://s1.bdstatic.com/r/www/cache/static/global/img/quickdelete_33e3eb8.png'
#  #  url = 'http://www.baidu.com/'
#  test = urllib.urlopen(url)
#  f = open('C:/test.png', 'wb')
#  f.write(test.read())
#  test.close()
#  f.close()

import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception, e:
    raise e
print 'bind port'
s.bind(('', 55689))
print 'start listen'
s.listen(5)

while True:
    try:
        conn, addr = s.accept()
        data = conn.recv(1024)
        print 'receive: {}'.format(data)
    except Exception, e:
        raise e

s.close()
