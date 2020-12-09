from PyQt5 import QtCore, QtWidgets, uic
from read_routine import *
#from ob3d import Ob3D
#from pyqtgraph import PlotWidget
#import pyqtgraph as pg
import sys
import time
from threading import Thread, current_thread
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import animation
from matplotlib import pyplot as plt
import numpy as np
from save_routine import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('../interfaces/mainwindow.ui', self)
        self.button_update = self.findChild(
            QtWidgets.QPushButton, 'connectButton')

        self.button_add_gesture =
