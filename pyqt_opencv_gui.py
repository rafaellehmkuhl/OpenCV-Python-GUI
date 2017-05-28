import sys
import numpy as np
import cv2
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QComboBox)


class Image(QWidget):
    """Common base for the images"""

    def __init__(self, name):
        super(Image, self).__init__()

        self.setFixedSize(500, 500)

        # Label for the image
        self.name_lbl = QLabel(name)

        # Label (frame) where the original image will be located, with true
        # scaling and maximum size
        self.frame_lbl = QLabel(self)
        self.frame_lbl.setMinimumSize(400, 400)
        self.frame_lbl.setScaledContents(True)

        self.createLayout()

    def createLayout(self):
        self.v_lay = QVBoxLayout()

        self.v_lay.addWidget(self.name_lbl)
        self.v_lay.addWidget(self.frame_lbl)

    def updateImage(self, opencv_rgb_image):

        self.cv_img_rgb = opencv_rgb_image

        height, width, channel = self.cv_img_rgb.shape
        bytesPerLine = 3 * width
        self.q_image = QImage(self.cv_img_rgb.data, width,
                              height, bytesPerLine, QImage.Format_RGB888)

        self.frame_lbl.setPixmap(QPixmap.fromImage(self.q_image))


class Filter(QWidget):
    """Common base class for all filters"""
    defaultK = 3
    filterCount = 0

    def __init__(self, name, minValue, maxValue, init, parent=None):
        super(Filter, self).__init__(parent=parent)

        self.filter_number = Filter.filterCount
        self.setMaximumHeight(65)
        self.k = init
        self.name = name

        # Increase the number of filters created
        Filter.filterCount += 1

        # Variable for the slider/label layout
        self.lay = QHBoxLayout(self)
        # Variable for the constant of the OpenCV filter
        self.k = self.defaultK
        # Label for the slider
        self.k_lbl = QLabel(str(self.k))
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
        self.thresh_sld.setValue(self.k)
        self.thresh_sld.setSingleStep(2)

    def createLayout(self):
        # Adds the slider and its label to the bottom of the main layout

        self.lay.addWidget(self.name_lbl)
        self.lay.addWidget(self.k_lbl)
        self.lay.addWidget(self.thresh_sld)
        self.lay.addWidget(self.delete_filter_btn)

    def changeValue(self, value):
        # Function for setting the value of k1

        if value % 2 == 1:
            self.k = value
        else:
            self.k = value + 1

        self.thresh_sld.setValue(self.k)
        self.k_lbl.setText(str(self.k))
        self.parent().updateImages()

    def resetValue(self):
        # Resets the K value to it's default
        self.changeValue(self.defaultK)

    def deleteFilter(self):
        self.parent().deleteFilter(self.filter_number)


class MainWindow(QWidget):

    filter_count = 0

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()
        self.filters = []

    def initUI(self):

        self.original_image = Image('Original')
        self.processed_image = Image('Processed')
        self.setBackground()

        self.createImagesLayout()
        self.createFiltersLayout()
        self.createButtons()
        self.createMainLayout()

    def createNewFilter(self):
        name = self.filter_select.currentText()

        if name == 'Threshold':
            min_value = 3
            max_value = 255
            init_value = 3
        if name == 'Gaussian Threshold':
            min_value = 31
            max_value = 255
            init_value = 3
        if name == 'HSV':
            min_value = 30
            max_value = 225
            init_value = 30
        if name == 'LAB':
            min_value = 3
            max_value = 255
            init_value = 3
        if name == 'Erosion':
            min_value = 3
            max_value = 101
            init_value = 3
        if name == 'Dilation':
            min_value = 3
            max_value = 101
            init_value = 3
        if name == 'Opening':
            min_value = 3
            max_value = 101
            init_value = 3
        if name == 'Closing':
            min_value = 3
            max_value = 101
            init_value = 3
        if name == 'Top Hat':
            min_value = 3
            max_value = 101
            init_value = 3
        if name == 'Black Hat':
            min_value = 3
            max_value = 101
            init_value = 3
        if name == 'Histogram Equalization':
            min_value = 3
            max_value = 255
            init_value = 3
        if name == 'Invert':
            min_value = 3
            max_value = 255
            init_value = 3
        if name == 'Canny':
            min_value = 3
            max_value = 255
            init_value = 3
        if name == 'Laplacian':
            min_value = 3
            max_value = 255
            init_value = 3

        self.filters.append(Filter(name, min_value, max_value, init_value))
        self.v_filters_lay.addWidget(self.filters[self.filter_count])
        self.filter_count += 1

        self.updateImages()

    def deleteFilter(self, filter_number):
        if self.filter_count > 0:
            to_delete = None
            for i, filter_del in enumerate(self.filters):
                if filter_del.filter_number == filter_number:
                    item_to_delete = self.v_filters_lay.takeAt(i)
                    item_to_delete.widget().deleteLater()
                    to_delete = i
            del self.filters[to_delete]
            self.filter_count -= 1

            for i in range(0, 10):
                QApplication.processEvents()
            self.resize(self.minimumSizeHint())
            self.updateImages()

    def createImagesLayout(self):
        # Horizontal layout for the two images
        self.h_img_lay = QHBoxLayout()
        self.h_img_lay.addStretch()
        self.h_img_lay.addWidget(self.original_image)
        self.h_img_lay.addWidget(self.processed_image)
        self.h_img_lay.addStretch()

    def createFiltersLayout(self):
        self.v_filters_lay = QVBoxLayout()

    def createMainLayout(self):
        # Creates the main layout (vertical)
        self.v_main_lay = QVBoxLayout()
        # Adds the images horizontal layout to the main layout
        self.v_main_lay.addLayout(self.h_img_lay)
        # Adds the buttons horizontal layout to the bottom of the main layout
        self.v_main_lay.addLayout(self.h_btn_lay)
        # Adds the sliders and their labels to the bottom of the main layout
        self.v_main_lay.addLayout(self.v_filters_lay)
        # Sets the main layout
        self.setLayout(self.v_main_lay)

        # Sets the geometry, position, window title and window default mode
        self.setGeometry(500, 100, 0, 0)
        self.setWindowTitle('Image processing')
        self.show()

    def createButtons(self):

        # ComboBox for filter selection
        self.filter_select = QComboBox()
        self.filter_select.addItems(['Threshold', 'Gaussian Threshold', 'HSV', 'LAB',
                                     'Erosion', 'Dilation', 'Opening', 'Closing',
                                     'Top Hat', 'Black Hat', 'Histogram Equalization',
                                     'Invert', 'Canny', 'Laplacian'])

        # Button for adding filters
        self.add_filter_btn = QPushButton('Add filter')
        self.add_filter_btn.clicked.connect(self.createNewFilter)

        # Button for selecting image
        self.select_image_btn = QPushButton('Open image')
        self.select_image_btn.clicked.connect(self.openImage)

        # Button for cleaning image
        self.clean_image_btn = QPushButton('Save images')
        self.clean_image_btn.clicked.connect(self.saveImages)

        # Horizontal layout for the buttons
        self.h_btn_lay = QHBoxLayout()
        self.h_btn_lay.addStretch(1)
        self.h_btn_lay.addWidget(self.filter_select)
        self.h_btn_lay.addWidget(self.add_filter_btn)
        self.h_btn_lay.addWidget(self.select_image_btn)
        self.h_btn_lay.addWidget(self.clean_image_btn)
        self.h_btn_lay.addStretch(1)

    def openImage(self):
        # Function for selecting the original image

        filter = "Images (*.png *.jpg)"
        image_path, _ = QFileDialog.getOpenFileName(
            self, 'Open image', 'Desktop', filter)
        self.path = image_path

        cv_img_bgr = cv2.imread(self.path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        self.original_image.updateImage(cv_img_rgb)
        self.updateImages()

    def saveImages(self):
        # Function for saving the processed image

        filter = "Images (*.png *.jpg)"

        image_path_orig, _ = QFileDialog.getSaveFileName(self, filter=filter)
        self.cv_img_processed_bgr = cv2.cvtColor(
            self.cv_img_processed_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path_orig, self.cv_img_processed_bgr)

        image_path_proc, _ = QFileDialog.getSaveFileName(self, filter=filter)
        self.orig_img_calculated_bgr = cv2.cvtColor(
            self.orig_img_calculated_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path_proc, self.orig_img_calculated_bgr)

    def updateImages(self):
        self.processImage()
        self.calculateOriginal()

    def processImage(self):
        # Function that processes the image using the OpenCV methods

        # Open the image
        self.cv_img_bgr = cv2.imread(self.path)
        self.cv_img_rgb = cv2.cvtColor(self.cv_img_bgr, cv2.COLOR_BGR2RGB)

        cv_before = self.cv_img_rgb

        if self.filter_count > 0:
            for i in range(0, self.filter_count):

                # Apply filters
                k = self.filters[i].k
                name = self.filters[i].name
                kernel = np.ones((k, k), np.uint8)

                if name == 'Invert':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.bitwise_not(cv_before)
                if name == 'Histogram Equalization':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cv_after = clahe.apply(cv_before)
                if name == 'Threshold':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    ret, cv_after = cv2.threshold(
                        cv_before, k, 255, cv2.THRESH_BINARY)
                if name == 'Gaussian Threshold':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.adaptiveThreshold(cv_before, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY, k, 2)
                if name == 'HSV':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2HSV)
                    lower_color = np.array([k - 35, 0, 0])
                    upper_color = np.array([k + 35, 255, 255])
                    cv_after = cv2.inRange(cv_before, lower_color, upper_color)
                if name == 'LAB':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2LAB)
                    L, a, b = cv2.split(cv_before)
                    ret, cv_after = cv2.threshold(L, k, 255, cv2.THRESH_BINARY)
                if name == 'Erosion':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.erode(cv_before, kernel, iterations=1)
                if name == 'Dilation':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.dilate(cv_before, kernel, iterations=1)
                if name == 'Opening':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.morphologyEx(
                        cv_before, cv2.MORPH_OPEN, kernel)
                if name == 'Closing':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.morphologyEx(
                        cv_before, cv2.MORPH_CLOSE, kernel)
                if name == 'Top Hat':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.morphologyEx(
                        cv_before, cv2.MORPH_TOPHAT, kernel)
                if name == 'Black Hat':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.morphologyEx(
                        cv_before, cv2.MORPH_BLACKHAT, kernel)
                if name == 'Canny':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.Canny(cv_before, 100, k)
                if name == 'Laplacian':
                    cv_before = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)
                    cv_after = cv2.Laplacian(cv_before, cv2.CV_64F)
                    cv_after = np.absolute(cv_after)
                    cv_after = np.uint8(cv_after)

                cv_before = cv2.cvtColor(cv_after, cv2.COLOR_GRAY2RGB)
        else:
            cv_after = cv2.cvtColor(cv_before, cv2.COLOR_RGB2GRAY)

        # Last image phase
        self.cv_img_processed_gray = cv_after

        # Convert image to RGB
        self.cv_img_processed_rgb = cv2.cvtColor(
            self.cv_img_processed_gray, cv2.COLOR_GRAY2RGB)

        # Updates the processed image frame
        self.processed_image.updateImage(self.cv_img_processed_rgb)

    def calculateOriginal(self):
        # Update original image with the contours

        self.orig_img_calculated_rgb = self.cv_img_rgb

        # Find contours
        contours, hierarchy = cv2.findContours(
            self.cv_img_processed_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #epsilon = 0.1 * cv2.arcLength(contours, True)
        #aprox_contours = cv2.approxPolyDP(contours, epsilon, True)

        # Apply contours
        cv2.drawContours(self.orig_img_calculated_rgb,
                         contours, -1, (0, 0, 255), 3)

        self.original_image.updateImage(self.orig_img_calculated_rgb)

    def setBackground(self):
        script_path = os.path.basename(
            os.path.dirname(os.path.realpath(__file__)))
        MainWindow.path = os.path.dirname(script_path) + 'default_BG.jpg'

        cv_img_bgr = cv2.imread(self.path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        self.original_image.updateImage(cv_img_rgb)
        self.processed_image.updateImage(cv_img_rgb)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
