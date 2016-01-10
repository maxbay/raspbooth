#!/usr/local/bin/python

import sys
import os
from PyQt4 import QtGui
sys.path.append(os.path.expanduser("~")+ '/Projects/raspbooth/src')
from ui_windows import Window

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())