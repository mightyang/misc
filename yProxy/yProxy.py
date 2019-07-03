#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : yProxy.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 23.06.2019
# Last Modified Date: 03.07.2019
# Last Modified By  : yang <mightyang@hotmail.com>


import Queue
import traceback
from yLogging import lg
import socket
import threading
import re


DATA_BLOCKSIZE = 4096
MAX_CONNECTIONS = 1000
QUEUE_LAST_CODE_BASE64 = 'UVVFVUVfTEFTVF9DT0RFX0JBU0U2NA=='
TRANSFER_LAST_CODE_BASE64 = 'VFJBTlNGRVJfTEFTVF9DT0RFX0JBU0U2NA=='
CONN_PASS_SIGNAL_BASE64 = 'Q09OTl9QQVNTX1NJR05BTF9CQVNFNjQ='
SOCKET_STOP_SIGNAL_BASE64 = 'U09DS0VUX1NUT1BfU0lHTkFMX0JBU0U2NA=='



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
        self.p = parent
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
        yThread.__init__(self, parent)
        self.requestData = Queue.Queue()
        self.workerCount = 5
        self.workers = []
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
    def __init__(self, parent=None, addr=('127.0.0.1', 1080)):
        yManager.__init__(self, parent, addr)
        self.browserConnQueue = Queue.Queue()

    def run(self):
        # 绑定本地端口
        if not self.bindAddr():
            return
        self.s.listen(10)
        # 连接远程服务器
        # 启动一定数量的 worker
        for i in range(self.workerCount):
            worker = yClientWorker(parent=self)
            self.workers.append(worker)
            worker.start()
            lg.debug(u'启动 worker 线程: {}'.format(worker.ident))
        # 等待浏览器接入
        while True:
            conn, addr = self.s.accept()
            # 将 conn 添加到 self.browserConnQueue 中
            self.browserConnQueue.put(conn)
        #  self.browserTransfer.start()

    def stop(self):
        self.s.close()


class yServerManager(yManager):
    def __init__(self, parent=None, addr=('127.0.0.1', 0)):
        yManager.__init__(self, parent, addr)
        self.netConnQueue = Queue.Queue()

    def run(self):
        pass

    def stop(self):
        self.dataTransfer.stop()
        self.netTransfer.stop()
        self.s.close()


class yWorker(yThread):
    """
    1. 保存socket线程的集合
    2. 保存socket线程之间的交流数据
    """
    def __init__(self, parent=None):
        yThread.__init__(self, parent)
        self.requestQueue = Queue.Queue()
        self.htmlQueue = Queue.Queue()

    def run(self):
        pass

    def stop(self):
        pass


class yClientWorker(yWorker):
    def __init__(self, parent=None):
        yWorker.__init__(self, parent=parent)

    def run(self):
        # 启动 transfer
        ct = yClientTransfer(parent=self)
        cdt = yClientDataTransfer(parent=self)
        ct.start()
        cdt.start()

    def stop(self):
        self.ct.stop()
        self.cdt.stop()


class yServerWorker(yWorker):
    def __init__(self, parent=None):
        yWorker.__init__(self, parent=parent)

    def run(self):
        pass

    def stop(self):
        self.dataTransfer.stop()
        self.netTransfer.stop()


class yTransfer(yThread):
    def __init__(self, parent=None):
        yThread.__init__(self, parent)

    def run(self):
        pass

    def stop(self):
        self.sendSelf(SOCKET_STOP_SIGNAL_BASE64)

    def setConn(self, conn):
        self.conn = conn
        self.sendSelf(CONN_PASS_SIGNAL_BASE64)

    def sendSelf(self, signal):
        tmpSock = socket.socket()
        try:
            tmpSock.sendto(signal, self.s.getsockname())
            return True
        except Exception:
            lg.error(u'给自身发送信号失败，异常信息: {}'.format(traceback.format_exc()))
            return False

    def encode(self, data):
        return data

    def decode(self, data):
        return data

    def requestHeaderAnalisis(self, data):
        splitter = '\r\n\r\n'
        if splitter in data:
            requestLines = data.split(splitter)[0].split('\r\n')[:-1]
            initialLine = re.findall(r'.+\s(.+)\s.+', requestLines[0])
            headerLines = dict([headerLine.split(':', 1) for headerLine in requestLines[1:]])
            return (initialLine, headerLines)
        else:
            return False


class yClientDataTransfer(yTransfer):
    """
    客户端中用来与服务端传递数据的类
    1. 传递 manager 的 requestQueue 中的加密请求给服务端
    2. 从服务端接收访问的网页内容，存储到 manager 的 htmlQueue 中
    """
    def __init__(self, parent=None):
        yTransfer.__init__(self, parent)

    def run(self):
        # 等待 requestQueue 中的请求
        while True:
            while True:
                dataBlock = self.p.requestQueue.get()
                # 如果 data 信息为结束信息，则结束获取
                if dataBlock == QUEUE_LAST_CODE_BASE64:
                    lg.debug(u'yClientDataTransfer 请求获取结束')
                    break
                # 发送请求到服务端
                lg.debug(u'收到数据: {}'.format(dataBlock))
                #  self.conn.send(dataBlock)
            # 等待服务端发送要访问的网页内容
            while True:
                dataBlock = self.conn.recv(DATA_BLOCKSIZE)
                if dataBlock == TRANSFER_LAST_CODE_BASE64:
                    lg.debug(u'yClientDataTransfer 网页内容获取结束')
                    break
                # 将收到的网页内容存到 queue 中
                self.htmlQueue.put(dataBlock)
        # 接收完毕后结束
        self.stop()


class yClientTransfer(yTransfer):
    """
    客户端中用来与浏览器传递数据的类
    1. 接收浏览器的请求，加密后存到 manager 的 queue 里
    2. 从 manager 的 htmlQueue 中获取加密的网页内容, 解密后发给浏览器
    """
    def __init__(self, parent=None):
        yTransfer.__init__(self, parent)
        self.connQueue = self.p.p.browserConnQueue

    def run(self):
        # 等待 browserConnQueue 中的 conn 进入
        while True:
            conn = self.connQueue.get()
            lg.debug(u'发现新的浏览器连接: {}'.format(conn.getpeername()))
            recvSize = 0
            headerPos = -1
            dataBlock = ''
            data = ''
            # 获取请求头
            while True:
                dataBlock = conn.recv(DATA_BLOCKSIZE)
                if not dataBlock:
                    break
                recvSize += len(dataBlock)
                # 将获取的部分请求内容存到 requestQueue 里
                self.p.requestQueue.put(dataBlock)
                data += dataBlock
                # 查找请求头的位置
                headerPos = data.find('\r\n\r\n')
                if headerPos != -1:
                    break
                if recvSize > 10000:
                    break
            if recvSize > 10000:
                conn.close()
                lg.error(u'请求头太长，假定为异常，停止接收数据，关闭连接')
                break
            # 获取请求头的大小
            headerSize = headerPos + 4
            # 解析请求头
            headerLines = self.requestHeaderAnalisis(data)
            # 判定模式：content-length 或者 chunked
            if 'Transfer-Encoding' in headerLines[1] and headerLines[1]['Transfer-Encoding'] != 'dentity':
                lg.debug(u'请求使用chunked传递, 继续接收')
                while True:
                    dataBlock = conn.recv(DATA_BLOCKSIZE)
                    if not dataBlock:
                        break
                    recvSize += len(dataBlock)
                    self.p.requestQueue.put(dataBlock)
            elif 'Content-Length' in headerLines[1]:
                lg.debug(u'请求使用固定长度传递, 继续接收，Content-Length: {}'.format(headerLines[1]['Content-Length']))
                # 继续接收 请求体
                while recvSize < int(headerLines[1]['Centent-Length'])+headerSize:
                    dataBlock = conn.recv(DATA_BLOCKSIZE)
                    if not dataBlock:
                        break
                    recvSize += len(dataBlock)
                    self.p.requestQueue.put(dataBlock)
            else:
                lg.debug(u'请求没有长度值')
                break
        # 等待返回 html 数据
        return
        while True:
            data = self.conn.recv(DATA_BLOCKSIZE)
            if len(data) == 0:
                break
            # 将请求加密存到 requestQueue 中
            self.requestQueue.put(self.encode(data))
        # 等待 htmlQueue 中的内容
        while True:
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
    def __init__(self, parent=None):
        yTransfer.__init__(self, parent)

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
    def __init__(self, parent=None):
        yTransfer.__init__(self, parent=parent)

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
    test = yClientManager()
    test.start()
