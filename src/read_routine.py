from sensors import *
import time


class ReadRoutine(object):
    __instance = None

    def __new__(cls):
        if ReadRoutine.__instance is None:
            total_s = 6
            ReadRoutine.__instance = object.__new__(cls)
            ReadRoutine.__instance.sensors = SensorsSet(total_s, Sensors.MAX_X)
            ReadRoutine.__instance.cycle_past = 0
            ReadRoutine.__instance.n_s = 6
            ReadRoutine.__instance.active_sensors = [False]*total_s
            ReadRoutine.__instance.sensor_pos = []
            ReadRoutine.__instance.FRTC = 32768.0
            ReadRoutine.__instance.rtc = 1
            ReadRoutine.__instance.start = time.time()
        return ReadRoutine.__instance

    def sync(self, sock):
        sync_sensor = False

        while not sync_sensor:
            #print ("a")
            cod1 = int.from_bytes(sock.recv(1), "little")
            # print("cod1:"+str(cod1))
            if cod1 == 255:

                cod2 = int.from_bytes(sock.recv(1), "little")
                # print("cod2:"+str(cod2))
                if (cod2 == 127):

                    cod3 = int.from_bytes(sock.recv(1), "little")
                    # print("cod3:"+str(cod3))
                    if cod3 == 254:
                        cod4 = int.from_bytes(sock.recv(1), "little")
                        # print("cod4:"+str(cod4))
                        if cod4 == 255:

                            sync_sensor = True

    def read_values(self, sock):

        active_sensors = [True]*self.n_s
        n_s = self.n_s
        # sock.recv(1)  # garbage
        #rtc = int.from_bytes(sock.recv(1)+sock.recv(1), "little")
        buffer = []
        a = []
        g = []
        sensor_pos = []
        self.rtc = time.time()-self.start
        for i in range(n_s):

            #pos = int.from_bytes(sock.recv(1), "little")-1
            # sock.recv(1)  # garbage

            # if (pos >= 6 or pos < 0):
            #    print("erro na sincronização lido posição:", pos, i)

            #    return

            #active_sensors[pos] = True
            sensor_pos.append(i)
            a.append([])
            g.append([])
            for _ in range(3):
                a[i].append(int.from_bytes(
                    sock.recv(1)+sock.recv(1), "little", signed=True))

            for _ in range(3):
                g[i].append(int.from_bytes(
                    sock.recv(1)+sock.recv(1), "little", signed=True))

        self.update_time()
        for i in range(n_s):

            self.sensors.list_s[i].append(a[i], g[i])

        self.active_sensors = active_sensors
        self.sensor_pos = sensor_pos
        #print (self.active_sensors)

    def update_time(self):

        self.sensors.rtc.append(self.rtc)


def main():

    ReadRoutine().read_values("a")
    ReadRoutine().update_time(2)
    ReadRoutine().update_time(4)
    ReadRoutine().update_time(2**15-1)
    ReadRoutine().update_time(1)
    #print (ReadRoutine().sensors)


if __name__ == "__main__":
    main()
