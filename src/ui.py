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
        QtGui.QWidget.__init__(self)

        self.start()

    def start(self):
        #screen dimentions
        self.x_display = int(str(QtGui.QDesktopWidget().availableGeometry()).strip("(").strip(")").split(",")[2].strip())
        self.y_display = int(str(QtGui.QDesktopWidget().availableGeometry()).strip("(").strip(")").split(",")[3].strip())

        #start button
        self.start_button = QtGui.QPushButton(self)
        self.start_button.setText('Press Button To Start')
        self.start_button.setStyleSheet("font-size:150px;background-color:#FFFFFF; border: 15px solid #222222")
        self.start_button.setFixedSize(self.x_display,self.y_display)

        #give start button powers
        self.cap = Capture(self.x_display,self.y_display)
        self.start_button.clicked.connect(self.exeCap)

        #size and show size button
        self.showFullScreen()
        self.center()
        self.show()
        self.raise_()


    def exeCap(self):
        if not self.cap.capturing:
            self.cap.startCapture()
            time.sleep(23)
            self.deleteLater
            self.saveInit()


        else:
            print("Currently Capturing")


    def saveInit(self):
        QtGui.QDialog.__init__(self)

        self.strip_path = self.cap.strip_path
        self.upld = Upload(self.strip_path)

        self.saveWindow()


    def saveWindow(self):

        #line edit widget
        self.le = QtGui.QLineEdit(self)
        self.le.setPlaceholderText("555-555-5555")
        self.le.setStyleSheet("font-size:150px;background-color:#FFFFFF; border: 5px solid #222222")
        self.le.setFixedWidth(self.x_display-(self.x_display*.05))

        #button widget
        self.pb = QtGui.QPushButton(self)
        self.pb.setText("Press 'Enter' to Submit")
        self.pb.setStyleSheet("font-size:100px;background-color:#FFFFFF") #; border: 2px solid #222222"
        self.pb.setFixedWidth(self.x_display-(self.x_display*.05))

        #regular expression restrictions
        reg_ex = QtCore.QRegExp("[0-9_]+")
        validator = QtGui.QRegExpValidator(reg_ex, self.le)
        self.le.setValidator(validator)

        #move widgets
        self.le.move(round(self.x_display*.025,0),(self.y_display*(1.0/3.0)-150))
        self.pb.move(round(self.x_display*.025,0),(self.y_display*(1.0/3.0)+50))

        #give widgets powers
        self.connect(self.pb, QtCore.SIGNAL("clicked()"),self.button_click)
        self.setWindowTitle("Learning")
        self.showFullScreen()
        self.raise_()
        self.show()

    def button_click(self):
        self.number = startWindow.makeUsable(str(self.le.text()))

        if startWindow.checkKosher(self.number):
            if self.upld.link == None:
                self.upld.sendToImgur()

            while self.upld.link == None:
                time.sleep(.25)

            self.upld.link = str(self.upld.link)
            sdtxt = sendText(self.upld.link,self.number)
            QtCore.QCoreApplication.instance().quit()

        else:
            redo = saveWindow(self.strip_path)

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

    @staticmethod
    def checkKosher(txt):
        kosher = True
        if len(txt) != 12:
            kosher = False
        return kosher



