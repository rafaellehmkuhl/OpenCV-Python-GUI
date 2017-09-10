if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication
    import sys
    from FeatureSelector import app

    app = QApplication(sys.argv)
    window = app.FeatureSelector()
    window.show()
    sys.exit(app.exec_())
