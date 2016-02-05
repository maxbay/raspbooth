#!/usr/local/bin/python

import sys
import os
from PyQt4 import QtGui
sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
from ui_windows import startWindow

def main():
    app = QtGui.QApplication(sys.argv)
    window = startWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

