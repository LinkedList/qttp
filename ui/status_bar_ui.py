# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'status_bar.ui',
# licensing of 'status_bar.ui' applies.
#
# Created: Sun Feb 17 10:17:03 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_StatusBar(object):
    def setupUi(self, StatusBar):
        StatusBar.setObjectName("StatusBar")
        StatusBar.resize(142, 28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StatusBar.sizePolicy().hasHeightForWidth())
        StatusBar.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(StatusBar)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.requestProgress = QtWidgets.QProgressBar(StatusBar)
        self.requestProgress.setStyleSheet("")
        self.requestProgress.setMaximum(100)
        self.requestProgress.setProperty("value", 0)
        self.requestProgress.setTextVisible(False)
        self.requestProgress.setObjectName("requestProgress")
        self.horizontalLayout_2.addWidget(self.requestProgress)
        self.cancelButton = QtWidgets.QPushButton(StatusBar)
        self.cancelButton.setStyleSheet("padding: 3px")
        self.cancelButton.setFlat(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.retranslateUi(StatusBar)
        QtCore.QMetaObject.connectSlotsByName(StatusBar)

    def retranslateUi(self, StatusBar):
        StatusBar.setWindowTitle(QtWidgets.QApplication.translate("StatusBar", "Form", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("StatusBar", "Cancel", None, -1))

