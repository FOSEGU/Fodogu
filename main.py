import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

ui = uic.loadUiType('UI/main.ui')[0]
class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
