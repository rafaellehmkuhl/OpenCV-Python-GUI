import sys
import numpy as np
import cv2
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog)

class Image(QWidget):
    """Common base for the images"""

    def __init__(self, name):
        super(Image, self).__init__()

        self.setFixedSize(500,500)

        # Label for the image
        self.name_lbl = QLabel(name)

        # Label (frame) where the original image will be located, with true scaling and maximum size
        self.frame_lbl = QLabel(self)
        self.frame_lbl.setMinimumSize(400,400)
        self.frame_lbl.setScaledContents(False)

        self.createLayout()

    def createLayout(self):
        self.v_lay = QVBoxLayout()

        self.v_lay.addWidget(self.name_lbl)
        self.v_lay.addWidget(self.frame_lbl)

    def updateImage(self, opencv_rgb_image):

        self.cv_img_rgb = opencv_rgb_image

        height, width, channel = self.cv_img_rgb.shape
        bytesPerLine = 3 * width
        self.q_image = QImage(self.cv_img_rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.frame_lbl.setPixmap(QPixmap.fromImage(self.q_image))

class Filter(QWidget):
    """Common base class for all filters"""
    defaultK = 3
    filterCount = 0

    def __init__(self, name, minValue, maxValue, init, parent=None):
        super(Filter, self).__init__(parent=parent)

        self.setMaximumHeight(65)

        self.k = init

        # Increase the number of filters created
        Filter.filterCount += 1

        # Variable for the slider/label layout
        self.lay = QHBoxLayout(self)

        # Variable for the constant of the OpenCV filter
        self.k = self.defaultK

        # Label for the slider
        self.k_lbl = QLabel(str(self.k))

        # Name for the slider
        self.name_lbl = QLabel(name)

        # Set default parameters
        self.setParameters(minValue, maxValue)

        # Adds the slider and it's label to the layout
        self.createLayout()

        # Function sending the slider signal to the processing function
        self.thresh_sld.valueChanged.connect(self.changeValue)

    def setParameters(self, minValue, maxValue):
        # Creates the slider for the OpenCV filter, with min, max, default and step values
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

class MainWindow(QWidget):

    filter_count = 0

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()
        self.filters = [None] * 100

    def initUI(self):

        self.original_image = Image('Original')
        self.processed_image = Image('Processed')
        self.setBackground()

        self.createImagesLayout()
        self.createFiltersLayout()
        self.createButtons()
        self.createMainLayout()

    def createNewFilter(self):

        self.filters[self.filter_count] = Filter('Filtro' + str(self.filter_count) + ': ', 3, 51, 3)
        self.v_filters_lay.addWidget(self.filters[self.filter_count])
        self.filter_count += 1

    def deleteFilter(self):
        if self.filter_count > 0:
            self.filter_count -= 1
            self.v_filters_lay.removeWidget(self.filters[self.filter_count])
            self.filters[self.filter_count].deleteLater()
            self.filters[self.filter_count] = None

            for i in range(0, 10):
                QApplication.processEvents()

            self.resize(self.minimumSizeHint())

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

        # Button for adding filters
        self.add_filter_btn = QPushButton('Add filter')
        self.add_filter_btn.clicked.connect(self.createNewFilter)

        # Create delete button
        self.delete_filter_btn = QPushButton('Delete last filter')
        self.delete_filter_btn.clicked.connect(self.deleteFilter)

        # Button for selecting image
        self.select_image_btn = QPushButton('Open image')
        self.select_image_btn.clicked.connect(self.openImage)

        # Button for cleaning image
        self.clean_image_btn = QPushButton('Save images')
        self.clean_image_btn.clicked.connect(self.saveImages)

        # Horizontal layout for the buttons
        self.h_btn_lay = QHBoxLayout()
        self.h_btn_lay.addStretch(1)
        self.h_btn_lay.addWidget(self.add_filter_btn)
        self.h_btn_lay.addWidget(self.delete_filter_btn)
        self.h_btn_lay.addWidget(self.select_image_btn)
        self.h_btn_lay.addWidget(self.clean_image_btn)
        self.h_btn_lay.addStretch(1)

    def openImage(self):
        # Function for selecting the original image

        filter = "Images (*.png *.jpg)"
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open image', 'Desktop', filter)
        self.path = image_path

        cv_img_bgr = cv2.imread(self.path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        self.original_image.updateImage(cv_img_rgb)
        self.updateImages()

    def saveImages(self):
        # Function for saving the processed image

        filter = "Images (*.png *.jpg)"

        image_path_orig, _ = QFileDialog.getSaveFileName(self, filter=filter)
        self.cv_img_processed_bgr = cv2.cvtColor(self.cv_img_processed_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path_orig, self.cv_img_processed_bgr)

        image_path_proc, _ = QFileDialog.getSaveFileName(self, filter=filter)
        self.orig_img_calculated_bgr = cv2.cvtColor(self.orig_img_calculated_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path_proc, self.orig_img_calculated_bgr)

    def updateImages(self):
        self.processImage()
        self.calculateOriginal()

    def processImage(self):
        # Function that processes the image using the OpenCV methods

        # Open the image
        self.cv_img_bgr = cv2.imread(self.path)
        self.cv_img_rgb = cv2.cvtColor(self.cv_img_bgr, cv2.COLOR_BGR2RGB)

        # Convert image to grayscale
        cv_img_gray = cv2.cvtColor(self.cv_img_bgr, cv2.COLOR_BGR2GRAY)

        cv_before = cv_img_gray

        if self.filter_count > 0:
            for i in range(0, self.filter_count):

                #Apply filters
                k = self.filters[i].k
                kernel = np.ones((k, k), np.uint8)
                cv_after = cv2.erode(cv_before, kernel, iterations = 1)
                #ret, cv_after = cv2.threshold(cv_before, 127, 255, cv2.THRESH_BINARY)
                cv_before = cv_after
        else:
            cv_after = cv_before

        # Last image phase
        self.cv_img_processed_gray = cv_after

        # Convert image to RGB
        self.cv_img_processed_rgb = cv2.cvtColor(self.cv_img_processed_gray, cv2.COLOR_GRAY2RGB)

        # Updates the processed image frame
        self.processed_image.updateImage(self.cv_img_processed_rgb)

    def calculateOriginal(self):
        # Update original image with the contours

        self.orig_img_calculated_rgb = self.cv_img_rgb

        # Find contours
        img, contours, hierarchy = cv2.findContours(self.cv_img_processed_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Apply contours
        cv2.drawContours(self.orig_img_calculated_rgb, contours, -1, (0, 0, 255), 3)

        self.original_image.updateImage(self.orig_img_calculated_rgb)

    def setBackground(self):
        script_path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        MainWindow.path = os.path.dirname(script_path) + 'default_BG.jpg'

        cv_img_bgr = cv2.imread(self.path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        self.original_image.updateImage(cv_img_rgb)
        self.processed_image.updateImage(cv_img_rgb)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())