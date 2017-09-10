import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog)

from CvPyGui import FilterCvQtContainer
from CvPyGui import ImageCvQtContainer
from CvPyGui.ui import gui

Ui_MainWindow = gui.Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):

    filter_count = 0

    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.initUI()
        self.filters = []

    def initUI(self):

        self.original_image = ImageCvQtContainer.Image(
            'Original', self.original_frame_lbl)
        self.processed_image = ImageCvQtContainer.Image(
            'Processed', self.processed_frame_lbl)
        self.setBackground()
        self.createButtons()

    def createNewFilter(self):
        name = self.filter_select.currentText()

        filters_types = {}
        filters_types["Threshold"] = [3, 255, 3, 1]
        filters_types["Gaussian Threshold"] = [31, 255, 3, 1]
        filters_types["HSV"] = [30, 255, 30, 1]
        filters_types["LAB"] = [3, 255, 3, 1]
        filters_types["Erosion"] = [3, 101, 3, 1]
        filters_types["Dilation"] = [3, 101, 3, 1]
        filters_types["Opening"] = [3, 101, 3, 1]
        filters_types["Closing"] = [3, 101, 3, 1]
        filters_types["Top Hat"] = [3, 101, 3, 1]
        filters_types["Black Hat"] = [3, 101, 3, 1]
        filters_types["Histogram Equalization"] = [3, 255, 3, 1]
        filters_types["Invert"] = [3, 255, 3, 1]
        filters_types["Canny Edges"] = [3, 255, 3, 1]
        filters_types["Laplacian"] = [3, 255, 3, 1]
        filter_params = filters_types[name]

        self.filters.append(FilterCvQtContainer.Filter(
            name, filter_params[0], filter_params[1], filter_params[2], filter_params[3], self))
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

    def createButtons(self):

        # ComboBox for filter selection
        self.filter_select.addItems(['Threshold', 'Gaussian Threshold', 'HSV', 'LAB',
                                     'Erosion', 'Dilation', 'Opening', 'Closing',
                                     'Top Hat', 'Black Hat', 'Histogram Equalization',
                                     'Invert', 'Canny', 'Laplacian'])

        # Button for adding filters
        self.add_filter_btn.clicked.connect(self.createNewFilter)
        # Checkbox for countours
        self.countours_check_box.stateChanged.connect(self.calculateOriginal)
        # Button for selecting image
        self.actionOpen_image.triggered.connect(self.openImage)
        # Buttons for saving images
        self.actionSave_processed_image.triggered.connect(self.processed_image.saveImage)
        self.actionSave_original_image.triggered.connect(self.original_image.saveImage)

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

    def updateImages(self):
        self.calculateProcessed()
        self.calculateOriginal()

    def setBackground(self):
        cv_img_rgb = np.zeros((700,700,3))
        self.original_image.updateImage(cv_img_rgb)
        self.processed_image.updateImage(cv_img_rgb)

    def calculateProcessed(self):
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
                cv_after = self.filters[i].process(cv_before, name)
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

        orig = self.orig_img_calculated_rgb = cv2.imread(self.path)
        orig = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)

        if self.countours_check_box.isChecked():

            # Find contours
            im, contours, hierarchy = cv2.findContours(
                self.cv_img_processed_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Apply contours
            cv2.drawContours(orig,
                             contours, -1, (0, 0, 255), 3)
        else:
            pass

        self.original_image.updateImage(orig)
