#!/usr/local/bin/python

import sys
import os
from PyQt4 import QtGui
sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
from capture import Capture

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window,self).__init__()

        self.initUI()

    def initUI(self):
        self.width =  500
        self.height = 500
        self.offset = 10

        self.setWindowTitle('Control Panel')

        self.capture = Capture()

        self.start_button = QtGui.QPushButton('Start',self)
        self.start_button.clicked.connect(self.capture.startCapture)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_button)


        self.setLayout(vbox)
        self.resize(self.height,self.width)
        self.center()
        self.show()
        self.raise_()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

