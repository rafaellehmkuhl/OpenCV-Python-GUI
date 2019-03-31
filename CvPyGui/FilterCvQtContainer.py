from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                             QPushButton, QSlider)


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
        self.process()

    def resetValue(self):
        # Resets the K value to it's default
        self.changeValue(self.defaultK)

    def deleteFilter(self):
        self.parent().parent().deleteFilter(self.filter_number)

    def process(self):

        k = self.k[0]

        if self.name == 'Moving Average':
            self.filtered_df = self.parent().variable_df.rolling(window=int(k), center=True).median().fillna(method='ffill').fillna(method='bfill')
            self.parent().variable_df = self.filtered_df
            self.parent().updatePlot()
        elif self.name == 'Set maximum':
            pass
        return