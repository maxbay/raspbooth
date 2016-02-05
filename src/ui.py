#!/usr/local/bin/python

import os
import sys
from PyQt4 import QtGui,QtCore
sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
from capture import Capture

class startWindow(QtGui.QWidget):

    def __init__(self):
        from capture import Capture

        QtGui.QWidget.__init__(self)

        self.start()

    def start(self):
        self.capturing = False

        self.x_display = int(str(QtGui.QDesktopWidget().availableGeometry()).strip("(").strip(")").split(",")[2].strip())
        self.y_display = int(str(QtGui.QDesktopWidget().availableGeometry()).strip("(").strip(")").split(",")[3].strip())

        self.cap = Capture(self.x_display,self.y_display)
        self.start_button = QtGui.QPushButton('Press Button To Start')
        self.start_button.setStyleSheet("font-size:150px;background-color:#FFFFFF; border: 15px solid #222222")
        self.start_button.setFixedSize(self.x_display-(self.x_display*.01),self.y_display-(self.y_display*.05))
        self.start_button.clicked.connect(self.exeCap)


        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        self.setLayout(vbox)
        self.setWindowTitle('Control Panel')
        #self.resize(self.x_display-(self.x_display*.01),self.y_display-(self.y_display*.05))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.showFullScreen()
        self.center()
        self.show()
        self.raise_()


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def exeCap(self):
        #TODO: Come up with relative path for capture.py
        if not self.cap.capturing:
            self.cap.startCapture()

        else:
            print("Currently Capturing")

class saveWindow(QtGui.QWidget):


    def __init__(self):
        super(saveWindow, self).__init__()

        self.initUI()

    def initUI(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Phone Number Entry',
            'Enter Your Phone Number (NOTE: Include Area Code):')


        if ok:
            print(text)

        """

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.center()
        self.show()
        self.raise_()


    def showDialog(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            self.le.setText(str(text))
    """

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def makeUsable(txt):
        pass




