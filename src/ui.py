#!/usr/local/bin/python

import os
import sys
import time
from PyQt4 import QtGui,QtCore
sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
from capture import Capture
from upload import Upload
from send_text import sendText

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


    def __init__(self,strip_path):
        super(saveWindow, self).__init__()

        self.strip_path = strip_path
        self.upld = Upload(self.strip_path)

        self.initUI()


    def initUI(self):


        self.number, ok = QtGui.QInputDialog.getText(self, 'Phone Number Entry',
            'Enter Your Phone Number (NOTE: Include Area Code):')

        if self.upld.link == None:
            self.upld.sendToImgur()
        if ok:
            while self.upld.link == None:

                time.sleep(.25)

            self.number = saveWindow.makeUsable(str(self.number))
            self.upld.link = str(self.upld.link)



            if saveWindow.makeUsable(self.number):
                self.sdtxt = sendText(self.upld.link,self.number)
            else:
                self.initUI


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
        NUMBERS = [str(x) for x in range(10)]

        if len(txt) == 10:
            txt = "1" + txt

        tmp_txt = ""
        for i in txt:
            if i in NUMBERS:
                tmp_txt += i

        txt = tmp_txt
        txt = "+" + txt

        return txt

    def checkKosher(txt):
        kosher = True
        if len(txt) != 12:
            kosher = False
        return kosher




