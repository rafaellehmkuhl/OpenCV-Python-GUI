from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                             QPushButton, QSlider)
import cv2
import numpy as np


class Filter(QWidget):
    """Common base class for all filters"""
    defaultK = 3
    filterCount = 0

    def __init__(self, name, minValue, maxValue, init, num_of_k, parent=None):
        super().__init__()

        self.filter_number = Filter.filterCount
        self.name = name
        self.num_of_k = num_of_k
        self.k = [init]

        # Increase the number of filters created
        Filter.filterCount += 1

        # Set maximum height
        self.setMaximumHeight(65)
        # Variable for the slider/label layout
        self.lay = QHBoxLayout(self)
        # Variable for the constant of the OpenCV filter
        self.k[0] = self.defaultK
        # Label for the slider
        self.k_lbl = [QLabel(str(self.k[0]))]
        # Name for the slider
        self.name_lbl = QLabel(self.name + ': ')
        # Set default parameters
        self.setParameters(minValue, maxValue)

        # Create delete button
        self.delete_filter_btn = QPushButton('X')
        self.delete_filter_btn.clicked.connect(self.deleteFilter)

        # Adds the slider and it's label to the layout
        self.createLayout()

        # Function sending the slider signal to the processing function
        self.thresh_sld.valueChanged.connect(self.changeValue)

    def setParameters(self, minValue, maxValue):
        # Creates the slider for the OpenCV filter, with min, max, default and
        # step values
        self.thresh_sld = QSlider(Qt.Horizontal, self)
        self.thresh_sld.setFocusPolicy(Qt.NoFocus)
        self.thresh_sld.setMinimum(minValue)
        self.thresh_sld.setMaximum(maxValue)
        self.thresh_sld.setValue(self.k[0])
        self.thresh_sld.setSingleStep(2)

    def createLayout(self):
        # Adds the slider and its label to the bottom of the main layout

        self.lay.addWidget(self.name_lbl)
        self.lay.addWidget(self.k_lbl[0])
        self.lay.addWidget(self.thresh_sld)
        self.lay.addWidget(self.delete_filter_btn)

    def changeValue(self, value):
        # Function for setting the value of k1

        if value % 2 == 1:
            self.k[0] = value
        else:
            self.k[0] = value + 1

        self.thresh_sld.setValue(self.k[0])
        self.k_lbl[0].setText(str(self.k[0]))
        self.parent().parent().updateImages()

    def resetValue(self):
        # Resets the K value to it's default
        self.changeValue(self.defaultK)

    def deleteFilter(self):
        self.parent().parent().deleteFilter(self.filter_number)

    def process(self, cv_before, name):

        k = self.k[0]
        kernel = np.ones((k, k), np.uint8)

        if name == 'Invert':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.bitwise_not(cv_before)
        elif name == 'Histogram Equalization':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cv_after = clahe.apply(cv_before)
        elif name == 'Threshold':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            ret, cv_after = cv2.threshold(
                cv_before, k, 255, cv2.THRESH_BINARY)
        elif name == 'Gaussian Threshold':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.adaptiveThreshold(cv_before, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, k, 2)
        elif name == 'HSV':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2HSV)
            lower_color = np.array([k - 35, 0, 0])
            upper_color = np.array([k + 35, 255, 255])
            cv_after = cv2.inRange(cv_before, lower_color, upper_color)
        elif name == 'LAB':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2LAB)
            L, a, b = cv2.split(cv_before)
            ret, cv_after = cv2.threshold(L, k, 255, cv2.THRESH_BINARY)
        elif name == 'Erosion':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.erode(cv_before, kernel, iterations=1)
        elif name == 'Dilation':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.dilate(cv_before, kernel, iterations=1)
        elif name == 'Opening':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.morphologyEx(
                cv_before, cv2.MORPH_OPEN, kernel)
        elif name == 'Closing':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.morphologyEx(
                cv_before, cv2.MORPH_CLOSE, kernel)
        elif name == 'Top Hat':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.morphologyEx(
                cv_before, cv2.MORPH_TOPHAT, kernel)
        elif name == 'Black Hat':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.morphologyEx(
                cv_before, cv2.MORPH_BLACKHAT, kernel)
        elif name == 'Canny':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.Canny(cv_before, 100, k)
        elif name == 'Laplacian':
            cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
            cv_after = cv2.Laplacian(cv_before, cv2.CV_64F)
            cv_after = np.absolute(cv_after)
            cv_after = np.uint8(cv_after)

        return cv_after