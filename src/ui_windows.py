#!/usr/local/bin/python

import sys
import os
from PyQt4 import QtGui, QtCore
sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
from capture import Capture


class startWindow(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.start()

    def start(self):
        self.capture = None

        self.start_button = QtGui.QPushButton('Start')
        self.cap = Capture()
        self.cap.setParent(self)
        self.cap.setWindowFlags(QtCore.Qt.Tool)
        self.start_button.clicked.connect(self.cap.startInit)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        self.setLayout(vbox)
        self.setWindowTitle('Control Panel')
        self.setGeometry(100,100,200,200)
        self.center()
        self.show()
        self.raise_()


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class saveWindow(QtGui.QWidget):

    def __init__(self):
        super(saveWindow, self).__init__()

        self.initUI()

    def initUI(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Email Entry',
            'Enter your email:')


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



