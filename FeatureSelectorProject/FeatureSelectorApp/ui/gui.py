# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 676)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.imageFrame = QtWidgets.QFrame(self.centralwidget)
        self.imageFrame.setMinimumSize(QtCore.QSize(800, 600))
        self.imageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imageFrame.setObjectName("imageFrame")
        self.verticalLayout.addWidget(self.imageFrame)
        self.horizontal_buttons_layout = QtWidgets.QHBoxLayout()
        self.horizontal_buttons_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontal_buttons_layout.setObjectName("horizontal_buttons_layout")
        self.btnLoadImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadImage.setObjectName("btnLoadImage")
        self.horizontal_buttons_layout.addWidget(self.btnLoadImage)
        self.btnSelectArea = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelectArea.setObjectName("btnSelectArea")
        self.horizontal_buttons_layout.addWidget(self.btnSelectArea)
        self.btnSaveSelection = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveSelection.setObjectName("btnSaveSelection")
        self.horizontal_buttons_layout.addWidget(self.btnSaveSelection)
        self.verticalLayout.addLayout(self.horizontal_buttons_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnLoadImage.setText(_translate("MainWindow", "Load Image"))
        self.btnSelectArea.setText(_translate("MainWindow", "Select area"))
        self.btnSaveSelection.setText(_translate("MainWindow", "Save Selection"))

