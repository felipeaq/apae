from read_routine import *
from bt_connection import *


import train_interface
from data_saver import *
from glove_model import *
import time


class TrainController:
    def __init__(self, file_data="../res/data.csv", file_phrase="../res/class.csv", one_file="../res/onefile.pkl", class_file="../res/multifile.pkl"):

        self.saver = DataSaver(file_data, file_phrase)
        self.__phrases = self.saver.load_phrase()
        self.model = GloveModel(one_file, class_file)

    def load_phrases(self) -> list:
        return self.__phrases

    def append_data(self, phrase: str) -> None:
        if self.is_stoped():
            self.saver.save_data(phrase, ReadRoutine().sensors)
        else:
            print("mão em movimento")
            # TODO colocar na interface grafica

    def update_phrase(self, old_phrase: str, new_phrase: str) -> None:
        print("update phrase", old_phrase, new_phrase)
        for i, item in enumerate(self.__phrases):
            if item == old_phrase:
                self.__phrases[i] = new_phrase
        self.saver.save_phrase(self.__phrases)
        self.saver.update_phrase(old_phrase, new_phrase)

    def delete_phrase(self, phrase: str) -> None:
        print("delete phrase", phrase)
        self.__phrases.remove(phrase)
        self.saver.save_phrase(self.__phrases)
        self.saver.delete_phrase(phrase)

    def append_phrase(self, phrase: str) -> None:
        self.__phrases.append(phrase)
        print("append phrase", phrase)
        self.saver.save_phrase(self.__phrases)

    def delete_last(self) -> None:
        self.saver.delete_last()

    def train(self) -> None:
        self.model.train(self.saver.load_data(),self.saver.load_novelty())

    def is_stoped(self) -> bool:
        #print(ReadRoutine().sensors.is_stoped(),not False in ReadRoutine().sensors.is_stoped())
        return not False in ReadRoutine().sensors.is_stoped()


def main():

    blue = btConnection()
    list_devices = blue.dicover_devices()
    u = blue.connect_bt(list_devices, "LUVAMOUSE")
    while len(ReadRoutine().sensors.list_s[0].a[0]) == 0:
        print("waiting...")
        time.sleep(1)
    train_interface.main()


if __name__ == "__main__":
    main()
