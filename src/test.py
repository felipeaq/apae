from read_routine import *
from bt_connection import *


from data_saver import *
from glove_model import *


class Test:
    def __init__(self, file_data="../res/data.csv", file_phrase="../res/class.csv", one_file="../res/onefile.pkl", class_file="../res/multifile.pkl"):

        self.saver = DataSaver(file_data, file_phrase)
        self.__phrases = self.saver.load_phrase()
        self.model = GloveModel(one_file, class_file)

    def pred(self):
        if bool(sum(ReadRoutine().sensors.is_stoped())):
            return self.model.predict(self.preprocess_pred())
        else:
            return "moving"

    def preprocess_pred(self):
        sensor = ReadRoutine().sensors
        values = []
        for i in range(6):
            values.extend([sensor.list_s[i].a[0][-1],
                           sensor.list_s[i].a[1][-1],
                           sensor.list_s[i].a[2][-1]])

        return [values]

    def train(self) -> None:
        self.model.train(self.saver.load_data(),self.saver.load_novelty())


def main():
    t = Test()

    blue = btConnection()
    list_devices = blue.dicover_devices()
    u = blue.connect_bt(list_devices, "LUVAMOUSE")
    t.train()
    while len(ReadRoutine().sensors.list_s[0].a[0]) == 0:
        print("waiting...")
        time.sleep(1)
    while True:
        time.sleep(0.1)
        print(t.pred())


if __name__ == "__main__":
    main()
