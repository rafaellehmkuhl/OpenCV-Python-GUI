if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from CvPyGui import Main

    app = QApplication(sys.argv)
    window = Main.MyApp()
    window.show()
    sys.exit(app.exec_())
