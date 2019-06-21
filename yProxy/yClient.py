#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yClient.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 10.06.2019
# Last Modified Date: 17.06.2019
# Last Modified By  : yang <mightyang@hotmail.com>

import yBase
import traceback
from yLogging import lg
import Queue
import socket


class yProxyClient(yBase.yProxyBase):
    def __init__(self, host='127.0.0.1', port=1080):
        yBase.yProxyBase.__init__(self)
        self.addr = (host, port)
        self.dstAddr = ('127.0.0.1', 11951)

    def run(self):
        lg.info(u'开始启动')
        # 检查端口是否被占用
        lg.debug(u'开始绑定端口')
        # 绑定地址
        try:
            self.s.bind(self.addr)
        except Exception:
            lg.error(u'无法绑定地址: {}:{}, 异常: \n{}'.format(self.addr[0], self.addr[1], traceback.format_exc()))
            return
        lg.debug(u'绑定地址成功')
        # test
        try:
            self.s.connect(self.dstAddr)
            print self.s.recv(self.blockSize)
            self.s.send('1231242412')
        except Exception:
            lg.error('无法连接地址: {}:{}, 异常: \n{}'.format(self.addr[0], 11951, traceback.format_exc()))
            return None


class yClientManager(yBase.yConnectThreadBase):
    def __init__(self, manager=None, addr=('127.0.0.1', 1080)):
        yBase.yConnectThreadBase.__init__(self, manager=manager, addr=addr)
        self.sAddr = ('127.0.0.1', 11951)
        self.bindAddr()
        self.recvSize = 0
        self.sendSize = 0

    def run(self):
        lg.debug(u'启动yClientManager')
        lg.debug(u'连接服务端')
        if self.connectServer():
            # 如果连接成功，则向服务器获取 worker 端口
            self.s.send('workerPort')
            self.s.recv(yBase.DATA_BLOCKSIZE)
        else:
            return
        while self.running:
            bs, addr = self.s.accept()
            worker = yClientWorker(self, bs, self.sAddr)
            worker.start()
        self.close()

    def connectServer(self):
        try:
            self.s.connect(self.sAddr)
        except Exception:
            lg.error(u'无法连接到服务器，异常信息: {}'.format(traceback.format.exc()))
            return False
        return True

    def stop(self):
        lg.debug(u'结束线程: {}'.format(self))
        self.running = False
        socket.socket().connect(self.addr)
        self.s.close()

    def close(self):
        self.running = False
        self.s.close()


class yClientWorker():
    def __init__(self, manager, browserSocket, sAddr):
        self.running = True
        self.requestDataQueue = Queue.Queue(1000)
        self.htmlQueue = Queue.Queue(1000)
        self.getterOver = False
        self.requesterOver = False
        self.getter = yClientGetter(manager=self, addr=('127.0.0.1', 0), bs=browserSocket)
        self.transfer = yClientTransfer(manager=self, addr=('127.0.0.1', 0), sAddr=sAddr)

    def start(self):
        lg.debug(u'启动 yClientWorker')
        self.getter.start()
        self.transfer.start()

    def stop(self):
        self.getter.stop()
        self.transfer.stop()
        self.running = False


class yClientTransfer(yBase.yConnectThreadBase):
    def __init__(self, manager=None, addr=('127.0.0.1', 0), sAddr=('127.0.0.1', 11951)):
        yBase.yConnectThreadBase.__init__(self, manager=manager, addr=addr)
        self.serverAddr = sAddr
        self.bindAddr()
        self.recvSize = 0

    def run(self):
        lg.debug(u'启动yTransfer')
        # 连接服务器端口
        try:
            self.s.connect(self.serverAddr)
        except Exception:
            lg.error('连接远端服务器: {} 失败'.format(self.serverAddr))
            self.stop()
            return
        lg.debug('yTransfer 等待接收 requestData')
        while self.running:
            data = self.manager.requestDataQueue.get()
            if data == 'requestDataOoOoOoOoOoOoOver':
                break
            else:
                lg.debug(data)
                # self.s.send(data)
        # 接收 html，放置到 htmlQueue
        while self.running:
            self.s.recv(yBase.DATA_BLOCKSIZE)
            if len(data) == 0:
                break
            else:
                self.manager.htmlQueue.put(data)
                self.recvSize += len(data)
        lg.debug('yTransfer receive: {} data'.format(self.recvSize))
        self.stop()

    def stop(self):
        lg.debug(u'结束线程: {}'.format(self))
        self.manager.requesterOver = True
        self.running = False
        self.s.close()


class yClientGetter(yBase.yConnectThreadBase):
    def __init__(self, manager=None, addr=('127.0.0.1', 0), bs=None):
        yBase.yConnectThreadBase.__init__(self, manager=manager, addr=addr)
        self.browserSocket = socket
        self.bindAddr()

    def run(self):
        lg.debug(u'启动yGetter')
        dataSize = 0
        data = ''
        # 接收浏览器 requestData
        lg.debug(u'yGetter 等待接收浏览器 requestData 信息')
        while self.running:
            data = self.browserSocket.recv(yBase.DATA_BLOCKSIZE)
            self.manager.requestDataQueue.put(data)
            if '\r\n\r\n' in data:
                break
        self.manager.requestDataQueue.put('requestDataOoOoOoOoOoOoOver')
        dataSize += len(data)
        # 接收 html 信息，并转发给浏览器
        while self.running:
            data = self.manager.htmlQueue.get()
            if data == 'htmlDataOoOoOoOoOoOoOver':
                break
            else:
                self.s.send(data)
        self.stop()

    def stop(self):
        lg.debug(u'结束线程: {}'.format(self))
        self.manager.getterOver = True
        self.manager.htmlQueue.put('getterOver')
        self.running = False
        self.s.close()


if __name__ == '__main__':
    test = yClientManager()
    test.start()
