import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog)

from CvPyGui import FilterCvQtContainer
from CvPyGui.ui import gui3

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

Ui_MainWindow = gui3.Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):

    filter_count = 0
    plots = []

    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.initUI()

        self.plots.append(self.plot1)
        self.plots.append(self.plot2)
        self.plots.append(self.plot3)

    def initUI(self):

        self.toolbar = NavigationToolbar(self.plot1.canvas, self)
        self.addToolBar(self.toolbar)
        self.actionLoad_data.triggered.connect(self.LoadDataFile)

    def LoadDataFile(self):
        # Function for selecting the original image
        filter = "Data file (*.csv, *.txt)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open image', 'Desktop', filter)
        self.path = file_path
        self.original_df = pd.read_csv(self.path, sep='.', delimiter='\t', na_values=['NaN', 'OutOfRange'], skiprows=(0,1,2,3,4,5,7))
        self.original_df['Tempo zerado'] = self.original_df['Tempo'] - self.original_df['Tempo'][0]
        self.original_df = self.original_df.set_index('Tempo zerado')
        for plot in self.plots:
            plot.comboLoadVariable.addItems(list(self.original_df))
            plot.connectButtons()
