if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication
    import sys
    from FeatureSelectorProject.FeatureSelectorApp import MainApp

    app = QApplication(sys.argv)
    window = MainApp.MyApp()
    window.show()
    sys.exit(app.exec_())
