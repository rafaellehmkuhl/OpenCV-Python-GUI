import sys
import numpy as np
import cv2
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QAction)


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        # Variable for the path of the image
        self.path = None

        # Variables for the constants of the OpenCV filters
        self.k1 = 3
        self.k2 = 99
        self.k3 = 51
        self.k4 = 3

        # Labels for the images
        original_img_label = QLabel('Original')
        processed_img_label = QLabel('Processed')

        # Labels for the sliders
        self.k1_lbl = QLabel(str(self.k1))
        self.k2_lbl = QLabel(str(self.k2))
        self.k3_lbl = QLabel(str(self.k3))
        self.k4_lbl = QLabel(str(self.k4))

        # Label (frame) where the original image will be located, with true scaling and maximum size
        self.orig_lbl = QLabel(self)
        self.orig_lbl.setScaledContents(True)
        self.orig_lbl.setMaximumSize(700,700)

        # Label (frame) where the processed image will be located, with true scaling and maximum size
        self.proc_lbl = QLabel(self)
        self.proc_lbl.setScaledContents(True)
        self.proc_lbl.setMaximumSize(700,700)

        # Button for selecting image
        select_image_btn = QPushButton('Select image')
        select_image_btn.clicked.connect(self.get_image)

        # Button for cleaning image
        clean_image_btn = QPushButton('Save image')
        clean_image_btn.clicked.connect(self.save_image)

        # Slider for the first OpenCV filter, with min, max, default and step values
        self.thresh1_sld = QSlider(Qt.Horizontal, self)
        self.thresh1_sld.setFocusPolicy(Qt.NoFocus)
        self.thresh1_sld.setMinimum(3)
        self.thresh1_sld.setMaximum(51)
        self.thresh1_sld.setValue(self.k1)
        self.thresh1_sld.setSingleStep(2)
        #Function sending the slider signal to the processing function
        self.thresh1_sld.valueChanged[int].connect(self.changeValue1)

        # Slider for the second OpenCV filter, with min, max, default and step values
        self.thresh2_sld = QSlider(Qt.Horizontal, self)
        self.thresh2_sld.setFocusPolicy(Qt.NoFocus)
        self.thresh2_sld.setMinimum(3)
        self.thresh2_sld.setMaximum(151)
        self.thresh2_sld.setValue(self.k2)
        self.thresh2_sld.setSingleStep(2)
        # Function sending the slider signal to the processing function
        self.thresh2_sld.valueChanged[int].connect(self.changeValue2)

        # Slider for the third OpenCV filter, with min, max, default and step values
        self.thresh3_sld = QSlider(Qt.Horizontal, self)
        self.thresh3_sld.setFocusPolicy(Qt.NoFocus)
        self.thresh3_sld.setMinimum(3)
        self.thresh3_sld.setMaximum(101)
        self.thresh3_sld.setValue(self.k3)
        self.thresh3_sld.setSingleStep(2)
        # Function sending the slider signal to the processing function
        self.thresh3_sld.valueChanged[int].connect(self.changeValue3)

        # Slider for the fourth OpenCV filter, with min, max, default and step values
        self.thresh4_sld = QSlider(Qt.Horizontal, self)
        self.thresh4_sld.setFocusPolicy(Qt.NoFocus)
        self.thresh4_sld.setMinimum(3)
        self.thresh4_sld.setMaximum(51)
        self.thresh4_sld.setValue(self.k4)
        self.thresh4_sld.setSingleStep(2)
        # Function sending the slider signal to the processing function
        self.thresh4_sld.valueChanged[int].connect(self.changeValue4)

        # Vertical layout for the original image and label
        v_orig_lay = QVBoxLayout()
        v_orig_lay.addWidget(original_img_label)
        v_orig_lay.addStretch(1)
        v_orig_lay.addWidget(self.orig_lbl)
        v_orig_lay.addStretch(1)

        # Vertical layout for the processed image and label
        v_proc_lay = QVBoxLayout()
        v_proc_lay.addWidget(processed_img_label)
        v_proc_lay.addStretch(1)
        v_proc_lay.addWidget(self.proc_lbl)
        v_proc_lay.addStretch(1)

        # Horizontal layout for the two images
        h_img_lay = QHBoxLayout()
        h_img_lay.addStretch(1)
        h_img_lay.addLayout(v_orig_lay)
        h_img_lay.addStretch(1)
        h_img_lay.addLayout(v_proc_lay)
        h_img_lay.addStretch(1)

        # Horizontal layout for the buttons
        h_btn_lay = QHBoxLayout()
        h_btn_lay.addStretch(1)
        h_btn_lay.addWidget(select_image_btn)
        h_btn_lay.addWidget(clean_image_btn)
        h_btn_lay.addStretch(1)

        # Creates the main layout (vertical)
        v_main_lay = QVBoxLayout()
        # Adds the images horizontal layout to the main layout
        v_main_lay.addLayout(h_img_lay)
        # Adds the sliders and their labels to the bottom of the main layout
        v_main_lay.addWidget(self.k1_lbl)
        v_main_lay.addWidget(self.thresh1_sld)
        v_main_lay.addWidget(self.k2_lbl)
        v_main_lay.addWidget(self.thresh2_sld)
        v_main_lay.addWidget(self.k3_lbl)
        v_main_lay.addWidget(self.thresh3_sld)
        v_main_lay.addWidget(self.k4_lbl)
        v_main_lay.addWidget(self.thresh4_sld)
        # Adds the buttons horizontal layout to the bottom of the main layout
        v_main_lay.addLayout(h_btn_lay)

        # Sets the main layout
        self.setLayout(v_main_lay)

        # Sets the geometry, position, window title and window default mode
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.showMaximized()

    def get_image(self):
        # Function for selecting the original image

        self.k1 = 3
        self.k2 = 99
        self.k3 = 51
        self.k4 = 3
        self.thresh1_sld.setValue(self.k1)
        self.thresh2_sld.setValue(self.k2)
        self.thresh3_sld.setValue(self.k3)
        self.thresh4_sld.setValue(self.k4)

        filter = "Images (*.png *.jpg)"
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open image', 'Desktop', filter)
        self.path = image_path

        cv_img_bgr = cv2.imread(self.path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        height, width, channel = cv_img_rgb.shape
        bytesPerLine = 3 * width
        img_rgb = QImage(cv_img_rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.orig_lbl.setPixmap(QPixmap.fromImage(img_rgb))
        self.process_image()

    def save_image(self):
        # Function for saving the processed image

        filter = "Images (*.png *.jpg)"

        image_path_orig, _ = QFileDialog.getSaveFileName(self, filter=filter)
        self.cv_img_cont_bgr = cv2.cvtColor(self.cv_img_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path_orig, self.cv_img_cont_bgr)

        image_path_proc, _ = QFileDialog.getSaveFileName(self, filter=filter)
        cv2.imwrite(image_path_proc, self.final_cv_img)

    def changeValue1(self, value1):
        # Function for setting the value of k1

        if value1%2 == 1:
            self.k1 = value1
        else:
            self.k1 = value1 + 1

        self.k1_lbl.setText(str(self.k1))
        self.process_image()

    def changeValue2(self, value2):
        # Function for setting the value of k2

        if value2%2 == 1:
            self.k2 = value2
        else:
            self.k2 = value2 + 1

        self.k2_lbl.setText(str(self.k2))
        self.process_image()

    def changeValue3(self, value3):
        # Function for setting the value of k3

        if value3%2 == 1:
            self.k3 = value3
        else:
            self.k3 = value3 + 1

        self.k3_lbl.setText(str(self.k3))
        self.process_image()

    def changeValue4(self, value4):
        # Function for setting the value of k3

        if value4%2 == 1:
            self.k4 = value4
        else:
            self.k4 = value4 + 1

        self.k4_lbl.setText(str(self.k4))
        self.process_image()

    def process_image(self):
        # Function that processes the image using the OpenCV methods

        # Open the image
        cv_img_bgr = cv2.imread(self.path)

        # Convert image to HSV
        cv_img_hsv = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2HSV)

        # Define range of desired color in HSV
        lower_color = np.array([30, 0, 35])
        upper_color = np.array([90, 255, 200])

        hsv_mask = cv2.inRange(cv_img_hsv, lower_color, upper_color)

        # Convert image to grayscale
        cv_img_gray = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2GRAY)

        # Apply blur
        cv_img_blur = cv2.GaussianBlur(hsv_mask, (self.k1, self.k1), 0)
        #cv_img_blur = cv2.bilateralFilter(cv_img_gray, self.k1, self.k3, self.k3)

        # Apply threshold
        #cv_img_thr = cv2.adaptiveThreshold(cv_img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.k2, 2)

        # Inverts black-white
        #cv_img_invert = cv2.bitwise_not(cv_img_thr)

        # Apply Top Hat
        opening_kernel = np.ones((self.k3, self.k3), np.uint8)
        cv_img_open = cv2.morphologyEx(cv_img_blur, cv2.MORPH_TOPHAT, opening_kernel)

        # Apply erosion
        erosion_kernel = np.ones((self.k4, self.k4), np.uint8)
        cv_img_eros = cv2.morphologyEx(cv_img_open, cv2.MORPH_CLOSE, erosion_kernel)

        # Convert image to RGB
        self.final_cv_img = cv2.cvtColor(cv_img_eros, cv2.COLOR_GRAY2RGB)

        # Convert image to QImage
        height, width, channel = self.final_cv_img.shape
        bytesPerLine = 3 * width
        self.final_qt_img = QImage(self.final_cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        # Updates the processed image frame
        self.proc_lbl.setPixmap(QPixmap.fromImage(self.final_qt_img))


        # Update original image with the contours
        self.cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)

        # Find contours
        img, contours, hierarchy = cv2.findContours(cv_img_eros, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Apply contours
        cv2.drawContours(self.cv_img_rgb, contours, -1, (0, 0, 255), 1)

        height, width, channel = self.cv_img_rgb.shape
        bytesPerLine = 3 * width
        qt_img_rgb = QImage(self.cv_img_rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.orig_lbl.setPixmap(QPixmap.fromImage(qt_img_rgb))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())