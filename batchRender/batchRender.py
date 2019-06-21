#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : batchRender.py
# Author            : yang <mightyang@hotmail.com>
# Date              : 16.01.2019
# Last Modified Date: 16.01.2019
# Last Modified By  : yang <mightyang@hotmail.com>
# -*- coding: utf-8 -*-
##############################################
# Author        : shaojiayang
# Email         : mightyang2@163.com
# Last modified : 2018-03-31 16:58
# Filename      : batchRender.py
# Description   :
##############################################
from PySide2 import QtCore, QtGui, QtWidgets
import sys
import os
import subprocess

os.environ["NUKE_PATH"] = r"\\192.168.2.3\plugins\nuke\nuke_plugins"
os.environ["NUKE_FONT_PATH"] = r"\\192.168.2.3\plugins\nuke\nuke_fonts"

class signalObject(QtCore.QObject):
    resultSignal = QtCore.Signal(int, int)
    sendResultSignal = QtCore.Signal(int, int)
    updateButtonSignal = QtCore.Signal(int)


class renderRunnable(QtCore.QRunnable):

    def __init__(self, ID, item, preScript, nukePath, threadpool=None):
        super(renderRunnable, self).__init__()
        self.obj = signalObject()
        self._threadpool = None
        self._item = item
        self._preScript = preScript
        self._nukePath = nukePath
        self._id = ID
        self._p = None
        self._isRendering = False
        if threadpool:
            self.connectDst(threadpool)

    def connectDst(self, dst):
        if isinstance(dst, renderThread):
            self._threadpool = dst
            self.obj.resultSignal.connect(self._threadpool.sendResult)

    def generateRenderScript(self, nkFile):
        scriptPath = os.path.join(
            os.path.dirname(nkFile), os.path.splitext(
                os.path.basename(nkFile))[0]+".py")
        with open(scriptPath, "w") as scriptFile:
            scriptFile.write('print "render script: %s"\n' % nkFile.replace("\\", "/"))
            scriptFile.write('nuke.scriptOpen("%s")\n' % nkFile.replace("\\", "/"))
            if self._preScript:
                scriptFile.write(self._preScript + "\n")
            scriptFile.write('ws = nuke.allNodes("Write")\n')
            scriptFile.write('if ws:\n')
            scriptFile.write('    for w in ws:\n')
            scriptFile.write('        if (not w["disable"].value()):\n')
            scriptFile.write('            print "Render Write: %s" % w.name()\n')
            scriptFile.write('            nuke.render(w, w.firstFrame(), w.lastFrame())\n')
            scriptFile.write('nuke.scriptExit()\n')
        return scriptPath

    def getID(self):
        return self._id

    def getThread(self):
        return self._p

    def isRendering(self):
        return self._isRendering

    def run(self):
        scriptPath = self.generateRenderScript(self._item.text())
        cmd = '"%s" -t --nukex -i "%s"' % (self._nukePath.replace(
            "\\", "/"), scriptPath.replace("\\", "/"))
        print "start render thread: [%d]." % self._id
        self._p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stdout)
#          while True:
#              line = p.stdout.readline()
#              if line:
#                  sys.stdout.write("[ID: %d]-> " % self._id + line)
#                  sys.stdout.flush()
#              else:
#                  break
        self._isRendering = True
        self._p.wait()
        self._isRendering = False
        os.remove(scriptPath)
        if self._p.returncode == 0:
            self.obj.resultSignal.emit(self._id, 0)
            print "render thread: [%d] is complete." % self._id
        else:
            self.obj.resultSignal.emit(self._id, 1)
            print "render thread: [%d] is failed." % self._id


class renderThread(QtCore.QThread):

    def __init__(self, main=None):
        super(renderThread, self).__init__()
        self.obj = signalObject()
        self._items = []
        self._preScript = ""
        self._nukePath = None
        self._runnables = {}
        self._threadpool = QtCore.QThreadPool()
        self._threadpool.setMaxThreadCount(1)
        self._main = None
        if main:
            self.connectDst(main)

    def connectDst(self, dst):
        if isinstance(dst, batchRenderGui):
            self._main = dst
            self._main.connectDst(self)
            self.obj.sendResultSignal.connect(self._main.renderUpdateGui)
            self.obj.updateButtonSignal.connect(self._main.updateButton)

    def sendResult(self, itemID, returncode):
        self.obj.sendResultSignal.emit(itemID, returncode)

    def stopThread(self):
        if self._runnables and not self._isRemoving:
            print "stopping all render threads."
            # clear thread pool
            self._threadpool.clear()
            # set status at removing
            self._isRemoving = True
            # stop rendering processes
            for ra in self._runnables:
                if self._runnables[ra].isRendering():
                    try:
                        self._runnables[ra].getThread().terminate()
                        self._runnables[ra].getThread().wait()
                        print "render thread: [%d] has been stopped." % self._runnables[ra].getID()
                    except Exception, err:
                        print err
                        return 1
            # clear all runnable
            self._runnables.clear()
            # change button to render
            self.obj.updateButtonSignal.emit(1)
            # set status at stopped
            self._isRemoving = False

    def run(self):
        print "starting render thread pool."
        self._isRemoving = False
        self._threadpool.setMaxThreadCount(self._main.getThreadCount())
        self._items = self._main.getItems()
        self.obj.updateButtonSignal.emit(0)
        for i in range(len(self._items)):
            self._runnables[i] = renderRunnable(
                i, self._items[i], self._main.getPreScript(), self._main.getNukePath(), self)
            self._threadpool.start(self._runnables[i])
        self._threadpool.waitForDone()
        self._threadpool.clear()


class batchRenderGui(QtWidgets.QWidget):
    stopThreadSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super(batchRenderGui, self).__init__(parent)
        self._nukePathField = None
        self._nukeFilePathField = None
        self._nukeFileListWidget = None
        self._nukeCountLabel = None
        self._nkRenderPreScriptWidget = None
        self._nkRenderThreadText = None
        self._threadpool = None
        self._nkCount = 0
        self._nkRenderedCount = 0
        self._nkRenderedFailedCount = 0
        self._activedItems = []
        self.initGui()

    def initGui(self):
        self.setWindowTitle("Yang's Render Tool")
        self.setToolTip("This script is used to batch render nk file.\n\
It create a py file, and call Nuke to execute it when Nuke startup.\n\
It is writed by yang for WenZhou JiaShi company.")
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)

        nukePathFrame = QtWidgets.QFrame()
        nukePathLayout = QtWidgets.QHBoxLayout()
        nukePathFrame.setLayout(nukePathLayout)
        nukePathLabel = QtWidgets.QLabel("Nuke Path: ")
        self._nukePathField = QtWidgets.QLineEdit()
        self._nukePathField.setText(
            r"C:\Program Files\Nuke11.1v2\Nuke11.1.exe")
        nukePathBrowser = QtWidgets.QPushButton("Browser")
        nukePathBrowser.clicked.connect(self.setNukePath)
        nukePathLayout.addWidget(nukePathLabel)
        nukePathLayout.addWidget(self._nukePathField)
        nukePathLayout.addWidget(nukePathBrowser)

        nukeFileListFrame = QtWidgets.QFrame()
        nukeFileListLayout = QtWidgets.QVBoxLayout()
        nukeFileListFrame.setLayout(nukeFileListLayout)
        nukeFilePathFrame = QtWidgets.QFrame()
        nukeFilePathLayout = QtWidgets.QHBoxLayout()
        nukeFilePathFrame.setLayout(nukeFilePathLayout)
        nukeFilePathLabel = QtWidgets.QLabel("Nuke Files Path: ")
        self._nukeFilePathField = QtWidgets.QLineEdit()
        self._nukeFilePathSearch = QtWidgets.QPushButton("Search")
        self._nukeFilePathSearch.clicked.connect(self.getNukeFiles)
        self._nukeFileListWidget = QtWidgets.QListWidget()
        self._nukeFileListWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        nukeFilePathLayout.addWidget(nukeFilePathLabel)
        nukeFilePathLayout.addWidget(self._nukeFilePathField)
        nukeFilePathLayout.addWidget(self._nukeFilePathSearch)
        nukeFileListLayout.addWidget(nukeFilePathFrame)
        nukeFileListLayout.addWidget(self._nukeFileListWidget)

        nukeRenderFrame = QtWidgets.QFrame()
        nukeRenderLayout = QtWidgets.QHBoxLayout()
        nukeRenderFrame.setLayout(nukeRenderLayout)
        self._nukeCountLabel = QtWidgets.QLabel(
            "Count: %d Rendered: %d Failed: %d" %
            (self._nkCount, self._nkRenderedCount, self._nkRenderedFailedCount))
        nukeRenderThreadFrame = QtWidgets.QFrame()
        nukeRenderThreadLayout = QtWidgets.QHBoxLayout()
        nukeRenderThreadFrame.setLayout(nukeRenderThreadLayout)
        nukeRenderThreadLabel = QtWidgets.QLabel("Num Once: ")
        self._nukeRenderThreadText = QtWidgets.QLineEdit()
        self._nukeRenderThreadText.setFixedWidth(25)
        self._nukeRenderThreadText.setInputMask("D")
        self._nukeRenderThreadText.setText("1")
        nukeRenderThreadLayout.addWidget(nukeRenderThreadLabel)
        nukeRenderThreadLayout.addWidget(self._nukeRenderThreadText)
        self._nukeRenderButton = QtWidgets.QPushButton("Render")
        nukeRenderLayout.addWidget(self._nukeCountLabel)
        nukeRenderLayout.addWidget(nukeRenderThreadFrame)
        nukeRenderLayout.addWidget(self._nukeRenderButton)

        nukeRenderPreScriptFrame = QtWidgets.QFrame()
        nukeRenderPreScriptLayout = QtWidgets.QVBoxLayout()
        nukeRenderPreScriptFrame.setLayout(nukeRenderPreScriptLayout)
        self._nkRenderPreScriptWidget = QtWidgets.QTextEdit()
        preScript = '''ns = nuke.allNodes("ParticleEmitter")
if ns:
    for n in ns:
    if n['rate'].hasExpression():
        n['rate'].clearAnimated()
        n['rate'].setValue(1)
nuke.scriptSave(nuke.root().name())
nuke.scriptClose()'''
        self._nkRenderPreScriptWidget.setText(preScript)
        nukeRenderPreScriptLayout.addWidget(self._nkRenderPreScriptWidget)

        mainLayout.addWidget(nukePathFrame)
        mainLayout.addWidget(nukeFileListFrame)
        mainLayout.addWidget(nukeRenderFrame)
        mainLayout.addWidget(nukeRenderPreScriptFrame)

    def setNukePath(self):
        getNukePathDialog = QtWidgets.QFileDialog()
        nukePath, _filter = getNukePathDialog.getOpenFileName(
            self, "Nuke Path", os.path.dirname(
                self._nukePathField.text()), "*.exe")
        self._nukePathField.setText(nukePath)

    def getNukeFiles(self):
        filePathList = []
        if self._nukeFilePathField.text():
            for root, dirs, files in os.walk(self._nukeFilePathField.text()):
                if files:
                    for f in files:
                        if os.path.splitext(f)[-1] == ".nk":
                            filePathList.append(os.path.join(root, f))

            self.updateListWidget(filePathList)
        self._nkCount = len(filePathList)
        self._nukeCountLabel.setText(
            "Count: %d Rendered: %d Failed: %d" %
            (self._nkCount, self._nkRenderedCount, self._nkRenderedFailedCount))

    def getPreScript(self):
        return self._nkRenderPreScriptWidget.toPlainText()

    def getNukePath(self):
        return self._nukePathField.text().strip()

    def getThreadCount(self):
        return int(self._nukeRenderThreadText.text())

    def getItems(self):
        self._activedItems = self._nukeFileListWidget.selectedItems()
        if not self._activedItems:
            self._activedItems = [
                self._nukeFileListWidget.item(i) for i in range(
                    self._nukeFileListWidget.count())]
        return self._activedItems

    def connectDst(self, dst):
        if isinstance(dst, renderThread):
            self._threadpool = dst
            print "main connect threadpool"
            self._nukeRenderButton.clicked.connect(self.startThread)
            self.stopThreadSignal.connect(self._threadpool.stopThread)

    def updateButton(self, code):
        if code:
            self._nukeRenderButton.setText("Render")
        else:
            self._nukeRenderButton.setText("Stop")

    def updateListWidget(self, pathList):
        self._nukeFileListWidget.clear()
        for p in pathList:
            self._nukeFileListWidget.addItem(QtWidgets.QListWidgetItem(p))

    def renderUpdateGui(self, itemID, returnCode):
        if returnCode == 0:
            self._nkRenderedCount += 1
            self._activedItems[itemID].setBackgroundColor(
                QtGui.QColor(128, 255, 128))
        else:
            self._nkRenderedFailedCount += 1
            self._activedItems[itemID].setBackgroundColor(
                QtGui.QColor(255, 128, 128))
        self._nukeCountLabel.setText(
            "Count: %d Rendered: %d Failed: %d" %
            (self._nkCount, self._nkRenderedCount, self._nkRenderedFailedCount))

    def startThread(self):
        if self._threadpool.isRunning():
            self.stopThreadSignal.emit()
        else:
            self._threadpool.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    br = batchRenderGui()
    rt = renderThread(br)
    br.show()
    sys.exit(app.exec_())
