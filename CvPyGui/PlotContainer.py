import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton, QSlider,
                             QComboBox)

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .FilterCvQtContainer import Filter

import random

class SinglePlotContainer(QWidget):

    num_plots = 0

    def __init__(self, parent=None):
        super().__init__()

        self.num_plots += 1

        self.variable_df = pd.DataFrame()

        self.figure = Figure() # don't use matplotlib.pyplot at all!
        self.canvas = FigureCanvas(self.figure)

        self.hLayout = QHBoxLayout(self)
        self.dataConfigColumn = QVBoxLayout()
        self.filtersColumn = QVBoxLayout()

        self.hLayout.addLayout(self.dataConfigColumn)
        self.hLayout.addWidget(self.canvas)
        self.hLayout.addLayout(self.filtersColumn)

        self.comboLoadVariable = QComboBox()
        self.dataConfigColumn.addWidget(self.comboLoadVariable)

        self.filter1 = Filter('Moving Average', 3, 30, 5, 1)
        self.filtersColumn.addWidget(self.filter1)

        # drawEvent = self.figure.canvas.mpl_connect('draw', self.updatePlot)

        self.plotRandom()

    def connectButtons(self):
        self.comboLoadVariable.activated[str].connect(self.loadVariable)

    def loadVariable(self, variable):
        self.variable_df = self.parent().parent().original_df[variable]
        self.plot()

    def plot(self):
        if self.num_plots != 0:
            self.axes = self.figure.add_subplot(111, sharex=self.parent().parent().plots[0].axes)
        else:
            self.axes = self.figure.add_subplot(111)
        self.axes.clear()
        self.axes.plot(self.variable_df, '-')
        self.canvas.draw()

    def updatePlot(self):
        ymax,ymin = self.axes.get_ylim()
        self.axes.clear()
        self.axes.set_ylim(ymax,ymin)
        self.axes.plot(self.variable_df, '-')
        self.canvas.draw()

    def plotRandom(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(10)]
        self.axes = self.figure.add_subplot(111)
        self.axes.clear()
        self.axes.plot(data, '-')
        self.canvas.draw()
