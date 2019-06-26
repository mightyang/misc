#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yProxy.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 23.06.2019
# Last Modified Date: 26.06.2019
# Last Modified By  : yang <mightyang@hotmail.com>


import Queue
import traceback
from yLogging import lg
import socket
import threading


DATA_BLOCKSIZE = 4096
MAX_CONNECTIONS = 1000
QUEUE_LAST_CODE_BASE64 = 'UVVFVUVfTEFTVF9DT0RFX0JBU0U2NA=='
TRANSFER_LAST_CODE_BASE64 = 'VFJBTlNGRVJfTEFTVF9DT0RFX0JBU0U2NA=='
clientSettings = {
    'ports': (1080)
}
serverSettings = {
    'ports': (11951)
}


class yVersion(object):
    def __init__(self, major=0, minor=0, build=0, revision=0):
        self.major = major
        self.minor = minor
        self.build = build
        self.revision = revision


class yBase(object):
    def __init__(self, parent=None):
        self.parent = None
        self.version = yVersion()


class yProxy(yBase):
    def __init__(self):
        self.managers = []
        self.addrList = []
        self.dataStatistics = ()

    def start(self):
        pass

    def stop(self):
        pass

    def readSettings(self):
        pass

    def saveSettings(self):
        pass


class yProxyClient(yProxy):
    def __init__(self):
        self.addrList = [('127.0.0.1', 1080)]

    def start(self):
        # 加载配置
        # 启动管理器
        for addr in self.addrList:
            manager = yManager.yClientManager()
            self.managers.append(manager)
            manager.start()

    def stop(self):
        pass


class yProxyServer(yProxy):
    def __init__(self):
        self.addrList = [('127.0.0.1', 11951)]
        self.log = ''
        self.logLevel = ''
        self.logPath

    def start(self):
        # 加载配置
        # 启动管理器
        for addr in self.addrList:
            manager = yManager.yClientManager()
            self.managers.append(manager)
            manager.start()

    def stop(self):
        pass


class yThread(threading.Thread, yBase):
    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        yBase.__init__(self, parent)
        self.s = socket.socket()

    def run(self):
        pass

    def stop(self):
        pass


class yManager(yThread):
    def __init__(self, parent=None, addr=('127.0.0.1', 0)):
        yThread.yThread.__init__(self, parent)
        self.requestData = Queue.Queue()
        self.addr = addr

    def bindAddr(self):
        # 绑定端口
        try:
            self.s.bind(self.addr)
        except Exception:
            lg.error(u'绑定地址: {} 失败, 错误信息: \n{}'.format(self.addr, traceback.format_exc()))
            return False
        return True

    def setAddr(self, addr):
        self.addr = addr

    def stop(self):
        self.dataTransfer.stop()
        self.s.close()


class yClientManager(yManager):
    def __init__(self, parent=None, addr=('127.0.0.1', 0)):
        yManager.__init__(self, parent, addr)

    def run(self):
        # 绑定本地端口
        # 连接远程服务器
        # 等待浏览器接入
        # 启动 worker 线程
        self.browserTransfer.start()

    def stop(self):
        self.s.close()


class yServerManager(yManager):
    def __init__(self, parent=None, addr=('127.0.0.1', 0)):
        yManager.__init__(self, parent, addr)

    def run(self):
        pass

    def stop(self):
        self.dataTransfer.stop()
        self.netTransfer.stop()
        self.s.close()


class yWorker(yThread):
    def __init__(self, parent=None):
        yThread.__init__(self, parent)

    def run(self):
        pass

    def stop(self):
        pass


class yClientWorker(yWorker):
    def __init__(self):
        yWorker.__init__(self)

    def run(self):
        # 绑定本地端口
        # 等待接入
        pass

    def stop(self):
        self.dataTransfer.stop()
        self.browserTransfer.stop()


class yServerWorker(yWorker):
    def __init__(self):
        yWorker.__init__(self)

    def run(self):
        pass

    def stop(self):
        self.dataTransfer.stop()
        self.netTransfer.stop()


class yTransfer(yThread):
    def __init__(self, parent=None, conn=None):
        yThread.__init__(self, parent, conn)
        self.conn = conn
        self.requestQueue = parent.requestQueue
        self.htmlQueue = parent.htmlQueue

    def run(self):
        pass

    def stop(self):
        pass

    def encode(self, data):
        return data

    def decode(self, data):
        return data


class yClientDataTransfer(yTransfer):
    """
    客户端中用来与服务端传递数据的类
    1. 传递 manager 的 requestQueue 中的加密请求给服务端
    2. 从服务端接收访问的网页内容，存储到 manager 的 htmlQueue 中
    """
    def __init__(self, parent=None, conn=None):
        yTransfer.__init__(self, parent, conn)

    def run(self):
        # 等待 requestQueue 中的请求
        while True:
            data = self.requestQueue.get()
            # 如果 data 信息为结束信息，则结束获取
            if data == QUEUE_LAST_CODE_BASE64:
                lg.debug(u'yClientDataTransfer 请求获取结束')
                break
            # 发送请求到服务端
            self.conn.send(data)
        # 等待服务端发送要访问的网页内容
        while True:
            data = self.conn.recv(DATA_BLOCKSIZE)
            if data == TRANSFER_LAST_CODE_BASE64:
                lg.debug(u'yClientDataTransfer 网页内容获取结束')
                break
            # 将收到的网页内容存到 queue 中
            self.htmlQueue.put(data)
        # 接收完毕后结束
        self.stop()


class yClientTransfer(yTransfer):
    """
    客户端中用来与浏览器传递数据的类
    1. 接收浏览器的请求，加密后存到 manager 的 queue 里
    2. 从 manager 的 htmlQueue 中获取加密的网页内容, 解密后发给浏览器
    """
    def __init__(self, parent=None, conn=None):
        yTransfer.__init__(self, parent, conn)

    def run(self):
        # 收集 conn 的请求
        while True:
            data = self.conn.recv(DATA_BLOCKSIZE)
            if data == '\r\n0\r\n\r\n':
                pass
        # 加密请求
        # 将请求存到 requestQueue 中
        # 等待 htmlQueue 中的内容
        # 解密内容
        # 发送 htmlQueue 中的内容给浏览器
        # 发送完毕后结束
        pass


class yServerDataTransfer(yTransfer):
    """
    服务端中用来与客户端传递数据的类
    1. 从客户端接收请求
    2. 解密请求
    3. 压缩加密网页内容
    4. 发送加密后的网页内容给客户端
    """
    def __init__(self, parent=None, conn=None):
        yTransfer.__init__(self, parent, conn)

    def run(self):
        # 收集 conn 的请求
        # 解密请求
        # 发送请求到 manager 的 requestQueue 中
        # 等待 manager 的 htmlQueue 中的网页内容
        # 发送 htmlQueue中的网页内容给客户端
        # 发送完毕后结束
        pass


class yServerTransfer(yTransfer):
    """
    服务端中用来解析请求，获取并加密网页内容的类
    1. 从 manager 的 requestQueue 中获取加密请求，解密后进行解析
    2. 访问请求中的网页，并将网页内容加密存到 manager 的 htmlQueue 中
    """
    def __init__(self, conn=None):
        yTransfer.__init__(self, conn)

    def run(self):
        # 从 manager 的 requestQueue 中获取请求
        # 解密请求
        # 解析请求
        # 访问请求中要访问的网页
        # 接收网页内容
        # 将网页内容加密并存到 manager 的 queue 里
        # 结束
        pass


if __name__ == '__main__':
    pass
