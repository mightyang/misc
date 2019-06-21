#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : test.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 20.03.2019
# Last Modified Date: 20.03.2019
# Last Modified By  : yang <mightyang@hotmail.com>

from PySide2 import QtWidgets
import sys
import time

def tf():
    for i in range(4):
        print("waiting {}".format(i))
        time.sleep(5)

app = QtWidgets.QApplication(sys.argv)
test = QtWidgets.QWidget()
l = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel('test')
l.addWidget(label)
test.setLayout(l)
test.show()
#  t = threading.Thread(target=test.show)
#  t.start()
sys.exit(app.exec_())
