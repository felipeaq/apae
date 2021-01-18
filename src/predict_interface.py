from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

from predict_controller import *
import threading
import time


class PredictUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(PredictUi, self).__init__()
        uic.loadUi('../interfaces/predicao.ui', self) 
        self.controller=PredictController()
        self.bind()
        self.show()
        t = threading.Thread(target=self.predict, args=())
        t.start()

    def bind(self):
        self.phrase_edit.setReadOnly(True)

    def predict(self):
        while True:
            
            text=self.controller.predict()[0]
            print (text)
            if text:
                self.phrase_edit.setText(text)
            time.sleep(0.1)

    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PredictUi()
    app.exec_()

if __name__=="__main__":
    main()