import sys
from PyQt5.QtWidgets import QApplication
import Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main.MyApp()
    window.show()
    sys.exit(app.exec_())
