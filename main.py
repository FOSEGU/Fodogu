import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

ui = uic.loadUiType('UI/main.ui')[0]
class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        global e_ifn, e_ofn, d_ifn, d_ofn
        e_ifn = self.e_inputbtn.clicked.connect(self.selectDAT)
        e_ofn = self.e_outputbtn.clicked.connect(self.selectDir)
        d_ifn = self.d_inputbtn.clicked.connect(self.selectDAT)
        d_ofn = self.d_outputbtn.clicked.connect(self.selectDir)

    def selectDAT(self):
        # path = select input .DAT file path
        path = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File")
        return path

    def selectDir(self):
        # path = select output dir path
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Destination")
        return path

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
