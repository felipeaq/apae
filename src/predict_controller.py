from glove_model import *
from data_saver import *
from read_routine import *
if __name__=="__main__":
    import predict_interface 
    from bt_connection import *

class PredictController:
    def __init__(self,one_file="../res/onefile.pkl", class_file="../res/multifile.pkl"):
        self.model = GloveModel(one_file, class_file)

    def predict(self):
        if bool(sum(ReadRoutine().sensors.is_stoped())):
            return self.model.predict(self.preprocess_pred())
        else:
            return [""]

    def preprocess_pred(self):
        sensor = ReadRoutine().sensors
        values = []
        for i in range(6):
            values.extend([sensor.list_s[i].a[0][-1],
                           sensor.list_s[i].a[1][-1],
                           sensor.list_s[i].a[2][-1]])

        return [values]


def main():

    blue = btConnection()
    list_devices = blue.dicover_devices()
    u = blue.connect_bt(list_devices, "LUVAMOUSE")
    while len(ReadRoutine().sensors.list_s[0].a[0]) == 0:
        print("waiting...")
        time.sleep(1)
    predict_interface.main()


if __name__=="__main__":
    main()