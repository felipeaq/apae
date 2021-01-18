from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

from train_controller import TrainController
import threading
import time


class TrainUi(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(TrainUi, self).__init__()
        uic.loadUi('../interfaces/treinamento.ui', self)  # Load the .ui file
        self.controller = TrainController()
        self.buttons = set()
        self.button_list = {"append_data": self.append_data_func, "update_phrase": self.update_phrase_func,
                            "delete_phrase": self.delete_phrase_func, "append_phrase": self.append_phrase_func, "delete_last": self.delete_last_func,
                            "train": self.train_func}
        self.bind()

        self.show()

    def bind(self):
        for button_name, button_func in self.button_list.items():

            button = self.findChild(
                QtWidgets.QPushButton, button_name)
            button.clicked.connect(button_func)
            self.buttons.add(button)
        self.list_phrases = self.findChild(QtWidgets.QListWidget, "listPhrase")
        self.list_phrases.addItems(self.controller.load_phrases())
        self.list_phrases.clicked.connect(self.select_phrase)

        self.phrase = self.findChild(QtWidgets.QLineEdit, "phrase")
        self.phrase.setReadOnly(True)

        self.new_phrase_text = self.findChild(
            QtWidgets.QLineEdit, "new_phrase_text")

        self.moving = self.findChild(QtWidgets.QLabel, "moving")
        print(self.moving, ",,")
        t = threading.Thread(target=self.is_moving, args=())
        t.start()

    def append_data_func(self):
        if not self.phrase.text():
            return
        self.controller.append_data(self.phrase.text())

    def update_phrase_func(self):

        row = self.list_phrases.currentRow()
        if not self.phrase.text() or not self.new_phrase_text.text() or self.new_phrase_text.text() in self.controller.load_phrases():
            return
        self.controller.update_phrase(
            self.list_phrases.currentItem().text(), self.new_phrase_text.text())
        self.update_list()
        self.list_phrases.setCurrentRow(row)
        # self.list_phrases.
        self.phrase.setText(self.list_phrases.currentItem().text())

    def delete_phrase_func(self):
        if not self.phrase.text():
            return
        self.controller.delete_phrase(self.phrase.text())
        self.update_list()
        self.phrase.setText("")

    def append_phrase_func(self):

        if not self.new_phrase_text.text() or self.new_phrase_text.text() in self.controller.load_phrases():
            return

        self.controller.append_phrase(self.new_phrase_text.text())
        self.list_phrases.addItem(self.new_phrase_text.text())

    def delete_last_func(self):
        self.controller.delete_last()

    def train_func(self):
        self.controller.train()

    def select_phrase(self):
        self.phrase.setText(self.list_phrases.currentItem().text())

    def update_list(self):
        self.list_phrases.clear()
        self.list_phrases.addItems(self.controller.load_phrases())

    def is_moving(self):

        while True:
            if self.controller.is_stoped():
                self.moving.setText("Mão parada")
            else:
                self.moving.setText("Mão em movimento")

            time.sleep(0.1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TrainUi()
    app.exec_()


if __name__ == "__main__":
    main()
