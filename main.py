# python3
# Subin Jo
# 2022. 10. 31

import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import decode, extractDJI

ui = uic.loadUiType('UI/main.ui')[0]


class MainWindow(QMainWindow, ui):
    ifn = ""
    ofn = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.d_inputbtn.clicked.connect(self.selectDAT)
        self.d_outputbtn.clicked.connect(self.selectDir)
        self.d_startbtn.clicked.connect(self.startDecode)

        self.e_inputbtn.clicked.connect(self.selectDAT)
        self.e_outputbtn.clicked.connect(self.selectDir)
        self.e_startbtn.clicked.connect(self.startExtract)

    def selectDAT(self):
        # path = select input .DAT file path
        path = QFileDialog.getOpenFileName(self, "Select File")
        if path[0]:
            self.ifn = path[0]
            self.d_itext.setText(self.ifn)
            self.e_itext.setText(self.ifn)
        else:
            QMessageBox.about(self, 'Warning', 'you didn\' select a file.')
        #self.d_itext.repaint()

    def selectDir(self):
        # path = select output dir path
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.ofn = path
            self.d_otext.setText(self.ofn)
            self.e_otext.setText(self.ofn)
        else:
            QMessageBox.about(self, 'Warning', 'you didn\' select a folder.')


    def startDecode(self):
        strResult = ""
        strResult += "Start Decoding\n"
        decode.checkType(self.ifn, self.ofn)
        strResult += "Complete Decoding\n"
        self.d_result.setText(strResult)

    def startExtract(self):
        strResult = ""
        strResult += "Start Extracting\n"
        extractDJI.extractDJI_main(self.ifn, self.ofn)
        strResult += "Complete Extracting\n"
        self.e_result.setText(strResult)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
