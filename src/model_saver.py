import pickle
from sklearn.svm import OneClassSVM
from sklearn.svm import SVC
import os.path


class ModelSaver:
    def __init__(self, one_file, class_file):
        self.one_file = one_file
        self.class_file = class_file

    def save_all(self, one_model, class_model):
        self.save(one_model, self.one_file)
        self.save(class_model, self.class_file)

    def load_all(self):
        return self.load(self.one_file), self.load(self.class_file)

    def save(self, model, file):
        with open(file, "wb") as f:
            pickle.dump(model, f)

    def load(self, file):
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                data = pickle.load(f)
            return data
