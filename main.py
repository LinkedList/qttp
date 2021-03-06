#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import re
from configparser import ConfigParser
from urllib.parse import urlparse

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QTabWidget,
    QApplication,
    QMainWindow,
    QMenu,
    QHeaderView,
    QTableWidgetItem,
    QFileDialog,
    QAction,
)

from environment import EnvironmentSwitcher
from headers_completer import HeadersCompleter
from req import Req
from req_thread import ReqThread
from response_tabs_widget import ResponseTabsWidget
from file_line import FileLine
from collections_history_tabs import CollectionsHistoryTabs
from response_info import ResponseInfo
from status_bar import StatusBar

from ui.main_ui import Ui_MainWindow

from url_completer import UrlCompleter
from key_value_editor import KeyValueEditor


class Qttp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Qttp, self).__init__()
        self.setupUi(self)

        self.prepareConfig()
        self.fileLine = FileLine()

        self.prepareMenu()

        self.envrionmentSwitcher = EnvironmentSwitcher()

        self.statusBar = StatusBar()
        self.statusbar.addPermanentWidget(self.statusBar)

        self.responseInfo = ResponseInfo()
        self.responseLayout.addWidget(self.responseInfo)

        self.responseTabs = ResponseTabsWidget()
        self.responseLayout.addWidget(self.responseTabs)

        self.comboBox.setEnabled(False)

        self.url.setFocus()
        self.sendButton.clicked.connect(self.request)
        self.saveButton.clicked.connect(self.saveRequest)
        self.url.returnPressed.connect(self.request)
        self.resizeInputHeadersHeader()
        self.inputHeaders.setColumnCount(2)
        self.inputHeaders.setRowCount(1)
        self.inputHeaders.setHorizontalHeaderLabels(["Key", "Value"])
        self.inputHeaders.cellDoubleClicked.connect(self.addHeaderRow)
        self.inputHeaders.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.inputHeaders.customContextMenuRequested.connect(self.headersMenu)

        headersDelegate = HeadersCompleter(self.inputHeaders)
        self.inputHeaders.setItemDelegateForColumn(0, headersDelegate)

        self.urlCompleter = UrlCompleter(self.url)
        self.url.setCompleter(self.urlCompleter)

        self.collectionsHistoryTabs = CollectionsHistoryTabs()
        self.collectionsHistoryTabs.set_item.connect(self.setFromHistory)
        self.collectionsHistoryLayout.addWidget(self.collectionsHistoryTabs)

        self.envrionmentSwitcher = EnvironmentSwitcher()
        self.collectionsHistoryLayout.addWidget(self.envrionmentSwitcher)

        splitterSizes = self.getMainSplitterSizes()
        print(type(splitterSizes))
        self.mainSplitter.setSizes(splitterSizes)

        self.disableRequestBody()

        self.buttonGroup.buttonClicked.connect(self.postBodySwitched)
        self.method.currentTextChanged.connect(self.onMethodChange)
        self.comboBox.currentTextChanged.connect(self.rawTypeChanged)
        self.currentBodyEditor = self.requestBody

    def prepareMenu(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)
        exitAction.setShortcut("Ctrl+Q")


    def rawTypeChanged(self, rawType):
        if rawType is not "Text":
            contentTypeToSet = re.search(r"\(([A-Za-z0-9_/]+)\)", rawType).group(1)
            self.setContentType(contentTypeToSet)

    def postBodySwitched(self, button):
        if button is self.formUrlEncodedButton:
            self.setContentType("application/x-www-form-urlencoded")
        elif button is self.binaryButton:
            self.setContentType("application/octet-stream")

        elif button is self.formDataButton:
            self.setContentType("multipart/form-data")

        if button is self.rawButton:
            self.comboBox.setEnabled(True)
        else:
            self.comboBox.setEnabled(False)

        if button is self.binaryButton:
            self.resetBodyEditor()
            self.currentBodyEditor = self.fileLine
        elif button is self.formDataButton or button is self.formUrlEncodedButton:
            self.resetBodyEditor()
            self.currentBodyEditor = KeyValueEditor()
        else:
            self.resetBodyEditor()
            self.currentBodyEditor = self.requestBody

        self.verticalLayout_21.addWidget(self.currentBodyEditor)

    def resetBodyEditor(self):
        self.currentBodyEditor.setParent(None)

    def setContentType(self, contentTypeToSet):
        contentType = self.inputHeaders.findItems("Content-Type", Qt.MatchExactly)
        if len(contentType) > 0:
            row = contentType[0].row()
        else:
            self.addHeaderRow()
            row = self.inputHeaders.rowCount() - 1
        item = self.inputHeaders.item(row, 1)
        if not item:
            headerName = QTableWidgetItem()
            headerName.setText("Content-Type")
            self.inputHeaders.setItem(row, 0, headerName)
            item = QTableWidgetItem()
            self.inputHeaders.setItem(row, 1, item)
            self.addHeaderRow()

        item.setText(contentTypeToSet)

    def getMainSplitterSizes(self):
        config = self.config
        config.read("config.ini")
        sizes = config["splitter"]["sizes"]
        if sizes:
            return [int(s) for s in sizes.split(",")]

        return []

    def prepareConfig(self):
        config = ConfigParser()
        config.read("config.ini")
        if not config.has_section("splitter"):
            config["splitter"] = {}

        if not config.has_option("splitter", "sizes"):
            config["splitter"]["sizes"] = ",".join(map(str, [200, 400, 400]))

        with open("config.ini", "w") as configfile:
            config.write(configfile)
        self.config = config

    def enableRequestBody(self):
        bodyTabIndex = self.requestContentTabs.indexOf(self.reqBodyTab)
        self.requestContentTabs.setTabEnabled(bodyTabIndex, True)

    def disableRequestBody(self):
        bodyTabIndex = self.requestContentTabs.indexOf(self.reqBodyTab)
        self.requestContentTabs.setTabEnabled(bodyTabIndex, False)

    def onMethodChange(self, httpMethod):
        if httpMethod == "GET":
            self.disableRequestBody()
        else:
            self.enableRequestBody()

    def resizeInputHeadersHeader(self):
        header = self.inputHeaders.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def forceAddHeaderRow(self):
        count = self.inputHeaders.rowCount()
        self.inputHeaders.setRowCount(count + 1)

    def addHeaderRow(self):
        count = self.inputHeaders.rowCount()
        item = self.inputHeaders.item(count - 1, 0)
        if item:
            self.inputHeaders.setRowCount(count + 1)

    def removeHeaderRow(self, item):
        self.inputHeaders.removeRow(item.row())

    def getInputHeaders(self):
        returnDict = {}
        rows = self.inputHeaders.rowCount()
        for row in range(0, rows):
            key = self.inputHeaders.item(row, 0)
            value = self.inputHeaders.item(row, 1)
            if key and value and key.text() and value.text():
                returnDict[key.text()] = value.text()
        return returnDict

    def buildReqObject(self):
        method = self.method.currentText()
        parsedUrl = urlparse(self.url.text())
        protocol = parsedUrl.scheme or "https"
        url = parsedUrl.netloc + parsedUrl.path
        headers = self.getInputHeaders()
        if type(self.currentBodyEditor) == KeyValueEditor:
            body = self.currentBodyEditor.getData()
        else:
            body = self.requestBody.toPlainText()

        rawFile = self.fileLine.getFile()
        return Req(method, protocol, url, headers, body, rawFile, self.getContext())

    def getContext(self):
        # Temporary stuff
        return {"url": "api.github.com", "file": "/home/martin/pseudo.txt"}

    def request(self):
        self.responseInfo.reset()
        reqObject = self.buildReqObject()
        self.thread = ReqThread(reqObject)
        self.thread.request_done.connect(self.afterRequest)
        self.thread.request_stopped.connect(self.afterStoppedRequest)
        self.statusBar.cancel_request.connect(self.thread.stop)
        self.statusBar.enable()
        self.thread.start()

    def afterStoppedRequest(self):
        self.statusBar.disable()

    def afterRequest(self, response, reqObject):
        self.statusBar.disable()
        self.urlCompleter.addItem(reqObject)
        self.collectionsHistoryTabs.insertToHistory(response, reqObject)
        self.responseInfo.translateStatus(response.status_code)
        self.responseInfo.setTime(response.elapsed.total_seconds())
        self.responseInfo.setContentType(response.headers["content-type"])
        self.responseTabs.setHeaders(response.headers)
        self.responseTabs.setResponseBody(response)

    def saveRequest(self):
        item = self.buildReqObject()
        self.collectionsHistoryTabs._saveRequest(item)

    def setFromHistory(self, req):
        self.url.setText(req.buildUrl())
        index = self.method.findText(req.method)
        self.method.setCurrentIndex(index)
        self.setInputHeadersFromHistory(req.headers)
        self.requestBody.setText(req.body)

    def setInputHeadersFromHistory(self, headers):
        self.inputHeaders.setRowCount(0)
        for key, value in headers.items():
            rowCount = self.inputHeaders.rowCount()
            self.inputHeaders.insertRow(rowCount)
            self.inputHeaders.setItem(rowCount, 0, QTableWidgetItem(key))
            self.inputHeaders.setItem(rowCount, 1, QTableWidgetItem(value))
        self.inputHeaders.insertRow(self.inputHeaders.rowCount())

    def headersMenu(self, position):
        menu = QMenu()
        newAction = menu.addAction("New")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.inputHeaders.mapToGlobal(position))
        if action == deleteAction:
            item = self.inputHeaders.itemAt(position)
            if item:
                self.removeHeaderRow(item)
        elif action == newAction:
            self.forceAddHeaderRow()

    def closeEvent(self, event):
        config = self.config
        config["splitter"]["sizes"] = ",".join(map(str, self.mainSplitter.sizes()))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def setTime(self, elapsed_seconds):
        self.time.setText(str(int(elapsed_seconds * 1000)) + " ms")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    prog = Qttp()
    prog.show()
    sys.exit(app.exec_())
