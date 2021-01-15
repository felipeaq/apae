import bluetooth
import sys
import uuid
import threading
import time

from read_routine import *
from save_routine import *
from enum import Enum


from PyQt5 import QtWidgets
from INTERFACE_choose_app import Ui_MainWindow as ChooseAppWindow


class Status(Enum):
    STOP = 0
    WORKING = 1
    FINDPROBLEM = -1
    FINISHED = -2
    CONNECTING = 2


class btConnection:
    def __init__(self, name="ACELEROMETROS", port=0x1001):
        self.name = name
        self.sock = None
        self.port = port
        self.status = Status.STOP
        self.t = None

    def dicover_devices(self, duration=3):

        #print("performing inquiry...")
        nearby_devices = bluetooth.discover_devices(
            duration=duration, lookup_names=True, flush_cache=True, lookup_class=False)
        #print (nearby_devices)

        #print("found %d devices" % len(nearby_devices))
        return nearby_devices

    def __connect(self, addr):
        #print (addr)

        # Create the client socket
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, self.port))
        self.sock.settimeout(10)

        #print("connected.  type stuff")
        try:
            self.sock.send("U".encode())
            self.status = Status.WORKING
        except:
            self.status = Status.FINISHED

        while True:
            try:
                ReadRoutine().sync(self.sock)
                ReadRoutine().read_values(self.sock)
                SaveRoutine().save_routine()
            except bluetooth.btcommon.BluetoothError as err:
                print ("exceção no bluetooth")
                print (err)
                print ("*"*20)
                self.sock.close()
                self.status = Status.FINISHED
                return -2

            except KeyboardInterrupt:
                #print ("finalizando conexão...")
                self.sock.close()
                self.status = Status.FINISHED
                return 1

        self.sock.close()
        return 0

    def connect_bt(self, list_devices, name):
        # print(self)
        # print(list_devices)
        # print(name)
        # nearby_devices=self.dicover_devices()
        i=0
        try:
            #print ("select device...")
            for i, name_local, in zip(range(len(list_devices)), list_devices):
                #print(i, name_local[1], name, name_local == name)
                if name_local[1] == name:
                    break

            # i=int(input())
            self.status = Status.CONNECTING
        except IndexError:
            return -1
        if list_devices:
            addr = list_devices[i][0]
            self.t = threading.Thread(target=self.__connect, args=(addr,))
            self.t.start()
            return 0
        return -2


def main():
    b = btConnection()
    list_devices = b.dicover_devices()
    b.connect_bt(list_devices, "ACELEROMETROS", open("gambiarra_close", "w"))

    # test_acsition(b)


if __name__ == "__main__":
    main()
