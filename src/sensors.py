from collections import deque
import numpy as np


class dequeSensor(deque):
    def __init__(self, iterable=(), maxlen=None):
        deque.__init__(self, iterable=iterable, maxlen=maxlen)
        self.real_len = 0
        self.last_acc_rate = 1

    def append(self, val):
        deque.append(self, val)
        self.real_len += 1

    def getxy(self, x):
        x = list(x)
        y = list(self)
        smallest = min(len(x), len(y))

        return x[0:smallest], y[0:smallest]


class Sensors:
    TOTAL_S = 6
    TOTAL_P = 6
    TO_DPS = 65
    RESIST = 32768
    IS_MOVING = 20  # TODO se mudar o DPS, essa variavel precisa mudar
    FILTER_SIZE = 10
    MAX_X = 512
    MAX_FFT = 10
    def __init__(self, maxlen):

        self.a = []
        self.g = []

        for i in range(Sensors.TOTAL_P//2):
            self.a.append(dequeSensor(maxlen=maxlen))
            self.g.append(dequeSensor(maxlen=maxlen))

    def append(self, a, g):

        for p, d in zip(a, self.a):

            d.append(p/Sensors.RESIST)

        for p, d in zip(g, self.g):
            d.append(p/Sensors.TO_DPS)

    def __repr__(self):
        return "\nax1: {}\n ax2: {}\n ax3: {}\n".format(
            self.a[0], self.a[1], self.a[2]
        )

    def abs_moving(self):
        s = 0
        # Se q quantidade de dados for maior que o tamanho do filtro
        if len(self.g[2]) > Sensors.FILTER_SIZE*3:
            for i in range(3):
                s = s + \
                    np.abs(
                        np.mean(list(self.g[i])[-Sensors.FILTER_SIZE:]) -
                        np.mean(list(self.g[i])[2*-Sensors.FILTER_SIZE:-Sensors.FILTER_SIZE]))

            return s
        return np.inf

    def is_stoped(self):
        return self.abs_moving() < Sensors.IS_MOVING


class SensorsSet():
    def __init__(self, ns, maxlen):
        self.list_s = []
        self.dic_s = {}
        for i in range(ns):
            sensor = Sensors(maxlen)
            self.list_s.append(sensor)
            self.dic_s["sensor"+str(i+1)] = sensor
        self.rtc = dequeSensor(maxlen=maxlen)

    def is_stoped(self):
        return [i.is_stoped() for i in self.list_s]

    def __repr__(self):
        s = ""
        for i in self.dic_s.items():
            s += str(i)+"\n"
        s += "('rtc', "+str(self.rtc)+")"+"\n"
        return s


def main():
    s1 = SensorsSet(6, Sensors.MAX_X)
    s1.append_at(2, [1, 2, 3])


if __name__ == "__main__":
    main()
