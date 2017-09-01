from PyQt5 import QtWidgets, QtCore, QtGui.Q
import cv2
import numpy as np
import sys
import os

import gui


class FeatureSelection(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Feature Selection")

        extractAction = 

        self.home()

    def home(self):
    	btn = QtWidgets.QPushButton("Quit", self)
    	btn.clicked.connect(close_application)
    	btn.resize(btn.minimumSizeHint())

def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = FeatureSelection()
    GUI.show()
    sys.exit(app.exec_())

def close_application(self):
	print("sooooooo custom")
	sys.exit()


if __name__ == '__main__':
    main()
