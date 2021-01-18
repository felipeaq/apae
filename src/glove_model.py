import pickle
import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import GridSearchCV
from model_saver import ModelSaver


class GloveModel:
    def __init__(self, one_file, class_file):
        self.saver = ModelSaver(one_file, class_file)
        self.one_class, self.multi_class = self.saver.load_all()
        self.one_file = one_file
        self.class_file = class_file
        
    def train(self, data,data_novelty):
        X, y = self.preprocessing(data)
        X_novelty,_ = self.preprocessing(data_novelty)
        print("start one")
        self.train_outlier(X,X_novelty)
        print("start two")
        self.train_class(X, y)
        print("end")
        self.saver.save_all(self.one_class, self.multi_class)

    def train_outlier(self, X,X_novelty):
        X_train=np.concatenate((X,X_novelty))
        y_train=[1]*len(X)+[-1]*len(X_novelty)
        tuned_parameters = [{'kernel': ['rbf'], 'gamma': ['scale'], 'nu': [.5,.7,.9]}]
        clf = GridSearchCV(OneClassSVM(), tuned_parameters, scoring="recall",verbose=0)
        clf.fit(X_train,y_train)
        self.one_class = clf

    def train_class(self, X, y):
        param_grid={'C': [0.1,1, 10, 100], 'gamma': ['scale'], 'kernel': ['rbf','linear'],'degree':[1,2,3,4]}
        self.multi_class =  GridSearchCV(SVC(),param_grid,refit=True,verbose=0)
        self.multi_class.fit(X,y)

    def predict(self, X):

        is_predict = self.predict_outlier(X)
        #print(is_predict)
        if is_predict[0] == -1:
            return [""]

        pred = self.predic_class(X)

        return pred

    def predict_outlier(self, X):
        return self.one_class.predict(X)

    def predic_class(self, X):
        return self.multi_class.predict(X)

    def load_model(self):
        pass

    def save_model(self):

        with open(self.class_file, "wb") as f:
            pickle.dump(self.multi_class, self.f)

    def preprocessing(self, data):

        other = []
        for i in range(6):
            other.extend(["gx%d" % i, "gy%d" % i, "gz%d" % i])
        other.append("category")
        other.append("timestamp")
        X = data.drop(other, axis=1).to_numpy()
        y = data["category"].values
        return X, y
