import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import decode

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

    def selectDAT(self):
        # path = select input .DAT file path
        path = QFileDialog.getOpenFileName(self, "Select File")
        if path[0]:
            self.ifn = path[0]
            self.d_itext.setText(self.ifn)
        else:
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')
        #self.d_itext.repaint()

    def selectDir(self):
        # path = select output dir path
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.ofn = path
            self.d_otext.setText(self.ofn)
        else:
            QMessageBox.about(self, 'Warning', '폴더를 선택하지 않았습니다.')


    def startDecode(self):
        strResult = ""
        strResult += "Start Decoding\n"
        decode.checkType(self.ifn, self.ofn)
        strResult += "Complete Decoding\n"
        self.d_result.setText(strResult)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
