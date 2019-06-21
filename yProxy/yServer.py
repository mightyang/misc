#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yServer.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.06.2019
# Last Modified Date: 17.06.2019
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase
from yLogging import lg
import urllib
import Queue
import socket


class yProxyServer(yBase.yProxyBase):
    def __init__(self):
        yBase.yProxyBase.__init__(self)
        self.max_conn = 1000
        self.passwords = ['123456']
        self.managers = []

    def run(self):
        pass

    def startManager(self):
        pass

    def startWorker(self):
        pass

    def restart(self):
        lg.debug(u'重启服务端')
        self.stop()
        self.start()

    def setPort(self, port):
        # 更改端口
        self.addr[1] = port
        lg.debug(u'更改端口为: {}'.format(port))
        self.restart()

    def checkPassword(self, conn):
        return True

    def comp(self, data):
        return data

    def unComp(self, data):
        return data

    def readConfig(self):
        pass

    def saveConfig(self):
        pass


class yManager(yBase.yConnectThreadBase):
    def __init__(self, manager=None, addr=('127.0.0.1', 11951)):
        yBase.yConnectThreadBase.__init__(self, manager=manager, addr=addr)
        self.bindAddr()
        self.recvSize = 0
        self.sendSize = 0

    def run(self):
        lg.debug(u'启动yTransfer')
        while self.running:
            # 先启动预备进程
            worker = yWorker()
            worker.start()
            if worker.isReady():
                transferAddr = worker.getTransferAddr()
            conn, addr = self.s.accept()
        self.close()

    def stop(self):
        lg.debug(u'结束线程: {}'.format(self))
        self.running = False
        socket.socket().connect(self.addr)
        self.s.close()

    def close(self):
        self.running = False
        self.s.close()


class yWorker():
    def __init__(self, manager=None, url=''):
        self.running = True
        self.requestDataQueue = Queue.Queue(1000)
        self.htmlQueue = Queue.Queue(1000)
        self.getterOver = False
        self.requesterOver = False
        self.getter = None
        self.transfer = None

    def getTransferAddr(self):
        return self.transfer.getAddr()

    def start(self):
        self.getter = yGetter(manager=self, addr=('127.0.0.1', 0))
        self.transfer = yTransfer(manager=self, addr=('127.0.0.1', 0))
        self.getter.start()
        self.transfer.start()

    def stop(self):
        self.getter.stop()
        self.transfer.stop()
        self.running = False


class yTransfer(yBase.yConnectThreadBase):
    def __init__(self, manager=None, addr=('127.0.0.1', 0)):
        yBase.yConnectThreadBase.__init__(self, manager=manager, addr=addr)
        self.bindAddr()
        self.recvSize = 0

    def run(self):
        lg.debug('启动yTransfer')
        # 接收 requestData，并放到 queue 里
        while self.running:
            data = self.s.recv(yBase.DATA_BLOCKSIZE)
            if len(data) != 0:
                self.manager.requestDataQueue.put(data)
            else:
                self.manager.requesterOver = True
                self.manager.requestDataQueue.put('requesterOver')
        # 发送 html 内容给 客户端
        while self.running:
            data = self.manager.htmlQueue.get()
            if self.manager.getterOver and data == 'getterOver':
                break
            else:
                self.s.send(data)
                self.recvSize += len(data)
        lg.debug('yTransfer receive: {} data'.format(self.recvSize))
        self.stop()

    def stop(self):
        lg.debug('结束线程: {}'.format(self))
        self.manager.requesterOver = True
        self.manager.requestDataQueue.put('requesterOver')
        self.running = False
        self.s.close()


class yGetter(yBase.yConnectThreadBase):
    def __init__(self, manager=None, addr=('127.0.0.1', 0), requestData=''):
        yBase.yConnectThreadBase.__init__(self, manager=manager, addr=addr)
        self.bindAddr()

    def run(self):
        lg.debug('启动yGetter')
        requestData = ''
        data = ''
        # 从 queue 里接收 requestData 信息
        while True:
            data = self.manager.requestDataQueue.get()
            if data == 'requesterOver' and self.manager.requesterOver:
                break
            else:
                requestData += data
        # 解析 requestData，访问网址
        f = urllib.urlopen(self.url)
        dataSize = 0
        while self.running:
            html = f.read(yBase.DATA_BLOCKSIZE)
            if len(html) != 0:
                self.manager.htmlQueue.put(html)
                dataSize += len(html)
                lg.debug('yGetter put: {} data'.format(dataSize))
            else:
                break
        self.stop()

    def stop(self):
        lg.debug('结束线程: {}'.format(self))
        self.manager.getterOver = True
        self.manager.htmlQueue.put('getterOver')
        self.running = False
        self.s.close()


if __name__ == '__main__':
    test = yProxyServer()
    test.start()
