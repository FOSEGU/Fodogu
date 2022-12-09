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
    strResult = ""

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
            QMessageBox.about(self, 'Warning', 'you didn\'t select a file.')
        #self.d_itext.repaint()

    def selectDir(self):
        # path = select output dir path
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.ofn = path
            self.d_otext.setText(self.ofn)
            self.e_otext.setText(self.ofn)
        else:
            QMessageBox.about(self, 'Warning', 'you didn\'t select a folder.')


    def startDecode(self):
        self.strResult += "Start Decoding\n"
        self.strResult = decode.checkType(self.ifn, self.ofn, self.strResult)
        #print("self.strResult: ", self.strResult)
        self.strResult += "Complete Decoding\n"
        self.d_result.setText(self.strResult)

    def startExtract(self):
        self.strResult += "Start Extracting\n"
        self.strResult = extractDJI.extractDJI_main(self.ifn, self.ofn, self.strResult)
        self.strResult += "Complete Extracting\n"
        self.e_result.setText(self.strResult)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
