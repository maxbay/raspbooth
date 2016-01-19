#!/usr/local/bin/python

import sys
import os
import time
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore
import gtk, pygtk # pygtk is a gtk dependency

class Capture(QtGui.QWidget):
    def __init__(self):
        super(Capture, self).__init__()

        #video containing widget layout params
        self.video_frame = QtGui.QLabel()
        lay = QtGui.QVBoxLayout()
        lay.addWidget(self.video_frame)
        self.showMaximized()
        self.setLayout(lay)
        self.raise_()

        self.capturing = False

    def nextFrameSlot(self):

        ret, frame = self.cap.read()
        #frame = Capture.cropVideo(frame).astype(np.uint8)
        frame = Capture.cvt3ChanGray(frame).astype(np.uint8)
        frame = cv2.flip(frame, 1).astype(np.uint8)  #  flips to create mirrior image
        frame_copy = frame.astype(np.uint8)  #  unmanipulated copy for writing to disk
        frame = Capture.fullScreen(frame, self.dsp_w, self.dsp_h, self.bkrnd).astype(np.uint8)

        FONT = cv2.FONT_HERSHEY_COMPLEX # font
        SCALE = 2 # pt size
        THICKNESS = 5 # boldness factor

        cur_time = time.time() # time of instance, float
        cur_time_int = int(cur_time) # instance of time, discretized

        if cur_time > self.snap_lst[self.snap_count]: # advances snap count if current time > end of previous snap period
            self.snap_count += 1


        remaining_float = self.snap_lst[self.snap_count] - cur_time - 1 # time remaining in snap period, used for flash taking snap
        remaining = self.snap_lst[self.snap_count] - cur_time_int - 1 # int of time remaining, used for display

        if remaining <= 1: # displays remaining time on screen, but last two seconds "SMILE!" is displayed
            text = "SMILE!"
        else:
            text = str(remaining)

        if remaining_float > 0 and remaining_float < .25: # increase image values to make fake flash
            frame = np.array(np.add(frame.astype(np.uint8),self.FAUX_FLASH)).astype(np.uint8)

            if self.take_snap[self.snap_count]: # check if picture for this snap period needs to be taken, if so...

                if not os.path.exists(self.snaps_dir): # make dir for all 4 pictures if it has not been created yet
                    os.makedirs(self.snaps_dir)
                file_name = os.path.join(self.snaps_dir,"test_image{0}.tif".format(str(self.snap_count + 1)))
                cv2.imwrite(file_name,frame_copy) # write picture to disk
                self.take_snap[self.snap_count] = False #indicate that picture has been taken, and another for this snap period not needed
                print("Snap {0}".format(str(self.snap_count)))

                if self.snap_count == len(self.snap_lst) - 1: # breaks from while loop if snap count > scheduled snaps
                    self.deleteLater()
                    self.timer.stop()
                    self.capturing = False
                    sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
                    from ui_windows import saveWindow
                    self.hide()
                    self.svw = saveWindow()


        mid_x, mid_y = Capture.findCenter(frame,text,FONT,SCALE,THICKNESS) # find x, y values in image to display text
        cv2.putText(frame,text,(mid_x,mid_y),FONT,SCALE,(255,255,255),THICKNESS) # insert text at x, y

        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def startCapture(self):
        self.fps = 24
        self.cap = cv2.VideoCapture('/home/pi/Downloads/fgt.mp4') #self.cap = cv2.VideoCapture(0)

        self.dsp_w = gtk.gdk.screen_width()
        self.dsp_h = gtk.gdk.screen_height()
        self.bkrnd = np.zeros(shape=(self.dsp_h,self.dsp_w,3)).astype(np.uint8)

        self.DELAY = 6
        self.FAUX_FLASH = 50
        self.epoch_time = np.int(time.time())

        self.snap1 = self.epoch_time + self.DELAY + 5
        self.snap2 = self.snap1 + self.DELAY
        self.snap3 = self.snap2 + self.DELAY
        self.snap4 = self.snap3 + self.DELAY
        self.snap_lst = [self.snap1, self.snap2, self.snap3, self.snap4]
        self.take_snap = [True, True, True, True]
        self.snap_count = 0

        HOME_DIR = os.path.expanduser('~')
        self.snaps_dir = os.path.join(HOME_DIR,'Desktop/tmp_photos',str(self.epoch_time))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def startInit(self):
        if not self.capturing:
            self.capturing = True
            self.startCapture()
            self.show()
        else:
            print("Already capturing")


    def deleteLater(self):
        self.cap.release()
        #super(QtGui.QWidget, self).deleteLater()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def findCenter(array, text, FONT, SCALE, THICKNESS): # values for x, y such that text is centered
        x = np.shape(array)[1]
        y = np.shape(array)[0]

        half_width = np.int(np.round(cv2.getTextSize(text,FONT,SCALE,THICKNESS)[0][0]/2,0))
        mid_x = np.int(np.round(x/2,0) - half_width)
        mid_y = np.int(np.round(y/2,0))

        return mid_x, mid_y # x value, y value

    @staticmethod
    def cropVideo(array): #crops video to 3:4 ratio

        w = np.int(np.shape(array)[1])
        h = np.int(np.shape(array)[0])
        target_w = np.int((h * .75))
        start = np.int((w/2) - (target_w/2))
        end = np.int((w/2) + (target_w/2))

        array = array[:,start:end]

        return array

    @staticmethod
    def cvt3ChanGray(array):
        if len(np.shape(array)) == 3:
            if np.shape(array)[2] == 3:
                array[:,:,0] = array[:,:,1] = array[:,:,2]
            else:
                pass #TODO: Add conditional exit

        else:
            pass #TODO: Add conditional exit

        return array

    @staticmethod
    def fullScreen(array, dsp_w, dsp_h, bkrnd):

        w = np.int(np.shape(array)[1])
        h  = np.int(np.shape(array)[0])

        if h >= w:
            ratio = float(dsp_h) / float(h)
        elif w > h:
            ratio = float(dsp_w) / float(w)

        array = cv2.resize(array, (0, 0), fx = ratio, fy = ratio, interpolation = cv2.INTER_LINEAR)

        w  = np.int(np.shape(array)[1])
        h  = np.int(np.shape(array)[0])

        x_offset = np.int(np.round(np.shape(bkrnd)[1]/2,0)) - np.int(np.round(w/2,0))
        y_offset = np.int(np.round(np.shape(bkrnd)[0]/2,0)) - np.int(np.round(h/2,0))

        if w < np.shape(bkrnd)[1] and h < np.shape(bkrnd)[0]:

            bkrnd[y_offset:y_offset + h, x_offset:x_offset + w] = array
            array = bkrnd

        return array


