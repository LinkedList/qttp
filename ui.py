# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(744, 493)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(1240, 890))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.method = QtWidgets.QComboBox(self.centralwidget)
        self.method.setObjectName("method")
        self.method.addItem("")
        self.method.addItem("")
        self.horizontalLayout.addWidget(self.method)
        self.url = QtWidgets.QLineEdit(self.centralwidget)
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.responseTab = QtWidgets.QWidget()
        self.responseTab.setObjectName("responseTab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.responseTab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(-1, -1, 1231, 831))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.responseText = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.responseText.setObjectName("responseText")
        self.verticalLayout_2.addWidget(self.responseText)
        self.tabWidget.addTab(self.responseTab, "")
        self.headersTab = QtWidgets.QWidget()
        self.headersTab.setObjectName("headersTab")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.headersTab)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(-1, -1, 1241, 831))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headersText = QtWidgets.QTextBrowser(self.verticalLayoutWidget_3)
        self.headersText.setObjectName("headersText")
        self.verticalLayout_3.addWidget(self.headersText)
        self.tabWidget.addTab(self.headersTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 744, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.method.setItemText(0, _translate("MainWindow", "GET"))
        self.method.setItemText(1, _translate("MainWindow", "POST"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.responseTab), _translate("MainWindow", "Response"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.headersTab), _translate("MainWindow", "Headers"))

