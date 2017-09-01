from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QFileDialog
import cv2


class Image(QWidget):
    """Common base for the images"""

    def __init__(self, name, label):
        super().__init__()

        # Label (frame) where the original image will be located, with scaling
        self.frame_lbl = label

    def updateImage(self, opencv_rgb_image):

        self.cv_img_rgb = opencv_rgb_image

        height, width, channel = self.cv_img_rgb.shape
        bytesPerLine = 3 * width
        self.q_image = QImage(self.cv_img_rgb.data, width,
                              height, bytesPerLine, QImage.Format_RGB888)

        self.frame_lbl.setPixmap(QPixmap.fromImage(self.q_image))

    def saveImage(self):
        # Function for saving the processed image

        filter = "Images (*.png *.jpg)"

        image_path, _ = QFileDialog.getSaveFileName(self, filter=filter)

        cv_img_bgr = cv2.cvtColor(
            self.cv_img_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path, cv_img_bgr)
