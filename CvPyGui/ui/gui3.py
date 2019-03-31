# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ..PlotContainer import SinglePlotContainer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainVLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainVLayout.setObjectName("mainVLayout")
        self.bottomCommandsHLayout = QtWidgets.QHBoxLayout()
        self.bottomCommandsHLayout.setObjectName("bottomCommandsHLayout")
        self.plotsVLayout = QtWidgets.QVBoxLayout()
        self.plotsVLayout.setObjectName("plotsVLayout")
        self.mainVLayout.addLayout(self.bottomCommandsHLayout)
        self.mainVLayout.addLayout(self.plotsVLayout)

        self.plot1 = SinglePlotContainer()
        self.plot1.setObjectName("plot1")
        self.plotsVLayout.addWidget(self.plot1)
        self.plot2 = SinglePlotContainer()
        self.plot2.setObjectName("plot2")
        self.plotsVLayout.addWidget(self.plot2)
        self.plot3 = SinglePlotContainer()
        self.plot3.setObjectName("plot3")
        self.plotsVLayout.addWidget(self.plot3)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1053, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.actionLoad_data = QtWidgets.QAction(MainWindow)
        self.actionLoad_data.setObjectName("actionLoad_data")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionLicense = QtWidgets.QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionLoad_data)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionLicense)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Analysis"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionLoad_data.setText(_translate("MainWindow", "Load data"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionLicense.setText(_translate("MainWindow", "License"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

