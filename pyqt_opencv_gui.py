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

        self.setMinimumSize(500,500)

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
        self.addToLayout()

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

    def addToLayout(self):
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
        self.parent().process_image()

    def resetValue(self):
        # Resets the K value to it's default
        self.changeValue(self.defaultK)

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):

        self.filter1 = Filter("HSV", 30, 225, 30)
        self.filter2 = Filter("Gaussian", 3, 51, 3)
        self.filter3 = Filter("Opening", 3, 51, 3)
        self.filter4 = Filter("Erosion", 3, 51, 3)

        self.original_image = Image('Original')
        self.processed_image = Image('Processed')
        self.setBackground()

        self.createImagesLayout()
        self.createButtons()
        self.createMainLayout()

    def createImagesLayout(self):
        # Horizontal layout for the two images
        self.h_img_lay = QHBoxLayout()
        self.h_img_lay.addStretch()
        self.h_img_lay.addWidget(self.original_image)
        self.h_img_lay.addWidget(self.processed_image)
        self.h_img_lay.addStretch()


    def createMainLayout(self):
        # Creates the main layout (vertical)
        self.v_main_lay = QVBoxLayout()
        # Adds the images horizontal layout to the main layout
        self.v_main_lay.addLayout(self.h_img_lay)
        # Adds the sliders and their labels to the bottom of the main layout
        self.v_main_lay.addWidget(self.filter1)
        self.v_main_lay.addWidget(self.filter2)
        self.v_main_lay.addWidget(self.filter3)
        self.v_main_lay.addWidget(self.filter4)
        # Adds the buttons horizontal layout to the bottom of the main layout
        self.v_main_lay.addLayout(self.h_btn_lay)
        # Sets the main layout
        self.setLayout(self.v_main_lay)

        # Sets the geometry, position, window title and window default mode
        self.setGeometry(500, 150, 0, 0)
        self.setWindowTitle('Image processing')
        self.show()

    def createButtons(self):
        # Button for selecting image
        self.select_image_btn = QPushButton('Select image')
        self.select_image_btn.clicked.connect(self.get_image)

        # Button for cleaning image
        self.clean_image_btn = QPushButton('Save image')
        self.clean_image_btn.clicked.connect(self.save_image)

        # Horizontal layout for the buttons
        self.h_btn_lay = QHBoxLayout()
        self.h_btn_lay.addStretch(1)
        self.h_btn_lay.addWidget(self.select_image_btn)
        self.h_btn_lay.addWidget(self.clean_image_btn)
        self.h_btn_lay.addStretch(1)

    def get_image(self):
        # Function for selecting the original image

        filter = "Images (*.png *.jpg)"
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open image', 'Desktop', filter)
        self.path = image_path

        cv_img_bgr = cv2.imread(self.path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        self.original_image.updateImage(cv_img_rgb)
        self.process_image()

    def save_image(self):
        # Function for saving the processed image

        filter = "Images (*.png *.jpg)"

        image_path_orig, _ = QFileDialog.getSaveFileName(self, filter=filter)
        self.cv_img_cont_bgr = cv2.cvtColor(self.cv_img_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path_orig, self.cv_img_cont_bgr)

        image_path_proc, _ = QFileDialog.getSaveFileName(self, filter=filter)
        cv2.imwrite(image_path_proc, self.final_cv_img)

    def process_image(self):
        # Function that processes the image using the OpenCV methods

        # Open the image
        cv_img_bgr = cv2.imread(self.path)

        # Convert image to HSV
        cv_img_hsv = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2HSV)

        # Define range of desired color in HSV
        lower_color = np.array([self.filter1.k - 30, 0, 35])
        upper_color = np.array([self.filter1.k + 30, 255, 200])

        hsv_mask = cv2.inRange(cv_img_hsv, lower_color, upper_color)

        # Convert image to grayscale
        cv_img_gray = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2GRAY)

        # Apply blur
        cv_img_blur = cv2.GaussianBlur(hsv_mask, (self.filter2.k, self.filter2.k), 0)
        #cv_img_blur = cv2.bilateralFilter(cv_img_gray, self.k1, self.k3, self.k3)

        # Apply threshold
        #cv_img_thr = cv2.adaptiveThreshold(cv_img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.k2, 2)

        # Inverts black-white
        #cv_img_invert = cv2.bitwise_not(cv_img_thr)

        # Apply Top Hat
        opening_kernel = np.ones((self.filter3.k, self.filter3.k), np.uint8)
        cv_img_open = cv2.morphologyEx(cv_img_blur, cv2.MORPH_TOPHAT, opening_kernel)

        # Apply erosion
        erosion_kernel = np.ones((self.filter4.k, self.filter4.k), np.uint8)
        cv_img_eros = cv2.morphologyEx(cv_img_open, cv2.MORPH_CLOSE, erosion_kernel)

        # Convert image to RGB
        self.final_cv_img = cv2.cvtColor(cv_img_eros, cv2.COLOR_GRAY2RGB)

        # Updates the processed image frame
        self.processed_image.updateImage(self.final_cv_img)


        # Update original image with the contours
        self.cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        # Find contours
        img, contours, hierarchy = cv2.findContours(cv_img_eros, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Apply contours
        cv2.drawContours(self.cv_img_rgb, contours, -1, (0, 0, 255), 1)

        self.original_image.updateImage(self.cv_img_rgb)

    def setBackground(self):
        self.script_path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        MainWindow.path = os.path.dirname(self.script_path) + 'default_BG.jpg'

        self.cv_img_bgr = cv2.imread(self.path)
        self.cv_img_rgb = cv2.cvtColor(self.cv_img_bgr, cv2.COLOR_BGR2RGB)

        self.original_image.updateImage(self.cv_img_rgb)
        self.processed_image.updateImage(self.cv_img_rgb)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())