# python3
# Subin Jo
# 2022. 10. 31

import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import decode, extractDJI, showFlight

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

        self.csv_btn.clicked.connect(self.showCSV)

    def selectDAT(self):
        # path = select input .DAT file path
        path = QFileDialog.getOpenFileName(self, "Select File")
        if path[0]:
            self.ifn = path[0]
            self.d_itext.setText(self.ifn)
            self.e_itext.setText(self.ifn)
        else:
            QMessageBox.about(self, 'Warning', 'you didn\'t select a file.')
        # self.d_itext.repaint()

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
        # print("self.strResult: ", self.strResult)
        self.strResult += "Complete Decoding\n"
        self.d_result.setText(self.strResult)

    def startExtract(self):
        self.strResult += "Start Extracting\n"
        self.strResult = extractDJI.extractDJI_main(self.ifn, self.ofn, self.strResult)
        self.strResult += "Complete Extracting\n"
        self.e_result.setText(self.strResult)

    def showFlight(self):
        if os.path.exists(self.ifn) and os.path.exists(self.ofn):
            p = self.ofn + "/" + os.path.basename(self.ifn) + "_output.csv"
            print(p)
            if os.path.exists(p):
                print("Show Flight Window")
                sw = FlightWindow(p)
                sw.exec()
            else:
                print("CSV not found")
        else:
            print("File Not Found")


class FlightWindow(QtWidgets.QDialog, QWidget):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle('Flight')
        self.w_width, self.w_height = 800, 500
        self.setMinimumSize(self.w_width, self.w_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        lines = showmap.getGPS(path)
        mdata = showmap.mappingGPS(lines)
        webview = QWebEngineView()
        webview.setHtml(mdata.getvalue().decode())
        layout.addWidget(webview)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
