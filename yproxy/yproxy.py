#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : yproxy.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 23.03.2019
# Last Modified Date: 26.03.2019
# Last Modified By  : yang <mightyang@hotmail.com>


import socket, random, logging, os, json, threading, hashlib, time, Queue


yl = logging.getLogger(__name__)


class connector(threading.Thread):
    __addr = ()
    __socket = None
    __time = 0
    __status = None
    __group = None
    __host = ''

    def __init__(self, host='127.0.0.1', group=None):
        threading.Thread.__init__(self)
        self.__socket = socket.socket()
        self.__status = status.STOPPED
        self.__key = self.md5()
        self.__group = group
        self.__host = host

    def randomValidePort(self):
        yl.debug('generate a random port for worker')
        sk = socket.socket()
        while True:
            port = random.randint(10000, 65535)
            if sk.connect_ex((self.host, port)) == 0:
                sk.close()
                return port

    def md5(self):
        m = hashlib.md5()
        m.update(str(time.time()))
        return m.hexdigest()

    def address(self):
        return self.__addr

    def pkgData(self, data):
        self.__key = self.md5()
        return '{}{}'.format(self.__key, data)

    def key(self):
        return self.__key

    def analizeContent(self, data):
        return (data[:32], data[32:])



class receiver(connector):
    def __init__(self, host='127.0.0.1', group=None):
        connector.__init__(self, host, group)
        self.__group = group

    def run(self):
        self.__addr = (self.__host, self.randomValidePort())
        yl.debug('start receiver thread')
        try:
            self.__socket.bind(self.__addr)
        except Exception, e:
            raise e
        self.__socket.listen(5)
        self.__status = status.RUNNING
        while True:
            conn, addr = self.__socket.accept()
            try:
                data = conn.recv(1024)
            except Exception, e:
                yl.error(e.message)
                continue
            if data == signal.STOP:
                break
            elif len(data) > 0:
                # 解析收到的数据
                result = self.analizeContent(data)
                # 如果收到数据中的key与当前一样，则转发内容, 否则发送错误代码
                if result[0] == self.__key:
                    if result[1] == returnCode.TEST_SIGNAL:
                        conn.send(self.pkgData(returnCode.OK_SIGNAL))
                        continue
                    if self.__group != None:
                        self.__group.__queue.put(result[1])
                else:
                    conn.send(returnCode.KEY_ERROR)
                    break
        self.__status = status.STOPPED
        self.__socket.close()


class sender(connector):
    def __init__(self, host='127.0.0.1', group=None):
        connector.__init__(self, host)
        self.__group = group

    def run(self):
        yl.debug('start sender thread')
        self.__addr = (self.__host, self.randomValidePort())
        try:
            self.__socket.bind(self.__addr)
        except Exception, e:
            raise e
        self.__socket.listen(5)
        self.__status = status.RUNNING
        while True:
            conn, addr = self.__socket.accept()
            try:
                data = conn.recv(1024)
            except Exception, e:
                yl.error(e.message)
                continue
            if data == signal.STOP:
                break
            elif len(data) > 0:
                # 解析收到的数据
                result = self.analizeContent(data)
                # 如果收到数据中的key与当前一样，则转发内容, 否则发送错误代码
                if result[0] == self.__key:
                    if self.__group != None:
                        self.__group.__queue.put(result[1])
                else:
                    conn.send(returnCode.KEY_ERROR)
                    break
        self.__status = status.STOPPED
        self.__socket.close()


class worker():
    '''
    receiver and senders
    '''
    def __init__(self, sc=3):
        self.__receiver = None
        self.__senders = []
        self.__workers = []
        self.__csender = None
        self.__queue = Queue.Queue()
        # sender线程的数量
        self.__sc = sc
        self.init()

    def init(self):
        self.__receiver = receiver(group=self)
        for i in range(self.__sc):
            self.__senders.append(sender(group=self))
        self.__csender=self.__sc[0]

    def setReceiver(self, receiver):
        self.__receiver = receiver

    def setSenders(self, senders):
        self.__senders = senders

    def appendSender(self, sender):
        self.__senders.append(sender)

    def removeSender(self, sender):
        self.__senders.remove(sender)

    def receiver(self):
        return self.__receiver

    def senders(self):
        return self.__senders

    def conInfo(self):
        # 返回所有key和端口 [receiver, senders]
        return [(self.__receiver.key(), self.__receiver.address[1])] + [(s.key(), s.address[1]) for s in self.__senders]


class workerGroup():
    def __init__(self):
        self.__worker = worker()

    def conInfo(self):
        return self.__worker.conInfo()


class yserver():
    def __init__(self, host='127.0.0.1', port=5782):
        self.__workerGroups = []
        self.__socket = None
        self.__settings = {'host':host, 'port':port, 'key':[]}
        self.__settingsfp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings')
        self.init()

    def init(self):
        # 初始化 server
        yl.debug('initialize yserver')
        self.readSettings()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.bind((self.__settings['host'], self.__settings['port']))
            self.__socket.listen(5)
        except Exception, e:
            raise e

    def waittingForClient(self):
        # 等待客户连接
        yl.debug('waitting for connection of client')
        while True:
            conn, addr = self.__socket.accept()
            try:
                data = conn.recv(1024)
            except Exception, e:
                raise e
            # 检查密码是否正确
            if self.checkKey(data):
                # 如果密码通过，创建 workers
                wg = self.createWorkerGroup()
                # 发送 workers 端口给客户
                conInfos = ' '.join([' '.join(key, port) for key, port in wg.conInfo()])
                conn.send(conInfos)
            else:
                # 发送密码错误代码给客户
                conn.send(returnCode.KEY_ERROR)

    def checkKey(self, key):
        if key in self.__settings['key']:
            return True
        else:
            return False

    def writeSettings(self):
        j = json.dumps(self.__settings)
        try:
            f = open(self.__settingsfp, 'wb')
            f.write(j)
        except Exception, e:
            raise e
        f.close()

    def readSettings(self):
        yl.debug('read settings')
        if os.path.exists(self.__settingsfp):
            f = open(self.__settingsfp, 'rb')
            settings = f.read()
            f.close()
            self.__settings = json.loads(settings)
        else:
            yl.debug('settings file is not exist, use default')

    def createWorkerGroup(self):
        wg = workerGroup()
        self.__workerGroups.append(wg)
        return wg

    def close(self):
        [wg.stop() for wg in self.__workerGroups]


class client():
    pass


class status():
    RUNNING = 0
    STOPPED = 1

class returnCode():
    KEY_ERROR = 'KEYERRORKEYERRORKEYERRORKEYERRORKEYERROR'
    TEST_SIGNAL = 'TESTSIGNALTESTSIGNALTESTSIGNALTESTSIGNALTESTSIGNALTESTSIGNALTESTSIGNAL'
    OK_SIGNAL= 'OKSIGNALOKSIGNALOKSIGNALOKSIGNALOKSIGNALOKSIGNALOKSIGNALOKSIGNALOKSIGNAL'

class signal():
    STOP = 'EEEEEEEFFFFFFFFexitFFFFFFFFEEEEEEE'
