from sensors import *
import os.path
import pandas as pd


class DataSaver:
    def __init__(self, file_data, file_phrase,file_novelty="../res/noveltydata.csv"):
        self.file_data = file_data
        self.file_phrase = file_phrase
        self.file_novelty = file_novelty
        if not os.path.isfile(file_data):
            with open(file_data, "a") as f:
                f.write("timestamp;")
                for i in range(6):
                    f.write("ax{i};ay{i};az{i};gx{i};gy{i};gz{i};".format(i=i))
                f.write("category\n")

    def save_data(self, category, sensor):
        with open(self.file_data, "a") as f:
            f.write("{};".format(sensor.rtc[-1]))
            for i in range(6):
                f.write("{};{};{};{};{};{};".format(
                    sensor.list_s[i].a[0][-1],
                    sensor.list_s[i].a[1][-1],
                    sensor.list_s[i].a[2][-1],
                    sensor.list_s[i].g[0][-1],
                    sensor.list_s[i].g[1][-1],
                    sensor.list_s[i].g[2][-1]))
            f.write("{}\n".format(category))

    def save_phrase(self, categoty_list):
        text = "\n".join(categoty_list)
        with open(self.file_phrase, "w") as f:
            f.write(text)

    def update_phrase(self, old_phrase, new_phrase):
        df = pd.read_csv(self.file_data, sep=";")
        df["category"].replace(old_phrase, new_phrase, inplace=True)
        df.to_csv(self.file_data, index=False, sep=";")

    def delete_phrase(self, phrase_to_remove):

        df = pd.read_csv(self.file_data, sep=";")
        df = df[df["category"] != phrase_to_remove]
        df.to_csv(self.file_data, index=False, sep=";")

    def delete_last(self):
        df = pd.read_csv(self.file_data, sep=";")
        df.drop(df.tail(1).index, inplace=True)
        df.to_csv(self.file_data, index=False, sep=";")

    def load_phrase(self):

        with open(self.file_phrase, "r") as f:
            category_list = f.read().split("\n")

        return category_list

    def load_data(self):
        return pd.read_csv(self.file_data, sep=";")

    def load_novelty(self):
        return pd.read_csv(self.file_novelty, sep=";")